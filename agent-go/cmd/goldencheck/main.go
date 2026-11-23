// Command goldencheck recomputes reference results (JSON lines from the Python agent)
// with the Go kernels in parallel and reports any unit whose canonical result differs.
//
//	goldencheck -workers 32 golden_list1.jsonl golden_list2.jsonl
package main

import (
	"bufio"
	"compress/gzip"
	"flag"
	"fmt"
	"io"
	"os"
	"strings"
	"sync"
	"sync/atomic"
	"time"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/canon"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/kernels"
)

func main() {
	workers := flag.Int("workers", 4, "parallel computations")
	flag.Parse()
	type row struct{ line string }
	jobs := make(chan string, 64)
	var done, bad int64
	var wg sync.WaitGroup
	start := time.Now()
	for i := 0; i < *workers; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for line := range jobs {
				v, err := canon.Parse([]byte(line))
				if err != nil {
					panic(err)
				}
				r := v.(canon.Object)
				name := r["kernel"].(string)
				unit, _ := canon.Int64(r["unit"])
				units, _ := canon.Int64(r["units"])
				ver, _ := canon.Int64(r["kernel_version"])
				t0 := time.Now()
				got, err := kernels.Run(name, ver, r["params"].(canon.Object), unit, units)
				h := ""
				if err == nil {
					h, err = canon.Hash(got)
				}
				n := atomic.AddInt64(&done, 1)
				if err != nil || h != r["result_sha256"] {
					atomic.AddInt64(&bad, 1)
					fmt.Printf("MISMATCH %s unit %d: %v %s\n", r["task"], unit, err, h)
				} else if n%50 == 0 {
					fmt.Printf("ok %d (%s unit %d in %s)\n", n, r["task"], unit, time.Since(t0).Round(time.Millisecond))
				}
			}
		}()
	}
	for _, path := range flag.Args() {
		f, err := os.Open(path)
		if err != nil {
			panic(err)
		}
		var in io.Reader = f
		if strings.HasSuffix(path, ".gz") {
			if in, err = gzip.NewReader(f); err != nil {
				panic(err)
			}
		}
		s := bufio.NewScanner(in)
		s.Buffer(make([]byte, 1<<20), 64<<20)
		for s.Scan() {
			jobs <- s.Text()
		}
		f.Close()
	}
	close(jobs)
	wg.Wait()
	fmt.Printf("checked %d units, %d mismatches, %s\n", done, bad, time.Since(start).Round(time.Second))
	if bad > 0 {
		os.Exit(1)
	}
}
