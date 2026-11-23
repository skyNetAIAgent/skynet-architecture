package main

import (
	"encoding/base64"
	"errors"
	"fmt"
	"io"
	"math"
	"net/url"
	"os"
	"regexp"
	"strconv"
	"strings"
	"unicode"
	"unicode/utf8"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/sig"
)

const apkReleaseURL = "https://github.com/skyNetAIAgent/skynet-architecture/releases/download/"
const apkMetadataLimit = 16 << 10

var apkPathPart = regexp.MustCompile(`^([A-Za-z0-9._~+-]|%[0-9a-fA-F]{2})+$`)
var apkDigest = regexp.MustCompile(`^[0-9a-f]{64}$`)

func printable(s string) bool {
	return utf8.ValidString(s) && strings.IndexFunc(s, func(r rune) bool { return !unicode.IsPrint(r) }) < 0
}

func validAPKURL(address string) bool {
	path, ok := strings.CutPrefix(address, apkReleaseURL)
	parts := strings.Split(path, "/")
	if !ok || len(parts) != 2 {
		return false
	}
	for i, part := range parts {
		decoded, err := url.PathUnescape(part)
		if err != nil || !apkPathPart.MatchString(part) || !printable(decoded) || strings.Contains(decoded, `\`) {
			return false
		}
		// A tag may contain an encoded slash. Traversal and empty segments are forbidden.
		for _, segment := range strings.Split(decoded, "/") {
			if segment == "" || segment == "." || segment == ".." {
				return false
			}
		}
		if i == 1 && !strings.HasSuffix(strings.ToLower(decoded), ".apk") {
			return false
		}
	}
	return true
}

func verifyAPKManifest(raw, signature []byte, installed, sdk int64) (bool, error) {
	if len(raw) > apkMetadataLimit || len(signature) > apkMetadataLimit {
		return false, errors.New("APK metadata too large")
	}
	doc, err := sig.Document(raw, signature, nil)
	if err != nil {
		return false, err
	}
	return apkOffer(doc, installed, sdk)
}

func apkOffer(doc Object, installed, sdk int64) (bool, error) {
	for field, limit := range map[string]int64{"format": 1, "version_code": math.MaxInt32, "size": math.MaxInt64, "min_sdk": math.MaxInt32} {
		n, ok := doc[field].(int64) // canon.Parse preserves the JSON number type
		if !ok || n < 1 || n > limit {
			return false, fmt.Errorf("invalid APK %s", field)
		}
	}
	for field, limit := range map[string]int{"version_name": 64, "notes": 500} {
		s, ok := doc[field].(string)
		if !ok || strings.TrimSpace(s) == "" || utf8.RuneCountInString(s) > limit || !printable(s) {
			return false, fmt.Errorf("invalid APK %s", field)
		}
	}
	digest, _ := doc["sha256"].(string)
	address, _ := doc["url"].(string)
	if !apkDigest.MatchString(digest) || !validAPKURL(address) {
		return false, errors.New("invalid APK digest or release URL")
	}
	return doc["version_code"].(int64) > installed && doc["min_sdk"].(int64) <= sdk, nil
}

// APK metadata is public. Pass the detached signature as one Base64 argument and
// pipe the original manifest bytes on stdin. Status 0 means offer, 3 means valid
// but inapplicable, and all other statuses are errors.
func verifyAPKCommand(args []string) (int, error) {
	if len(args) != 3 {
		return 2, errors.New("usage: verify-apk-manifest INSTALLED_VERSION_CODE SDK SIGNATURE_BASE64 < latest.json")
	}
	installed, err := strconv.ParseInt(args[0], 10, 64)
	if err != nil || installed < 0 {
		return 2, errors.New("invalid installed version code")
	}
	sdk, err := strconv.ParseInt(args[1], 10, 32)
	if err != nil || sdk <= 0 {
		return 2, errors.New("invalid Android SDK level")
	}
	if len(args[2]) > base64.StdEncoding.EncodedLen(apkMetadataLimit) {
		return 1, errors.New("APK signature too large")
	}
	signature, err := base64.StdEncoding.DecodeString(args[2])
	if err != nil {
		return 1, err
	}
	raw, err := io.ReadAll(io.LimitReader(os.Stdin, apkMetadataLimit+1))
	if err != nil {
		return 1, err
	}
	offer, err := verifyAPKManifest(raw, signature, installed, sdk)
	if err != nil {
		return 1, err
	}
	if !offer {
		return 3, nil
	}
	return 0, nil
}
