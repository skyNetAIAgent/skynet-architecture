# Windows x64 installer

Download the EXE and the matching `.exe.sha256` from the same project release. In
PowerShell, open the download folder and compare the checksum. [GitHub Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases)

```powershell
$file = 'SkyNetAgentSetup-0.2.2.exe'
$expected = ((Get-Content -Raw "$file.sha256") -split '\s+')[0]
if ((Get-FileHash $file -Algorithm SHA256).Hash -ne $expected) { throw 'Checksum mismatch.' }
```

Open the verified EXE. SmartScreen may show **Windows protected your PC** because the
installer has no code signature. Choose **More info**, confirm the filename, then choose
**Run anyway**. Setup installs for the current user. Clear either startup checkbox to
change when the agent runs.

The agent accepts signed updates to its own files. A newer installer updates the bundled
Python. Install over the existing copy to keep the device identity and waiting results.
The Start menu uninstaller also keeps these by default. Its optional data deletion
checkbox includes the outbox and pending signed records.

## Build and test

Use a clean checkout with LF line endings for the signed files. From the repository root
on x64 Windows, run PowerShell 7 with a fresh build directory. The build checks for Inno
Setup 6.3.3 or newer on PATH or in its usual location. It uses Chocolatey to install
6.3.3 if the compiler is missing.

```powershell
./installer/windows/build.ps1 -BuildDir build
```

`python.lock` must contain the exact 3.12 patch version and 64-digit SHA-256 of its
official `python-<version>-embed-amd64.zip`. For a new pin, authenticate the archive using
the instructions and Sigstore bundle linked from the Python release page, then record
its SHA-256. An empty or invalid pin stops the build before download. [Python 3.12.10 release](https://www.python.org/downloads/release/python-31210/)

The build verifies the archive before extraction. The embedded interpreter stages only
files from the authenticated release manifest. At install time it checks the bundle
again, including its file list, before executing the candidate. The stock
`python312._pth` supplies the standard library. The launcher and candidate check add
the selected release directory to `sys.path` under `-I`.

On a disposable Windows profile with no existing SkyNet installation, run the smoke
test. It installs silently, checks sign-in registration and the CLI without system
Python on PATH, then uninstalls and checks the retained data.

```powershell
./installer/windows/smoke.ps1 -BuildDir build
```

Alternatively, run **Actions → Windows installer → Run workflow**. After the smoke
test passes, download the `SkyNetAgentSetup-x64` artifact. Its `SkyNetAgentSetup-<version>.exe`
and `.exe.sha256` are the two assets to attach manually to the matching GitHub Release.
