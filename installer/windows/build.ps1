param([Parameter(Mandatory)][string]$BuildDir,
      [string]$AssetDir = "$PSScriptRoot/../../dist",
      [ValidateSet("amd64","arm64")][string]$Arch = "amd64")

$ErrorActionPreference = 'Stop'
$build = (New-Item -ItemType Directory -Force -Path $BuildDir).FullName
& python -IB "$PSScriptRoot/stage.py" $build $AssetDir $Arch
if ($LASTEXITCODE -ne 0) { throw 'Signed release verification failed.' }
$version = (Get-Content -Raw -LiteralPath "$build/release/release.json" | ConvertFrom-Json).version
$iscc = Get-Command ISCC.exe -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty Source
if (-not $iscc) { $iscc = Join-Path ${env:ProgramFiles(x86)} 'Inno Setup 6/ISCC.exe' }
$innoArch = if ($Arch -eq 'arm64') { 'arm64' } else { 'x64os' }
& $iscc "/DBuildDir=$build" "/DAgentVersion=$version" "/DTargetArch=$innoArch" "/DAssetArch=$Arch" "$PSScriptRoot/skynet-agent.iss"
if ($LASTEXITCODE -ne 0) { throw 'Inno Setup compilation failed.' }
$exe = Get-Item -LiteralPath "$build/dist/SkyNetAgentSetup-$version-$Arch.exe"
$sha = (Get-FileHash -Algorithm SHA256 -LiteralPath $exe.FullName).Hash.ToLowerInvariant()
Set-Content -LiteralPath "$($exe.FullName).sha256" -Value "$sha  $($exe.Name)" -Encoding ascii
