<#
set_webhook.ps1

Sets a Telegram webhook for your bot. It attempts to detect a running ngrok
HTTPS tunnel by querying the local ngrok API at http://127.0.0.1:4040/api/tunnels.
If no ngrok tunnel is found it will prompt you to paste a public HTTPS URL.

Usage:
  .\set_webhook.ps1               # uses $env:BOT_TOKEN and ngrok if present
  .\set_webhook.ps1 -Url <url>    # use explicit public URL
  .\set_webhook.ps1 -Secret <s>   # optional secret token for webhook verification
#>
[CmdletBinding()]
param(
    [string]$Url,
    [string]$Secret
)

function Get-BotToken {
    if ($env:BOT_TOKEN -and $env:BOT_TOKEN -ne '') { return $env:BOT_TOKEN }
    if ($env:TELEGRAM_TOKEN -and $env:TELEGRAM_TOKEN -ne '') { return $env:TELEGRAM_TOKEN }
    $t = Read-Host -Prompt 'BOT_TOKEN nicht gesetzt. Bitte Bot-Token eingeben (keine Leerzeile)'
    if (-not $t -or $t -eq '') { Write-Error 'Kein Token; Abbruch.'; exit 1 }
    return $t
}

$token = Get-BotToken

if (-not $Url) {
    # Try to detect ngrok tunnel via its local API
    try {
        $tunnels = Invoke-RestMethod -Uri 'http://127.0.0.1:4040/api/tunnels' -Method Get -ErrorAction Stop
        $https = $tunnels.tunnels | Where-Object { $_.public_url -like 'https:*' } | Select-Object -First 1
        if ($https -and $https.public_url) {
            $Url = $https.public_url
            Write-Output "Found ngrok HTTPS tunnel: $Url"
        }
    } catch {
        Write-Output 'Ngrok API not available on http://127.0.0.1:4040 — make sure ngrok is running if you expect it.'
    }
}

if (-not $Url) {
    $Url = Read-Host -Prompt 'Bitte die öffentliche HTTPS-URL eingeben (z.B. https://xyz.ngrok.io/telegram)'
    if (-not $Url -or $Url -eq '') { Write-Error 'Keine URL angegeben; Abbruch.'; exit 1 }
}

# Ensure the URL is HTTPS
if ($Url -notlike 'https:*') {
    Write-Warning "Die angegebene URL sieht nicht nach HTTPS aus: $Url"
}

# Build body for setWebhook
$body = @{ url = $Url }
# Allowed updates minimal set — adjust if you need more
$body.allowed_updates = '["message","inline_query"]'
if ($Secret) { $body.secret_token = $Secret }

$api = "https://api.telegram.org/bot$token/setWebhook"
Write-Output "Setting webhook to $Url ..."
try {
    $resp = Invoke-RestMethod -Uri $api -Method Post -Body $body
    if ($resp.ok) {
        Write-Output "Webhook gesetzt: $($resp.result.url)"
    } else {
        Write-Error "setWebhook response not OK: $($resp | ConvertTo-Json -Depth 3)"
    }
} catch {
    Write-Error "Fehler beim Setzen des Webhook: $_"
    exit 1
}

# Show webhook info
try {
    $info = Invoke-RestMethod -Uri "https://api.telegram.org/bot$token/getWebhookInfo" -Method Get
    Write-Output "getWebhookInfo:"
    $info | ConvertTo-Json -Depth 4 | Write-Output
} catch {
    Write-Warning 'Konnte getWebhookInfo nicht abfragen.'
}
