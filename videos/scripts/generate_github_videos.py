#!/usr/bin/env python3
"""
Generate 6 crisp 1280x720 @ 24fps "Liquid & Morphing Motion" 2D Vector MP4s
in videos/github/ explaining each file in .github/ (referencing docs/solutions/.github/).
Rendered at 2x Supersampling (2560x1440) and downscaled via LANCZOS to 1280x720
for razor-sharp anti-aliased Bezier curves, organic morphing blobs, and liquid droplets.
"""

import math
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Callable, List, Tuple

from PIL import Image, ImageDraw, ImageFont

OUT_W, OUT_H = 1280, 720
S = 2  # 2x Supersampling
WIDTH, HEIGHT = OUT_W * S, OUT_H * S  # 2560x1440
FPS = 24

# Snow & Arctic Blue Palette
BG = "#F4F8FC"
BLOB_1 = "#E6F0FD"
BLOB_2 = "#DFF1FE"
BLOB_3 = "#EDF5FF"
SURFACE = "#FFFFFF"
SURFACE_ALT = "#F8FAFC"
SHADOW = "#DBEAFE"
BORDER = "#BFDBFE"
BORDER_MUTED = "#CBD5E1"

TEXT = "#0F172A"
TEXT_SUB = "#334155"
TEXT_MUTED = "#64748B"

NAVY = "#1E3A8A"
ROYAL = "#1D4ED8"
BLUE = "#2563EB"
SKY = "#0284C7"
BLUE_SOFT = "#EFF6FF"
BLUE_TINT = "#DBEAFE"

PASS_FG = "#059669"
PASS_BG = "#ECFDF5"
BLOCK_FG = "#DC2626"
BLOCK_BG = "#FEF2F2"


def load_font(size: int, bold: bool = False, mono: bool = False) -> ImageFont.FreeTypeFont:
    sz = size * S
    if mono:
        candidates = (
            [r"C:\Windows\Fonts\consolab.ttf", r"C:\Windows\Fonts\consola.ttf"]
            if bold
            else [r"C:\Windows\Fonts\consola.ttf", r"C:\Windows\Fonts\cour.ttf"]
        )
    else:
        candidates = (
            [
                r"C:\Windows\Fonts\LeelaUIb.ttf",
                r"C:\Windows\Fonts\tahomabd.ttf",
                r"C:\Windows\Fonts\segoeuib.ttf",
            ]
            if bold
            else [
                r"C:\Windows\Fonts\LeelawUI.ttf",
                r"C:\Windows\Fonts\tahoma.ttf",
                r"C:\Windows\Fonts\segoeui.ttf",
            ]
        )
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, sz)
    return ImageFont.load_default()


F_TITLE = load_font(24, bold=True)
F_SUB = load_font(16, bold=False)
F_HEAD = load_font(19, bold=True)
F_BODY = load_font(16, bold=False)
F_BODY_B = load_font(16, bold=True)
F_SMALL = load_font(14, bold=False)
F_SMALL_B = load_font(14, bold=True)
F_CODE = load_font(14, bold=False, mono=True)
F_CODE_B = load_font(14, bold=True, mono=True)
F_MONO_B = load_font(15, bold=True, mono=True)


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def seg_t(t: float, start: float, end: float) -> float:
    if end <= start:
        return 1.0 if t >= end else 0.0
    return clamp01((t - start) / (end - start))


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def ease_out_cubic(t: float) -> float:
    t = clamp01(t)
    return 1.0 - (1.0 - t) ** 3


def ease_in_out_cubic(t: float) -> float:
    t = clamp01(t)
    return 4 * t * t * t if t < 0.5 else 1 - ((-2 * t + 2) ** 3) / 2


def spring_ease(t: float) -> float:
    """Smooth slightly bouncy spring easing for morphing containers."""
    t = clamp01(t)
    if t >= 1.0:
        return 1.0
    return 1.0 - math.exp(-7.0 * t) * math.cos(5.5 * t)


def overshoot_settle(t: float) -> float:
    """#48 Overshoot/Settle: eases past 1.0 slightly then settles cleanly at 1.0."""
    t = clamp01(t)
    if t >= 1.0:
        return 1.0
    c1 = 1.70158
    c3 = c1 + 1.0
    return 1.0 + c3 * ((t - 1.0) ** 3) + c1 * ((t - 1.0) ** 2)


def hex_to_rgb(h: str) -> Tuple[int, int, int]:
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def mix_color(c_bg: str, c_fg: str, alpha: float) -> str:
    a = clamp01(alpha)
    r1, g1, b1 = hex_to_rgb(c_bg)
    r2, g2, b2 = hex_to_rgb(c_fg)
    return f"#{int(r1 + (r2 - r1) * a):02x}{int(g1 + (g2 - g1) * a):02x}{int(b1 + (b2 - b1) * a):02x}"


# --- Liquid Background Blobs & Cubic Bezier Streams ---

def draw_organic_blob(
    draw: ImageDraw.ImageDraw,
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    t_raw: float,
    phase: float,
    fill: str,
    n_pts: int = 48,
) -> None:
    pts = []
    ang_base = t_raw * math.tau + phase
    for i in range(n_pts):
        theta = (i / n_pts) * math.tau
        wobble = (
            1.0
            + 0.12 * math.sin(3 * theta + ang_base)
            + 0.08 * math.cos(2 * theta - ang_base * 1.3)
            + 0.05 * math.sin(5 * theta + ang_base * 0.7)
        )
        px = cx + rx * wobble * math.cos(theta)
        py = cy + ry * wobble * math.sin(theta)
        pts.append((px, py))
    draw.polygon(pts, fill=fill)


def draw_liquid_bg(draw: ImageDraw.ImageDraw, t_raw: float) -> None:
    # 3 morphing organic snow-blue blobs drifting behind the cards
    draw_organic_blob(
        draw,
        (260 + 80 * math.sin(t_raw * math.tau)) * S,
        (220 + 50 * math.cos(t_raw * math.tau)) * S,
        340 * S,
        240 * S,
        t_raw,
        0.0,
        BLOB_1,
    )
    draw_organic_blob(
        draw,
        (1020 + 70 * math.cos(t_raw * math.tau)) * S,
        (480 + 55 * math.sin(t_raw * math.tau)) * S,
        360 * S,
        260 * S,
        t_raw,
        2.1,
        BLOB_2,
    )
    draw_organic_blob(
        draw,
        (640 + 90 * math.sin(t_raw * math.tau + 1.2)) * S,
        (140 + 35 * math.cos(t_raw * math.tau * 2)) * S,
        280 * S,
        160 * S,
        t_raw,
        4.2,
        BLOB_3,
    )


