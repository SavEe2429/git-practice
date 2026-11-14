#!/usr/bin/env python3
"""
Generate 6 crisp 1280x720 MP4 walkthrough videos (Terminal + Flow Diagram)
using Pillow + FFmpeg.
"""

import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1280, 720
FPS = 12


def load_font(size: int, mono: bool = False) -> ImageFont.FreeTypeFont:
    candidates = (
        [
            r"C:\Windows\Fonts\consola.ttf",
            r"C:\Windows\Fonts\cour.ttf",
        ]
        if mono
        else [
            r"C:\Windows\Fonts\leelawui.ttf",
            r"C:\Windows\Fonts\tahoma.ttf",
            r"C:\Windows\Fonts\segoeui.ttf",
        ]
    )
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


FONT_TITLE = load_font(28)
FONT_SUB = load_font(18)
FONT_BODY = load_font(17)
FONT_MONO = load_font(18, mono=True)
FONT_SMALL = load_font(14)

SCENES = [
    {
        "filename": "01-gitflow-branching.mp4",
        "module": "MODULE 1",
        "title": "Linear History (Rebase) & Conventional Commits",
        "why": "Why: Keep main a clean single straight line with Rebase",
        "steps": ["1. Fork & Clone", "2. feature/* from main", "3. Conventional Commit", "4. Rebase onto main"],
        "lines": [
            ("$ git clone https://github.com/<you>/esp32-workshop.git", "#7dd3fc"),
            ("Cloning into 'esp32-workshop'...", "#94a3b8"),
            ("$ git checkout -b feature/fast-blink main", "#7dd3fc"),
            ("Switched to a new branch 'feature/fast-blink'", "#94a3b8"),
            ("$ git add -A && git commit -m \"feat(blink): add fast blink preset\"", "#7dd3fc"),
            ("[feature/fast-blink] feat(blink): add fast blink preset", "#86efac"),
            ("$ git fetch origin && git rebase origin/main", "#7dd3fc"),
            ("Successfully rebased and updated refs/heads/feature/fast-blink.", "#86efac"),
            ("$ python exercises/verify.py --module 1", "#7dd3fc"),
            ("  [PASS] Linear history & Conventional Commits", "#fde047"),
        ],
    },
    {
        "filename": "02-pull-request-review.mp4",
        "module": "MODULE 2",
        "title": "Issue Forms (.yml), Pull Request & Rebase Merge",
        "why": "Why: Structured YAML Issues + Linear History on main",
        "steps": ["1. Issue Form (.yml)", "2. Open PR -> main", "3. CI & Linear Check", "4. Rebase & Delete"],
        "lines": [
            ("$ git push -u origin feature/fast-blink", "#7dd3fc"),
            (" * [new branch] feature/fast-blink -> origin/feature/fast-blink", "#94a3b8"),
            ("$ gh pr create --base main --fill", "#7dd3fc"),
            ("Loaded .github/pull_request_template.md", "#fde047"),
            ("Created pull request #1: feat(blink): add fast blink preset", "#86efac"),
            ("Checking Require linear history & CI status checks...", "#94a3b8"),
            ("  [PASS] Peer Review: Approved", "#86efac"),
            ("  [PASS] CI / lint, unit-test, build-esp32", "#86efac"),
            ("$ gh pr merge 1 --rebase --delete-branch", "#7dd3fc"),
            ("Rebased & merged PR #1 into main (branch deleted)!", "#fde047"),
        ],
    },
    {
        "filename": "03-pre-commit-hooks.mp4",
        "module": "MODULE 3",
        "title": "Pre-commit Hooks (clang-format & Commit Lint)",
        "why": "Why: Catch formatting & bad commit messages in 1s locally",
        "steps": ["1. pre-commit install", "2. Bad commit blocked", "3. Auto clang-format", "4. Valid commit PASS"],
        "lines": [
            ("$ pre-commit install && pre-commit install --hook-type commit-msg", "#7dd3fc"),
            ("pre-commit installed at .git/hooks/pre-commit", "#94a3b8"),
            ("$ git commit -m \"update code\"", "#7dd3fc"),
            ("clang-format....................................Failed (auto-fixed)", "#fca5a5"),
            ("conventional-pre-commit.........................Failed", "#fca5a5"),
            ("  Error: Commit message must start with feat/fix/style/ci...", "#fca5a5"),
            ("$ git add src/main.cpp", "#7dd3fc"),
            ("$ git commit -m \"style: format main.cpp with clang-format\"", "#7dd3fc"),
            ("clang-format....................................Passed", "#86efac"),
            ("conventional-pre-commit.........................Passed", "#86efac"),
        ],
    },
    {
        "filename": "04-platformio-unit-testing.mp4",
        "module": "MODULE 4",
        "title": "PlatformIO Unit Testing (Native Unity + ESP32)",
        "why": "Why: Test pure C++ logic in seconds without physical hardware",
        "steps": ["1. lib/blink_math", "2. [env:native]", "3. pio test -e native", "4. Build ESP32"],
        "lines": [
            ("$ pio test -e native -v", "#7dd3fc"),
            ("Testing native:test_native ...", "#94a3b8"),
            ("test_main.cpp:25:test_add_numbers_positive      [PASSED]", "#86efac"),
            ("test_main.cpp:26:test_clamp_interval_bounds     [PASSED]", "#86efac"),
            ("test_main.cpp:27:test_next_led_state_toggles    [PASSED]", "#86efac"),
            ("test_main.cpp:28:test_calculate_cycle_ms        [PASSED]", "#86efac"),
            ("----------------------- 4 Tests 0 Failures -----------------------", "#fde047"),
            ("$ pio run -e esp32doit-devkit-v1", "#7dd3fc"),
            ("RAM: 6.7% | Flash: 22.2% | Built firmware.bin", "#94a3b8"),
            ("========================= [SUCCESS] ==============================", "#86efac"),
        ],
    },
    {
        "filename": "05-github-actions-ci.mp4",
        "module": "MODULE 5",
        "title": "GitHub Actions Continuous Integration (CI)",
        "why": "Why: Verify every PR on clean Ubuntu runner automatically",
        "steps": ["1. Trigger PR/Push", "2. Job: lint", "3. Job: unit-test", "4. Job: build-esp32"],
        "lines": [
            ("GitHub Actions: .github/workflows/ci.yml triggered by PR #2", "#fde047"),
            ("[Job 1/3: lint] Running pre-commit checks...", "#7dd3fc"),
            ("  -> trailing-whitespace, clang-format [PASS]", "#86efac"),
            ("[Job 2/3: unit-test] Restoring ~/.platformio cache...", "#7dd3fc"),
            ("  -> pio test -e native: 4/4 PASSED", "#86efac"),
            ("[Job 3/3: build-esp32] pio run -e esp32doit-devkit-v1", "#7dd3fc"),
            ("  -> Built firmware.bin, bootloader.bin, partitions.bin", "#86efac"),
            ("  -> (If release/*) Uploaded Artifact rc-firmware", "#94a3b8"),
            ("$ gh run list --workflow ci.yml --limit 1", "#7dd3fc"),
            ("completed   success   CI - Lint, Test & Build", "#86efac"),
        ],
    },
    {
        "filename": "06-github-actions-release.mp4",
        "module": "MODULE 6",
        "title": "Release Branch -> CI -> Rebase main -> Tag v*.*.*",
        "why": "Why: Verify release/v* via CI, keep main linear, then Tag",
        "steps": ["1. release/v1.0.0", "2. CI Green -> Rebase", "3. Tag v1.0.0 on main", "4. GitHub Release"],
        "lines": [
            ("$ git checkout -b release/v1.0.0 main && git push -u origin release/v1.0.0", "#7dd3fc"),
            ("CI triggered on release/v1.0.0 -> [PASS] (Artifact ready)", "#86efac"),
            ("$ gh pr create --base main --fill && gh pr merge --rebase --delete-branch", "#7dd3fc"),
            ("Rebased release/v1.0.0 into main & deleted branch!", "#94a3b8"),
            ("$ git checkout main && git pull origin main", "#7dd3fc"),
            ("$ git tag -a v1.0.0 -m \"release: v1.0.0\" && git push origin v1.0.0", "#7dd3fc"),
            ("GitHub Actions: release.yml running esptool merge_bin...", "#fde047"),
            ("  [Asset 1] esp32doit-v1.0.0-firmware.bin (OTA)", "#fde047"),
            ("  [Asset 2] esp32doit-v1.0.0-merged-firmware.bin (0x0 1-file)", "#fde047"),
            ("$ python exercises/verify.py --all  -->  ALL PASS!", "#86efac"),
        ],
    },
]


