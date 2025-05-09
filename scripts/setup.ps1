# Setup script for Renovation Estimator project (Windows PowerShell version)
# Uses uv for faster Python environment setup

Write-Host "Setting up Renovation Estimator environment..." -ForegroundColor Green

# Check if uv is installed
$uvInstalled = $null
try {
    $uvInstalled = Get-Command uv -ErrorAction Stop
} catch {
    Write-Host "Installing uv package manager..." -ForegroundColor Yellow
    
    # Download and run the installer
    Invoke-WebRequest -Uri https://astral.sh/uv/install.ps1 -OutFile install-uv.ps1
    .\install-uv.ps1
    Remove-Item install-uv.ps1
    
    Write-Host "uv installed successfully!" -ForegroundColor Green
    # Reload PATH
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    uv venv
}

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
uv pip install -r requirements.txt

# Create necessary data directories
New-Item -ItemType Directory -Force -Path "data\synthetic" | Out-Null
New-Item -ItemType Directory -Force -Path "data\fine_tuning" | Out-Null
New-Item -ItemType Directory -Force -Path "data\evaluation" | Out-Null

Write-Host "Environment setup complete!" -ForegroundColor Green
Write-Host "To activate the environment, run: .venv\Scripts\activate" -ForegroundColor Cyan
Write-Host "To run the application, run: streamlit run app.py" -ForegroundColor Cyan 