def cubic_bezier_pt(
    p0: Tuple[float, float], p1: Tuple[float, float], p2: Tuple[float, float], p3: Tuple[float, float], u: float
) -> Tuple[float, float]:
    m = 1.0 - u
    x = m**3 * p0[0] + 3 * m**2 * u * p1[0] + 3 * m * u**2 * p2[0] + u**3 * p3[0]
    y = m**3 * p0[1] + 3 * m**2 * u * p1[1] + 3 * m * u**2 * p2[1] + u**3 * p3[1]
    return x, y


def draw_liquid_stream(
    draw: ImageDraw.ImageDraw,
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    color: str,
    t_raw: float,
    stream_p: float = 1.0,
    n_droplets: int = 3,
) -> None:
    """Draw a flexible Cubic Bezier stream with flowing liquid droplets."""
    dx = (x1 - x0) * 0.55
    wave = 18 * S * math.sin(t_raw * math.tau * 2.0)
    p0 = (x0, y0)
    p1 = (x0 + dx, y0 + wave)
    p2 = (x1 - dx, y1 - wave)
    p3 = (x1, y1)

    steps = 28
    max_i = max(1, int(steps * clamp01(stream_p)))
    pts = [cubic_bezier_pt(p0, p1, p2, p3, i / steps) for i in range(max_i + 1)]
    if len(pts) >= 2:
        draw.line(pts, fill=color, width=4 * S, joint="curve")

    # Flowing droplets along the Bezier curve
    if stream_p > 0.25:
        for k in range(n_droplets):
            u = (t_raw * 2.4 + k / n_droplets) % 1.0
            if u <= stream_p:
                bx, by = cubic_bezier_pt(p0, p1, p2, p3, u)
                r = (7.0 - 2.5 * u) * S
                draw.ellipse([bx - r, by - r, bx + r, by + r], fill=color)
                # Inner bright core
                rc = r * 0.45
                draw.ellipse([bx - rc, by - rc, bx + rc, by + rc], fill="#FFFFFF")


# --- True-Centered Text & Morphing Container Helpers (all coords in 1x logical, scaled by S) ---

def draw_text_center_box(
    draw: ImageDraw.ImageDraw, x0: float, y0: float, x1: float, y1: float, text: str, font: ImageFont.FreeTypeFont, fill: str
) -> None:
    cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    if "\n" in text:
        bbox = draw.multiline_textbbox((0, 0), text, font=font, align="center", spacing=6 * S)
        tx = cx - (bbox[0] + bbox[2]) / 2.0
        ty = cy - (bbox[1] + bbox[3]) / 2.0
        draw.multiline_text((tx, ty), text, font=font, fill=fill, align="center", spacing=6 * S)
    else:
        bbox = draw.textbbox((0, 0), text, font=font)
        tx = cx - (bbox[0] + bbox[2]) / 2.0
        ty = cy - (bbox[1] + bbox[3]) / 2.0
        draw.text((tx, ty), text, font=font, fill=fill)


def draw_text_vcenter_left(
    draw: ImageDraw.ImageDraw, x: float, y0: float, y1: float, text: str, font: ImageFont.FreeTypeFont, fill: str
) -> None:
    cy = (y0 + y1) / 2.0
    bbox = draw.textbbox((0, 0), text, font=font)
    ty = cy - (bbox[1] + bbox[3]) / 2.0
    draw.text((x - bbox[0], ty), text, font=font, fill=fill)


def draw_pill(
    draw: ImageDraw.ImageDraw,
    x: float,
    y: float,
    text: str,
    bg: str,
    fg: str,
    border: str = "",
    font: ImageFont.FreeTypeFont = F_SMALL_B,
    pad_x: int = 14,
    pad_y: int = 8,
    radius: int = 9,
    min_h: float = 0,
) -> Tuple[float, float, float, float]:
    sx, sy = x * S, y * S
    px, py = pad_x * S, pad_y * S
    bbox = draw.textbbox((0, 0), text, font=font)
    w = (bbox[2] - bbox[0]) + px * 2
    h = max(min_h * S, (bbox[3] - bbox[1]) + py * 2)
    x1, y1 = sx + w, sy + h
    draw.rounded_rectangle([sx, sy, x1, y1], radius=radius * S, fill=bg, outline=border if border else None, width=2 * S if border else 0)
    draw_text_center_box(draw, sx, sy, x1, y1, text, font, fg)
    return x, y, x1 / S, y1 / S


def draw_pill_right(
    draw: ImageDraw.ImageDraw,
    x_right: float,
    y: float,
    text: str,
    bg: str,
    fg: str,
    border: str = "",
    font: ImageFont.FreeTypeFont = F_SMALL_B,
    pad_x: int = 14,
    pad_y: int = 8,
    min_h: float = 0,
) -> Tuple[float, float, float, float]:
    bbox = draw.textbbox((0, 0), text, font=font)
    w = (bbox[2] - bbox[0]) / S + pad_x * 2
    return draw_pill(draw, x_right - w, y, text, bg, fg, border, font, pad_x, pad_y, min_h=min_h)


def draw_card(
    draw: ImageDraw.ImageDraw,
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    fill: str = SURFACE,
    outline: str = BORDER,
    radius: float = 16,
    width: int = 2,
    shadow: bool = True,
) -> None:
    sx0, sy0, sx1, sy1 = x0 * S, y0 * S, x1 * S, y1 * S
    r = int(radius * S)
    if shadow:
        draw.rounded_rectangle([sx0 + 4 * S, sy0 + 6 * S, sx1 + 4 * S, sy1 + 6 * S], radius=r, fill=SHADOW)
    draw.rounded_rectangle([sx0, sy0, sx1, sy1], radius=r, fill=fill, outline=outline, width=width * S)


def draw_check(draw: ImageDraw.ImageDraw, cx: float, cy: float, r: float, bg: str = PASS_FG) -> None:
    scx, scy, sr = cx * S, cy * S, r * S
    draw.ellipse([scx - sr, scy - sr, scx + sr, scy + sr], fill=bg)
    pts = [(scx - sr * 0.44, scy + sr * 0.02), (scx - sr * 0.12, scy + sr * 0.36), (scx + sr * 0.46, scy - sr * 0.32)]
    draw.line(pts, fill="#FFFFFF", width=max(3, int(sr * 0.22)), joint="curve")