def draw_frame(scene: dict, active_step: int, visible_lines: int, total_lines: int) -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), "#0f172a")
    draw = ImageDraw.Draw(img)

    # Top Header Bar
    draw.rectangle([0, 0, WIDTH, 96], fill="#1e3a8a")
    draw.rounded_rectangle([32, 18, 165, 50], radius=6, fill="#0284c7")
    draw.text((46, 23), scene["module"], font=FONT_SUB, fill="#ffffff")
    draw.text((185, 16), scene["title"], font=FONT_TITLE, fill="#ffffff")
    draw.text((32, 60), scene["why"], font=FONT_SUB, fill="#bae6fd")

    # Flow Step Pipeline (4 boxes)
    box_w = 275
    gap = 28
    start_x = 40
    y_top = 122
    for idx, step_text in enumerate(scene["steps"]):
        x0 = start_x + idx * (box_w + gap)
        x1 = x0 + box_w
        is_active = idx == active_step
        is_done = idx < active_step
        fill_color = "#0284c7" if is_active else ("#166534" if is_done else "#1e293b")
        border_color = "#7dd3fc" if is_active else ("#4ade80" if is_done else "#475569")
        draw.rounded_rectangle([x0, y_top, x1, y_top + 64], radius=10, fill=fill_color, outline=border_color, width=3)
        draw.text((x0 + 18, y_top + 20), step_text, font=FONT_BODY, fill="#ffffff")
        if idx < 3:
            ax = x1 + 4
            draw.line([ax, y_top + 32, ax + gap - 8, y_top + 32], fill="#64748b", width=3)

    # Terminal Window
    tx0, ty0, tx1, ty1 = 40, 212, WIDTH - 40, HEIGHT - 48
    draw.rounded_rectangle([tx0, ty0, tx1, ty1], radius=12, fill="#020617", outline="#334155", width=2)
    draw.rectangle([tx0, ty0, tx1, ty0 + 34], fill="#1e293b")
    for i, col in enumerate(["#ef4444", "#eab308", "#22c55e"]):
        draw.ellipse([tx0 + 16 + i * 22, ty0 + 10, tx0 + 28 + i * 22, ty0 + 22], fill=col)
    draw.text((tx0 + 96, ty0 + 8), "bash — esp32-git-workshop", font=FONT_SMALL, fill="#cbd5e1")

    # Terminal Lines
    line_y = ty0 + 52
    for text, color in scene["lines"][:visible_lines]:
        draw.text((tx0 + 24, line_y), text, font=FONT_MONO, fill=color)
        line_y += 38

    # Progress Bar at bottom
    progress = visible_lines / max(1, total_lines)
    draw.rectangle([40, HEIGHT - 24, WIDTH - 40, HEIGHT - 16], fill="#1e293b")
    draw.rectangle([40, HEIGHT - 24, int(40 + (WIDTH - 80) * progress), HEIGHT - 16], fill="#38bdf8")

    return img


