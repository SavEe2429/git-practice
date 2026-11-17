#!/usr/bin/env python3
"""
Draw clean numbered red callout boxes and step arrows onto real GitHub/VS Code
screenshots into docs/images/anno-*.png for LAB01-LAB06 manuals.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

IMG_DIR = Path(__file__).resolve().parents[1] / "images"

RED = "#DC2626"
RED_FILL = "#991B1B"
WHITE = "#FFFFFF"


def get_font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    candidates = (
        [r"C:\Windows\Fonts\leelauib.ttf", r"C:\Windows\Fonts\tahomabd.ttf", r"C:\Windows\Fonts\arialbd.ttf"]
        if bold
        else [r"C:\Windows\Fonts\leelawui.ttf", r"C:\Windows\Fonts\tahoma.ttf", r"C:\Windows\Fonts\arial.ttf"]
    )
    for c in candidates:
        if Path(c).exists():
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()


def draw_callout(
    draw: ImageDraw.ImageDraw,
    img_w: int,
    img_h: int,
    box: tuple[int, int, int, int],
    num: int,
    label: str,
    label_pos: str = "bottom",
    scale: float = 1.0,
) -> None:
    x1, y1, x2, y2 = box
    lw = max(3, int(3.5 * scale))
    # Outer white halo + red box
    draw.rectangle([x1 - 2, y1 - 2, x2 + 2, y2 + 2], outline=WHITE, width=lw + 2)
    draw.rectangle([x1, y1, x2, y2], outline=RED, width=lw)

    font = get_font(max(15, int(16 * scale)), bold=True)
    badge_r = max(13, int(14 * scale))
    # Number badge at top-left corner of box (clean number only — no text pill inside image)
    bx, by = x1 - badge_r // 2, y1 - badge_r // 2
    bx = max(badge_r + 2, min(img_w - badge_r - 2, bx))
    by = max(badge_r + 2, min(img_h - badge_r - 2, by))
    draw.ellipse([bx - badge_r, by - badge_r, bx + badge_r, by + badge_r], fill=RED_FILL, outline=WHITE, width=max(2, int(2 * scale)))
    nbbox = draw.textbbox((0, 0), str(num), font=font)
    nw, nh = nbbox[2] - nbbox[0], nbbox[3] - nbbox[1]
    draw.text((bx - nw / 2, by - nh / 2 - int(2 * scale)), str(num), font=font, fill=WHITE)


def annotate(src_name: str, out_name: str, items: list[dict]) -> None:
    im = Image.open(IMG_DIR / src_name).convert("RGB")
    w, h = im.size
    scale = max(1.0, w / 1024.0)
    draw = ImageDraw.Draw(im)
    for it in items:
        draw_callout(
            draw,
            w,
            h,
            it["box"],
            it["num"],
            it["label"],
            it.get("pos", "bottom"),
            scale=scale,
        )
    im.save(IMG_DIR / out_name)
    print(f"Saved docs/images/{out_name} ({w}x{h})")


def main() -> None:
    # 1. LAB 01: Fork & Clone
    annotate(
        "gh-01-repo-fork.png",
        "anno-01-repo-fork.png",
        [
            {"num": 1, "box": (844, 150, 916, 180), "label": "กด Fork ไป Account ตัวเอง", "pos": "left"},
            {"num": 2, "box": (646, 204, 734, 234), "label": "หลัง Fork กด <> Code เพื่อ Copy URL", "pos": "bottom"},
        ],
    )

    # 2. LAB 02: Issues tab -> New issue
    annotate(
        "gh-02-issues.png",
        "anno-02-issues.png",
        [
            {"num": 1, "box": (74, 104, 152, 142), "label": "เข้าแท็บ Issues บน Fork", "pos": "bottom"},
            {"num": 2, "box": (916, 152, 996, 184), "label": "กดปุ่ม New issue เลือก YAML Form", "pos": "left"},
        ],
    )

    # 3. LAB 02: Issue Detail result
    annotate(
        "gh-02-issue-detail.png",
        "anno-02-issue-detail.png",
        [
            {"num": 1, "box": (44, 385, 1690, 545), "label": "จำหมายเลข Issue (เช่น #2 หรือ #1) เพื่อนำไปใส่ Closes #<เลข> ใน PR", "pos": "top"},
            {"num": 2, "box": (1760, 820, 1930, 940), "label": "Labels ถูกติดให้อัตโนมัติจาก YAML Form", "pos": "left"},
        ],
    )

    # 4. LAB 02: Pull requests tab -> New pull request
    annotate(
        "gh-03-pulls.png",
        "anno-02-pulls.png",
        [
            {"num": 1, "box": (276, 196, 458, 254), "label": "เข้าแท็บ Pull requests", "pos": "bottom"},
            {"num": 2, "box": (1678, 286, 1886, 342), "label": "กด New pull request เพื่อเปิด PR", "pos": "left"},
        ],
    )

    # 5. LAB 02: Compare & Create PR
    annotate(
        "gh-03-compare.png",
        "anno-02-compare.png",
        [
            {"num": 1, "box": (154, 556, 636, 622), "label": "เลือก base: main <- compare: feature/...", "pos": "bottom"},
            {"num": 2, "box": (1988, 714, 2312, 784), "label": "ใส่ Closes #<เลข> แล้วกด Create pull request", "pos": "left"},
        ],
    )

    # 6. LAB 02: PR Merged result
    annotate(
        "gh-03-pr-detail.png",
        "anno-02-pr-detail.png",
        [
            {"num": 1, "box": (500, 432, 670, 498), "label": "ตรวจผล Checks (ต้องผ่านสีเขียวก่อน Merge)", "pos": "bottom"},
            {"num": 2, "box": (46, 360, 196, 412), "label": "เลือก Rebase and merge จนสถานะขึ้น Merged", "pos": "right"},
        ],
    )

    # 7. LAB 02: VS Code Extension
    annotate(
        "vscode-pr-ext.png",
        "anno-02-vscode-pr.png",
        [
            {"num": 1, "box": (384, 462, 632, 536), "label": "กด Install (หรือค้นหา GitHub Pull Requests ใน VS Code)", "pos": "right"},
        ],
    )

    # 8. LAB 05: Actions list -> click workflow run
    annotate(
        "gh-04-actions-list.png",
        "anno-05-actions-list.png",
        [
            {"num": 1, "box": (12, 132, 152, 162), "label": "เลือกดู Workflow: CI - Lint, Test & Build", "pos": "right"},
            {"num": 2, "box": (274, 210, 610, 268), "label": "คลิกชื่อ Commit/Run เพื่อดูกราฟ 3 Jobs", "pos": "right"},
        ],
    )

    # 9. LAB 05: Actions 3-job graph result
    annotate(
        "gh-05-actions-graph.png",
        "anno-05-actions-graph.png",
        [
            {"num": 1, "box": (302, 384, 486, 426), "label": "คลิก Job นี้เพื่อดู Log Pre-commit", "pos": "top"},
            {"num": 2, "box": (518, 384, 708, 426), "label": "คลิกดูผล Unity Test", "pos": "bottom"},
            {"num": 3, "box": (738, 384, 928, 426), "label": "คลิกดูผล Build ESP32", "pos": "top"},
        ],
    )

    # 10. LAB 06: Releases assets download
    annotate(
        "gh-05-releases.png",
        "anno-06-releases.png",
        [
            {"num": 1, "box": (68, 1176, 248, 1224), "label": "เปิดดูรายการไฟล์ Assets ของ Tag เวอร์ชัน", "pos": "right"},
            {"num": 2, "box": (126, 1322, 610, 1366), "label": "คลิกโหลดไฟล์ *-merged-firmware.bin เพื่อนำไป Flash ที่ 0x0", "pos": "right"},
        ],
    )


if __name__ == "__main__":
    main()
