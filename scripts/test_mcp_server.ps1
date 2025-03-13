#!/usr/bin/env pwsh
# PowerShell script to run the MCP server test

# Activate virtual environment
. .\databricks-mcp\Scripts\Activate.ps1

# Ensure no MCP servers are already running
$serverProcesses = Get-Process -Name pwsh | Where-Object { $_.CommandLine -like "*start_mcp_server.ps1*" }
if ($serverProcesses) {
    Write-Host "Found existing MCP server processes, stopping them first..."
    $serverProcesses | ForEach-Object { 
        Stop-Process -Id $_.Id -Force 
        Write-Host "Stopped process $($_.Id)"
    }
}

# Run the test 
Write-Host "Running MCP server tests..."
python test_mcp_server.py

# When done, clean up any leftover processes
$serverProcesses = Get-Process -Name pwsh | Where-Object { $_.CommandLine -like "*start_mcp_server.ps1*" }
if ($serverProcesses) {
    Write-Host "Cleaning up any remaining MCP server processes..."
    $serverProcesses | ForEach-Object { 
        Stop-Process -Id $_.Id -Force 
        Write-Host "Stopped process $($_.Id)"
    }
} 