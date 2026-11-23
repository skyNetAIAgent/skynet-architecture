//go:build !windows

package records

import "os"

func publishSeed(from, to string) error { return os.Link(from, to) }
