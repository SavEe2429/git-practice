import html
from pathlib import Path
import subprocess
from playwright.sync_api import sync_playwright

PRES_DIR = Path(r"c:\Users\nongs\Desktop\git_practice\presentation")
IMG_DIR = PRES_DIR / "img"
HTML_DIR = Path(r"C:\Users\nongs\.gemini\antigravity\brain\42179393-0e9b-47fe-bcaa-9120998435a1\scratch\diagrams_v2")
IMG_DIR.mkdir(parents=True, exist_ok=True)
HTML_DIR.mkdir(parents=True, exist_ok=True)

SELF_CHECK = Path(r"C:\ThClaws\ohters\Phew\.thclaws\plugins\diagram-design\skills\diagram-design\scripts\self_check.py")

HEAD_TEMPLATE = """<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=Geist+Mono:wght@400;500;600;700&family=Sarabun:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'Sarabun', 'Geist', sans-serif; background: #ffffff; margin: 0; padding: 0; }}
    svg {{ display: block; }}
  </style>
</head>
<body>
{svg}
</body>
</html>
"""

# Minimalist Unified Navy-Slate Tokens (Zero messy patchy colors, Edge-to-Edge Container!):
#   Outer Canvas = #F8FAFC fill with #E2E8F0 1.4px stroke (single outer border — NO double box!)
#   Default Node = #FFFFFF fill with #CBD5E1 1.4px stroke
#   Focal Node   = #EEF5FA fill with #1F5F8B 1.8px stroke
#   Badge Chip   = #1F5F8B or #EEF5FA (consistent across slides)
#   Ink          = #12306E (Primary) / #475569 (Secondary)

DEFS = """  <defs>
    <marker id="arr" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#64748B"/>
    </marker>
    <marker id="arr-navy" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#1F5F8B"/>
    </marker>
  </defs>"""


def esc(s: str) -> str:
    return html.escape(str(s), quote=False)


def wrap(sid, w, h, title, desc, inner, bg="#F8FAFC", border="#CBD5E1"):
    """Full-bleed diagram framed cleanly by a single edge-to-edge rounded surface (no outer Pic padding!)."""
    return f"""<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="{sid}-t {sid}-d">
  <title id="{sid}-t">{esc(title)}</title>
  <desc id="{sid}-d">{esc(desc)}</desc>
{DEFS}
  <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="{bg}" stroke="{border}" stroke-width="1.5"/>
{inner}
</svg>"""


def node(x, y, w, h, title, sub="", focal=False, mono_t=False, mono_s=True, t_sz=17, s_sz=13):
    fill = "#EEF5FA" if focal else "#FFFFFF"
    stroke = "#1F5F8B" if focal else "#CBD5E1"
    sw = "1.8" if focal else "1.3"
    tcol = "#12306E" if focal else "#0F172A"
    scol = "#1F5F8B" if focal else "#64748B"
    tf = "'Geist Mono', monospace" if mono_t else "'Sarabun', sans-serif"
    sf = "'Geist Mono', monospace" if mono_s else "'Sarabun', sans-serif"
    cx = x + w / 2
    if sub:
        ty = y + h * 0.44
        sy = y + h * 0.76
        sub_el = f'\n  <text x="{cx}" y="{sy:.1f}" fill="{scol}" font-size="{s_sz}" font-weight="600" font-family="{sf}" text-anchor="middle">{esc(sub)}</text>'
    else:
        ty = y + h * 0.56
        sub_el = ""
    return f"""  <rect class="fit-box" x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>
  <text x="{cx}" y="{ty:.1f}" fill="{tcol}" font-size="{t_sz}" font-weight="700" font-family="{tf}" text-anchor="middle">{esc(title)}</text>{sub_el}"""


def chip(x, y, text, w=108):
    return f"""  <rect x="{x}" y="{y}" width="{w}" height="24" rx="12" fill="#EEF5FA" stroke="#CBD5E1" stroke-width="1"/>
  <text x="{x + w/2:.1f}" y="{y + 16}" fill="#1F5F8B" font-size="11.5" font-weight="700" font-family="'Geist Mono', 'Sarabun', sans-serif" text-anchor="middle">{esc(text)}</text>"""


def term_shell(w, h, cmd, lines):
    """Minimalist Light/Dark-Slate terminal visual matching unified Navy-Slate skin."""
    rows = []
    for idx, (txt, status) in enumerate(lines):
        ly = 92 + idx * 34
        if status == "PASS":
            badge = f'<rect x="{w-96}" y="{ly-16}" width="72" height="22" rx="11" fill="#EEF5FA" stroke="#1F5F8B" stroke-width="1"/><text x="{w-60}" y="{ly-1}" fill="#1F5F8B" font-size="11.5" font-weight="700" font-family="\'Geist Mono\', monospace" text-anchor="middle">PASSED</text>'
        elif status == "INFO":
            badge = f'<rect x="{w-96}" y="{ly-16}" width="72" height="22" rx="11" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="1"/><text x="{w-60}" y="{ly-1}" fill="#475569" font-size="11.5" font-weight="700" font-family="\'Geist Mono\', monospace" text-anchor="middle">DONE</text>'
        else:
            badge = ""
        rows.append(f'  <text x="28" y="{ly}" fill="#1E293B" font-size="13.5" font-weight="600" font-family="\'Geist Mono\', \'Sarabun\', monospace">{esc(txt)}</text>\n  {badge}')
    return f"""  <rect x="1" y="1" width="{w-2}" height="40" rx="10" fill="#EEF5FA"/>
  <rect x="1" y="30" width="{w-2}" height="12" fill="#EEF5FA"/>
  <line x1="1" y1="42" x2="{w-1}" y2="42" stroke="#CBD5E1" stroke-width="1.2"/>
  <circle cx="24" cy="21" r="5" fill="#94A3B8"/>
  <circle cx="42" cy="21" r="5" fill="#CBD5E1"/>
  <circle cx="60" cy="21" r="5" fill="#CBD5E1"/>
  <text x="82" y="26" fill="#12306E" font-size="13.5" font-weight="700" font-family="'Geist Mono', monospace">$ {esc(cmd)}</text>
""" + "\n".join(rows)


DIAGRAMS = {}

# ==============================================================================
# SECTION 01: s02, s03, s04, s05
# ==============================================================================

# s02 (Type A — 872x252): 4-Station Firmware Delivery Pipeline
DIAGRAMS["s02"] = (872, 252, "Enterprise Firmware Delivery Pipeline", wrap(
    "s02", 872, 252,
    "Enterprise ESP32 Firmware Delivery Pipeline",
    "Four-station horizontal pipeline from Feature Branch to Local Gate, Cloud CI, and Merged Binary.",
    """  <line x1="212" y1="142" x2="234" y2="142" stroke="#64748B" stroke-width="2.2" marker-end="url(#arr)"/>
  <line x1="424" y1="142" x2="446" y2="142" stroke="#64748B" stroke-width="2.2" marker-end="url(#arr)"/>
  <line x1="636" y1="142" x2="658" y2="142" stroke="#1F5F8B" stroke-width="2.4" marker-end="url(#arr-navy)"/>
""" +
    chip(64, 34, "STATION 01") +
    chip(276, 34, "STATION 02") +
    chip(488, 34, "STATION 03") +
    chip(700, 34, "STATION 04") +
    node(24, 78, 188, 128, "Issue & Branch", "feature/*", t_sz=18, s_sz=14) +
    node(236, 78, 188, 128, "Local Gate", "Pre-commit (2s)", t_sz=18, s_sz=14) +
    node(448, 78, 188, 128, "Cloud CI & PR", "Test + Build", focal=True, t_sz=18, s_sz=14) +
    node(660, 78, 188, 128, "Release .bin", "Tag -> Flash 0x0", focal=True, t_sz=18, s_sz=14)
))

