#!/usr/bin/env python3
"""
Generate 6 crisp 1280x720 @ 24fps Motion Graphic Vector Explanation MP4s
in a Snow & Arctic Blue theme (#F4F8FC) with:
- 100% ASCII/English CLI in monospace CMD bars (zero missing Thai glyphs)
- 100% true vertical & horizontal text centering via bbox midpoints
- Real result screenshots from docs/images/*.png in framed cards
using Pillow + FFmpeg (libx264, yuv420p).
"""

import math
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Callable, Dict, List, Tuple

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1280, 720
FPS = 24
ROOT_DIR = Path(__file__).resolve().parents[2]
IMAGES_DIR = ROOT_DIR / "docs" / "images"

# Snow & Arctic Blue Palette
BG = "#F4F8FC"
GRID = "#E8F0FA"
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

# Semantic colors (used ONLY for PASS / BLOCKED highlights)
PASS_FG = "#059669"
PASS_BG = "#ECFDF5"
BLOCK_FG = "#DC2626"
BLOCK_BG = "#FEF2F2"


def load_font(size: int, bold: bool = False, mono: bool = False) -> ImageFont.FreeTypeFont:
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
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


F_TITLE = load_font(25, bold=True)
F_SUB = load_font(16, bold=False)
F_STAGE = load_font(22, bold=True)
F_HEAD = load_font(19, bold=True)
F_BODY = load_font(17, bold=False)
F_BODY_B = load_font(17, bold=True)
F_SMALL = load_font(14, bold=False)
F_SMALL_B = load_font(14, bold=True)
F_MONO = load_font(16, bold=False, mono=True)
F_MONO_B = load_font(16, bold=True, mono=True)
F_MONO_LG = load_font(19, bold=True, mono=True)


# --- Screenshot Preloader ---

_SHOT_CACHE: Dict[Tuple[str, int, int], Image.Image] = {}


def get_fitted_screenshot(filename: str, max_w: int, max_h: int) -> Image.Image:
    key = (filename, max_w, max_h)
    if key not in _SHOT_CACHE:
        path = IMAGES_DIR / filename
        im = Image.open(path).convert("RGB")
        sw, sh = im.size
        scale = min(max_w / sw, max_h / sh)
        nw, nh = max(1, int(sw * scale)), max(1, int(sh * scale))
        _SHOT_CACHE[key] = im.resize((nw, nh), Image.Resampling.LANCZOS)
    return _SHOT_CACHE[key]


def draw_screenshot_card(
    img: Image.Image,
    draw: ImageDraw.ImageDraw,
    filename: str,
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    caption: str = "",
    outline: str = BLUE,
) -> None:
    draw.rounded_rectangle([x0 + 3, y0 + 5, x1 + 3, y1 + 5], radius=12, fill=SHADOW)
    draw.rounded_rectangle([x0, y0, x1, y1], radius=12, fill=SURFACE, outline=outline, width=2)
    pad = 10
    cap_h = 28 if caption else 0
    max_w = int((x1 - x0) - pad * 2)
    max_h = int((y1 - y0) - pad * 2 - cap_h)
    shot = get_fitted_screenshot(filename, max_w, max_h)
    sx = int(x0 + ((x1 - x0) - shot.width) / 2)
    sy = int(y0 + pad + (max_h - shot.height) / 2)
    img.paste(shot, (sx, sy))
    draw.rectangle([sx, sy, sx + shot.width, sy + shot.height], outline=BORDER_MUTED, width=1)
    if caption:
        draw_text_center_box(draw, x0, y1 - cap_h - 4, x1, y1 - 2, caption, F_SMALL_B, NAVY)


# --- Math & Easing ---

def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def seg_t(t: float, start: float, end: float) -> float:
    if end <= start:
        return 1.0 if t >= end else 0.0
    return clamp01((t - start) / (end - start))


def ease_out_cubic(t: float) -> float:
    t = clamp01(t)
    return 1.0 - (1.0 - t) ** 3


def ease_in_out_cubic(t: float) -> float:
    t = clamp01(t)
    return 4 * t * t * t if t < 0.5 else 1 - ((-2 * t + 2) ** 3) / 2


def hex_to_rgb(h: str) -> Tuple[int, int, int]:
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def mix_color(c_bg: str, c_fg: str, alpha: float) -> str:
    a = clamp01(alpha)
    r1, g1, b1 = hex_to_rgb(c_bg)
    r2, g2, b2 = hex_to_rgb(c_fg)
    return f"#{int(r1 + (r2 - r1) * a):02x}{int(g1 + (g2 - g1) * a):02x}{int(b1 + (b2 - b1) * a):02x}"


# --- Base Grid ---

def make_bg() -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    for x in range(0, WIDTH, 40):
        draw.line([(x, 0), (x, HEIGHT)], fill=GRID, width=1)
    for y in range(0, HEIGHT, 40):
        draw.line([(0, y), (WIDTH, y)], fill=GRID, width=1)
    return img


BASE_BG = make_bg()


# --- True-Centered Text Helpers ---

def draw_text_center_box(
    draw: ImageDraw.ImageDraw,
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: str,
) -> None:
    cx = (x0 + x1) / 2.0
    cy = (y0 + y1) / 2.0
    if "\n" in text:
        bbox = draw.multiline_textbbox((0, 0), text, font=font, align="center", spacing=6)
        tx = cx - (bbox[0] + bbox[2]) / 2.0
        ty = cy - (bbox[1] + bbox[3]) / 2.0
        draw.multiline_text((tx, ty), text, font=font, fill=fill, align="center", spacing=6)
    else:
        bbox = draw.textbbox((0, 0), text, font=font)
        tx = cx - (bbox[0] + bbox[2]) / 2.0
        ty = cy - (bbox[1] + bbox[3]) / 2.0
        draw.text((tx, ty), text, font=font, fill=fill)


def draw_text_vcenter_left(
    draw: ImageDraw.ImageDraw,
    x: float,
    y0: float,
    y1: float,
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: str,
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
    pad_x: int = 16,
    pad_y: int = 9,
    radius: int = 10,
    min_h: float = 0,
) -> Tuple[float, float, float, float]:
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    w = tw + pad_x * 2
    h = max(min_h, th + pad_y * 2)
    x1, y1 = x + w, y + h
    draw.rounded_rectangle([x, y, x1, y1], radius=radius, fill=bg, outline=border if border else None, width=2 if border else 0)
    draw_text_center_box(draw, x, y, x1, y1, text, font, fg)
    return x, y, x1, y1


