package update

import (
	"errors"
	"path/filepath"
	"reflect"
	"time"
)

type trial struct {
	Confirmed bool `json:"confirmed"`
	Seq       int  `json:"seq"`
	Failures  int  `json:"failures"`
}

// RecordExit serializes trial accounting and rollback with activation. Missing files
// trigger an immediate rollback. One-shot command failures are handled by the caller.
func RecordExit(home string, observed Current, fast, missing bool) (bool, error) {
	return recordExit(home, observed, fast, missing, nil)
}
func recordExit(home string, observed Current, fast, missing bool, keys []string) (bool, error) {
	changed := false
	err := Locked(home, func() error {
		c, h, err := state(home)
		if err != nil {
			return err
		}
		if !reflect.DeepEqual(c, observed) {
			changed = true
			return nil
		}
		var t trial
		if err = load(filepath.Join(home, "launch-trial.json"), &t); err != nil {
			return err
		}
		if t.Seq != c.Seq || !fast {
			t = trial{Seq: c.Seq, Confirmed: !fast && !missing}
		}
		if fast {
			t.Failures++
		}
		if err = save(home, "launch-trial.json", t); err != nil {
			return err
		}
		if !missing && t.Failures < 3 {
			return nil
		}
		if c.Previous == nil {
			return errors.New("no previous release to restore")
		}
		if _, err = verifiedPath(home, *c.Previous, keys); err != nil {
			return err
		}
		if !contains(h.Bad, c.Seq) {
			h.Bad = append(h.Bad, c.Seq)
		}
		if err = save(home, "release-history.json", h); err != nil {
			return err
		}
		if err = save(home, "max_seq.json", h.Seq); err != nil {
			return err
		}
		if err = save(home, "bad_seqs.json", h.Bad); err != nil {
			return err
		}
		restored := Current{Entry: *c.Previous, Activated: time.Now().Unix(), RolledBack: c.Seq}
		if err = save(home, "current.json", restored); err != nil {
			return err
		}
		changed = true
		return nil
	})
	return changed, err
}

// Confirm records a completed work-loop step, including normal offline waiting.
func Confirm(home string, seq int) error {
	return Locked(home, func() error {
		c, err := CurrentVersion(home)
		if err != nil || c.Runtime != "go" || c.Seq != seq {
			return err
		}
		return save(home, "launch-trial.json", trial{Seq: seq, Confirmed: true})
	})
}

// Recover finishes a partially committed bad-release rollback and restores the legacy watermark.
func Recover(home string) error {
	// A running installation can continue using its current release during a download.
	c, h, err := state(home)
	if err != nil {
		return err
	}
	var floor int
	if err = load(filepath.Join(home, "max_seq.json"), &floor); err != nil {
		return err
	}
	if floor >= h.Seq && !contains(h.Bad, c.Seq) {
		return nil
	}
	return Locked(home, func() error {
		c, h, err := state(home)
		if err != nil {
			return err
		}
		var floor int
		if err = load(filepath.Join(home, "max_seq.json"), &floor); err != nil {
			return err
		}
		if floor < h.Seq {
			if err = save(home, "max_seq.json", h.Seq); err != nil {
				return err
			}
		}
		if !contains(h.Bad, c.Seq) {
			return nil
		}
		if c.Previous == nil {
			return errors.New("failed release has no previous version")
		}
		if _, err = VerifiedPath(home, *c.Previous); err != nil {
			return err
		}
		if err = save(home, "bad_seqs.json", h.Bad); err != nil {
			return err
		}
		return save(home, "current.json", Current{Entry: *c.Previous, Activated: time.Now().Unix(), RolledBack: c.Seq})
	})
}
