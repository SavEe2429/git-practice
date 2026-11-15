# ESP32 Git, Pre-commit, Testing & CI/CD Workshop (Starter)

โปรเจกต์เริ่มต้นสำหรับฝึกปฏิบัติใน Workshop บนบอร์ด **DOIT ESP32 DevKit v1** (`esp32doit-devkit-v1`)

## โครงสร้างโปรเจกต์
- `lib/blink_math/` — Pure C++ logic (แยกจาก `Arduino.h` เพื่อให้รัน Unit Test บนเครื่องและ CI ได้)
- `src/main.cpp` — โค้ดหลักสำหรับบอร์ด ESP32 (Blink LED + Serial)
- `test/` — โฟลเดอร์สำหรับเขียน Unity Unit Tests (ใน Module 4)
- `platformio.ini` — ไฟล์ตั้งค่า PlatformIO

## การ Build เบื้องต้น
```bash
pio run -e esp32doit-devkit-v1
```

> ดูคู่มือฉบับเต็มได้ที่ `../docs/workshop-manual.pdf` และแบบฝึกหัดได้ที่ `../exercises/exercises.md`

<!-- verified build & test -->