# s03 (Type A — 872x252): 4 Organizational Roles Flow
DIAGRAMS["s03"] = (872, 252, "Four Organizational Roles", wrap(
    "s03", 872, 252,
    "Four Organizational Roles Collaborating",
    "Clean 4-column role interaction from Developer to QA/CI, Tech Lead, and Production.",
    """  <line x1="212" y1="142" x2="234" y2="142" stroke="#64748B" stroke-width="2.2" marker-end="url(#arr)"/>
  <line x1="424" y1="142" x2="446" y2="142" stroke="#1F5F8B" stroke-width="2.2" marker-end="url(#arr-navy)"/>
  <line x1="636" y1="142" x2="658" y2="142" stroke="#1F5F8B" stroke-width="2.2" marker-end="url(#arr-navy)"/>
""" +
    chip(54, 34, "ROLE 01", 128) +
    chip(266, 34, "ROLE 02", 128) +
    chip(478, 34, "ROLE 03", 128) +
    chip(690, 34, "ROLE 04", 128) +
    node(24, 78, 188, 128, "Firmware Dev", "Code, Unit Test & เปิด PR", mono_s=False, t_sz=18, s_sz=13.5) +
    node(236, 78, 188, 128, "DevOps / CI System", "Pipeline ตรวจอัตโนมัติ", focal=True, mono_s=False, t_sz=17, s_sz=13.5) +
    node(448, 78, 188, 128, "Tech Lead & QA", "Review & เทส Hardware", mono_s=False, t_sz=18, s_sz=13.5) +
    node(660, 78, 188, 128, "Production", "ดึงไฟล์ 0x0 ไป Flash", focal=True, mono_s=False, t_sz=18, s_sz=13.5)
))

# s04 (Type A — 872x252): Shift-Left Quality Speed vs Cost Comparison
DIAGRAMS["s04"] = (872, 252, "Shift-Left Detection Speed", wrap(
    "s04", 872, 252,
    "Shift-Left Early Bug Detection",
    "Horizontal bar chart comparing detection speed and cost across Local Gate, Cloud CI, and Field Failure.",
    """  <text x="36" y="54" fill="#12306E" font-size="16" font-weight="700">1. Local Gate (Pre-commit + Native Test)</text>
  <rect x="380" y="34" width="116" height="32" rx="8" fill="#1F5F8B"/>
  <text x="438" y="55" fill="#FFFFFF" font-size="14" font-weight="700" font-family="'Geist Mono', monospace" text-anchor="middle">2 วินาที</text>
  <text x="514" y="55" fill="#1F5F8B" font-size="15" font-weight="700">แก้ได้ทันที · Cost ต่ำสุด</text>

  <line x1="32" y1="88" x2="840" y2="88" stroke="#E2E8F0" stroke-width="1.2"/>

  <text x="36" y="130" fill="#12306E" font-size="16" font-weight="700">2. Cloud CI Gate (GitHub Actions CI)</text>
  <rect x="380" y="110" width="212" height="32" rx="8" fill="#EEF5FA" stroke="#1F5F8B" stroke-width="1.5"/>
  <text x="486" y="131" fill="#12306E" font-size="14" font-weight="700" font-family="'Geist Mono', monospace" text-anchor="middle">1–2 นาที</text>
  <text x="610" y="131" fill="#475569" font-size="15" font-weight="600">กันโค้ดพังเข้า Branch main</text>

  <line x1="32" y1="164" x2="840" y2="164" stroke="#E2E8F0" stroke-width="1.2"/>

  <text x="36" y="206" fill="#475569" font-size="16" font-weight="700">3. หลุดไปหน้างาน (ไม่มี Gate ตรวจ)</text>
  <rect x="380" y="186" width="448" height="32" rx="8" fill="#E2E8F0"/>
  <text x="604" y="207" fill="#334155" font-size="14" font-weight="700" font-family="'Geist Mono', monospace" text-anchor="middle">หลายวัน / สัปดาห์ · Re-flash บอร์ดหน้างานทั้งหมด</text>
"""
))

# s05 (Type B — 476x296): 3-Layer Quality Funnel
DIAGRAMS["s05"] = (476, 296, "Three-Layer Quality Gate Architecture", wrap(
    "s05", 476, 296,
    "Three-Layer Quality Gate Funnel",
    "Stacked three-gate funnel showing Local Gate, Cloud CI, and Release Delivery.",
    """  <line x1="238" y1="96"  x2="238" y2="114" stroke="#64748B" stroke-width="2" marker-end="url(#arr)"/>
  <line x1="238" y1="186" x2="238" y2="204" stroke="#1F5F8B" stroke-width="2" marker-end="url(#arr-navy)"/>
""" +
    node(28, 24, 420, 72, "Layer 1: Local Gate", "Pre-commit Format + Commit Rule (< 3s)", t_sz=16, s_sz=12.5) +
    node(58, 114, 360, 72, "Layer 2: Cloud CI Gate", "Unity Native Test + ESP32 Build (~2m)", focal=True, t_sz=16, s_sz=12.5) +
    node(88, 204, 300, 72, "Layer 3: Release Gate", "Tag v* -> merge-bin (0x0)", focal=True, t_sz=16, s_sz=12.5)
))

# ==============================================================================
# SECTION 02 (LAB 01): s06, s07, s08, s09, s10
# ==============================================================================

# s06 (Type A — 872x252): Internal Team Shared Repo + Parallel Feature Branches
DIAGRAMS["s06"] = (872, 252, "Shared Repo Parallel Feature Branches", wrap(
    "s06", 872, 252,
    "Shared Repo with Parallel Feature Branches",
    "Locked main branch with parallel feature and fix branches merging cleanly via Pull Requests.",
    """  <text x="32" y="66" fill="#12306E" font-size="15" font-weight="700" font-family="'Geist Mono', monospace">main (Locked)</text>
  <line x1="172" y1="62" x2="824" y2="62" stroke="#12306E" stroke-width="3"/>
  <circle cx="216" cy="62" r="8" fill="#FFFFFF" stroke="#12306E" stroke-width="2.5"/>
  <circle cx="536" cy="62" r="9" fill="#EEF5FA" stroke="#1F5F8B" stroke-width="2.5"/>
  <circle cx="776" cy="62" r="9" fill="#EEF5FA" stroke="#1F5F8B" stroke-width="2.5"/>
  <text x="536" y="38" fill="#1F5F8B" font-size="13" font-weight="700" text-anchor="middle">PR #1 Merged</text>
  <text x="776" y="38" fill="#1F5F8B" font-size="13" font-weight="700" text-anchor="middle">PR #2 Merged</text>

  <path d="M 216,70 Q 216,132 268,132 H 484 Q 536,132 536,75" fill="none" stroke="#1F5F8B" stroke-width="2.4" marker-end="url(#arr-navy)"/>
  <rect x="272" y="112" width="196" height="36" rx="18" fill="#FFFFFF" stroke="#1F5F8B" stroke-width="1.6"/>
  <text x="370" y="135" fill="#1F5F8B" font-size="14" font-weight="700" font-family="'Geist Mono', monospace" text-anchor="middle">Dev A: feature/blink</text>

  <path d="M 216,70 Q 216,202 284,202 H 724 Q 776,202 776,75" fill="none" stroke="#64748B" stroke-width="2.2" marker-end="url(#arr)"/>
  <rect x="468" y="182" width="204" height="36" rx="18" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1.5"/>
  <text x="570" y="205" fill="#334155" font-size="14" font-weight="700" font-family="'Geist Mono', monospace" text-anchor="middle">Dev B: fix/watchdog</text>
"""
))

