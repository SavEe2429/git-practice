# ESP32 Git, Pre-commit, Testing & CI/CD Workshop (Starter)

โปรเจกต์เริ่มต้นและ Workspace หลักสำหรับผู้เรียนบนบอร์ด **DOIT ESP32 DevKit v1** (`esp32doit-devkit-v1`)

## โครงสร้างโปรเจกต์
- `lib/blink_math/` — Pure C++ logic (แยกจาก `Arduino.h` เพื่อให้รัน Unit Test บนเครื่องและ CI ได้)
- `src/main.cpp` — โค้ดหลักสำหรับบอร์ด ESP32 (Blink LED + Serial)
- `test/` — โฟลเดอร์สำหรับเขียน Unity Unit Tests (ใน Lab 04)
- `scripts/` — สคริปต์สำหรับผู้เรียน (`check_env.py` และ `verify.py`)
- `platformio.ini` — ไฟล์ตั้งค่า PlatformIO
- `pyproject.toml` / `uv.lock` — กำหนดแพ็กเกจ Python แบบ Local (`pre-commit`, `platformio`, `esptool` ใน `workshop/.venv`)

## คำสั่งที่ใช้บ่อย (รันจากโฟลเดอร์ `workshop/`)
```powershell
$env:Path = "C:\msys64\ucrt64\bin;$env:Path"
uv sync
uv run scripts/check_env.py
uv run pio run -e esp32doit-devkit-v1
uv run pio test -e native -v
uv run scripts/verify.py --all
```

> ดูใบงานปฏิบัติการ (`LAB00–LAB06` ทั้ง `.pdf` และ `.docx`) ได้ที่ `../exercises/labs/` และโจทย์แบบฝึกหัดได้ที่ `../exercises/exercises.md`
