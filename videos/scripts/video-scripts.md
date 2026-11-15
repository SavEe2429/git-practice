# Video Scripts & Storyboards (ประกอบคู่มือทั้ง 6 Modules)

ไฟล์นี้เป็นสคริปต์และ Storyboard สำหรับวิดีโอ Motion Graphic แบบกระชับ (**15–18 วินาที**) ในธีมสีหิมะ ขาว-น้ำเงิน (**Snow & Arctic Blue** `#F4F8FC`) รูปแบบ **Command/Event (CLI ภาษาอังกฤษล้วน) → Detector/Gate → Visual Reaction + ภาพผลลัพธ์จริงจาก `docs/images/`** ความละเอียด `1280x720` @ `24fps` (Silent Visual Loop) ที่สร้างจาก `videos/scripts/generate_videos.py`

---

## 01. Linear History (Rebase) & Conventional Commits (`01-gitflow-branching.mp4`, 15s)
- **ขั้นตอน 1/3:** `git switch -c feature/fast-blink` → แตกสายจาก `main` (`C1`) แล้วสร้าง Commit `C2`, `C3`
- **ขั้นตอน 2/3:** `git fetch origin  # main updated with C4` → `main` มีอัปเดต `C4` (เตือนปม Merge ไขว้)
- **ขั้นตอน 3/3:** `git rebase origin/main` → ยก `C2`, `C3` ต่อท้าย `C4` เป็นเส้นตรงเส้นเดียว + แสดงภาพจริง `docs/images/term-01-git-log.png`

## 02. Issue Forms, Pull Request & Rebase Merge (`02-pull-request-review.mp4`, 16s)
- **ขั้นตอน 1/3:** `gh issue create --template bug_report.yml` → เปิด **Issue #2**
- **ขั้นตอน 2/3:** `gh pr create --base main --body "Closes #2"` → ด่าน **Branch Protection** ตรวจ Checklist + CI ผ่าน → ปลดล็อก Merge
- **ขั้นตอน 3/3:** `gh pr merge 3 --rebase --delete-branch` → ต่อท้าย `main` + ลบ branch + ปิด Issue #2 + แสดงภาพจริง `docs/images/gh-03-pr-detail.png`

## 03. Pre-commit Hooks (`03-pre-commit-hooks.mp4`, 15s)
- **ขั้นตอน 1/3:** `git commit -m "add blink"` → Layout 2 ช่อง: `clang-format` จัดรูปโค้ด + `conventional-pre-commit` **BLOCKED**
- **ขั้นตอน 2/3:** `git commit -m "feat: add blink"` → **ใช้ Layout 2 ช่องชุดเดิม** เปลี่ยนสถานะเป็นสีเขียว **PASS** ทั้งหมด
- **ขั้นตอน 3/3:** `pre-commit run --all-files` → แสดงภาพจริง `docs/images/term-02-pre-commit.png`

## 04. PlatformIO Unit Testing (`04-platformio-unit-testing.mp4`, 15s)
- **ขั้นตอน 1/3:** `ls lib/blink_math/ src/main.cpp  # Decoupled` → แยก `blink_math.cpp` ออกจาก `main.cpp`
- **ขั้นตอน 2/3:** `pio test -e native` → รัน Unit Test บน PC (**PASS 3/3 < 1s**)
- **ขั้นตอน 3/3:** `pio run -e esp32doit-devkit-v1` → ได้ `firmware.bin` + แสดงภาพจริง `docs/images/term-03-pio-build.png`

## 05. GitHub Actions CI (`05-github-actions-ci.mp4`, 15s)
- **ขั้นตอน 1/3:** `git push origin feature/fast-blink` → ด่าน `on: [push, pull_request]` **TRIGGERED** เปิด `ubuntu-latest`
- **ขั้นตอน 2/3:** `gh run watch` → รัน **`lint`** + **`test-native`** ขนานกัน
- **ขั้นตอน 3/3:** `gh run list --workflow ci.yml` → **`build-esp32`** ผ่าน + แสดงภาพจริง `docs/images/gh-05-actions-graph.png`

## 06. GitHub Actions Release (`06-github-actions-release.mp4`, 18s)
- **ขั้นตอน 1/4:** `git tag -a v1.0.0 -m "release: v1.0.0"` → ป้าย Tag **`v1.0.0`** ปรากฏบน Commit บน `main`
- **ขั้นตอน 2/4:** `git push origin v1.0.0` → ด่าน `tags: ['v*.*.*']` ตรงกัน → **TRIGGERED `release.yml`!**
- **ขั้นตอน 3/4:** `esptool merge-bin -o merged-firmware.bin ...` → รวม 4 ไฟล์ (`bootloader` + `partitions` + `boot_app0` + `firmware`) เป็น `merged-firmware.bin`
- **ขั้นตอน 4/4:** `gh release view v1.0.0` → แสดง Asset `firmware.bin` (OTA) & `merged-firmware.bin` (`0x0`) + ภาพจริง `docs/images/gh-05-releases.png`