def draw_pill_right(
    draw: ImageDraw.ImageDraw,
    x_right: float,
    y: float,
    text: str,
    bg: str,
    fg: str,
    border: str = "",
    font: ImageFont.FreeTypeFont = F_SMALL_B,
    pad_x: int = 16,
    pad_y: int = 9,
    min_h: float = 0,
) -> Tuple[float, float, float, float]:
    bbox = draw.textbbox((0, 0), text, font=font)
    w = (bbox[2] - bbox[0]) + pad_x * 2
    return draw_pill(draw, x_right - w, y, text, bg, fg, border, font, pad_x, pad_y, min_h=min_h)


def draw_box_with_text(
    draw: ImageDraw.ImageDraw,
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    text: str,
    fill: str = SURFACE_ALT,
    outline: str = BORDER,
    fg: str = TEXT,
    font: ImageFont.FreeTypeFont = F_BODY_B,
    radius: int = 12,
    width: int = 2,
) -> None:
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)
    draw_text_center_box(draw, x0, y0, x1, y1, text, font, fg)


def draw_focus_card(
    draw: ImageDraw.ImageDraw,
    x0: float = 56,
    y0: float = 108,
    x1: float = 1224,
    y1: float = 566,
    outline: str = BORDER,
    fill: str = SURFACE,
    radius: int = 18,
) -> None:
    draw.rounded_rectangle([x0 + 4, y0 + 7, x1 + 4, y1 + 7], radius=radius, fill=SHADOW)
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=2)


def draw_sub_card(
    draw: ImageDraw.ImageDraw,
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    fill: str = BLUE_SOFT,
    outline: str = BORDER,
    radius: int = 12,
    width: int = 2,
) -> None:
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)


def draw_cmd_bar(
    draw: ImageDraw.ImageDraw,
    x0: float,
    y0: float,
    x1: float,
    cmd: str,
    st: float,
    accent: str = BLUE,
    type_end: float = 0.28,
) -> bool:
    """Top Command/Event bar inside focus card. Strictly ASCII/English for monospace font."""
    assert cmd.isascii(), f"CMD bar must be pure ASCII/English, got: {cmd!r}"
    y1 = y0 + 54
    draw.rounded_rectangle([x0, y0, x1, y1], radius=12, fill=NAVY, outline=accent, width=2)
    p_type = seg_t(st, 0.0, type_end)
    n_chars = max(1, int(len(cmd) * p_type))
    shown = cmd[:n_chars]
    cursor = "_" if p_type < 1.0 else ""
    draw_text_vcenter_left(draw, x0 + 20, y0, y1, f"$ {shown}{cursor}", F_MONO_LG, "#FFFFFF")

    entered = st >= type_end
    enter_pulse = type_end <= st <= type_end + 0.12
    pill_bg = SKY if enter_pulse else (PASS_FG if entered else "#334155")
    draw_pill_right(draw, x1 - 12, y0 + 9, "ENTER", pill_bg, "#FFFFFF", font=F_SMALL_B, pad_x=14, pad_y=6, min_h=36)
    return entered


def draw_arrow(
    draw: ImageDraw.ImageDraw,
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    color: str,
    progress: float = 1.0,
    width: int = 4,
    head: int = 12,
) -> None:
    p = clamp01(progress)
    if p <= 0.01:
        return
    cx, cy = lerp(x0, x1, p), lerp(y0, y1, p)
    draw.line([(x0, y0), (cx, cy)], fill=color, width=width)
    if p > 0.15:
        angle = math.atan2(y1 - y0, x1 - x0)
        a1, a2 = angle + math.radians(150), angle - math.radians(150)
        draw.polygon(
            [(cx, cy), (cx + head * math.cos(a1), cy + head * math.sin(a1)), (cx + head * math.cos(a2), cy + head * math.sin(a2))],
            fill=color,
        )


def draw_dashed_line(
    draw: ImageDraw.ImageDraw, x0: float, y0: float, x1: float, y1: float, color: str, dash: int = 10, gap: int = 8, width: int = 3
) -> None:
    dist = math.hypot(x1 - x0, y1 - y0)
    if dist < 1:
        return
    dx, dy = (x1 - x0) / dist, (y1 - y0) / dist
    pos = 0.0
    while pos < dist:
        end = min(dist, pos + dash)
        draw.line([(x0 + dx * pos, y0 + dy * pos), (x0 + dx * end, y0 + dy * end)], fill=color, width=width)
        pos += dash + gap


def draw_check(draw: ImageDraw.ImageDraw, cx: float, cy: float, r: float, bg: str = PASS_FG) -> None:
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=bg)
    pts = [(cx - r * 0.44, cy + r * 0.02), (cx - r * 0.12, cy + r * 0.36), (cx + r * 0.46, cy - r * 0.32)]
    draw.line(pts, fill="#FFFFFF", width=max(2, int(r * 0.22)), joint="curve")


def draw_x_mark(draw: ImageDraw.ImageDraw, cx: float, cy: float, r: float, bg: str = BLOCK_FG) -> None:
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=bg)
    d = r * 0.36
    w = max(2, int(r * 0.22))
    draw.line([(cx - d, cy - d), (cx + d, cy + d)], fill="#FFFFFF", width=w)
    draw.line([(cx - d, cy + d), (cx + d, cy - d)], fill="#FFFFFF", width=w)


def draw_commit_node(
    draw: ImageDraw.ImageDraw, cx: float, cy: float, r: float, label: str, fill: str, outline: str, text_color: str = TEXT
) -> None:
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=outline, width=3)
    draw_text_center_box(draw, cx - r, cy - r, cx + r, cy + r, label, F_MONO_B, text_color)


def draw_chrome(
    draw: ImageDraw.ImageDraw,
    module_tag: str,
    title: str,
    subtitle: str,
    scene_idx: int,
    total_scenes: int,
    t_raw: float,
    duration_sec: int,
) -> None:
    draw.rectangle([0, 0, WIDTH, 90], fill=SURFACE)
    draw.line([(0, 90), (WIDTH, 90)], fill=BORDER, width=2)

    _, _, tag_x1, _ = draw_pill(draw, 40, 14, module_tag, NAVY, "#FFFFFF", font=F_SMALL_B, pad_x=12, pad_y=6, min_h=30)
    draw_text_vcenter_left(draw, tag_x1 + 14, 12, 46, title, F_TITLE, TEXT)
    draw_text_vcenter_left(draw, 40, 50, 82, subtitle, F_SUB, SKY)

    px = WIDTH - 40
    for idx in range(total_scenes - 1, -1, -1):
        label = f"ขั้นตอน {idx + 1}/{total_scenes}"
        is_active = idx == scene_idx
        is_done = idx < scene_idx
        bg = BLUE if is_active else (BLUE_TINT if is_done else SURFACE_ALT)
        fg = "#FFFFFF" if is_active else (NAVY if is_done else TEXT_MUTED)
        border = BLUE if is_active else (BORDER if is_done else BORDER_MUTED)
        x0, _, _, _ = draw_pill_right(draw, px, 14, label, bg, fg, border, F_SMALL_B, pad_x=12, pad_y=6, min_h=30)
        px = x0 - 8

    draw.rectangle([0, HEIGHT - 46, WIDTH, HEIGHT], fill=SURFACE)
    draw.line([(0, HEIGHT - 46), (WIDTH, HEIGHT - 46)], fill=BORDER, width=2)
    bx0, bx1, by = 40, WIDTH - 145, HEIGHT - 23
    draw.rounded_rectangle([bx0, by - 4, bx1, by + 4], radius=4, fill=BLUE_TINT)
    draw.rounded_rectangle([bx0, by - 4, bx0 + (bx1 - bx0) * clamp01(t_raw), by + 4], radius=4, fill=BLUE)
    sec = min(duration_sec, int(t_raw * duration_sec))
    draw_text_vcenter_left(draw, WIDTH - 125, HEIGHT - 46, HEIGHT, f"00:{sec:02d} / 00:{duration_sec:02d}", F_MONO, TEXT_MUTED)


