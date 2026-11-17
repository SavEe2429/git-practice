# ESP32 GitFlow, Pull Request, Pre-commit, Testing & CI/CD Workshop

ชุดสื่อการสอนและโปรเจกต์ฝึกปฏิบัติสำหรับพัฒนา Firmware บนบอร์ด **DOIT ESP32 DevKit v1** (`esp32doit-devkit-v1`) ด้วย PlatformIO

## เริ่มต้นจากศูนย์ (Start from 0 — ก่อนเริ่ม Lab 01)
1. **ติดตั้ง Git + VS Code:** โหลด Git (`git-scm.com`) และ Visual Studio Code (`code.visualstudio.com`)
2. **ติดตั้ง PlatformIO ครบทั้ง 2 ส่วน** *(สำคัญมาก — ใช้คนละหน้าที่)*:
   - **PlatformIO IDE (VS Code Extension — ปุ่ม UI ใน VS Code):** เปิด VS Code กด `Ctrl+Shift+X` ค้นหา **`PlatformIO IDE`** → กด **Install** → รอแถบมุมขวาล่างโหลด *"PlatformIO: Installing PlatformIO Core..."* จนเสร็จ แล้วกด Reload/Restart VS Code *(และลง **`GitHub Pull Requests`** ด้วย)*
   - **PlatformIO Core CLI (`pio` ใน Terminal / CI):** เปิด PowerShell ทำตามใบงาน **[LAB00-Environment_Setup.pdf](docs/labs/LAB00-Environment_Setup.pdf)** เพื่อลง `uv`, `pio` (`uv tool install platformio`), `pre-commit`, `esptool`, WinLibs `gcc` และ pre-cache แพ็กเกจ ESP32 ล่วงหน้า
3. **เช็กความพร้อมเครื่อง:** `cd` เข้าโฟลเดอร์โปรเจกต์แล้วรัน `uv run exercises/check_env.py`

---

## โครงสร้างโฟลเดอร์
- **[workshop/](workshop/)** — Starter Project สำหรับผู้เรียนลงมือปฏิบัติ (`lib/blink_math`, `src/main.cpp`, `platformio.ini`)
- **[docs/](docs/)** — ใบงานปฏิบัติการและคู่มือผู้สอน
  - [docs/README.md](docs/README.md) — สารบัญใบงาน **LAB00–LAB06** (ทั้ง `.pdf` และ `.docx` สำหรับส่งงาน)
  - [docs/instructor-guide.md](docs/instructor-guide.md) — คู่มือผู้สอนและตารางเวลา Workshop
- **[presentation/](presentation/)** — สไลด์ประกอบการสอน (`ESP32_Git_CICD_Workshop.pptx`)
- **[exercises/](exercises/)** — แบบฝึกหัด, เฉลย และระบบตรวจผล (7 ใบงาน `LAB00–LAB06` คู่กับตัวตรวจ `Module 1–6`)
  - [exercises/check_env.py](exercises/check_env.py) — สคริปต์เช็กความพร้อมเครื่องสำหรับ **Lab 00** (`uv run exercises/check_env.py` หรือ `python exercises/check_env.py`)
  - [exercises/exercises.md](exercises/exercises.md) — โจทย์และเกณฑ์ผ่านทั้ง 6 Modules
  - [exercises/answer-key.md](exercises/answer-key.md) — แนวทางเฉลยคำถามท้ายบท (`Q1`–`Q3`)
  - [exercises/verify.py](exercises/verify.py) — สคริปต์ตรวจผลอัตโนมัติ (`uv run exercises/verify.py --all` หรือ `python exercises/verify.py --all`)
  - [exercises/solutions/](exercises/solutions/) — ไฟล์เฉลยอ้างอิงทั้งหมด
- **[videos/](videos/)** — วิดีโอ MP4 ประกอบแต่ละ Module (`videos/` และ `videos/github/`) + [Storyboard/Script](videos/scripts/video-scripts.md)
