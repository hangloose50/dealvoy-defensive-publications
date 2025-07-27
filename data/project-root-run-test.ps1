# project-root-run-test.ps1

$scriptName = 'test_sheet_write.py'
$dir = Get-Location

while ($dir -and -not (Test-Path "$dir\$scriptName")) {
    $parent = Split-Path $dir -Parent
    if ($parent -eq $dir) { break }
    $dir = $parent
}

if (Test-Path "$dir\$scriptName") {
    Write-Host "▶️ Found $scriptName in: $dir" -ForegroundColor Green
    Push-Location $dir
    python .\$scriptName
    Pop-Location
} else {
    Write-Host "❌ Could not locate $scriptName under $(Get-Location)" -ForegroundColor Red
}
