#!/usr/bin/env python3
"""
Generate 6 individual Lab Sheet PDFs (1 file = 1 topic) into docs/labs/.
Each lab includes objectives, outcomes, copy-paste ready code/configs matching
exercises/solutions/ and workshop/, expected terminal output, questions,
exercises, and full-width (1 per row) real screenshots.
"""

import html
import subprocess
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parents[1]
LABS_DIR = DOCS_DIR / "labs"
HTML_DIR = DOCS_DIR / "labs_html"
LABS_DIR.mkdir(exist_ok=True)
HTML_DIR.mkdir(exist_ok=True)
EDGE_EXE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

LABS = [
    {
        "slug": "LAB00-Environment_Setup",
        "title": "Lab 00: Environment Setup &amp; Toolchain Preparation (เตรียมเครื่องครบทุก Lab)",
        "objectives": [
            "ติดตั้งเครื่องมือทั้งหมดที่ใช้ตั้งแต่ Lab 01 ถึง Lab 06 ไว้ล่วงหน้าในจุดเดียว (Git, <code>uv</code>, CLI Tools, VS Code Extensions, WinLibs <code>gcc</code> และ PlatformIO)",
            "Fork โปรเจกต์ Pre-cache แพ็กเกจ ESP32, เปิดใช้งาน GitHub Actions บน Fork และตรวจสอบความพร้อมด้วย <code>exercises/check_env.py</code>",
        ],
        "outcomes": [
            "สามารถเรียกใช้งานคำสั่ง <code>git</code>, <code>uv</code>, <code>pre-commit</code>, <code>pio</code>, <code>esptool</code> (และ <code>gh</code>/<code>gcc</code>) จาก Terminal ได้จริง",
            "รัน <code>uv run exercises/check_env.py</code> ผ่านและ Build โปรเจกต์ตัวอย่าง <code>workshop/</code> ล่วงหน้าได้ก่อนเริ่ม Lab 01",
        ],
        "tools": [
            "Windows 10/11 (PowerShell), macOS หรือ Linux พร้อมสิทธิ์ติดตั้งโปรแกรมและอินเทอร์เน็ต",
            "VS Code (Visual Studio Code) และบัญชี GitHub ส่วนตัว",
            "สคริปต์ตรวจความพร้อม: <code>uv run exercises/check_env.py</code>",
        ],
        "experiments": [
            ("LAB-0001", "(core-cli) ติดตั้ง Git, ตั้งค่าผู้ใช้งาน และติดตั้ง <code>uv</code> พร้อมชุด CLI Tools ทั้งหมดสำหรับทุก Lab (<code>pre-commit</code>, <code>platformio</code>, <code>esptool</code>)"),
            ("LAB-0002", "(compilers &amp; gh) ติดตั้ง WinLibs <code>gcc/g++</code> สำหรับ Windows (ใช้ใน Lab 04) และ GitHub CLI <code>gh</code> (Optional สำหรับ Lab 05–06)"),
            ("LAB-0003", "(vscode &amp; warmup) Fork + Clone โปรเจกต์, ติดตั้ง VS Code Extensions 2 ตัวตามที่แนะนำ, พรีโหลด PlatformIO ESP32 และเปิดใช้งาน Actions"),
        ],
        "details": [
            {
                "heading": "LAB-0001 (ส่วนที่ 1/2): ติดตั้ง Git CLI และตั้งชื่อ/อีเมลผู้ใช้",
                "desc": "ติดตั้ง Git (Windows: <code>winget install Git.Git</code> หรือโหลดจาก git-scm.com) แล้วตั้งค่าตัวตนสำหรับสร้าง Commit — <strong>หมายเหตุสำหรับเครื่องคอมพิวเตอร์มหาวิทยาลัย:</strong> หากใช้เครื่องส่วนกลาง แนะนำให้ใช้ <code>git config --local</code> ภายในโฟลเดอร์งานหลังจาก Clone แทน <code>--global</code>",
                "code": """# 1. ตรวจสอบ Git (หรือติดตั้งบน Windows)
winget install Git.Git
git --version

# 2. ตั้งค่าชื่อและอีเมลสำหรับเครื่องส่วนตัว (ถ้าเป็นเครื่องมหาลัย ให้ทำ --local หลัง Clone ใน LAB-0003)
git config --global user.name "Your Name"
git config --global user.email "you@example.com" """,
            },
            {
                "heading": "LAB-0001 (ส่วนที่ 2/2): ติดตั้ง uv และเครื่องมือ CLI สำหรับทุก Lab (pre-commit, pio, esptool)",
                "desc": "ติดตั้ง <code>uv</code> ตัวเดียวเพื่อจัดการ Python + CLI Tools ของ Workshop ทั้งหมด (รวมของเดิมที่เคยอยู่แยกใน Lab 03, 04 และ 06 มาลงพร้อมกันที่นี่) แล้วรัน <code>uv tool update-shell</code> เพื่อเพิ่ม PATH บน Windows",
                "code": """# Windows (PowerShell): ติดตั้ง uv (macOS/Linux: curl -LsSf https://astral.sh/uv/install.sh | sh)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# เปิด Terminal ใหม่แล้วติดตั้ง CLI Tools ทั้งหมดในชุดเดียว:
uv tool install pre-commit
uv tool install platformio
uv tool install esptool
uv tool update-shell""",
            },
            {
                "heading": "LAB-0002: ติดตั้ง C/C++ Compiler (gcc) บน Windows และ GitHub CLI (gh)",
                "desc": "ลง WinLibs <code>gcc/g++</code> เพื่อใช้คอมไพล์ <code>pio test -e native</code> ใน Lab 04 (บน Linux/macOS มี <code>gcc</code>/<code>clang</code> แล้ว; หากเครื่องมหาลัยล็อกสิทธิ์ลง <code>gcc</code> ไม่ได้ ให้ดูผลรันบน Cloud CI Linux ใน Lab 05 แทนได้) และลง <code>gh</code> (Optional) สำหรับดูสถานะ Actions/Release",
                "code": """# 1. Windows: ติดตั้ง MinGW/WinLibs gcc/g++ สำหรับ [env:native]
winget install BrechtSanders.WinLibs.POSIX.UCRT

# 2. Optional: ติดตั้ง GitHub CLI (gh) — เปิด Terminal ใหม่หลังติดตั้งเพื่อรีเฟรช PATH
winget install GitHub.cli""",
            },
            {
                "heading": "LAB-0003 (ขั้นตอนที่ 1/2): Fork โปรเจกต์, Clone ลงเครื่อง และเปิดใช้งาน Actions",
                "desc": "เปิด Repository หลัก <code>https://github.com/SavEe2429/git-practice</code> -> กด <code>[1] Fork</code> -> กด <code>[2] &lt;&gt; Code</code> เพื่อ Copy URL ของ Fork ตัวเอง จากนั้น Clone ลงเครื่อง และเข้าแท็บ <strong>Actions</strong> บน Fork แล้วกดปุ่มสีเขียว <em>I understand my workflows, go ahead and enable them</em> เตรียมไว้ล่วงหน้า",
                "images": [
                    ("../images/anno-01-repo-fork.png", "หน้าเว็บ GitHub: [1] กดปุ่ม Fork -> [2] กด <> Code เพื่อ Copy URL ของ Fork ตัวเอง"),
                ],
                "code": """# Clone จาก Fork ของตัวเอง (เปลี่ยน <your-username> เป็นชื่อบัญชี GitHub ของคุณ)
git clone https://github.com/<your-username>/git-practice.git
cd git-practice

# เพิ่ม upstream อ้างอิง Repo ต้นทางของอาจารย์
git remote add upstream https://github.com/SavEe2429/git-practice.git""",
            },
            {
                "heading": "LAB-0003 (ขั้นตอนที่ 2/2): ติดตั้ง VS Code Extensions, Pre-cache ESP32 และตรวจเครื่อง",
                "desc": "เปิดโฟลเดอร์ <code>workshop/</code> ใน VS Code กด <strong>Install Recommended Extensions</strong> (ติดตั้งครบ 2 ตัวคือ <code>platformio.platformio-ide</code> และ <code>github.vscode-pull-request-github</code> — ไม่ต้องลงตัวอื่นเพิ่ม) จากนั้นลอง Build 1 รอบเพื่อโหลด Toolchain/Framework ESP32 มารอไว้ และรัน <code>check_env.py</code>",
                "code": """# 1. เปิดโปรเจกต์ใน VS Code (จะขึ้นแจ้งเตือน Recommended Extensions ด้านขวาล่างอัตโนมัติ)
code workshop

# 2. Pre-cache Toolchain + Arduino ESP32 Framework ล่วงหน้า (รันใน Terminal)
pio run -d workshop -e esp32doit-devkit-v1

# 3. ตรวจความพร้อมเครื่องทั้งหมดด้วย check_env.py
uv run exercises/check_env.py""",
            },
        ],
        "expected_output": """$ uv run exercises/check_env.py
=== Pre-Workshop Environment Check ===

[OK] Git: git version 2.54.0.windows.1
[OK] Git identity: Your Name <you@example.com>
[OK] uv: uv 0.11.x
[OK] pre-commit: pre-commit 4.x.x
[OK] GitHub CLI: gh version 2.x.x
[OK] PlatformIO: PlatformIO Core, version 6.x.x
[OK] C/C++ Compiler (สำหรับ pio test -e native): gcc ...
============================================
พร้อมเข้าเรียน Workshop แล้ว!""",
        "results": [
            "LAB-0001: ผลลัพธ์ของ <code>git --version</code>, <code>uv --version</code>, <code>pre-commit --version</code>, <code>pio --version</code>",
            "LAB-0003: ผลลัพธ์จริงจาก <code>uv run exercises/check_env.py</code> (ครบทุกเครื่องมือหรือไม่)",
        ],
        "questions": [
            "Q1: เหตุใดเราจึงควรรัน <code>pio run</code> และติดตั้ง CLI Tools ให้จบตั้งแต่ Lab 00 ก่อนเข้าเรียน Lab 01–06?",
            "Q2: หากใช้เครื่องคอมพิวเตอร์ส่วนกลางของมหาวิทยาลัย เหตุใดจึงควรใช้ <code>git config --local</code> และกด Sign Out ออกจากบัญชี GitHub/VS Code เมื่อเลิกใช้งาน?",
        ],
        "exercise": {
            "code": "LAB-0004",
            "desc": "รันสคริปต์ตรวจสภาพแวดล้อมให้ครบและบันทึกหลักฐานว่าเครื่องพร้อมเข้าเรียน Lab 01 แล้ว",
            "snippet": """uv run exercises/check_env.py
pio --version && pre-commit --version""",
        },
        "screenshots": [
            ("../images/term-00-check-env.png", "ผลลัพธ์จริงจากการรัน uv run exercises/check_env.py ตรวจสอบความพร้อมเครื่อง"),
        ],
    },
    {
        "slug": "LAB01-Linear_Git_Rebase",
        "title": "Lab 01: Linear Git (Rebase), Fork Workflow &amp; Conventional Commits",
        "objectives": [
            "เรียนรู้การทำงานแบบ Fork &amp; Branch Workflow เพื่อแยกพื้นที่พัฒนาและทำงานร่วมกันบน Repository โดยไม่เขียนทับกัน",
            "เรียนรู้การรักษาประวัติ Commit บน <code>main</code> ให้เป็นเส้นตรง (Linear History) ด้วย <code>git rebase</code> และเขียน Conventional Commits",
        ],
        "outcomes": [
            "ตรวจสอบสถานะ Fork / Remote และใช้งานโปรเจกต์ ESP32 PlatformIO ที่เตรียมไว้จาก Lab 00 ได้ถูกต้อง",
            "แตก Branch <code>feature/*</code> จาก <code>main</code>, Commit ตามมาตรฐาน, และ Rebase ให้ทัน <code>origin/main</code> ได้",
            "ตรวจสอบประวัติด้วย <code>git log --graph --oneline</code> แล้วเห็นโครงสร้างเส้นตรง",
        ],
        "tools": [
            "เครื่องมือทั้งหมดติดตั้งและผ่านการตรวจจาก <strong>Lab 00</strong> เรียบร้อยแล้ว (Git CLI, <code>uv</code>, <code>pio</code>, Fork &amp; Clone ในเครื่อง)",
            "Repository ต้นทาง: <code>https://github.com/SavEe2429/git-practice</code>",
            "วิดีโอประกอบ: <code>videos/01-gitflow-branching.mp4</code>",
        ],
        "experiments": [
            ("LAB-0101", "(remote-check) ตรวจสอบ Remote <code>origin</code> (Fork ของตัวเอง) กับ <code>upstream</code> (Repo อาจารย์) ที่เตรียมไว้จาก Lab 00"),
            ("LAB-0102", "(branch &amp; rebase) แตก <code>feature/fast-blink</code> จาก <code>main</code>, แก้โค้ดใน <code>workshop/</code>, Commit แบบ Conventional Commits และฝึก <code>git rebase</code>"),
        ],
        "details": [
            {
                "heading": "LAB-0101: ตรวจสอบ Remote ของ Fork และสถานะ Repository ก่อนเริ่มแก้โค้ด",
                "desc": "ใช้โปรเจกต์ที่ Fork และ Clone มาแล้วใน Lab 00 (หากยังไม่ได้ทำ ให้กลับไปดูขั้นตอนกด <code>[1] Fork</code> -&gt; <code>[2] &lt;&gt; Code</code> ใน Lab 00 ก่อน) แล้วตรวจว่า <code>origin</code> ชี้ไปที่ Fork ของตัวเอง และ <code>upstream</code> ชี้ไปที่ต้นทาง",
                "images": [
                    ("../images/anno-01-repo-fork.png", "หน้าเว็บ GitHub (อ้างอิงจาก Lab 00): [1] Fork เป็นบัญชีตัวเอง -> [2] <> Code คัดลอก URL"),
                ],
                "code": """# 1. เข้าโฟลเดอร์โปรเจกต์ที่ Clone มาใน Lab 00 แล้วตรวจ Remote
cd git-practice
git remote -v

# 2. อัปเดต main ให้ตรงล่าสุดและเช็กประวัติ Commit ปัจจุบัน
git switch main
git log --oneline -n 5""",
            },
            {
                "heading": "LAB-0102: แตก Feature Branch, Conventional Commit และ Rebase",
                "desc": "สร้าง Branch ใหม่สำหรับทำงานแทนการแก้บน <code>main</code> โดยตรง จากนั้น Commit ตามรูปแบบ <code>&lt;type&gt;(scope): &lt;summary&gt;</code> และฝึกดึงฐานล่าสุดด้วย <code>git rebase</code>",
                "code": """# 1. แตก branch ใหม่จาก main
git checkout -b feature/fast-blink main

# 2. แก้ไฟล์ workshop/src/main.cpp แล้ว Stage + Commit แบบ Conventional Commits:
git add workshop/src/main.cpp
git commit -m "feat(blink): support fast blink interval"

# 3. อัปเดตฐานให้ทัน main โดยไม่สร้าง merge commit (หาก main ยังไม่ขยับจะขึ้น up to date)
git fetch origin
git rebase origin/main
git log --graph --oneline -n 6""",
            },
        ],
        "expected_output": """$ git remote -v
origin    https://github.com/<your-username>/git-practice.git (fetch)
origin    https://github.com/<your-username>/git-practice.git (push)
upstream  https://github.com/SavEe2429/git-practice.git (fetch)
upstream  https://github.com/SavEe2429/git-practice.git (push)

$ git log --graph --oneline -n 4
* 9a4c21e (HEAD -> feature/fast-blink) feat(blink): support fast blink interval
* 7b3e10a (origin/main, main) docs: update lab guides
* 4d2f81b ci: add native test and esp32 build workflow
* 1c0a9d2 chore: initial workshop structure""",
        "results": [
            "LAB-0101: ผลลัพธ์จากการรัน <code>git remote -v</code> (แสดง <code>origin</code> และ <code>upstream</code>)",
            "LAB-0102: ผลลัพธ์จาก <code>git log --graph --oneline -n 6</code> (เป็นเส้นตรงหรือไม่)",
        ],
        "questions": [
            "Q1: การทำงานแบบ Fork Workflow (แยก <code>origin</code> ออกจาก <code>upstream</code>) มีข้อดีทางวิศวกรรมอย่างไรเมื่อเทียบกับการ Push เข้า Repo หลักโดยตรง?",
            "Q2: การใช้ <code>git rebase</code> แตกต่างจาก <code>git merge</code> อย่างไรในหน้าตาของ <code>git log --graph</code>?",
            "Q3: โครงสร้างของ Conventional Commit (เช่น <code>feat(blink): ...</code>) มีประโยชน์ต่อการทำงานเป็นทีมอย่างไร?",
        ],
        "exercise": {
            "code": "LAB-0103",
            "desc": "ทดลองเพิ่มฟังก์ชันใหม่ใน <code>workshop/lib/blink_math/</code> บน branch <code>feature/slow-blink</code> แล้ว Commit และตรวจผ่านด้วย <code>verify.py</code>",
            "snippet": """git checkout -b feature/slow-blink main
# เพิ่มโค้ดและ Commit ด้วย prefix ที่ถูกต้อง (feat:, fix:, docs:)
uv run exercises/verify.py --module 1""",
        },
        "screenshots": [
            ("../images/term-01-git-log.png", "ผลลัพธ์จริงจาก git log --graph --oneline: ประวัติบน Branch เรียงเป็นเส้นตรง"),
        ],
    },
    {
        "slug": "LAB02-Issue_Forms_PR_Protection",
        "title": "Lab 02: YAML Issue Forms, Pull Request (Rebase) &amp; Branch Protection",
        "objectives": [
            "เรียนรู้การสร้างแบบฟอร์มแจ้งปัญหาและขอฟีเจอร์ด้วยไฟล์ YAML (<code>.github/ISSUE_TEMPLATE/*.yml</code>) และ PR Template",
            "เรียนรู้การเปิด Pull Request, ทำ Code Review, ใช้ Rebase and Merge และตั้ง Branch Protection บน <code>main</code>",
        ],
        "outcomes": [
            "สร้างและใช้งาน <code>bug_report.yml</code>, <code>feature_request.yml</code>, <code>config.yml</code> และ <code>pull_request_template.md</code> ได้",
            "เปิด Pull Request เข้า <code>main</code>, ตรวจ Code Review และ Merge แบบ Rebase พร้อมลบ Branch อัตโนมัติได้",
            "ตั้งค่า Branch Protection Rules เพื่อป้องกันการ Push ตรงเข้า <code>main</code> ได้",
        ],
        "tools": [
            "GitHub Web (เปิด Issue &amp; PR) และ <strong>VS Code Extension: GitHub Pull Requests</strong> (ติดตั้งไว้แล้วจาก <strong>Lab 00</strong>)",
            "ไฟล์ปลายทาง: <code>.github/ISSUE_TEMPLATE/*.yml</code> และ <code>.github/pull_request_template.md</code>",
            "วิดีโอประกอบ: <code>videos/02-pull-request-review.mp4</code>",
        ],
        "experiments": [
            ("LAB-0201", "(issue-yml) ตั้งค่า Issue Forms (<code>.github/ISSUE_TEMPLATE/*.yml</code>) แล้ว Merge เข้า <code>main</code> บน Fork เพื่อเปิดใช้งานฟอร์มบนเว็บ GitHub"),
            ("LAB-0202", "(web-issue) ทดลองกดเปิด Issue จริงบนหน้าเว็บ GitHub (แท็บ <strong>Issues -&gt; New issue</strong>) ด้วยฟอร์มที่สร้างไว้"),
            ("LAB-0203", "(pr-2-ways) Push branch <code>feature/fast-blink</code> แล้วเปิด/Merge PR แบบ <strong>Rebase and merge</strong> (เลือกทำได้ทั้งผ่าน<strong>เว็บ GitHub</strong> และ <strong>VS Code Extension</strong>) พร้อมตั้ง Branch Protection และ <strong>Logout</strong> ออกจาก VS Code เมื่อจบ Lab"),
        ],
        "details": [
            {
                "heading": "LAB-0201 (ส่วนที่ 1/2): bug_report.yml — ส่วนหัวฟอร์ม (Metadata) & ช่องระบุเวอร์ชัน/สภาพแวดล้อม",
                "desc": "กำหนดชื่อฟอร์ม, Prefix หัวข้อ <code>[Bug]: </code>, Label อัตโนมัติ และช่องรับข้อมูล 2 ตัวแรก (<code>input</code> สำหรับเลขเวอร์ชัน และ <code>dropdown</code> สำหรับเลือกรุ่นบอร์ด/CI)",
                "code": """name: Bug Report (แจ้งบั๊ก Firmware)
description: รายงานปัญหาที่พบในโปรเจกต์ ESP32 DOIT DevKit v1
title: "[Bug]: "
labels: ["bug", "triage"]
body:
  - type: markdown
    attributes:
      value: กรุณากรอกข้อมูลให้ครบถ้วนเพื่อให้ทีมจำลองปัญหาและแก้ไขได้เร็วขึ้นครับ

  - type: input
    id: version
    attributes:
      label: เวอร์ชันเฟิร์มแวร์ / Tag หรือ Commit
      description: ระบุ Tag (เช่น v1.0.0) หรือเลข Commit ที่พบปัญหา
      placeholder: v1.0.0
    validations: { required: true }

  - type: dropdown
    id: environment
    attributes:
      label: สภาพแวดล้อมที่พบปัญหา
      options:
        - DOIT ESP32 DevKit v1 (Hardware จริง)
        - PlatformIO Native Test ([env:native])
        - GitHub Actions CI
    validations: { required: true }""",
            },
            {
                "heading": "LAB-0201 (ส่วนที่ 2/2): bug_report.yml — ช่องอธิบายอาการ (textarea) & ยืนยัน (checkboxes)",
                "desc": "ต่อท้ายลงใน <code>body:</code> ของไฟล์ <code>.github/ISSUE_TEMPLATE/bug_report.yml</code> เพื่อบังคับให้กรอกขั้นตอนทำซ้ำและติ๊กยืนยันก่อน Submit",
                "code": """  - type: textarea
    id: description
    attributes:
      label: อาการที่พบ & ขั้นตอนการทำซ้ำ (Steps to Reproduce)
      placeholder: |
        1. รันคำสั่ง...
        2. ผลลัพธ์ที่เกิดขึ้น...
        3. ผลลัพธ์ที่คาดหวัง...
    validations: { required: true }

  - type: checkboxes
    id: checklist
    attributes:
      label: ยืนยันเบื้องต้น
      options:
        - label: ทดสอบบน branch main หรือ release ล่าสุดแล้ว
          required: true""",
            },
            {
                "heading": "LAB-0202 (ส่วนที่ 1/2): feature_request.yml — ฟอร์มขอฟีเจอร์ใหม่ (Why / How / Target Branch)",
                "desc": "วางลงใน <code>.github/ISSUE_TEMPLATE/feature_request.yml</code> เพื่อให้ผู้เสนอฟีเจอร์อธิบายปัญหา (<code>problem</code>), แนวทางแก้ (<code>solution</code>) และเลือก Branch เป้าหมาย",
                "code": """name: Feature Request (ขอฟีเจอร์ใหม่)
description: เสนอฟีเจอร์ใหม่หรือการปรับปรุงสำหรับโปรเจกต์ ESP32
title: "[Feat]: "
labels: ["enhancement"]
body:
  - type: textarea
    id: problem
    attributes:
      label: ปัญหาหรือความต้องการ (Why)
      placeholder: เช่น ต้องการปรับความถี่ไฟกระพริบตามค่า Input
    validations: { required: true }

  - type: textarea
    id: solution
    attributes:
      label: แนวทางที่เสนอ (How)
      placeholder: เพิ่มฟังก์ชันใน lib/blink_math/ และเขียน Unit Test รองรับ
    validations: { required: true }

  - type: dropdown
    id: target_branch
    attributes:
      label: Branch เป้าหมาย (Linear History + Rebase)
      options:
        - main (PR + Rebase and merge)
        - release/v* (เฉพาะแก้บั๊กก่อนปล่อยเวอร์ชัน)
      default: 0""",
            },
            {
                "heading": "LAB-0202 (ส่วนที่ 2/2): config.yml — ปิด Blank Issue และนำไฟล์ขึ้น main บน Fork",
                "desc": "วางลงใน <code>.github/ISSUE_TEMPLATE/config.yml</code> เพื่อบังคับใช้ฟอร์มมาตรฐาน แล้ว Commit/PR เข้า <code>main</code> บน Fork ก่อน (GitHub จะอ่าน Issue Template จาก <code>main</code> เท่านั้น)",
                "code": """# วางลงใน .github/ISSUE_TEMPLATE/config.yml
blank_issues_enabled: false
contact_links:
  - name: คู่มือ Workshop (Docs)
    url: https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms
    about: เอกสารอ้างอิงไวยากรณ์ YAML สำหรับ GitHub Issue Forms""",
                "images": [
                    ("../images/gh-02-issue-templates.png", "ตรวจสอบให้แน่ใจว่าทั้ง 3 ไฟล์ใน .github/ISSUE_TEMPLATE/ ถูก Merge เข้า main บน Fork แล้ว"),
                ],
            },
            {
                "heading": "LAB-0203 (ขั้นตอนที่ 1/3): กดเปิด Issue จริงบนหน้าเว็บ GitHub",
                "desc": "เข้าหน้า Fork ของตัวเองบนเว็บ GitHub -> <code>[1]</code> คลิกแท็บ <strong>Issues</strong> -> <code>[2]</code> กดปุ่มเขียว <strong>New issue</strong> -> เลือกฟอร์ม Feature Request / Bug Report แล้วกรอกจนได้เลข Issue (เช่น <code>#1</code> หรือ <code>#2</code>)",
                "images": [
                    ("../images/anno-02-issues.png", "กดตามลำดับ: [1] คลิกแท็บ Issues -> [2] กดปุ่ม New issue เพื่อเลือก YAML Form"),
                    ("../images/anno-02-issue-detail.png", "หน้าจอหลังสร้าง Issue: [1] จำเลข Issue (เช่น #2 หรือ #1) และ [2] ตรวจ Labels ที่ติดอัตโนมัติ"),
                ],
            },
            {
                "heading": "LAB-0203 (ขั้นตอนที่ 2/3): เปิดและ Merge PR — วิธีที่ 1 ผ่านเว็บ GitHub โดยตรง",
                "desc": "รัน <code>git push -u origin feature/fast-blink</code> จากนั้นบนเว็บ GitHub: <code>[1]</code> เข้าแท็บ <strong>Pull requests</strong> -> <code>[2]</code> กด <strong>New pull request</strong> (หรือปุ่ม Compare & pull request) -> ตั้ง <code>[1] base: main &lt;- compare: feature/...</code> -> ใส่ <code>Closes #1</code> ในช่องคำอธิบาย -> กด <code>[2] Create pull request</code> -> รอ CI แล้วกด <strong>Rebase and merge</strong> + <strong>Delete branch</strong>",
                "images": [
                    ("../images/anno-02-pulls.png", "บนหน้า Fork: [1] คลิกแท็บ Pull requests -> [2] กดปุ่ม New pull request"),
                    ("../images/anno-02-compare.png", "หน้า Compare: [1] เลือก base: main <- compare: feature/... -> ใส่ Closes #<เลข> -> [2] กด Create pull request"),
                ],
            },
            {
                "heading": "LAB-0203 (ขั้นตอนที่ 3/3): เปิด PR — วิธีที่ 2 ผ่าน VS Code Extension + บังคับ Logout และตั้ง Branch Protection",
                "desc": "ใน VS Code: <code>[1]</code> เปิดแถบ <strong>GitHub Pull Requests</strong> (ติดตั้งไว้แล้วจาก Lab 00) -&gt; Sign in with GitHub -&gt; Create Pull Request (ตั้ง Base = <code>main</code>, ใส่ <code>Closes #1</code>) -&gt; Merge แบบ Rebase <strong>และเมื่อจบ Lab บนเครื่องห้องปฏิบัติการมหาวิทยาลัย ต้องกด Accounts (มุมซ้ายล่าง VS Code) -&gt; Sign Out (Logout) ทุกครั้ง!</strong> จากนั้นตั้ง Branch Protection ใน Settings -&gt; Branches (<code>[x] Require a pull request</code> และ <code>[x] Require linear history</code>)",
                "images": [
                    ("../images/anno-02-vscode-pr.png", "วิธีที่ 2: [1] เปิด GitHub Pull Requests -> Sign in -> Create PR -> จบ Lab ต้องกด Accounts -> Sign Out ทุกครั้ง"),
                ],
            },
        ],
        "expected_output": """# บนหน้าเว็บ GitHub หลัง Merge PR ด้วย Rebase and merge:
✓ Merged 1 commit into main from feature/fast-blink
✓ Issue #1 closed automatically (via "Closes #1")
✓ Branch feature/fast-blink deleted

# เมื่อตรวจสอบผ่าน VS Code Extension หลังใช้งานเสร็จ:
VS Code Accounts -> <your-username> (GitHub) -> Sign Out (เรียบร้อย)""",
        "results": [
            "LAB-0201: สังเกตหน้าจอ New Issue บนเว็บ GitHub หลัง Merge ไฟล์ <code>.yml</code> เข้า <code>main</code>",
            "LAB-0202: เปรียบเทียบขั้นตอนเปิด PR ผ่าน<strong>เว็บ GitHub</strong> กับ <strong>VS Code Extension</strong> และการ Logout",
        ],
        "questions": [
            "Q1: การใช้ Issue Form แบบ <code>.yml</code> ดีกว่าการปล่อยให้กรอก Issue แบบข้อความเปล่าอย่างไร?",
            "Q2: ตัวเลือก <strong>Require linear history</strong> ใน Branch Protection ช่วยป้องกันอะไร และเหตุใดจึงควร Sign Out ออกจาก GitHub ใน VS Code หลังเลิกใช้งานเครื่องส่วนกลาง?",
            "Q3: ทำไมหลัง Merge PR เข้า <code>main</code> แล้วจึงควรลบ Branch ย่อยทิ้งทันที?",
        ],
        "exercise": {
            "code": "LAB-0204",
            "desc": "เปิด Issue 1 รายการด้วยฟอร์ม <code>feature_request.yml</code> บนหน้าเว็บ GitHub จากนั้นเปิด PR (ผ่านเว็บหรือ VS Code Extension) พร้อมใส่ <code>Closes #1</code> เพื่อปิด Issue แล้วตรวจด้วย <code>verify.py</code>",
            "snippet": """# ในรายละเอียด PR (ผ่านเว็บ GitHub หรือ VS Code Extension) ให้ใส่: Closes #1
# หากใช้เครื่องห้องแล็บ อย่าลืม VS Code Accounts -> Sign Out หลังทำเสร็จ!
uv run exercises/verify.py --module 2""",
        },
        "screenshots": [
            ("../images/anno-02-pr-detail.png", "ผลลัพธ์หลังเปิด PR และ Merge: [1] ตรวจ Checks ผ่านสีเขียว -> [2] กด Rebase and merge จนขึ้นสถานะ Merged"),
        ],
    },
    {
        "slug": "LAB03-Pre_commit_Hooks",
        "title": "Lab 03: Pre-commit Hooks (Quality Gate ก่อน Commit)",
        "objectives": [
            "เรียนรู้การติดตั้งและใช้งาน Pre-commit Hooks เพื่อตรวจคุณภาพโค้ดในเครื่องก่อนเข้า Git History",
            "เข้าใจการทำงานของ <code>clang-format</code> (จัดฟอร์แมต C/C++) และ <code>conventional-pre-commit</code> (ตรวจ Commit Message)",
        ],
        "outcomes": [
            "ติดตั้ง <code>pre-commit</code> และเปิดใช้งาน Git Hooks ทั้ง <code>pre-commit</code> และ <code>commit-msg</code> ได้",
            "แก้ไขปัญหาเมื่อ Hook บล็อก Commit ที่จัดฟอร์แมตผิดหรือตั้งชื่อ Commit ไม่ตรงมาตรฐานได้",
        ],
        "tools": [
            "<code>pre-commit</code> CLI (ติดตั้งไว้แล้วจาก <strong>Lab 00</strong>)",
            "ไฟล์ปลายทาง: <code>.pre-commit-config.yaml</code> และ <code>.clang-format</code>",
            "วิดีโอประกอบ: <code>videos/03-pre-commit-hooks.mp4</code>",
        ],
        "experiments": [
            ("LAB-0301", "(config &amp; hooks) ก๊อปวาง <code>.pre-commit-config.yaml</code> และเปิดใช้งาน Git Hook ทั้ง 2 ประเภท (<code>pre-commit</code> และ <code>commit-msg</code>)"),
            ("LAB-0302", "(break-fix) ทดลองจัดฟอร์แมตโค้ดให้เพี้ยน + พิมพ์ Commit Message ผิด เพื่อสังเกตการทำงานของ Hook"),
        ],
        "details": [
            {
                "heading": "LAB-0301 (ส่วนที่ 1/3): .pre-commit-config.yaml — Hook ตรวจไฟล์พื้นฐาน (pre-commit-hooks)",
                "desc": "วางที่ root ของ Repo เพื่อลบช่องว่างท้ายบรรทัด (<code>trailing-whitespace</code>), จัดบรรทัดท้ายไฟล์, ตรวจไวยากรณ์ YAML และกันเผลอ Commit ไฟล์ขนาดใหญ่เกิน 500 KB",
                "code": """repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v6.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=500']""",
            },
            {
                "heading": "LAB-0301 (ส่วนที่ 2/3): .pre-commit-config.yaml — จัด Format C/C++ อัตโนมัติ (clang-format)",
                "desc": "ต่อท้ายลงใน <code>repos:</code> โดยอ้างอิงกติกาจากไฟล์ <code>.clang-format</code> ที่มีใน Repo แล้ว (Google Style, IndentWidth: 2, ColumnLimit: 100)",
                "code": """  - repo: https://github.com/pre-commit/mirrors-clang-format
    rev: v23.1.5
    hooks:
      - id: clang-format
        types_or: [c++, c]""",
            },
            {
                "heading": "LAB-0301 (ส่วนที่ 3/3): .pre-commit-config.yaml — ตรวจ Commit Message (stage: commit-msg)",
                "desc": "เพิ่ม Hook ตรวจหัวข้อ Commit ใน Stage <code>commit-msg</code> เพื่อบังคับให้ใช้ Type ตามมาตรฐาน Conventional Commits ก่อนบันทึกลง History",
                "code": """  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: v4.5.0
    hooks:
      - id: conventional-pre-commit
        stages: [commit-msg]
        args: [feat, fix, docs, style, refactor, test, ci, chore, build]""",
            },
            {
                "heading": "LAB-0302: ผูก Git Hook ทั้ง 2 Stage เข้า Repo และทดสอบ Break-Fix (Terminal)",
                "desc": "ใช้เครื่องมือ <code>pre-commit</code> ที่ลงไว้แล้วจาก Lab 00 เพื่อผูก Hook เข้ากับ <code>.git/hooks/</code> ของโปรเจกต์ แล้วทดลองแก้ช่องว่างใน <code>workshop/src/main.cpp</code> ให้เพี้ยนเพื่อดู Hook ทำงานจริง",
                "code": """# 1. ผูก hook ทั้ง 2 stage เข้ากับ .git/hooks/ (ตัว pre-commit CLI ลงไว้แล้วใน Lab 00)
pre-commit install
pre-commit install --hook-type commit-msg

# 2. รันตรวจทุกไฟล์ทันที:
pre-commit run --all-files

# 3. เปิดไฟล์ workshop/src/main.cpp แก้ช่องว่าง/ย่อหน้าให้เพี้ยน แล้วลอง Commit ผิดกฎ:
git add workshop/src/main.cpp
git commit -m "bad commit message"

# 4. clang-format จะจัดหน้าให้ใหม่ -> สั่ง git add อีกรอบแล้ว Commit ด้วย prefix ที่ถูกต้อง:
git add workshop/src/main.cpp
git commit -m "style: format main.cpp with clang-format" """,
            },
        ],
        "expected_output": """$ pre-commit run --all-files
trim trailing whitespace.................................................Passed
fix end of files.........................................................Passed
check yaml...............................................................Passed
check for added large files..............................................Passed
clang-format.............................................................Passed""",
        "results": [
            "LAB-0301: ผลลัพธ์จากการรัน <code>pre-commit run --all-files</code>",
            "LAB-0302: ข้อความแจ้งเตือนที่พบเมื่อลอง Commit ด้วยข้อความ <code>\"bad commit message\"</code>",
        ],
        "questions": [
            "Q1: เหตุใดเมื่อ <code>clang-format</code> ขึ้น Failed ในครั้งแรก เราจึงต้องรัน <code>git add</code> ใหม่อีกครั้งก่อน Commit?",
            "Q2: การใช้ Pre-commit ในเครื่องช่วยลดภาระของ GitHub Actions CI ได้อย่างไร?",
        ],
        "exercise": {
            "code": "LAB-0303",
            "desc": "ตรวจสอบ Hook ทั้งหมดในเครื่องด้วย <code>pre-commit run --all-files</code> และตรวจผ่านด้วย <code>verify.py</code>",
            "snippet": """pre-commit run --all-files
uv run exercises/verify.py --module 3""",
        },
        "screenshots": [
            ("../images/term-02-pre-commit.png", "ผลลัพธ์จริงของการรัน pre-commit run --all-files ผ่านทุก Hook"),
        ],
    },
    {
        "slug": "LAB04-PlatformIO_Unit_Testing",
        "title": "Lab 04: PlatformIO Unit Testing (Native Unity &amp; ESP32 Structure)",
        "objectives": [
            "เรียนรู้การแยก Pure C++ Logic (<code>lib/blink_math/</code>) ออกจากโค้ดฮาร์ดแวร์ (<code>Arduino.h</code>) เพื่อให้ทดสอบได้เร็ว",
            "เรียนรู้การเขียน Unit Test ด้วย Unity Framework และรันบน <code>[env:native]</code> รวมถึงโครงสร้าง Test สำหรับบอร์ด ESP32 จริง",
        ],
        "outcomes": [
            "ตั้งค่า <code>platformio.ini</code> ให้รองรับทั้ง <code>[env:esp32doit-devkit-v1]</code> และ <code>[env:native]</code> ได้",
            "เขียน Test Cases ด้วย <code>TEST_ASSERT_EQUAL_INT</code> / <code>TEST_ASSERT_EQUAL_UINT8</code> และรัน <code>pio test -e native</code> ผ่านได้",
        ],
        "tools": [
            "PlatformIO IDE / <code>pio</code> และ C/C++ Compiler (<code>gcc/g++</code>) ที่ติดตั้งและ pre-cache ไว้แล้วจาก <strong>Lab 00</strong> (หากเครื่องใดไม่ได้ลง <code>gcc</code> ในเครื่อง ให้รัน Build ESP32 ในเครื่องแล้วดูผล <code>[env:native]</code> บน Cloud CI ใน Lab 05 แทนได้)",
            "ไฟล์ปลายทาง: <code>workshop/platformio.ini</code>, <code>workshop/test/test_native/test_main.cpp</code>, <code>workshop/test/test_esp32/test_hardware.cpp</code>",
            "วิดีโอประกอบ: <code>videos/04-platformio-unit-testing.mp4</code>",
        ],
        "experiments": [
            ("LAB-0401", "(native-test) ก๊อปวางตั้งค่า <code>workshop/platformio.ini</code> และเขียน Unit Test ครบ 4 ฟังก์ชันใน <code>test_main.cpp</code>"),
            ("LAB-0402", "(esp32-build) ศึกษา <code>test_hardware.cpp</code> และรัน <code>pio test -e native -v</code> เทียบกับ <code>pio run -e esp32doit-devkit-v1</code>"),
        ],
        "details": [
            {
                "heading": "LAB-0401: ตั้งค่า Dual Environment ใน workshop/platformio.ini",
                "desc": "แยก Environment สำหรับบอร์ดจริง (<code>esp32doit-devkit-v1</code>) ออกจาก Host PC Test (<code>native</code>) โดยใส่ <code>test_build_src = no</code> เพื่อไม่ให้ดึง <code>main.cpp</code> ที่มี <code>&lt;Arduino.h&gt;</code> มาคอมไพล์ปะปน",
                "code": """[env:esp32doit-devkit-v1]
platform = espressif32
board = esp32doit-devkit-v1
framework = arduino
monitor_speed = 115200
test_filter = test_esp32

[env:native]
platform = native
test_build_src = no
test_filter = test_native""",
            },
            {
                "heading": "LAB-0402 (ส่วนที่ 1/2): test_main.cpp — ส่วนประกาศ Test Cases สำหรับ Pure Logic (blink_math)",
                "desc": "นำเข้า <code>&lt;unity.h&gt;</code> และ <code>blink_math.h</code> แล้วเขียนฟังก์ชันทดสอบทั้งกรณีปกติและค่าขอบเขตของ <code>add_numbers</code>, <code>clamp_interval</code>, <code>next_led_state</code> และ <code>calculate_cycle_ms</code>",
                "code": """#include <unity.h>
#include "blink_math.h"

void setUp(void) {}
void tearDown(void) {}

void test_add_numbers_positive(void) {
  TEST_ASSERT_EQUAL_INT(5, blink_math::add_numbers(2, 3));
  TEST_ASSERT_EQUAL_INT(0, blink_math::add_numbers(-4, 4));
}

void test_clamp_interval_bounds(void) {
  TEST_ASSERT_EQUAL_INT(100, blink_math::clamp_interval(20));
  TEST_ASSERT_EQUAL_INT(500, blink_math::clamp_interval(500));
  TEST_ASSERT_EQUAL_INT(5000, blink_math::clamp_interval(9999));
}

void test_next_led_state_toggles(void) {
  TEST_ASSERT_EQUAL_UINT8(1, blink_math::next_led_state(0));
  TEST_ASSERT_EQUAL_UINT8(0, blink_math::next_led_state(1));
}

void test_calculate_cycle_ms(void) {
  TEST_ASSERT_EQUAL_INT(1000, blink_math::calculate_cycle_ms(400, 600));
  TEST_ASSERT_EQUAL_INT(100, blink_math::calculate_cycle_ms(10, 10));
}""",
            },
            {
                "heading": "LAB-0402 (ส่วนที่ 2/2): test_main.cpp — ฟังก์ชัน main() สั่งรัน Test Runner",
                "desc": "ต่อท้ายลงใน <code>workshop/test/test_native/test_main.cpp</code> เพื่อเปิด Suite ด้วย <code>UNITY_BEGIN()</code>, เรียก <code>RUN_TEST(...)</code> ครบทั้ง 4 ฟังก์ชัน แล้วคืนค่า Exit Code ด้วย <code>UNITY_END()</code>",
                "code": """int main(int argc, char** argv) {
  UNITY_BEGIN();
  RUN_TEST(test_add_numbers_positive);
  RUN_TEST(test_clamp_interval_bounds);
  RUN_TEST(test_next_led_state_toggles);
  RUN_TEST(test_calculate_cycle_ms);
  return UNITY_END();
}""",
            },
            {
                "heading": "LAB-0403: ศึกษาไฟล์ test_hardware.cpp (มีให้ใน Repo แล้ว) และคำสั่งรัน Test/Build",
                "desc": "เปรียบเทียบไฟล์ <code>workshop/test/test_esp32/test_hardware.cpp</code> ที่ใช้ <code>setup()</code>/<code>loop()</code> บนบอร์ดจริง แล้วลองรันคำสั่ง Build และ Native Test ใน Terminal",
                "code": """// --- คำสั่งรันใน Terminal (เครื่องมือทั้งหมดลงไว้แล้วใน Lab 00) ---
// 1. รัน Native Unit Test บน Host PC:
pio test -d workshop -e native -v

// 2. Build เฟิร์มแวร์ .bin:
pio run -d workshop -e esp32doit-devkit-v1

// 3. ทดสอบบนบอร์ด ESP32 จริง (เมื่อต่อบอร์ดผ่าน USB):
pio test -d workshop -e esp32doit-devkit-v1""",
            },
        ],
        "expected_output": """$ pio test -d workshop -e native -v
test/test_native/test_main.cpp:30: test_add_numbers_positive    [PASSED]
test/test_native/test_main.cpp:31: test_clamp_interval_bounds   [PASSED]
test/test_native/test_main.cpp:32: test_next_led_state_toggles  [PASSED]
test/test_native/test_main.cpp:33: test_calculate_cycle_ms      [PASSED]
----------------------- 4 Tests 0 Failures 0 Ignored -----------------------

$ pio run -d workshop -e esp32doit-devkit-v1
RAM:   [=         ]   6.x% (used ~21 KB from 327680 bytes)
Flash: [==        ]  20.x% (used ~270 KB from 1310720 bytes)
========================= [SUCCESS] Took ~15s =========================""",
        "results": [
            "LAB-0401: จำนวน Test Cases ที่รันผ่านบน <code>[env:native]</code> และเวลาที่ใช้",
            "LAB-0402: ขนาด RAM และ Flash ที่ใช้จากการ Build <code>esp32doit-devkit-v1</code>",
        ],
        "questions": [
            "Q1: ทำไมเราต้องแยกฟังก์ชันคำนวณไว้ใน <code>lib/blink_math/</code> โดยไม่ใส่ <code>#include &lt;Arduino.h&gt;</code>?",
            "Q2: การตั้งค่า <code>test_build_src = no</code> ใน <code>[env:native]</code> มีไว้เพื่ออะไร?",
        ],
        "exercise": {
            "code": "LAB-0404",
            "desc": "เขียน Test Cases ใน <code>workshop/test/test_native/test_main.cpp</code> ให้ครบทั้ง 4 ฟังก์ชันของ <code>blink_math</code> แล้วรัน <code>verify.py</code>",
            "snippet": """pio test -d workshop -e native -v
uv run exercises/verify.py --module 4""",
        },
        "screenshots": [
            ("../images/term-03-pio-build.png", "ผลลัพธ์จริงของการ Build เฟิร์มแวร์สำหรับ esp32doit-devkit-v1"),
        ],
    },
    {
        "slug": "LAB05-GitHub_Actions_CI_YAML",
        "title": "Lab 05: GitHub Actions Continuous Integration (CI) &amp; YAML Deep-Dive",
        "objectives": [
            "เข้าใจโครงสร้างไฟล์ YAML (<code>.github/workflows/ci.yml</code>) และแหล่งค้นหา Actions จาก GitHub Marketplace",
            "ออกแบบ CI Pipeline 3 ขั้นตอน (<code>lint</code> → <code>unit-test</code> → <code>build-esp32</code>) โดยใช้ <code>uv</code> และ Caching",
        ],
        "outcomes": [
            "อธิบายความหมายของ <code>on</code>, <code>defaults.run.working-directory</code>, <code>jobs</code>, <code>needs</code>, <code>uses</code>, <code>with</code>, <code>run</code> ได้",
            "ตรวจสอบผลการรัน CI บนแท็บ GitHub Actions และอ่าน Log เพื่อแก้ไขเมื่อ CI แดงได้",
        ],
        "tools": [
            "GitHub Actions &amp; GitHub Marketplace (<code>https://github.com/marketplace?type=actions</code>)",
            "ไฟล์ปลายทาง: <code>.github/workflows/ci.yml</code>",
            "วิดีโอประกอบ: <code>videos/05-github-actions-ci.mp4</code>",
        ],
        "experiments": [
            ("LAB-0501", "(enable-ci) เปิดใช้งาน GitHub Actions บน Fork ของตัวเองในแท็บ <strong>Actions</strong> แล้วก๊อปวาง <code>.github/workflows/ci.yml</code> ฉบับเต็ม"),
            ("LAB-0502", "(break-fix) ทดลองทำให้ Unit Test พังใน PR เพื่อดู CI แดง จากนั้นแก้ให้กลับมาเขียว"),
        ],
        "details": [
            {
                "heading": "LAB-0501 (ส่วนที่ 1/4): ci.yml — Trigger (on:) & Working Directory (defaults:)",
                "desc": "กำหนดให้ CI ทำงานเมื่อ Push เข้า <code>main</code> / <code>release/**</code> (Branch เตรียม Release Candidate) หรือเปิด PR เข้า <code>main</code> และกำหนดโฟลเดอร์เริ่มต้นในการรันคำสั่งเป็น <code>workshop</code>",
                "code": """name: CI - Lint, Test & Build

on:
  push:
    branches: [main, 'release/**']
  pull_request:
    branches: [main]

defaults:
  run:
    working-directory: workshop""",
            },
            {
                "heading": "LAB-0501 (ส่วนที่ 2/4): ci.yml — Job 1 (lint: ตรวจ Format & YAML ด้วย Pre-commit)",
                "desc": "ขอ Cloud Linux VM (<code>ubuntu-latest</code>), ดึงโค้ดด้วย <code>checkout@v7</code>, ตั้งค่า Python/uv ด้วย <code>setup-uv@v10.3.3</code> และรัน <code>pre-commit/action@v3.0.1</code> ตรวจซ้ำบน Cloud",
                "code": """jobs:
  lint:
    name: Code Format & Lint Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: astral-sh/setup-uv@v10.3.3
        with:
          python-version: '3.12'
          enable-cache: false
      - uses: pre-commit/action@v3.0.1""",
            },
            {
                "heading": "LAB-0501 (ส่วนที่ 3/4): ci.yml — Job 2 (unit-test: รัน Unity Test หลัง lint ผ่าน)",
                "desc": "ใช้ <code>needs: lint</code> เพื่อรอ Job แรกผ่านก่อน แล้ว Cache <code>~/.platformio/.cache</code> ผูก Key กับ <code>platformio.ini</code> ก่อนรัน <code>pio test -e native -v</code>",
                "code": """  unit-test:
    name: Native Unit Tests (Unity)
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v7
      - uses: astral-sh/setup-uv@v10.3.3
        with: { python-version: '3.12', enable-cache: false }
      - uses: actions/cache@v6
        with:
          path: ~/.platformio/.cache
          key: ${{ runner.os }}-pio-native-${{ hashFiles('workshop/platformio.ini') }}
      - run: uv tool install platformio
      - run: pio test -e native -v""",
            },
            {
                "heading": "LAB-0501 (ส่วนที่ 4/4): ci.yml — Job 3 (build-esp32: คอมไพล์ .bin & Upload Artifact)",
                "desc": "รอ <code>needs: unit-test</code> แล้วจึงลอง Build เฟิร์มแวร์จริง <code>esp32doit-devkit-v1</code> และหากเป็น Branch <code>release/**</code> ให้แนบไฟล์ <code>.bin</code> เก็บไว้ตรวจสอบด้วย <code>upload-artifact@v7</code>",
                "code": """  build-esp32:
    name: Build Firmware (esp32doit-devkit-v1)
    runs-on: ubuntu-latest
    needs: unit-test
    steps:
      - uses: actions/checkout@v7
      - uses: astral-sh/setup-uv@v10.3.3
        with: { python-version: '3.12', enable-cache: false }
      - uses: actions/cache@v6
        with:
          path: ~/.platformio
          key: ${{ runner.os }}-pio-esp32-${{ hashFiles('workshop/platformio.ini') }}
      - run: uv tool install platformio
      - run: pio run -e esp32doit-devkit-v1
      - if: startsWith(github.ref, 'refs/heads/release/')
        uses: actions/upload-artifact@v7
        with:
          name: rc-firmware-${{ github.sha }}
          path: |
            workshop/.pio/build/esp32doit-devkit-v1/firmware.bin
            workshop/.pio/build/esp32doit-devkit-v1/bootloader.bin
            workshop/.pio/build/esp32doit-devkit-v1/partitions.bin
          retention-days: 7""",
            },
            {
                "heading": "LAB-0502: เปิดใช้งาน Actions บน Fork และดูผลลัพธ์บนแท็บ Actions / CLI",
                "desc": "บน Fork ของตัวเองให้เข้าแท็บ <strong>Actions</strong> (หากขึ้นแจ้งเตือนให้กดปุ่มสีเขียว <em>I understand my workflows, go ahead and enable them</em>) จากนั้น <code>[1]</code> เลือก Workflow <code>CI - Lint, Test & Build</code> แล้ว <code>[2]</code> คลิกที่ชื่อ Run เพื่อเปิดดูกราฟ",
                "images": [
                    ("../images/anno-05-actions-list.png", "บนแท็บ Actions: [1] เลือก Workflow CI - Lint, Test & Build -> [2] คลิกชื่อ Run เพื่อดูรายละเอียด 3 Jobs"),
                ],
                "code": """# ตรวจสอบ Tag ล่าสุดของ Action และดูรายการ CI Run ผ่าน CLI:
gh api repos/actions/checkout/releases/latest --jq .tag_name
gh run list --workflow ci.yml --limit 3""",
            },
        ],
        "expected_output": """$ gh run list --workflow ci.yml --limit 3
STATUS  TITLE                          WORKFLOW                    BRANCH  ELAPSED
✓       ci: add github actions ci      CI - Lint, Test & Build     main    1m12s
✓       feat(blink): fast blink        CI - Lint, Test & Build     feat    1m08s""",
        "results": [
            "LAB-0501: เวลาที่ใช้ในแต่ละ Job (<code>lint</code>, <code>unit-test</code>, <code>build-esp32</code>) บน GitHub Actions",
            "LAB-0502: อาการที่เกิดขึ้นบนหน้า Pull Request เมื่อ Unit Test ใน CI ไม่ผ่าน",
        ],
        "questions": [
            "Q1: เหตุใดใน <code>ci.yml</code> จึงต้องระบุ <code>defaults: run: working-directory: workshop</code>?",
            "Q2: คีย์เวิร์ด <code>needs: unit-test</code> ใน Job <code>build-esp32</code> ทำหน้าที่อะไร?",
            "Q3: การทำ <code>actions/cache@v6</code> กับโฟลเดอร์ <code>~/.platformio</code> ช่วยเรื่องอะไร?",
        ],
        "exercise": {
            "code": "LAB-0503",
            "desc": "เปิด PR เข้า <code>main</code> บน Fork ของตัวเอง รอให้ Actions ขึ้นสีเขียวครบทั้ง 3 Jobs แล้วตรวจด้วย <code>verify.py</code>",
            "snippet": """gh run list --workflow ci.yml --limit 3
uv run exercises/verify.py --module 5""",
        },
        "screenshots": [
            ("../images/anno-05-actions-graph.png", "ผลลัพธ์หลังคลิก Run: กราฟ 3 Jobs ([1] Lint -> [2] Unit Test -> [3] Build ESP32) ผ่านสีเขียวครบ (คลิกแต่ละกล่องเพื่อดู Log ได้)"),
        ],
    },
    {
        "slug": "LAB06-Release_Tag_and_Firmware_Bin",
        "title": "Lab 06: Automated Release (CD), Tagging &amp; Flashing with esptool",
        "objectives": [
            "เข้าใจความแตกต่างระหว่าง <code>firmware.bin</code> (สำหรับ OTA) กับ <code>merged-firmware.bin</code> (สำหรับ Flash ใหม่ไฟล์เดียวที่ <code>0x0</code>)",
            "เรียนรู้การทำงานของ <code>release.yml</code> เมื่อ Push Tag <code>v*.*.*</code> และการนำไฟล์ไป Flash ลงบอร์ดจริงด้วย <code>esptool</code>",
        ],
        "outcomes": [
            "ปล่อยเวอร์ชันผ่าน <code>git tag -a v1.0.0</code> และสร้าง GitHub Release อัตโนมัติได้",
            "อธิบายวิธีนำไฟล์จาก Release ไป Flash ลงบอร์ด DOIT ESP32 DevKit v1 ได้ทั้งแบบ CLI และเว็บ",
        ],
        "tools": [
            "เครื่องมือ <code>esptool</code> (ติดตั้งไว้แล้วจาก <strong>Lab 00</strong>) หรือเว็บ <code>https://espressif.github.io/esptool-js/</code>",
            "ไฟล์ปลายทาง: <code>.github/workflows/release.yml</code>",
            "วิดีโอประกอบ: <code>videos/06-github-actions-release.mp4</code>",
        ],
        "experiments": [
            ("LAB-0601", "(tag-release) ก๊อปวาง <code>.github/workflows/release.yml</code> ฉบับเต็ม และติด Tag <code>v1.0.0</code> บน <code>main</code>"),
            ("LAB-0602", "(flash-bin) ตรวจสอบไฟล์ Asset ในหน้า GitHub Releases และคำสั่ง Flash ด้วย <code>esptool</code>"),
        ],
        "details": [
            {
                "heading": "LAB-0601 (ส่วนที่ 1/3): release.yml — Trigger เฉพาะ Tag v*.*.* & สิทธิ์เขียน Release",
                "desc": "ตั้งค่าให้ทำงานเฉพาะตอน Push Tag เวอร์ชัน (<code>v1.0.0</code>) และเปิดสิทธิ์ <code>contents: write</code> เพื่อให้ GitHub Actions สร้างหน้า Release และแนบไฟล์ <code>.bin</code> ได้",
                "code": """name: Release Firmware (CD)

on:
  push:
    tags: ['v*.*.*']

permissions:
  contents: write

defaults:
  run:
    working-directory: workshop""",
            },
            {
                "heading": "LAB-0601 (ส่วนที่ 2/3): release.yml — Setup เครื่องมือ, รัน Test & Build Firmware",
                "desc": "ติดตั้ง <code>platformio</code> และ <code>esptool</code> ด้วย <code>uv tool install</code> แล้วรัน <code>pio test -e native</code> ซ้ำอีกครั้งก่อนสั่ง Compile ไฟล์ <code>.bin</code>",
                "code": """jobs:
  release:
    name: Build & Publish ESP32 Release
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: astral-sh/setup-uv@v10.3.3
        with: { python-version: '3.12', enable-cache: false }
      - uses: actions/cache@v6
        with:
          path: ~/.platformio
          key: ${{ runner.os }}-pio-esp32-${{ hashFiles('workshop/platformio.ini') }}
      - run: |
          uv tool install platformio
          uv tool install esptool
      - run: pio test -e native
      - run: pio run -e esp32doit-devkit-v1""",
            },
            {
                "heading": "LAB-0601 (ส่วนที่ 3/3): release.yml — รวม 3 ไฟล์ด้วย esptool merge-bin & สร้าง GitHub Release",
                "desc": "ใช้ <code>esptool merge-bin</code> รวม <code>bootloader.bin</code> (0x1000) + <code>partitions.bin</code> (0x8000) + <code>firmware.bin</code> (0x10000) เป็นไฟล์เดียวที่ Offset <code>0x0</code> แล้วอัปโหลดด้วย <code>softprops/action-gh-release@v3</code>",
                "code": """      - name: Prepare Release Binaries
        shell: bash
        run: |
          mkdir -p dist
          BUILD_DIR=".pio/build/esp32doit-devkit-v1"
          cp "${BUILD_DIR}/firmware.bin" "dist/esp32doit-${GITHUB_REF_NAME}-firmware.bin"
          esptool --chip esp32 merge-bin \\
            -o "dist/esp32doit-${GITHUB_REF_NAME}-merged-firmware.bin" \\
            --flash-mode dio --flash-freq 40m --flash-size 4MB \\
            0x1000 "${BUILD_DIR}/bootloader.bin" \\
            0x8000 "${BUILD_DIR}/partitions.bin" \\
            0x10000 "${BUILD_DIR}/firmware.bin"

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v3
        with:
          generate_release_notes: true
          files: |
            workshop/dist/esp32doit-${{ github.ref_name }}-firmware.bin
            workshop/dist/esp32doit-${{ github.ref_name }}-merged-firmware.bin""",
            },
            {
                "heading": "LAB-0602: ติด Tag Push ขึ้น GitHub, กดดาวน์โหลด .bin จาก Releases และ Flash ที่ 0x0",
                "desc": "<strong>สำคัญ:</strong> ต้อง Merge <code>release.yml</code> เข้า <code>main</code> บน Fork ก่อนติด Tag! เมื่อ Actions สร้าง Release เสร็จ ให้เข้าแท็บ Releases -> <code>[1]</code> เปิด Assets -> <code>[2]</code> คลิกโหลด <code>*-merged-firmware.bin</code> มา Flash ลงบอร์ดที่ Offset <code>0x0</code>",
                "images": [
                    ("../images/anno-06-releases.png", "หน้า GitHub Release หลัง Push Tag: [1] เปิดดู Assets -> [2] คลิกโหลดไฟล์ *-merged-firmware.bin"),
                ],
                "code": """# 1. ดึง main ล่าสุด (ที่มี release.yml แล้ว) จากนั้นติด Tag และ Push:
git checkout main
git pull origin main
git tag -a v1.0.0 -m "release: v1.0.0"
git push origin v1.0.0

# 2. Flash ผ่าน Terminal ด้วย esptool ที่ติดตั้งไว้แล้วใน Lab 00 (เปลี่ยน COM3 เป็นพอร์ตของบอร์ด):
esptool --chip esp32 --port COM3 --baud 460800 write-flash 0x0 esp32doit-v1.0.0-merged-firmware.bin
# หรือใช้เว็บ https://espressif.github.io/esptool-js/ -> Connect -> 0x0 -> เลือก merged-firmware.bin""",
            },
        ],
        "expected_output": """$ gh release list --limit 3
TITLE   TYPE    TAG NAME  PUBLISHED
v0.1.0  Latest  v0.1.0    about 1 minute ago

$ uv run exercises/verify.py --all
...
Summary: 18 PASS | 0 FAIL | 0 WARN (All modules verified)""",
        "results": [
            "LAB-0601: รายชื่อไฟล์ Assets ที่ปรากฏในหน้า GitHub Release <code>v1.0.0</code>",
            "LAB-0602: ขนาดไฟล์ <code>firmware.bin</code> เทียบกับ <code>merged-firmware.bin</code>",
        ],
        "questions": [
            "Q1: เพราะเหตุใด GitHub Release จึงควรแนบทั้ง <code>firmware.bin</code> และ <code>merged-firmware.bin</code>?",
            "Q2: เหตุใดเราจึงควรติด Tag หลังจาก Rebase/Merge เข้า <code>main</code> เสร็จแล้ว แทนที่จะติด Tag ก่อน Rebase?",
        ],
        "exercise": {
            "code": "LAB-0603",
            "desc": "ปล่อย Release เวอร์ชัน <code>v1.0.0</code> ใน Fork ของตัวเอง แล้วรันตรวจครบทั้ง 6 Modules ด้วย <code>verify.py --all</code>",
            "snippet": """gh release list --limit 3
uv run exercises/verify.py --all""",
        },
        "screenshots": [
            ("../images/term-04-verify.png", "ผลลัพธ์หลังรัน uv run exercises/verify.py --all ตรวจผ่านครบทั้ง 6 Modules"),
        ],
    },
]

