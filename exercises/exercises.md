# แบบฝึกหัดและเกณฑ์ประเมินผล (Exercises & Pass Criteria)

โฟลเดอร์นี้รวมโจทย์ฝึกปฏิบัติทั้ง **6 Modules** (จับคู่กับใบงาน **7 ฉบับ: `LAB00–LAB06`**) สำหรับโปรเจกต์ [workshop/](../workshop) พร้อมระบบตรวจผลแบบ **Hybrid**:
1. **สคริปต์ตรวจอัตโนมัติ:** รันจากโฟลเดอร์ root ของ Repo ด้วย `uv run exercises/verify.py --module <1-6>` หรือ `--all` (ใช้ `python exercises/verify.py ...` แทนก็ได้เช่นกัน)
2. **Visual Checklist:** ตารางเช็กเกณฑ์ผ่านด้วยตาบน GitHub UI / Terminal
   - *หมายเหตุ:* เกณฑ์ออนไลน์ใน Module 2 (Merged PR), Module 5 (CI run) และ Module 6 (GitHub Release) จะตรวจผ่านต่อเมื่อ Push ขึ้น Fork บน `github.com` และ `gh auth login` แล้วเท่านั้น (หากทดสอบแบบ Offline / local remote จะขึ้น `[WARN]` แทน `[FAIL]`)

---

## วิธีเตรียมเครื่องและใช้งาน `verify.py` (ใช้ `uv` หรือ `python`)
> **ก่อนเริ่ม Module 1:** ทำตามใบงาน **LAB 00 (Environment Setup)** ให้เรียบร้อยเพื่อลง `git`, `uv`, `pre-commit`, `platformio`, `esptool`, `gh`, `gcc` และพรีโหลดแพ็กเกจ ESP32 ครบในที่เดียว จากนั้น `cd` เข้าโฟลเดอร์ root ของ Repo (`git-practice`) แล้วเช็กความพร้อมด้วยคำสั่งด้านล่าง:

```powershell
# 0. เช็กความพร้อมเครื่องก่อนเริ่ม (รายละเอียดการติดตั้งทั้งหมดอยู่ใน LAB 00)
uv run exercises/check_env.py

# 1. ตรวจเฉพาะ Module 1 (ใช้ python แทน uv run ได้เหมือนกัน)
uv run exercises/verify.py --module 1

# 2. ตรวจทั้งหมด Modules 1-6
uv run exercises/verify.py --all
```
> หมายเหตุ:
> - ตามโครงสร้าง **Option A** โฟลเดอร์ `.github/` และ `.pre-commit-config.yaml` จะวางไว้ที่ **Root ของ Repo** ส่วนโค้ด PlatformIO อยู่ใน `workshop/` (จึงต้องมี `defaults: run: working-directory: workshop` ในไฟล์ `.yml`)
> - คำสั่งในเอกสารนี้แยกคนละบรรทัดแทน `&&` เพื่อให้รันได้ทั้งบน **Windows PowerShell 5.1**, PowerShell 7 และ Bash

---

## แบบฝึกหัดทั้ง 6 Modules

### Module 1: Linear History (Rebase), Fork Workflow & Conventional Commits
**เป้าหมาย:** Fork Repo เพื่อแยกพื้นที่ทำงาน (รองรับผู้เรียน 20+ คนไม่ชนกัน), รักษา `main` ให้เป็นเส้นตรงด้วย `git rebase` จาก `upstream/main`, แก้ Conflict และเขียน Commit Message ตามมาตรฐาน
- **โจทย์:**
  1. กด **Fork** Repository หลักไปยัง GitHub Account ของตัวเอง แล้ว `git clone` ลงเครื่อง พร้อมเพิ่ม `upstream` remote (`git remote add upstream https://github.com/SavEe2429/git-practice.git`)
  2. แตก branch `feature/fast-blink` จาก `main` (`git switch -c feature/fast-blink main`) แล้วแก้บรรทัดที่ 15 ใน `workshop/src/main.cpp` (`clamp_interval(500)` → `clamp_interval(200)`)
  3. Commit ด้วยรูปแบบ Conventional Commits เช่น `feat(blink): support fast blink preset`
  4. ฝึกอัปเดตฐานให้ทัน Repo ต้นทางด้วย `git fetch upstream` แล้วตามด้วย `git rebase upstream/main` (ไม่สร้าง merge commit) และถ้ามี Conflict ให้แก้แล้วรัน `git add <file>` ต่อด้วย `git rebase --continue` จากนั้น Push ขึ้น Fork ด้วย `git push --force-with-lease -u origin feature/fast-blink`
