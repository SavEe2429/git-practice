# แบบฝึกหัดและเกณฑ์ประเมินผล (Exercises & Pass Criteria)

โฟลเดอร์นี้รวมโจทย์ฝึกปฏิบัติทั้ง **6 Modules** สำหรับโปรเจกต์ [workshop/](../workshop) พร้อมระบบตรวจผลแบบ **Hybrid**:
1. **สคริปต์ตรวจอัตโนมัติ:** รัน `python exercises/verify.py --module <1-6>` หรือ `--all`
2. **Visual Checklist:** ตารางเช็กเกณฑ์ผ่านด้วยตาบน GitHub UI / Terminal

---

## วิธีเตรียมเครื่องและใช้งาน `verify.py` (ใช้ `uv`)
```bash
# 0. เช็กความพร้อมเครื่องก่อนเริ่ม (แนะนำทำล่วงหน้า)
uv run exercises/check_env.py

# 1. ตรวจเฉพาะ Module 1
uv run exercises/verify.py --module 1

# 2. ตรวจทั้งหมด 1-6
uv run exercises/verify.py --all
```
> หมายเหตุ: ตามโครงสร้าง **Option A** โฟลเดอร์ `.github/` และ `.pre-commit-config.yaml` จะวางไว้ที่ **Root ของ Repo** ส่วนโค้ด PlatformIO อยู่ใน `workshop/` (จึงต้องมี `defaults: run: working-directory: workshop` ในไฟล์ `.yml`)

---

## แบบฝึกหัดทั้ง 6 Modules

### Module 1: Linear History (Rebase), Fork Workflow & Conventional Commits
**เป้าหมาย:** Fork Repo เพื่อแยกพื้นที่ทำงาน (รองรับผู้เรียน 20+ คนไม่ชนกัน), รักษา `main` ให้เป็นเส้นตรงด้วย `git rebase`, และเขียน Commit Message ตามมาตรฐาน
- **โจทย์:**
  1. กด **Fork** Repository หลักไปยัง GitHub Account ของตัวเอง แล้ว `git clone` ลงเครื่อง
  2. แตก branch `feature/fast-blink` จาก `main` แล้วปรับค่า `blink_interval_ms` หรือเพิ่มฟังก์ชันใน `lib/blink_math/`
  3. Commit ด้วยรูปแบบ Conventional Commits เช่น `feat(blink): support fast blink preset`
  4. ฝึกอัปเดตให้ทัน `main` ด้วย `git fetch origin && git rebase origin/main` (ไม่สร้าง merge commit)
- **เกณฑ์ผ่าน:**
  - [ ] มี branch `main` ที่ประวัติเป็นเส้นตรง (Linear History)
  - [ ] ข้อความ commit ขึ้นต้นด้วย `feat:`, `fix:`, `docs:` ฯลฯ ตามมาตรฐาน
  - [ ] `python exercises/verify.py --module 1` ขึ้น `[PASS]`

---

### Module 2: Issue Forms (`.yml`), Pull Request (Rebase) & Branch Protection
**เป้าหมาย:** สร้างแบบฟอร์ม Issue ด้วย YAML, สร้าง PR Template, ทำ Code Review และตั้งค่า Branch Protection บังคับ Linear History
- **โจทย์:**
  1. สร้างไฟล์ Issue Forms ด้วย YAML ใน `.github/ISSUE_TEMPLATE/`: `bug_report.yml`, `feature_request.yml`, และ `config.yml` (อ้างอิงจาก `exercises/solutions/.github/ISSUE_TEMPLATE/`)
  2. สร้างไฟล์ `.github/pull_request_template.md`
  3. ลองเปิด Issue ใหม่บน GitHub Fork ของตัวเอง เพื่อดูหน้าตาฟอร์มที่สร้างจากไฟล์ `.yml`
  4. Push `feature/fast-blink` ขึ้น Fork แล้วเปิด Pull Request เข้า **`main`** (และตั้ง Branch Protection บน `main` โดยติ๊ก **Require linear history**)
  5. Review และ Merge PR เข้า `main` ด้วย **Rebase and merge** (`gh pr merge --rebase --delete-branch`)
