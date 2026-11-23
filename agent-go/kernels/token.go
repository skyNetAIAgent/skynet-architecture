package kernels

import (
	"crypto/sha256"
	"encoding/binary"
	"math/big"
)

type shape struct { v, d, count int64 }

func token(p obj, units int64) job {
	fields(p, "shapes weights seed seeds", true)
	bounds := list(p["weights"], 2, 2)
	lo := number(bounds[0], -128, 127)
	hi := number(bounds[1], lo, 127)
	count := number(p["seeds"], 1, 1000)
	start := number(p["seed"], 0, 1 << 32 - count)
	shapes := axis(p["shapes"], 256, func(v any) shape {
		a := list(v, 3, 3)
		s := shape{number(a[0], 1, 150000), number(a[1], 1, 4096), number(a[2], 1, 64)}
		require(s.v * s.d * s.count <= 150000 * 4096 * 2, "too many logits")
		return s
	}, true)
	var table [256]int8
	for i := range table {
		table[i] = int8(lo + int64(i) * (hi - lo + 1) / 256)
	}
	point := grid(units, len(shapes), int(count))
	return func(unit int64) obj {
		i := point(unit)
		return certificate(shapes[i[0]], start + int64(i[1]), &table)
	}
}

func vector(dst []int8, seed int64, tag byte, index int64, table *[256]int8) {
	var block [13]byte
	block[0] = tag
	binary.BigEndian.PutUint32(block[1:], uint32(seed))
	binary.BigEndian.PutUint32(block[5:], uint32(index))
	for i := 0; i < len(dst); i += 32 {
		binary.BigEndian.PutUint32(block[9:], uint32(i / 32))
		hash := sha256.Sum256(block[:])
		for j := 0; j < min(32, len(dst) - i); j++ {
			dst[i + j] = table[hash[j]]
		}
	}
}

func abs(x int64) int64 {
	if x < 0 {
		return -x
	}
	return x
}

func dot(a, b []int8) int64 {
	var out int64
	for i, x := range a {
		out += int64(x) * int64(b[i])
	}
	return out
}

func distance(a, b []int8) int64 {
	var out int64
	for i, x := range a {
		out += abs(int64(x) - int64(b[i]))
	}
	return out
}

type leaf struct { centre []int8; radius, first, end int64 }

func certificate(s shape, seed int64, table *[256]int8) obj {
	row := make([]int8, s.d)
	root := make([]int8, s.d)
	vector(root, seed, 'W', 0, table)
	queries := make([][]int8, s.count)
	scores, winners := make([]int64, s.count), make([]int64, s.count)
	for j := range queries {
		queries[j] = make([]int8, s.d)
		vector(queries[j], seed, 'h', int64(j), table)
	}
	var leaves []leaf
	var radius int64
	for first := int64(0); first < s.v; first += 128 {
		l := leaf{centre: make([]int8, s.d), first: first, end: min(s.v, first + 128)}
		for i := first; i < l.end; i++ {
			vector(row, seed, 'W', i, table)
			if i == first {
				copy(l.centre, row)
			}
			l.radius = max(l.radius, distance(row, l.centre))
			if first == 0 {
				radius = l.radius
			} else {
				radius = max(radius, distance(row, root))
			}
			for j, h := range queries {
				score := dot(row, h)
				if i == 0 || score > scores[j] {
					scores[j], winners[j] = score, i
				}
			}
		}
		leaves = append(leaves, l)
	}
	var rows, checks int64
	for j, h := range queries {
		claim := winners[j]
		vector(row, seed, 'W', claim, table)
		score := dot(row, h)
		winner, best := claim, score
		read, bounds := int64(1), int64(1)
		var norm int64
		for _, x := range h {
			norm = max(norm, abs(int64(x)))
		}
		if dot(root, h) + radius * norm >= score {
			for _, l := range leaves {
				bounds++
				if dot(l.centre, h) + l.radius * norm < score {
					continue
				}
				for i := l.first; i < l.end; i++ {
					if i == claim {
						continue
					}
					vector(row, seed, 'W', i, table)
					x := dot(row, h)
					if x > best || (x == best && i < winner) {
						best, winner = x, i
					}
					read++
				}
			}
		}
		require(winner == claim, "certificate disagrees with argmax")
		rows += read
		checks += read * s.d + bounds * (s.d + 1)
	}
	full := s.v * s.d * s.count
	return obj{"kernel": "token-certificate@1", "V": s.v, "d": s.d, "vectors": s.count, "seed": seed, "winners": winners,
		"rows_read": rows, "verify_mults": checks, "full_mults": full, "verify_over_full": ratio(big.NewRat(checks, full))}
}