# s07 (Type A — 872x252): Shared Branch vs Fork Workflow Decision
DIAGRAMS["s07"] = (872, 252, "When to Use Shared Repo vs Fork", wrap(
    "s07", 872, 252,
    "Comparing Shared Repository vs Fork Workflow",
    "Decision visual showing internal company teams using Shared Branches vs external contributors and students using Forks.",
    """  <line x1="274" y1="68"  x2="314" y2="68"  stroke="#64748B" stroke-width="2" marker-end="url(#arr)"/>
  <line x1="576" y1="68"  x2="616" y2="68"  stroke="#1F5F8B" stroke-width="2" marker-end="url(#arr-navy)"/>
  <line x1="274" y1="184" x2="314" y2="184" stroke="#64748B" stroke-width="2" marker-end="url(#arr)"/>
  <line x1="576" y1="184" x2="616" y2="184" stroke="#1F5F8B" stroke-width="2" marker-end="url(#arr-navy)"/>
""" +
    node(28, 32, 244, 74, "ทีมภายในองค์กร", "มีสิทธิ์ Write ใน Shared Repo", mono_s=False, t_sz=17, s_sz=13) +
    node(318, 32, 256, 74, "แตก Feature Branch", "feature/* ใน Shared Repo", t_sz=17, s_sz=13) +
    node(620, 32, 224, 74, "ไม่ต้อง Fork", "สะดวกและเร็วกว่า", focal=True, mono_s=False, t_sz=17, s_sz=13) +
    node(28, 146, 244, 74, "External / ห้องเรียน", "ไม่มีสิทธิ์แก้ Main Repo", mono_s=False, t_sz=16.5, s_sz=13) +
    node(318, 146, 256, 74, "กด Fork สำเนาแยก", "ได้สิทธิ์ Admin ใน Fork ตัวเอง", mono_s=False, t_sz=17, s_sz=13) +
    node(620, 146, 224, 74, "ส่ง PR ข้าม Repo", "ปลอดภัยต่อ Main Repo", focal=True, mono_s=False, t_sz=17, s_sz=13)
))

# s08 (Type A — 872x252): Tangled Merge vs Linear Rebase Visual
DIAGRAMS["s08"] = (872, 252, "Tangled Merge vs Linear Rebase", wrap(
    "s08", 872, 252,
    "Linear Git History via Rebase vs Tangled Merge",
    "Side-by-side comparison of tangled merge graph vs clean straight commit graph.",
    """  <rect x="24" y="24" width="396" height="204" rx="10" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.3"/>
  <text x="44" y="54" fill="#64748B" font-size="14" font-weight="700" font-family="'Geist Mono', monospace">MERGE ปกติ (เส้น Commit ไขว้กัน)</text>
  <line x1="56" y1="116" x2="388" y2="116" stroke="#94A3B8" stroke-width="2.4"/>
  <path d="M 96,124 Q 124,186 184,186 H 264 Q 324,186 352,124" fill="none" stroke="#94A3B8" stroke-width="2" stroke-dasharray="5,3"/>
  <circle cx="96"  cy="116" r="8" fill="#FFFFFF" stroke="#64748B" stroke-width="2"/>
  <circle cx="220" cy="116" r="8" fill="#FFFFFF" stroke="#64748B" stroke-width="2"/>
  <circle cx="352" cy="116" r="8" fill="#FFFFFF" stroke="#64748B" stroke-width="2"/>
  <circle cx="220" cy="186" r="7" fill="#FFFFFF" stroke="#94A3B8" stroke-width="2"/>

  <rect x="448" y="24" width="400" height="204" rx="10" fill="#EEF5FA" stroke="#1F5F8B" stroke-width="1.8"/>
  <text x="468" y="54" fill="#12306E" font-size="14" font-weight="700" font-family="'Geist Mono', monospace">GIT REBASE (Linear 100%)</text>
  <line x1="476" y1="138" x2="816" y2="138" stroke="#1F5F8B" stroke-width="3" marker-end="url(#arr-navy)"/>
  <circle cx="512" cy="138" r="10" fill="#FFFFFF" stroke="#12306E" stroke-width="2.5"/>
  <circle cx="600" cy="138" r="10" fill="#FFFFFF" stroke="#12306E" stroke-width="2.5"/>
  <circle cx="688" cy="138" r="11" fill="#1F5F8B"/>
  <circle cx="768" cy="138" r="11" fill="#1F5F8B"/>
  <text x="512" y="174" fill="#475569" font-size="12" font-weight="600" text-anchor="middle">main 1</text>
  <text x="600" y="174" fill="#475569" font-size="12" font-weight="600" text-anchor="middle">main 2</text>
  <text x="688" y="174" fill="#12306E" font-size="12" font-weight="700" text-anchor="middle">feat 1</text>
  <text x="768" y="174" fill="#12306E" font-size="12" font-weight="700" text-anchor="middle">feat 2</text>
"""
))

# s09 (Type B — 476x296): Rebase Steps & Conflict Resolution
DIAGRAMS["s09"] = (476, 296, "Rebase and Conflict Resolution Flow", wrap(
    "s09", 476, 296,
    "Three-Step Rebase and Conflict Resolution Flow",
    "Vertical workflow for git fetch, git rebase origin/main, solving conflicts, and push --force-with-lease.",
    """  <line x1="238" y1="92"  x2="238" y2="112" stroke="#64748B" stroke-width="2" marker-end="url(#arr)"/>
  <line x1="238" y1="184" x2="238" y2="204" stroke="#1F5F8B" stroke-width="2" marker-end="url(#arr-navy)"/>
""" +
    node(32, 24, 412, 68, "1. Fetch ฐานล่าสุดแล้ว Rebase", "git fetch origin && git rebase origin/main", t_sz=16, s_sz=12.5) +
    node(32, 114, 412, 68, "2. ถ้า Conflict -> แก้ + git add", "git rebase --continue (ทำจนครบทุก Commit)", focal=True, t_sz=15.5, s_sz=12) +
    node(32, 204, 412, 68, "3. Push ขึ้น GitHub อย่างปลอดภัย", "git push --force-with-lease", t_sz=15.5, s_sz=12.5)
))