def draw_chrome(
    draw: ImageDraw.ImageDraw,
    file_badge: str,
    title: str,
    subtitle: str,
    step_idx: int,
    total_steps: int,
    t_raw: float,
    duration_sec: int,
) -> None:
    draw.rectangle([0, 0, WIDTH, 90 * S], fill=SURFACE)
    draw.line([(0, 90 * S), (WIDTH, 90 * S)], fill=BORDER, width=2 * S)

    _, _, bx1, _ = draw_pill(draw, 40, 14, file_badge, NAVY, "#FFFFFF", font=F_SMALL_B, pad_x=12, pad_y=6, min_h=30)
    draw_text_vcenter_left(draw, (bx1 + 14) * S, 12 * S, 46 * S, title, F_TITLE, TEXT)
    draw_text_vcenter_left(draw, 40 * S, 50 * S, 82 * S, subtitle, F_SUB, SKY)

    px = 1240.0
    for idx in range(total_steps - 1, -1, -1):
        label = f"จุดที่ {idx + 1}/{total_steps}"
        is_active = idx == step_idx
        is_done = idx < step_idx
        bg = BLUE if is_active else (BLUE_TINT if is_done else SURFACE_ALT)
        fg = "#FFFFFF" if is_active else (NAVY if is_done else TEXT_MUTED)
        border = BLUE if is_active else (BORDER if is_done else BORDER_MUTED)
        x0, _, _, _ = draw_pill_right(draw, px, 14, label, bg, fg, border, F_SMALL_B, pad_x=12, pad_y=6, min_h=30)
        px = x0 - 8

    draw.rectangle([0, (720 - 46) * S, WIDTH, HEIGHT], fill=SURFACE)
    draw.line([(0, (720 - 46) * S), (WIDTH, (720 - 46) * S)], fill=BORDER, width=2 * S)
    bx0, bx1, by = 40 * S, (1280 - 145) * S, (720 - 23) * S
    draw.rounded_rectangle([bx0, by - 4 * S, bx1, by + 4 * S], radius=4 * S, fill=BLUE_TINT)
    draw.rounded_rectangle([bx0, by - 4 * S, bx0 + (bx1 - bx0) * clamp01(t_raw), by + 4 * S], radius=4 * S, fill=BLUE)
    sec = min(duration_sec, int(t_raw * duration_sec))
    draw_text_vcenter_left(draw, (1280 - 125) * S, (720 - 46) * S, HEIGHT, f"00:{sec:02d} / 00:{duration_sec:02d}", F_CODE, TEXT_MUTED)


def draw_bottom_callout(draw: ImageDraw.ImageDraw, title: str, thai: str, accent: str = BLUE) -> None:
    draw_card(draw, 40, 582, 1240, 658, fill=SURFACE, outline=accent, radius=12)
    draw.rectangle([54 * S, 594 * S, 60 * S, 646 * S], fill=accent)
    draw_text_vcenter_left(draw, 76 * S, 588 * S, 618 * S, title, F_BODY_B, TEXT)
    draw_text_vcenter_left(draw, 76 * S, 620 * S, 652 * S, thai, F_BODY, TEXT_SUB)


def draw_code_spotlight(
    draw: ImageDraw.ImageDraw,
    filepath: str,
    lines: List[str],
    hl_start: int,
    hl_end: int,
    prev_start: int,
    prev_end: int,
    st: float,
    field_tag: str = "",
) -> Tuple[float, float]:
    """#19 Rack Focus (dimmed unfocused lines) + #26 Field Isolation Pill.
    Returns (stream_start_x_1x, stream_start_y_1x)."""
    x0, y0, x1, y1 = 40, 108, 636, 566
    draw_card(draw, x0, y0, x1, y1, fill=SURFACE, outline=BORDER)

    draw.rounded_rectangle([x0 * S, y0 * S, x1 * S, (y0 + 42) * S], radius=16 * S, fill=NAVY)
    draw.rectangle([x0 * S, (y0 + 22) * S, x1 * S, (y0 + 42) * S], fill=NAVY)
    draw_text_vcenter_left(draw, (x0 + 18) * S, y0 * S, (y0 + 42) * S, filepath, F_MONO_B, "#FFFFFF")

    code_top = y0 + 54
    n_lines = max(1, len(lines))
    avail_h = (y1 - 14) - code_top
    row_h = min(24.0, avail_h / n_lines)

    # #45 Staged transition: Stage 1 (0.0..0.24) spotlight morphs + rack focus dims unfocused lines
    trans_p = seg_t(st, 0.0, 0.24)
    sp = spring_ease(trans_p)
    s_cur = lerp(prev_start, hl_start, sp)
    e_cur = lerp(prev_end, hl_end, sp)
    hy0 = code_top + s_cur * row_h - 2
    hy1 = code_top + (e_cur + 1) * row_h + 2
    morph_r = int((10 + 4 * math.sin(trans_p * math.pi)) * S)

    draw.rounded_rectangle([(x0 + 10) * S, hy0 * S, (x1 - 10) * S, hy1 * S], radius=morph_r, fill=BLUE_SOFT, outline=BLUE, width=2 * S)
    draw.rectangle([(x0 + 10) * S, (hy0 + 4) * S, (x0 + 16) * S, (hy1 - 4) * S], fill=BLUE)

    # #19 Rack Focus dimming: unfocused lines fade to soft #B8C4D4, focused lines pop #0F172A / #1D4ED8
    dim_alpha = ease_out_cubic(seg_t(st, 0.04, 0.22))
    dim_col = mix_color("#94A3B8", "#B8C5D6", dim_alpha)
    focus_col = mix_color(NAVY, ROYAL, 0.35)

    for idx, line in enumerate(lines):
        assert line.isascii(), f"Code box must be pure ASCII, got: {line!r}"
        ly0 = (code_top + idx * row_h) * S
        ly1 = (code_top + (idx + 1) * row_h) * S
        in_hl = hl_start <= idx <= hl_end
        col = focus_col if in_hl else dim_col
        font = F_CODE_B if in_hl else F_CODE
        draw_text_vcenter_left(draw, (x0 + 26) * S, ly0, ly1, line, font, col)

    hl_cy = (hy0 + hy1) / 2.0
    if field_tag:
        # #26 Field Isolation: pill lifts out from spotlight edge and settles before returning
        pop_in = overshoot_settle(seg_t(st, 0.08, 0.28))
        pop_out = 1.0 - ease_out_cubic(seg_t(st, 0.90, 1.00))
        pop = pop_in * pop_out
        if pop > 0.05:
            bbox = draw.textbbox((0, 0), field_tag, font=F_SMALL_B)
            pw = (bbox[2] - bbox[0]) / S + 22
            px = lerp(x1 - pw - 16, x1 - pw * 0.45, pop)
            py = hl_cy - 16
            _, _, px1, _ = draw_pill(draw, px, py, field_tag, NAVY, "#FFFFFF", border=BLUE, font=F_SMALL_B, pad_x=11, pad_y=6, min_h=32)
            return px1, hl_cy
    return float(x1), hl_cy


def split_steps(t_raw: float, n_steps: int, hold_sec: float, duration_sec: int) -> Tuple[int, float]:
    anim_sec = max(1.0, duration_sec - hold_sec)
    sec = t_raw * duration_sec
    if sec >= anim_sec:
        return n_steps - 1, 1.0
    per = anim_sec / n_steps
    idx = min(n_steps - 1, int(sec / per))
    st = clamp01((sec - idx * per) / per)
    return idx, st


# ==============================================================================
# 01: .github/ISSUE_TEMPLATE/bug_report.yml (16s, 4 steps)
# ==============================================================================

