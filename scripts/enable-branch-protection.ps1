<#
PowerShell helper to attempt to enable branch protection for `main`.

Usage:
  - Ensure `gh` CLI is installed and you are logged in (`gh auth login`).
  - Run this script from PowerShell as a user with sufficient rights.

Note: GitHub may return HTTP 403 if the repo is private and the plan doesn't permit programmatic branch protection.
#>

param()

$body = @{
    required_status_checks = @{ strict = $true; contexts = @("CI") }
    enforce_admins = $true
    required_pull_request_reviews = @{ dismiss_stale_reviews = $true; require_code_owner_reviews = $false; required_approving_review_count = 1 }
} | ConvertTo-Json -Depth 5

Write-Host "Attempting to set branch protection on 'main'..."

# Run the gh api call
$cmd = "gh api --method PUT /repos/hentschel873-cyber/Python/branches/main/protection -f '$body'"
Write-Host $cmd

Invoke-Expression $cmd

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to set branch protection. Check repository visibility / plan or run the GUI steps in docs/BRANCH_PROTECTION.md"
} else {
    Write-Host "Branch protection API call completed. Verify on GitHub Settings → Branches."
}
