# Video Scripts & Storyboards (ประกอบคู่มือทั้ง 6 Modules)

ไฟล์นี้เป็นสคริปต์และ Storyboard สำหรับวิดีโอ MP4 ทั้ง 6 ตอนในโฟลเดอร์ `videos/` (สามารถใช้คู่กับวิดีโอที่สร้างอัตโนมัติ หรือใช้อัดเสียงพากย์/อัดหน้าจอเพิ่มเติมได้)

---

## 01. Linear History (Rebase) & Conventional Commits (`01-gitflow-branching.mp4`)
- **ความยาว:** ~20 วินาที (Demo Flow)
- **Scene 1 (Why):** แสดงภาพ `main` เส้นตรงด้วย Rebase เทียบกับ Merge Commit ที่พันกันเป็นใยแมงมุม
- **Scene 2 (Terminal):** Fork → Clone → `git checkout -b feature/fast-blink main` → `git rebase origin/main`
- **Scene 3 (Commit):** รัน `git commit -m "feat(blink): add fast blink preset"` → ตรวจผ่านด้วย `verify.py --module 1`

## 02. Issue Forms (`.yml`), Pull Request & Rebase Merge (`02-pull-request-review.mp4`)
- **ความยาว:** ~20 วินาที
- **Scene 1 (Issue & Push):** แสดง Issue Form (`.yml`) + `git push -u origin feature/fast-blink`
- **Scene 2 (PR Template):** `gh pr create --base main --fill` แสดง Checklist จาก `.github/pull_request_template.md`
- **Scene 3 (Review & Rebase Merge):** แสดงสถานะ CI Check + `Require linear history` → `gh pr merge --rebase --delete-branch`

## 03. Pre-commit Hooks (`03-pre-commit-hooks.mp4`)
- **ความยาว:** ~20 วินาที
- **Scene 1 (Install):** `pre-commit install` และ `pre-commit install --hook-type commit-msg`
- **Scene 2 (Fail Demo):** ลอง `git commit -m "bad msg"` → แสดง `clang-format` แก้ไฟล์และ `conventional-pre-commit` บล็อกข้อความ
- **Scene 3 (Pass):** แก้เป็น `git commit -m "style: format main.cpp"` → `[PASS]`

## 04. PlatformIO Unit Testing (`04-platformio-unit-testing.mp4`)
- **ความยาว:** ~20 วินาที
- **Scene 1 (Architecture):** แผนภาพแยก `lib/blink_math` (Pure C++) ออกจาก `src/main.cpp` (`Arduino.h`)
- **Scene 2 (Native Test):** รัน `pio test -e native -v` → แสดงผล Unity `4 Tests 0 Failures` (PASSED)
- **Scene 3 (ESP32 Build):** รัน `pio run -e esp32doit-devkit-v1` → `[SUCCESS]`

## 05. GitHub Actions CI (`05-github-actions-ci.mp4`)
- **ความยาว:** ~20 วินาที
- **Scene 1 (Pipeline):** แสดง Workflow 3 Jobs: `lint` → `unit-test` → `build-esp32`
- **Scene 2 (Run Log):** จำลองการรันบน `ubuntu-latest` พร้อม Cache `.platformio` และ Upload Artifact บน `release/*`
- **Scene 3 (Status):** แสดงผลสีเขียวบน PR Status Check

## 06. GitHub Actions Release (`06-github-actions-release.mp4`)
- **ความยาว:** ~20 วินาที
- **Scene 1 (Release Branch & CI):** `git checkout -b release/v1.0.0 main` → Push ให้ `ci.yml` ผ่าน → Rebase & Merge เข้า `main` และลบ branch
- **Scene 2 (Tag & Merge Bin):** `git tag -a v1.0.0 -m "release: v1.0.0"` → `git push origin v1.0.0` → `esptool.py merge_bin`
- **Scene 3 (Release):** แสดงหน้า GitHub Release `v1.0.0` พร้อมไฟล์แนบทั้ง `firmware.bin` และ `merged-firmware.bin`
