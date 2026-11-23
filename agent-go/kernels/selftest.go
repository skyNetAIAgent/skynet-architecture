package kernels

import (
	"crypto/ed25519"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"math/big"
)

type matrix [32][32]int64

func randomMatrix(seed uint64) matrix {
	var m matrix
	for i := range m {
		for j := range m[i] {
			seed = seed * 6364136223846793005 + 1442695040888963407
			m[i][j] = int64(seed >> 33) - (1 << 30)
		}
	}
	return m
}

func selftest(p obj, units int64) job {
	fields(p, "rounds", false)
	rounds := number(get(p, "rounds", 4), 1, 64)
	require(units == 1, "selftest has one unit")
	return func(unit int64) obj {
		h := sha256.New()
		m := randomMatrix(2026)
		mod := new(big.Int).Lsh(big.NewInt(1), 32)
		for r := int64(0); r < rounds; r++ {
			b := randomMatrix(uint64(1000 + r))
			var next matrix
			for i := range m {
				for j := range b {
					var sum, term big.Int
					for k, x := range m[i] {
						sum.Add(&sum, term.SetInt64(x * b[k][j]))
					}
					if j != 0 {
						h.Write([]byte(","))
					}
					h.Write([]byte(sum.String()))
					next[i][j] = int64(int32(sum.Mod(&sum, mod).Uint64()))
				}
				h.Write([]byte("\n"))
			}
			m = next
		}
		frac := new(big.Rat)
		for k := int64(1); k < 60; k++ {
			frac.Add(frac, big.NewRat(1, k * (k + 1)))
		}
		fmt.Fprintln(h, ratio(frac))
		p := new(big.Int).Sub(new(big.Int).Lsh(big.NewInt(1), 255), big.NewInt(19))
		direct := new(big.Int).Exp(big.NewInt(3), big.NewInt(10000), p)
		half := new(big.Int).Exp(big.NewInt(3), big.NewInt(5000), p)
		pub, _ := hex.DecodeString("3d4017c3e843895a92b70aa74d1b7ebc9c982ccf2ec4968cc0cd55f12af4660c")
		sig, _ := hex.DecodeString("92a009a9f0d4cab8720e820b5f642540a2b27b5416503f8fb3762223ebdb69da085ac1e43e15996e458f3613d0f11d8c387b2eaeb4302aeeb00d291612bb0c00")
		checks := []struct{name string; ok bool}{
			{"ed25519", ed25519.Verify(pub, []byte{0x72}, sig) && !ed25519.Verify(pub, []byte{0x73}, sig)},
			{"fraction", frac.Cmp(big.NewRat(59, 60)) == 0},
			{"pow", direct.Cmp(half.Exp(half, big.NewInt(2), p)) == 0},
			{"sha256", fmt.Sprintf("%x", sha256.Sum256([]byte("abc"))) == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"},
		}
		ok := true
		for _, c := range checks {
			bit := 0
			if c.ok {
				bit = 1
			} else {
				ok = false
			}
			fmt.Fprintf(h, "%s=%d\n", c.name, bit)
		}
		return obj{"kernel": "selftest@1", "rounds": rounds, "digest": fmt.Sprintf("%x", h.Sum(nil)), "ok": ok}
	}
}
