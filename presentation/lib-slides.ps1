# Helpers + one Build-<id> function per slide. Dot-sourced by build-slides.ps1.
# Theme & visual system matched directly to NDRS_MODBUS_SIMULATOR/report/presentation/lib-slides.ps1
$FONT = 'Leelawadee UI'
$MONO = 'Consolas'
$ImgDir = Join-Path $PSScriptRoot 'img'

function RGBc([string]$h) {
    $h = $h.TrimStart('#')
    return [Convert]::ToInt32($h.Substring(0,2),16) + 256*[Convert]::ToInt32($h.Substring(2,2),16) + 65536*[Convert]::ToInt32($h.Substring(4,2),16)
}

$NAVY   = RGBc '1F5F8B'
$BLUE   = RGBc '1F5F8B'
$SKY    = RGBc 'C9DDEE'
$SKY2   = RGBc 'A9C8E2'
$PALE   = RGBc 'E6EFF7'
$AMBER  = RGBc 'F0A93B'
$CREAM  = RGBc 'FDF7EC'
$CREAM2 = RGBc 'F6E7DF'
$WHITE  = RGBc 'FFFFFF'
$STEEL  = RGBc 'E6EFF7'
$RUN    = RGBc '2E8B57'
$FAULT  = RGBc 'C8413B'
$RUNT   = RGBc 'E3F2E9'
$FAULTT = RGBc 'FBE4E2'
$AMBERT = RGBc 'FDEFD6'
$DARK   = RGBc '1E293B'
$INK    = RGBc '111827'
$MUTED  = RGBc '64748B'

function New-Slide($pres, $id) {
    $s = $pres.Slides.Add($pres.Slides.Count + 1, 12)
    $s.FollowMasterBackground = 0
    $s.Background.Fill.Solid()
    $s.Background.Fill.ForeColor.RGB = $WHITE
    $script:onNavy = $false
    return $s
}

function Navy-Bg($s) {
    $s.Background.Fill.Solid()
    $s.Background.Fill.ForeColor.RGB = $NAVY
    $script:onNavy = $true
}

$script:warns = @()
$script:noFit = $false

function Fit($b, $min) {
    $tf = $b.TextFrame; $r = $tf.TextRange
    $w = $b.Width - $tf.MarginLeft - $tf.MarginRight
    $h = $b.Height - $tf.MarginTop - $tf.MarginBottom
    while (($r.BoundHeight -gt ($h + 1) -or $r.BoundWidth -gt ($w + 1)) -and $r.Font.Size -gt $min) {
        $r.Font.Size = [int]($r.Font.Size - 1)
    }
    if ($r.BoundHeight -gt ($h + 1) -or $r.BoundWidth -gt ($w + 1)) {
        $n = [Math]::Min(30, $r.Text.Length)
        $script:warns += ('s' + $b.Parent.SlideIndex + ' [' + $r.Font.Size + 'pt h=' + [int]$r.BoundHeight + '/' + [int]$h + '] ' + $r.Text.Substring(0, $n).Replace("`r", ' '))
    }
}

function Txt($s, $t, $l, $tp, $w, $h, $size, $color, $bold, $align, $anchor, $minSize) {
    if (-not $minSize) { $minSize = $(if ($size -lt 22) { 14 } else { 16 }) }
    $b = $s.Shapes.AddTextbox(1, $l, $tp, $w, $h)
    $tf = $b.TextFrame; $tf.WordWrap = -1; $tf.AutoSize = 0
    $tf.MarginLeft = 0; $tf.MarginRight = 0; $tf.MarginTop = 0; $tf.MarginBottom = 0
    $tf.VerticalAnchor = [int]$anchor
    $r = $tf.TextRange; $r.Text = $t
    $r.Font.Name = $FONT; $r.Font.NameComplexScript = $FONT; $r.Font.Size = $size
    $r.Font.Color.RGB = [int]$color; $r.Font.Bold = [int]$bold; $r.ParagraphFormat.Alignment = [int]$align
    $b.Height = $h
    if (-not $script:noFit) { Fit $b $minSize }
    return $b
}

function Heading($s, $main, $sub, $x, $y, $w, $align, $color) {
    $script:noFit = $true
    $b = Txt $s ($main + "`r" + $sub) $x $y $w 180 42 $color -1 $align 1
    $script:noFit = $false
    $b.TextFrame.TextRange.Paragraphs(2).Font.Size = 30
    $b.TextFrame.TextRange.Paragraphs(2).Font.Bold = 0
    $b.TextFrame.TextRange.ParagraphFormat.SpaceWithin = 0.88
    return $b
}

