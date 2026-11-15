# Build ESP32_Git_CICD_Workshop.pptx through PowerPoint COM Automation.
# Input : content.json (titles + Thai speaker notes), lib-slides.ps1 (Build-s01..Build-s18), docs/images/*.png
# Output: docs/presentation/ESP32_Git_CICD_Workshop.pptx + PNG renders (1280x720) in docs/presentation/out/
param(
    [string]$Out = (Join-Path $PSScriptRoot 'ESP32_Git_CICD_Workshop.pptx'),
    [string]$OutDir = (Join-Path $PSScriptRoot 'out'),
    [int]$Pause = 200,
    [string]$Only = '',
    [switch]$NoSave,
    [string]$Leaf = 'none',
    [switch]$Decor,
    [string]$RefPptx = 'C:\ThClaws\ohters\NDRS_MODBUS_SIMULATOR\report\presentation\final\NDRS_จักรพันธ์_ModbusSim_แบบร่าง.pptx'
)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
. (Join-Path $PSScriptRoot 'lib-slides.ps1')

$items = (Get-Content (Join-Path $PSScriptRoot 'content.json') -Raw -Encoding UTF8 | ConvertFrom-Json) | ForEach-Object { $_ }

$app = New-Object -ComObject PowerPoint.Application
$app.Visible = -1

foreach ($old in @($app.Presentations)) {
    if (($old.Path -eq '' -and $old.Saved -eq 0) -or $old.FullName -eq $Out) {
        $old.Saved = -1
        $old.Close()
    }
}

$pp = $app.Presentations.Add(-1)
if ($null -eq $pp) { throw 'Presentations.Add returned null' }
$pp.PageSetup.SlideWidth = 960
$pp.PageSetup.SlideHeight = 540

$fs = $pp.SlideMaster.Theme.ThemeFontScheme
foreach ($ff in @($fs.MajorFont, $fs.MinorFont)) {
    $ff.Item(1).Name = $FONT
    $ff.Item(2).Name = $FONT
}

$summary = @(); $idx = 0
foreach ($it in $items) {
    $idx++
    if ($Only -ne '' -and (',' + $Only + ',') -notlike ('*,' + $it.id + ',*')) { continue }
    $script:clicks = 0
    if ($it.id -eq 's01' -and (Test-Path $RefPptx)) {
        [void]$pp.Slides.InsertFromFile($RefPptx, $pp.Slides.Count, 1, 1)
        $s = $pp.Slides.Item($pp.Slides.Count)
        $s.Shapes.Item('Text 1').TextFrame.TextRange.Text = 'Workshop · พ.ศ. 2569'
        $s.Shapes.Item('Text 2').TextFrame.TextRange.Text = 'การพัฒนาเฟิร์มแวร์ ESP32'
        $s.Shapes.Item('Text 3').TextFrame.TextRange.Text = 'ด้วย Git, Pre-commit, Unit Testing'
        $s.Shapes.Item('Text 4').TextFrame.TextRange.Text = 'และระบบ CI/CD อัตโนมัติ'
        $s.Shapes.Item('Text 5').TextFrame.TextRange.Text = 'ESP32 FIRMWARE ENGINEERING WORKSHOP'
        $s.Shapes.Item('Text 6').TextFrame.TextRange.Text = 'GIT REBASE · PRE-COMMIT · PLATFORMIO UNITY · GITHUB ACTIONS'
        $s.Shapes.Item('Text 8').TextFrame.TextRange.Text = 'DOIT ESP32 DevKit v1'
        $s.Shapes.Item('Text 9').TextFrame.TextRange.Text = 'GitHub Actions · PlatformIO · esptool merge-bin'
        $s.Shapes.Item('Text 10').TextFrame.TextRange.Text = '18 Slides · Hands-on Lab & Automated Verification'
        $s.Shapes.Item('Text 11').TextFrame.TextRange.Text = 'ESP32 Firmware Engineering · Git, Pre-commit, Testing & CI/CD Workshop'
        $s.Shapes.Item('Text 13').TextFrame.TextRange.Text = '1'
    } elseif ($it.id -eq 's18' -and (Test-Path $RefPptx)) {
        [void]$pp.Slides.InsertFromFile($RefPptx, $pp.Slides.Count, 39, 39)
        $s = $pp.Slides.Item($pp.Slides.Count)
        $s.Shapes.Item('Text 4').TextFrame.TextRange.Text = 'ESP32 Firmware Engineering · Git & CI/CD'
        $s.Shapes.Item('Text 9').TextFrame.TextRange.Text = '18'
    } else {
        $s = New-Slide $pp $it.id
        & ("Build-" + $it.id) $s $it $it.sec
        if ($Decor) { Add-Decor $s (11 * $idx) }
        Add-Border $s $Leaf
    }

    $nr = $s.NotesPage.Shapes.Placeholders.Item(2).TextFrame.TextRange
    $nr.Text = $it.notes
    $nr.Font.Name = $FONT
    $nr.Font.NameComplexScript = $FONT

    $pp.Windows.Item(1).View.GotoSlide($s.SlideIndex)
    Start-Sleep -Milliseconds $Pause
    $summary += "{0,2} {1,-5} clicks={2}" -f $s.SlideIndex, $it.id, $script:clicks
}

New-Item -ItemType Directory -Force $OutDir | Out-Null
$od = (Resolve-Path $OutDir).Path
Get-ChildItem $od -Filter 's*.png' | Remove-Item
foreach ($sl in $pp.Slides) {
    $sl.Export((Join-Path $od ('s{0:D2}.png' -f $sl.SlideIndex)), 'PNG', 1280, 720)
}

if (-not $NoSave) {
    $pp.SaveAs($Out, 24, -1)   # 24 = ppSaveAsOpenXMLPresentation; -1 embeds TrueType fonts
}

if ($script:warns.Count) {
    'OVERFLOW WARNINGS:'
    $script:warns
} else {
    'OVERFLOW WARNINGS: none'
}
$summary
"deck: $($pp.Name) slides=$($pp.Slides.Count) out=$Out"
if (-not $NoSave) { $pp.Close() }