BUG_LINES = [
    'name: Bug Report',
    'title: "[Bug]: "',
    'labels: ["bug", "triage"]',
    'body:',
    '  - type: input',
    '    id: version',
    '    attributes:',
    '      label: Firmware Version / Tag',
    '      placeholder: v1.0.0',
    '    validations:',
    '      required: true',
    '  - type: dropdown',
    '    id: environment',
    '    attributes:',
    '      label: Environment',
    '      options: [ESP32, Native, CI]',
    '  - type: checkboxes',
    '    id: checklist',
    '    attributes:',
    '      label: Pre-check Confirmation',
    '      options:',
    '        - label: Tested on latest branch',
    '          required: true',
]

BUG_STEPS = [
    (0, 2, "title + labels", "Metadata & Auto-Labels", "กำหนดชื่อฟอร์ม คำนำหน้า [Bug]: และติดป้าย bug + triage อัตโนมัติ"),
    (4, 10, "type: input", "Required Text Input", "สร้างช่องกรอกเวอร์ชัน/Tag พร้อมบังคับกรอก (required: true)"),
    (11, 15, "type: dropdown", "Environment Dropdown", "สร้างตัวเลือก Dropdown ป้องกันผู้แจ้งพิมพ์ชื่อสภาพแวดล้อมผิด"),
    (16, 22, "type: checkboxes", "Mandatory Checkbox", "บังคับติ๊กยืนยันก่อนกด Submit Issue เพื่อให้ทีมจำลองบั๊กได้ทันที"),
]


def render_01_bug(draw: ImageDraw.ImageDraw, t_raw: float) -> None:
    sc, st = split_steps(t_raw, 4, 2.0, 16)
    draw_chrome(draw, "FILE 01", ".github/ISSUE_TEMPLATE/bug_report.yml", "แบบฟอร์มแจ้งบั๊กแบบมีโครงสร้าง (Issue Form YAML)", sc, 4, t_raw, 16)

    ps, pe = (BUG_STEPS[sc - 1][0], BUG_STEPS[sc - 1][1]) if sc > 0 else (BUG_STEPS[0][0], BUG_STEPS[0][1])
    hs, he, ftag, title, thai = BUG_STEPS[sc]
    sx, hl_y = draw_code_spotlight(draw, ".github/ISSUE_TEMPLATE/bug_report.yml", BUG_LINES, hs, he, ps, pe, st, ftag)

    # #45 Staged transition + #48 Overshoot/Settle + #51 Readability Hold
    stream_p = ease_out_cubic(seg_t(st, 0.16, 0.40))
    settle = overshoot_settle(seg_t(st, 0.24, 0.48))
    target_h = [458, 340, 440, 380][sc]
    prev_h = [458, 458, 340, 440][sc]
    card_y1 = 108 + lerp(prev_h, target_h, settle)
    y_off = (1.0 - settle) * 14.0

    draw_liquid_stream(draw, sx * S, hl_y * S, 712 * S, ((108 + card_y1) / 2 + y_off) * S, BLUE, t_raw, stream_p)
    draw_card(draw, 712, 108 + y_off, 1240, card_y1 + y_off, fill=SURFACE, outline=BLUE, radius=16 + 4 * math.sin(seg_t(st, 0.0, 0.45) * math.pi))
    draw_pill(draw, 738, 130 + y_off, "GitHub Rendered UI", BLUE_TINT, NAVY, BLUE, min_h=34)
    draw_text_vcenter_left(draw, 738 * S, (174 + y_off) * S, (210 + y_off) * S, title, F_HEAD, NAVY)

    if sc == 0:
        draw_card(draw, 738, 226, 1212, 470, SURFACE_ALT, BORDER, shadow=False)
        draw_text_vcenter_left(draw, 760 * S, 246 * S, 282 * S, "Title:  [Bug]: Timer overflow on ESP32", F_BODY_B, TEXT)
        draw_pill(draw, 760, 304, "label: bug", BLOCK_BG, BLOCK_FG, BLOCK_FG, min_h=36)
        draw_pill(draw, 895, 304, "label: triage", BLUE_TINT, NAVY, BLUE, min_h=36)
        draw_text_vcenter_left(draw, 760 * S, 370 * S, 420 * S, "ติดป้ายและจัดหมวดหมู่ให้อัตโนมัติทันทีที่เปิด Issue", F_BODY, TEXT_SUB)
    elif sc == 1:
        draw_text_vcenter_left(draw, 738 * S, 232 * S, 266 * S, "Firmware Version / Tag *", F_BODY_B, TEXT)
        draw_card(draw, 738, 276, 1212, 332, "#FFFFFF", BLUE, radius=10, shadow=False)
        draw_text_vcenter_left(draw, 758 * S, 276 * S, 332 * S, "v1.0.0", F_CODE_B, TEXT)
        draw_pill(draw, 738, 360, "required: true (ห้ามเว้นว่าง)", BLOCK_BG, BLOCK_FG, BLOCK_FG, min_h=38)
    elif sc == 2:
        draw_text_vcenter_left(draw, 738 * S, 232 * S, 266 * S, "Environment *", F_BODY_B, TEXT)
        for idx, opt in enumerate(["DOIT ESP32 DevKit v1 (Hardware)", "PlatformIO Native Test ([env:native])", "GitHub Actions CI"]):
            oy = 278 + idx * 64
            active = idx == 0
            draw_card(draw, 738, oy, 1212, oy + 50, BLUE_SOFT if active else SURFACE_ALT, BLUE if active else BORDER, radius=10, shadow=False)
            draw_text_vcenter_left(draw, 760 * S, oy * S, (oy + 50) * S, opt, F_BODY_B if active else F_BODY, NAVY if active else TEXT_SUB)
    else:
        draw_text_vcenter_left(draw, 738 * S, 232 * S, 266 * S, "Pre-check Confirmation *", F_BODY_B, TEXT)
        draw_card(draw, 738, 278, 1212, 344, PASS_BG, PASS_FG, radius=10, shadow=False)
        draw_check(draw, 768, 311, 14, PASS_FG)
        draw_text_vcenter_left(draw, 796 * S, 278 * S, 344 * S, "Tested on latest branch (Required)", F_BODY_B, PASS_FG)
        draw_pill_right(draw, 1212, 380, "Submit new issue", PASS_FG, "#FFFFFF", font=F_BODY_B, min_h=44)

    draw_bottom_callout(draw, f"bug_report.yml — {title}", thai, BLUE)


# ==============================================================================
# 02: .github/ISSUE_TEMPLATE/feature_request.yml (15s, 3 steps)
# ==============================================================================

