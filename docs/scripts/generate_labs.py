#!/usr/bin/env python3
"""
Generate individual Lab Sheet PDFs (LAB00..LAB06, 1 file = 1 topic) into docs/labs/.
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
            "<strong>คำศัพท์สำคัญ (Glossary):</strong> <code>PATH</code> (รายชื่อโฟลเดอร์ที่ Terminal ค้นหาคำสั่ง), <code>uv</code> (ตัวจัดการ Python CLI ที่แยก Environment สะอาดกว่า <code>pip</code> กลาง), <code>Toolchain</code> (ชุดคอมไพเลอร์สร้างไฟล์ <code>.bin</code>), <code>origin</code> (Fork ของคุณ) vs <code>upstream</code> (Repo ต้นทางอาจารย์)",
            "สคริปต์ตรวจความพร้อม: <code>uv run exercises/check_env.py</code> (ใช้ <code>python exercises/check_env.py</code> แทนได้เช่นกัน)",
        ],
        "experiments": [
            ("LAB-0000", "(start-from-0) เริ่มจากศูนย์: ติดตั้ง Git + VS Code + Extension <strong>PlatformIO IDE</strong> (UI) และ <strong>GitHub Pull Requests</strong> พร้อมเข้าใจความต่างระหว่าง Extension กับ CLI"),
            ("LAB-0001", "(core-cli) ติดตั้ง <code>uv</code> และชุด CLI Tools ทั้งหมด (<code>pre-commit</code>, <code>platformio</code>, <code>esptool</code>) พร้อมรีเฟรช PATH"),
            ("LAB-0002", "(compilers &amp; gh) ติดตั้ง WinLibs <code>gcc/g++</code> สำหรับ Windows (ใช้ใน Lab 04) และ GitHub CLI <code>gh</code> (Optional สำหรับ Lab 05–06)"),
            ("LAB-0003", "(fork &amp; warmup) Fork + Clone ลงพาทสั้นๆ, ตั้งค่า Git <code>--local</code>, Pre-cache ESP32 และตรวจเครื่องด้วย <code>check_env.py</code>"),
        ],
        "details": [
            {
                "heading": "LAB-0000: เริ่มต้นจากศูนย์ — ติดตั้ง Git + VS Code และ PlatformIO IDE Extension",
                "desc": "Workshop นี้ใช้ PlatformIO <strong>2 ส่วนคู่กัน</strong>: (1) <strong>PlatformIO IDE Extension</strong> ใน VS Code สำหรับเขียนโค้ด/กด Build/Upload และ (2) <strong>PlatformIO CLI (<code>pio</code>)</strong> สำหรับพิมพ์คำสั่งใน Terminal และรันบน GitHub Actions CI — เริ่มจากลง Git, VS Code, กด <code>Ctrl+Shift+X</code> ใน VS Code ค้นหา <strong>PlatformIO IDE</strong> -> กด <strong>Install</strong> -> รอตัวโหลดมุมขวาล่างขึ้นเสร็จแล้ว Restart VS Code",
                "images": [
                    ("../images/anno-02-vscode-pr.png", "หน้า Extension (ตัวอย่าง): ใน VS Code กด Ctrl+Shift+X ค้นหา PlatformIO IDE และ GitHub Pull Requests เพื่อติดตั้ง"),
                ],
                "code": """# 1. Windows: ติดตั้ง Git และ Visual Studio Code (หากยังไม่มีในเครื่อง)
winget install Git.Git
winget install Microsoft.VisualStudioCode
git --version

