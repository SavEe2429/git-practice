#!/usr/bin/env python3
"""Capture real local command outputs into crisp terminal PNGs for the PDF manual."""

import os
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "images"
OUT.mkdir(parents=True, exist_ok=True)

FONT = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 15)
FONT_SM = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 13)


def run_and_render(title: str, cmd_display: str, cmd: list[str], out_name: str, env_extra: dict | None = None) -> None:
    env = os.environ.copy()
    if env_extra:
        env.update(env_extra)
    p = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, timeout=120)
    raw = (p.stdout or "") + (("\n" + p.stderr) if p.stderr else "")
    lines = [f"$ {cmd_display}"] + [l[:105] for l in raw.strip().splitlines()[:22]]

    w = 960
    h = max(210, 58 + len(lines) * 22 + 18)
    img = Image.new("RGB", (w, h), "#0f172a")
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, 34], fill="#1e293b")
    for i, c in enumerate(["#ef4444", "#eab308", "#22c55e"]):
        d.ellipse([14 + i * 20, 10, 26 + i * 20, 22], fill=c)
    d.text((86, 9), title, font=FONT_SM, fill="#cbd5e1")

    y = 48
    for idx, line in enumerate(lines):
        col = "#7dd3fc" if idx == 0 else ("#86efac" if ("Passed" in line or "PASS" in line or "SUCCESS" in line) else ("#fca5a5" if "FAIL" in line else "#e2e8f0"))
        d.text((18, y), line, font=FONT, fill=col)
        y += 22

    img.save(OUT / out_name)
    print(f"Saved {OUT / out_name}")


def main() -> None:
    pio = str(Path.home() / ".platformio" / "penv" / "Scripts" / "pio.exe")
    local_tmp = str(Path.home() / "AppData" / "Local" / "Temp")
    run_and_render("git log --graph --oneline (SavEe2429/git-practice)", "git log --graph --oneline -n 6", ["git", "log", "--graph", "--oneline", "-n", "6"], "term-01-git-log.png")
    run_and_render("pre-commit run --all-files", "pre-commit run --all-files", ["pre-commit", "run", "--all-files"], "term-02-pre-commit.png")
    run_and_render("PlatformIO Build (esp32doit-devkit-v1)", "pio run -d workshop -e esp32doit-devkit-v1", [pio, "run", "-d", "workshop", "-e", "esp32doit-devkit-v1"], "term-03-pio-build.png", {"TEMP": local_tmp, "TMP": local_tmp})
    run_and_render("Workshop Self-Check (verify.py)", "uv run exercises/verify.py --all", ["uv", "run", "exercises/verify.py", "--all"], "term-04-verify.png")


if __name__ == "__main__":
    main()