TEMPLATE = """<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8" />
  <title>{title}</title>
  <style>
    @page {{
      size: A4;
      margin: 20mm 16mm 18mm 16mm;
      @top-right {{
        content: "ESP32 Git, Testing & CI/CD Workshop\\A Dept. Computer Engineering / PlatformIO Lab";
        white-space: pre;
        font-family: "Leelawadee UI", "Tahoma", sans-serif;
        font-size: 8.5pt;
        color: #475569;
        text-align: right;
      }}
      @bottom-right {{
        content: "Page " counter(page) " of " counter(pages);
        font-family: "Leelawadee UI", "Tahoma", sans-serif;
        font-size: 9pt;
        color: #334155;
      }}
    }}
    * {{ box-sizing: border-box; }}
    body {{
      font-family: "Leelawadee UI", "Tahoma", "Segoe UI", sans-serif;
      color: #111827;
      font-size: 10pt;
      line-height: 1.5;
      margin: 0;
      padding: 0;
      background: #ffffff;
    }}
    .doc-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-bottom: 1.5px solid #1e3a8a;
      padding-bottom: 6px;
      margin-bottom: 14px;
      font-size: 8.5pt;
      color: #475569;
    }}
    .doc-header .left {{
      font-weight: 700;
      color: #1e3a8a;
      font-size: 9.5pt;
    }}
    h1.lab-title {{
      text-align: center;
      font-size: 13pt;
      font-weight: 700;
      text-decoration: underline;
      margin: 6px 0 14px 0;
      color: #0f172a;
    }}
    h3.sec {{
      font-size: 10.5pt;
      font-weight: 700;
      margin: 12px 0 6px 0;
      color: #0f172a;
    }}
    ol, ul {{
      margin: 4px 0 8px 0;
      padding-left: 22px;
    }}
    li {{ margin-bottom: 3px; }}
    code {{
      font-family: "Consolas", "Courier New", monospace;
      font-size: 9pt;
      background: #f1f5f9;
      padding: 1px 4px;
      border-radius: 3px;
    }}
    .exp-row {{
      margin: 6px 0 4px 12px;
    }}
    .exp-code {{
      text-decoration: underline;
      font-weight: 600;
      margin-right: 6px;
    }}
    .code-box {{
      background: #f8fad2;
      border: 1px solid #475569;
      padding: 8px 12px;
      margin: 4px 0 10px 12px;
      font-family: "Consolas", "Courier New", monospace;
      font-size: 8.2pt;
      line-height: 1.38;
      white-space: pre-wrap;
      word-break: break-word;
      overflow-wrap: anywhere;
      color: #0f172a;
    }}
    .term-box {{
      background: #0f172a;
      border: 1px solid #334155;
      border-radius: 4px;
      padding: 8px 12px;
      margin: 6px 0 12px 12px;
      font-family: "Consolas", "Courier New", monospace;
      font-size: 8pt;
      line-height: 1.38;
      white-space: pre-wrap;
      word-break: break-word;
      overflow-wrap: anywhere;
      color: #e2e8f0;
    }}
    .fill-line {{
      border-bottom: 1px solid #334155;
      height: 20px;
      margin: 4px 0 8px 12px;
    }}
    .q-block {{
      margin: 6px 0 8px 12px;
    }}
    .shot-grid {{
      display: grid;
      grid-template-columns: {shot_cols};
      gap: 12px;
      margin: 8px 0 8px 12px;
    }}
    .shot-card {{
      border: 1px solid #cbd5e1;
      padding: 8px;
      background: #ffffff;
      text-align: center;
      break-inside: avoid;
    }}
    .shot-card img {{
      width: 100%;
      height: auto;
      display: block;
      border: 1px solid #e2e8f0;
    }}
    .shot-cap {{
      font-size: 8.5pt;
      color: #475569;
      margin-top: 4px;
    }}
    .page-break {{ page-break-before: always; }}
  </style>
</head>
<body>
  <div class="doc-header">
    <div class="left">DOIT ESP32 DevKit v1 • PlatformIO Workshop</div>
    <div class="right">Git, Pre-commit, Testing &amp; GitHub Actions CI/CD</div>
  </div>

  <h1 class="lab-title">{title}</h1>

  <h3 class="sec">วัตถุประสงค์การเรียนรู้ (Objective)</h3>
  <ol>{objectives_html}</ol>

  <h3 class="sec">ผลลัพธ์การเรียนรู้ (Learning Outcomes)</h3>
  <ol>{outcomes_html}</ol>

  <h3 class="sec">เครื่องมือและไฟล์ที่ต้องเตรียม (Tools &amp; Prerequisites)</h3>
  <ul>{tools_html}</ul>

  <h3 class="sec">การทดลอง (Experiments)</h3>
  {experiments_html}

  <div class="page-break"></div>

  <h3 class="sec" style="text-decoration: underline;">รายละเอียดการทดลองและขั้นตอนปฏิบัติ (Step-by-Step Guide &amp; Code):</h3>
  {details_html}

  <h3 class="sec">ตัวอย่างผลลัพธ์ใน Terminal (Expected Output)</h3>
  <div class="term-box">{expected_output_html}</div>

  <h3 class="sec">บันทึกผล (Results)</h3>
  {results_html}

  <h3 class="sec">การสังเกตและตอบคำถาม (Observation and Questions)</h3>
  {questions_html}

  <h3 class="sec" style="text-decoration: underline;">แบบฝึกหัด</h3>
  <div class="exp-row">
    <span class="exp-code">{ex_code}:</span> {ex_desc}
  </div>
  <div class="code-box">{ex_snippet}</div>

  <h3 class="sec" style="text-decoration: underline;">ภาพประกอบผลลัพธ์จริง (Screenshots)</h3>
  <div class="shot-grid">
    {shots_html}
  </div>
</body>
</html>
"""


