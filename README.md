# ESP32 Git, Pull Request, Pre-commit, Testing & CI/CD Workshop

ชุดสื่อการสอนและโปรเจกต์ฝึกปฏิบัติสำหรับพัฒนา Firmware บนบอร์ด **DOIT ESP32 DevKit v1** (`esp32doit-devkit-v1`) ด้วย PlatformIO, Pre-commit Hooks และ GitHub Actions CI/CD

## เริ่มต้นจากศูนย์ (Start from 0 — ก่อนเริ่ม Lab 01)
1. **ตรวจสอบ Git + VS Code + MSYS2:** ติดตั้ง Git (`https://git-scm.com/`), Visual Studio Code (`https://code.visualstudio.com/`) และ MSYS2 (`https://www.msys2.org/` พร้อมรัน `pacman -S mingw-w64-ucrt-x86_64-gcc` ในหน้าต่าง **MSYS2 UCRT64**)
2. **ติดตั้ง PlatformIO ครบทั้ง 2 ส่วน** *(ใช้คู่กันคนละหน้าที่)*:
   - **PlatformIO IDE (VS Code Extension — ปุ่ม UI ใน VS Code):** เปิด VS Code กด `Ctrl+Shift+X` ค้นหา **`PlatformIO IDE`** → กด **Install** → รอแถบมุมขวาล่างโหลด *"PlatformIO: Installing PlatformIO Core..."* จนเสร็จ แล้ว Restart VS Code
   - **Local Toolchain (`uv sync` ใน `workshop/`):** เปิด PowerShell ทำตามใบงาน **[LAB00-Environment_Setup.pdf](exercises/labs/LAB00-Environment_Setup.pdf)** เพื่อลง `uv`, Clone โปรเจกต์ไว้ที่ **Desktop** (`cd $HOME\Desktop`), ตั้งค่า `--local` (รวม `git lg`), เปิดโฟลเดอร์ `workshop/` เป็น Workspace หลัก (`code workshop`) และรัน `uv sync` เพื่อติดตั้ง `pre-commit`, `platformio`, `esptool` แบบ Local ลงใน `workshop/.venv`
3. **เช็กความพร้อมเครื่องและ Pre-cache ESP32:** ใน Terminal ของ `workshop/` รัน:
   ```powershell
   $env:Path = "C:\msys64\ucrt64\bin;$env:Path"
   uv run scripts/check_env.py
   uv run pio run -e esp32doit-devkit-v1
   ```

---

## โครงสร้างโฟลเดอร์
- **[workshop/](workshop/)** — Starter Project และ Workspace หลักสำหรับผู้เรียน (`lib/blink_math`, `src/main.cpp`, `platformio.ini`, `pyproject.toml`, `scripts/`)
  - [workshop/scripts/check_env.py](workshop/scripts/check_env.py) — สคริปต์เช็กความพร้อมเครื่องสำหรับ **Lab 00** (`uv run scripts/check_env.py` จากใน `workshop/`)
  - [workshop/scripts/verify.py](workshop/scripts/verify.py) — สคริปต์ตรวจผลอัตโนมัติ (`uv run scripts/verify.py --module <1-6>` หรือ `--all` จากใน `workshop/`)
- **[exercises/](exercises/)** — ใบงานปฏิบัติการและโจทย์แบบฝึกหัดทั้งหมด
  - [exercises/labs/](exercises/labs/) — ใบงาน **LAB00–LAB06** ทั้งไฟล์ **`.pdf`** และ **`.docx`** สำหรับทำและส่งงาน
  - [exercises/exercises.md](exercises/exercises.md) — โจทย์และเกณฑ์ผ่านทั้ง 6 Modules
- **[presentation/](presentation/)** — สไลด์ประกอบการสอน (`ESP32_Git_CICD_Workshop.pptx`)
- **[videos/](videos/)** — วิดีโอ MP4 ประกอบแต่ละ Module (`videos/` และ `videos/github/`) + [Storyboard/Script](videos/scripts/video-scripts.md)
