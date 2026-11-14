# ESP32 GitFlow, Pull Request, Pre-commit, Testing & CI/CD Workshop

ชุดสื่อการสอนและโปรเจกต์ฝึกปฏิบัติสำหรับพัฒนา Firmware บนบอร์ด **DOIT ESP32 DevKit v1** (`esp32doit-devkit-v1`) ด้วย PlatformIO

## โครงสร้างโฟลเดอร์
- **[workshop/](workshop/)** — Starter Project สำหรับผู้เรียนลงมือปฏิบัติ (`lib/blink_math`, `src/main.cpp`, `platformio.ini`)
- **[docs/](docs/)** — คู่มือการเรียนรู้แบบ Visual-First
  - [docs/workshop-manual.pdf](docs/workshop-manual.pdf) — คู่มือฉบับ PDF พร้อมแผนภาพนำทางและคำอธิบาย **How / Why / Benefits**
- **[exercises/](exercises/)** — แบบฝึกหัด, เฉลย และระบบตรวจผล
  - [exercises/exercises.md](exercises/exercises.md) — โจทย์และเกณฑ์ผ่านทั้ง 6 Modules
  - [exercises/verify.py](exercises/verify.py) — สคริปต์ตรวจผลอัตโนมัติ (`python exercises/verify.py --all`)
  - [exercises/solutions/](exercises/solutions/) — ไฟล์เฉลยอ้างอิงทั้งหมด
- **[videos/](videos/)** — วิดีโอ MP4 ประกอบแต่ละ Module + [Storyboard/Script](videos/scripts/video-scripts.md)
