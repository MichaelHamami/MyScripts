
$device1 = "Speakers (Logitech G533 Gaming Headset)"
$device2 = "Speakers (High Definition Audio Device)"

$Audio = Get-AudioDevice -playback

if ($Audio.Name.StartsWith($device1)) {
    Write-Output "Audio device now set to $device2" 
   (Get-AudioDevice -list | Where-Object Name -like ("$device2*") | Set-AudioDevice).Name
}  Else {
    Write-Output "Audio device now set to $device1"
   (Get-AudioDevice -list | Where-Object Name -like ("$device1*") | Set-AudioDevice).Name
}

Stop-Process -Name "powershell" -Force