# s10 (Type B — 476x296): Conventional Commits Anatomy
DIAGRAMS["s10"] = (476, 296, "Conventional Commits Format Anatomy", wrap(
    "s10", 476, 296,
    "Conventional Commit Prefix Anatomy",
    "Top syntax box showing <type>: <summary> feeding 4 standard commit types: feat, fix, docs, and test.",
    """  <line x1="238" y1="96" x2="238" y2="122" stroke="#1F5F8B" stroke-width="2" marker-end="url(#arr-navy)"/>
""" +
    node(32, 22, 412, 74, "<type>: <สรุปสั้นๆ ว่าทำอะไร>", "Example: feat: add 200ms blink pattern", focal=True, t_sz=16, s_sz=12.5) +
    node(32, 124, 196, 68, "feat:", "เพิ่ม Feature ใหม่", mono_t=True, mono_s=False, t_sz=16, s_sz=12.5) +
    node(248, 124, 196, 68, "fix:", "แก้ไข Bug ในโค้ด", mono_t=True, mono_s=False, t_sz=16, s_sz=12.5) +
    node(32, 206, 196, 68, "docs: / test:", "แก้ Docs / เพิ่ม Test", mono_t=True, mono_s=False, t_sz=15, s_sz=12.5) +
    node(248, 206, 196, 68, "ci: / chore:", "ตั้ง CI / ดูแล Repo", mono_t=True, mono_s=False, t_sz=15, s_sz=12.5)
))

# ==============================================================================
# SECTION 03 (LAB 02): s11, s12, s13, s14
# ==============================================================================

# s11 (Type A — 872x252): Standardized Issue Form + PR Gate Result Wireframe
DIAGRAMS["s11"] = (872, 252, "Standardized Issue Form and PR Gate UI", wrap(
    "s11", 872, 252,
    "GitHub Issue Form and Locked PR Review Gate",
    "Side-by-side clean wireframe showing structured Issue Form UI feeding Locked PR Merge Gate.",
    """  <line x1="416" y1="126" x2="454" y2="126" stroke="#1F5F8B" stroke-width="2.4" marker-end="url(#arr-navy)"/>
  <!-- Left Wireframe: Issue Form -->
  <rect x="28" y="24" width="384" height="204" rx="10" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.4"/>
  <rect x="28" y="24" width="384" height="36" rx="10" fill="#EEF5FA"/>
  <text x="46" y="47" fill="#12306E" font-size="14" font-weight="700" font-family="'Geist Mono', monospace">New Issue · Bug Report Form</text>
  <text x="46" y="84" fill="#334155" font-size="13.5" font-weight="700">1. รุ่นบอร์ด ESP32 *</text>
  <rect x="46" y="92" width="346" height="28" rx="6" fill="#F8FAFC" stroke="#CBD5E1"/>
  <text x="58" y="111" fill="#12306E" font-size="12.5" font-family="'Geist Mono', monospace">DOIT ESP32 DevKit v1</text>
  <text x="46" y="146" fill="#334155" font-size="13.5" font-weight="700">2. ขั้นตอนการทำซ้ำ &amp; อาการ *</text>
  <rect x="46" y="154" width="346" height="54" rx="6" fill="#F8FAFC" stroke="#CBD5E1"/>
  <text x="58" y="176" fill="#64748B" font-size="12">บังคับกรอกครบก่อนกด Submit...</text>

  <!-- Right Wireframe: Locked PR -->
  <rect x="460" y="24" width="384" height="204" rx="10" fill="#EEF5FA" stroke="#1F5F8B" stroke-width="1.6"/>
  <rect x="460" y="24" width="384" height="36" rx="10" fill="#1F5F8B"/>
  <text x="478" y="47" fill="#FFFFFF" font-size="14" font-weight="700" font-family="'Geist Mono', monospace">Pull Request #1 · Closes #2</text>
  <rect x="478" y="76" width="348" height="38" rx="6" fill="#FFFFFF" stroke="#CBD5E1"/>
  <text x="494" y="100" fill="#12306E" font-size="13.5" font-weight="700">[x] Checklist ตรวจความเรียบร้อยครบ</text>
  <rect x="478" y="124" width="348" height="38" rx="6" fill="#FFFFFF" stroke="#1F5F8B"/>
  <text x="494" y="148" fill="#1F5F8B" font-size="13.5" font-weight="700">Cloud CI Checks: PASSED (3/3)</text>
  <rect x="478" y="174" width="188" height="36" rx="8" fill="#1F5F8B"/>
  <text x="572" y="197" fill="#FFFFFF" font-size="13.5" font-weight="700" text-anchor="middle">Merge to main (Unlocked)</text>
"""
))

# s12 (Type B — 476x296): Issue Form YAML -> Web Form Flow
DIAGRAMS["s12"] = (476, 296, "YAML Issue Form Anatomy", wrap(
    "s12", 476, 296,
    "YAML Issue Form Structure",
    "Anatomy of .github/ISSUE_TEMPLATE YAML showing top metadata, input types, and required validation.",
    """  <line x1="238" y1="92"  x2="238" y2="112" stroke="#64748B" stroke-width="2" marker-end="url(#arr)"/>
  <line x1="238" y1="184" x2="238" y2="204" stroke="#1F5F8B" stroke-width="2" marker-end="url(#arr-navy)"/>
""" +
    node(32, 24, 412, 68, "1. ส่วนหัวของฟอร์ม (Metadata)", "name: Bug Report  |  labels: [\"bug\"]", t_sz=15.5, s_sz=12.5) +
    node(32, 114, 412, 68, "2. ช่องรับข้อมูล (body:)", "type: dropdown / input / textarea", t_sz=15.5, s_sz=12.5) +
    node(32, 204, 412, 68, "3. บังคับกรอก (validations:)", "required: true  (ปิด Blank Issue ใน config.yml)", focal=True, t_sz=15.5, s_sz=12)
))

# s13 (Type B — 476x296): PR Template & Closes #Issue Automation
DIAGRAMS["s13"] = (476, 296, "PR Template and Closes #Issue Automation", wrap(
    "s13", 476, 296,
    "Pull Request Template and Auto-Closing Issues",
    "Flow from pull_request_template.md with Closes #N to Merge PR automatically closing Issue #N.",
    """  <line x1="238" y1="92"  x2="238" y2="112" stroke="#64748B" stroke-width="2" marker-end="url(#arr)"/>
  <line x1="238" y1="184" x2="238" y2="204" stroke="#1F5F8B" stroke-width="2" marker-end="url(#arr-navy)"/>
""" +
    node(32, 24, 412, 68, ".github/pull_request_template.md", "PR Template ที่มี Checklist เตือนความจำ", mono_t=True, mono_s=False, t_sz=14.5, s_sz=12.5) +
    node(32, 114, 412, 68, "ใส่คำสั่งเชื่อมงาน: Closes #1", "ระบบรู้ทันทีว่า PR นี้สร้างมาเพื่อปิด Issue #1", t_sz=15.5, s_sz=12.5) +
    node(32, 204, 412, 68, "กด Rebase and merge -> ปิดอัตโนมัติ", "Issue #1 เปลี่ยนเป็น Closed ทันที", focal=True, t_sz=15, s_sz=12.5)
))

# s14 (Type B — 476x296): Role Benefits from Issue Form + Branch Protection
DIAGRAMS["s14"] = (476, 296, "How Issue Forms and Branch Protection Help Teams", wrap(
    "s14", 476, 296,
    "Team Impact of Structured Issues and Protected Main Branch",
    "Structured grid showing impact on Reporter, Developer, and Tech Lead.",
    """  <line x1="238" y1="92"  x2="238" y2="112" stroke="#64748B" stroke-width="2" marker-end="url(#arr)"/>
  <line x1="238" y1="184" x2="238" y2="204" stroke="#1F5F8B" stroke-width="2" marker-end="url(#arr-navy)"/>
""" +
    node(32, 24, 412, 68, "Reporter & Developer", "ได้ Spec บอร์ดครบตั้งแต่ต้น ไม่ต้องถามซ้ำ", mono_s=False, t_sz=16, s_sz=12.5) +
    node(32, 114, 412, 68, "Cloud CI & Reviewer", "เช็กผลอัตโนมัติและ Checklist ก่อน Review โค้ด", mono_s=False, t_sz=16, s_sz=12.5) +
    node(32, 204, 412, 68, "Branch Protection บน main", "Lock ปุ่ม Merge จนกว่า CI จะผ่าน 100%", focal=True, mono_s=False, t_sz=16, s_sz=12.5)
))