def build_lab(lab: dict) -> None:
    objectives_html = "".join(f"<li>{o}</li>" for o in lab["objectives"])
    outcomes_html = "".join(f"<li>{o}</li>" for o in lab["outcomes"])
    tools_html = "".join(f"<li>{t}</li>" for t in lab["tools"])
    experiments_html = "".join(
        f'<div class="exp-row"><span class="exp-code">{code}:</span> {desc}</div>'
        for code, desc in lab["experiments"]
    )
    detail_blocks = []
    for item in lab["details"]:
        if isinstance(item, dict):
            heading = item["heading"]
            desc = item.get("desc", "")
            code = item.get("code", "")
            imgs = item.get("images", [])
        else:
            heading, code = item
            desc, imgs = "", []
        blk = f'<div class="exp-row"><strong>{heading}</strong></div>'
        if desc:
            blk += f'<div class="exp-row" style="margin-top:2px;color:#334155;">{desc}</div>'
        if code:
            blk += f'<div class="code-box">{html.escape(code)}</div>'
        for src, cap in imgs:
            blk += f'<div class="shot-card" style="margin:6px 0 10px 12px;"><img src="{src}" alt="{html.escape(cap)}"/><div class="shot-cap">{html.escape(cap)}</div></div>'
        detail_blocks.append(blk)
    details_html = "".join(detail_blocks)
    expected_output_html = html.escape(lab["expected_output"])
    results_html = "".join(
        f'<div class="q-block">{r}<div class="fill-line"></div><div class="fill-line"></div></div>'
        for r in lab["results"]
    )
    questions_html = "".join(
        f'<div class="q-block">{q}<div class="fill-line"></div><div class="fill-line"></div></div>'
        for q in lab["questions"]
    )
    shot_cols = "1fr"
    shots_html = "".join(
        f'<div class="shot-card"><img src="{src}" alt="{html.escape(cap)}"/><div class="shot-cap">{html.escape(cap)}</div></div>'
        for src, cap in lab["screenshots"]
    )

    rendered = TEMPLATE.format(
        title=lab["title"],
        objectives_html=objectives_html,
        outcomes_html=outcomes_html,
        tools_html=tools_html,
        experiments_html=experiments_html,
        details_html=details_html,
        expected_output_html=expected_output_html,
        results_html=results_html,
        questions_html=questions_html,
        ex_code=lab["exercise"]["code"],
        ex_desc=lab["exercise"]["desc"],
        ex_snippet=html.escape(lab["exercise"]["snippet"]),
        shot_cols=shot_cols,
        shots_html=shots_html,
    )

    html_path = HTML_DIR / f"{lab['slug']}.html"
    pdf_path = LABS_DIR / f"{lab['slug']}.pdf"
    html_path.write_text(rendered, encoding="utf-8")

    subprocess.run(
        [
            EDGE_EXE,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_path}",
            f"file:///{str(html_path).replace(chr(92), '/')}",
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print(f"Generated: labs/{pdf_path.name} ({pdf_path.stat().st_size} bytes)")


def main() -> None:
    for lab in LABS:
        build_lab(lab)


if __name__ == "__main__":
    main()
