# คู่มือสำหรับผู้สอน (Instructor Runbook)

## 1. การเตรียม Repository หลักก่อนวันเรียน (Option A: Single Public Repo + Fork)
1. สร้าง **Public Repository** บน GitHub (เช่น `esp32-git-cicd-workshop`) เพื่อให้ผู้เรียนทุกคนได้ **GitHub Actions ฟรีไม่จำกัดนาที**
2. Push โฟลเดอร์ทั้งหมด (`workshop/`, `docs/`, `exercises/`, `videos/`, `.gitignore`, `README.md`) ขึ้นเป็น branch `main` โดยคงไฟล์ Skeleton (`# TODO` / `starter-placeholder`) ไว้ตามเดิม
3. แจ้งผู้เรียน **20+ คน** ให้ทำตาม **[Lab 00 (Environment Setup)](./labs/LAB00-Environment_Setup.pdf)** ล่วงหน้า 1 วันก่อนเข้าคลาส เพื่อติดตั้ง Git, `uv`, `pre-commit`, `platformio`, `esptool`, VS Code Extensions, WinLibs `gcc` และพรีโหลด ESP32 package ให้ผ่าน `uv run exercises/check_env.py` ครบทั้งหมด (ลดปัญหาเน็ตห้องแล็บช้าและไม่ต้องติดตั้งแยกกลาง Lab 01–06)
4. เน้นย้ำรูปแบบ Branching ของ Workshop: **`main` เป็นเส้นตรงด้วย Rebase** และแยก branch เฉพาะตอนเตรียม **`release/v*`** เท่านั้น (ไม่มี `develop`)
5. กำชับวิธีวางโค้ดใน **Lab 02–06**: ไฟล์เริ่มต้นมีโครง `# TODO` / `starter-placeholder` อยู่แล้ว ให้ผู้เรียน **Ctrl+A เลือกทั้งหมดแล้ววางทับ (Replace whole file)** ไม่ใช่เอาไปต่อท้ายไฟล์เดิม มิฉะนั้น `platformio.ini`, `test_main.cpp` และ `.yml` จะซ้ำกัน

---

## 2. ตารางเวลาแนะนำ (Half-Day ~4 ชั่วโมง / Full-Day ~6 ชั่วโมง)
| ช่วงเวลา | เนื้อหา | สิ่งที่ผู้เรียนต้องทำได้ |
| :--- | :--- | :--- |
| 00:00 – 00:30 | เปิดตัว & เช็กเครื่อง (`check_env.py`) | Fork Repo + Clone + ตั้ง `upstream` + ตรวจด้วย `check_env.py` |
| 00:30 – 01:15 | **Module 1:** Linear Git (Rebase) & Conventional Commits | แตก `feature/*` + Commit + `git rebase upstream/main` + แก้ Conflict + `--force-with-lease` (`verify.py --module 1`) |
| 01:15 – 02:00 | **Module 2:** Issue Forms (`.yml`), PR & Protection | สร้าง Issue `.yml` + เปิด PR เข้า `main` + Rebase & Merge (`verify.py --module 2`) |
| 02:00 – 02:45 | **Module 3:** Pre-commit Hooks | Stage `.pre-commit-config.yaml` + ติดตั้ง hook 2 stage + ทดสอบ Break-Fix แยกขั้น (`verify.py --module 3`) |
| 02:45 – 03:30 | **Module 4:** PlatformIO Unit Test (`native`) | รัน `pio test -d workshop -e native` ผ่าน 4+ เคส (`verify.py --module 4`) |
| 03:30 – 04:30 | **Module 5:** GitHub Actions CI & YAML + Break & Fix | เขียน `ci.yml` + ทดลองทำให้ CI แดงแล้วแก้ให้เขียว (`verify.py --module 5`) |
| 04:30 – 05:30 | **Module 6:** Auto Release & Flash ด้วย `esptool` | Merge `release/v1.0.0` → `main` → Tag `v1.0.0` → โหลด `.bin` (`verify.py --all`) + Logout เครื่องรวม |

---