def draw_bottom_callout(draw: ImageDraw.ImageDraw, title: str, thai: str, accent: str = BLUE) -> None:
    draw.rounded_rectangle([60, 586, 1228, 662], radius=12, fill=SHADOW)
    draw.rounded_rectangle([56, 582, 1224, 658], radius=12, fill=SURFACE, outline=accent, width=2)
    draw.rectangle([70, 594, 76, 646], fill=accent)
    draw_text_vcenter_left(draw, 92, 588, 618, title, F_BODY_B, TEXT)
    draw_text_vcenter_left(draw, 92, 620, 652, thai, F_BODY, TEXT_SUB)


def split_scenes(t_raw: float, n_scenes: int, hold_sec: float, duration_sec: int) -> Tuple[int, float]:
    anim_sec = max(1.0, duration_sec - hold_sec)
    sec = t_raw * duration_sec
    if sec >= anim_sec:
        return n_scenes - 1, 1.0
    per = anim_sec / n_scenes
    idx = min(n_scenes - 1, int(sec / per))
    st = clamp01((sec - idx * per) / per)
    return idx, st


# ==============================================================================
# 01: Linear History (Rebase) — 15s (3 scenes)
# ==============================================================================

def render_01(img: Image.Image, draw: ImageDraw.ImageDraw, t_raw: float) -> None:
    sc, st = split_scenes(t_raw, 3, 2.5, 15)
    draw_chrome(draw, "MODULE 01", "Linear History (Rebase) & Conventional Commits", "แตก Branch, ทำงานแยก, แล้ว Rebase ให้ประวัติเป็นเส้นตรงเส้นเดียว", sc, 3, t_raw, 15)
    draw_focus_card(draw)

    if sc == 0:
        entered = draw_cmd_bar(draw, 86, 128, 1194, "git switch -c feature/fast-blink", st)
        p = ease_out_cubic(seg_t(st, 0.30, 0.85)) if entered else 0.0

        draw.line([(210, 425), (520, 425)], fill=BLUE, width=5)
        draw_pill(draw, 96, 405, "main", BLUE_TINT, NAVY, BLUE, min_h=40)
        draw_commit_node(draw, 250, 425, 26, "C0", BLUE_SOFT, BLUE)
        draw_commit_node(draw, 420, 425, 26, "C1", BLUE_SOFT, BLUE)

        if p > 0.05:
            draw.line([(420, 425), (520, 300), (lerp(520, 950, p), 300)], fill=SKY, width=5)
            draw_pill(draw, 910, 232, "feature/fast-blink", BLUE_TINT, SKY, SKY, min_h=38)
            if p > 0.35:
                draw_commit_node(draw, 640, 300, 26, "C2", "#FFFFFF", SKY)
            if p > 0.70:
                draw_commit_node(draw, 830, 300, 26, "C3", "#FFFFFF", SKY)

        draw_bottom_callout(draw, "ขั้นตอน 1: แตก Branch ใหม่", "สร้าง branch feature/fast-blink ออกจาก C1 แล้วเพิ่ม Commit C2, C3", BLUE)

    elif sc == 1:
        draw_cmd_bar(draw, 86, 128, 1194, "git fetch origin  # main updated with C4", st)
        p = ease_out_cubic(seg_t(st, 0.30, 0.85))

        draw.line([(210, 425), (lerp(420, 820, p), 425)], fill=BLUE, width=5)
        draw_pill(draw, 96, 405, "main", BLUE_TINT, NAVY, BLUE, min_h=40)
        draw_commit_node(draw, 250, 425, 26, "C0", BLUE_SOFT, BLUE)
        draw_commit_node(draw, 420, 425, 26, "C1", BLUE_SOFT, BLUE)
        if p > 0.35:
            draw_commit_node(draw, 720, 425, 28, "C4", BLUE_TINT, NAVY)
            draw_pill(draw, 646, 466, "New on main", BLUE_SOFT, ROYAL, BLUE, min_h=34)

        draw.line([(420, 425), (520, 295), (860, 295)], fill=SKY, width=4)
        draw_pill(draw, 96, 275, "feature/*", BLUE_SOFT, SKY, SKY, min_h=38)
        draw_commit_node(draw, 620, 295, 24, "C2", "#FFFFFF", SKY)
        draw_commit_node(draw, 790, 295, 24, "C3", "#FFFFFF", SKY)

        if p > 0.65:
            draw_dashed_line(draw, 790, 295, 960, 425, BLOCK_FG)
            draw_commit_node(draw, 960, 425, 24, "M", BLOCK_BG, BLOCK_FG, BLOCK_FG)
            draw_pill(draw, 888, 336, "Merge ไขว้!", BLOCK_BG, BLOCK_FG, BLOCK_FG, min_h=36)

        draw_bottom_callout(draw, "ขั้นตอน 2: ประวัติแยกสาย", "main อัปเดต C4 แล้ว หากใช้ Merge ปกติจะเกิดปมไขว้ M อ่านประวัติยาก", ROYAL)

    else:
        entered = draw_cmd_bar(draw, 86, 128, 1194, "git rebase origin/main", st, PASS_FG if st > 0.68 else BLUE)
        p = ease_in_out_cubic(seg_t(st, 0.22, 0.68)) if entered else 0.0

        line_y = 265 if p > 0.72 else 415
        draw.line([(210, line_y), (1120, line_y)], fill=PASS_FG if p > 0.72 else BLUE, width=5)
        draw_pill(draw, 96, line_y - 20, "main", BLUE_TINT, NAVY, BLUE, min_h=40)
        draw_commit_node(draw, 250, line_y, 24, "C0", BLUE_SOFT, BLUE)
        draw_commit_node(draw, 410, line_y, 24, "C1", BLUE_SOFT, BLUE)
        draw_commit_node(draw, 580, line_y, 26, "C4", BLUE_TINT, NAVY)

        if p < 0.72:
            g_col = mix_color(SURFACE, BORDER, 1.0 - p)
            draw_dashed_line(draw, 410, line_y, 530, 295, g_col)
            draw_commit_node(draw, 540, 295, 20, "C2", SURFACE, g_col, g_col)
            draw_commit_node(draw, 680, 295, 20, "C3", SURFACE, g_col, g_col)

        arc = math.sin(p * math.pi) * 55
        c2x, c2y = lerp(540, 770, p), lerp(295, line_y, p) - arc
        c3x, c3y = lerp(680, 960, p), lerp(295, line_y, p) - arc
        draw_commit_node(draw, c2x, c2y, 26, "C2'", PASS_BG if p > 0.7 else BLUE_SOFT, PASS_FG if p > 0.7 else SKY)
        draw_commit_node(draw, c3x, c3y, 26, "C3'", PASS_BG if p > 0.7 else BLUE_SOFT, PASS_FG if p > 0.7 else SKY)

        if p > 0.72:
            draw_screenshot_card(img, draw, "term-01-git-log.png", 96, 315, 1184, 545, "ผลลัพธ์จริง: git log --oneline --graph (Linear History)", PASS_FG)

        draw_bottom_callout(draw, "ขั้นตอน 3: Linear History เส้นตรง", "ยก C2, C3 มาต่อท้าย C4 เป็นเส้นตรงเส้นเดียว อ่านง่ายและย้อนตรวจได้แม่นยำ", PASS_FG if p > 0.72 else BLUE)