function Head($s, $it) {
    # Exact NDRS_จักรพันธ์_ModbusSim_แบบร่าง.pptx content-slide chrome
    [void](Box $s 1 0 0 960 14 $NAVY -1 0)
    [void](Box $s 9 838 28 6 6 $SKY -1 0)
    [void](Box $s 9 856 42 4 4 $SKY2 -1 0)
    [void](Box $s 9 872 26 8 8 $SKY -1 0)

    if ($it.sec) { [void](Txt $s $it.sec 40 22 760 22 14 $NAVY -1 1 3 12) }
    [void](Txt $s $it.title 40 46 840 46 32 $INK -1 1 3 22)
    [void](Box $s 1 40 96 48 3 $NAVY -1 0)
    if ($it.sub) { [void](Txt $s $it.sub 100 90 800 26 16 $MUTED 0 1 3 12) }

    [void](Box $s 1 40 462 880 1 $SKY -1 0)
    if ($it.sec) { [void](Txt $s $it.sec 40 468 420 20 12 $NAVY 0 1 3 11) }
    [void](Txt $s 'ESP32 Firmware Engineering · Workshop 2026' 470 468 450 20 12 $MUTED 0 3 3 11)
    [void](Box $s 1 0 512 960 28 $PALE -1 0)
    $pg = Box $s 5 886 514 44 22 $WHITE $SKY 1; $pg.Adjustments.Item(1) = 0.5
    [void](Txt $s "$($s.SlideIndex)" 886 514 44 22 12 $NAVY -1 2 3 10)
}

function Box($s, $shape, $l, $t, $w, $h, $fill, $line, $lw) {
    $x = $s.Shapes.AddShape($shape, $l, $t, $w, $h)
    if ($fill -ge 0) { $x.Fill.ForeColor.RGB = [int]$fill } else { $x.Fill.Visible = 0 }
    if ($line -ge 0) { $x.Line.ForeColor.RGB = [int]$line; $x.Line.Weight = [single]$lw } else { $x.Line.Visible = 0 }
    $x.Shadow.Visible = 0
    return $x
}

function Icon($s, $name, $x, $y, $sz, $color) {
    $p = Join-Path $PSScriptRoot "decor\$color\$name.svg"
    return $s.Shapes.AddPicture($p, 0, -1, $x, $y, $sz, $sz)
}

function Disc($s, $icon, $cx, $cy, $d) {
    $c = Box $s 9 ($cx - $d/2) ($cy - $d/2) $d $d $SKY -1 0
    return @($c, (Icon $s $icon ($cx - $d*0.28) ($cy - $d*0.28) ($d*0.56) 'navy'))
}

function Blob($s, $cx, $cy, $d, $fill) {
    return Box $s 9 ($cx - $d/2) ($cy - $d/2) $d $d $fill -1 0
}

function Cartoon($s, $id, $cx, $cy, $mw, $mh) {
    $p = Join-Path $PSScriptRoot "decor\soco\$id.png"
    $im = [System.Drawing.Image]::FromFile($p); $r = [Math]::Min($mw / $im.Width, $mh / $im.Height); $w = $im.Width * $r; $h = $im.Height * $r; $im.Dispose()
    return $s.Shapes.AddPicture($p, 0, -1, $cx - $w/2, $cy - $h/2, $w, $h)
}

function Card($s, $x, $y, $w, $h) {
    $c = Box $s 5 $x $y $w $h $WHITE $SKY 1.25
    $c.Adjustments.Item(1) = 0.07
    return $c
}

function Label($s, $text, $x, $y, $w, $h, $style) {
    switch ($style) {
        'solid' { $f = $NAVY;   $l = $NAVY;  $c = $WHITE }
        'dark'  { $f = $NAVY;   $l = $SKY;   $c = $WHITE }
        'amber' { $f = $AMBERT; $l = $AMBER; $c = $NAVY }
        default { $f = $WHITE;  $l = $NAVY;  $c = $NAVY }
    }
    $b = Box $s 5 $x $y $w $h $f $l 2.25; $b.Adjustments.Item(1) = 0.3
    $tf = $b.TextFrame; $tf.WordWrap = -1; $tf.MarginLeft = 10; $tf.MarginRight = 10; $tf.MarginTop = 2; $tf.MarginBottom = 2
    $tf.VerticalAnchor = 3
    $r = $tf.TextRange; $r.Text = $text; $r.Font.Name = $FONT; $r.Font.NameComplexScript = $FONT
    $r.Font.Size = 20; $r.Font.Bold = -1; $r.Font.Color.RGB = [int]$c; $r.ParagraphFormat.Alignment = 2
    Fit $b 13
    return $b
}

