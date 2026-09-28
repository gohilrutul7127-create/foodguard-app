$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendDir = Join-Path $root "backend"
$venvPython = Join-Path $backendDir "venv\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    Write-Host "Python virtual environment not found at: $venvPython"
    Write-Host "Run the project setup first or recreate the backend venv."
    exit 1
}

while ($true) {
    Write-Host "Starting FoodGuard backend..."
    try {
        & $venvPython (Join-Path $backendDir "manage.py") migrate
        & $venvPython (Join-Path $backendDir "manage.py") runserver 0.0.0.0:8000
    }
    catch {
        Write-Host "Backend crashed: $($_.Exception.Message)"
    }

    Write-Host "Backend restarting in 5 seconds..."
    Start-Sleep -Seconds 5
}
