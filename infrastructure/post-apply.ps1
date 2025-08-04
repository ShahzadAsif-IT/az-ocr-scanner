winget install --id jqlang.jq -e

$raw = terraform output -json | ConvertFrom-Json
$raw.PSObject.Properties.ForEach({
    "$($_.Name)=""$([string]$_.Value.value)"""
}) | Set-Content ..\.env
