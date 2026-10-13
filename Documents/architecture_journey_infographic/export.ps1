$ErrorActionPreference = 'Stop'
$outDir = $PSScriptRoot
$chrome = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
$profile = Join-Path $env:TEMP 'axion-infographic-chrome'
$htmlUri = ([System.Uri](Join-Path $outDir 'architecture_journey.html')).AbsoluteUri
$baseArgs = @('--headless', '--disable-gpu', '--no-first-run', "--user-data-dir=$profile")
& $chrome @baseArgs --no-pdf-header-footer "--print-to-pdf=$outDir\architecture_journey.pdf" $htmlUri | Out-Null
foreach ($svg in Get-ChildItem -LiteralPath $outDir -Filter '*.svg') {
    $svgUri = ([System.Uri]$svg.FullName).AbsoluteUri
    & $chrome @baseArgs "--screenshot=$outDir\$($svg.BaseName).png" --window-size=1600,1000 --hide-scrollbars $svgUri | Out-Null
}
