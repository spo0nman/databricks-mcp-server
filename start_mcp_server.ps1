#!/usr/bin/env pwsh
# Wrapper script to run the MCP server start script from scripts directory

# Get the directory of this script
$scriptPath = $MyInvocation.MyCommand.Path
$scriptDir = Split-Path $scriptPath -Parent

# Change to the script directory
Set-Location $scriptDir

# Run the actual server script
& "$scriptDir\scripts\start_mcp_server.ps1" 