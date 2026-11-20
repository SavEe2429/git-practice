# แบบฝึกหัดและเกณฑ์ประเมินผล (Exercises & Pass Criteria)

โฟลเดอร์นี้รวมโจทย์ฝึกปฏิบัติทั้ง **6 Modules** (จับคู่กับใบงาน **7 ฉบับ: `LAB00–LAB06`** ใน [labs/](./labs/)) สำหรับโปรเจกต์ [workshop/](../workshop) พร้อมระบบตรวจผลแบบ **Hybrid**:
1. **สคริปต์ตรวจอัตโนมัติ:** เปิดโฟลเดอร์ `workshop/` เป็น Workspace หลัก (`code workshop`) แล้วรันจากใน `workshop/` ด้วย `uv run scripts/verify.py --module <1-6>` หรือ `--all`
2. **Visual Checklist:** ตารางเช็กเกณฑ์ผ่านด้วยตาบน GitHub UI / Terminal
   - *หมายเหตุ:* เกณฑ์ออนไลน์ใน Module 2 (Merged PR), Module 5 (CI run) และ Module 6 (GitHub Release) ให้ตรวจดูบนหน้าเว็บ GitHub (แท็บ PR / Actions / Releases) ได้โดยตรง

---

## วิธีเตรียมเครื่องและใช้งาน `verify.py` (รันจากโฟลเดอร์ `workshop/`)
> **ก่อนเริ่ม Module 1:** ทำตามใบงาน **[LAB00-Environment_Setup.pdf](./labs/LAB00-Environment_Setup.pdf)** ให้เรียบร้อยเพื่อติดตั้ง `git`, `uv`, MSYS2 `gcc/g++` (`C:\msys64\ucrt64\bin`), Clone โปรเจกต์ไว้ที่ **Desktop** (`cd $HOME\Desktop`), ตั้งค่า `--local` (รวม `git lg`), เปิด `workshop/` เป็น Workspace หลัก (`code workshop`), รัน `uv sync` (ติดตั้ง `pre-commit`, `platformio`, `esptool` ลงใน `workshop/.venv`), รัน `uv run scripts/check_env.py` ตรวจเครื่อง และพรีโหลดแพ็กเกจ ESP32 ล่วงหน้า

```powershell
# 0. เช็กความพร้อมเครื่องก่อนเริ่ม (รันจากโฟลเดอร์ workshop/)
$env:Path = "C:\msys64\ucrt64\bin;$env:Path"
uv run scripts/check_env.py

# 1. ตรวจเฉพาะ Module 1
uv run scripts/verify.py --module 1

# 2. ตรวจทั้งหมด Modules 1-6
uv run scripts/verify.py --all
```
> หมายเหตุ:
> - ตามโครงสร้าง **Option A** โฟลเดอร์ `.github/` และ `.pre-commit-config.yaml` จะวางไว้ที่ **Root ของ Repo** ส่วนโค้ด PlatformIO และ `.venv` อยู่ใน `workshop/` (จึงต้องมี `defaults: run: working-directory: workshop` ในไฟล์ `.yml`)
> - คำสั่งในเอกสารนี้แยกคนละบรรทัดแทน `&&` เพื่อให้รันได้ทั้งบน **Windows PowerShell 5.1**, PowerShell 7 และ Bash

---

## แบบฝึกหัดทั้ง 6 Modules

### Module 1: Linear History (Rebase), Fork Workflow & Conventional Commits
**เป้าหมาย:** Fork Repo เพื่อแยกพื้นที่ทำงาน (`origin`), ใช้ `git lg` ดูกราฟ, รักษาประวัติให้เป็นเส้นตรงด้วย `git rebase main`, จำลองและแก้ Conflict จริง และเขียน Commit Message ตามมาตรฐาน
- **โจทย์ (คู่กับ [LAB01-Linear_Git_Rebase.pdf](./labs/LAB01-Linear_Git_Rebase.pdf)):**
  1. ตั้งค่า Git Alias `git lg` (`git config --local alias.lg "log --oneline --all --graph --decorate"`)
  2. แตก branch `feature/fast-blink` จาก `main` (`git switch -c feature/fast-blink main`) แล้วแก้บรรทัดที่ 15 ใน `src/main.cpp` (`clamp_interval(500)` → `clamp_interval(200)`)
  3. รัน `git add .` → `git commit -m "feat(blink): support fast blink interval"` → `git push -u origin feature/fast-blink`
  4. **จำลอง Commit ใหม่บน `main` ให้กราฟแยก 2 เส้น:** สลับไป `git switch main` → แก้บรรทัดที่ 15 ใน `src/main.cpp` เป็น `clamp_interval(300)` → `git add .` → `git commit -m "chore(blink): update default interval on main to 300ms"` → `git push origin main` → รัน `git lg -n 5` ดูกราฟแยก 2 เส้น
  5. สลับกลับมา `git switch feature/fast-blink` แล้วสั่ง `git rebase main` → เปิด `src/main.cpp` แก้ Conflict โดยลบเส้น `<<<<<<<`, `=======`, `>>>>>>>` ให้เหลือเฉพาะโค้ดใหม่ (`clamp_interval(200)`) → รัน `git add .` → `git rebase --continue` → ตรวจกราฟเส้นตรงด้วย `git lg -n 5` แล้ว Push ด้วย `git push --force-with-lease -u origin feature/fast-blink`