# ==============================================================================
# 02: Issue #2 -> PR (Closes #2) + Branch Protection -> Rebase & Merge — 16s
# ==============================================================================

def render_02(img: Image.Image, draw: ImageDraw.ImageDraw, t_raw: float) -> None:
    sc, st = split_scenes(t_raw, 3, 2.5, 16)
    draw_chrome(draw, "MODULE 02", "Issue Forms, Pull Request & Rebase Merge", "เปิด Issue #2 -> เปิด PR (Closes #2) -> Branch Protection -> Rebase & Merge", sc, 3, t_raw, 16)
    draw_focus_card(draw)

    if sc == 0:
        draw_cmd_bar(draw, 86, 128, 1194, "gh issue create --template bug_report.yml", st)
        p = ease_out_cubic(seg_t(st, 0.28, 0.80))

        draw_sub_card(draw, 96, 206, 750, 532, SURFACE_ALT, BORDER)
        draw_pill(draw, 120, 224, "Bug Report Form (.yml)", BLUE_TINT, NAVY, BLUE, min_h=34)
        for idx, txt in enumerate(["หัวข้อ: Fast blink LED timing issue", "บอร์ด: ESP32 DOIT DevKit V1", "ผลที่คาดหวัง: Blink 100ms cleanly"]):
            fy = 278 + idx * 72
            draw_sub_card(draw, 120, fy, 724, fy + 52, "#FFFFFF", BORDER)
            draw_text_vcenter_left(draw, 140, fy, fy + 52, txt, F_BODY, TEXT)

        draw_arrow(draw, 770, 368, 880, 368, BLUE, p)
        if p > 0.55:
            draw_box_with_text(draw, 895, 280, 1184, 456, "Issue #2\n\nOPENED", PASS_BG, PASS_FG, PASS_FG, F_STAGE, width=3)

        draw_bottom_callout(draw, "ขั้นตอน 1: เปิด Issue #2 จากแบบฟอร์ม", "กรอกข้อมูลครบผ่าน Issue Form (.yml) แล้วระบบออกหมายเลข Issue #2 อัตโนมัติ", BLUE)

    elif sc == 1:
        draw_cmd_bar(draw, 86, 128, 1194, 'gh pr create --base main --body "Closes #2"', st)
        draw_sub_card(draw, 96, 204, 1184, 536, SURFACE_ALT, BLUE)
        draw_pill(draw, 124, 222, "Branch Protection Gate", BLUE_TINT, NAVY, BLUE, min_h=36)
        draw_text_vcenter_left(draw, 355, 222, 258, "PR #3: feat(blink): fast preset  (Closes #2)", F_BODY_B, TEXT)

        gates = [
            ("Checklist จาก PR Template ครบถ้วน", st > 0.35),
            ("CI Status Check: lint + test-native + build-esp32 PASS", st > 0.58),
            ("Require linear history: พร้อมปลดล็อก Merge", st > 0.80),
        ]
        for idx, (label, ok) in enumerate(gates):
            gy = 282 + idx * 74
            draw_sub_card(draw, 124, gy, 1154, gy + 54, PASS_BG if ok else "#FFFFFF", PASS_FG if ok else BORDER)
            if ok:
                draw_check(draw, 154, gy + 27, 14, PASS_FG)
            draw_text_vcenter_left(draw, 184, gy, gy + 54, label, F_BODY_B if ok else F_BODY, PASS_FG if ok else TEXT_MUTED)

        draw_bottom_callout(draw, "ขั้นตอน 2: ด่าน Branch Protection", "ตรวจสอบ Checklist และรอ CI ผ่านครบทุกตัวก่อนปลดล็อกปุ่ม Rebase & Merge", PASS_FG if st > 0.80 else BLUE)

    else:
        entered = draw_cmd_bar(draw, 86, 128, 1194, "gh pr merge 3 --rebase --delete-branch", st, PASS_FG if st > 0.68 else BLUE)
        p = ease_in_out_cubic(seg_t(st, 0.25, 0.72)) if entered else 0.0

        # Left summary
        draw.line([(160, 310), (540, 310)], fill=BLUE, width=5)
        draw_pill(draw, 86, 290, "main", BLUE_TINT, NAVY, BLUE, min_h=40)
        draw_commit_node(draw, 220, 310, 22, "C1", BLUE_SOFT, BLUE)
        draw_commit_node(draw, 350, 310, 22, "C2", BLUE_SOFT, BLUE)
        draw_commit_node(draw, lerp(460, 485, p), lerp(230, 310, p), 24, "PR3", PASS_BG if p > 0.7 else BLUE_SOFT, PASS_FG if p > 0.7 else SKY)

        if p > 0.7:
            draw_pill(draw, 86, 388, "Branch Auto-Deleted", BLOCK_BG, BLOCK_FG, BLOCK_FG, min_h=38)
            draw_pill(draw, 86, 444, "Issue #2 Closed Automatically", PASS_BG, PASS_FG, PASS_FG, min_h=38)

        # Right real screenshot
        draw_screenshot_card(img, draw, "gh-03-pr-detail.png", 590, 200, 1194, 545, "ผลลัพธ์จริง: PR Merged + All Checks Green", PASS_FG if p > 0.7 else BLUE)

        draw_bottom_callout(draw, "ขั้นตอน 3: Rebase & Merge สมบูรณ์", "ต่อท้าย main เป็นเส้นตรง ลบ branch ชั่วคราวอัตโนมัติ และปิด Issue #2 ทันที", PASS_FG if p > 0.7 else BLUE)


