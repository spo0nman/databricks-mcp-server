#!/usr/bin/env pwsh
# Start script for the Databricks MCP server

# Check if the virtual environment exists
if (-not (Test-Path -Path ".venv")) {
    Write-Host "Virtual environment not found. Please create it first:"
    Write-Host "uv venv"
    exit 1
}

# Activate virtual environment
. .\.venv\Scripts\Activate.ps1

# Check if environment variables are set
if (-not (Get-Item -Path Env:DATABRICKS_HOST -ErrorAction SilentlyContinue) -or 
    -not (Get-Item -Path Env:DATABRICKS_TOKEN -ErrorAction SilentlyContinue)) {
    Write-Host "Warning: DATABRICKS_HOST and/or DATABRICKS_TOKEN environment variables are not set."
    Write-Host "You can set them now or the server will look for them in other sources."
    $continue = Read-Host "Do you want to continue? (y/n)"
    if ($continue -ne "y") {
        exit 1
    }
}

# Start the server
Write-Host "Starting Databricks MCP server at $(Get-Date)"
if (Get-Item -Path Env:DATABRICKS_HOST -ErrorAction SilentlyContinue) {
    Write-Host "Databricks Host: $env:DATABRICKS_HOST"
}

uv run src.server.databricks_mcp_server

Write-Host "Server stopped at $(Get-Date)" 