# ==============================================================================
# SECTION 04 (LAB 03): s15, s16, s17, s18
# ==============================================================================

# s15 (Type A — 872x252): Pre-commit Intercept Flow (Result)
DIAGRAMS["s15"] = (872, 252, "Pre-commit Local Gate Result", wrap(
    "s15", 872, 252,
    "Automatic Two-Second Pre-commit Check on git commit",
    "Flow from git commit trigger to formatting/YAML checks to either fast auto-fix halt or clean commit.",
    """  <line x1="246" y1="126" x2="278" y2="126" stroke="#64748B" stroke-width="2.2" marker-end="url(#arr)"/>
  <line x1="572" y1="126" x2="604" y2="126" stroke="#1F5F8B" stroke-width="2.2" marker-end="url(#arr-navy)"/>
""" +
    chip(74, 34, "TRIGGER", 120) +
    chip(366, 34, "2 SECONDS", 120) +
    chip(666, 34, "OUTCOME", 120) +
    node(28, 76, 218, 128, "git commit -m ...", "สั่ง Commit โค้ดในเครื่อง", mono_t=True, mono_s=False, t_sz=17, s_sz=13.5) +
    node(282, 76, 290, 128, "ตรวจ Format + Message", "clang-format · YAML · Commit", mono_s=False, t_sz=18, s_sz=13.5) +
    node(608, 76, 236, 128, "โค้ดสะอาด 100%", "ไม่ผ่าน=Block / ผ่าน=Commit", focal=True, mono_s=False, t_sz=18, s_sz=13.5)
))

# s16 (Type B — 476x296): .clang-format & Two-Stage Hook Architecture
DIAGRAMS["s16"] = (476, 296, "Two-Stage Pre-commit Hook Architecture", wrap(
    "s16", 476, 296,
    ".clang-format and Two-Stage Hook Pipeline",
    "Top rule file .clang-format feeding Stage 1 pre-commit file hooks and Stage 2 commit-msg hook.",
    """  <line x1="238" y1="92"  x2="238" y2="112" stroke="#64748B" stroke-width="2" marker-end="url(#arr)"/>
  <line x1="238" y1="184" x2="238" y2="204" stroke="#1F5F8B" stroke-width="2" marker-end="url(#arr-navy)"/>
""" +
    node(32, 24, 412, 68, "กติกากลาง: .clang-format", "BasedOnStyle: Google · IndentWidth: 2", t_sz=15.5, s_sz=12.5) +
    node(32, 114, 412, 68, "Stage 1 (stage: pre-commit)", "ตรวจไฟล์พื้นฐาน · YAML · จัด Format C++", t_sz=15.5, s_sz=12.5) +
    node(32, 204, 412, 68, "Stage 2 (stage: commit-msg)", "conventional-pre-commit ตรวจ Conventional Commit", focal=True, t_sz=15.5, s_sz=11.5)
))

# s17 (Type B — 476x296): Where to Find Pre-commit Hooks (pre-commit.com + GitHub Search)
DIAGRAMS["s17"] = (476, 296, "Discovering and Pinning Pre-commit Hooks", wrap(
    "s17", 476, 296,
    "Finding Pre-commit Hooks Across Official List and GitHub",
    "Two discovery channels: pre-commit.com/hooks.html for pre-commit-hooks and mirrors-clang-format, and GitHub Search (.pre-commit-hooks.yaml) for compilerla/conventional-pre-commit, each pinned with rev versions.",
    """  <line x1="126" y1="100" x2="126" y2="132" stroke="#64748B" stroke-width="1.8" marker-end="url(#arr)"/>
  <line x1="350" y1="100" x2="350" y2="132" stroke="#64748B" stroke-width="1.8" marker-end="url(#arr)"/>
  <line x1="126" y1="200" x2="126" y2="222" stroke="#1F5F8B" stroke-width="1.8" marker-end="url(#arr-navy)"/>
  <line x1="350" y1="200" x2="350" y2="222" stroke="#1F5F8B" stroke-width="1.8" marker-end="url(#arr-navy)"/>
""" +
    node(22, 24, 208, 76, "pre-commit.com/hooks.html", "Starter List + pre-commit/mirrors-*", mono_t=True, mono_s=False, t_sz=12, s_sz=10.2) +
    node(246, 24, 208, 76, "GitHub Search (Code/Repo)", "คำค้น + path:.pre-commit-hooks.yaml", mono_t=False, mono_s=False, t_sz=13, s_sz=9.8) +
    node(22, 134, 208, 66, "Official & Mirrors", "pre-commit-hooks, mirrors-clang-format", mono_t=False, mono_s=False, t_sz=13, s_sz=9.8) +
    node(246, 134, 208, 66, "Community Repo", "compilerla/conventional-pre-commit", mono_t=False, mono_s=False, t_sz=13, s_sz=10) +
    node(22, 224, 208, 48, "rev: v6.0.0 / v23.1.5", mono_t=True, focal=True, t_sz=12) +
    node(246, 224, 208, 48, "rev: v4.5.0", mono_t=True, focal=True, t_sz=13)
))

# s18 (Type A — 872x252): Clean Terminal Showcase of Pre-commit Running
DIAGRAMS["s18"] = (872, 252, "Terminal Output of Pre-commit Checks", wrap(
    "s18", 872, 252,
    "Pre-commit Terminal Output Showing All Hooks Passed",
    "Minimalist terminal window showing pre-commit running checks and passing in 2 seconds.",
    term_shell(872, 252, "uv run pre-commit run --all-files", [
        ("trim trailing whitespace ..............................................", "PASS"),
        ("fix end of files ......................................................", "PASS"),
        ("check yaml ............................................................", "PASS"),
        ("clang-format (C/C++ Google Style, Indent 2) ...........................", "PASS"),
        ("conventional-pre-commit (Conventional Commits) ........................", "PASS"),
    ]),
    bg="#FFFFFF", border="#CBD5E1"
))

# ==============================================================================
# SECTION 05 (LAB 04): s19, s20, s21, s22
# ==============================================================================