# ==============================================================================
# 03: Pre-commit Hooks — 15s (3 scenes, Scene 2 matches Scene 1 layout!)
# ==============================================================================

def render_03(img: Image.Image, draw: ImageDraw.ImageDraw, t_raw: float) -> None:
    sc, st = split_scenes(t_raw, 3, 2.5, 15)
    draw_chrome(draw, "MODULE 03", "Pre-commit Hooks (clang-format & Commit Lint)", "ด่านตรวจบนเครื่อง: จัดหน้า C++ อัตโนมัติและบล็อกชื่อ Commit ที่ผิดมาตรฐาน", sc, 3, t_raw, 15)
    draw_focus_card(draw)

    if sc == 0:
        # Scene 1: FAIL layout (2 side-by-side panels)
        entered = draw_cmd_bar(draw, 86, 128, 1194, 'git commit -m "add blink"', st, BLOCK_FG if st > 0.45 else BLUE)
        blocked = entered and st > 0.45

        draw_sub_card(draw, 86, 204, 620, 536, BLUE_SOFT, BLUE)
        draw_pill(draw, 110, 224, "Hook 1: clang-format", BLUE_TINT, NAVY, BLUE, min_h=36)
        draw_text_vcenter_left(draw, 110, 282, 314, "Before:  if(x){blink();}", F_MONO, TEXT_MUTED)
        if entered:
            draw_text_vcenter_left(draw, 110, 336, 368, "After:   if (x) {", F_MONO_B, ROYAL)
            draw_text_vcenter_left(draw, 110, 368, 400, "           blink();", F_MONO_B, ROYAL)
            draw_text_vcenter_left(draw, 110, 400, 432, "         }", F_MONO_B, ROYAL)
            draw_pill(draw, 110, 464, "AUTO-FIXED (จัดหน้า C++ ให้แล้ว)", BLUE_TINT, NAVY, BLUE, min_h=40)

        draw_sub_card(draw, 650, 204, 1194, 536, BLOCK_BG if blocked else SURFACE_ALT, BLOCK_FG if blocked else BORDER)
        draw_pill(draw, 676, 224, "Hook 2: conventional-pre-commit", BLOCK_BG if blocked else BLUE_TINT, BLOCK_FG if blocked else NAVY, BLOCK_FG if blocked else BLUE, min_h=36)
        draw_text_vcenter_left(draw, 676, 300, 344, 'git commit -m "add blink"', F_MONO_LG, BLOCK_FG if blocked else TEXT)
        if blocked:
            draw_x_mark(draw, 1146, 244, 20, BLOCK_FG)
            draw_text_vcenter_left(draw, 676, 370, 412, "ขาด prefix เช่น feat: / fix: / style:", F_BODY_B, BLOCK_FG)
            draw_pill(draw, 676, 464, "BLOCKED! แก้ชื่อ Commit แล้วลองใหม่", BLOCK_FG, "#FFFFFF", min_h=40)

        draw_bottom_callout(draw, "ขั้นตอน 1: Pre-commit Hook จับจุดผิดพลาด", "clang-format จัดรูปโค้ดให้เรียบร้อย ส่วน conventional-pre-commit บล็อกชื่อที่ไม่มี prefix", BLOCK_FG if blocked else BLUE)

    elif sc == 1:
        # Scene 2: PASS — EXACT SAME 2-panel layout as Scene 1!
        entered = draw_cmd_bar(draw, 86, 128, 1194, 'git commit -m "feat: add blink"', st, PASS_FG if st > 0.45 else BLUE)
        passed = entered and st > 0.45

        draw_sub_card(draw, 86, 204, 620, 536, PASS_BG if passed else BLUE_SOFT, PASS_FG if passed else BLUE)
        draw_pill(draw, 110, 224, "Hook 1: clang-format & whitespace", PASS_BG if passed else BLUE_TINT, PASS_FG if passed else NAVY, PASS_FG if passed else BLUE, min_h=36)
        draw_text_vcenter_left(draw, 110, 290, 326, "Formatted C++:", F_MONO, TEXT_SUB)
        draw_text_vcenter_left(draw, 110, 336, 368, "if (x) {", F_MONO_B, PASS_FG if passed else ROYAL)
        draw_text_vcenter_left(draw, 110, 368, 400, "  blink();", F_MONO_B, PASS_FG if passed else ROYAL)
        draw_text_vcenter_left(draw, 110, 400, 432, "}", F_MONO_B, PASS_FG if passed else ROYAL)
        if passed:
            draw_check(draw, 572, 244, 20, PASS_FG)
            draw_pill(draw, 110, 464, "PASS! โค้ดสะอาดตามมาตรฐาน", PASS_FG, "#FFFFFF", min_h=40)

        draw_sub_card(draw, 650, 204, 1194, 536, PASS_BG if passed else SURFACE_ALT, PASS_FG if passed else BORDER)
        draw_pill(draw, 676, 224, "Hook 2: conventional-pre-commit", PASS_BG if passed else BLUE_TINT, PASS_FG if passed else NAVY, PASS_FG if passed else BLUE, min_h=36)
        draw_text_vcenter_left(draw, 676, 300, 344, 'git commit -m "feat: add blink"', F_MONO_LG, PASS_FG if passed else TEXT)
        if passed:
            draw_check(draw, 1146, 244, 20, PASS_FG)
            draw_text_vcenter_left(draw, 676, 370, 412, 'มี prefix "feat:" ถูกต้องตามมาตรฐาน', F_BODY_B, PASS_FG)
            draw_pill(draw, 676, 464, "PASS! บันทึก Commit สำเร็จ", PASS_FG, "#FFFFFF", min_h=40)

        draw_bottom_callout(draw, "ขั้นตอน 2: ผ่านครบทุกด่าน (PASS)", "แก้ชื่อเป็น feat: add blink แล้วทั้ง clang-format และ conventional-pre-commit ผ่านฉลุย", PASS_FG if passed else BLUE)

    else:
        # Scene 3: Real screenshot of pre-commit all Passed
        draw_cmd_bar(draw, 86, 128, 1194, "pre-commit run --all-files", 1.0, PASS_FG)
        draw_pill(draw, 86, 204, "Commit: feat: add blink", PASS_BG, PASS_FG, PASS_FG, F_MONO_B, min_h=40)
        draw_pill_right(draw, 1194, 204, "All Hooks Passed!", PASS_FG, "#FFFFFF", font=F_BODY_B, min_h=40)
        draw_screenshot_card(img, draw, "term-02-pre-commit.png", 86, 264, 1194, 545, "ผลลัพธ์จริง: Pre-commit Hooks ผ่านทั้งหมด", PASS_FG)

        draw_bottom_callout(draw, "ขั้นตอน 3: บันทึก Commit อย่างปลอดภัย", "โค้ดสะอาดและ Commit message เป็นมาตรฐานก่อนส่งขึ้น GitHub", PASS_FG)