- **เกณฑ์ผ่าน:**
  - [ ] มี branch `main` ที่ประวัติเป็นเส้นตรง (Linear History) และมี branch `feature/*` ที่มี commit ใหม่ต่อจาก `main`
  - [ ] ข้อความ commit ขึ้นต้นด้วย `feat:`, `fix:`, `docs:` ฯลฯ ตามมาตรฐาน
  - [ ] `uv run exercises/verify.py --module 1` ขึ้น `[PASS]`

---

### Module 2: Issue Forms (`.yml`), Pull Request (Rebase) & Branch Protection
**เป้าหมาย:** สร้างแบบฟอร์ม Issue ด้วย YAML, ใช้/ปรับปรุง PR Template, ทำ Code Review และตั้งค่า Branch Protection บังคับ Linear History
- **โจทย์:**
  1. แทนที่ไฟล์ Issue Forms Skeleton ใน `.github/ISSUE_TEMPLATE/`: `bug_report.yml`, `feature_request.yml` และ `config.yml` ตามใบงาน **LAB 02** (อ้างอิงเฉลยที่ `exercises/solutions/.github/ISSUE_TEMPLATE/`)
  2. ตรวจสอบ (หรือปรับแต่งเพิ่มเติม) ไฟล์ `.github/pull_request_template.md` ที่มีให้ใน Repo แล้ว นำไฟล์ทั้งหมดขึ้น `main` บน Fork ของตัวเองก่อน (GitHub อ่าน Issue Template จาก `main` เท่านั้น)
  3. ลองเปิด Issue ใหม่บน GitHub Fork ของตัวเอง เพื่อดูหน้าตาฟอร์ม Dropdown/Input/Checkbox ที่สร้างจากไฟล์ `.yml`
  4. Push `feature/fast-blink` ขึ้น Fork แล้วเปิด Pull Request เข้า **`main`** (ผ่านเว็บ GitHub หรือ VS Code Extension) และตั้ง Branch Protection / Ruleset บน `main` โดยติ๊ก **Require linear history**
  5. Review และ Merge PR เข้า `main` ด้วย **Rebase and merge** (`gh pr merge --rebase --delete-branch`) — และหากใช้เครื่องรวม อย่าลืม Logout ออกจาก VS Code, `gh` และ Browser
- **เกณฑ์ผ่าน:**
  - [ ] หน้า **Issues → New Issue** บน GitHub แสดงฟอร์ม Dropdown/Input/Checkbox จากไฟล์ `.yml`
  - [ ] หน้า PR บน GitHub แสดง Checklist จาก Template อัตโนมัติ
  - [ ] มี PR ที่ถูก Rebase & Merge เข้า `main` แล้ว
  - [ ] `uv run exercises/verify.py --module 2` ขึ้น `[PASS]`

---

### Module 3: Pre-commit Hooks (Quality Gate)
**เป้าหมาย:** ป้องกันโค้ดผิดฟอร์แมตและข้อความ Commit ผิดรูปแบบก่อนเข้า Git History
- **โจทย์:**
  1. ตรวจสอบไฟล์ `.clang-format` ที่มีให้แล้วที่ root และแทนที่เนื้อหาใน `.pre-commit-config.yaml` (ลบ `repos: []` และ `# TODO`) ตามใบงาน **LAB 03** แล้วรัน `git add .pre-commit-config.yaml` ก่อนเสมอ
  2. ติดตั้ง hook ทั้ง `pre-commit` และ `commit-msg` (`pre-commit install` และ `pre-commit install --hook-type commit-msg`)
  3. **ทดลอง Break-Fix แบบแยก 2 ขั้น:**
     - **ขั้น A (Format Hook):** เพิ่มบรรทัดที่จัดช่องว่างผิดจงใจ เช่น `int   precommit_test =  1;` ท้ายฟังก์ชัน `setup()` ใน `workshop/src/main.cpp` แล้ว `git add workshop/src/main.cpp` → `git commit -m "style: test clang-format"` เพื่อดู hook บล็อกและจัดฟอร์แมตให้อัตโนมัติ → รัน `git add workshop/src/main.cpp` อีกรอบ
     - **ขั้น B (Commit-Msg Hook):** ลองรัน `git commit -m "bad commit message"` เพื่อดู hook `conventional-pre-commit` ปฏิเสธข้อความที่ไม่ถูกกติกา
  4. แก้ข้อความเป็น `git commit -m "style: format main.cpp with clang-format"` แล้ว Commit ให้ผ่าน (และ Commit `.pre-commit-config.yaml` ด้วย `chore(hooks): configure pre-commit`)
