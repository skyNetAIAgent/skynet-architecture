//go:build !windows && !linux

package records

import "os"

func publishSeed(from, to string) error { return os.Link(from, to) }
