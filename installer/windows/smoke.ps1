param([Parameter(Mandatory)][string]$BuildDir)

$ErrorActionPreference = 'Stop'
$env:PATH = "$env:SystemRoot\System32;$env:SystemRoot"
if (Get-Command python.exe -ErrorAction SilentlyContinue) { throw 'System Python is still on PATH.' }
$app = Join-Path ([Environment]::GetFolderPath('LocalApplicationData')) 'SkyNetAgent'
$group = Join-Path ([Environment]::GetFolderPath('Programs')) 'SkyNet Agent'
$runKey = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run'
if ((Test-Path -LiteralPath $app) -or (Test-Path -LiteralPath $group) -or
    (Get-ItemPropertyValue $runKey SkyNetAgent -ErrorAction SilentlyContinue)) {
    throw 'This smoke test needs a fresh agent profile.'
}

function Run-Setup([string]$Exe, [string[]]$Options) {
    $process = Start-Process -FilePath $Exe -ArgumentList $Options -WindowStyle Hidden -Wait -PassThru
    if ($process.ExitCode -ne 0) { throw "$Exe failed with exit code $($process.ExitCode)." }
}

$version = (Get-Content -Raw -LiteralPath "$BuildDir/release/release.json" | ConvertFrom-Json).version
$exe = Get-Item -LiteralPath "$BuildDir/dist/SkyNetAgentSetup-$version.exe"
$expected = ((Get-Content -Raw -LiteralPath "$($exe.FullName).sha256") -split '\s+')[0]
if ((Get-FileHash -LiteralPath $exe.FullName).Hash -ne $expected) { throw 'Invalid installer checksum.' }
$silent = @('/VERYSILENT', '/SUPPRESSMSGBOXES', '/NORESTART')
Run-Setup $exe.FullName ($silent + '/CURRENTUSER' + '/TASKS=autostart')
if ((Get-ItemPropertyValue $runKey SkyNetAgent) -ne ('"{0}\python\pythonw.exe" "{0}\launcher.py" run' -f $app)) {
    throw 'Autostart did not select the bundled interpreter.'
}
$result = & "$app/skynet-agent.cmd" selftest
if ($LASTEXITCODE -ne 0 -or $result -notcontains 'Installed files match the signed release: yes') {
    throw "Offline selftest failed: $result"
}
$reported = & "$app/skynet-agent.cmd" version
if ($LASTEXITCODE -ne 0 -or "$reported" -notlike "skynet-agent $version (*") {
    throw "Unexpected version output: $reported"
}
foreach ($folder in 'outbox', 'net/pending') {
    New-Item -ItemType Directory -Force -Path "$app/$folder" | Out-Null
    Set-Content -LiteralPath "$app/$folder/smoke.json" -Value '{}'
}
Set-Content -LiteralPath "$app/identity.key" -Value 'smoke'
$uninstaller = Get-Item -Path "$app/unins*.exe"
Run-Setup $uninstaller.FullName $silent
if ((Test-Path -LiteralPath $group) -or (Get-ItemPropertyValue $runKey SkyNetAgent -ErrorAction SilentlyContinue)) {
    throw 'The Start menu group or autostart entry survived uninstall.'
}
foreach ($item in 'python', 'versions', 'launcher.py', 'skynet-agent.cmd', $uninstaller.Name) {
    if (Test-Path -LiteralPath "$app/$item") { throw "Uninstall left $item." }
}
foreach ($item in 'identity.key', 'outbox/smoke.json', 'net/pending/smoke.json') {
    if (-not (Test-Path -LiteralPath "$app/$item")) { throw "Uninstall lost $item." }
}
