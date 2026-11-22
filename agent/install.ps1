# Installer of the SkyNet research agent for Windows (PowerShell).
#
# It only finds Python, downloads agent/install.py from the project repository
# and runs it. It does not need administrator rights, does not start the agent
# and does not turn autostart on. Read agent/README.md first.
#
# Everything runs inside one script block, so that nothing (settings, variables,
# functions) is left behind in your PowerShell window when the text of this file
# is piped into Invoke-Expression.

& {
    $ErrorActionPreference = "Stop"
    [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12

    $base = "https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main"
    if ($env:SKYNET_AGENT_BASE_URL) { $base = $env:SKYNET_AGENT_BASE_URL.TrimEnd("/") }

    function Find-SkyNetPython {
        $candidates = @(@("py", "-3"), @("python"), @("python3"))
        foreach ($candidate in $candidates) {
            $exe = $candidate[0]
            if (-not (Get-Command $exe -ErrorAction SilentlyContinue)) { continue }
            $rest = @()
            if ($candidate.Count -gt 1) { $rest = $candidate[1..($candidate.Count - 1)] }
            try {
                & $exe @rest -c "import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)" 2>$null
                if ($LASTEXITCODE -eq 0) { return ,$candidate }
            } catch { }
        }
        return $null
    }

    $python = Find-SkyNetPython
    if (-not $python) {
        Write-Host "Python 3.9 or newer was not found."
        Write-Host "Install it from https://www.python.org/downloads/ (or run: winget install Python.Python.3.12),"
        Write-Host "open a new PowerShell window and run this installer again."
        return
    }

    $tmp = Join-Path ([IO.Path]::GetTempPath()) ("skynet-agent-install-" + [Guid]::NewGuid().ToString("N") + ".py")
    try {
        Invoke-WebRequest -UseBasicParsing -Uri "$base/agent/install.py" -OutFile $tmp
        $exe = $python[0]
        $rest = @()
        if ($python.Count -gt 1) { $rest = $python[1..($python.Count - 1)] }
        & $exe @rest -I $tmp @args
    } finally {
        Remove-Item -Force $tmp -ErrorAction SilentlyContinue
    }
} @args