- **เกณฑ์ผ่าน:**
  - [ ] หน้า **Issues → New Issue** บน GitHub แสดงฟอร์ม Dropdown/Input/Checkbox จากไฟล์ `.yml`
  - [ ] หน้า PR บน GitHub แสดง Checklist จาก Template อัตโนมัติ
  - [ ] มี PR ที่ถูก Rebase & Merge เข้า `main` แล้ว
  - [ ] `python exercises/verify.py --module 2` ขึ้น `[PASS]`

---

### Module 3: Pre-commit Hooks (Quality Gate)
**เป้าหมาย:** ป้องกันโค้ดผิดฟอร์แมตและข้อความ Commit ผิดรูปแบบก่อนเข้า Git History
- **โจทย์:**
  1. สร้าง `.pre-commit-config.yaml` และ `.clang-format`
  2. ติดตั้ง hook ทั้ง `pre-commit` และ `commit-msg`
  3. **ทดลองทำให้พัง:** ตั้งใจเว้นวรรคท้ายบรรทัดหรือจัดย่อหน้า `src/main.cpp` ให้เพี้ยน แล้วลอง `git commit -m "bad msg"` เพื่อดู Hook บล็อกและแก้ฟอร์แมตอัตโนมัติ
  4. แก้ข้อความเป็น `style: format main.cpp with clang-format` แล้ว Commit ใหม่อีกครั้ง
- **เกณฑ์ผ่าน:**
  - [ ] รัน `pre-commit run --all-files` ผ่านทุก hook
  - [ ] Commit ข้อความผิดรูปแบบถูกบล็อกจริง และข้อความถูกต้องผ่านได้
  - [ ] `python exercises/verify.py --module 3` ขึ้น `[PASS]`

---

### Module 4: PlatformIO Unit Testing
**เป้าหมาย:** เขียนและรัน Unity Unit Tests บน `[env:native]` พร้อมโครงสร้าง Test สำหรับบอร์ด ESP32 จริง
- **โจทย์:**
  1. เพิ่ม `[env:native]` ใน `workshop/platformio.ini` พร้อม `test_build_src = no` และ `test_filter`
  2. สร้างไฟล์ `test/test_native/test_main.cpp` ทดสอบฟังก์ชันทั้งหมดใน `blink_math` (อย่างน้อย 4 test cases)
  3. เพิ่มโครงสร้าง `test/test_esp32/test_hardware.cpp` สำหรับเทสบนบอร์ดจริง
  4. รัน `pio test -e native` (บน Windows ต้องมี `gcc`/`g++` จาก MinGW/WinLibs ใน PATH)
- **เกณฑ์ผ่าน:**
  - [ ] `pio test -e native` แสดงผล `PASSED` ครบทุก test case
  - [ ] `pio run -e esp32doit-devkit-v1` ยังคอมไพล์ผ่านปกติ
  - [ ] `python exercises/verify.py --module 4` ขึ้น `[PASS]`

---

### Module 5: GitHub Actions Continuous Integration (CI) & YAML Deep-Dive
**เป้าหมาย:** เข้าใจโครงสร้างไฟล์ `.yml`, รู้จักแหล่งค้นหา Actions จาก GitHub Marketplace และให้ CI ตรวจ Lint, Unit Test, Build อัตโนมัติทุก PR
- **โจทย์:**
  1. เปิด **GitHub Marketplace (`github.com/marketplace?type=actions`)** ค้นหา Action ที่ใช้ในงาน (เช่น `actions/checkout`, `actions/setup-python`, `actions/cache`, `pre-commit/action`) แล้วดูแท็บ **Usage** และเวอร์ชันล่าสุด (`@v4`, `@v5`)
  2. สร้าง `.github/workflows/ci.yml` โดยระบุ `on:` (Trigger), `jobs:` (`lint` → `unit-test` → `build-esp32` เชื่อมด้วย `needs:`), และ `steps:` (`uses:` / `with:` / `run:` / `if:`)
  3. ตั้งค่า Cache `~/.platformio` และอัปโหลด Build Artifact เฉพาะเมื่อ Push branch `release/*`
  4. เปิด PR จาก `feature/*` เข้า `main` ใน Fork ของตัวเอง แล้วดูผลลัพธ์สีเขียวบนแท็บ **Actions**
