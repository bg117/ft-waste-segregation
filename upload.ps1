param (
    [string[]]$src,
    [string]$dest,
    [switch]$usb,
    [switch]$ssh
)

# Determine IP address based on the first argument
if ($usb) {
    $ip = "192.168.7.2"
}
else {
    $ip = "192.168.8.2"
}

$delimSrcs = '"' + ($src -join '" "') + '"'

# Upload each file using SCP
$scpCommand = "scp -r $delimSrcs ft@${ip}:$dest"
Write-Host "Executing: $scpCommand"
Invoke-Expression $scpCommand

# SSH command to create a new session
if ($ssh) {
    $sshCommand = "ssh ft@$ip"
    Write-Host "Starting SSH session: $sshCommand"
    Invoke-Expression $sshCommand
}