function Callout($s, $text, $lx, $ly, $lw, $lh, $tx, $ty) {
    $b = Label $s $text $lx $ly $lw $lh 'light'
    $cx = $lx + $lw/2; $cy = $ly + $lh/2
    if ([Math]::Abs($tx - $cx) / $lw -gt [Math]::Abs($ty - $cy) / $lh) {
        $sx = if ($tx -gt $cx) { $lx + $lw } else { $lx }; $sy = $cy
    } else {
        $sx = $cx; $sy = if ($ty -gt $cy) { $ly + $lh } else { $ly }
    }
    $ln = $s.Shapes.AddLine($sx, $sy, $tx, $ty)
    $ln.Line.ForeColor.RGB = $NAVY; $ln.Line.Weight = 2.25; $ln.Line.EndArrowheadStyle = 6
    $ln.Line.EndArrowheadLength = 3; $ln.Line.EndArrowheadWidth = 3
    return @($ln, $b)
}

function Node($s, $text, $x, $y, $w, $h, $style, $size) {
    if (-not $size) { $size = 20 }
    switch ($style) {
        'solid' { $f = $NAVY;   $l = -1;     $c = $WHITE }
        'acc'   { $f = $PALE;   $l = -1;     $c = $NAVY }
        'tint'  { $f = $STEEL;  $l = -1;     $c = $NAVY }
        'good'  { $f = $RUNT;   $l = $RUN;   $c = $NAVY }
        'bad'   { $f = $FAULTT; $l = $FAULT; $c = $NAVY }
        'amber' { $f = $AMBERT; $l = $AMBER; $c = $NAVY }
        default { $f = $WHITE;  $l = $NAVY;  $c = $NAVY }
    }
    $b = Box $s 5 $x $y $w $h $f $l 2; $b.Adjustments.Item(1) = 0.12
    $tf = $b.TextFrame; $tf.WordWrap = -1; $tf.MarginLeft = 8; $tf.MarginRight = 8; $tf.MarginTop = 3; $tf.MarginBottom = 3; $tf.VerticalAnchor = 3
    $r = $tf.TextRange; $r.Text = $text; $r.Font.Name = $FONT; $r.Font.NameComplexScript = $FONT
    $r.Font.Size = $size; $r.Font.Bold = -1; $r.Font.Color.RGB = [int]$c; $r.ParagraphFormat.Alignment = 2
    Fit $b 13
    return $b
}

function Arr($s, $x1, $y1, $x2, $y2, $col) {
    if (-not $col) { $col = $NAVY }
    $ln = $s.Shapes.AddLine($x1, $y1, $x2, $y2)
    $ln.Line.ForeColor.RGB = [int]$col; $ln.Line.Weight = 2.5; $ln.Line.EndArrowheadStyle = 2
    $ln.Line.EndArrowheadLength = 2; $ln.Line.EndArrowheadWidth = 2
    return $ln
}

function CodeBox($s, $code, $x, $y, $w, $h, $size) {
    if (-not $size) { $size = 13 }
    $b = Box $s 5 $x $y $w $h $DARK $NAVY 1.5; $b.Adjustments.Item(1) = 0.04
    $tf = $b.TextFrame; $tf.WordWrap = -1; $tf.MarginLeft = 10; $tf.MarginRight = 10; $tf.MarginTop = 6; $tf.MarginBottom = 6; $tf.VerticalAnchor = 1
    $r = $tf.TextRange; $r.Text = $code
    $r.Font.Name = $MONO; $r.Font.NameComplexScript = $FONT
    $r.Font.Size = $size; $r.Font.Bold = 0; $r.Font.Color.RGB = $WHITE; $r.ParagraphFormat.Alignment = 1
    Fit $b 10
    return $b
}

function Corner($s, $pos, $right) {
    # Footer and slide number are already rendered by Head (NDRS chrome)
}

function Step($s, $shapes) {
    $first = $true
    foreach ($sh in @($shapes)) {
        $e = $s.TimeLine.MainSequence.AddEffect($sh, 10, 0, $(if ($first) { 1 } else { 2 }))
        $e.Timing.Duration = 0.5; $first = $false
    }
    $script:clicks++
}

