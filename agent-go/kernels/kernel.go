// Package kernels runs built-in version 1 computations on strict JSON data.
package kernels

import (
	"fmt"
	"math/big"
	"math/bits"
	"strings"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/canon"
)

type obj = canon.Object
type job func(unit int64) obj
type builder func(params obj, units int64) job

var registry = map[string]builder{
	"selftest": selftest, "lottery-b": lottery, "exit-scam-a": exitScam,
	"apprentice-seats": seats, "exit-campaign-b": campaign,
	"lottery-adaptive": adaptive, "token-certificate": token,
	"t4-scale": t4Scale, "exam-thresholds": examThresholds,
	"merge-attribution": mergeAttribution, "verification-enumerations": verificationEnumerations,
}

func Supported(name string, version int64) bool {
	return version == 1 && registry[name] != nil
}

// Builders report malformed nested fields through a private, typed error.
// The API converts only these validation errors; programming errors propagate.
type invalid string

func (e invalid) Error() string {
	return string(e)
}

func require(ok bool, msg string) {
	if !ok {
		panic(invalid(msg))
	}
}

func catch(err *error) {
	if v := recover(); v != nil {
		if e, ok := v.(invalid); ok {
			*err = e
		} else {
			panic(v)
		}
	}
}

func compile(name string, version int64, p obj, units int64) job {
	require(Supported(name, version), "unsupported kernel or version")
	require(p != nil && units >= 1 && units <= 1000000, "invalid parameters or unit count")
	return registry[name](p, units)
}

func Validate(name string, version int64, params obj, units int64) (err error) {
	defer catch(&err)
	compile(name, version, params, units)
	return nil
}

func Run(name string, version int64, params obj, unit, units int64) (result obj, err error) {
	defer catch(&err)
	require(unit >= 0 && unit < units, "unit outside task")
	return compile(name, version, params, units)(unit), nil
}

func fields(p obj, allowed string, exact bool) {
	keys := strings.Fields(allowed)
	if exact {
		require(len(p) == len(keys), "missing parameter")
	}
	for k := range p {
		found := false
		for _, key := range keys {
			if key == k {
				found = true
				break
			}
		}
		require(found, "unknown parameter " + k)
	}
}

func get(p obj, k string, fallback any) any {
	if v, ok := p[k]; ok {
		return v
	}
	return fallback
}

func number(v any, lo, hi int64) int64 {
	n, ok := canon.Int64(v)
	require(ok && n >= lo && n <= hi, fmt.Sprintf("expected integer in [%d,%d]", lo, hi))
	return n
}

func list(v any, lo, hi int) []any {
	a, ok := v.([]any)
	require(ok && len(a) >= lo && len(a) <= hi, "invalid array length or type")
	return a
}

func axis[T comparable](v any, limit int, parse func(any) T, unique bool) []T {
	a := list(v, 1, limit)
	values := make([]T, len(a))
	seen := map[T]bool{}
	for i, value := range a {
		values[i] = parse(value)
		require(!unique || !seen[values[i]], "duplicate axis value")
		seen[values[i]] = true
	}
	return values
}

func ints(v any, lo, hi int64, limit int) []int64 {
	return axis(v, limit, func(x any) int64 { return number(x, lo, hi) }, true)
}

type pair struct { n, d int64 }

func fraction(v any, maxDen int64, zero, proper, reduce bool) pair {
	a := list(v, 2, 2)
	d := number(a[1], 1, maxDen)
	lo, hi := int64(1), d
	if zero {
		lo = 0
	}
	if proper {
		hi--
	}
	n := number(a[0], lo, hi)
	if reduce {
		r := big.NewRat(n, d)
		n, d = r.Num().Int64(), r.Denom().Int64()
	}
	return pair{n, d}
}

func shares(v any) []pair {
	return axis(v, 256, func(x any) pair { return fraction(x, 1000, true, false, true) }, true)
}

func (p pair) rat() *big.Rat {
	return big.NewRat(p.n, p.d)
}

func (p pair) String() string {
	return fmt.Sprintf("%d/%d", p.n, p.d)
}

func ratio(r *big.Rat) string {
	return r.Num().String() + "/" + r.Denom().String()
}

func highest(a []int64) int64 {
	v := a[0]
	for _, n := range a[1:] {
		v = max(v, n)
	}
	return v
}

func denBits(a []pair) int64 {
	var n int
	for _, x := range a {
		n = max(n, bits.Len64(uint64(x.d)))
	}
	return int64(n)
}

// Decode a mixed-radix ordinal, with the last axis varying fastest.
func grid(units int64, lengths ...int) func(int64) []int {
	size := int64(1)
	for _, n := range lengths {
		size *= int64(n)
	}
	require(size == units, "units must equal grid size")
	return func(unit int64) []int {
		out := make([]int, len(lengths))
		for i := len(out) - 1; i >= 0; i-- {
			out[i] = int(unit % int64(lengths[i]))
			unit /= int64(lengths[i])
		}
		return out
	}
}

func pow(base *big.Int, exp int64) *big.Int {
	return new(big.Int).Exp(base, big.NewInt(exp), nil)
}

func times(a, b *big.Int) *big.Int {
	return new(big.Int).Mul(a, b)
}

func comb(n, k int64) *big.Int {
	return new(big.Int).Binomial(n, k)
}

