# Read-only host report. Run in PowerShell; no administrator required.
$ErrorActionPreference = 'Stop'
$os = Get-CimInstance Win32_OperatingSystem
$cpu = Get-CimInstance Win32_Processor
[pscustomobject]@{
    Windows = $os.Caption
    Build = $os.BuildNumber
    Architecture = $os.OSArchitecture
    RAMGiB = [math]::Round($os.TotalVisibleMemorySize / 1MB, 1)
    VirtualizationEnabled = ($cpu.VirtualizationFirmwareEnabled -join ',')
} | Format-List
Get-Volume | Where-Object DriveLetter | Select-Object DriveLetter, FileSystem,
    @{N='FreeGiB';E={[math]::Round($_.SizeRemaining/1GB,1)}},
    @{N='TotalGiB';E={[math]::Round($_.Size/1GB,1)}} | Format-Table
if (Get-Command wsl.exe -ErrorAction SilentlyContinue) {
    wsl.exe --status
    wsl.exe --list --verbose
} else { Write-Output 'WSL command not available.' }