function Pic($s, $name, $x, $y, $w, $angle) {
    $p = Join-Path $ImgDir $name
    if (-not (Test-Path $p)) { throw "Image not found: $p" }
    $im = [System.Drawing.Image]::FromFile($p); $h = $w * $im.Height / $im.Width; $im.Dispose()
    $c = Box $s 5 ($x-8) ($y-8) ($w+16) ($h+16) $WHITE $PALE 1.5; $c.Adjustments.Item(1) = 0.03
    $pic = $s.Shapes.AddPicture($p, 0, -1, $x, $y, $w, $h)
    if ($angle -ne 0) { $c.Rotation = $angle; $pic.Rotation = $angle }
    return @($c, $pic)
}

function Flat($parts) {
    $o = New-Object System.Collections.ArrayList
    foreach ($p in $parts) { foreach ($q in @($p)) { [void]$o.Add($q) } }
    return $o.ToArray()
}

function Add-Border($s, $mode) {
    if ($mode -eq 'none') { return }
    $cols = if ($mode -eq 'green') { @('g1', 'g2', 'g3') } elseif ($script:onNavy) { @('sky', 'white', 'blue') } else { @('navy', 'blue', 'sky') }
    $names = @('eco', 'spa', 'grass', 'psychiatry', 'nest_eco_leaf')
    $rnd = New-Object System.Random 7
    foreach ($edge in 'top', 'bottom') {
        $x = -10
        while ($x -lt 960) {
            $sz = 72 + $rnd.Next(0, 26)
            $y = if ($edge -eq 'top') { -$sz * 0.62 + $rnd.Next(0, 6) } else { 518 - $rnd.Next(0, 6) }
            $pic = Icon $s $names[$rnd.Next(0, $names.Count)] $x $y $sz $cols[$rnd.Next(0, $cols.Count)]
            $pic.Rotation = [single]($rnd.Next(0, 360))
            $x += 62 + $rnd.Next(0, 36)
        }
    }
}

$DecorCols = @('F0A93B', '3CC2B4', 'F58A7A', 'A596E8', '7CCB6B', 'FFD166')
function Flower($s, $cx, $cy, $d, $petal, $core) {
    $p = $d * 0.42; $r = $d * 0.27
    $parts = foreach ($k in 0..4) {
        $a = $k * 72 * [Math]::PI / 180
        $o = Box $s 9 ($cx + $r * [Math]::Sin($a) - $p/2) ($cy - $r * [Math]::Cos($a) - $p/2) $p $p $petal -1 0
        $o.Name
    }
    $c = Box $s 9 ($cx - $d*0.17) ($cy - $d*0.17) ($d*0.34) ($d*0.34) $core -1 0
    return $s.Shapes.Range([object[]](@($parts) + $c.Name)).Group()
}

function Add-Decor($s, $seed) {
    $busy = foreach ($sh in $s.Shapes) { ,@($sh.Left, $sh.Top, ($sh.Left + $sh.Width), ($sh.Top + $sh.Height)) }
    $rnd = New-Object System.Random $seed
    $kinds = @('star5', 'flower', 'star4', 'cloud', 'wave', 'star5', 'dot', 'flower', 'star4', 'dot')
    $placed = New-Object System.Collections.ArrayList
    $tries = 0; $k = 0
    while ($placed.Count -lt 8 -and $tries -lt 900) {
        $tries++
        $kind = $kinds[$k % $kinds.Count]
        $sz = switch ($kind) { 'cloud' { 64 } 'wave' { 90 } 'flower' { 30 + $rnd.Next(0, 10) } 'dot' { 10 + $rnd.Next(0, 6) } default { 18 + $rnd.Next(0, 14) } }
        $h = switch ($kind) { 'cloud' { 40 } 'wave' { 20 } default { $sz } }
        $e = $rnd.Next(0, 4); $b = $rnd.Next(6, 90)
        $x = if ($e -eq 0) { $b } elseif ($e -eq 1) { 954 - $sz - $b } else { $rnd.Next(6, [int](954 - $sz)) }
        $y = if ($e -eq 2) { $b } elseif ($e -eq 3) { 534 - $h - $b } else { $rnd.Next(6, [int](534 - $h)) }
        $m = if ($script:bigGap) { 36 } else { 12 }
        $hit = $false
        foreach ($r in @($busy) + @($placed)) { if ($x - $m -lt $r[2] -and $x + $sz + $m -gt $r[0] -and $y - $m -lt $r[3] -and $y + $h + $m -gt $r[1]) { $hit = $true; break } }
        if ($hit) { continue }
        $col = RGBc $DecorCols[$rnd.Next(0, $DecorCols.Count)]
        switch ($kind) {
            'star5'  { $x2 = Box $s 92 $x $y $sz $sz $col -1 0; $x2.Rotation = [single]$rnd.Next(-20, 20) }
            'star4'  { [void](Box $s 91 $x $y $sz $sz $col -1 0) }
            'flower' { [void](Flower $s ($x + $sz/2) ($y + $sz/2) $sz $col (RGBc 'FFD166')) }
            'cloud'  { [void](Box $s 179 $x $y $sz $h $(if ($script:onNavy) { RGBc '9CC5FF' } else { RGBc 'DCE8F8' }) -1 0) }
            'wave'   { [void](Box $s 103 $x $y $sz $h $col -1 0) }
            'dot'    { [void](Box $s 9 $x $y $sz $sz $col -1 0) }
        }
        [void]$placed.Add(@(($x - 40), ($y - 40), ($x + $sz + 40), ($y + $h + 40)))
        $k++
    }
    $script:bigGap = $false
}