# ==============================================================================
# 04: PlatformIO Unit Testing — 15s (3 scenes)
# ==============================================================================

def render_04(img: Image.Image, draw: ImageDraw.ImageDraw, t_raw: float) -> None:
    sc, st = split_scenes(t_raw, 3, 2.5, 15)
    draw_chrome(draw, "MODULE 04", "PlatformIO Unit Testing (Native Unity + ESP32)", "แยกตรรกะคำนวณมาเทสบน PC ให้ไว แล้วค่อย Build ลงบอร์ด ESP32 จริง", sc, 3, t_raw, 15)
    draw_focus_card(draw)

    if sc == 0:
        draw_cmd_bar(draw, 86, 128, 1194, "ls lib/blink_math/ src/main.cpp  # Decoupled", st)
        draw_sub_card(draw, 86, 212, 610, 534, BLUE_SOFT, BLUE, width=3)
        draw_pill(draw, 114, 234, "Pure C++ (คำนวณ)", BLUE, "#FFFFFF", min_h=38)
        draw_text_vcenter_left(draw, 114, 290, 326, "lib/blink_math/blink_math.cpp", F_MONO_B, NAVY)
        for idx, fn in enumerate(["• clamp_interval()", "• next_led_state()", "• calculate_cycle_ms()"]):
            draw_text_vcenter_left(draw, 114, 340 + idx * 38, 374 + idx * 38, fn, F_MONO, TEXT)
        draw_pill(draw, 114, 466, "ไม่พึ่ง Arduino.h -> เทสบน PC ได้", PASS_BG, PASS_FG, PASS_FG, min_h=40)

        draw_sub_card(draw, 650, 212, 1194, 534, SURFACE_ALT, BORDER)
        draw_pill(draw, 678, 234, "Hardware Layer (ขาบอร์ด)", BLUE_TINT, NAVY, BLUE, min_h=38)
        draw_text_vcenter_left(draw, 678, 290, 326, "src/main.cpp", F_MONO_B, NAVY)
        for idx, fn in enumerate(["• pinMode(LED_PIN, OUTPUT)", "• digitalWrite(LED_PIN, state)", "• delay(interval)"]):
            draw_text_vcenter_left(draw, 678, 340 + idx * 38, 374 + idx * 38, fn, F_MONO, TEXT_SUB)
        draw_pill(draw, 678, 466, "คอมไพล์ลงบอร์ด ESP32 จริง", BLUE_SOFT, SKY, SKY, min_h=40)

        draw_bottom_callout(draw, "ขั้นตอน 1: แยกไฟล์คำนวณออกจากฮาร์ดแวร์", "แยก blink_math.cpp ออกจาก digitalWrite ใน main.cpp เพื่อทดสอบบน PC ได้ทันที", BLUE)

    elif sc == 1:
        entered = draw_cmd_bar(draw, 86, 128, 1194, "pio test -e native", st, PASS_FG if st > 0.72 else BLUE)
        cases = [
            ("test_clamp_interval_bounds", entered and st > 0.35),
            ("test_next_led_state_toggles", entered and st > 0.54),
            ("test_calculate_cycle_ms", entered and st > 0.72),
        ]
        for idx, (cname, ok) in enumerate(cases):
            cy = 212 + idx * 102
            draw_sub_card(draw, 86, cy, 1194, cy + 80, PASS_BG if ok else SURFACE_ALT, PASS_FG if ok else BORDER)
            draw_text_vcenter_left(draw, 120, cy, cy + 80, cname, F_MONO_LG, TEXT)
            if ok:
                draw_pill_right(draw, 1160, cy + 18, "PASS", PASS_FG, "#FFFFFF", font=F_BODY_B, min_h=44)

        draw_bottom_callout(draw, "ขั้นตอน 2: รัน Unit Test บน PC (< 1 วินาที)", "รัน pio test -e native ผ่านครบ 3/3 เคสในเสี้ยววินาที โดยไม่ต้องต่อบอร์ด", PASS_FG if st > 0.72 else BLUE)

    else:
        entered = draw_cmd_bar(draw, 86, 128, 1194, "pio run -e esp32doit-devkit-v1", st, PASS_FG if st > 0.70 else BLUE)
        p = ease_out_cubic(seg_t(st, 0.28, 0.75)) if entered else 0.0

        draw_box_with_text(draw, 86, 220, 350, 410, "ESP32\nDevKit V1", BLUE_SOFT, NAVY, NAVY, F_STAGE, width=3)
        if p > 0.7:
            draw_pill(draw, 86, 434, "firmware.bin Built!", PASS_BG, PASS_FG, PASS_FG, F_BODY_B, min_h=42)
        draw_arrow(draw, 365, 315, 455, 315, PASS_FG if p > 0.7 else BLUE, p)

        draw_screenshot_card(img, draw, "term-03-pio-build.png", 470, 200, 1194, 545, "ผลลัพธ์จริง: PlatformIO Build ESP32 สำเร็จ", PASS_FG if p > 0.7 else BLUE)

        draw_bottom_callout(draw, "ขั้นตอน 3: คอมไพล์เฟิร์มแวร์ ESP32 สำเร็จ", "เมื่อตรรกะผ่านบน PC แล้ว จึง Build firmware.bin สำหรับบอร์ด ESP32 จริง", PASS_FG if p > 0.7 else BLUE)


# ==============================================================================
# 05: GitHub Actions CI — 15s (3 scenes)
# ==============================================================================