- **เกณฑ์ผ่าน:**
  - [ ] รัน `pre-commit run --all-files` ผ่านทุก hook
  - [ ] Commit ข้อความผิดรูปแบบถูกบล็อกจริง และข้อความถูกต้องผ่านได้
  - [ ] `uv run exercises/verify.py --module 3` ขึ้น `[PASS]`

---

### Module 4: PlatformIO Unit Testing
**เป้าหมาย:** เขียนและรัน Unity Unit Tests บน `[env:native]` พร้อมโครงสร้าง Test สำหรับบอร์ด ESP32 จริง
- **โจทย์:**
  1. แทนที่เนื้อหาใน `workshop/platformio.ini` (ลบ `; TODO`) เพื่อเพิ่ม `[env:native]` พร้อม `test_build_src = no` และ `test_filter = test_native`
  2. แทนที่เนื้อหาใน `workshop/test/test_native/test_main.cpp` (ลบ `test_starter_example` / `main()` เดิม) เพื่อเขียน Test Cases ทดสอบฟังก์ชันทั้งหมดใน `blink_math` อย่างน้อย 4 test cases
  3. ศึกษาไฟล์ `workshop/test/test_esp32/test_hardware.cpp` ที่มีให้ใน Repo สำหรับเทสบนบอร์ดจริง
  4. รัน `pio test -d workshop -e native -v` (บน Windows ต้องมี `gcc`/`g++` จาก MinGW/WinLibs ใน PATH — หากไม่มีและลงไม่ได้ ให้ใช้ `pio run -d workshop -e esp32doit-devkit-v1` แล้วตรวจผล `native` บน GitHub Actions ใน Module 5)
- **เกณฑ์ผ่าน:**
  - [ ] `pio test -d workshop -e native` แสดงผล `PASSED` ครบทุก test case (หรือขึ้น `[WARN]` ใน `verify.py` หากเครื่องไม่มี `gcc`)
  - [ ] `pio run -d workshop -e esp32doit-devkit-v1` คอมไพล์ผ่านปกติ
  - [ ] `uv run exercises/verify.py --module 4` ขึ้น `[PASS]` (ไม่มี `[FAIL]`)

---

### Module 5: GitHub Actions Continuous Integration (CI) & YAML Deep-Dive
**เป้าหมาย:** เข้าใจโครงสร้างไฟล์ `.yml`, รู้จักแหล่งค้นหา Actions จาก GitHub Marketplace และให้ CI ตรวจ Lint, Unit Test, Build อัตโนมัติทุก PR
- **โจทย์:**
  1. เปิด **GitHub Marketplace (`github.com/marketplace?type=actions`)** ค้นหา Action ที่ใช้ในงาน (เช่น `actions/checkout`, `astral-sh/setup-uv`, `actions/cache`, `pre-commit/action`) แล้วดูแท็บ **Usage** และเวอร์ชันล่าสุด (เช่น `@v7`, `@v6`, `@v3`)
  2. แทนที่ไฟล์ `.github/workflows/ci.yml` (ลบ `on: workflow_dispatch:` และ job `starter-placeholder:`) โดยกำหนด `on:`, `defaults.run.working-directory: workshop`, `jobs:` (`lint` → `unit-test` → `build-esp32` เชื่อมด้วย `needs:`), และ `steps:` (`uses:` / `with:` / `run:` / `if:`)
  3. ตั้งค่า Cache `~/.platformio` และอัปโหลด Build Artifact (`rc-firmware-*`) เฉพาะเมื่อ Push branch `release/*`
  4. เปิด PR จาก `feature/*` เข้า `main` ใน Fork ของตัวเอง แล้วดูผลลัพธ์สีเขียวบนแท็บ **Actions**
- **เกณฑ์ผ่าน:**
  - [ ] อธิบายความหมายของ `on`, `defaults.run.working-directory`, `jobs`, `needs`, `uses`, `with`, `run`, `if` ใน `ci.yml` ได้
  - [ ] แท็บ GitHub Actions แสดงเครื่องหมายถูกสีเขียวครบทั้ง 3 jobs
  - [ ] เมื่อสร้าง branch `release/v1.0.0` มี Artifact `rc-firmware-*` ให้ดาวน์โหลด
  - [ ] `uv run exercises/verify.py --module 5` ขึ้น `[PASS]`