# ==================== SLIDES s01 .. s18 (NDRS Theme + Image-First) ====================

function Build-s01($s, $it, $pos) {
    $script:bigGap = $true
    [void](Blob $s 740 270 440 $STEEL)
    [void](Cartoon $s 15162 740 270 340 290)
    $script:noFit = $true
    $h = Txt $s ($it.title + "`r" + $it.sub) 50 60 560 230 50 $NAVY -1 1 1
    $script:noFit = $false
    $h.TextFrame.TextRange.Paragraphs(2).Font.Bold = 0
    [void](Txt $s 'DOIT ESP32 DevKit v1 (esp32doit)' 50 340 560 44 30 $NAVY -1 1 3)
    [void](Txt $s 'Workshop 2026' 50 390 560 44 30 $NAVY 0 1 3)
}

function Build-s02($s, $it, $pos) {
    Head $s $it
    $st = @(
        @('1. Dev', 'Issue + Branch', 'tint'),
        @('2. Local Gate', 'Pre-commit', 'amber'),
        @('3. GitHub CI', 'Lint + Test + Build', 'acc'),
        @('4. Release', 'Tag -> .bin', 'solid')
    )
    $k = 0
    foreach ($e in $st) {
        $x = 40 + $k * 228; $k++
        $n = Node $s "$($e[0])`r$($e[1])" $x 128 200 78 $e[2] 18
        $parts = @($n)
        if ($k -lt 4) { $parts += (Arr $s ($x + 202) 167 ($x + 226) 167) }
        Step $s $parts
    }
    $p = Pic $s 'gh-01-repo-fork.png' 50 214 325 0
    $p2 = Pic $s 'gh-04-actions.png' 595 214 280 0
    Step $s (Flat @($p, $p2))
    Step $s (Callout $s "จับบั๊กในเครื่องก่อน`r-> ผ่าน CI บน Cloud" 392 285 186 76 590 322)
    Corner $s $pos $false
}

function Build-s03($s, $it, $pos) {
    Head $s $it
    $g = @(
        @('zap', '1. Fast Local (<3s)', 'clang-format · check-yaml · commit-msg'),
        @('cpu', '2. Cloud Unit & Build', 'pio test -e native -> pio run esp32'),
        @('shield-check', '3. Release (Tag v*)', 'esptool merge-bin -> GitHub Release')
    )
    $y = 132
    foreach ($e in $g) {
        $cd = Card $s 40 $y 420 100
        $dc = Disc $s $e[0] 90 ($y + 50) 56
        $t1 = Txt $s $e[1] 134 ($y + 12) 316 34 20 $NAVY -1 1 3 15
        $t2 = Txt $s $e[2] 134 ($y + 48) 316 42 15 $NAVY 0 1 1 12
        Step $s (Flat @($cd, $dc, $t1, $t2))
        $y += 112
    }
    $pic = Pic $s 'vid-actions-ci.png' 485 138 430 0
    Step $s $pic
    Step $s (Callout $s 'Fail Fast: เทสบน PC ก่อนลงบอร์ด' 520 404 360 48 640 360)
    Corner $s $pos $false
}