def render_05(img: Image.Image, draw: ImageDraw.ImageDraw, t_raw: float) -> None:
    sc, st = split_scenes(t_raw, 3, 2.5, 15)
    draw_chrome(draw, "MODULE 05", "GitHub Actions Continuous Integration (CI)", "git push / PR -> ด่าน on: [push, pull_request] -> lint & test-native -> build-esp32", sc, 3, t_raw, 15)
    draw_focus_card(draw)

    if sc == 0:
        entered = draw_cmd_bar(draw, 86, 128, 1194, "git push origin feature/fast-blink", st)
        p = ease_out_cubic(seg_t(st, 0.30, 0.82)) if entered else 0.0

        draw_box_with_text(draw, 96, 265, 430, 480, "Event Detector\n\non: [push, pull_request]", BLUE_SOFT, BLUE, NAVY, F_HEAD, width=3)
        draw_arrow(draw, 445, 372, 575, 372, PASS_FG if p > 0.5 else BLUE, p)
        if p > 0.4:
            draw_sub_card(draw, 590, 240, 1194, 505, PASS_BG if p > 0.75 else SURFACE_ALT, PASS_FG if p > 0.75 else ROYAL, width=3)
            draw_pill(draw, 622, 266, "TRIGGERED: ci.yml", PASS_FG if p > 0.75 else BLUE, "#FFFFFF", min_h=38)
            draw_text_vcenter_left(draw, 622, 330, 368, "Runner: ubuntu-latest", F_MONO_LG, NAVY)
            draw_text_vcenter_left(draw, 622, 380, 418, "Cache: ~/.platformio (Restored)", F_MONO, TEXT_SUB)
            draw_text_vcenter_left(draw, 622, 428, 466, "Starting parallel jobs: lint + test-native", F_BODY_B, PASS_FG if p > 0.75 else SKY)

        draw_bottom_callout(draw, "ขั้นตอน 1: Trigger เปิดเครื่อง ubuntu-latest", "เมื่อ push หรือเปิด PR ด่าน on: [push, pull_request] จะสั่งรัน ci.yml ทันที", PASS_FG if p > 0.75 else BLUE)

    elif sc == 1:
        draw_cmd_bar(draw, 86, 128, 1194, "gh run watch  # Running lint & test-native in parallel", 1.0, BLUE)
        p = ease_out_cubic(seg_t(st, 0.12, 0.78))
        ok = p > 0.85

        for idx, (jtitle, jcmd, jsub) in enumerate([
            ("Job 1: lint", "pre-commit run --all-files", "clang-format & whitespace"),
            ("Job 2: test-native", "pio test -e native", "Unity Unit Tests (3/3 cases)"),
        ]):
            x0 = 86 + idx * 574
            x1 = x0 + 534
            draw_sub_card(draw, x0, 212, x1, 524, PASS_BG if ok else BLUE_SOFT, PASS_FG if ok else BLUE, width=3)
            draw_pill(draw, x0 + 28, 236, jtitle, PASS_FG if ok else BLUE, "#FFFFFF", min_h=38)
            draw_text_vcenter_left(draw, x0 + 28, 300, 338, jcmd, F_MONO_B, TEXT)
            draw_text_vcenter_left(draw, x0 + 28, 344, 380, jsub, F_BODY, TEXT_SUB)
            draw.rounded_rectangle([x0 + 28, 404, x1 - 28, 434], radius=8, fill=BLUE_TINT)
            draw.rounded_rectangle([x0 + 28, 404, x0 + 28 + (x1 - x0 - 56) * p, 434], radius=8, fill=PASS_FG if ok else BLUE)
            if ok:
                draw_pill(draw, x0 + 28, 456, "PASS", PASS_FG, "#FFFFFF", min_h=40)

        draw_bottom_callout(draw, "ขั้นตอน 2: รัน Job 1 (lint) และ Job 2 (test-native) ขนานกัน", "รันตรวจสไตล์โค้ดและ Unit Test พร้อมกันเพื่อลดเวลาการรอผลให้เร็วที่สุด", PASS_FG if ok else BLUE)

    else:
        draw_cmd_bar(draw, 86, 128, 1194, "gh run list --workflow ci.yml  # Status: completed", 1.0, PASS_FG)
        draw_box_with_text(draw, 86, 206, 370, 310, "lint\nPASS", PASS_BG, PASS_FG, PASS_FG, F_MONO_B)
        draw_box_with_text(draw, 86, 330, 370, 434, "test-native\nPASS", PASS_BG, PASS_FG, PASS_FG, F_MONO_B)
        draw_pill(draw, 86, 460, "build-esp32  PASS!", PASS_FG, "#FFFFFF", font=F_BODY_B, min_h=44)

        draw_arrow(draw, 384, 258, 450, 340, PASS_FG, 1.0)
        draw_arrow(draw, 384, 382, 450, 355, PASS_FG, 1.0)

        draw_screenshot_card(img, draw, "gh-05-actions-graph.png", 465, 200, 1194, 545, "ผลลัพธ์จริง: GitHub Actions 3-Job CI Pipeline", PASS_FG)

        draw_bottom_callout(draw, "ขั้นตอน 3: ปลดล็อก build-esp32 สำเร็จ", "เมื่อ lint และ test-native ผ่าน จึงคอมไพล์ firmware.bin และขึ้นติ๊กเขียวบน PR", PASS_FG)


# ==============================================================================
# 06: GitHub Actions Release — 18s (4 scenes)
# ==============================================================================