# s19 (Type A — 872x252): 0.18s Native Unit Test vs 45s Hardware Flashing
DIAGRAMS["s19"] = (872, 252, "Native Unit Test Speed Result", wrap(
    "s19", 872, 252,
    "0.18s Host Native Test vs 45s Hardware Board Flashing",
    "Bar comparison showing 250x speedup when testing C++ firmware logic natively on PC.",
    """  <rect x="24" y="24" width="824" height="92" rx="10" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.3"/>
  <text x="44" y="60" fill="#475569" font-size="16.5" font-weight="700">Test บนบอร์ดจริง</text>
  <text x="44" y="84" fill="#64748B" font-size="13" font-family="'Geist Mono', monospace">Flash via USB Cable</text>
  <rect x="268" y="48" width="424" height="44" rx="8" fill="#E2E8F0"/>
  <text x="480" y="75" fill="#334155" font-size="15" font-weight="700" font-family="'Geist Mono', monospace" text-anchor="middle">45 วินาที / รอบ · รันบน Cloud CI ไม่ได้</text>
  <text x="768" y="77" fill="#64748B" font-size="22" font-weight="700" font-family="'Geist Mono', monospace" text-anchor="middle">45.0s</text>

  <rect x="24" y="132" width="824" height="96" rx="10" fill="#EEF5FA" stroke="#1F5F8B" stroke-width="1.8"/>
  <text x="44" y="168" fill="#12306E" font-size="17" font-weight="700">Native Unit Test (Host PC)</text>
  <text x="44" y="194" fill="#1F5F8B" font-size="13.5" font-weight="700" font-family="'Geist Mono', monospace">pio test -e native</text>
  <rect x="268" y="158" width="108" height="44" rx="8" fill="#1F5F8B"/>
  <text x="322" y="185" fill="#FFFFFF" font-size="14.5" font-weight="700" font-family="'Geist Mono', monospace" text-anchor="middle">0.18s</text>
  <text x="548" y="185" fill="#12306E" font-size="16.5" font-weight="700" text-anchor="middle">เร็วขึ้น 250 เท่า · 5/5 PASSED</text>
  <text x="768" y="187" fill="#12306E" font-size="24" font-weight="700" font-family="'Geist Mono', monospace" text-anchor="middle">0.18s</text>
"""
))

# s20 (Type B — 476x296): Hardware-Decoupled Architecture
DIAGRAMS["s20"] = (476, 296, "Hardware-Decoupled Firmware Architecture", wrap(
    "s20", 476, 296,
    "Separating Pure Logic from Hardware Peripherals",
    "lib/blink_math pure C++ library consumed by both src/main.cpp and test/test_main.cpp.",
    """  <path d="M 176,106 V 138 Q 176,150 164,150 H 134 Q 122,150 122,162 V 184" fill="none" stroke="#64748B" stroke-width="2" marker-end="url(#arr)"/>
  <path d="M 300,106 V 138 Q 300,150 312,150 H 342 Q 354,150 354,162 V 184" fill="none" stroke="#1F5F8B" stroke-width="2.2" marker-end="url(#arr-navy)"/>
""" +
    node(88, 28, 300, 78, "lib/blink_math/", "Pure C++ Logic (ไม่ใช้ Arduino.h)", focal=True, mono_t=True, t_sz=17, s_sz=13) +
    node(28, 186, 192, 82, "src/main.cpp", "Hardware GPIO / LED จริง", mono_t=True, mono_s=False, t_sz=15.5, s_sz=12.5) +
    node(256, 186, 192, 82, "test/test_main.cpp", "รัน Unity Test บน Host PC", focal=True, mono_t=True, mono_s=False, t_sz=15, s_sz=12.5)
))

# s21 (Type B — 476x296): PlatformIO Dual Environments (platformio.ini)
DIAGRAMS["s21"] = (476, 296, "PlatformIO Dual Environments", wrap(
    "s21", 476, 296,
    "PlatformIO Dual Environments in platformio.ini",
    "Split diagram showing [env:esp32doit-devkit-v1] for hardware build vs [env:native] for host tests.",
    node(32, 24, 412, 54, "platformio.ini (กำหนด Dual Environment)", focal=False, mono_s=False, t_sz=15.5) +
    node(32, 98, 412, 80, "[env:esp32doit-devkit-v1]", "platform = espressif32  |  pio run (Build .bin)", mono_t=True, t_sz=15, s_sz=12) +
    node(32, 194, 412, 80, "[env:native]", "platform = native · test_build_src = no (pio test)", focal=True, mono_t=True, t_sz=16, s_sz=12)
))

# s22 (Type B — 476x296): Unity Test Lifecycle
DIAGRAMS["s22"] = (476, 296, "Unity Test Case Anatomy", wrap(
    "s22", 476, 296,
    "Unity Unit Test Execution Flow",
    "Sequential Unity test lifecycle: UNITY_BEGIN -> RUN_TEST + TEST_ASSERT_EQUAL -> UNITY_END.",
    """  <line x1="238" y1="92"  x2="238" y2="112" stroke="#64748B" stroke-width="2" marker-end="url(#arr)"/>
  <line x1="238" y1="184" x2="238" y2="204" stroke="#1F5F8B" stroke-width="2" marker-end="url(#arr-navy)"/>
""" +
    node(32, 24, 412, 68, "1. UNITY_BEGIN()", "เริ่มเปิด Test Suite และตั้งค่าเริ่มต้น", mono_t=True, mono_s=False, t_sz=15.5, s_sz=12.5) +
    node(32, 114, 412, 68, "2. RUN_TEST(...) + TEST_ASSERT_EQUAL", "เทียบค่าจริงกับ Expected Value (Normal & Boundary)", focal=True, mono_t=True, mono_s=False, t_sz=14, s_sz=11.5) +
    node(32, 204, 412, 68, "3. UNITY_END()", "สรุปจำนวน Case ผ่าน/ตก พร้อม Exit Code", mono_t=True, mono_s=False, t_sz=15.5, s_sz=12.5)
))

# ==============================================================================
# SECTION 06 (LAB 05): s23, s24, s25, s26
# ==============================================================================

# s23 (Type A — 872x252): Cloud CI 3-Job Pipeline Result
DIAGRAMS["s23"] = (872, 252, "Cloud CI Automated Pipeline Result", wrap(
    "s23", 872, 252,
    "GitHub Actions CI Three-Stage Verification Result",
    "Horizontal Cloud CI flow: Push/PR triggers Lint Check, Unity Native Test, ESP32 Compile, and Merge Gate.",
    """  <line x1="196" y1="142" x2="218" y2="142" stroke="#64748B" stroke-width="2.2" marker-end="url(#arr)"/>
  <line x1="400" y1="142" x2="422" y2="142" stroke="#64748B" stroke-width="2.2" marker-end="url(#arr)"/>
  <line x1="604" y1="142" x2="626" y2="142" stroke="#1F5F8B" stroke-width="2.4" marker-end="url(#arr-navy)"/>
""" +
    chip(48, 34, "JOB 01", 120) +
    chip(252, 34, "JOB 02", 120) +
    chip(456, 34, "JOB 03", 120) +
    chip(676, 34, "RESULT", 120) +
    node(24, 78, 172, 128, "1. Lint Check", "ตรวจ Format ซ้ำ", mono_s=False, t_sz=17, s_sz=13.5) +
    node(228, 78, 172, 128, "2. Unit Test", "pio test -e native", t_sz=17, s_sz=13) +
    node(432, 78, 172, 128, "3. Build ESP32", "ลอง Compile .bin จริง", mono_s=False, t_sz=17, s_sz=13) +
    node(636, 78, 212, 128, "PR Merge Gate", "เขียว=ผ่าน / แดง=Block", focal=True, mono_s=False, t_sz=18, s_sz=13.5)
))