function Build-s04($s, $it, $pos) {
    Head $s $it
    $c1 = Card $s 40 132 410 148
    $i1 = Icon $s 'network' 54 146 36 'navy'
    $t1 = Txt $s "GitHub Marketplace & Official actions/*`ractions/checkout@v7 · actions/cache@v6`rastral-sh/setup-uv@v10.3.3" 102 142 336 128 16 $NAVY 0 1 3 13
    Step $s @($c1, $i1, $t1)

    $c2 = Card $s 40 296 410 148
    $i2 = Icon $s 'shield-check' 54 310 36 'navy'
    $t2 = Txt $s "pre-commit.com/hooks.html`rpre-commit-hooks (v6.0.0)`rmirrors-clang-format (v23.1.5)`rconventional-pre-commit (v4.5.0)" 102 306 336 128 16 $NAVY 0 1 3 13
    Step $s @($c2, $i2, $t2)

    $pic = Pic $s 'vid-gh-ci-yml.png' 475 138 440 0
    Step $s $pic
    Step $s (Callout $s 'Pin Version เสมอ (@v7, @v10.3.3)' 500 406 380 48 680 350)
    Corner $s $pos $false
}

function Build-s05($s, $it, $pos) {
    Head $s $it
    $steps = @('1. Issue', '2. Branch', '3. Commit', '4. Rebase', '5. PR & CI', '6. Release')
    $k = 0
    foreach ($st in $steps) {
        $x = 40 + $k * 148; $k++
        $style = if ($k -eq 4) { 'amber' } elseif ($k -eq 6) { 'solid' } else { 'acc' }
        $n = Node $s $st $x 128 130 48 $style 17
        $parts = @($n)
        if ($k -lt 6) { $parts += (Arr $s ($x + 132) 152 ($x + 146) 152) }
        Step $s $parts
    }
    $pic = Pic $s 'vid-gitflow.png' 110 192 520 0
    Step $s $pic
    Step $s (Callout $s 'Rebase ก่อนเปิด PR -> ประวัติเส้นตรง' 650 260 270 72 520 290)
    Corner $s $pos $false
}

function Build-s06($s, $it, $pos) {
    Head $s $it
    $p1 = Pic $s 'gh-02-issue-templates.png' 45 126 405 0
    Step $s $p1
    $p2 = Pic $s 'gh-02-issues.png' 495 126 405 0
    Step $s $p2
    Step $s (Callout $s 'bug_report.yml + feature_request.yml + config.yml (validations: required)' 80 414 800 42 260 375)
    Corner $s $pos $false
}

function Build-s07($s, $it, $pos) {
    Head $s $it
    $syn = Node $s '<type>(<scope>): <description>   |   feat:  fix:  docs:  test:  ci:  chore:' 40 128 880 54 'solid' 19
    Step $s @($syn)

    $pic = Pic $s 'vid-gitflow.png' 48 196 470 0
    Step $s $pic

    $c1 = Card $s 545 196 375 186
    $t1 = Txt $s "ประโยชน์ของ Conventional Commits`r• ไล่ประวัติ git log เข้าใจทันที`r• Pre-commit ตรวจรูปแบบอัตโนมัติ`r• release.yml สร้าง Release Notes ให้เอง" 563 206 340 166 17 $NAVY 0 1 3 13
    Step $s @($c1, $t1)
    Step $s (Callout $s 'ตัวอย่าง: feat(blink): fast mode' 545 404 375 50 480 340)
    Corner $s $pos $false
}

function Build-s08($s, $it, $pos) {
    Head $s $it
    $p1 = Pic $s 'vid-pre-commit.png' 40 124 415 0
    Step $s $p1
    $p2 = Pic $s 'term-02-pre-commit.png' 40 360 440 0
    Step $s $p2
    $cb = CodeBox $s "# .pre-commit-config.yaml`rrepos:`r  - repo: .../pre-commit-hooks (v6.0.0)`r  - repo: .../mirrors-clang-format (v23.1.5)`r  - repo: .../conventional-pre-commit (v4.5.0)`r    stages: [commit-msg]`r`r# .clang-format`rBasedOnStyle: Google | IndentWidth: 2" 495 124 425 236 12
    Step $s @($cb)
    Step $s (Callout $s 'ผ่านทุกด่านในเครื่องก่อนเกิด commit' 520 388 380 48 450 412)
    Corner $s $pos $false
}

