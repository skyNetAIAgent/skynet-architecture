#!/usr/bin/env bash
# Build both main packages as Android executables for extraction to nativeLibraryDir.
set -euo pipefail
export LC_ALL=C CGO_ENABLED=0 GOTOOLCHAIN=local GOPROXY=off GOWORK=off GOAMD64=v1 GOARM64=v8.0
android_dir=$(cd "$(dirname "$0")" && pwd)
cd "$android_dir/../agent-go"
stock_go=$(command -v go)
stock_root=$(cd "$("$stock_go" env GOROOT)" && pwd -P)
if [[ $("$stock_go" env GOVERSION) != go1.27.4 ]]; then
    echo 'The Android build requires Go 1.27.4 (including its source tree).' >&2
    exit 1
fi
build_tmp=$(mktemp -d)
trap 'rm -rf -- "$build_tmp"' EXIT
output="$android_dir/app/src/main/jniLibs"

build_agent() {
    local arch=$1 abi=$2 machine=$3 tool=$4 root=$5
    local binary="$build_tmp/$abi/libskynet.so" flags='-s -w -linkmode=internal -I /system/bin/linker64'
    mkdir -p "$(dirname "$binary")"
    # Go engine of desktop release 13 (1.3.2). APK versionCode is separate.
    flags+=' -X main.version=1.3.2 -X main.releaseSeq=13'
    if [[ $arch == amd64 ]]; then flags+=' -R 16384'; fi
    GOOS=android GOARCH="$arch" GOROOT="$root" "$tool" build -buildvcs=false -trimpath \
        -buildmode=pie -ldflags="$flags" -o "$binary" ./cmd/skynet-agent
    local description header
    description=$(file -b "$binary")
    header=$(readelf -hW "$binary")
    echo "$abi: $description"
    [[ -x $binary && $description == *"ELF 64-bit LSB pie executable, $machine,"* &&
        $description == *'interpreter /system/bin/linker64,'* &&
        $header =~ Entry\ point\ address:[[:space:]]+0x[1-9a-fA-F][0-9a-fA-F]* ]] || {
        echo "Invalid Android executable for $abi" >&2
        return 1
    }
}

build_agent arm64 arm64-v8a 'ARM aarch64' "$stock_go" "$stock_root"

# Stock cmd/go and cmd/link both consult internal/platform. The release supports
# pure-Go AMD64 PIE and Android AMD64 code generation, but requires cgo when
# combining them. Opt in only in these two private host tools for this build.
toolroot="$build_tmp/go"
cp -RL "$stock_root" "$toolroot"
# Go installed from a module cache may have read-only directories.
chmod -R u+w "$toolroot"
platform=src/internal/platform/supported.go
tool_dir="pkg/tool/$("$stock_go" env GOHOSTOS)_$("$stock_go" env GOHOSTARCH)"
patch -s --fuzz=0 "$toolroot/$platform" <<'PATCH'
@@ -126,7 +126,7 @@
 
 	switch goos {
 	case "android":
-		if goarch != "arm64" {
+		if goarch != "arm64" && goarch != "amd64" {
 			return true
 		}
 	case "ios":
@@ -232,7 +232,7 @@
 
 func InternalLinkPIESupported(goos, goarch string) bool {
 	switch goos + "/" + goarch {
-	case "android/arm64",
+	case "android/arm64", "android/amd64",
 		"darwin/amd64", "darwin/arm64",
 		"linux/amd64", "linux/arm64", "linux/loong64", "linux/ppc64", "linux/ppc64le", "linux/s390x",
 		"windows/386", "windows/amd64", "windows/arm64":
PATCH
mkdir "$build_tmp/host"
GOROOT="$toolroot" GOOS=$("$stock_go" env GOHOSTOS) GOARCH=$("$stock_go" env GOHOSTARCH) \
    "$stock_go" build -trimpath -o "$build_tmp/host/" cmd/go cmd/link
mv -f "$build_tmp/host/go" "$toolroot/bin/go"
mv -f "$build_tmp/host/link" "$toolroot/$tool_dir/link"
build_agent amd64 x86_64 'x86-64' "$toolroot/bin/go" "$toolroot"

# Only publish the files after both builds and ELF checks pass.
for abi in arm64-v8a x86_64; do
    install -d "$output/$abi"
    install -m 755 "$build_tmp/$abi/libskynet.so" "$output/$abi/libskynet.so"
done
