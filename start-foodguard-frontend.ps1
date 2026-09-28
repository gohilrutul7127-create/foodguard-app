$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path

if (-not (Test-Path (Join-Path $root "node_modules"))) {
    Write-Host "Installing frontend dependencies..."
    Push-Location $root
    & npm install
    Pop-Location
}

while ($true) {
    Write-Host "Starting FoodGuard frontend..."
    Push-Location $root
    try {
        & npm run dev -- --host 0.0.0.0
    }
    catch {
        Write-Host "Frontend crashed: $($_.Exception.Message)"
    }
    finally {
        Pop-Location
    }

    Write-Host "Frontend restarting in 5 seconds..."
    Start-Sleep -Seconds 5
}