FEAT_LINES = [
    'name: Feature Request',
    'title: "[Feat]: "',
    'labels: ["enhancement"]',
    'body:',
    '  - type: textarea',
    '    id: problem',
    '    attributes:',
    '      label: Problem / Motivation (Why)',
    '    validations:',
    '      required: true',
    '  - type: textarea',
    '    id: solution',
    '    attributes:',
    '      label: Proposed Solution (How)',
    '      placeholder: Add to lib/blink_math/',
    '  - type: dropdown',
    '    id: target_branch',
    '    attributes:',
    '      label: Target Branch (Linear)',
    '      options: [main, release/v*]',
    '      default: 0',
]

FEAT_STEPS = [
    (0, 2, "title + labels", "Feature Prefix & Label", "ตั้งคำนำหน้า [Feat]: และติดป้าย enhancement แยกจากบั๊กชัดเจน"),
    (4, 14, "type: textarea", "Why & How Textareas", "แยกช่องอธิบายปัญหา (Why) และแนวทางแก้ไข (How) ให้รีวิวได้ไว"),
    (15, 20, "default: 0", "Target Branch Default", "กำหนดตัวเลือก Branch เป้าหมายเริ่มต้นเป็น main (Rebase & Merge)"),
]


def render_02_feat(draw: ImageDraw.ImageDraw, t_raw: float) -> None:
    sc, st = split_steps(t_raw, 3, 2.0, 15)
    draw_chrome(draw, "FILE 02", ".github/ISSUE_TEMPLATE/feature_request.yml", "แบบฟอร์มเสนอฟีเจอร์ใหม่ (Why / How / Target Branch)", sc, 3, t_raw, 15)

    ps, pe = (FEAT_STEPS[sc - 1][0], FEAT_STEPS[sc - 1][1]) if sc > 0 else (FEAT_STEPS[0][0], FEAT_STEPS[0][1])
    hs, he, ftag, title, thai = FEAT_STEPS[sc]
    sx, hl_y = draw_code_spotlight(draw, ".github/ISSUE_TEMPLATE/feature_request.yml", FEAT_LINES, hs, he, ps, pe, st, ftag)

    stream_p = ease_out_cubic(seg_t(st, 0.16, 0.40))
    settle = overshoot_settle(seg_t(st, 0.24, 0.48))
    target_h = [350, 410, 360][sc]
    prev_h = [350, 350, 410][sc]
    card_y1 = 108 + lerp(prev_h, target_h, settle)

    draw_liquid_stream(draw, sx * S, hl_y * S, 712 * S, ((108 + card_y1) / 2) * S, BLUE, t_raw, stream_p)
    draw_card(draw, 712, 108, 1240, card_y1, fill=SURFACE, outline=BLUE)
    draw_pill(draw, 738, 130, "GitHub Rendered UI", BLUE_TINT, NAVY, BLUE, min_h=34)
    draw_text_vcenter_left(draw, 738 * S, 174 * S, 210 * S, title, F_HEAD, NAVY)

    if sc == 0:
        draw_card(draw, 738, 226, 1212, 410, SURFACE_ALT, BORDER, shadow=False)
        draw_text_vcenter_left(draw, 760 * S, 248 * S, 284 * S, "Title:  [Feat]: Add fast blink preset", F_BODY_B, TEXT)
        draw_pill(draw, 760, 306, "label: enhancement", BLUE_TINT, ROYAL, BLUE, min_h=38)
    elif sc == 1:
        draw_text_vcenter_left(draw, 738 * S, 226 * S, 258 * S, "1. Problem / Motivation (Why) *", F_BODY_B, TEXT)
        draw_card(draw, 738, 264, 1212, 340, "#FFFFFF", BLUE, radius=10, shadow=False)
        draw_text_vcenter_left(draw, 756 * S, 264 * S, 340 * S, "Need faster LED blink for Wi-Fi pairing status", F_BODY, TEXT_SUB)
        draw_text_vcenter_left(draw, 738 * S, 360 * S, 392 * S, "2. Proposed Solution (How) *", F_BODY_B, TEXT)
        draw_card(draw, 738, 398, 1212, 474, BLUE_SOFT, BLUE, radius=10, shadow=False)
        draw_text_vcenter_left(draw, 756 * S, 398 * S, 474 * S, "Add preset function in lib/blink_math/ + Unity test", F_BODY, NAVY)
    else:
        draw_text_vcenter_left(draw, 738 * S, 232 * S, 266 * S, "Target Branch (Linear History)", F_BODY_B, TEXT)
        draw_card(draw, 738, 278, 1212, 340, BLUE_SOFT, BLUE, radius=10, shadow=False)
        draw_text_vcenter_left(draw, 758 * S, 278 * S, 340 * S, "main (PR + Rebase and merge)  [default: 0]", F_BODY_B, NAVY)
        draw_card(draw, 738, 356, 1212, 418, SURFACE_ALT, BORDER, radius=10, shadow=False)
        draw_text_vcenter_left(draw, 758 * S, 356 * S, 418 * S, "release/v* (Hotfix before release)", F_BODY, TEXT_MUTED)

    draw_bottom_callout(draw, f"feature_request.yml — {title}", thai, BLUE)


# ==============================================================================
# 03: .github/ISSUE_TEMPLATE/config.yml (15s, 3 steps)
# ==============================================================================

CFG_LINES = [
    'blank_issues_enabled: false',
    '',
    'contact_links:',
    '  - name: Workshop Docs',
    '    url: https://docs.github.com/...',
    '    about: YAML syntax for Issue Forms',
]

CFG_STEPS = [
    (0, 0, "blank_issues: false", "Disable Blank Issues", "ปิดปุ่ม Blank Issue บังคับให้ทุกคนใช้แบบฟอร์ม Bug/Feature เสมอ"),
    (2, 5, "contact_links", "Add Contact Links", "เพิ่มลิงก์คู่มืออ้างอิงในหน้าเลือกเปิด Issue ช่วยผู้เรียนเปิดดูได้ทันที"),
    (0, 5, "Issue Chooser", "Issue Chooser Result", "หน้าเลือก Issue บน GitHub แสดงเฉพาะฟอร์มมาตรฐาน + ลิงก์คู่มือ"),
]


