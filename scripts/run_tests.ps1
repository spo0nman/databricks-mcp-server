#!/usr/bin/env pwsh
# PowerShell script to run all tests

# Activate virtual environment
. ..\databricks-mcp\Scripts\Activate.ps1

# Make sure there are no existing MCP server processes
$serverProcesses = Get-Process -Name pwsh | Where-Object { $_.CommandLine -like "*start_server.ps1*" }
if ($serverProcesses) {
    Write-Host "Found existing MCP server processes, stopping them first..."
    $serverProcesses | ForEach-Object { 
        Stop-Process -Id $_.Id -Force 
        Write-Host "Stopped process $($_.Id)"
    }
}

# Set timeout in seconds
$timeout = 60

# Run the tests with a timeout
Write-Host "Running tests with a $timeout second timeout..."

# Run direct tests
Write-Host "Running direct tests..."
$job = Start-Job -ScriptBlock { 
    cd $using:PWD
    cd ..
    python -m tests.test_direct
}

# Monitor the job and output in real-time
$start = Get-Date
while ($job.State -eq "Running") {
    # Get any new output
    $output = Receive-Job -Job $job
    if ($output) {
        Write-Host $output
    }
    
    # Check if we've hit the timeout
    $elapsed = (Get-Date) - $start
    if ($elapsed.TotalSeconds -gt $timeout) {
        Write-Host "Direct test is taking too long, terminating..."
        Stop-Job -Job $job
        break
    }
    
    # Sleep briefly
    Start-Sleep -Seconds 1
}

# Output final results
$output = Receive-Job -Job $job
if ($output) {
    Write-Host $output
}

Remove-Job -Job $job -Force

# Run tool tests
Write-Host "Running tool tests..."
$job = Start-Job -ScriptBlock { 
    cd $using:PWD
    cd ..
    python -m tests.test_tools
}

# Monitor the job and output in real-time
$start = Get-Date
while ($job.State -eq "Running") {
    # Get any new output
    $output = Receive-Job -Job $job
    if ($output) {
        Write-Host $output
    }
    
    # Check if we've hit the timeout
    $elapsed = (Get-Date) - $start
    if ($elapsed.TotalSeconds -gt $timeout) {
        Write-Host "Tool test is taking too long, terminating..."
        Stop-Job -Job $job
        break
    }
    
    # Sleep briefly
    Start-Sleep -Seconds 1
}

# Output final results
$output = Receive-Job -Job $job
if ($output) {
    Write-Host $output
}

Remove-Job -Job $job -Force

# Run MCP client tests
Write-Host "Running MCP client tests..."
$job = Start-Job -ScriptBlock { 
    cd $using:PWD
    cd ..
    python -m tests.test_mcp_client
}

# Monitor the job and output in real-time
$start = Get-Date
while ($job.State -eq "Running") {
    # Get any new output
    $output = Receive-Job -Job $job
    if ($output) {
        Write-Host $output
    }
    
    # Check if we've hit the timeout
    $elapsed = (Get-Date) - $start
    if ($elapsed.TotalSeconds -gt $timeout) {
        Write-Host "MCP client test is taking too long, terminating..."
        Stop-Job -Job $job
        break
    }
    
    # Sleep briefly
    Start-Sleep -Seconds 1
}

# Output final results
$output = Receive-Job -Job $job
if ($output) {
    Write-Host $output
}

Remove-Job -Job $job -Force

# Clean up any leftover processes
$serverProcesses = Get-Process -Name pwsh | Where-Object { $_.CommandLine -like "*start_server.ps1*" }
if ($serverProcesses) {
    Write-Host "Cleaning up any remaining MCP server processes..."
    $serverProcesses | ForEach-Object { 
        Stop-Process -Id $_.Id -Force 
        Write-Host "Stopped process $($_.Id)"
    }
} 