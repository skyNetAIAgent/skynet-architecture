# SkyNet agent · G1

This Go 1.22 module implements the offline protocol and the seven version 1 compute kernels. It uses the Go standard library. The module contains library packages and a shared compatibility test suite.

| Package | Entry points |
| --- | --- |
| `canon` | `Parse` preserves integer precision and rejects duplicate keys, invalid Unicode and non-finite numbers. `Marshal(v, true)` produces ASCII hash input. `Marshal(v, false)` produces UTF-8 wire bytes. |
| `sig` | `Document` verifies the detached signature over the original bytes, then parses the object. A nil key list selects the pinned release key. |
| `records` | `LoadSeed`, `Make`, `Wire`, `Parse` and `Verify` implement device identity and the six record types. Pass the current Unix time to the verifier. A valid future-dated record returns `ErrFuture`. First-time key creation uses a private temporary file and a non-replacing hard link. |
| `nostr` | `SecretFromSeed`, `Public`, `Sign`, `Verify` and `MakeEvent` implement x-only BIP-340 keys and kind 9467 events. Signing accepts a 32-byte auxiliary value for reproducible vectors or nil for fresh randomness. The `math/big` scalar operations have variable execution time. |
| `kernels` | `Validate` and `Run` take a name, version and parameter object from `canon.Parse`. `Run` also takes the zero-based unit and total units. Its result can be passed directly to `canon.Hash`. |
| `tasks` | `ParseSigned` validates an index using the supplied local release sequence. A structurally valid task carries a `Reason` when closed, too new, unsupported or rejected by its kernel. The compute registry excludes `ai-answer`. |

## Build and test

Run the following PowerShell commands from the module directory. The caches and temporary files are local to the working tree.

```powershell
$go = 'D:\skyNet\go-build\go\bin\go.exe'
$cacheDir = Join-Path (Get-Location) '.go-work'
$env:GOCACHE = Join-Path $cacheDir 'cache'
$env:GOPATH = Join-Path $cacheDir 'path'
$env:GOTMPDIR = Join-Path $cacheDir 'tmp'
New-Item -ItemType Directory -Force $env:GOCACHE,$env:GOPATH,$env:GOTMPDIR | Out-Null
$env:GOTOOLCHAIN = 'local'
$env:GOFLAGS = '-mod=mod'
$env:CGO_ENABLED = '0'
$env:GOPROXY = 'off'
$env:GOSUMDB = 'off'
$env:SKYNET_GOLDEN = ''
& $go build ./...
& $go vet ./...
& $go test -count=1 -timeout 1h ./...
```

The ordinary suite reads the signed index and 1,261 node records. It includes the RFC 8032 and BIP-340 vectors, the review’s record and event IDs, and 513 golden units. Each selected unit runs through the kernel registry and must match both the stored canonical result and its SHA-256.

| `SKYNET_GOLDEN` | Units selected by `TestGoldenLong` |
| --- | --- |
| `sample` | 73 units. Every `exit-scam-a` unit whose number is divisible by ten in each task, plus both supplied `token-certificate` units. |
| `long` | 686 units with a recorded Python duration over 60 seconds. |
| `all` | All 1,199 supplied units from both files. |

```powershell
$env:SKYNET_GOLDEN = 'sample'
& $go test -run '^TestGoldenLong$' -count=1 -timeout 24h -v .
$env:SKYNET_GOLDEN = 'all'
& $go test -run '^TestGoldenLong$' -count=1 -timeout 0 -v .
```

The compressed JSONL files in `testdata` preserve the supplied bytes and row order. The index and detached signature are byte-for-byte copies. For `slow.json`, a timing belongs to a golden row when task ID, unit and result hash all match. The largest matching `elapsed_s` decides the category. All 413 rows without a recorded time were timed locally with the Python implementation and took less than one second each.

## Random JSON corpus and fuzzing

`testdata/corpus.jsonl` holds 2,000 random JSON values generated independently
with the Python reference plus 25 inputs that must be rejected and 10
documented strictness divergences (`kind:"divergent"`, Python more lenient).
`TestCorpusCompat` compares `canon.Parse`/`Marshal` against the stored Python
canonical/wire bytes and SHA-256, or:

```powershell
& $go run ./cmd/canoncheck corpus.jsonl
```

Fuzz the strict JSON parser and the detached-signature parser (no panics on
arbitrary input):

```powershell
& $go test -run '^$' -fuzz=FuzzCanonParse -fuzztime=45s .
& $go test -run '^$' -fuzz=FuzzSigLines -fuzztime=45s .
```
