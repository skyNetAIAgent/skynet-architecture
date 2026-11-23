package update

import (
	"encoding/json"
	"errors"
	"fmt"
	"io/fs"
	"os"
	"path"
	"path/filepath"
	"strings"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/sig"
)

// A launcher already running Python 0.3 imports this module after exit 75.
const Adapter = "import os\nimport subprocess\nimport sys\n\n\ndef main(argv=None):\n    home = os.environ['SKYNET_AGENT_HOME']\n    exe = 'skynet-agent.exe' if os.name == 'nt' else 'skynet-agent'\n    return subprocess.call([os.path.join(home, exe), 'launch'] + (sys.argv[1:] if argv is None else argv))\n"

var adapters = map[string][]byte{"skynet_agent/__init__.py": {}, "skynet_agent/cli.py": []byte(Adapter)}

func checkedTree(dir string, files map[string]File) error {
	if err := directory(dir); err != nil {
		return err
	}
	dirs := map[string]bool{".": true}
	for name := range files {
		if !fs.ValidPath(name) || strings.ContainsAny(name, `\:`) {
			return fmt.Errorf("unsafe path %q", name)
		}
		for p := path.Dir(name); p != "."; p = path.Dir(p) {
			dirs[p] = true
		}
	}
	count := 0
	err := filepath.WalkDir(dir, func(p string, de fs.DirEntry, err error) error {
		if err != nil {
			return err
		}
		rel, err := filepath.Rel(dir, p)
		if err != nil {
			return err
		}
		name := filepath.ToSlash(rel)
		if de.IsDir() && dirs[name] {
			return directory(p)
		}
		if name == "release.json" || name == "release.json.sig" {
			return regular(p)
		}
		meta, ok := files[name]
		if !ok {
			return fmt.Errorf("unexpected entry %s", name)
		}
		if meta.Size < 0 || meta.Size > maxBinary {
			return errors.New("invalid file size")
		}
		b, err := read(p, meta.Size)
		if err != nil {
			return err
		}
		if !matches(b, meta) {
			return fmt.Errorf("signed size or hash mismatch for %s", name)
		}
		count++
		return nil
	})
	if err == nil && count != len(files) {
		return errors.New("incomplete release tree")
	}
	return err
}
func manifestBytes(dir string) ([]byte, []byte, error) {
	if err := directory(dir); err != nil {
		return nil, nil, err
	}
	raw, err := read(filepath.Join(dir, "release.json"), maxManifest)
	if err != nil {
		return nil, nil, err
	}
	signature, err := read(filepath.Join(dir, "release.json.sig"), 16384)
	return raw, signature, err
}
func (d document) files(compat bool) (map[string]File, error) {
	t, ok := d.Targets[Platform()]
	if !ok {
		return nil, errors.New("no target for " + Platform())
	}
	files := map[string]File{t.Name: t.File}
	if compat {
		for name, b := range adapters {
			f, ok := d.Compat[name]
			if !ok || !matches(b, f) {
				return nil, errors.New("missing or changed bridge adapter")
			}
			files[name] = f
		}
	}
	return files, nil
}
func verify(dir string, e Entry, keys []string) error {
	raw, signature, err := manifestBytes(dir)
	if err != nil {
		return err
	}
	if e.Digest != "" && e.Digest != digest(raw) {
		return errors.New("manifest fingerprint changed")
	}
	if e.Runtime == "go" {
		d, err := parse(raw, signature, keys)
		if err != nil {
			return err
		}
		if d.Seq != e.Seq || d.Version != e.Version {
			return errors.New("wrong Go release")
		}
		files, err := d.files(e.Compat)
		if err != nil {
			return err
		}
		return checkedTree(dir, files)
	}
	if _, err := sig.Document(raw, signature, keys); err != nil {
		return err
	}
	var r struct {
		Format, Seq int
		Version     string
		Files       map[string]File
	}
	if err := json.Unmarshal(raw, &r); err != nil {
		return err
	}
	if r.Format != 1 || r.Seq != e.Seq || r.Version != e.Version || r.Files["skynet_agent/cli.py"].SHA256 == "" {
		return errors.New("wrong Python release")
	}
	return checkedTree(dir, r.Files)
}
func VerifiedPath(home string, e Entry) (string, error) {
	return verifiedPath(home, e, nil)
}

// VerifyCandidate checks the signed release next to the executable against its build metadata.
func VerifyCandidate(dir, version string, seq int) error {
	_, err := os.Lstat(filepath.Join(dir, "skynet_agent"))
	if err != nil && !errors.Is(err, os.ErrNotExist) {
		return err
	}
	return verify(dir, Entry{Runtime: "go", Seq: seq, Version: version, Compat: err == nil}, nil)
}