# s24 (Type B — 476x296): Workflow Anatomy (Trigger -> Runner -> Steps)
DIAGRAMS["s24"] = (476, 296, "CI Workflow Structural Anatomy", wrap(
    "s24", 476, 296,
    "Three Structural Blocks of ci.yml",
    "Trigger (on:) -> Job & Runner (runs-on:) -> Steps (Checkout -> Setup -> Run).",
    """  <line x1="238" y1="92"  x2="238" y2="112" stroke="#64748B" stroke-width="2" marker-end="url(#arr)"/>
  <line x1="238" y1="184" x2="238" y2="204" stroke="#1F5F8B" stroke-width="2" marker-end="url(#arr-navy)"/>
""" +
    node(32, 24, 412, 68, "Block 1: Trigger (on:)", "push / pull_request -> Event เริ่มรัน CI", mono_s=False, t_sz=16, s_sz=12.5) +
    node(32, 114, 412, 68, "Block 2: Job & Runner (runs-on:)", "ubuntu-latest -> ขอ Cloud Linux VM สะอาด", t_sz=16, s_sz=12.5) +
    node(32, 204, 412, 68, "Block 3: Steps (ลำดับคำสั่ง)", "3.1 Checkout  ->  3.2 Setup  ->  3.3 Run Test", focal=True, t_sz=16, s_sz=12.5)
))

# s25 (Type B — 476x296): Where to Find Actions & Version Pinning
DIAGRAMS["s25"] = (476, 296, "GitHub Marketplace and Version Pinning", wrap(
    "s25", 476, 296,
    "Discovering Verified Actions and Pinning @Version",
    "GitHub Marketplace top node feeding verified orgs and pinned checkout@v7, cache@v6, and setup-uv@v10.",
    """  <path d="M 176,94 V 104 Q 176,112 156,112 H 104 Q 94,112 94,122 V 134" fill="none" stroke="#64748B" stroke-width="1.8" marker-end="url(#arr)"/>
  <line x1="238" y1="94" x2="238" y2="134" stroke="#64748B" stroke-width="1.8" marker-end="url(#arr)"/>
  <path d="M 300,94 V 104 Q 300,112 320,112 H 372 Q 382,112 382,122 V 134" fill="none" stroke="#64748B" stroke-width="1.8" marker-end="url(#arr)"/>
  <line x1="94"  y1="196" x2="94"  y2="216" stroke="#1F5F8B" stroke-width="1.8" marker-end="url(#arr-navy)"/>
  <line x1="238" y1="196" x2="238" y2="216" stroke="#1F5F8B" stroke-width="1.8" marker-end="url(#arr-navy)"/>
  <line x1="382" y1="196" x2="382" y2="216" stroke="#1F5F8B" stroke-width="1.8" marker-end="url(#arr-navy)"/>
""" +
    node(48, 22, 380, 72, "github.com/marketplace?type=actions", "Official Catalog สำหรับ Action มาตรฐาน", mono_t=True, mono_s=False, t_sz=14.5, s_sz=12.5) +
    node(24, 136, 140, 60, "Checkout โค้ด", "actions/*", mono_s=True, t_sz=14, s_sz=12) +
    node(174, 136, 128, 60, "Cache Build", "actions/*", mono_s=True, t_sz=14.5, s_sz=12) +
    node(312, 136, 140, 60, "Setup uv/PIO", "astral-sh/*", mono_s=True, t_sz=14, s_sz=12) +
    node(24, 218, 140, 54, "checkout@v7", mono_t=True, focal=True, t_sz=13.5) +
    node(174, 218, 128, 54, "cache@v6", mono_t=True, focal=True, t_sz=13.5) +
    node(312, 218, 140, 54, "setup-uv@v10", mono_t=True, focal=True, t_sz=13)
))

# s26 (Type B — 476x296): Speeding up CI with Cache & Artifacts
DIAGRAMS["s26"] = (476, 296, "CI Cache and Artifacts Optimization", wrap(
    "s26", 476, 296,
    "PlatformIO Cache Speedup and Artifact Storage",
    "Showing cache hit speedup for ~/.platformio and artifact upload of built firmware binaries.",
    node(32, 24, 412, 68, "ไม่มี Cache: โหลด PlatformIO ใหม่ทุกรอบ (~4 นาที)", mono_s=False, t_sz=14.5) +
    node(32, 114, 412, 68, "ใช้ actions/cache@v6 เก็บ ~/.platformio (~1 นาที)", "key ผูกกับ hashFiles('workshop/platformio.ini')", focal=True, t_sz=14, s_sz=12) +
    node(32, 204, 412, 68, "upload-artifact@v7 เก็บ Build Artifact (.bin)", "ดาวน์โหลดไป Test ต่อได้บน Branch release/**", t_sz=14.5, s_sz=12.5)
))

# ==============================================================================
# SECTION 07 (LAB 06 & SUMMARY): s27, s28, s29, s30, s31
# ==============================================================================

# s27 (Type A — 872x252): Tag v1.0.0 -> GitHub Releases Page Result
DIAGRAMS["s27"] = (872, 252, "GitHub Release Result on Tag Push", wrap(
    "s27", 872, 252,
    "Push Version Tag Produces Ready-to-Flash Assets on GitHub Releases",
    "Flow from git tag v1.0.0 to Cloud Merge-Bin to Release page showing OTA and Merged factory .bin files.",
    """  <line x1="252" y1="126" x2="294" y2="126" stroke="#1F5F8B" stroke-width="2.4" marker-end="url(#arr-navy)"/>
""" +
    node(28, 56, 222, 140, "git tag v1.0.0", "git push --tags", focal=False, mono_t=True, t_sz=18, s_sz=13.5) +
    """  <!-- Release Page Wireframe -->
  <rect x="300" y="24" width="544" height="204" rx="10" fill="#EEF5FA" stroke="#1F5F8B" stroke-width="1.6"/>
  <rect x="300" y="24" width="544" height="38" rx="10" fill="#1F5F8B"/>
  <text x="322" y="48" fill="#FFFFFF" font-size="14.5" font-weight="700" font-family="'Geist Mono', monospace">GitHub Releases · v1.0.0 (Latest)</text>
  <rect x="322" y="78" width="500" height="58" rx="8" fill="#FFFFFF" stroke="#CBD5E1"/>
  <text x="342" y="103" fill="#0F172A" font-size="15" font-weight="700" font-family="'Geist Mono', monospace">esp32doit-v1.0.0-firmware.bin</text>
  <text x="342" y="124" fill="#64748B" font-size="12.5">App Firmware ล้วน สำหรับอัปเดตผ่าน OTA</text>
  <rect x="322" y="150" width="500" height="62" rx="8" fill="#FFFFFF" stroke="#1F5F8B" stroke-width="1.6"/>
  <text x="342" y="176" fill="#12306E" font-size="15.5" font-weight="700" font-family="'Geist Mono', monospace">esp32doit-v1.0.0-merged-firmware.bin</text>
  <text x="342" y="198" fill="#1F5F8B" font-size="12.5" font-weight="700">Merged Binary: Bootloader + Partitions + App (Flash ที่ 0x0)</text>
"""
))