def render_03_cfg(draw: ImageDraw.ImageDraw, t_raw: float) -> None:
    sc, st = split_steps(t_raw, 3, 2.0, 15)
    draw_chrome(draw, "FILE 03", ".github/ISSUE_TEMPLATE/config.yml", "ควบคุมหน้าเลือก Issue (ปิด Blank Issue + เพิ่มลิงก์คู่มือ)", sc, 3, t_raw, 15)

    ps, pe = (CFG_STEPS[sc - 1][0], CFG_STEPS[sc - 1][1]) if sc > 0 else (CFG_STEPS[0][0], CFG_STEPS[0][1])
    hs, he, ftag, title, thai = CFG_STEPS[sc]
    sx, hl_y = draw_code_spotlight(draw, ".github/ISSUE_TEMPLATE/config.yml", CFG_LINES, hs, he, ps, pe, st, ftag)

    stream_p = ease_out_cubic(seg_t(st, 0.16, 0.40))
    draw_liquid_stream(draw, sx * S, hl_y * S, 712 * S, 336 * S, BLUE, t_raw, stream_p)
    draw_card(draw, 712, 108, 1240, 566, fill=SURFACE, outline=BLUE)
    draw_pill(draw, 738, 130, "GitHub Issue Chooser", BLUE_TINT, NAVY, BLUE, min_h=34)
    draw_text_vcenter_left(draw, 738 * S, 174 * S, 210 * S, title, F_HEAD, NAVY)

    draw_card(draw, 738, 226, 1212, 294, BLUE_SOFT if sc == 2 else SURFACE_ALT, BLUE if sc == 2 else BORDER, radius=10, shadow=False)
    draw_text_vcenter_left(draw, 760 * S, 226 * S, 294 * S, "Bug Report (แจ้งบั๊ก Firmware)", F_BODY_B, NAVY)
    draw_pill_right(draw, 1194, 242, "Get started", BLUE, "#FFFFFF", min_h=36)

    draw_card(draw, 738, 308, 1212, 376, BLUE_SOFT if sc == 2 else SURFACE_ALT, BLUE if sc == 2 else BORDER, radius=10, shadow=False)
    draw_text_vcenter_left(draw, 760 * S, 308 * S, 376 * S, "Feature Request (ขอฟีเจอร์ใหม่)", F_BODY_B, NAVY)
    draw_pill_right(draw, 1194, 324, "Get started", BLUE, "#FFFFFF", min_h=36)

    if sc >= 1:
        draw_card(draw, 738, 390, 1212, 458, PASS_BG, PASS_FG, radius=10, shadow=False)
        draw_text_vcenter_left(draw, 760 * S, 390 * S, 458 * S, "Workshop Docs (Issue Forms Guide)", F_BODY_B, PASS_FG)
        draw_pill_right(draw, 1194, 406, "Open link", PASS_FG, "#FFFFFF", min_h=36)

    draw_pill(draw, 738, 486, "Blank issue: HIDDEN (blank_issues_enabled: false)", BLOCK_BG, BLOCK_FG, BLOCK_FG, min_h=38)

    draw_bottom_callout(draw, f"config.yml — {title}", thai, BLUE)


# ==============================================================================
# 04: .github/pull_request_template.md (15s, 3 steps)
# ==============================================================================

PR_LINES = [
    '## Summary',
    '<!-- Describe what & why -->',
    '',
    '## Type of Change',
    '- [ ] feat: new feature',
    '- [ ] fix: bug fix',
    '- [ ] release: release prep',
    '- [ ] ci / docs / test',
    '',
    '## Checklist before Review',
    '- [ ] pre-commit run --all-files',
    '- [ ] pio test -e native',
    '- [ ] pio run -e esp32doit-devkit-v1',
    '- [ ] Updated docs or unit tests',
]

PR_STEPS = [
    (0, 1, "## Summary", "Auto-Filled Summary", "เติมหัวข้อ Summary อัตโนมัติทันทีที่ผู้เรียนกดสร้าง Pull Request"),
    (3, 7, "- [ ] Type", "Type of Change Checkboxes", "แปลง Markdown - [ ] เป็น Checkbox ให้ติ๊กเลือกประเภทของ PR ได้สะดวก"),
    (9, 13, "## Checklist", "Pre-Review Checklist", "เตือนให้รัน pre-commit, native test และ build ESP32 ก่อนขอ Review"),
]


def render_04_pr(draw: ImageDraw.ImageDraw, t_raw: float) -> None:
    sc, st = split_steps(t_raw, 3, 2.0, 15)
    draw_chrome(draw, "FILE 04", ".github/pull_request_template.md", "แม่แบบคำอธิบายและ Checklist อัตโนมัติเมื่อเปิด Pull Request", sc, 3, t_raw, 15)

    ps, pe = (PR_STEPS[sc - 1][0], PR_STEPS[sc - 1][1]) if sc > 0 else (PR_STEPS[0][0], PR_STEPS[0][1])
    hs, he, ftag, title, thai = PR_STEPS[sc]
    sx, hl_y = draw_code_spotlight(draw, ".github/pull_request_template.md", PR_LINES, hs, he, ps, pe, st, ftag)

    stream_p = ease_out_cubic(seg_t(st, 0.16, 0.40))
    draw_liquid_stream(draw, sx * S, hl_y * S, 712 * S, 336 * S, BLUE, t_raw, stream_p)
    draw_card(draw, 712, 108, 1240, 566, fill=SURFACE, outline=BLUE)
    draw_pill(draw, 738, 130, "GitHub New PR Preview", BLUE_TINT, NAVY, BLUE, min_h=34)
    draw_text_vcenter_left(draw, 738 * S, 174 * S, 210 * S, title, F_HEAD, NAVY)

    if sc == 0:
        draw_card(draw, 738, 226, 1212, 430, SURFACE_ALT, BLUE, radius=10, shadow=False)
        draw_text_vcenter_left(draw, 760 * S, 244 * S, 280 * S, "Summary (สรุปการเปลี่ยนแปลง)", F_HEAD, NAVY)
        draw_text_vcenter_left(draw, 760 * S, 294 * S, 332 * S, "Closes #2 — Add 100ms fast blink preset", F_BODY, TEXT)
    elif sc == 1:
        for idx, (lbl, chk) in enumerate([("feat: new feature", True), ("fix: bug fix", False), ("ci / docs / test", False)]):
            cy = 232 + idx * 72
            draw_card(draw, 738, cy, 1212, cy + 54, PASS_BG if chk else SURFACE_ALT, PASS_FG if chk else BORDER, radius=10, shadow=False)
            if chk:
                draw_check(draw, 768, cy + 27, 13, PASS_FG)
            draw_text_vcenter_left(draw, 796 * S, cy * S, (cy + 54) * S, lbl, F_MONO_B if chk else F_BODY, PASS_FG if chk else TEXT_MUTED)
    else:
        for idx, lbl in enumerate(["pre-commit run --all-files", "pio test -e native", "pio run -e esp32doit-devkit-v1"]):
            cy = 232 + idx * 72
            draw_card(draw, 738, cy, 1212, cy + 54, PASS_BG, PASS_FG, radius=10, shadow=False)
            draw_check(draw, 768, cy + 27, 13, PASS_FG)
            draw_text_vcenter_left(draw, 796 * S, cy * S, (cy + 54) * S, lbl, F_MONO_B, PASS_FG)

    draw_bottom_callout(draw, f"pull_request_template.md — {title}", thai, BLUE)


# ==============================================================================
# 05: .github/workflows/ci.yml (16s, 4 steps)
# ==============================================================================

