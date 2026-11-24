// Board report drafts have no legacy compute "record" field. This also keeps
// Python agents sharing the profile from picking them up as compute results.
package outbox

import (
	"crypto/ed25519"
	"crypto/sha256"
	"encoding/hex"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"time"
	"unicode"
	"unicode/utf8"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/ai"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/config"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/records"
)

const reportSummary = "machine-generated, unverified"

var taskIDPattern = regexp.MustCompile("^[0-9a-f]{64}$")

func reportName(taskID string) string { return "report-" + taskID + ".json" }

func IsReportName(name string) bool {
	id := strings.TrimSuffix(strings.TrimPrefix(name, "report-"), ".json")
	return taskIDPattern.MatchString(id) && reportName(id) == name
}

func reportHash(o Object) string {
	return fmt.Sprintf("%x", sha256.Sum256([]byte(config.Str(o["text"]))))
}

func dismissedPath(home, name string) string { return filepath.Join(home, "net", "ai-dismissed", name) }

// ReportSeen also covers dismissals after the draft has left the outbox.
func ReportSeen(home, taskID string) (bool, error) {
	if !taskIDPattern.MatchString(taskID) {
		return false, errors.New("invalid task id")
	}
	name := reportName(taskID)
	for _, path := range []string{filepath.Join(home, "outbox", name), dismissedPath(home, name), filepath.Join(home, "sent", name)} {
		_, err := os.Stat(path)
		if !errors.Is(err, os.ErrNotExist) {
			return err == nil, err
		}
	}
	return false, nil
}

// PruneDismissed removes refusal markers for tasks that are no longer on the
// board. Markers are only consulted for tasks present on the board (the
// eligibility check looks at the board first), so stale markers are dead
// weight: dropping them bounds net/ai-dismissed by the current board size.
// A task that leaves the board and later reappears can be drafted again,
// which is acceptable: the draft still requires human approval.
func PruneDismissed(home string, onBoard map[string]bool) error {
	dir := filepath.Join(home, "net", "ai-dismissed")
	names, err := Names(home, filepath.Join("net", "ai-dismissed"))
	if err != nil {
		return err
	}
	for _, name := range names {
		id := strings.TrimSuffix(strings.TrimPrefix(name, "report-"), ".json")
		if reportName(id) != name || onBoard[id] {
			continue
		}
		if err := os.Remove(filepath.Join(dir, name)); err != nil && !errors.Is(err, os.ErrNotExist) {
			return err
		}
	}
	return nil
}

func checkConfiguredText(home, text string) error {
	cfg, err := config.Load(home)
	if err != nil {
		return err
	}
	return checkReportText(text, config.Num(config.Get(cfg, "ai.max_answer_chars"), ai.MaxAnswerChars))
}

func checkReportText(text string, maxChars int64) error {
	if !utf8.ValidString(text) || strings.TrimSpace(text) == "" || int64(utf8.RuneCountInString(text)) > maxChars {
		return fmt.Errorf("report text must contain 1 to %d UTF-8 characters", maxChars)
	}
	for i, r := range text {
		if r == '\r' && i+1 < len(text) && text[i+1] == '\n' {
			continue
		}
		if (unicode.IsControl(r) && r != '\n' && r != '\t') || unicode.Is(unicode.Bidi_Control, r) || r == '\u2028' || r == '\u2029' {
			return errors.New("report text contains a display control character")
		}
	}
	return nil
}

// SaveReportDraft and the review mutations are called with the profile state lock held.
func SaveReportDraft(home, taskID, text string) (string, error) {
	seen, err := ReportSeen(home, taskID)
	if err != nil {
		return "", err
	}
	if seen {
		return "", errors.New("task already drafted or dismissed")
	}
	if err := checkConfiguredText(home, text); err != nil {
		return "", err
	}
	names, err := Names(home, "outbox")
	if err != nil {
		return "", err
	}
	if len(names) >= Limit {
		return "", errors.New("the outbox is full")
	}
	name := reportName(taskID)
	o := Object{"kind": "report", "task": taskID, "summary": reportSummary, "text": text, "approved": false, "created": time.Now().Unix()}
	return name, config.Write(filepath.Join(home, "outbox", name), o)
}