# s28 (Type B — 476x296): ESP32 Memory Offsets & esptool merge-bin
DIAGRAMS["s28"] = (476, 296, "ESP32 Flash Partitions and merge-bin", wrap(
    "s28", 476, 296,
    "Merging 3 ESP32 Flash Partitions at Offset 0x0",
    "Three flash partitions (0x1000 bootloader, 0x8000 partitions, 0x10000 firmware) merging into one 0x0 file.",
    """  <line x1="94"  y1="126" x2="94"  y2="180" stroke="#1F5F8B" stroke-width="1.8" marker-end="url(#arr-navy)"/>
  <line x1="238" y1="126" x2="238" y2="180" stroke="#1F5F8B" stroke-width="1.8" marker-end="url(#arr-navy)"/>
  <line x1="382" y1="126" x2="382" y2="180" stroke="#1F5F8B" stroke-width="1.8" marker-end="url(#arr-navy)"/>
""" +
    node(24, 34, 140, 90, "0x1000", "bootloader.bin", mono_t=True, t_sz=16, s_sz=12) +
    node(174, 34, 128, 90, "0x8000", "partitions.bin", mono_t=True, t_sz=16, s_sz=12) +
    node(312, 34, 140, 90, "0x10000", "firmware.bin", mono_t=True, t_sz=16, s_sz=12) +
    node(24, 182, 428, 84, "esptool --chip esp32 merge-bin (0x0)", "รวม 3 ไฟล์เป็น Binary เดียว ไม่ต้องจำ Offset ตอน Flash", focal=True, mono_t=True, mono_s=False, t_sz=14.5, s_sz=12.5)
))

# s29 (Type B — 476x296): Release Workflow Structure (release.yml)
DIAGRAMS["s29"] = (476, 296, "Release Workflow Configuration", wrap(
    "s29", 476, 296,
    "Three Key Elements of release.yml",
    "Tag trigger v*, contents: write permission, and softprops/action-gh-release.",
    """  <line x1="238" y1="92"  x2="238" y2="112" stroke="#64748B" stroke-width="2" marker-end="url(#arr)"/>
  <line x1="238" y1="184" x2="238" y2="204" stroke="#1F5F8B" stroke-width="2" marker-end="url(#arr-navy)"/>
""" +
    node(32, 24, 412, 68, "1. Trigger: on: push: tags: ['v*']", "ทำงานเฉพาะตอน Push Tag เวอร์ชัน (เช่น v1.0.0)", t_sz=15, s_sz=12.5) +
    node(32, 114, 412, 68, "2. Permission: contents: write", "อนุญาตให้ Workflow สร้าง GitHub Release และแนบไฟล์ได้", t_sz=14.5, s_sz=12.5) +
    node(32, 204, 412, 68, "3. Upload: gh-release@v3", "Upload ทั้งไฟล์ OTA และ Factory Binary อัตโนมัติ", focal=True, t_sz=15, s_sz=12.5)
))

# s30 (Type B — 476x296): Automated Student Verification Scripts
DIAGRAMS["s30"] = (476, 296, "check_env.py and verify.py Output", wrap(
    "s30", 476, 296,
    "Automated Workshop Environment Check and Lab Verification",
    "Minimalist terminal view showing verify.py checking Exercise 1 to 6.",
    term_shell(476, 296, "uv run python exercises/verify.py", [
        ("Lab 01: Branch & Rebase ......", "PASS"),
        ("Lab 02: Issue & PR Gate ......", "PASS"),
        ("Lab 03: Pre-commit Hooks .....", "PASS"),
        ("Lab 04: Unity Native Test ....", "PASS"),
        ("Lab 05 & 06: CI + Release ....", "PASS"),
    ]),
    bg="#FFFFFF", border="#CBD5E1"
))

# s31 (Type A — 872x252): 6-Milestone Complete Pipeline Roadmap Summary
DIAGRAMS["s31"] = (872, 252, "Six-Milestone Engineering Pipeline Summary", wrap(
    "s31", 872, 252,
    "Summary of All Six Quality Gates Across the Workshop",
    "Six milestone cards from Lab 01 Linear Git to Lab 06 Automated Release.",
    """  <line x1="286" y1="82"  x2="306" y2="82"  stroke="#64748B" stroke-width="1.8" marker-end="url(#arr)"/>
  <line x1="566" y1="82"  x2="586" y2="82"  stroke="#64748B" stroke-width="1.8" marker-end="url(#arr)"/>
  <line x1="718" y1="122" x2="718" y2="142" stroke="#1F5F8B" stroke-width="2" marker-end="url(#arr-navy)"/>
  <line x1="588" y1="184" x2="568" y2="184" stroke="#1F5F8B" stroke-width="2" marker-end="url(#arr-navy)"/>
  <line x1="308" y1="184" x2="288" y2="184" stroke="#1F5F8B" stroke-width="2" marker-end="url(#arr-navy)"/>
""" +
    node(28, 36, 258, 86, "Lab 01: Git Rebase", "Branch & Linear History", mono_s=False, t_sz=17, s_sz=13) +
    node(308, 36, 258, 86, "Lab 02: Issue & PR", "Issue Form & Lock main", mono_s=False, t_sz=17, s_sz=13) +
    node(588, 36, 258, 86, "Lab 03: Pre-commit", "Local Gate ใน 2 วินาที", mono_s=False, t_sz=17, s_sz=13) +
    node(588, 144, 258, 86, "Lab 04: Unit Test", "Native Test 0.18s บน Host", focal=True, mono_s=False, t_sz=17, s_sz=13) +
    node(308, 144, 258, 86, "Lab 05: Cloud CI", "Lint & Build ESP32", focal=True, mono_s=False, t_sz=17, s_sz=13) +
    node(28, 144, 258, 86, "Lab 06: Release CD", "Tag -> merge-bin (0x0)", focal=True, mono_s=False, t_sz=17, s_sz=13)
))

AUTO_FIT_JS = """() => {
  const boxes = Array.from(document.querySelectorAll('rect.fit-box')).map(r => ({
    x: parseFloat(r.getAttribute('x')),
    y: parseFloat(r.getAttribute('y')),
    w: parseFloat(r.getAttribute('width')),
    h: parseFloat(r.getAttribute('height'))
  }));
  for (const t of document.querySelectorAll('svg text')) {
    const tx = parseFloat(t.getAttribute('x'));
    const ty = parseFloat(t.getAttribute('y'));
    const box = boxes.find(b => tx >= b.x && tx <= b.x + b.w && ty >= b.y && ty <= b.y + b.h);
    if (!box) continue;
    const maxW = box.w - 16;
    let fs = parseFloat(t.getAttribute('font-size') || '14');
    while (t.getBBox().width > maxW && fs > 9.5) {
      fs -= 0.5;
      t.setAttribute('font-size', fs.toFixed(1));
    }
  }
}"""


def main():
    failures = 0
    files = []
    for sid, (w, h, title, svg_code) in sorted(DIAGRAMS.items()):
        hp = HTML_DIR / f"dd-{sid}.html"
        hp.write_text(HEAD_TEMPLATE.format(title=title, svg=svg_code), encoding="utf-8")
        res = subprocess.run(["uv", "run", "python", str(SELF_CHECK), str(hp)], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"[FAIL] {sid}: {res.stdout} {res.stderr}")
            failures += 1
        else:
            print(f"[PASS] {sid}")
        files.append((sid, hp))

    if failures > 0:
        raise RuntimeError(f"{failures} diagrams failed self_check.py")

    with sync_playwright() as p:
        b = p.chromium.launch(channel="msedge")
        page = b.new_page(device_scale_factor=3)
        for sid, hp in files:
            page.goto(f"file://{hp.resolve()}")
            page.wait_for_load_state("networkidle")
            page.evaluate(AUTO_FIT_JS)
            out_png = IMG_DIR / f"img-{sid}.png"
            page.locator("svg").first.screenshot(path=str(out_png), omit_background=True)
            print(f"Exported {out_png.name}")
        b.close()


if __name__ == "__main__":
    main()