function Build-s09($s, $it, $pos) {
    Head $s $it
    $n1 = Node $s 'Merge: สร้าง Merge Commit ซ้ำซ้อน' 40 128 425 50 'bad' 18
    $n2 = Node $s 'Rebase: git rebase origin/main (เส้นตรง)' 495 128 425 50 'good' 18
    Step $s @($n1, $n2)

    $p1 = Pic $s 'vid-gitflow.png' 40 190 425 0
    $p2 = Pic $s 'term-01-git-log.png' 495 230 425 0
    Step $s (Flat @($p1, $p2))
    Step $s (Callout $s 'git log --oneline --graph เส้นตรง 100%' 500 356 410 52 680 320)
    Corner $s $pos $false
}

function Build-s10($s, $it, $pos) {
    Head $s $it
    $p1 = Pic $s 'gh-03-pr-detail.png' 45 126 405 0
    Step $s $p1
    $p2 = Pic $s 'gh-03-pulls.png' 495 126 405 0
    Step $s $p2
    Step $s (Callout $s 'pull_request_template.md · Closes #2 · ล็อก Merge จนกว่า CI เขียว + ลบ branch' 60 414 840 42 260 375)
    Corner $s $pos $false
}

function Build-s11($s, $it, $pos) {
    Head $s $it
    $n1 = Node $s "Pure Logic (PC / Cloud)`rlib/blink_math/blink_math.cpp" 40 136 390 88 'good' 18
    $n2 = Node $s "Hardware (ESP32 Arduino)`rsrc/main.cpp (GPIO / delay)" 40 246 390 88 'tint' 18
    $n3 = Node $s "รัน Unity Unit Test ([env:native])`rใช้เวลา < 1 วินาที ไม่ต้องต่อบอร์ด" 40 356 390 88 'solid' 18
    Step $s @($n1, $n2)
    Step $s @($n3)

    $pic = Pic $s 'vid-pio-test.png' 460 136 460 0
    Step $s $pic
    Step $s (Callout $s 'แยก Logic ออกมา -> เทสไวระดับมิลลิวินาที' 480 412 420 48 640 370)
    Corner $s $pos $false
}

function Build-s12($s, $it, $pos) {
    Head $s $it
    $ini = "[env:esp32doit-devkit-v1]`rplatform = espressif32`rframework = arduino`rtest_filter = test_esp32`r`r[env:native]`rplatform = native`rtest_build_src = no`rtest_filter = test_native"
    $cb = CodeBox $s $ini 40 132 410 198 13
    Step $s @($cb)

    $n1 = Node $s "test_native/test_main.cpp -> pio test -e native`rtest_esp32/test_hardware.cpp -> pio run -e esp32doit-devkit-v1" 40 346 410 86 'acc' 15
    Step $s @($n1)

    $pic = Pic $s 'term-03-pio-build.png' 475 138 445 0
    Step $s $pic
    Step $s (Callout $s 'ผลบิลด์ & เทสจริงบน PlatformIO' 510 410 380 44 690 380)
    Corner $s $pos $false
}

function Build-s13($s, $it, $pos) {
    Head $s $it
    $p1 = Pic $s 'vid-gh-ci-yml.png' 40 134 450 0
    Step $s $p1

    $c1 = Node $s "1. Triggers (on:)`rpush: [main, release/**] · pull_request: [main]" 515 134 405 84 'amber' 16
    $c2 = Node $s "2. Jobs & Runner`rjobs: lint / unit-test · runs-on: ubuntu-latest" 515 234 405 84 'acc' 16
    $c3 = Node $s "3. Steps: uses: vs run:`ruses: actions/checkout@v7 · run: pio test -e native" 515 334 405 84 'good' 16
    Step $s @($c1, $c2, $c3)
    Step $s (Callout $s 'working-directory: workshop' 120 412 310 48 240 360)
    Corner $s $pos $false
}

function Build-s14($s, $it, $pos) {
    Head $s $it
    $c1 = Node $s "1. Parallel & needs:`rlint + test-native -> needs: build-esp32" 40 134 415 86 'acc' 17
    $c2 = Node $s "2. Cache (actions/cache@v6)`r~/.platformio + hashFiles('platformio.ini')" 40 236 415 86 'amber' 17
    $c3 = Node $s "3. Artifacts (upload-artifact@v7)`rเก็บ .bin บน release/** (7 วัน)" 40 338 415 86 'good' 17
    Step $s @($c1, $c2, $c3)

    $pic = Pic $s 'gh-05-actions-graph.png' 485 130 415 0
    Step $s $pic
    Step $s (Callout $s 'กราฟ Pipeline จริงบน GitHub Actions' 510 412 380 42 680 370)
    Corner $s $pos $false
}

