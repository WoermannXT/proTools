# SortImages.ps1
$exifToolPath = "E:\exiftool\exiftool.exe"  # Path to exiftool.exe
$sourceFolder = "E:\40"   # Source folder containing images
$outputFolder = "E:\Res"  # Destination folder for sorted images

if (-not (Test-Path -Path $outputFolder -PathType Container)) {
    New-Item -ItemType Directory -Path $outputFolder | Out-Null
}

# Iterate through each image in the source folder
Get-ChildItem -Path $sourceFolder -Filter *.jpg | ForEach-Object {
	# Get GPS coordinates using ExifTool
	$gpsInfo = & $exifToolPath $_.FullName -gpslatitude -gpslongitude -n

	if ($gpsInfo -and $gpsInfo.Count -eq 2) {
		# Extract numeric degrees, minutes, and direction
		$latitudeDegrees = [regex]::Match($gpsInfo[0], '-?\d+').Value
		$latitudeMinutes = [regex]::Match($gpsInfo[0], '\d+\.\d+').Value.Split('.')[1].Substring(0, 3)
		#$latitudeDirection = [regex]::Match($gpsInfo[0], '[NSEW]').Value

		$longitudeDegrees = [regex]::Match($gpsInfo[1], '-?\d+').Value
		$longitudeMinutes = [regex]::Match($gpsInfo[1], '\d+\.\d+').Value.Split('.')[1].Substring(0, 3)
		#$longitudeDirection = [regex]::Match($gpsInfo[1], '[NSEW]').Value

		Write-Output "$latitudeMinutes_$longitudeMinutes"

		# Create destination folder based on coordinates
		$destinationFolder = $outputFolder
		# Direction
		#$destinationFolder = Join-Path $destinationFolder "$latitudeDirection"
		#if (-not (Test-Path -Path $destinationFolder -PathType Container)) {
		#	New-Item -ItemType Directory -Path $destinationFolder | Out-Null
		#}
		#$destinationFolder = Join-Path $destinationFolder "$longitudeDirection"
		#if (-not (Test-Path -Path $destinationFolder -PathType Container)) {
		#	New-Item -ItemType Directory -Path $destinationFolder | Out-Null
		#}
		#Degrees
		$destinationFolder = Join-Path $destinationFolder "$latitudeDegrees"
		if (-not (Test-Path -Path $destinationFolder -PathType Container)) {
			New-Item -ItemType Directory -Path $destinationFolder | Out-Null
		}
		$destinationFolder = Join-Path $destinationFolder "$longitudeDegrees"
		if (-not (Test-Path -Path $destinationFolder -PathType Container)) {
			New-Item -ItemType Directory -Path $destinationFolder | Out-Null
		}
		

		# Print the destination path
		Write-Output "Copying $_ to $destinationFolder"

		# Copy the image to the destination folder
		Copy-Item -Path $_.FullName -Destination $destinationFolder -Force
	}
}