def render_06(img: Image.Image, draw: ImageDraw.ImageDraw, t_raw: float) -> None:
    sc, st = split_scenes(t_raw, 4, 2.5, 18)
    draw_chrome(draw, "MODULE 06", "Release Tag & esptool merge-bin (4-in-1 Firmware)", "git tag v1.0.0 -> ตรวจ tags: ['v*.*.*'] -> esptool merge-bin -> GitHub Release", sc, 4, t_raw, 18)
    draw_focus_card(draw)

    if sc == 0:
        entered = draw_cmd_bar(draw, 86, 128, 1194, 'git tag -a v1.0.0 -m "release: v1.0.0"', st)
        p = ease_out_cubic(seg_t(st, 0.30, 0.80)) if entered else 0.0

        draw.line([(210, 430), (1050, 430)], fill=BLUE, width=5)
        draw_pill(draw, 96, 410, "main", BLUE_TINT, NAVY, BLUE, min_h=40)
        draw_commit_node(draw, 320, 430, 26, "C1", BLUE_SOFT, BLUE)
        draw_commit_node(draw, 580, 430, 26, "C2", BLUE_SOFT, BLUE)
        draw_commit_node(draw, 860, 430, 28, "C3", BLUE_TINT, NAVY)
        if p > 0.25:
            draw_pill(draw, 796, 295, "TAG: v1.0.0", NAVY, "#FFFFFF", font=F_BODY_B, min_h=44)
            draw_arrow(draw, 860, 344, 860, 396, NAVY, p)

        draw_bottom_callout(draw, "ขั้นตอน 1: ติดป้ายเวอร์ชัน v1.0.0 บน main", "สร้าง Annotated Tag v1.0.0 เพื่อระบุจุดปล่อยเวอร์ชันบน Commit ล่าสุดของ main", BLUE)

    elif sc == 1:
        entered = draw_cmd_bar(draw, 86, 128, 1194, "git push origin v1.0.0", st, PASS_FG if st > 0.65 else BLUE)
        p = ease_out_cubic(seg_t(st, 0.28, 0.80)) if entered else 0.0

        draw_box_with_text(draw, 96, 260, 430, 480, "Pattern Detector\n\ntags: ['v*.*.*']", BLUE_SOFT, BLUE, NAVY, F_HEAD, width=3)
        draw_arrow(draw, 445, 370, 580, 370, PASS_FG if p > 0.55 else BLUE, p)
        if p > 0.45:
            draw_sub_card(draw, 595, 250, 1194, 490, PASS_BG if p > 0.75 else SURFACE_ALT, PASS_FG if p > 0.75 else BLUE, width=3)
            draw_pill(draw, 628, 278, "MATCHED: v1.0.0", PASS_FG, "#FFFFFF", font=F_BODY_B, min_h=40)
            draw_text_vcenter_left(draw, 628, 344, 386, "TRIGGERED: .github/workflows/release.yml", F_MONO_B, PASS_FG)
            draw_text_vcenter_left(draw, 628, 400, 442, "กำลังเตรียม Build & Merge Firmware...", F_BODY, TEXT_SUB)

        draw_bottom_callout(draw, "ขั้นตอน 2: ด่าน tags: ['v*.*.*'] ตรวจพบรูปแบบตรงกัน", "เมื่อ Push Tag v1.0.0 ขึ้น GitHub ด่านตรวจจับสั่งเริ่มทำงาน release.yml ทันที", PASS_FG if p > 0.75 else BLUE)

    elif sc == 2:
        entered = draw_cmd_bar(draw, 86, 128, 1194, "esptool merge-bin -o merged-firmware.bin ...", st, PASS_FG if st > 0.80 else BLUE)
        p = ease_in_out_cubic(seg_t(st, 0.25, 0.82)) if entered else 0.0
        done = p > 0.85

        parts = [("0x1000", "bootloader.bin", 214), ("0x8000", "partitions.bin", 296), ("0xe000", "boot_app0.bin", 378), ("0x10000", "firmware.bin", 460)]
        for offset, name, py in parts:
            draw_sub_card(draw, 86, py, 470, py + 60, BLUE_SOFT, BLUE)
            draw_pill(draw, 102, py + 11, offset, BLUE_TINT, NAVY, font=F_MONO_B, pad_x=12, pad_y=6, min_h=38)
            draw_text_vcenter_left(draw, 232, py, py + 60, name, F_MONO_B, TEXT)
            draw_arrow(draw, 482, py + 30, 595, 368, PASS_FG if done else BLUE, p)

        draw_sub_card(draw, 610, 240, 1194, 495, PASS_BG if done else SURFACE_ALT, PASS_FG if done else NAVY, width=3)
        draw_pill(draw, 640, 266, "esptool merge-bin", NAVY, "#FFFFFF", min_h=38)
        draw_text_vcenter_left(draw, 640, 326, 368, "merged-firmware.bin (Offset 0x0)", F_MONO_LG, PASS_FG if done else NAVY)
        draw.rounded_rectangle([640, 384, 1160, 414], radius=8, fill=BLUE_TINT)
        draw.rounded_rectangle([640, 384, 640 + 520 * p, 414], radius=8, fill=PASS_FG if done else BLUE)
        if done:
            draw_pill(draw, 640, 434, "4-in-1 Binary Ready!", PASS_FG, "#FFFFFF", min_h=40)

        draw_bottom_callout(draw, "ขั้นตอน 3: รวม 4 ไฟล์เป็น merged-firmware.bin", "รวม bootloader + partitions + boot_app0 + firmware เป็นไฟล์เดียวสำหรับแฟลชที่ 0x0", PASS_FG if done else BLUE)

    else:
        draw_cmd_bar(draw, 86, 128, 1194, "gh release view v1.0.0  # Assets Published!", 1.0, PASS_FG)
        draw_sub_card(draw, 86, 204, 570, 545, SURFACE_ALT, BLUE, width=2)
        draw_pill(draw, 110, 224, "GitHub Release Assets", NAVY, "#FFFFFF", font=F_BODY_B, min_h=38)

        draw_sub_card(draw, 110, 286, 546, 390, "#FFFFFF", BORDER)
        draw_pill(draw, 128, 306, "OTA", BLUE_TINT, NAVY, min_h=36)
        draw_text_vcenter_left(draw, 212, 302, 342, "firmware.bin", F_MONO_B, TEXT)
        draw_text_vcenter_left(draw, 128, 348, 380, "สำหรับอัปเดตผ่าน Wi-Fi / OTA", F_SMALL, TEXT_SUB)

        draw_sub_card(draw, 110, 410, 546, 518, PASS_BG, PASS_FG)
        draw_pill(draw, 128, 430, "0x0", PASS_FG, "#FFFFFF", min_h=36)
        draw_text_vcenter_left(draw, 212, 426, 466, "merged-firmware.bin", F_MONO_B, PASS_FG)
        draw_text_vcenter_left(draw, 128, 472, 504, "สำหรับแฟลช 1-Click ที่ตำแหน่ง 0x0", F_SMALL_B, PASS_FG)

        draw_screenshot_card(img, draw, "gh-05-releases.png", 590, 204, 1194, 545, "ผลลัพธ์จริง: GitHub Release Assets", PASS_FG)

        draw_bottom_callout(draw, "ขั้นตอน 4: ออกหน้า GitHub Release v1.0.0 สำเร็จ", "ผู้ใช้ดาวน์โหลด firmware.bin (OTA) หรือ merged-firmware.bin (0x0) ไปใช้งานได้ทันที", PASS_FG)


SCENES: List[Tuple[str, int, Callable[[Image.Image, ImageDraw.ImageDraw, float], None]]] = [
    ("01-gitflow-branching.mp4", 15, render_01),
    ("02-pull-request-review.mp4", 16, render_02),
    ("03-pre-commit-hooks.mp4", 15, render_03),
    ("04-platformio-unit-testing.mp4", 15, render_04),
    ("05-github-actions-ci.mp4", 15, render_05),
    ("06-github-actions-release.mp4", 18, render_06),
]


def render_video(filename: str, duration_sec: int, renderer: Callable[[Image.Image, ImageDraw.ImageDraw, float], None], out_dir: Path) -> None:
    out_mp4 = out_dir / filename
    total_frames = FPS * duration_sec
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{WIDTH}x{HEIGHT}", "-r", str(FPS), "-i", "-",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "20",
        "-movflags", "+faststart", str(out_mp4),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    assert proc.stdin is not None
    try:
        for frame_idx in range(total_frames):
            t_raw = frame_idx / max(1, total_frames - 1)
            img = BASE_BG.copy()
            draw = ImageDraw.Draw(img)
            renderer(img, draw, t_raw)
            proc.stdin.write(img.tobytes())
        proc.stdin.close()
        if proc.wait() != 0:
            raise RuntimeError(f"ffmpeg failed for {filename}")
    finally:
        if proc.poll() is None:
            proc.kill()
    print(f"Generated ({FPS}fps, {duration_sec}s): {out_mp4}")


def main() -> int:
    if not shutil.which("ffmpeg"):
        print("Error: ffmpeg not found in PATH", file=sys.stderr)
        return 1
    out_dir = Path(__file__).resolve().parents[1]
    for filename, dur, renderer in SCENES:
        render_video(filename, dur, renderer, out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