### แบบฝึกหัดเสริม (Break & Fix Lab): จำลอง CI พัง & Merge Conflict
1. **CI แดง:** ลองแก้ `test_add_numbers_positive` ใน `workshop/test/test_native/test_main.cpp` ให้คาดหวังค่าผิด (เช่น `TEST_ASSERT_EQUAL_INT(99, ...)`) แล้ว Push เข้า PR → ดู CI ขึ้น ❌ สีแดงและบล็อก Merge → อ่าน Log แก้กลับเป็น `5` แล้ว Push จนเขียว ✅
2. **Merge Conflict:** แก้บรรทัดเดียวกันใน `workshop/src/main.cpp` บน 2 branches → Rebase & Merge อันแรกเข้า `main` → อีกอันจะติด Conflict → ฝึกแก้ด้วย `git fetch upstream` ตามด้วย `git rebase upstream/main` แล้วเลือกโค้ดที่ถูกต้อง, `git add workshop/src/main.cpp`, `git rebase --continue`

---

### Module 6: GitHub Actions Release (CD) & การ Flash ด้วย `esptool`
**เป้าหมาย:** ปล่อยเวอร์ชันเฟิร์มแวร์อัตโนมัติเมื่อ Merge เข้า `main` และติด Tag `v*.*.*` พร้อมนำไฟล์ไป Flash ลงบอร์ดจริง
- **โจทย์:**
  1. แทนที่ไฟล์ `.github/workflows/release.yml` (ลบ `workflow_dispatch:` และ `starter-placeholder:`) ให้ทำงานเมื่อ Push Tag `v*.*.*`
  2. ใช้ `esptool --chip esp32 merge-bin` รวม `bootloader.bin` + `partitions.bin` + `firmware.bin` เป็น `merged-firmware.bin`
  3. แตก branch `release/v1.0.0` จาก `main` → `git push -u origin release/v1.0.0` เพื่อให้ `ci.yml` รันตรวจผ่านสีเขียว
  4. เปิด PR เข้า `main` → กด **Rebase and merge** และลบ `release/v1.0.0` ทิ้ง (`main` ยังคงเป็นเส้นตรงเส้นเดียว)
  5. ติด Tag บน `main` (ทำทีละบรรทัดเพื่อให้รันได้ทั้ง PowerShell 5.1 และ Bash):
     ```powershell
     git switch main
     git pull origin main
     git tag -a v1.0.0 -m "release: v1.0.0"
     git push origin v1.0.0
     ```
  6. *(ถ้ามีบอร์ดจริง)* ดาวน์โหลด `esp32doit-v1.0.0-merged-firmware.bin` จากหน้า Releases แล้ว Flash ลงบอร์ดด้วย `esptool` (ติดตั้งไว้แล้วใน LAB 00):
     ```powershell
     esptool --chip esp32 --port COM3 --baud 460800 write-flash 0x0 esp32doit-v1.0.0-merged-firmware.bin
     ```
     *(หรือเปิดเว็บ [ESP Tool](https://espressif.github.io/esptool-js/) บน Chrome/Edge เสียบสาย USB แล้วเลือกไฟล์ที่ Address `0x0` ได้ทันทีโดยไม่ต้องลงโปรแกรม)*
  7. **Shared-PC Cleanup (สำคัญมากสำหรับเครื่องห้องแล็บ):** Sign Out ออกจาก VS Code (`Accounts -> Sign Out`), รัน `gh auth logout`, ล้าง Git Credential Manager (`cmdkey /list`), Sign Out บน Browser และลบโฟลเดอร์งานที่ Clone ไว้
- **เกณฑ์ผ่าน:**
  - [ ] หน้า **Releases** บน GitHub มีเวอร์ชัน `v1.0.0` พร้อม Release Notes อัตโนมัติ
  - [ ] มีไฟล์แนบครบทั้ง `esp32doit-v1.0.0-firmware.bin` และ `esp32doit-v1.0.0-merged-firmware.bin`
  - [ ] `uv run exercises/verify.py --all` ขึ้น `[PASS]` ครบทุกข้อที่ทำได้ (หรือ `[WARN]` 1 ข้อกรณีไม่มี `gcc`)
