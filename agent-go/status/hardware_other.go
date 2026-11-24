//go:build !linux && !windows

package status

import "context"

func Hardware(ctx context.Context) (string, int64, []GPU) {
	return "", 0, nvidiaGPUs(ctx)
}
