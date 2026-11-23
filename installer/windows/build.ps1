param([Parameter(Mandatory)][string]$BuildDir)

$ErrorActionPreference = 'Stop'
$lock = Get-Content -Raw -LiteralPath "$PSScriptRoot/python.lock" | ConvertFrom-Json
if ($lock.version -notmatch '^3\.12\.\d+$' -or $lock.sha256 -notmatch '^[a-fA-F0-9]{64}$') {
    throw 'Set the verified SHA-256 of the official embeddable archive in python.lock.'
}
$build = (New-Item -ItemType Directory -Path $BuildDir).FullName
$archive = Join-Path $build 'python.zip'
$url = "https://www.python.org/ftp/python/$($lock.version)/python-$($lock.version)-embed-amd64.zip"
Invoke-WebRequest -Uri $url -OutFile $archive
if ((Get-FileHash -Algorithm SHA256 -LiteralPath $archive).Hash -ne $lock.sha256) {
    throw 'The Python archive does not match python.lock.'
}
Expand-Archive -LiteralPath $archive -DestinationPath "$build/python"
$python = Join-Path $build 'python/python.exe'
& $python -IB "$PSScriptRoot/stage.py" $build
if ($LASTEXITCODE -ne 0) { throw 'Signed release verification failed.' }
$version = (Get-Content -Raw -LiteralPath "$build/release/release.json" | ConvertFrom-Json).version

$iscc = (Get-Command ISCC.exe -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1).Source
if (-not $iscc) {
    $iscc = Join-Path ${env:ProgramFiles(x86)} 'Inno Setup 6/ISCC.exe'
    if (-not (Test-Path -LiteralPath $iscc)) {
        choco install innosetup --version=6.3.3 --yes --no-progress
        if ($LASTEXITCODE -ne 0) { throw 'Could not install Inno Setup.' }
    }
}
$runtimeVersion = (Get-Item -LiteralPath $python).VersionInfo.FileVersionRaw
& $iscc "/DBuildDir=$build" "/DAgentVersion=$version" "/DRuntimeFileVersion=$runtimeVersion" "$PSScriptRoot/skynet-agent.iss"
if ($LASTEXITCODE -ne 0) { throw 'Inno Setup compilation failed.' }
$exe = Get-Item -LiteralPath "$build/dist/SkyNetAgentSetup-$version.exe"
$sha = (Get-FileHash -Algorithm SHA256 -LiteralPath $exe.FullName).Hash.ToLowerInvariant()
Set-Content -LiteralPath "$($exe.FullName).sha256" -Value "$sha  $($exe.Name)" -Encoding ascii