function Build-s15($s, $it, $pos) {
    Head $s $it
    $p1 = Pic $s 'vid-actions-release.png' 40 130 430 0
    Step $s $p1
    $p2 = Pic $s 'gh-05-releases.png' 530 124 340 0
    Step $s $p2
    Step $s (Callout $s 'Tag v*.*.* + permissions: contents: write -> esptool merge-bin (0x0) -> action-gh-release@v3' 40 412 680 42 260 360)
    Corner $s $pos $true
}

function Build-s16($s, $it, $pos) {
    Head $s $it
    $c1 = Card $s 40 132 435 142
    $i1 = Icon $s 'activity' 56 148 38 'navy'
    $t1 = Txt $s "1. Pre-check: uv run exercises/check_env.py`rตรวจ Git, Python, pre-commit, gh, PlatformIO, gcc`rแจ้งจุดที่ขาดก่อนเริ่ม Workshop" 106 142 355 122 17 $NAVY 0 1 3 13
    Step $s @($c1, $i1, $t1)

    $c2 = Card $s 40 292 435 156
    $i2 = Icon $s 'shield-check' 56 308 38 'navy'
    $t2 = Txt $s "2. Self-check: uv run exercises/verify.py`rตรวจคำตอบครบ 6 Modules อัตโนมัติ`rBranch, Commits, YAML, Pre-commit, pio test & CI" 106 302 355 136 17 $NAVY 0 1 3 13
    Step $s @($c2, $i2, $t2)

    $pic = Pic $s 'term-04-verify.png' 520 126 350 0
    Step $s $pic
    Step $s (Callout $s 'นักเรียนตรวจ PASS ด้วยตัวเอง' 515 414 360 40 680 380)
    Corner $s $pos $false
}

function Build-s17($s, $it, $pos) {
    Head $s $it
    $g = @(
        @('Repo & Templates', '.github/ISSUE_TEMPLATE/*.yml & PR template', ''),
        @('Pre-commit & Format', '.pre-commit-config.yaml + .clang-format', ''),
        @('Linear Git Flow', 'Conventional Commits + git rebase origin/main', ''),
        @('Testable Design', 'แยก Pure Logic ออกจาก Hardware -> [env:native]', 'amber'),
        @('CI Pipeline (ci.yml)', 'lint -> unit-test -> build + cache & pin version', ''),
        @('Release CD (release.yml)', 'Tag v*.*.* + esptool merge-bin -> Release', 'good')
    )
    $k = 0
    foreach ($e in $g) {
        $x = 40 + ($k % 2) * 450; $y = 144 + [int][Math]::Floor($k / 2) * 112; $k++
        $c = Box $s 5 $x $y 430 98 $WHITE $STEEL 1.5; $c.Adjustments.Item(1) = 0.08
        $parts = @($c)
        if ($e[2]) { $parts += (Box $s 1 $x ($y + 8) 8 82 $(if ($e[2] -eq 'amber') { $AMBER } else { $RUN }) -1 0) }
        $b = Box $s 9 ($x + 18) ($y + 24) 48 48 $STEEL -1 0
        $b.TextFrame.TextRange.Text = "$k"; $b.TextFrame.TextRange.Font.Name = $FONT; $b.TextFrame.TextRange.Font.NameComplexScript = $FONT
        $b.TextFrame.TextRange.Font.Size = 24; $b.TextFrame.TextRange.Font.Bold = -1; $b.TextFrame.TextRange.Font.Color.RGB = $NAVY
        $b.TextFrame.MarginLeft = 0; $b.TextFrame.MarginRight = 0; $b.TextFrame.MarginTop = 0; $b.TextFrame.MarginBottom = 0
        $parts += $b
        $parts += (Txt $s $e[0] ($x + 80) ($y + 10) 336 34 21 $NAVY -1 1 3 15)
        $parts += (Txt $s $e[1] ($x + 80) ($y + 46) 336 42 15 $NAVY 0 1 1 12)
        Step $s $parts
    }
    Corner $s $pos $false
}

function Build-s18($s, $it, $pos) {
    $script:bigGap = $true
    [void](Blob $s 740 270 440 $STEEL)
    [void](Cartoon $s 27646 740 270 340 290)
    $script:noFit = $true
    $h = Txt $s ($it.title + "`r" + $it.sub) 50 120 560 260 88 $NAVY -1 1 1
    $script:noFit = $false
    $h.TextFrame.TextRange.Paragraphs(2).Font.Size = 66
}
