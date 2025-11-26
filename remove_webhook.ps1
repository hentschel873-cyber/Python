<#
remove_webhook.ps1

Removes the webhook for your Telegram bot (sets webhook to an empty URL).
Usage:
  .\remove_webhook.ps1
#>
[CmdletBinding()]
param()

function Get-BotToken {
    if ($env:BOT_TOKEN -and $env:BOT_TOKEN -ne '') { return $env:BOT_TOKEN }
    if ($env:TELEGRAM_TOKEN -and $env:TELEGRAM_TOKEN -ne '') { return $env:TELEGRAM_TOKEN }
    $t = Read-Host -Prompt 'BOT_TOKEN nicht gesetzt. Bitte Bot-Token eingeben (keine Leerzeile)'
    if (-not $t -or $t -eq '') { Write-Error 'Kein Token; Abbruch.'; exit 1 }
    return $t
}

$token = Get-BotToken

$api = "https://api.telegram.org/bot$token/setWebhook"
Write-Output 'Removing webhook (setting to empty URL)...'
try {
    $resp = Invoke-RestMethod -Uri $api -Method Post -Body @{ url = '' }
    if ($resp.ok) { Write-Output 'Webhook removed.' } else { Write-Error "setWebhook response not OK: $($resp | ConvertTo-Json -Depth 3)" }
} catch {
    Write-Error "Error removing webhook: $_"
    exit 1
}

try { $info = Invoke-RestMethod -Uri "https://api.telegram.org/bot$token/getWebhookInfo" -Method Get; $info | ConvertTo-Json -Depth 4 | Write-Output } catch { Write-Warning 'Could not fetch webhook info.' }