## 3. จุดที่ผู้เรียนมักติดบ่อยหน้างาน (Troubleshooting สำหรับ TA/ผู้สอน)
- **`pio` หรือ `esptool` ไม่เจอใน PowerShell หลังลงด้วย `uv`:** ลืมรัน `uv tool update-shell` หรือยังไม่ได้ปิดแล้วเปิด Terminal ใหม่ (กรณีเร่งด่วนบน VS Code ที่มี PlatformIO IDE อยู่แล้ว ให้เรียกผ่าน `& "$env:USERPROFILE\.platformio\penv\Scripts\pio.exe"`)
- **Windows Build Error `cc1plus.exe: too many filenames given ... @C:\WINDOWS\TEMP\...`:** เกิดเมื่อตัวแปร `TEMP`/`TMP` ของ session ชี้ไปที่ `C:\WINDOWS\TEMP` ที่เขียนไม่ได้หรือติดข้อจำกัด — ให้สร้างโฟลเดอร์ชั่วคราวแล้วตั้ง `$env:TEMP="C:\Temp"; $env:TMP="C:\Temp"` ก่อนรัน `pio`
- **Windows รัน `pio test -e native` ไม่ได้ (`gcc is not recognized`):** ลืมลง `gcc`/`g++` หรือเครื่องห้องแล็บล็อกสิทธิ์ติดตั้ง WinLibs (ให้ดูผลรัน Native Test บน GitHub Actions `ubuntu-latest` ใน Lab 05 แทนได้ โดย `verify.py` จะขึ้นแค่ `[WARN]`)
- **ใช้ `&&` ใน PowerShell 5.1 แล้วพัง:** Windows PowerShell 5.1 (ค่าเริ่มต้นบน Windows 10/11) ไม่รองรับ `&&` ให้รันทีละบรรทัดหรือใช้ `;` แทน
- **ข้อความสีแดงจาก `git` ใน PowerShell:** `git` พิมพ์สถานะความคืบหน้าลง stderr ซึ่ง PowerShell อาจแสดงเป็นสีแดง `NativeCommandError` ทั้งที่คำสั่งสำเร็จ ให้อ่านข้อความจริงก่อนตัดสินว่า Error
- **`working-directory` ใน YAML:** เพราะโปรเจกต์ PlatformIO อยู่ใน `workshop/` ต้องใส่ `defaults: run: working-directory: workshop` (ใช้เฉพาะกับคำสั่ง `run:` ส่วน `uses:` เช่น `upload-artifact` / `action-gh-release` ยังต้องระบุ `workshop/...` เต็ม)
- **GitHub Actions ไม่รันใน Fork:** GitHub ปิด Actions ใน Repo ที่ Fork มาเป็นค่าเริ่มต้น ให้ผู้เรียนกดเข้าไปที่แท็บ **Actions** บน Fork ตัวเองแล้วกดปุ่มสีเขียว **"I understand my workflows, go ahead and enable them"**

---

## 4. รายการตรวจสอบก่อนลุกจากเครื่องห้องปฏิบัติการ (Shared-PC 4-Point Logout Checklist)
กำชับผู้เรียนทุกคนหลังจบ Workshop ให้ทำครบทั้ง **4 จุด**:
1. **VS Code:** คลิกไอคอน **Accounts** (รูปคนมุมซ้ายล่าง) → เลือก `<username> (GitHub)` → **Sign Out** (รวมถึง Settings Sync / GitHub Copilot ถ้ามี)
2. **GitHub CLI:** รัน `gh auth logout` ใน Terminal
3. **Windows Credential Manager & Local Config:** เปิด Control Panel → Credential Manager → Windows Credentials ลบรายการ `git:https://github.com` และ `gh:github.com*` (หรือตรวจด้วย `cmdkey /list` / `cmdkey /delete:git:https://github.com`)
4. **Browser & Workspace:** กด **Sign out** บนหน้าเว็บ `github.com` (หรือใช้โหมด Incognito), ปิดหน้าต่างเบราว์เซอร์ และลบโฟลเดอร์โปรเจกต์/ไฟล์ `.bin` ที่โหลดไว้ในเครื่องรวมออก