CI_LINES = [
    'name: CI - Lint, Test & Build',
    'on:',
    '  push: { branches: [main, "release/**"] }',
    '  pull_request: { branches: [main] }',
    'defaults:',
    '  run: { working-directory: workshop }',
    'jobs:',
    '  lint:',
    '    runs-on: ubuntu-latest',
    '    steps:',
    '      - uses: actions/checkout@v7',
    '      - uses: pre-commit/action@v3.0.1',
    '  unit-test:',
    '    needs: lint',
    '    steps:',
    '      - uses: actions/cache@v6',
    '      - run: pio test -e native -v',
    '  build-esp32:',
    '    needs: unit-test',
    '    steps:',
    '      - run: pio run -e esp32doit-devkit-v1',
    '      - if: startsWith(github.ref, "refs/heads/release/")',
    '        uses: actions/upload-artifact@v7',
]

CI_STEPS = [
    (0, 5, "on: push + PR", "Workflow Triggers", "ทำงานอัตโนมัติเมื่อ Push เข้า main/release/** หรือเปิด PR เข้า main"),
    (7, 11, "job: lint", "Job 1: lint", "รัน pre-commit บน ubuntu-latest ตรวจ format และชื่อ commit"),
    (12, 16, "needs: lint", "Job 2: unit-test (needs: lint)", "รอ lint ผ่านก่อน แล้วกู้ Cache ~/.platformio/.cache รัน pio test -e native"),
    (17, 22, "needs: unit-test", "Job 3: build-esp32 (needs: unit-test)", "คอมไพล์เฟิร์มแวร์ ESP32 และอัปโหลด Artifact เมื่ออยู่บน release/*"),
]


def render_05_ci(draw: ImageDraw.ImageDraw, t_raw: float) -> None:
    sc, st = split_steps(t_raw, 4, 2.0, 16)
    draw_chrome(draw, "FILE 05", ".github/workflows/ci.yml", "Workflow ตรวจสอบโค้ดอัตโนมัติ 3 ขั้นตอน (lint -> unit-test -> build-esp32)", sc, 4, t_raw, 16)

    ps, pe = (CI_STEPS[sc - 1][0], CI_STEPS[sc - 1][1]) if sc > 0 else (CI_STEPS[0][0], CI_STEPS[0][1])
    hs, he, ftag, title, thai = CI_STEPS[sc]
    sx, hl_y = draw_code_spotlight(draw, ".github/workflows/ci.yml", CI_LINES, hs, he, ps, pe, st, ftag)

    stream_p = ease_out_cubic(seg_t(st, 0.16, 0.40))
    stream_col = PASS_FG if sc == 3 else BLUE
    draw_liquid_stream(draw, sx * S, hl_y * S, 712 * S, 336 * S, stream_col, t_raw, stream_p)
    draw_card(draw, 712, 108, 1240, 566, fill=SURFACE, outline=stream_col)
    draw_pill(draw, 738, 130, "GitHub Actions Pipeline", BLUE_TINT, NAVY, BLUE, min_h=34)
    draw_text_vcenter_left(draw, 738 * S, 174 * S, 210 * S, title, F_HEAD, NAVY)

    stages = [
        ("1. lint", "pre-commit checks", sc >= 1),
        ("2. unit-test", "pio test -e native (Cache)", sc >= 2),
        ("3. build-esp32", "firmware.bin + Artifact", sc >= 3),
    ]
    for idx, (sname, ssub, active) in enumerate(stages):
        sy = 228 + idx * 102
        is_cur = idx == (sc - 1)
        bg = PASS_BG if (active and not is_cur or sc == 3) else (BLUE_SOFT if is_cur else SURFACE_ALT)
        out = PASS_FG if (active and not is_cur or sc == 3) else (BLUE if is_cur else BORDER)
        draw_card(draw, 738, sy, 1212, sy + 76, bg, out, radius=12, shadow=False)
        draw_text_vcenter_left(draw, 760 * S, (sy + 8) * S, (sy + 40) * S, sname, F_BODY_B, TEXT)
        draw_text_vcenter_left(draw, 760 * S, (sy + 40) * S, (sy + 68) * S, ssub, F_SMALL, TEXT_SUB)
        if active:
            draw_pill_right(draw, 1192, sy + 20, "PASS" if (not is_cur or sc == 3) else "RUNNING", PASS_FG if (not is_cur or sc == 3) else BLUE, "#FFFFFF", min_h=36)

    draw_bottom_callout(draw, f"ci.yml — {title}", thai, stream_col)


# ==============================================================================
# 06: .github/workflows/release.yml (16s, 4 steps, 4-file liquid merge)
# ==============================================================================

REL_LINES = [
    'name: Release Firmware (CD)',
    'on:',
    '  push:',
    '    tags: ["v*.*.*"]',
    'permissions:',
    '  contents: write',
    'jobs:',
    '  release:',
    '    runs-on: ubuntu-latest',
    '    steps:',
    '      - run: pio test -e native',
    '      - run: pio run -e esp32doit-devkit-v1',
    '      - name: Merge Binaries',
    '        run: |',
    '          esptool --chip esp32 merge-bin \\',
    '            -o dist/merged-firmware.bin \\',
    '            0x1000 bootloader.bin \\',
    '            0x8000 partitions.bin \\',
    '            0x10000 firmware.bin',
    '      - uses: softprops/action-gh-release@v3',
    '        with:',
    '          generate_release_notes: true',
    '          files: dist/*-firmware.bin',
]

REL_STEPS = [
    (1, 5, "tags: v*.*.*", "Tag Trigger & Write Permission", "ทำงานเมื่อ Push Tag รูปแบบ v*.*.* พร้อมขอสิทธิ์ contents: write เพื่อสร้าง Release"),
    (10, 11, "pio test + run", "Pre-Release Test & Build", "รัน Unit Test และ Build เฟิร์มแวร์ ESP32 ใหม่อีกครั้งก่อนแพ็กไฟล์"),
    (12, 18, "esptool merge-bin", "Liquid Merge -> merged-firmware.bin", "หลอมรวม 4 ไฟล์ (bootloader + partitions + boot_app0 + firmware) เป็นไฟล์เดียวที่ 0x0"),
    (19, 22, "action-gh-release", "Publish GitHub Release", "สร้างหน้า Release v1.0.0 พร้อม Release Notes และแนบทั้งไฟล์ OTA + 0x0 อัตโนมัติ"),
]


