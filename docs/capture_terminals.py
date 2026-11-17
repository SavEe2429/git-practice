#!/usr/bin/env python3
"""Capture real local command outputs into crisp terminal PNGs with proper Thai font shaping."""

import html
import os
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "images"
OUT.mkdir(parents=True, exist_ok=True)


def line_color(idx: int, line: str) -> str:
    if idx == 0:
        return "#7dd3fc"
    if any(tok in line for tok in ("Passed", "[PASS]", "[OK]", "SUCCESS", "พร้อมเข้าเรียน")):
        return "#86efac"
    if "[WARN]" in line or "Skipped" in line:
        return "#fde047"
    if "[FAIL]" in line or "MISSING" in line or "Failed" in line:
        return "#fca5a5"
    return "#e2e8f0"


def render_html_terminal(browser, title: str, lines: list[str], out_name: str) -> None:
    rows = []
    for idx, line in enumerate(lines):
        col = line_color(idx, line)
        rows.append(f'<div class="line" style="color:{col}">{html.escape(line) or "&nbsp;"}</div>')
    body_html = "\n".join(rows)

    doc_html = f"""<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8" />
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: #0f172a;
      width: 960px;
      font-family: "Consolas", "Leelawadee UI", "Tahoma", monospace;
    }}
    .titlebar {{
      height: 36px;
      background: #1e293b;
      display: flex;
      align-items: center;
      padding: 0 14px;
      gap: 8px;
      border-bottom: 1px solid #334155;
    }}
    .dot {{ width: 12px; height: 12px; border-radius: 50%; display: inline-block; }}
    .title {{
      margin-left: 12px;
      color: #cbd5e1;
      font-size: 13px;
      font-family: "Consolas", "Leelawadee UI", sans-serif;
    }}
    .screen {{
      padding: 16px 20px 20px 20px;
      font-size: 14.5px;
      line-height: 1.55;
      white-space: pre-wrap;
      word-break: break-word;
    }}
    .line {{ min-height: 22px; }}
  </style>
</head>
<body>
  <div class="titlebar">
    <span class="dot" style="background:#ef4444"></span>
    <span class="dot" style="background:#eab308"></span>
    <span class="dot" style="background:#22c55e"></span>
    <span class="title">{html.escape(title)}</span>
  </div>
  <div class="screen">{body_html}</div>
</body>
</html>"""

    page = browser.new_page(viewport={"width": 960, "height": 400}, device_scale_factor=1.5)
    page.set_content(doc_html)
    height = page.evaluate("() => Math.ceil(document.body.scrollHeight)")
    page.set_viewport_size({"width": 960, "height": max(210, height)})
    page.screenshot(path=str(OUT / out_name), full_page=True)
    page.close()
    print(f"Saved {OUT / out_name}")


def run_and_render(
    browser,
    title: str,
    cmd_display: str,
    cmd: list[str],
    out_name: str,
    env_extra: dict | None = None,
    max_lines: int = 38,
) -> None:
    env = os.environ.copy()
    if env_extra:
        env.update(env_extra)
    p = subprocess.run(
        cmd,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        timeout=120,
    )
    raw = (p.stdout or "") + (("\n" + p.stderr) if p.stderr else "")
    lines = [f"$ {cmd_display}"] + [l[:220] for l in raw.strip().splitlines()[:max_lines]]
    render_html_terminal(browser, title, lines, out_name)


def main() -> None:
    pio = str(Path.home() / ".platformio" / "penv" / "Scripts" / "pio.exe")
    local_tmp = str(Path.home() / "AppData" / "Local" / "Temp")
    args = os.sys.argv[1:]
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel="msedge")
        try:
            if not args or "env" in args:
                run_and_render(browser, "Pre-Workshop Check (check_env.py)", "uv run exercises/check_env.py", ["uv", "run", "exercises/check_env.py"], "term-00-check-env.png", {"TEMP": local_tmp, "TMP": local_tmp})
            if not args or "git" in args:
                run_and_render(browser, "git log --graph --oneline --decorate (SavEe2429/git-practice)", "git log --graph --oneline --decorate -n 6", ["git", "log", "--graph", "--oneline", "--decorate", "-n", "6"], "term-01-git-log.png")
            if not args or "precommit" in args:
                run_and_render(browser, "pre-commit run --all-files", "pre-commit run --all-files", ["pre-commit", "run", "--all-files"], "term-02-pre-commit.png")
            if not args or "pio" in args:
                run_and_render(browser, "PlatformIO Build (esp32doit-devkit-v1)", "pio run -d workshop -e esp32doit-devkit-v1", [pio, "run", "-d", "workshop", "-e", "esp32doit-devkit-v1"], "term-03-pio-build.png", {"TEMP": local_tmp, "TMP": local_tmp})
            if not args or "verify" in args:
                run_and_render(browser, "Workshop Self-Check (verify.py)", "uv run exercises/verify.py --all", ["uv", "run", "exercises/verify.py", "--all"], "term-04-verify.png", max_lines=45)
        finally:
            browser.close()


if __name__ == "__main__":
    main()