- **เกณฑ์ผ่าน:**
  - [ ] รัน `git lg -n 5` แล้วเห็นกราฟเรียงเป็นเส้นตรงเส้นเดียว (Linear History) โดย `feature/fast-blink` ต่อปลาย `main`
  - [ ] ข้อความ commit ขึ้นต้นด้วย `feat:`, `fix:`, `chore:`, `docs:` ฯลฯ ตามมาตรฐาน Conventional Commits
  - [ ] `uv run scripts/verify.py --module 1` ขึ้น `[PASS]`

---

### Module 2: Issue Forms (`.yml`), Pull Request (Web) & Branch Protection
**เป้าหมาย:** สร้างแบบฟอร์ม Issue ด้วย YAML, เปิด Issue และ Pull Request บนหน้าเว็บ GitHub แบบ Rebase and merge และตั้งค่า Branch Protection บังคับ Linear History
- **โจทย์ (คู่กับ [LAB02-Issue_Forms_PR_Protection.pdf](./labs/LAB02-Issue_Forms_PR_Protection.pdf)):**
  1. แทนที่ไฟล์ Issue Forms Skeleton ใน `.github/ISSUE_TEMPLATE/`: `bug_report.yml`, `feature_request.yml` และ `config.yml`
  2. ตรวจไวยากรณ์ YAML แล้ว Stage, Commit และ Push ขึ้น branch `feature/fast-blink` ที่กำลังทำอยู่ (`git add ../.github/ISSUE_TEMPLATE/` → `git commit -m "docs(github): add YAML issue forms and chooser config"` → `git push -u origin feature/fast-blink`)
  3. บนหน้าเว็บ GitHub ของตัวเอง: เข้าแท็บ **Issues → New issue** ทดลองเปิด Issue ใหม่จนได้หมายเลข Issue (เช่น `#1`)
  4. เข้าแท็บ **Pull requests → New pull request** เลือก `base: main <- compare: feature/fast-blink` ใส่ `Closes #1` ในรายละเอียด PR แล้วกด **Create pull request**
  5. กดลูกศรข้างปุ่ม Merge เลือก **Rebase and merge** และกด **Delete branch** จากนั้นใน Terminal ของเครื่องรัน `git switch main` และ `git pull origin main`
  6. ตั้งค่า Branch Protection บนเว็บ GitHub (`Settings -> Branches -> Add classic branch protection rule`, pattern `main`, ติ๊ก **Require a pull request before merging** และ **Require linear history**)
- **เกณฑ์ผ่าน:**
  - [ ] ไฟล์ `.yml` ทั้ง 3 ไฟล์ใน `.github/ISSUE_TEMPLATE/` มี fields ครบและไวยากรณ์ YAML ถูกต้อง
  - [ ] มี PR ที่ถูก Rebase and merge เข้า `main` บนหน้าเว็บ GitHub แล้ว
  - [ ] `uv run scripts/verify.py --module 2` ขึ้น `[PASS]`

---

