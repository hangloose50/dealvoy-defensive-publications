# verify_structure.ps1

# 1. List of files and folders that must exist
$required = @(
    "app\__init__.py",
    "app\main.py",
    "app\config.py",
    "app\database.py",
    "app\models.py",
    "app\schemas.py",
    "app\api\v1\webhook.py",
    "dashboard_builder.py",
    "utils\health.py",
    ".env",
    "credentials.json"
)

Write-Host ""
Write-Host "Verifying required files and folders..." 
Write-Host "--------------------------------------"

foreach ($path in $required) {
    if (Test-Path $path) {
        Write-Host "FOUND   : $path"
    }
    else {
        Write-Host "MISSING : $path" -ForegroundColor Red
    }
}

# 2. Check for unexpected top-level items
$allowedTop = @(
    "app","utils","pipelines","logs","data",
    "dashboard_builder.py",".env","credentials.json"
)

Write-Host ""
Write-Host "Checking for unexpected items at root..."
Write-Host "-----------------------------------------"

$allItems = Get-ChildItem -Name
$unexpected = $allItems | Where-Object { $allowedTop -notcontains $_ }

if ($unexpected) {
    foreach ($item in $unexpected) {
        Write-Host "UNEXPECTED : $item" -ForegroundColor Yellow
    }
}
else {
    Write-Host "No unexpected items found at root."
}

Write-Host "" 
