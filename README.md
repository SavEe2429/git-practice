# ESP32 GitFlow, Pull Request, Pre-commit, Testing & CI/CD Workshop

ชุดสื่อการสอนและโปรเจกต์ฝึกปฏิบัติสำหรับพัฒนา Firmware บนบอร์ด **DOIT ESP32 DevKit v1** (`esp32doit-devkit-v1`) ด้วย PlatformIO

## โครงสร้างโฟลเดอร์
- **[workshop/](workshop/)** — Starter Project สำหรับผู้เรียนลงมือปฏิบัติ (`lib/blink_math`, `src/main.cpp`, `platformio.ini`)
- **[docs/](docs/)** — ใบงานปฏิบัติการและคู่มือผู้สอน
  - [docs/README.md](docs/README.md) — สารบัญใบงาน **LAB01–LAB06** (ทั้ง `.pdf` และ `.docx` สำหรับส่งงาน)
  - [docs/instructor-guide.md](docs/instructor-guide.md) — คู่มือผู้สอนและตารางเวลา Workshop
- **[presentation/](presentation/)** — สไลด์ประกอบการสอน (`ESP32_Git_CICD_Workshop.pptx`)
- **[exercises/](exercises/)** — แบบฝึกหัด, เฉลย และระบบตรวจผล
  - [exercises/check_env.py](exercises/check_env.py) — สคริปต์เช็กความพร้อมเครื่องก่อนเรียน (`uv run exercises/check_env.py`)
  - [exercises/exercises.md](exercises/exercises.md) — โจทย์และเกณฑ์ผ่านทั้ง 6 Modules
  - [exercises/answer-key.md](exercises/answer-key.md) — แนวทางเฉลยคำถามท้ายบท (`Q1`–`Q3`)
  - [exercises/verify.py](exercises/verify.py) — สคริปต์ตรวจผลอัตโนมัติ (`uv run exercises/verify.py --all`)
  - [exercises/solutions/](exercises/solutions/) — ไฟล์เฉลยอ้างอิงทั้งหมด
- **[videos/](videos/)** — วิดีโอ MP4 ประกอบแต่ละ Module (`videos/` และ `videos/github/`) + [Storyboard/Script](videos/scripts/video-scripts.md)