def render_scene(scene: dict, out_dir: Path, tmp_dir: Path) -> None:
    scene_tmp = tmp_dir / scene["filename"].replace(".mp4", "")
    if scene_tmp.exists():
        shutil.rmtree(scene_tmp)
    scene_tmp.mkdir(parents=True, exist_ok=True)

    lines = scene["lines"]
    total_lines = len(lines)
    frame_idx = 0

    # Hold intro frame
    intro = draw_frame(scene, 0, 1, total_lines)
    for _ in range(FPS):
        intro.save(scene_tmp / f"frame_{frame_idx:04d}.png")
        frame_idx += 1

    # Reveal each line smoothly
    for count in range(1, total_lines + 1):
        step = min(3, int((count - 1) * 4 / total_lines))
        frame = draw_frame(scene, step, count, total_lines)
        hold_frames = FPS * 2 if count == total_lines else int(FPS * 1.4)
        for _ in range(hold_frames):
            frame.save(scene_tmp / f"frame_{frame_idx:04d}.png")
            frame_idx += 1

    out_mp4 = out_dir / scene["filename"]
    cmd = [
        "ffmpeg",
        "-y",
        "-framerate", str(FPS),
        "-i", str(scene_tmp / "frame_%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(out_mp4),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    shutil.rmtree(scene_tmp)
    print(f"Generated: {out_mp4}")


def main() -> int:
    if not shutil.which("ffmpeg"):
        print("Error: ffmpeg not found in PATH", file=sys.stderr)
        return 1
    out_dir = Path(__file__).resolve().parent
    tmp_dir = out_dir / "_tmp_frames"
    tmp_dir.mkdir(exist_ok=True)
    for scene in SCENES:
        render_scene(scene, out_dir, tmp_dir)
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