func readReport(home, name string) (Object, error) {
	if !IsReportName(name) {
		return nil, errors.New("invalid report draft name")
	}
	o, err := config.Read(filepath.Join(home, "outbox", name))
	if err != nil {
		return nil, err
	}
	if o["kind"] != "report" || o["summary"] != reportSummary || name != reportName(config.Str(o["task"])) {
		return nil, errors.New("draft target or machine-generated label does not match")
	}
	return o, nil
}

func ReviewReport(home, name string) (Object, string, error) {
	o, err := readReport(home, name)
	if err != nil {
		return nil, "", err
	}
	if err = checkReportText(config.Str(o["text"]), ai.MaxAnswerChars); err != nil {
		return nil, "", err
	}
	return o, reportHash(o), nil
}

func EditReport(home, name, text string) error {
	o, err := readReport(home, name)
	if err != nil {
		return err
	}
	if o["sending"] == true {
		return errors.New("publication already started for this report")
	}
	if err := checkConfiguredText(home, text); err != nil {
		return err
	}
	o["text"], o["approved"] = text, false
	delete(o, "approved_sha256")
	delete(o, "net_record")
	return config.Write(filepath.Join(home, "outbox", name), o)
}

// Approval freezes the exact text, task and machine-generated label in a signed
// report. No board journal or transport queue is involved until Flush.
func ApproveReport(home, name, hash string) error {
	o, err := readReport(home, name)
	if err != nil {
		return err
	}
	if hash != reportHash(o) {
		return errors.New("review the current text with outbox show before approving")
	}
	if err := checkConfiguredText(home, config.Str(o["text"])); err != nil {
		return err
	}
	if reportApproved(o) {
		return nil
	}
	if o["sending"] == true {
		return errors.New("publication already started for this report")
	}
	seed, err := records.LoadSeed(home, true)
	if err != nil {
		return err
	}
	env, err := records.Make(seed, "report", Object{"task": o["task"], "summary": reportSummary, "text": o["text"]}, time.Now().Unix())
	if err != nil {
		return err
	}
	o["approved_sha256"], o["approved"], o["net_record"] = hash, true, env
	return config.Write(filepath.Join(home, "outbox", name), o)
}

// The name binds the task at review time. The envelope has to carry precisely
// those three reviewed fields (even a valid optional "revises" changes meaning).
func reportApproved(o Object) bool {
	body := config.Obj(config.Obj(o["net_record"])["body"])
	p := config.Obj(body["payload"])
	return o["approved"] == true && o["approved_sha256"] == reportHash(o) &&
		taskIDPattern.MatchString(config.Str(o["task"])) && o["summary"] == reportSummary &&
		body["type"] == "report" && len(p) == 3 && p["summary"] == reportSummary &&
		p["task"] == config.Str(o["task"]) && p["text"] == config.Str(o["text"])
}

func prepareReport(home string, e Entry, seed []byte) error {
	body := config.Obj(config.Obj(e.Data["net_record"])["body"])
	key := ed25519.NewKeyFromSeed(seed)
	if body["author"] != hex.EncodeToString(key.Public().(ed25519.PublicKey)) {
		return errors.New("approved report signature belongs to a different device")
	}
	// After a lost acknowledgement, another receiver may already have this
	// record. Edits must not turn an uncertain delivery into a second record.
	if e.Data["sending"] != true {
		e.Data["sending"] = true
		return config.Write(filepath.Join(home, "outbox", e.Name), e.Data)
	}
	return nil
}

func DropReport(home, name string) error {
	o, err := readReport(home, name)
	if err != nil {
		return err
	}
	// Persist the dismissal before removing the draft. A crash between the
	// two operations cannot recreate it on the next poll or publish it.
	if err = config.Write(dismissedPath(home, name), Object{"task": o["task"]}); err != nil {
		return err
	}
	return os.Remove(filepath.Join(home, "outbox", name))
}