### Module 3: Pre-commit Hooks (Quality Gate)
**เป้าหมาย:** ป้องกันโค้ดผิดฟอร์แมตและข้อความ Commit ผิดรูปแบบก่อนเข้า Git History ด้วย Local Pre-commit Hooks
- **โจทย์ (คู่กับ [LAB03-Pre_commit_Hooks.pdf](./labs/LAB03-Pre_commit_Hooks.pdf)):**
  1. แทนที่เนื้อหาใน `.pre-commit-config.yaml` ที่ Root ของ Repo (ลบ `repos: []` และ `# TODO`) แล้วรัน `git add ../.pre-commit-config.yaml` จากใน `workshop/` ก่อนเสมอ
  2. ติดตั้ง hook ทั้ง 2 stage ด้วย `uv run pre-commit install` และ `uv run pre-commit install --hook-type commit-msg` จากนั้นรัน `uv run pre-commit run --all-files` แล้วรัน `git add ../.pre-commit-config.yaml` และ `git add .` ตามด้วย `git commit -m "chore(hooks): configure pre-commit and clang-format"`
  3. **ทดลอง Break-Fix แบบแยก 2 ขั้น:**
     - **ขั้น A (Format Hook):** เปิดไฟล์ `src/main.cpp` ค้างไว้ใน VS Code แล้วเพิ่มบรรทัดที่เว้นช่องว่างเกินจงใจ `int   precommit_test =  1;` ท้ายฟังก์ชัน `setup()` แล้วกด Save → รัน `uv run pre-commit run --all-files` ใน Terminal → สังเกตว่า Terminal ขึ้น `clang-format...Failed` และหน้าโค้ด `src/main.cpp` ถูกแก้ช่องว่างเป็น `int precommit_test = 1;` ให้อัตโนมัติทันที → รัน `git add .` ใหม่
     - **ขั้น B (Commit-Msg Hook):** ลองรัน `git commit -m "bad commit message"` เพื่อดู hook `conventional-pre-commit` บล็อกข้อความผิดกฎ → แก้ข้อความเป็น `git commit -m "style: format main.cpp with clang-format"` จน Commit สำเร็จ
- **เกณฑ์ผ่าน:**
  - [ ] รัน `uv run pre-commit run --all-files` ผ่านทุก hook
  - [ ] Commit ข้อความผิดรูปแบบถูกบล็อกจริง และข้อความถูกต้องผ่านได้
  - [ ] `uv run scripts/verify.py --module 3` ขึ้น `[PASS]`

---

### Module 4: PlatformIO Unit Testing
**เป้าหมาย:** เขียนและรัน Unity Unit Tests บน `[env:native]` พร้อมคอมไพล์เฟิร์มแวร์สำหรับบอร์ด ESP32 จริง
- **โจทย์ (คู่กับ [LAB04-PlatformIO_Unit_Testing.pdf](./labs/LAB04-PlatformIO_Unit_Testing.pdf)):**
  1. แทนที่เนื้อหาใน `workshop/platformio.ini` (ลบ `; TODO`) เพื่อกำหนดทั้ง `[env:esp32doit-devkit-v1]` และ `[env:native]` (`test_build_src = no`, `test_filter = test_native`)
  2. แทนที่เนื้อหาใน `workshop/test/test_native/test_main.cpp` (ลบโค้ดเดิมทั้งหมด) เพื่อเขียน Unit Tests ทดสอบฟังก์ชันทั้งหมดใน `blink_math` ครบ 4 test cases
  3. ตั้ง PATH ของ MSYS2 ใน PowerShell (`$env:Path = "C:\msys64\ucrt64\bin;$env:Path"`) แล้วรัน `uv run pio test -e native -v` และ `uv run pio run -e esp32doit-devkit-v1`
  4. รัน `git add .` → `git commit -m "test(native): add [env:native] and blink_math unity tests"` → `git push origin HEAD`
- **เกณฑ์ผ่าน:**
  - [ ] `uv run pio test -e native -v` แสดงผล `PASSED` ครบทั้ง 4 test cases (`4 test cases: 4 succeeded`)
  - [ ] `uv run pio run -e esp32doit-devkit-v1` คอมไพล์ผ่าน `[SUCCESS]`
  - [ ] `uv run scripts/verify.py --module 4` ขึ้น `[PASS]`

---