- **เกณฑ์ผ่าน:**
  - [ ] อธิบายความหมายของ `on`, `jobs`, `needs`, `uses`, `with`, `run`, `if` ใน `ci.yml` ได้
  - [ ] แท็บ GitHub Actions แสดงเครื่องหมายถูกสีเขียวครบทั้ง 3 jobs
  - [ ] เมื่อสร้าง branch `release/v1.0.0` มี Artifact `rc-firmware-*` ให้ดาวน์โหลด
  - [ ] `python exercises/verify.py --module 5` ขึ้น `[PASS]`

### แบบฝึกหัดเสริม (Break & Fix Lab): จำลอง CI พัง & Merge Conflict
1. **CI แดง:** ลองแก้ `test_add_numbers_positive` ใน `test_main.cpp` ให้คาดหวังค่าผิด (เช่น `TEST_ASSERT_EQUAL_INT(99, ...)`) แล้ว Push เข้า PR → ดู CI ขึ้น ❌ สีแดงและบล็อก Merge → อ่าน Log แก้กลับให้ถูกต้องจนเขียว ✅
2. **Merge Conflict:** แก้บรรทัดเดียวกันใน `src/main.cpp` บน 2 branches → Rebase & Merge อันแรกเข้า `main` → อีกอันจะติด Conflict → ฝึกแก้ด้วย `git fetch origin && git rebase origin/main` แล้วเลือกโค้ดที่ถูกต้องก่อน `git rebase --continue`

---

### Module 6: GitHub Actions Release (CD) & การ Flash ด้วย `esptool`
**เป้าหมาย:** ปล่อยเวอร์ชันเฟิร์มแวร์อัตโนมัติเมื่อ Merge เข้า `main` และติด Tag `v*.*.*` พร้อมนำไฟล์ไป Flash ลงบอร์ดจริง
- **โจทย์:**
  1. สร้าง `.github/workflows/release.yml` ที่ทำงานเมื่อ Push Tag `v*.*.*`
  2. ใช้ `esptool --chip esp32 merge-bin` รวม `bootloader.bin` + `partitions.bin` + `firmware.bin` เป็น `merged-firmware.bin`
  3. แตก branch `release/v1.0.0` จาก `main` → `git push -u origin release/v1.0.0` เพื่อให้ `ci.yml` รันตรวจผ่านสีเขียว
  4. เปิด PR เข้า `main` → กด **Rebase and merge** และลบ `release/v1.0.0` ทิ้ง (`main` ยังคงเป็นเส้นตรงเส้นเดียว)
  5. ติด Tag บน `main`: `git checkout main && git pull && git tag -a v1.0.0 -m "release: v1.0.0" && git push origin v1.0.0`
  6. *(ถ้ามีบอร์ดจริง)* ดาวน์โหลด `esp32doit-v1.0.0-merged-firmware.bin` จากหน้า Releases แล้ว Flash ลงบอร์ดด้วย `esptool`:
     ```bash
     uv tool install esptool
     esptool --chip esp32 --port COM3 --baud 460800 write-flash 0x0 esp32doit-v1.0.0-merged-firmware.bin
     ```
     *(หรือเปิดเว็บ [ESP Tool](https://espressif.github.io/esptool-js/) บน Chrome/Edge เสียบสาย USB แล้วเลือกไฟล์ที่ Address `0x0` ได้ทันทีโดยไม่ต้องลงโปรแกรม)*
- **เกณฑ์ผ่าน:**
  - [ ] หน้า **Releases** บน GitHub มีเวอร์ชัน `v1.0.0` พร้อม Release Notes อัตโนมัติ
  - [ ] มีไฟล์แนบครบทั้ง `esp32doit-v1.0.0-firmware.bin` และ `esp32doit-v1.0.0-merged-firmware.bin`
  - [ ] `python exercises/verify.py --module 6` ขึ้น `[PASS]`
