# run_local.ps1 — start the bot locally using the virtualenv
# Usage: Open PowerShell in the repo root and run:
#   .\run_local.ps1
# The script will try to activate `.venv` and then either use the existing
# BOT_TOKEN environment variable or prompt you for a token for this session.

# Try to activate .venv if present
$venvPath = Join-Path $PSScriptRoot '.venv\Scripts\Activate.ps1'
if (Test-Path $venvPath) {
    Write-Output "Activating virtualenv: $venvPath"
    & $venvPath
} else {
    Write-Output "No .venv found at $venvPath — ensure dependencies are installed or create one with: python -m venv .venv"
}

# Read token from BOT_TOKEN or prompt the user
if (-not $env:BOT_TOKEN -or $env:BOT_TOKEN -eq '') {
    $token = Read-Host -Prompt "BOT_TOKEN nicht gesetzt. Bitte Bot-Token eingeben (es wird nur für diese Sitzung gesetzt)"
    if ($token -and $token -ne '') {
        $env:BOT_TOKEN = $token
    } else {
        Write-Error "Kein Token eingegeben. Abbruch."
        exit 1
    }
} else {
    Write-Output "Using BOT_TOKEN from environment."
}

# Ensure python is available
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Error "Python ist nicht in PATH. Stelle sicher, dass das .venv aktiviert ist oder Python installiert ist."
    exit 1
}

# Install recommended deps if requirements exist (non-interactive)
if (Test-Path "$PSScriptRoot\requirements.txt") {
    Write-Output "Installing requirements (if needed)..."
    python -m pip install -r "$PSScriptRoot\requirements.txt"
}

# Start the bot (token is read by main.py from BOT_TOKEN)
Write-Output "Starting bot (press Ctrl+C to stop)..."
python "$PSScriptRoot\main.py" --run-bot --token $env:BOT_TOKEN