### Module 5: GitHub Actions Continuous Integration (CI) & YAML Deep-Dive
**เป้าหมาย:** เข้าใจโครงสร้างไฟล์ `.yml`, คีย์เวิร์ดหลัก และให้ CI ตรวจ Lint, Unit Test, Build อัตโนมัติทุก PR
- **โจทย์ (คู่กับ [LAB05-GitHub_Actions_CI_YAML.pdf](./labs/LAB05-GitHub_Actions_CI_YAML.pdf)):**
  1. แทนที่ไฟล์ `.github/workflows/ci.yml` (ลบ `on: workflow_dispatch:` และ job `starter-placeholder:`) โดยกำหนด `on:`, `defaults.run.working-directory: workshop`, และ `jobs:` ทั้ง 3 ขั้น (`lint` → `unit-test` → `build-esp32` เชื่อมด้วย `needs:`)
  2. ตรวจไวยากรณ์ YAML ด้วย `uv run pre-commit run check-yaml --all-files`
  3. แตก branch `git switch -c ci/add-workflow main` → `git add ../.github/workflows/ci.yml` → `git commit -m "ci: add lint, native test and esp32 build workflow"` → `git push -u origin ci/add-workflow`
  4. เปิด PR เข้า `main` บนหน้าเว็บ GitHub แล้วดูผลลัพธ์สีเขียวครบ 3 Jobs บนแท็บ **Actions** (พร้อมทดลองทำ Break-Fix แก้ค่า Assert ใน `test_main.cpp` ให้ผิดแล้วแก้กลับจนเขียว)
- **เกณฑ์ผ่าน:**
  - [ ] แท็บ GitHub Actions แสดงเครื่องหมายถูกสีเขียวครบทั้ง 3 jobs (`lint` → `unit-test` → `build-esp32`)
  - [ ] `uv run scripts/verify.py --module 5` ขึ้น `[PASS]`

---

### Module 6: GitHub Actions Release (CD), Tagging, Flashing & Shared-PC Cleanup
**เป้าหมาย:** ปล่อยเวอร์ชันเฟิร์มแวร์อัตโนมัติเมื่อติด Tag `v*.*.*`, นำไฟล์ไป Flash ลงบอร์ดจริง และล้างบัญชีออกจากเครื่องส่วนกลางครบ 3 จุด
- **โจทย์ (คู่กับ [LAB06-Release_Tag_and_Firmware_Bin.pdf](./labs/LAB06-Release_Tag_and_Firmware_Bin.pdf)):**
  1. แทนที่ไฟล์ `.github/workflows/release.yml` (ลบ `workflow_dispatch:` และ `starter-placeholder:`) ให้ทำงานเมื่อ Push Tag `v*.*.*` และใช้ `esptool --chip esp32 merge-bin` รวม `bootloader.bin` + `partitions.bin` + `firmware.bin` เป็น `merged-firmware.bin`
  2. นำ `release.yml` เข้า `main` ผ่าน branch `release/v1.0.0` → เปิด PR บนเว็บ GitHub → กด **Rebase and merge**
  3. ดึง `main` ล่าสุดลงเครื่องแล้วติด Tag `v1.0.0`:
     ```powershell
     git switch main
     git pull origin main
     git tag -a v1.0.0 -m "release: v1.0.0"
     git push origin v1.0.0
     ```
  4. ดาวน์โหลด `esp32doit-v1.0.0-merged-firmware.bin` จากหน้า **Releases** บนเว็บ GitHub เพื่อนำไป Flash ที่ Address `0x0`:
     ```powershell
     uv run esptool --chip esp32 --port COM3 --baud 460800 write-flash 0x0 esp32doit-v1.0.0-merged-firmware.bin
     ```
  5. **Shared-PC Cleanup (ทำครบ 3 จุดก่อนลุกจากเครื่องห้องแล็บ):**
     - **จุดที่ 1 (VS Code):** คลิกไอคอน `Accounts` (มุมซ้ายล่าง) → เลือกบัญชี GitHub → `Sign Out`
     - **จุดที่ 2 (Windows Credential Manager):** รัน `cmdkey /list` และลบรายการ `git:https://github.com`
     - **จุดที่ 3 (Browser & Workspace):** กด `Sign out` บน `github.com` และลบโฟลเดอร์งานบน Desktop (`Remove-Item -Recurse -Force $HOME\Desktop\git-practice`)
- **เกณฑ์ผ่าน:**
  - [ ] หน้า **Releases** บน GitHub มีเวอร์ชัน `v1.0.0` พร้อมไฟล์แนบทั้ง `esp32doit-v1.0.0-firmware.bin` และ `esp32doit-v1.0.0-merged-firmware.bin`
  - [ ] `uv run scripts/verify.py --all` ขึ้น `[PASS]` ครบทุกข้อ
