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
        "slug": "LAB01-Linear_Git_Rebase",
        "title": "Lab 01: Linear Git (Rebase), Fork Workflow &amp; Conventional Commits",
        "objectives": [
            "เรียนรู้การทำงานแบบ Fork &amp; Branch Workflow เพื่อแยกพื้นที่พัฒนาและทำงานร่วมกันบน Repository โดยไม่เขียนทับกัน",
            "เรียนรู้การรักษาประวัติ Commit บน <code>main</code> ให้เป็นเส้นตรง (Linear History) ด้วย <code>git rebase</code> และเขียน Conventional Commits",
        ],
        "outcomes": [
            "Fork และ Clone โปรเจกต์ ESP32 PlatformIO ลงเครื่องได้ถูกต้อง",
            "แตก Branch <code>feature/*</code> จาก <code>main</code>, Commit ตามมาตรฐาน, และ Rebase ให้ทัน <code>origin/main</code> ได้",
            "ตรวจสอบประวัติด้วย <code>git log --graph --oneline</code> แล้วเห็นโครงสร้างเส้นตรง",
        ],
        "tools": [
            "Git CLI (2.40+) &amp; GitHub Account (สำหรับกด Fork)",
            "Repository ต้นทาง: <code>https://github.com/SavEe2429/git-practice</code>",
            "สคริปต์ตรวจความพร้อม: <code>uv run exercises/check_env.py</code>",
            "วิดีโอประกอบ: <code>videos/01-gitflow-branching.mp4</code>",
        ],
        "experiments": [
            ("LAB-0101", "(env &amp; fork) ตรวจสอบความพร้อมเครื่อง, กด Fork Repo หลักไปยัง Account ของตัวเอง และ Clone ลงเครื่อง"),
            ("LAB-0102", "(branch &amp; rebase) แตก <code>feature/fast-blink</code> จาก <code>main</code>, แก้โค้ดใน <code>workshop/</code>, Commit แบบ Conventional Commits และฝึก <code>git rebase</code>"),
        ],
        "details": [
            (
                "LAB-0101: ตรวจสอบเครื่อง, กด Fork บน GitHub และ Clone โปรเจกต์ (Terminal)",
                """# 1. กดปุ่ม Fork บนหน้าเว็บ https://github.com/SavEe2429/git-practice
# 2. Clone จาก Fork ของตัวเองลงเครื่อง
git clone https://github.com/<your-username>/git-practice.git
cd git-practice

# 3. ตรวจสอบ remote และความพร้อมเครื่องมือด้วย uv
git remote -v
uv run exercises/check_env.py""",
            ),
            (
                "LAB-0102: สร้าง feature branch, Conventional Commit และ Rebase (Terminal)",
                """# แตก branch ใหม่จาก main (ไม่ทำโค้ดบน main โดยตรง)
git checkout -b feature/fast-blink main

# แก้ไขไฟล์ workshop/src/main.cpp (เช่น ปรับ blink_interval_ms)
# จากนั้น Stage และ Commit ด้วยรูปแบบ Conventional Commits:
git add workshop/src/main.cpp
git commit -m "feat(blink): support fast blink interval"

# อัปเดต branch ให้ทัน main เสมอด้วย rebase (ไม่สร้าง merge commit)
git fetch origin
git rebase origin/main
git log --graph --oneline -n 6""",
            ),
        ],
        "expected_output": """$ uv run exercises/check_env.py
[OK] git        : git version 2.4x.x
[OK] gh         : gh version 2.xx.x
[OK] pre-commit : pre-commit 4.x.x
[OK] pio        : PlatformIO Core 6.1.x
Environment ready!

$ git log --graph --oneline -n 4
* 9a4c21e (HEAD -> feature/fast-blink) feat(blink): support fast blink interval
* 7b3e10a (origin/main, main) docs: update lab guides
* 4d2f81b ci: add native test and esp32 build workflow
* 1c0a9d2 chore: initial workshop structure""",
        "results": [
            "LAB-0101: ผลลัพธ์จากการรัน <code>uv run exercises/check_env.py</code>",
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
            ("../images/gh-01-repo-fork.png", "ตัวอย่างหน้า Repo บน GitHub พร้อมปุ่ม Fork"),
            ("../images/term-01-git-log.png", "ตัวอย่างผลลัพธ์ git log --graph --oneline"),
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
            "GitHub Repository (Fork ของผู้เรียน) &amp; GitHub CLI (<code>gh</code>)",
            "ไฟล์ปลายทาง: <code>.github/ISSUE_TEMPLATE/*.yml</code> และ <code>.github/pull_request_template.md</code>",
            "วิดีโอประกอบ: <code>videos/02-pull-request-review.mp4</code>",
        ],
        "experiments": [
            ("LAB-0201", "(issue-yml) ก๊อปวางโครงสร้าง Issue Forms ลงใน <code>.github/ISSUE_TEMPLATE/*.yml</code> และทดสอบเปิด Issue"),
            ("LAB-0202", "(pr-rebase) Push branch <code>feature/fast-blink</code> ขึ้น GitHub, เปิด PR เข้า <code>main</code> และตั้ง Branch Protection"),
        ],
        "details": [
            (
                "LAB-0201: ไฟล์ .github/ISSUE_TEMPLATE/bug_report.yml (Copy-Paste Ready)",
                """name: Bug Report (แจ้งบั๊ก Firmware)
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
      required: true

  - type: textarea
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
        - label: ทดสอบบน branch develop หรือ release ล่าสุดแล้ว
          required: true""",
            ),
            (
                "LAB-0202: ไฟล์ .github/ISSUE_TEMPLATE/feature_request.yml และ config.yml (Copy-Paste Ready)",
                """# --- วางลงใน .github/ISSUE_TEMPLATE/feature_request.yml ---
name: Feature Request (ขอฟีเจอร์ใหม่)
description: เสนอฟีเจอร์ใหม่หรือการปรับปรุงสำหรับโปรเจกต์ ESP32
title: "[Feat]: "
labels: ["enhancement"]
body:
  - type: textarea
    id: problem
    attributes:
      label: ปัญหาหรือความต้องการ (Why)
      description: อธิบายว่าทำไมถึงต้องมีฟีเจอร์นี้
      placeholder: เช่น ต้องการปรับความถี่ไฟกระพริบตามค่า Input เพื่อแสดงสถานะการเชื่อมต่อ
    validations:
      required: true

  - type: textarea
    id: solution
    attributes:
      label: แนวทางที่เสนอ (How)
      description: ระบุฟังก์ชันหรือไฟล์ที่คาดว่าจะเพิ่ม/แก้ไข (เช่น lib/blink_math)
      placeholder: เพิ่มฟังก์ชันใน lib/blink_math/ และเขียน Unit Test รองรับ
    validations:
      required: true

  - type: dropdown
    id: target_branch
    attributes:
      label: Branch เป้าหมาย (Linear History + Rebase)
      options:
        - main (PR + Rebase and merge)
        - release/v* (เฉพาะแก้บั๊กก่อนปล่อยเวอร์ชัน)
      default: 0

# --- วางลงใน .github/ISSUE_TEMPLATE/config.yml ---
blank_issues_enabled: false
contact_links:
  - name: คู่มือ Workshop (Docs)
    url: https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms
    about: เอกสารอ้างอิงไวยากรณ์ YAML สำหรับ GitHub Issue Forms""",
            ),
            (
                "LAB-0203: เปิด Pull Request เข้า main และ Merge แบบ Rebase + ลบ Branch (Terminal)",
                """# 1. Push branch ขึ้น Fork ของตัวเอง
git push -u origin feature/fast-blink

# 2. เปิด PR เข้า main (GitHub จะโหลด .github/pull_request_template.md อัตโนมัติ)
gh pr create --base main --fill

# 3. หลังผ่าน Review และ CI สีเขียว -> Rebase & Merge และลบ branch ทิ้ง
gh pr merge --rebase --delete-branch

# 4. ตั้ง Branch Protection บน GitHub:
# Settings -> Branches -> Add rule (main):
#   [x] Require a pull request before merging
#   [x] Require status checks to pass before merging
#   [x] Require linear history""",
            ),
        ],
        "expected_output": """$ gh pr create --base main --fill
https://github.com/<your-username>/git-practice/pull/1

$ gh pr merge 1 --rebase --delete-branch
✓ Rebased and merged pull request #1 (feat(blink): support fast blink interval)
✓ Deleted branch feature/fast-blink""",
        "results": [
            "LAB-0201: สังเกตหน้าจอ New Issue เมื่อมีไฟล์ <code>.yml</code> ใน <code>.github/ISSUE_TEMPLATE/</code>",
            "LAB-0202: ผลการตั้ง Branch Protection และสถานะหลัง Rebase &amp; Merge PR",
        ],
        "questions": [
            "Q1: การใช้ Issue Form แบบ <code>.yml</code> ดีกว่าการปล่อยให้กรอก Issue แบบข้อความเปล่าอย่างไร?",
            "Q2: ตัวเลือก <strong>Require linear history</strong> ใน Branch Protection ช่วยป้องกันอะไร?",
            "Q3: ทำไมหลัง Merge PR เข้า <code>main</code> แล้วจึงควรลบ Branch ย่อยทิ้งทันที?",
        ],
        "exercise": {
            "code": "LAB-0204",
            "desc": "เปิด Issue 1 รายการด้วยฟอร์ม <code>feature_request.yml</code> จากนั้นสร้าง PR เพื่อปิด Issue นั้นและตรวจด้วย <code>verify.py</code>",
            "snippet": """# ในรายละเอียด PR ให้ใส่: Closes #1 (เลข Issue ที่เปิดไว้)
uv run exercises/verify.py --module 2""",
        },
        "screenshots": [
            ("../images/gh-02-issue-templates.png", "ไฟล์ .github/ISSUE_TEMPLATE/*.yml ใน Repository"),
            ("../images/gh-02-issues.png", "หน้าจอเลือก Issue Template (YAML Forms) บน GitHub"),
            ("../images/gh-03-pulls.png", "หน้า Pull Requests บน GitHub"),
            ("../images/gh-03-pr-detail.png", "รายละเอียด Pull Request #1 ที่ผ่าน CI และ Merge แบบ Rebase"),
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
            "<code>uv</code> (<code>uv tool install pre-commit</code>)",
            "ไฟล์ปลายทาง: <code>.pre-commit-config.yaml</code> และ <code>.clang-format</code>",
            "วิดีโอประกอบ: <code>videos/03-pre-commit-hooks.mp4</code>",
        ],
        "experiments": [
            ("LAB-0301", "(install) ก๊อปวาง <code>.pre-commit-config.yaml</code> และติดตั้ง Hook ทั้ง 2 ประเภท (<code>pre-commit</code> และ <code>commit-msg</code>)"),
            ("LAB-0302", "(break-fix) ทดลองจัดฟอร์แมตโค้ดให้เพี้ยน + พิมพ์ Commit Message ผิด เพื่อสังเกตการทำงานของ Hook"),
        ],
        "details": [
            (
                "LAB-0301: ไฟล์ .pre-commit-config.yaml และ .clang-format (Copy-Paste Ready)",
                """# --- วางลงใน .pre-commit-config.yaml (Root ของ Repo) ---
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v6.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=500']

  - repo: https://github.com/pre-commit/mirrors-clang-format
    rev: v23.1.5
    hooks:
      - id: clang-format
        types_or: [c++, c]

  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: v4.5.0
    hooks:
      - id: conventional-pre-commit
        stages: [commit-msg]
        args: [feat, fix, docs, style, refactor, test, ci, chore, build]

# --- ไฟล์ .clang-format (มีให้ใน Repo แล้ว) ---
# BasedOnStyle: Google
# IndentWidth: 2
# ColumnLimit: 100
# SortIncludes: false""",
            ),
            (
                "LAB-0302: ติดตั้ง Hook และทดสอบ Break-Fix (Terminal)",
                """# 1. ติดตั้ง pre-commit ด้วย uv และผูกเข้ากับ .git/hooks/
uv tool install pre-commit
pre-commit install
pre-commit install --hook-type commit-msg

# 2. รันตรวจทุกไฟล์ทันที:
pre-commit run --all-files

# 3. ทดลองทำให้ Hook บล็อก (จัดย่อหน้าผิด + commit message ผิด):
git add workshop/src/main.cpp
git commit -m "bad commit message"

# 4. clang-format จะแก้ไฟล์ให้ -> ต้อง git add ใหม่แล้ว Commit ด้วย prefix ที่ถูกต้อง:
git add workshop/src/main.cpp
git commit -m "style: format main.cpp with clang-format" """,
            ),
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
            "VS Code + PlatformIO IDE (<code>pio</code>)",
            "Windows: MinGW/WinLibs (<code>gcc</code>/<code>g++</code>) ใน PATH สำหรับรัน <code>[env:native]</code>",
            "ไฟล์ปลายทาง: <code>workshop/platformio.ini</code>, <code>workshop/test/test_native/test_main.cpp</code>, <code>workshop/test/test_esp32/test_hardware.cpp</code>",
            "วิดีโอประกอบ: <code>videos/04-platformio-unit-testing.mp4</code>",
        ],
        "experiments": [
            ("LAB-0401", "(native-test) ก๊อปวางตั้งค่า <code>workshop/platformio.ini</code> และเขียน Unit Test ครบ 4 ฟังก์ชันใน <code>test_main.cpp</code>"),
            ("LAB-0402", "(esp32-build) ศึกษา <code>test_hardware.cpp</code> และรัน <code>pio test -e native -v</code> เทียบกับ <code>pio run -e esp32doit-devkit-v1</code>"),
        ],
        "details": [
            (
                "LAB-0401: ไฟล์ workshop/platformio.ini (Copy-Paste Ready)",
                """[env:esp32doit-devkit-v1]
platform = espressif32
board = esp32doit-devkit-v1
framework = arduino
monitor_speed = 115200
test_filter = test_esp32

[env:native]
platform = native
test_build_src = no
test_filter = test_native""",
            ),
            (
                "LAB-0402: ไฟล์ workshop/test/test_native/test_main.cpp (Copy-Paste Ready)",
                """#include <unity.h>
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
}

int main(int argc, char** argv) {
  UNITY_BEGIN();
  RUN_TEST(test_add_numbers_positive);
  RUN_TEST(test_clamp_interval_bounds);
  RUN_TEST(test_next_led_state_toggles);
  RUN_TEST(test_calculate_cycle_ms);
  return UNITY_END();
}""",
            ),
            (
                "LAB-0403: ไฟล์ workshop/test/test_esp32/test_hardware.cpp และคำสั่งรัน Test/Build",
                """// --- วางลงใน workshop/test/test_esp32/test_hardware.cpp ---
#include <Arduino.h>
#include <unity.h>
#include "blink_math.h"

#ifndef LED_BUILTIN
#define LED_BUILTIN 2
#endif

void setUp(void) { pinMode(LED_BUILTIN, OUTPUT); }
void tearDown(void) { digitalWrite(LED_BUILTIN, LOW); }

void test_led_pin_toggle_hardware(void) {
  uint8_t state = blink_math::next_led_state(LOW);
  digitalWrite(LED_BUILTIN, state);
  delay(50);
  TEST_ASSERT_EQUAL_UINT8(HIGH, state);
}

void setup() {
  delay(2000);
  UNITY_BEGIN();
  RUN_TEST(test_led_pin_toggle_hardware);
  UNITY_END();
}

void loop() {}

// --- คำสั่งรันใน Terminal ---
// pio test -d workshop -e native -v
// pio run -d workshop -e esp32doit-devkit-v1
// pio test -d workshop -e esp32doit-devkit-v1   (เมื่อต่อบอร์ดจริง)""",
            ),
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
            ("LAB-0501", "(yaml-anatomy) ก๊อปวาง <code>.github/workflows/ci.yml</code> ฉบับเต็มและตรวจเวอร์ชัน Actions ใน GitHub Marketplace"),
            ("LAB-0502", "(break-fix) ทดลองทำให้ Unit Test พังใน PR เพื่อดู CI แดง จากนั้นแก้ให้กลับมาเขียว"),
        ],
        "details": [
            (
                "LAB-0501: ไฟล์ .github/workflows/ci.yml ฉบับเต็ม (Copy-Paste Ready)",
                """name: CI - Lint, Test & Build

on:
  push:
    branches:
      - main
      - 'release/**'
  pull_request:
    branches:
      - main

defaults:
  run:
    working-directory: workshop

jobs:
  lint:
    name: Code Format & Lint Check
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v7

      - name: Set up uv
        uses: astral-sh/setup-uv@v10.3.3
        with:
          python-version: '3.12'
          enable-cache: false

      - name: Run pre-commit checks
        uses: pre-commit/action@v3.0.1

  unit-test:
    name: Native Unit Tests (Unity)
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - name: Checkout repository
        uses: actions/checkout@v7

      - name: Set up uv
        uses: astral-sh/setup-uv@v10.3.3
        with:
          python-version: '3.12'
          enable-cache: false

      - name: Cache PlatformIO
        uses: actions/cache@v6
        with:
          path: ~/.platformio/.cache
          key: ${{ runner.os }}-pio-native-${{ hashFiles('workshop/platformio.ini') }}

      - name: Install PlatformIO with uv
        run: uv tool install platformio

      - name: Run Native Unit Tests
        run: pio test -e native -v

  build-esp32:
    name: Build Firmware (esp32doit-devkit-v1)
    runs-on: ubuntu-latest
    needs: unit-test
    steps:
      - name: Checkout repository
        uses: actions/checkout@v7

      - name: Set up uv
        uses: astral-sh/setup-uv@v10.3.3
        with:
          python-version: '3.12'
          enable-cache: false

      - name: Cache PlatformIO
        uses: actions/cache@v6
        with:
          path: ~/.platformio
          key: ${{ runner.os }}-pio-esp32-${{ hashFiles('workshop/platformio.ini') }}

      - name: Install PlatformIO with uv
        run: uv tool install platformio

      - name: Build ESP32 Firmware
        run: pio run -e esp32doit-devkit-v1

      - name: Upload Release Candidate Artifact
        if: startsWith(github.ref, 'refs/heads/release/')
        uses: actions/upload-artifact@v7
        with:
          name: rc-firmware-${{ github.sha }}
          path: |
            workshop/.pio/build/esp32doit-devkit-v1/firmware.bin
            workshop/.pio/build/esp32doit-devkit-v1/bootloader.bin
            workshop/.pio/build/esp32doit-devkit-v1/partitions.bin
          retention-days: 7""",
            ),
            (
                "LAB-0502: วิธีค้นหา Action (uses:) และตรวจสอบสถานะ CI ผ่าน CLI",
                """# 1. ค้นหาที่ GitHub Marketplace: https://github.com/marketplace?type=actions
# 2. ตรวจสอบเลข Tag ล่าสุดผ่าน GitHub CLI (หลีกเลี่ยง tag ที่ไม่มีอยู่จริง):
gh api repos/actions/checkout/releases/latest --jq .tag_name
gh api repos/astral-sh/setup-uv/releases/latest --jq .tag_name

# 3. ตรวจสอบรายการรัน CI ล่าสุด
gh run list --workflow ci.yml --limit 3""",
            ),
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
            ("../images/gh-04-actions-list.png", "รายการ Workflow Runs ในแท็บ Actions"),
            ("../images/gh-04-actions.png", "รายละเอียด Jobs ทั้ง 3 ขั้นตอนใน GitHub Actions"),
            ("../images/gh-05-actions-graph.png", "กราฟ CI 3 Jobs สีเขียวจริงบน SavEe2429/git-practice"),
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
            "ไฟล์ปลายทาง: <code>.github/workflows/release.yml</code>",
            "เครื่องมือ Flash: <code>esptool</code> หรือเว็บ <code>https://espressif.github.io/esptool-js/</code>",
            "วิดีโอประกอบ: <code>videos/06-github-actions-release.mp4</code>",
        ],
        "experiments": [
            ("LAB-0601", "(tag-release) ก๊อปวาง <code>.github/workflows/release.yml</code> ฉบับเต็ม และติด Tag <code>v1.0.0</code> บน <code>main</code>"),
            ("LAB-0602", "(flash-bin) ตรวจสอบไฟล์ Asset ในหน้า GitHub Releases และคำสั่ง Flash ด้วย <code>esptool</code>"),
        ],
        "details": [
            (
                "LAB-0601: ไฟล์ .github/workflows/release.yml ฉบับเต็ม (Copy-Paste Ready)",
                """name: Release Firmware (CD)

on:
  push:
    tags:
      - 'v*.*.*'

permissions:
  contents: write

defaults:
  run:
    working-directory: workshop

jobs:
  release:
    name: Build & Publish ESP32 Release
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v7

      - name: Set up uv
        uses: astral-sh/setup-uv@v10.3.3
        with:
          python-version: '3.12'
          enable-cache: false

      - name: Cache PlatformIO
        uses: actions/cache@v6
        with:
          path: ~/.platformio
          key: ${{ runner.os }}-pio-esp32-${{ hashFiles('workshop/platformio.ini') }}

      - name: Install PlatformIO & esptool with uv
        run: |
          uv tool install platformio
          uv tool install esptool

      - name: Run Native Unit Tests before Release
        run: pio test -e native

      - name: Build ESP32 Firmware
        run: pio run -e esp32doit-devkit-v1

      - name: Prepare Release Binaries
        shell: bash
        run: |
          mkdir -p dist
          BUILD_DIR=".pio/build/esp32doit-devkit-v1"
          cp "${BUILD_DIR}/firmware.bin" "dist/esp32doit-${GITHUB_REF_NAME}-firmware.bin"

          # Merge bootloader, partitions, and firmware into a single flashable binary (at 0x0)
          esptool --chip esp32 merge-bin \\
            -o "dist/esp32doit-${GITHUB_REF_NAME}-merged-firmware.bin" \\
            --flash_mode dio \\
            --flash_freq 40m \\
            --flash_size 4MB \\
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
            ),
            (
                "LAB-0602: การติด Tag และนำ merged-firmware.bin ไป Flash ลงบอร์ด ESP32 จริง (Terminal)",
                """# 1. ตรวจสอบว่า main อัปเดตล่าสุดและ CI เขียวแล้ว จากนั้นติด Tag และ Push:
git checkout main
git pull origin main
git tag -a v1.0.0 -m "release: v1.0.0"
git push origin v1.0.0

# 2. Flash ผ่าน Terminal ด้วย uv / esptool (เปลี่ยน COM3 เป็นพอร์ตของบอร์ด):
uv tool install esptool
esptool --chip esp32 --port COM3 --baud 460800 write-flash 0x0 esp32doit-v1.0.0-merged-firmware.bin

# 3. หรือ Flash ผ่านเว็บเบราว์เซอร์ (ไม่ต้องลงโปรแกรม):
# เปิด https://espressif.github.io/esptool-js/ -> Connect -> ใส่ Address 0x0 -> เลือก merged-firmware.bin""",
            ),
        ],
        "expected_output": """$ gh release list --limit 3
TITLE   TYPE    TAG NAME  PUBLISHED
v0.1.0  Latest  v0.1.0    about 1 minute ago

$ uv run exercises/verify.py --all
...
Summary: 17 PASS | 0 FAIL | 0 WARN (All modules verified)""",
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
            ("../images/gh-05-releases.png", "หน้า GitHub Release v0.1.0 พร้อมไฟล์ firmware.bin และ merged-firmware.bin"),
            ("../images/term-04-verify.png", "ตัวอย่างผลรัน uv run exercises/verify.py --all"),
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

  <h3 class="sec" style="text-decoration: underline;">รายละเอียดการทดลองและโค้ดฉบับเต็ม (Copy-Paste Ready):</h3>
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
    details_html = "".join(
        f'<div class="exp-row"><strong>{heading}</strong></div><div class="code-box">{html.escape(code)}</div>'
        for heading, code in lab["details"]
    )
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