# 2. ใน VS Code กด Ctrl+Shift+X ค้นหาและติดตั้ง Extension 2 ตัวนี้:
#    - platformio.platformio-ide  (รอแถบ 'Installing PlatformIO Core...' เสร็จ แล้ว Restart VS Code)
#    - github.vscode-pull-request-github
# 3. เฉพาะเครื่องส่วนตัวเท่านั้น (ถ้าใช้เครื่องมหาลัย ให้ข้ามไปใช้ --local หลัง Clone ใน LAB-0003):
# git config --global user.name "Your Name"
# git config --global user.email "you@example.com" """,
            },
            {
                "heading": "LAB-0001: ติดตั้ง uv, CLI Tools ทั้งหมด (pre-commit, pio, esptool) และเปิด Terminal ใหม่",
                "desc": "ลง PlatformIO IDE Extension ใน VS Code อย่างเดียวจะพิมพ์ <code>pio</code> ใน PowerShell นอก VS Code ไม่เจอ — จึงต้องลง <code>uv</code> เพื่อติดตั้ง CLI Tools ครบทั้ง 3 ตัว (<code>pre-commit</code>, <code>platformio</code>, <code>esptool</code>) แล้วรัน <code>uv tool update-shell</code> จากนั้น <strong>ปิด Terminal เดิมแล้วเปิด PowerShell หน้าต่างใหม่</strong> เพื่อรีเฟรช PATH",
                "code": """# 1. Windows (PowerShell): ติดตั้ง uv (macOS/Linux: curl -LsSf https://astral.sh/uv/install.sh | sh)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2. ปิดแล้วเปิด Terminal ใหม่ จากนั้นลง CLI Tools ทั้งหมด + อัปเดต PATH:
uv tool install pre-commit
uv tool install platformio
uv tool install esptool
uv tool update-shell

# 3. ปิด แล้วเปิด PowerShell ใหม่อีกรอบ! แล้วเช็กเวอร์ชัน:
pre-commit --version
pio --version
esptool version""",
            },
            {
                "heading": "LAB-0002: ติดตั้ง C/C++ Compiler (gcc) บน Windows และ GitHub CLI (gh)",
                "desc": "ลง WinLibs <code>gcc/g++</code> สำหรับรัน <code>pio test -e native</code> ใน Lab 04 (อาจใช้เวลาโหลดสักครู่และขอสิทธิ์ Admin; หลังลงเสร็จให้เปิด Terminal ใหม่แล้วเช็ก <code>g++ --version</code> หากเครื่องมหาลัยล็อกสิทธิ์ ให้ข้ามไปดูผล Native Test บน Cloud CI ใน Lab 05 แทนได้) และลง <code>gh</code> (Optional)",
                "code": """# 1. Windows: ติดตั้ง MinGW/WinLibs gcc/g++ สำหรับ [env:native]
winget install BrechtSanders.WinLibs.POSIX.UCRT

# 2. Optional: ติดตั้ง GitHub CLI (gh)
winget install GitHub.cli

# 3. เปิด Terminal ใหม่เพื่อรีเฟรช PATH แล้วตรวจสอบ:
g++ --version
gh --version""",
            },
            {
                "heading": "LAB-0003 (ขั้นตอนที่ 1/2): Fork โปรเจกต์, Clone ลงพาทสั้นๆ และตั้งค่า --local",
                "desc": "เปิด <code>https://github.com/SavEe2429/git-practice</code> -> กด <code>[1] Fork</code> -> กด <code>[2] &lt;&gt; Code</code> Copy URL ของ Fork ตัวเอง จากนั้นเข้าแท็บ <strong>Actions</strong> บน Fork กดปุ่มเขียว <strong>I understand my workflows, go ahead and enable them</strong> และ Clone ลงพาทสั้นๆ (เช่น <code>C:\\ws</code> หรือ Desktop; ชื่อโฟลเดอร์จะเป็น <code>git-practice</code>) พร้อมเข้าโฟลเดอร์ <code>cd git-practice</code>",
                "images": [
                    ("../images/anno-01-repo-fork.png", "หน้าเว็บ GitHub: [1] กดปุ่ม Fork -> [2] กด <> Code เพื่อ Copy URL ของ Fork ตัวเอง"),
                ],
                "code": """# 1. สร้างโฟลเดอร์สั้นๆ เพื่อเลี่ยงปัญหา Windows path ยาว แล้ว Clone จาก Fork ของตัวเอง:
mkdir C:\\ws -Force
cd C:\\ws
git clone https://github.com/<your-username>/git-practice.git
cd git-practice

# 2. เพิ่ม upstream อ้างอิง Repo อาจารย์ และตั้งชื่อผู้เขียนแบบ --local (ปลอดภัยบนเครื่องรวม):
git remote add upstream https://github.com/SavEe2429/git-practice.git
git config --local user.name "Your Name"
git config --local user.email "you@example.com" """,
            },
            {
                "heading": "LAB-0003 (ขั้นตอนที่ 2/2): VS Code Extensions, Pre-cache ESP32, แก้ Windows TEMP & ตรวจเครื่อง",
                "desc": "ใน <code>C:\\ws\\git-practice</code> เปิด <code>code workshop</code> แล้วกด <strong>Install Recommended Extensions</strong> (2 ตัว: <code>platformio.platformio-ide</code> และ <code>github.vscode-pull-request-github</code>; หมายเหตุ: Extension มี <code>pio.exe</code> แยกของตัวเองอยู่ใน <code>~/.platformio/penv/</code> ต่างจาก CLI ที่ลงผ่าน <code>uv</code>) รอบแรก <code>pio run</code> จะโหลดไฟล์ ~20–60 วินาที หากเจอ Error <code>cc1plus.exe: too many filenames given</code> ให้ตั้ง <code>$env:TEMP</code> ก่อนรันใหม่",
                "code": """# 1. เปิดโฟลเดอร์ workshop ใน VS Code (ต้องอยู่ในโฟลเดอร์ root git-practice ก่อน):
code workshop

# 2. [แก้ปัญหา Windows TEMP ล่วงหน้า หากเครื่องชี้ TEMP ไปที่ C:\\WINDOWS\\TEMP]:
New-Item -ItemType Directory -Force C:\\Temp | Out-Null
$env:TEMP="C:\\Temp"; $env:TMP="C:\\Temp"

# 3. Pre-cache Toolchain + Arduino ESP32 (หาก `pio` ไม่พบใน PATH ใช้ & "$env:USERPROFILE\\.platformio\\penv\\Scripts\\pio.exe"):
pio run -d workshop -e esp32doit-devkit-v1

# 4. ตรวจความพร้อมเครื่องทั้งหมดจากโฟลเดอร์ root (ใช้ python แทน uv run ได้เหมือนกัน):
uv run exercises/check_env.py""",
            },
        ],
        "expected_output": """$ uv run exercises/check_env.py
=== Pre-Workshop Environment Check ===

[OK] Git: git version 2.54.0.windows.1
[OK] Git identity: Your Name <you@example.com>
[OK] uv: uv 0.11.31
[OK] pre-commit: pre-commit 4.7.0
[OK] PlatformIO CLI (in PATH): PlatformIO Core, version 6.2.0
[OK] esptool: esptool v5.x
[OK] GitHub CLI: gh version 2.x.x (auth: logged in)
[WARN] ไม่พบ gcc/g++ ใน PATH ... (หากเครื่องไม่ได้ลง WinLibs ให้ดูผลบน CI ใน Lab 05 แทน)
[OK] Windows TEMP: C:\\Temp
======================================================
พร้อมบางส่วน (พบ 1 คำเตือน [WARN] — อ่านรายละเอียดด้านบนก่อนเริ่ม Lab 04 / Lab 06)
# หมายเหตุ: หากยังไม่ได้เปิด Terminal ใหม่หลัง uv tool update-shell ภาพด้านล่างจะขึ้น [WARN] ให้ทำตามคำแนะนำในช่องที่ขึ้นเตือน""",
        "results": [
            "LAB-0001: ผลลัพธ์ของ <code>git --version</code>, <code>uv --version</code>, <code>pre-commit --version</code>, <code>pio --version</code> และ <code>esptool version</code>",
            "LAB-0003: ผลลัพธ์จริงจาก <code>uv run exercises/check_env.py</code> และ <code>pio run -d workshop -e esp32doit-devkit-v1</code>",
        ],
        "questions": [
            "Q1: เหตุใดเราจึงควรติดตั้งทั้ง VS Code PlatformIO IDE และ CLI Tools + Pre-cache <code>pio run</code> ให้จบตั้งแต่ Lab 00?",
            "Q2: หากใช้เครื่องคอมพิวเตอร์ส่วนกลางของมหาวิทยาลัย เหตุใดจึงควรใช้ <code>git config --local</code> และกด Sign Out ออกจากบัญชี GitHub/VS Code/Credential Manager เมื่อเลิกใช้งาน?",
        ],
        "exercise": {
            "code": "LAB-0004",
            "desc": "รันสคริปต์ตรวจสภาพแวดล้อมจากโฟลเดอร์ root ของ <code>git-practice</code> และบันทึกหลักฐานว่าคำสั่งทั้งหมดพร้อมเข้าเรียน Lab 01 แล้ว",
            "snippet": """cd C:\\ws\\git-practice
pio --version
pre-commit --version
esptool version
uv run exercises/check_env.py""",
        },
        "screenshots": [
            ("../images/term-00-check-env.png", "ตัวอย่างผลรันจริงจาก uv run exercises/check_env.py (รายการที่ยังไม่อยู่ใน PATH จะขึ้น [WARN] พร้อมคำสั่งแก้ไข)"),
        ],
    },
    {
        "slug": "LAB01-Linear_Git_Rebase",
        "title": "Lab 01: Linear Git (Rebase), Fork Workflow &amp; Conventional Commits",
        "objectives": [
            "เข้าใจภาพความแตกต่างระหว่าง <code>origin</code> (Fork ของตัวเอง) กับ <code>upstream</code> (Repo ต้นทางของอาจารย์) และการซิงก์งานร่วมกันโดยไม่ทับกัน",
            "เรียนรู้การรักษาประวัติ Commit บน <code>main</code> ให้เป็นเส้นตรงด้วย <code>git rebase upstream/main</code>, การแก้ Rebase Conflict และการ Push ด้วย <code>--force-with-lease</code>",
        ],
        "outcomes": [
            "ตรวจสอบสถานะ <code>origin</code> / <code>upstream</code> และอัปเดตฐานโค้ดล่าสุดจาก <code>upstream/main</code> ได้ถูกต้อง",
            "แตก Branch <code>feature/*</code> จาก <code>main</code>, แก้โค้ดและ Commit แบบ Conventional Commits, แก้ Rebase Conflict และ Push ด้วย <code>--force-with-lease</code> ได้",
            "ตรวจสอบประวัติด้วย <code>git log --graph --oneline --decorate</code> แล้วเห็นโครงสร้างเส้นตรง (Linear History)",
        ],
        "tools": [
            "เครื่องมือทั้งหมดติดตั้งและผ่านการตรวจจาก <strong>Lab 00</strong> เรียบร้อยแล้ว (Git CLI, <code>uv</code>, <code>pio</code>, Fork &amp; Clone ในเครื่อง)",
            "Repository ต้นทาง (<code>upstream</code>): <code>https://github.com/SavEe2429/git-practice</code>",
            "วิดีโอประกอบ: <code>videos/01-gitflow-branching.mp4</code>",
        ],
        "experiments": [
            ("LAB-0101", "(remote-check) เข้าใจภาพ Merge vs Rebase, ตรวจ <code>origin</code> vs <code>upstream</code> และซิงก์ <code>main</code> ให้ทัน <code>upstream/main</code>"),
            ("LAB-0102", "(branch &amp; rebase) แตก <code>feature/fast-blink</code> ด้วย <code>git switch -c</code>, แก้ <code>workshop/src/main.cpp</code>, Commit และ Rebase บน <code>upstream/main</code>"),
            ("LAB-0103", "(conflict &amp; force-push) วิธีแก้ Rebase Conflict (ความหมายของ <code>HEAD</code> ตอน rebase) และการ Push หลัง Rebase ด้วย <code>--force-with-lease</code>"),
        ],
        "details": [
            {
                "heading": "LAB-0101: เปรียบเทียบกราฟ Merge vs Rebase และตรวจ Remote (origin vs upstream)",
                "desc": "<code>origin</code> คือ Fork บนบัญชีคุณเอง (ไม่ขยับถ้าคุณไม่ Push) ส่วน <code>upstream</code> คือ Repo ต้นทางที่มีโค้ดใหม่จากอาจารย์/เพื่อน — การใช้ <code>git rebase</code> จะยก Commit ของเราไปต่อท้าย <code>upstream/main</code> ทำให้ประวัติเป็นเส้นตรงเส้นเดียว (ต่างจาก <code>git merge</code> ที่แตกเป็น 2 เส้นแล้วรวบกลับ) หมายเหตุ: บน PowerShell 5.1 ข้อความของ <code>git</code> ที่ออก stderr อาจขึ้นตัวสีแดงแม้สำเร็จ ให้อ่านข้อความจริงก่อนเสมอ",
                "images": [
                    ("../images/anno-01-repo-fork.png", "หน้าเว็บ GitHub (อ้างอิงจาก Lab 00): [1] Fork เป็นบัญชีตัวเอง -> [2] <> Code คัดลอก URL"),
                ],
                "code": """# ภาพเปรียบเทียบใน git log --graph:
# [Merge - แตกเป็น 2 เส้น]       [Rebase - เส้นตรงเส้นเดียว]
#   *   Merge branch 'feat'        * C3' (HEAD -> feature/fast-blink)
#   |\\                             * C2' (upstream/main, main)
#   | * C3 (feature)               * C1  chore: initial starter
#   * | C2 (upstream/main)
#   |/
#   * C1

# 1. เข้าโฟลเดอร์ที่ Clone ไว้ใน Lab 00 แล้วตรวจ Remote ทั้ง 2 ตัว:
cd C:\\ws\\git-practice
git remote -v

# 2. อัปเดต main ของเครื่องและ Fork ให้ตรงกับ upstream/main ล่าสุด:
git switch main
git pull --rebase upstream main
git push origin main""",
            },
            {
                "heading": "LAB-0102: แตก Feature Branch, แก้ workshop/src/main.cpp, Commit &amp; Rebase จาก upstream/main",
                "desc": "แตก Branch ใหม่ด้วย <code>git switch -c</code> จากนั้นลองแก้บรรทัดที่ 15 ใน <code>workshop/src/main.cpp</code> จาก <code>blink_math::clamp_interval(500);</code> เป็น <code>200</code> แล้ว Commit ตามรูปแบบ Conventional Commits และฝึกซิงก์กับ <code>upstream/main</code>",
                "code": """# 1. แตก branch ใหม่จาก main (ใช้ git switch -c ให้เป็นแบบเดียวกันตลอด)
git switch -c feature/fast-blink main

# 2. เปิด workshop/src/main.cpp แก้บรรทัดที่ 15 ใน setup():
#    blink_interval_ms = blink_math::clamp_interval(200);  // fast blink preset
# จากนั้น Stage และ Commit แบบ Conventional Commits:
git add workshop/src/main.cpp
git commit -m "feat(blink): support fast blink interval"

# 3. ดึงฐานล่าสุดจาก upstream (Repo อาจารย์) แล้ว Rebase:
git fetch upstream
git rebase upstream/main
git log --graph --oneline --decorate -n 6""",
            },
            {
                "heading": "LAB-0103: การแก้ Rebase Conflict, ออกจาก Vim และ Push ด้วย --force-with-lease",
                "desc": "<strong>สำคัญมาก:</strong> ระหว่าง <code>git rebase</code> สัญลักษณ์ <code>&lt;&lt;&lt;&lt;&lt;&lt;&lt; HEAD</code> คือ<strong>โค้ดฝั่ง <code>upstream/main</code> (ฐานใหม่)</strong> ส่วนด้านล่าง <code>=======</code> คือ<strong>โค้ด Commit ของเรา</strong>! หลังแก้ Conflict เสร็จให้ใช้ <code>git push --force-with-lease</code> (<strong>ห้าม</strong>รัน <code>git pull</code> ตามคำแนะนำ error และ<strong>ห้าม</strong> force-push เข้า <code>main</code> เด็ดขาด)",
                "code": """# --- แนะนำตั้ง Editor เป็น VS Code ก่อนกันติดหน้าจอ Vim ---
git config --local core.editor "code --wait"

# --- หากเกิด CONFLICT ระหว่าง git rebase upstream/main ---
# 1. เปิดไฟล์ที่มีปัญหา ลบเส้น <<<<<<< HEAD, =======, >>>>>>> แล้วเก็บโค้ดที่ถูกต้อง
# 2. Stage ไฟล์ที่แก้แล้ว แล้วทำ Rebase ต่อ (ถ้าเผลอเข้าหน้า Vim ให้พิมพ์ :wq แล้ว Enter):
git add workshop/src/main.cpp
git rebase --continue
# (หากทำพลาดอยากถอยกลับก่อน Rebase ให้ใช้: git rebase --abort)

# 3. หลัง Rebase ประวัติ Commit Hash จะเปลี่ยน ทำให้ git push ปกติถูก Reject -> ใช้ --force-with-lease:
git push --force-with-lease -u origin feature/fast-blink""",
            },
        ],
        "expected_output": """$ git remote -v
origin    https://github.com/<your-username>/git-practice.git (fetch)
origin    https://github.com/<your-username>/git-practice.git (push)
upstream  https://github.com/SavEe2429/git-practice.git (fetch)
upstream  https://github.com/SavEe2429/git-practice.git (push)

$ git log --graph --oneline --decorate -n 4
* 9a4c21e (HEAD -> feature/fast-blink, origin/feature/fast-blink) feat(blink): support fast blink interval
* 7c796a2 (upstream/main, origin/main, main) chore(workshop): restore starter skeleton files for student labs 02-06
* f75e649 docs(workshop): add Lab 00 setup, consolidate installs, update slides and screenshots""",
        "results": [
            "LAB-0101: ผลลัพธ์จากการรัน <code>git remote -v</code> (แสดงครบทั้ง <code>origin</code> และ <code>upstream</code>)",
            "LAB-0102: ผลลัพธ์จาก <code>git log --graph --oneline --decorate -n 6</code> (เป็นเส้นตรงเส้นเดียวหรือไม่)",
        ],
        "questions": [
            "Q1: การทำงานแบบ Fork Workflow (แยก <code>origin</code> ออกจาก <code>upstream</code>) มีข้อดีทางวิศวกรรมอย่างไรเมื่อเทียบกับการ Push เข้า Repo หลักโดยตรง?",
            "Q2: การใช้ <code>git rebase</code> แตกต่างจาก <code>git merge</code> อย่างไรในหน้าตาของ <code>git log --graph</code>?",
            "Q3: เหตุใดหลัง <code>git rebase</code> แล้วจึงต้องใช้ <code>git push --force-with-lease</code> แทน <code>git pull</code> หรือ <code>git push --force</code>?",
        ],
        "exercise": {
            "code": "LAB-0104",
            "desc": "ตรวจว่าอยู่บน <code>feature/fast-blink</code> ที่มี Commit ใหม่ต่อปลาย <code>main</code> แบบเส้นตรง (หรือทดลองแตก <code>git switch -c feature/slow-blink main</code> เพิ่มฟังก์ชันใน <code>blink_math/</code>) แล้วรัน <code>verify.py</code>",
            "snippet": """# ตรวจผล Module 1 (ต้องมี feature/* branch ที่ Commit งานจริงต่อจาก main):
uv run exercises/verify.py --module 1""",
        },
        "screenshots": [
            ("../images/term-01-git-log.png", "ตัวอย่างผลลัพธ์จาก git log --graph --oneline --decorate: ประวัติ Commit เรียงเป็นเส้นตรง"),
        ],
    },
    {
        "slug": "LAB02-Issue_Forms_PR_Protection",
        "title": "Lab 02: YAML Issue Forms, Pull Request (Rebase) &amp; Branch Protection",
        "objectives": [
            "เรียนรู้การสร้างแบบฟอร์มแจ้งปัญหาและขอฟีเจอร์ด้วยไฟล์ YAML (<code>.github/ISSUE_TEMPLATE/*.yml</code>) และการใช้ PR Template",
            "เรียนรู้การเปิด Pull Request ได้ทั้งผ่านเว็บ GitHub และ VS Code Extension, ทำ Rebase and Merge และตั้ง Branch Protection บน <code>main</code>",
        ],
        "outcomes": [
            "แทนที่ Skeleton ใน <code>bug_report.yml</code>, <code>feature_request.yml</code> และ <code>config.yml</code> แล้วใช้งานฟอร์มบน GitHub ได้จริง",
            "เปิด Pull Request เข้า <code>main</code>, ตรวจ Checks และ Merge แบบ Rebase พร้อมลบ Branch อัตโนมัติได้",
            "ตั้งค่า Branch Protection / Rulesets เพื่อบังคับ PR และ Linear History บน <code>main</code> ได้ รวมถึง Logout ออกจากเครื่องส่วนกลางได้ครบ",
        ],
        "tools": [
            "GitHub Web (เปิด Issue &amp; PR) และ <strong>VS Code Extension: GitHub Pull Requests</strong> (<code>github.vscode-pull-request-github</code> จาก Lab 00)",
            "ไฟล์ปลายทาง: <code>.github/ISSUE_TEMPLATE/*.yml</code> (มีโครง <code># TODO</code> อยู่แล้ว) และ <code>.github/pull_request_template.md</code> (มีให้ใน Repo แล้ว)",
            "วิดีโอประกอบ: <code>videos/02-pull-request-review.mp4</code>",
        ],
        "experiments": [
            ("LAB-0201", "(issue-yml) แทนที่ไฟล์ Issue Forms (<code>bug_report.yml</code>, <code>feature_request.yml</code>, <code>config.yml</code>) แล้ว Push/Merge เข้า <code>main</code> บน Fork เพื่อเปิดใช้งานฟอร์ม"),
            ("LAB-0202", "(web-issue) ทดลองกดเปิด Issue จริงบนหน้าเว็บ GitHub (แท็บ <strong>Issues -&gt; New issue</strong>) ด้วยฟอร์มที่สร้างไว้"),
            ("LAB-0203", "(pr-2-ways) Push branch <code>feature/fast-blink</code> แล้วเปิด/Merge PR แบบ <strong>Rebase and merge</strong> (<strong>เลือกทำ 1 ใน 2 วิธี:</strong> เว็บ GitHub หรือ VS Code Extension) + ตั้ง Branch Protection + Logout"),
        ],
        "details": [
            {
                "heading": "LAB-0201 (ส่วนที่ 1/2): bug_report.yml — ลบ # TODO เดิมทั้งหมด แล้ววางส่วนหัวฟอร์ม + version + environment",
                "desc": "<strong>คำสั่งสำคัญ (สำคัญทุก Lab):</strong> เปิดไฟล์ <code>.github/ISSUE_TEMPLATE/bug_report.yml</code> แล้วกด <strong>Ctrl+A ลบเนื้อหา <code># TODO</code> เดิมออกทั้งหมด</strong> ก่อนวางโค้ดส่วนที่ 1/2 ลงไป (จากนั้นนำส่วนที่ 2/2 ไปต่อท้ายทันที)",
                "code": """# [Ctrl+A ลบเนื้อหาเดิมทั้งหมดใน .github/ISSUE_TEMPLATE/bug_report.yml แล้ววาง]
name: Bug Report (แจ้งบั๊ก Firmware)
description: รายงานปัญหาที่พบในโปรเจกต์ ESP32 DOIT DevKit v1
title: "[Bug]: "
labels: ["bug", "triage"]
body:
  - type: markdown
    attributes:
      value: |
        กรุณากรอกข้อมูลให้ครบถ้วนเพื่อให้ทีมจำลองปัญหาและแก้ไขได้เร็วขึ้นครับ

  - type: input
    id: version
    attributes:
      label: เวอร์ชันเฟิร์มแวร์ / Tag หรือ Commit
      description: ระบุ Tag (เช่น v1.0.0) หรือเลข Commit ที่พบปัญหา
      placeholder: v1.0.0
    validations:
      required: true

  - type: dropdown
    id: environment
    attributes:
      label: สภาพแวดล้อมที่พบปัญหา
      options:
        - DOIT ESP32 DevKit v1 (Hardware จริง)
        - PlatformIO Native Test ([env:native])
        - GitHub Actions CI
    validations:
      required: true""",
            },
            {
                "heading": "LAB-0201 (ส่วนที่ 2/2): bug_report.yml — ต่อท้าย description และ checklist",
                "desc": "นำโค้ดด้านล่างนี้ไป<strong>ต่อท้าย</strong>ไฟล์ <code>.github/ISSUE_TEMPLATE/bug_report.yml</code> ให้ครบ 4 fields (สำหรับไฟล์เฉลยสมบูรณ์เทียบได้ที่ <code>exercises/solutions/.github/ISSUE_TEMPLATE/</code>)",
                "code": """  - type: textarea
    id: description
    attributes:
      label: อาการที่พบ & ขั้นตอนการทำซ้ำ (Steps to Reproduce)
      placeholder: |
        1. รันคำสั่ง...
        2. ผลลัพธ์ที่เกิดขึ้น...
        3. ผลลัพธ์ที่คาดหวัง...
    validations:
      required: true

  - type: checkboxes
    id: checklist
    attributes:
      label: ยืนยันเบื้องต้น
      options:
        - label: ทดสอบบน branch main หรือ release ล่าสุดแล้ว
          required: true""",
            },
            {
                "heading": "LAB-0201 (เพิ่มเติม): feature_request.yml &amp; config.yml — ลบ # TODO เดิมในแต่ละไฟล์แล้ววางแทน",
                "desc": "เปิด <code>.github/ISSUE_TEMPLATE/feature_request.yml</code> และ <code>config.yml</code> กด <strong>Ctrl+A ลบโครงเดิมออกทั้งหมด</strong> แล้ววางโค้ด 2 บล็อกด้านล่างลงในแต่ละไฟล์ตามชื่อไฟล์ (ส่วน <code>.github/pull_request_template.md</code> มีให้ครบใน Repo แล้ว)",
                "code": """# === ไฟล์ที่ 1: .github/ISSUE_TEMPLATE/feature_request.yml (Ctrl+A แล้ววางทับ) ===
name: Feature Request (ขอฟีเจอร์ใหม่)
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
      options: [main (PR + Rebase and merge), release/v* (เฉพาะแก้บั๊กก่อนปล่อยเวอร์ชัน)]
      default: 0""",
            },
            {
                "heading": "LAB-0201 (ปิดท้าย): config.yml — ลบ # TODO เดิมแล้ววางเนื้อหา config.yml",
                "desc": "วางบล็อกนี้ลงใน <code>.github/ISSUE_TEMPLATE/config.yml</code> (<strong>กด Ctrl+A ลบโครงเดิมออกทั้งหมดก่อนวาง</strong> — เฉพาะเนื้อหา YAML เท่านั้น จากนั้นค่อยรันคำสั่ง Terminal ในกล่องถัดไป)",
                "code": """# [Ctrl+A ลบเนื้อหาเดิมทั้งหมดใน .github/ISSUE_TEMPLATE/config.yml แล้ววางทับ]
blank_issues_enabled: false
contact_links:
  - name: คู่มือ Workshop (Docs)
    url: https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms
    about: เอกสารอ้างอิงไวยากรณ์ YAML สำหรับ GitHub Issue Forms""",
            },
            {
                "heading": "LAB-0201 (ส่งขึ้น GitHub): ตรวจ YAML และนำ Issue Forms ขึ้น main บน Fork ก่อนเปิดหน้า New Issue",
                "desc": "ตรวจไวยากรณ์ YAML จากนั้น Commit และ Push เข้า <code>main</code> บน Fork ของตัวเองก่อน (GitHub จะอ่าน Issue Template จาก branch <code>main</code> เท่านั้น และตอนนี้เรายังไม่ได้เปิด Branch Protection จึง Push เข้า <code>main</code> เพื่อติดตั้งฟอร์มก่อนได้)",
                "images": [
                    ("../images/gh-02-issue-templates.png", "ตรวจสอบให้แน่ใจว่าทั้ง 3 ไฟล์ใน .github/ISSUE_TEMPLATE/ ถูก Push/Merge เข้า main บน Fork แล้ว"),
                ],
                "code": """# ตรวจ YAML แล้วนำไฟล์ Issue Forms ขึ้น main บน Fork ก่อนเปิด Issue:
uv run --with pyyaml python -c "import yaml,glob; [yaml.safe_load(open(f,encoding='utf-8')) for f in glob.glob('.github/**/*.yml',recursive=True)]; print('YAML OK')"
git switch main
git add .github/ISSUE_TEMPLATE/
git commit -m "docs(github): add YAML issue forms and chooser config"
git push origin main""",
            },
            {
                "heading": "LAB-0202: กดเปิด Issue จริงบนหน้าเว็บ GitHub (สังเกตหมายเลข #Issue)",
                "desc": "เข้าหน้า Fork ของตัวเองบนเว็บ GitHub -> <code>[1]</code> คลิกแท็บ <strong>Issues</strong> -> <code>[2]</code> กดปุ่มเขียว <strong>New issue</strong> -> เลือกฟอร์ม Feature Request / Bug Report แล้วกรอกจนได้เลข Issue (เช่น <code>#1</code> หรือ <code>#2</code>) เพื่อนำไปใช้อ้างอิงปิด Issue อัตโนมัติด้วย <code>Closes #&lt;เลข&gt;</code> ใน PR",
                "images": [
                    ("../images/anno-02-issues.png", "กดตามลำดับ: [1] คลิกแท็บ Issues -> [2] กดปุ่ม New issue เพื่อเลือก YAML Form"),
                    ("../images/anno-02-issue-detail.png", "ตัวอย่างหน้า Issue บน GitHub: [1] ดูเลข Issue (เช่น #2) เพื่อนำไปใส่ Closes #2 และ [2] ดูป้าย Labels อัตโนมัติ (ใน Fork ของคุณจะแสดงช่องที่กรอกจาก .yml)"),
                ],
            },
            {
                "heading": "LAB-0203 (วิธีที่ 1 — เว็บ GitHub): Push feature/fast-blink และเปิด PR แบบ Rebase and merge",
                "desc": "อัปเดต branch งานให้ทัน <code>main</code> บน Fork (<code>git switch feature/fast-blink</code> -&gt; <code>git rebase main</code> -&gt; <code>git push --force-with-lease -u origin feature/fast-blink</code>) จากนั้นบนเว็บ GitHub: <code>[1]</code> เข้าแท็บ <strong>Pull requests</strong> -> <code>[2]</code> กด <strong>New pull request</strong> -> ในหน้า Compare ให้เลือก <code>[1] base: main &lt;- compare: feature/fast-blink</code> (เปลี่ยนช่องขวาจาก main เป็น feature branch ของคุณ!) -> พิมพ์ <code>Closes #&lt;เลข&gt;</code> แล้วกด <code>[2] Create pull request</code> -> กดลูกศรเลือก <strong>Rebase and merge</strong> + <strong>Delete branch</strong>",
                "images": [
                    ("../images/anno-02-pulls.png", "บนหน้า Fork: [1] คลิกแท็บ Pull requests -> [2] กดปุ่ม New pull request"),
                    ("../images/anno-02-compare.png", "หน้า Compare: [1] เลือก base: main <- compare: feature/fast-blink (สลับช่องขวาจาก main เป็น branch งานของคุณ) -> ใส่ Closes #<เลข> -> [2] กด Create pull request"),
                ],
            },
            {
                "heading": "LAB-0203 (วิธีที่ 2 — VS Code Extension): เปิด PR ใน VS Code + ตั้ง Branch Protection + Logout",
                "desc": "<strong>เลือกทำวิธีนี้แทนวิธีที่ 1 ได้:</strong> กดไอคอน <strong>GitHub (รูปแมว)</strong> บนแถบซ้าย Activity Bar ของ VS Code (Extension <code>github.vscode-pull-request-github</code> จาก Lab 00 ดังภาพ) -> กด <strong>Sign in with GitHub</strong> -> กด <strong>Create Pull Request</strong> (Base = <code>main</code>, ใส่ <code>Closes #&lt;เลข&gt;</code>) -> Merge ด้วย Rebase — <strong>ตั้ง Branch Protection:</strong> เข้า Repo บนเว็บ -> <strong>Settings -> Branches -> Add classic branch protection rule</strong> (หรือ Rulesets) ใส่ pattern <code>main</code> แล้วติ๊ก <strong>Require a pull request before merging</strong> + <strong>Require linear history</strong> — <strong>และถ้าใช้เครื่องมหาลัย ต้อง Logout ออกด้วยทุกครั้ง!</strong>",
                "images": [
                    ("../images/anno-02-vscode-pr.png", "Extension GitHub Pull Requests ที่ติดตั้งไว้จาก Lab 00 (กดไอคอน GitHub แถบซ้ายใน VS Code เพื่อ Sign in / Create PR และกด Accounts มุมซ้ายล่าง -> Sign Out เมื่อเลิกใช้)"),
                ],
                "code": """# หากตั้ง PR บนเครื่องรวม ให้ Logout ทั้ง 2 จุดทันทีเมื่อจบ Lab 02:
# 1. VS Code: คลิกไอคอน Accounts (มุมซ้ายล่าง) -> <your-username> (GitHub) -> Sign Out
# 2. Terminal (หากเคย gh auth login ไว้):
gh auth logout""",
            },
        ],
        "expected_output": """# บนหน้าเว็บ GitHub หลัง Merge PR ด้วย Rebase and merge:
✓ Merged 1 commit into main from feature/fast-blink
✓ Issue #1 closed automatically (via "Closes #1")
✓ Branch feature/fast-blink deleted

# เมื่อตรวจสอบผ่าน VS Code Extension หลังใช้งานเสร็จ:
VS Code Accounts -> <your-username> (GitHub) -> Sign Out (เรียบร้อย)""",
        "results": [
            "LAB-0202: เลข Issue และ Labels ที่แสดงบนหน้าเว็บ GitHub หลัง Push ไฟล์ <code>.yml</code> เข้า <code>main</code>",
            "LAB-0203: เปรียบเทียบขั้นตอนเปิด PR ผ่าน<strong>เว็บ GitHub</strong> กับ <strong>VS Code Extension</strong> และตรวจสถานะหลังตั้ง Branch Protection",
        ],
        "questions": [
            "Q1: การใช้ Issue Form แบบ <code>.yml</code> ดีกว่าการปล่อยให้กรอก Issue แบบข้อความเปล่าอย่างไร?",
            "Q2: ตัวเลือก <strong>Require linear history</strong> ใน Branch Protection ช่วยป้องกันอะไร และเหตุใดจึงควร Sign Out ออกจาก GitHub ใน VS Code หลังเลิกใช้งานเครื่องส่วนกลาง?",
            "Q3: ทำไมหลัง Merge PR เข้า <code>main</code> แล้วจึงควรลบ Branch ย่อยทิ้งทันที?",
        ],
        "exercise": {
            "code": "LAB-0204",
            "desc": "เปิด Issue 1 รายการด้วยฟอร์ม <code>feature_request.yml</code> บนหน้าเว็บ GitHub จากนั้นเปิด PR (ผ่านเว็บหรือ VS Code Extension) พร้อมใส่ <code>Closes #&lt;เลข&gt;</code> เพื่อปิด Issue แล้วตรวจด้วย <code>verify.py</code>",
            "snippet": """# ในรายละเอียด PR (ผ่านเว็บ GitHub หรือ VS Code Extension) ให้ใส่: Closes #<เลข>
# หากใช้เครื่องห้องแล็บ อย่าลืม VS Code Accounts -> Sign Out หลังทำเสร็จ!
uv run exercises/verify.py --module 2""",
        },
        "screenshots": [
            ("../images/anno-02-pr-detail.png", "ผลลัพธ์หลังเปิด PR และ Merge สำเร็จ: [1] ตรวจแท็บ Checks ผ่านครบ -> [2] สถานะเปลี่ยนเป็น Merged"),
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
            "แทนที่ Skeleton <code>.pre-commit-config.yaml</code> และติดตั้ง Git Hooks ทั้ง <code>pre-commit</code> และ <code>commit-msg</code> ได้",
            "แก้ไขปัญหาเมื่อ Hook บล็อกไฟล์ที่จัดฟอร์แมตผิดหรือข้อความ Commit ไม่ตรงมาตรฐานได้ (เข้าใจสาเหตุต้อง <code>git add</code> ซ้ำและ Stage config)",
        ],
        "tools": [
            "<code>pre-commit</code> CLI (ติดตั้งไว้แล้วจาก <strong>Lab 00</strong>)",
            "ไฟล์ปลายทาง: <code>.pre-commit-config.yaml</code> (แทนที่โครง <code>repos: []</code>) และ <code>.clang-format</code> (มีให้ใน Repo แล้ว ไม่ต้องสร้างใหม่)",
            "วิดีโอประกอบ: <code>videos/03-pre-commit-hooks.mp4</code>",
        ],
        "experiments": [
            ("LAB-0301", "(config &amp; hooks) แทนที่ <code>.pre-commit-config.yaml</code>, Stage ไฟล์ด้วย <code>git add</code> และติดตั้ง Hook 2 Stage"),
            ("LAB-0302", "(break-fix) ทดสอบแยก 2 ขั้น: ขั้น A ให้ Hook จัดฟอร์แมตไฟล์เพี้ยน และขั้น B ทดสอบ Commit Message ผิดรูปแบบ"),
        ],
        "details": [
            {
                "heading": "LAB-0301 (ส่วนที่ 1/3): .pre-commit-config.yaml — ลบ repos: [] เดิมออก แล้ววาง Hook พื้นฐาน",
                "desc": "<strong>คำสั่งสำคัญ:</strong> เปิด <code>.pre-commit-config.yaml</code> แล้วกด <strong>Ctrl+A ลบ <code>repos: []</code> และ <code># TODO</code> เดิมออกทั้งหมด</strong> จากนั้นวางส่วนที่ 1/3 (ตามด้วยส่วนที่ 2/3 และ 3/3 ต่อท้ายในไฟล์เดียวกัน)",
                "code": """# [Ctrl+A ลบเนื้อหาเดิมใน .pre-commit-config.yaml แล้ววางส่วนที่ 1-3 ต่อกัน]
repos:
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
                "heading": "LAB-0301 (ส่วนที่ 2/3): .pre-commit-config.yaml — ต่อท้าย Hook จัด Format C/C++ (clang-format)",
                "desc": "ต่อท้ายลงใน <code>repos:</code> ของ <code>.pre-commit-config.yaml</code> โดยอ้างอิงกติกาจากไฟล์ <code>.clang-format</code> ที่มีใน Repo แล้ว (Google Style, IndentWidth: 2, ColumnLimit: 100)",
                "code": """  - repo: https://github.com/pre-commit/mirrors-clang-format
    rev: v23.1.5
    hooks:
      - id: clang-format
        types_or: [c++, c]""",
            },
            {
                "heading": "LAB-0301 (ส่วนที่ 3/3): .pre-commit-config.yaml — ต่อท้าย Hook ตรวจ Commit Message (commit-msg)",
                "desc": "ต่อท้ายลงใน <code>repos:</code> เพื่อตรวจหัวข้อ Commit ใน Stage <code>commit-msg</code> (หมายเหตุ: <code>pre-commit run --all-files</code> จะรันเฉพาะ Hook ตรวจไฟล์ ส่วน <code>conventional-pre-commit</code> จะทำงานตอนสั่ง <code>git commit</code>)",
                "code": """  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: v4.5.0
    hooks:
      - id: conventional-pre-commit
        stages: [commit-msg]
        args: [feat, fix, docs, style, refactor, test, ci, chore, build]""",
            },
            {
                "heading": "LAB-0301 (ปิดท้าย): Stage ไฟล์ .pre-commit-config.yaml และติดตั้ง Git Hook ทั้ง 2 Stage",
                "desc": "<strong>สำคัญ:</strong> ต้องรัน <code>git add .pre-commit-config.yaml</code> ก่อนและหลัง <code>pre-commit run --all-files</code> เพราะหากวางไฟล์ใน VS Code โดยไม่มีบรรทัดว่างปิดท้าย <code>end-of-file-fixer</code> จะเติมบรรทัดท้ายไฟล์ให้อัตโนมัติ (ต้อง <code>git add -u</code> อีกรอบ ไม่เช่นนั้นจะได้ Error <code>Your pre-commit configuration is unstaged</code>; บน Windows ข้อความ <code>LF will be replaced by CRLF</code> เป็นคำเตือนปกติ)",
                "code": """# 1. Stage ไฟล์ config ก่อนเสมอ + ผูก Hook ทั้ง 2 stage เข้า .git/hooks/:
git add .pre-commit-config.yaml
pre-commit install
pre-commit install --hook-type commit-msg

# 2. รันตรวจทุกไฟล์ (รอบแรกจะโหลด env ของ 3 hook repositories สักครู่):
pre-commit run --all-files

# 3. Stage ไฟล์ที่ end-of-file-fixer อาจปรับปรุงให้เรียบร้อย แล้ว Commit:
git add -u
git commit -m "chore(hooks): configure pre-commit and clang-format" """,
            },
            {
                "heading": "LAB-0302: ทดสอบ Break-Fix แยก 2 ขั้น (ขั้น A: Format Hook -> ขั้น B: Commit-Msg Hook)",
                "desc": "แยกทดสอบทีละ Stage เพื่อไม่ให้ Format Hook บล็อกก่อน Stage <code>commit-msg</code>: ขั้น A เพิ่มบรรทัดที่จัดช่องว่างผิดจงใจ <code>int   precommit_test =  1;</code> ท้ายฟังก์ชัน <code>setup()</code> ใน <code>workshop/src/main.cpp</code> (มองเห็นชัดแม้ก๊อปวางจาก PDF) -> ดู <code>clang-format</code> จัดให้ใหม่ -> <code>git add</code> -> ขั้น B ลอง Commit ด้วยข้อความผิดกฎเพื่อดู <code>conventional-pre-commit</code> บล็อกจริง แล้วจึง Commit ให้ผ่าน",
                "code": """# ขั้น A: เพิ่มท้ายฟังก์ชัน setup() ใน workshop/src/main.cpp:  int   precommit_test =  1;
git add workshop/src/main.cpp
git commit -m "style: test clang-format"
# -> จะขึ้น clang-format Failed (files were modified by this hook) เพราะ hook จัดช่องว่างให้!

# ขั้น B: Stage ไฟล์ที่ถูกจัดฟอร์แมตแล้ว จากนั้นลองตั้งชื่อ Commit ผิดกฎ:
git add workshop/src/main.cpp
git commit -m "bad commit message"
# -> รอบนี้ pre-commit ผ่านแล้ว ทำให้ commit-msg ทำงานและบล็อกข้อความผิดทันที!

# ขั้น C: แก้ข้อความเป็น Conventional Commit แล้ว Commit ให้สำเร็จ:
git commit -m "style: format main.cpp with clang-format" """,
            },
        ],
        "expected_output": """$ pre-commit run --all-files
trim trailing whitespace.................................................Passed
fix end of files.........................................................Passed
check yaml...............................................................Passed
check for added large files..............................................Passed
clang-format.............................................................Passed

$ git commit -m "bad commit message"
...
Conventional Commit......................................................Failed
- hook id: conventional-pre-commit
- exit code: 1
[Bad commit message] >> bad commit message""",
        "results": [
            "LAB-0301: ผลลัพธ์จากการรัน <code>pre-commit run --all-files</code>",
            "LAB-0302: ข้อความแจ้งเตือนทั้งตอน <code>clang-format Failed</code> (ขั้น A) และ <code>Conventional Commit Failed</code> (ขั้น B)",
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
            "แทนที่ Skeleton ใน <code>platformio.ini</code> เพื่อรองรับทั้ง <code>[env:esp32doit-devkit-v1]</code> และ <code>[env:native]</code> ได้",
            "แทนที่ Skeleton <code>test_main.cpp</code> ด้วย 4 Test Cases และรัน <code>pio test -e native</code> (หรือเข้าใจวิธีแก้ปัญหา Windows/CI fallback) ได้",
        ],
        "tools": [
            "PlatformIO CLI (<code>pio</code>) และ <code>gcc/g++</code> จาก <strong>Lab 00</strong> (หากไม่มี <code>gcc</code> ในเครื่อง ให้รัน <code>pio run</code> ตรวจ Build แล้วไปดูผล <code>[env:native]</code> บน Cloud CI ใน Lab 05 ได้)",
            "ไฟล์ปลายทาง: <code>workshop/platformio.ini</code> (มีโครง TODO), <code>workshop/test/test_native/test_main.cpp</code> (มีโครง TODO) และ <code>workshop/test/test_esp32/test_hardware.cpp</code>",
            "วิดีโอประกอบ: <code>videos/04-platformio-unit-testing.mp4</code>",
        ],
        "experiments": [
            ("LAB-0401", "(platformio-ini) แทนที่ <code>workshop/platformio.ini</code> เพื่อเพิ่ม <code>[env:native]</code> คู่กับ <code>[env:esp32doit-devkit-v1]</code>"),
            ("LAB-0402", "(native-tests) แทนที่ <code>workshop/test/test_native/test_main.cpp</code> ด้วย Unit Tests ครบ 4 ฟังก์ชันของ <code>blink_math</code>"),
            ("LAB-0403", "(run-and-commit) รัน <code>pio test -d workshop -e native -v</code> เทียบกับ <code>pio run -d workshop -e esp32doit-devkit-v1</code> (พร้อมคู่มือแก้ปัญหา Windows) แล้ว Commit/Push"),
        ],
        "details": [
            {
                "heading": "LAB-0401: workshop/platformio.ini — Ctrl+A ลบเนื้อหาเดิมทั้งหมด แล้ววาง Dual Environment",
                "desc": "<strong>คำสั่งสำคัญ:</strong> เปิด <code>workshop/platformio.ini</code> แล้วกด <strong>Ctrl+A ลบเนื้อหา Starter เดิม (; TODO) ออกทั้งหมด</strong> แล้ววางบล็อกนี้แทน (ห้ามวางต่อท้าย มิฉะนั้นจะ Error <code>section 'env:esp32doit-devkit-v1' already exists</code>)",
                "code": """; [Ctrl+A ลบเนื้อหาเดิมทั้งหมดใน workshop/platformio.ini แล้ววางแทน]
[env:esp32doit-devkit-v1]
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
                "heading": "LAB-0402 (ส่วนที่ 1/2): test_main.cpp — ลบไฟล์เดิมทั้งหมด แล้ววาง Header & 4 Test Cases",
                "desc": "<strong>คำสั่งสำคัญ:</strong> เปิด <code>workshop/test/test_native/test_main.cpp</code> แล้วกด <strong>Ctrl+A ลบโค้ดเดิมทั้งหมด</strong> (รวม <code>test_starter_example</code> และ <code>main()</code> เดิม มิฉะนั้นจะมี <code>main()</code> ซ้ำ!) แล้ววางส่วนที่ 1/2 ลงไปก่อนตามด้วยส่วนที่ 2/2",
                "code": """// [Ctrl+A ลบเนื้อหาเดิมทั้งหมดใน workshop/test/test_native/test_main.cpp แล้ววางส่วนที่ 1+2]
#include <unity.h>
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
                "heading": "LAB-0402 (ส่วนที่ 2/2): test_main.cpp — ต่อท้ายฟังก์ชัน main() สั่งรัน Test Runner",
                "desc": "ต่อท้ายลงใน <code>workshop/test/test_native/test_main.cpp</code> เพื่อเปิด Suite ด้วย <code>UNITY_BEGIN()</code>, เรียก <code>RUN_TEST(...)</code> ครบทั้ง 4 ฟังก์ชัน แล้วคืนค่า Exit Code ด้วย <code>UNITY_END()</code> (ไฟล์เฉลยเทียบได้ที่ <code>exercises/solutions/test/test_native/test_main.cpp</code>)",
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
                "heading": "LAB-0403 (ขั้นที่ 1/2): รัน Test & Build และวิธีแก้ปัญหาที่พบบ่อยบน Windows",
                "desc": "ศึกษาไฟล์ <code>workshop/test/test_esp32/test_hardware.cpp</code> ที่มีให้ใน Repo แล้วรัน Test/Build จากโฟลเดอร์ root ของ Repo — <strong>กรณีไม่มี gcc บน Windows:</strong> สามารถลง WinLibs หรือดูผลผ่าน Linux Cloud CI ใน Lab 05 ได้ (<code>verify.py</code> จะขึ้น <code>[WARN]</code> ไม่ถือว่า FAIL) และหมายเหตุ: คำสั่ง <code>pio run</code> ด้านล่างใช้คอมไพล์อย่างเดียวไม่ต้องเสียบบอร์ด (เฉพาะ <code>pio test -e esp32doit-devkit-v1</code> หรือ upload จึงจะถามหา COM Port)",
                "code": """# 1. รัน Native Unit Test บน Host PC:
pio test -d workshop -e native -v

# 2. หากเจอ Error `'gcc' is not recognized`: ติดตั้ง WinLibs แล้วเปิด Terminal ใหม่ (หรือไปตรวจบน CI ใน Lab 05):
winget install BrechtSanders.WinLibs.POSIX.UCRT
g++ --version

# 3. Build เฟิร์มแวร์ .bin (หากเจอ cc1plus: too many filenames ให้ตั้ง $env:TEMP ก่อน):
New-Item -ItemType Directory -Force C:\\Temp | Out-Null
$env:TEMP="C:\\Temp"; $env:TMP="C:\\Temp"
pio run -d workshop -e esp32doit-devkit-v1""",
            },
            {
                "heading": "LAB-0403 (ขั้นที่ 2/2): บันทึกการเปลี่ยนแปลงขึ้น Git (เพื่อทดสอบบน CI ใน Lab 05)",
                "desc": "เมื่อแก้ไข <code>workshop/platformio.ini</code> และ <code>test_main.cpp</code> เสร็จแล้ว ให้ Stage + Commit และ Push ขึ้น Fork เพื่อเตรียมใช้งานร่วมกับ CI ใน Lab 05 (หากคำสั่ง <code>pio</code> ไม่อยู่ใน PATH ใช้ <code>&amp; \"$env:USERPROFILE\\.platformio\\penv\\Scripts\\pio.exe\"</code> แทนได้)",
                "code": """# Stage, Commit (pre-commit จะจัด clang-format ให้อัตโนมัติ) และ Push:
git add workshop/platformio.ini workshop/test/test_native/test_main.cpp
git commit -m "test(native): add [env:native] and blink_math unity tests"
git push origin HEAD""",
            },
        ],
        "expected_output": """$ pio test -d workshop -e native -v
test/test_native/test_main.cpp:~: test_add_numbers_positive    [PASSED]
test/test_native/test_main.cpp:~: test_clamp_interval_bounds   [PASSED]
test/test_native/test_main.cpp:~: test_next_led_state_toggles  [PASSED]
test/test_native/test_main.cpp:~: test_calculate_cycle_ms      [PASSED]
----------------------- 4 Tests 0 Failures 0 Ignored -----------------------

$ pio run -d workshop -e esp32doit-devkit-v1
RAM:   [=         ]  ~6.7% (used ~22 KB from 327680 bytes)
Flash: [==        ] ~22.2% (used ~291 KB from 1310720 bytes)
========================= [SUCCESS] Took ~20s =========================""",
        "results": [
            "LAB-0403 (Unit Test): จำนวน Test Cases ที่รันผ่านบน <code>[env:native]</code> (หรือบันทึก <code>[WARN]</code> กรณีเครื่องไม่มี <code>gcc</code>)",
            "LAB-0403 (Firmware Build): ขนาด RAM และ Flash ที่ใช้จากการ Build <code>esp32doit-devkit-v1</code>",
        ],
        "questions": [
            "Q1: ทำไมเราต้องแยกฟังก์ชันคำนวณไว้ใน <code>lib/blink_math/</code> โดยไม่ใส่ <code>#include &lt;Arduino.h&gt;</code>?",
            "Q2: การตั้งค่า <code>test_build_src = no</code> ใน <code>[env:native]</code> มีไว้เพื่ออะไร?",
        ],
        "exercise": {
            "code": "LAB-0404",
            "desc": "ตรวจสอบว่ามี Test Cases ใน <code>workshop/test/test_native/test_main.cpp</code> ครบทั้ง 4 ฟังก์ชันของ <code>blink_math</code> แล้วรัน <code>verify.py</code>",
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
            "เข้าใจโครงสร้างไฟล์ YAML (<code>.github/workflows/ci.yml</code>), คีย์เวิร์ดหลัก และแหล่งค้นหา Actions จาก GitHub Marketplace",
            "ออกแบบ CI Pipeline 3 ขั้นตอน (<code>lint</code> → <code>unit-test</code> → <code>build-esp32</code>) โดยใช้ <code>uv</code> และ Caching",
        ],
        "outcomes": [
            "อธิบายความหมายของ <code>on</code>, <code>defaults.run.working-directory</code>, <code>jobs</code>, <code>needs</code>, <code>uses</code>, <code>with</code>, <code>run</code>, <code>if</code> ได้",
            "แทนที่ Skeleton <code>ci.yml</code>, ตรวจสอบผลการรัน CI บนแท็บ GitHub Actions และแก้ไขเมื่อทำ Break-Fix CI แดงได้",
        ],
        "tools": [
            "GitHub Actions &amp; GitHub Marketplace (<code>https://github.com/marketplace?type=actions</code>)",
            "ไฟล์ปลายทาง: <code>.github/workflows/ci.yml</code> (มีโครง <code>starter-placeholder</code> อยู่แล้ว ต้องลบทิ้งทั้งหมด)",
            "วิดีโอประกอบ: <code>videos/05-github-actions-ci.mp4</code>",
        ],
        "experiments": [
            ("LAB-0501", "(enable-ci) เปิด Actions บน Fork, อ่านตารางคีย์ YAML และแทนที่ <code>.github/workflows/ci.yml</code> (ลบ <code>starter-placeholder</code>)"),
            ("LAB-0502", "(break-fix) Push PR เข้า <code>main</code> แล้วทดลองแก้ Test ให้พังเพื่อดู CI แดง จากนั้นแก้ให้กลับมาเขียว + ทดสอบ Artifact on <code>release/v1.0.0</code>"),
        ],
        "details": [
            {
                "heading": "LAB-0501 (ตารางอ้างอิง): ความหมายของ YAML Keys ใน GitHub Actions",
                "desc": "ทำความเข้าใจคำศัพท์ทั้งหมดที่ใช้ใน <code>ci.yml</code> ก่อนลงมือวางโค้ด (ข้อควรรู้: <code>defaults.run.working-directory</code> ใช้เฉพาะกับคำสั่ง <code>run:</code> เท่านั้น ไม่ได้ครอบคลุม <code>uses:</code> เช่น <code>upload-artifact</code> จึงยังต้องเขียน path เต็ม <code>workshop/.pio/...</code>)",
                "code": """# คีย์หลัก -> หน้าที่และความหมาย
# on:                  -> กำหนดเหตุการณ์ทริกเกอร์ ('release/**' ต้องใส่ quote กัน * กลายเป็น YAML alias)
# defaults.run:        -> ตั้งโฟลเดอร์เริ่มต้นให้ทุก step ที่เป็น `run:` (workshop)
# jobs / runs-on:      -> แยกกลุ่มงาน (เช่น lint, unit-test) บน VM Linux (ubuntu-latest)
# needs:               -> รอให้ Job ก่อนหน้าผ่านก่อน จึงค่อยเริ่ม Job ถัดไป
# uses: / with:        -> เรียก Action สำเร็จรูปจาก Marketplace (เช่น checkout@v7) พร้อมส่งพารามิเตอร์
# run:                 -> รันคำสั่ง Shell ใน Runner VM (setup-uv จะเพิ่ม ~/.local/bin เข้า PATH ให้ pio)
# if: / ${{ ... }}     -> เงื่อนไข + Expression เช่น startsWith(github.ref, ...), hashFiles('...')""",
            },
            {
                "heading": "LAB-0501 (ส่วนที่ 1/4): ci.yml — Ctrl+A ลบ starter-placeholder เดิมออก แล้ววาง Trigger & Defaults",
                "desc": "<strong>คำสั่งสำคัญ:</strong> เปิด <code>.github/workflows/ci.yml</code> แล้วกด <strong>Ctrl+A ลบเนื้อหาเดิมทั้งหมด</strong> (รวม <code>on: workflow_dispatch:</code> และ job <code>starter-placeholder:</code> มิฉะนั้น <code>verify.py</code> จะ FAIL!) แล้ววางส่วนที่ 1/4 ถึง 4/4 ต่อกัน",
                "code": """# [Ctrl+A ลบ starter-placeholder เดิมใน .github/workflows/ci.yml แล้ววางส่วนที่ 1-4 ต่อกัน]
name: CI - Lint, Test & Build

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
                "heading": "LAB-0501 (ส่วนที่ 2/4): ci.yml — ต่อท้าย Job 1 (lint: ตรวจ Format & YAML ด้วย Pre-commit)",
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
                "heading": "LAB-0501 (ส่วนที่ 3/4): ci.yml — ต่อท้าย Job 2 (unit-test: รัน Unity Test หลัง lint ผ่าน)",
                "desc": "ใช้ <code>needs: lint</code> เพื่อรอ Job แรกผ่านก่อน แล้ว Cache <code>~/.platformio/.cache</code> ผูก Key กับ <code>workshop/platformio.ini</code> ก่อนรัน <code>pio test -e native -v</code>",
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
                "heading": "LAB-0501 (ส่วนที่ 4/4): ci.yml — ต่อท้าย Job 3 (build-esp32: คอมไพล์ .bin & Upload Artifact)",
                "desc": "รอ <code>needs: unit-test</code> แล้วจึงลอง Build เฟิร์มแวร์จริง <code>esp32doit-devkit-v1</code> และหากเป็น Branch <code>release/**</code> ให้แนบไฟล์ <code>.bin</code> เก็บไว้ด้วย <code>upload-artifact@v7</code> (ไฟล์เฉลยเทียบได้ที่ <code>exercises/solutions/.github/workflows/ci.yml</code>)",
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
                "heading": "LAB-0502: Push CI ขึ้น Fork, ดูผล 3 Jobs บนแท็บ Actions และทดสอบ Break-Fix",
                "desc": "ตรวจ YAML -> Commit + Push บน Branch <code>ci/add-workflow</code> แล้วเปิด PR เข้า <code>main</code> บน Fork จากนั้นเข้าแท็บ <strong>Actions</strong> (หากยังไม่เคยกด Enable ให้กดปุ่มเขียวก่อน) -> <code>[1]</code> เลือก Workflow -> <code>[2]</code> คลิกดูกราฟ 3 Jobs — <strong>Break &amp; Fix:</strong> ลองแก้ <code>test_main.cpp</code> ให้ Assert ผิด (<code>99</code>) แล้ว Push ซ้ำดู CI แดง จากนั้นแก้กลับเป็น <code>5</code> จนเขียวแล้ว Rebase &amp; Merge เข้า <code>main</code>",
                "images": [
                    ("../images/anno-05-actions-list.png", "บนแท็บ Actions: [1] เลือก Workflow CI - Lint, Test & Build -> [2] คลิกชื่อ Run เพื่อดูรายละเอียด 3 Jobs"),
                ],
                "code": """# 1. ตรวจ YAML + Commit & Push ขึ้น Branch เพื่อเปิด PR เข้า main:
pre-commit run check-yaml --all-files
git switch -c ci/add-workflow main
git add .github/workflows/ci.yml
git commit -m "ci: add lint, native test and esp32 build workflow"
git push -u origin ci/add-workflow

# 2. (Optional Break-Fix) แก้ test_add_numbers_positive เป็น 99 แล้ว Push -> ดู CI แดง -> แก้กลับเป็น 5!
# 3. ตรวจ Tag ล่าสุดของ Action และรายการ Run ผ่าน CLI:
gh api repos/actions/checkout/releases/latest --jq .tag_name
gh run list --workflow ci.yml --limit 3""",
            },
        ],
        "expected_output": """$ gh run list --workflow ci.yml --limit 3
STATUS  TITLE                                              WORKFLOW                 BRANCH           ELAPSED
✓       ci: add lint, native test and esp32 build workflow CI - Lint, Test & Build  ci/add-workflow  1m12s
✓       test(native): add [env:native] and unity tests     CI - Lint, Test & Build  main             1m08s""",
        "results": [
            "LAB-0501: เวลาที่ใช้ในแต่ละ Job (<code>lint</code>, <code>unit-test</code>, <code>build-esp32</code>) บน GitHub Actions",
            "LAB-0502: อาการที่เกิดขึ้นบนหน้า Pull Request เมื่อ Unit Test ใน CI ไม่ผ่าน และผลหลังแก้กลับให้เขียว",
        ],
        "questions": [
            "Q1: เหตุใดใน <code>ci.yml</code> จึงต้องระบุ <code>defaults: run: working-directory: workshop</code> (และเหตุใด <code>upload-artifact</code> ยังต้องเขียน path ขึ้นต้นด้วย <code>workshop/</code>)?",
            "Q2: คีย์เวิร์ด <code>needs: unit-test</code> ใน Job <code>build-esp32</code> ทำหน้าที่อะไร?",
            "Q3: การทำ <code>actions/cache@v6</code> กับโฟลเดอร์ <code>~/.platformio</code> ช่วยเรื่องอะไร?",
        ],
        "exercise": {
            "code": "LAB-0503",
            "desc": "Merge PR ที่มี <code>ci.yml</code> เข้า <code>main</code> บน Fork (หรือลอง Push branch <code>release/v1.0.0</code> เพื่อตรวจ Artifact <code>rc-firmware-*</code>) แล้วรัน <code>verify.py</code>",
            "snippet": """gh run list --workflow ci.yml --limit 3
uv run exercises/verify.py --module 5""",
        },
        "screenshots": [
            ("../images/anno-05-actions-graph.png", "ผลลัพธ์หลังคลิก Run: กราฟ 3 Jobs ([1] Lint -> [2] Unit Test -> [3] Build ESP32) ผ่านสีเขียวครบ (คลิกแต่ละกล่องเพื่อดู Log ได้)"),
        ],
    },
    {
        "slug": "LAB06-Release_Tag_and_Firmware_Bin",
        "title": "Lab 06: Automated Release (CD), Tagging, Flashing &amp; Shared-PC Cleanup",
        "objectives": [
            "เข้าใจความแตกต่างระหว่าง <code>firmware.bin</code> (สำหรับ OTA) กับ <code>merged-firmware.bin</code> (สำหรับ Flash ใหม่ไฟล์เดียวที่ <code>0x0</code>)",
            "เรียนรู้การทำงานของ <code>release.yml</code> เมื่อ Push Tag <code>v*.*.*</code>, การนำไฟล์ไป Flash ด้วย <code>esptool</code> และการล้างบัญชีออกจากเครื่องส่วนกลาง",
        ],
        "outcomes": [
            "แทนที่ Skeleton <code>release.yml</code>, ปล่อยเวอร์ชันผ่าน <code>git tag -a v1.0.0</code> และสร้าง GitHub Release อัตโนมัติได้",
            "อธิบายวิธีนำไฟล์จาก Release ไป Flash ลงบอร์ด DOIT ESP32 DevKit v1 ได้ และทำ Shared-PC Cleanup ได้ครบ 4 จุด",
        ],
        "tools": [
            "เครื่องมือ <code>esptool</code> (ติดตั้งไว้แล้วจาก <strong>Lab 00</strong>) หรือเว็บ <code>https://espressif.github.io/esptool-js/</code>",
            "ไฟล์ปลายทาง: <code>.github/workflows/release.yml</code> (มีโครง <code>starter-placeholder</code> อยู่แล้ว ต้องลบทิ้งทั้งหมด)",
            "วิดีโอประกอบ: <code>videos/06-github-actions-release.mp4</code>",
        ],
        "experiments": [
            ("LAB-0601", "(tag-release) แทนที่ <code>.github/workflows/release.yml</code> (ลบ <code>starter-placeholder</code>), Merge เข้า <code>main</code> และติด Tag <code>v1.0.0</code>"),
            ("LAB-0602", "(flash-bin) ตรวจสอบไฟล์ Asset ในหน้า GitHub Releases และคำสั่ง Flash ด้วย <code>esptool</code>"),
            ("LAB-0603", "(logout-cleanup) ปฏิบัติตาม Checklist ออกจากบัญชีครบทั้ง 4 จุดก่อนลุกจากเครื่องคอมพิวเตอร์มหาวิทยาลัย"),
        ],
        "details": [
            {
                "heading": "LAB-0601 (ส่วนที่ 1/3): release.yml — Ctrl+A ลบ starter-placeholder เดิม แล้ววาง Trigger Tag & Permissions",
                "desc": "<strong>คำสั่งสำคัญ:</strong> เปิด <code>.github/workflows/release.yml</code> แล้วกด <strong>Ctrl+A ลบเนื้อหาเดิมทั้งหมด</strong> (รวม <code>workflow_dispatch:</code> และ <code>starter-placeholder:</code>) จากนั้นวางส่วนที่ 1/3, 2/3 และ 3/3 ต่อกัน (เทียบฉบับเต็มได้ที่ <code>exercises/solutions/.github/workflows/release.yml</code>)",
                "code": """# [Ctrl+A ลบ starter-placeholder เดิมใน .github/workflows/release.yml แล้ววางส่วนที่ 1-3]
name: Release Firmware (CD)

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
                "heading": "LAB-0601 (ส่วนที่ 2/3): release.yml — ต่อท้าย Job release (Setup, Test & Build Firmware)",
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
                "heading": "LAB-0601 (ส่วนที่ 3/3): release.yml — ต่อท้ายด้วย esptool merge-bin & action-gh-release",
                "desc": "<strong>ระวังการย่อหน้า YAML:</strong> 2 step ด้านล่างต้องเว้น 6 ช่องให้ตรงกับ <code>- uses:</code> ด้านบน! (คำสั่ง <code>merge-bin</code> ใช้ <code>shell: bash</code> บน GitHub Runner จึงใช้เครื่องหมาย <code>\\</code> ต่อบรรทัดได้ ส่วนใน PowerShell บนเครื่องห้ามใช้ <code>\\</code> ต่อบรรทัด และ <code>files:</code> ยังต้องเขียน path เต็ม <code>workshop/dist/...</code>)",
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
                "heading": "LAB-0602: นำ release.yml เข้า main, ติด Tag v1.0.0, โหลด .bin และ Flash ที่ 0x0",
                "desc": "<strong>สำคัญ:</strong> ต้อง Commit/PR ให้ <code>release.yml</code> อยู่บน <code>main</code> ของ Fork ก่อนติด Tag! (หมายเหตุ: หากติด Tag ผิดพลาดสามารถลบแล้วทำใหม่ได้ด้วย <code>git tag -d v1.0.0</code> และ <code>git push origin :refs/tags/v1.0.0</code>)",
                "images": [
                    ("../images/anno-06-releases.png", "ตัวอย่างหน้า GitHub Release (จากเวอร์ชัน v0.1.0 — ในงานของคุณจะแสดง v1.0.0): [1] เปิดดู Assets -> [2] คลิกโหลดไฟล์ *-merged-firmware.bin"),
                ],
                "code": """# 1. Commit + PR release.yml เข้า main บน Fork ก่อน (เช่นผ่าน release/v1.0.0):
git switch -c release/v1.0.0 main
git add .github/workflows/release.yml
git commit -m "ci(cd): add release workflow for v*.*.* tags"
git push -u origin release/v1.0.0
# -> เปิด PR เข้า main แล้วกด Rebase and merge

# 2. ดึง main ล่าสุดที่มี release.yml แล้วติด Tag v1.0.0 และ Push:
git switch main
git pull origin main
git tag -a v1.0.0 -m "release: v1.0.0"
git push origin v1.0.0

# 3. Flash ผ่าน Terminal ด้วย esptool จาก Lab 00 (เปลี่ยน COM3 เป็นพอร์ตของบอร์ด):
esptool --chip esp32 --port COM3 --baud 460800 write-flash 0x0 esp32doit-v1.0.0-merged-firmware.bin
# หรือใช้เว็บ https://espressif.github.io/esptool-js/ -> Connect -> 0x0 -> เลือก merged-firmware.bin""",
            },
            {
                "heading": "LAB-0603: Shared-PC Logout Checklist (ทำครบ 4 จุดก่อนลุกจากเครื่องมหาวิทยาลัย)",
                "desc": "เพื่อความปลอดภัยของบัญชี GitHub ส่วนตัวบนเครื่องห้องปฏิบัติการมหาวิทยาลัย ห้ามลืมออกจากระบบเพียงแค่ปิดหน้าต่าง ต้องเช็กให้ครบทั้ง <strong>4 จุด</strong>: (1) VS Code, (2) GitHub CLI, (3) Windows Credential Manager และ (4) Browser + โฟลเดอร์งาน",
                "code": """# [1] VS Code: คลิกไอคอน Accounts (รูปคนมุมซ้ายล่าง) -> <username> (GitHub) -> Sign Out
# [2] GitHub CLI: ออกจากระบบใน Terminal
gh auth logout

# [3] Windows Credential Manager: ตรวจและลบทั้ง git: และ gh: Token ในเครื่อง Windows
cmdkey /list
# cmdkey /delete:git:https://github.com
# cmdkey /delete:gh:github.com:<your-username>  (หรือลบผ่าน Control Panel -> Credential Manager)

# [4] Browser & Workspace: กด Sign out บน github.com แล้วลบโฟลเดอร์งาน / Downloads (.bin)
cd C:\\
Remove-Item -Recurse -Force C:\\ws\\git-practice""",
            },
        ],
        "expected_output": """$ gh release list --limit 3
TITLE   TYPE    TAG NAME  PUBLISHED
v1.0.0  Latest  v1.0.0    about 1 minute ago

$ uv run exercises/verify.py --all
...
Summary: 19 PASS | 0 FAIL | 0 WARN
# (หมายเหตุ: หากเครื่องห้องแล็บไม่ได้ลง gcc จะแสดง Summary: 18 PASS | 0 FAIL | 1 WARN ซึ่งถือว่าผ่านครบ)""",
        "results": [
            "LAB-0602 (Assets): รายชื่อไฟล์ Assets ที่ปรากฏในหน้า GitHub Release <code>v1.0.0</code>",
            "LAB-0602 (Binary Size): ขนาดไฟล์ <code>firmware.bin</code> เทียบกับ <code>merged-firmware.bin</code> (ทำไมจึงต่างกัน ~65 KB)",
        ],
        "questions": [
            "Q1: เพราะเหตุใด GitHub Release จึงควรแนบทั้ง <code>firmware.bin</code> และ <code>merged-firmware.bin</code>?",
            "Q2: เหตุใดเราจึงควรติด Tag หลังจาก Rebase/Merge เข้า <code>main</code> เสร็จแล้ว แทนที่จะติด Tag ก่อน Rebase?",
        ],
        "exercise": {
            "code": "LAB-0604",
            "desc": "ปล่อย Release เวอร์ชัน <code>v1.0.0</code> ใน Fork ของตัวเอง, รัน <code>verify.py --all</code> เก็บหลักฐาน จากนั้นทำ Shared-PC Cleanup (<code>LAB-0603</code>) ก่อนลุกจากเครื่อง",
            "snippet": """gh release list --limit 3
uv run exercises/verify.py --all""",
        },
        "screenshots": [
            ("../images/term-04-verify.png", "ตัวอย่างผลรัน uv run exercises/verify.py --all (จุดที่ยังไม่ได้ทำบนเครื่อง/GitHub จะขึ้น [WARN]/[FAIL] ให้ไล่แก้จนผ่านครบทั้ง 19 รายการ)"),
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
      gap: 28px;
      margin: 26px 0 26px 12px;
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
            blk += f'<div class="shot-card" style="margin:26px 0 26px 12px;"><img src="{src}" alt="{html.escape(cap)}"/><div class="shot-cap">{html.escape(cap)}</div></div>'
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