def render_06_rel(draw: ImageDraw.ImageDraw, t_raw: float) -> None:
    sc, st = split_steps(t_raw, 4, 2.0, 16)
    draw_chrome(draw, "FILE 06", ".github/workflows/release.yml", "Workflow ปล่อยเวอร์ชันอัตโนมัติ (Tag v*.*.* -> Liquid Merge -> GitHub Release)", sc, 4, t_raw, 16)

    ps, pe = (REL_STEPS[sc - 1][0], REL_STEPS[sc - 1][1]) if sc > 0 else (REL_STEPS[0][0], REL_STEPS[0][1])
    hs, he, ftag, title, thai = REL_STEPS[sc]
    sx, hl_y = draw_code_spotlight(draw, ".github/workflows/release.yml", REL_LINES, hs, he, ps, pe, st, ftag)

    stream_p = ease_out_cubic(seg_t(st, 0.16, 0.40))
    stream_col = PASS_FG if sc == 3 else BLUE
    draw_liquid_stream(draw, sx * S, hl_y * S, 712 * S, 336 * S, stream_col, t_raw, stream_p)
    draw_card(draw, 712, 108, 1240, 566, fill=SURFACE, outline=stream_col)
    draw_pill(draw, 738, 130, "GitHub Release Output", BLUE_TINT, NAVY, BLUE, min_h=34)
    draw_text_vcenter_left(draw, 738 * S, 174 * S, 210 * S, title, F_HEAD, NAVY)

    if sc == 0:
        draw_card(draw, 738, 232, 1212, 430, BLUE_SOFT, BLUE, radius=12, shadow=False)
        draw_pill(draw, 764, 260, "TAG: v1.0.0", NAVY, "#FFFFFF", font=F_BODY_B, min_h=40)
        draw_text_vcenter_left(draw, 764 * S, 324 * S, 362 * S, "Matched: tags: ['v*.*.*']", F_MONO_B, PASS_FG)
        draw_text_vcenter_left(draw, 764 * S, 368 * S, 404 * S, "Permission: contents: write (Enabled)", F_BODY, TEXT_SUB)
    elif sc == 1:
        for idx, (lbl, cmd) in enumerate([("Native Unity Tests", "pio test -e native -> PASS"), ("ESP32 Firmware Build", "pio run -e esp32doit-devkit-v1 -> OK")]):
            ry = 236 + idx * 104
            draw_card(draw, 738, ry, 1212, ry + 82, PASS_BG, PASS_FG, radius=12, shadow=False)
            draw_check(draw, 770, ry + 41, 15, PASS_FG)
            draw_text_vcenter_left(draw, 800 * S, (ry + 10) * S, (ry + 42) * S, lbl, F_BODY_B, TEXT)
            draw_text_vcenter_left(draw, 800 * S, (ry + 42) * S, (ry + 72) * S, cmd, F_CODE, PASS_FG)
    elif sc == 2:
        # 4 files liquid-merging via Bezier streams into merged-firmware.bin
        parts = [("0x1000", "bootloader"), ("0x8000", "partitions"), ("0xe000", "boot_app0"), ("0x10000", "firmware")]
        for idx, (off, name) in enumerate(parts):
            ry = 228 + idx * 72
            draw_card(draw, 738, ry, 945, ry + 54, BLUE_SOFT, BLUE, radius=10, shadow=False)
            draw_pill(draw, 748, ry + 10, off, BLUE_TINT, NAVY, font=F_CODE_B, pad_x=8, pad_y=4, min_h=34)
            draw_text_vcenter_left(draw, 838 * S, ry * S, (ry + 54) * S, name, F_CODE_B, TEXT)
            draw_liquid_stream(draw, 945 * S, (ry + 27) * S, 1020 * S, 365 * S, PASS_FG if st > 0.7 else BLUE, t_raw, n_droplets=2)

        draw_card(draw, 1022, 260, 1218, 470, PASS_BG if st > 0.7 else BLUE_SOFT, PASS_FG if st > 0.7 else BLUE, radius=20, shadow=False)
        draw_text_center_box(draw, 1022 * S, 260 * S, 1218 * S, 470 * S, "merged-\nfirmware\n.bin\n\n(0x0)", F_MONO_B, PASS_FG if st > 0.7 else NAVY)
    else:
        draw_card(draw, 738, 228, 1212, 515, SURFACE_ALT, PASS_FG, radius=12, shadow=False)
        draw_pill(draw, 762, 248, "Release v1.0.0 Published", PASS_FG, "#FFFFFF", font=F_BODY_B, min_h=38)
        draw_card(draw, 762, 308, 1188, 384, "#FFFFFF", BORDER, radius=10, shadow=False)
        draw_pill(draw, 780, 328, "OTA", BLUE_TINT, NAVY, min_h=34)
        draw_text_vcenter_left(draw, 860 * S, 308 * S, 384 * S, "esp32doit-v1.0.0-firmware.bin", F_CODE_B, TEXT)
        draw_card(draw, 762, 400, 1188, 476, PASS_BG, PASS_FG, radius=10, shadow=False)
        draw_pill(draw, 780, 420, "0x0", PASS_FG, "#FFFFFF", min_h=34)
        draw_text_vcenter_left(draw, 860 * S, 400 * S, 476 * S, "esp32doit-v1.0.0-merged-firmware.bin", F_CODE_B, PASS_FG)

    draw_bottom_callout(draw, f"release.yml — {title}", thai, stream_col)


SCENES: List[Tuple[str, int, Callable[[ImageDraw.ImageDraw, float], None]]] = [
    ("01-bug-report-yml.mp4", 16, render_01_bug),
    ("02-feature-request-yml.mp4", 15, render_02_feat),
    ("03-config-yml.mp4", 15, render_03_cfg),
    ("04-pull-request-template-md.mp4", 15, render_04_pr),
    ("05-ci-yml.mp4", 16, render_05_ci),
    ("06-release-yml.mp4", 16, render_06_rel),
]


def render_video(filename: str, duration_sec: int, renderer: Callable[[ImageDraw.ImageDraw, float], None], out_dir: Path) -> None:
    out_mp4 = out_dir / filename
    total_frames = FPS * duration_sec
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{OUT_W}x{OUT_H}", "-r", str(FPS), "-i", "-",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "20",
        "-movflags", "+faststart", str(out_mp4),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    assert proc.stdin is not None
    try:
        for frame_idx in range(total_frames):
            t_raw = frame_idx / max(1, total_frames - 1)
            img = Image.new("RGB", (WIDTH, HEIGHT), BG)
            draw = ImageDraw.Draw(img)
            draw_liquid_bg(draw, t_raw)
            renderer(draw, t_raw)
            # 2x Supersampled LANCZOS downscale to 1280x720
            out_img = img.resize((OUT_W, OUT_H), Image.Resampling.LANCZOS)
            proc.stdin.write(out_img.tobytes())
        proc.stdin.close()
        if proc.wait() != 0:
            raise RuntimeError(f"ffmpeg failed for {filename}")
    finally:
        if proc.poll() is None:
            proc.kill()
    print(f"Generated (2x SS -> {OUT_W}x{OUT_H} @ {FPS}fps, {duration_sec}s): {out_mp4}")


def main() -> int:
    if not shutil.which("ffmpeg"):
        print("Error: ffmpeg not found in PATH", file=sys.stderr)
        return 1
    out_dir = Path(__file__).resolve().parents[1] / "github"
    out_dir.mkdir(parents=True, exist_ok=True)
    for filename, dur, renderer in SCENES:
        render_video(filename, dur, renderer, out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
