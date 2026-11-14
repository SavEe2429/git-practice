## สรุปการเปลี่ยนแปลง (Summary)
<!-- อธิบายสั้นๆ ว่า PR นี้ทำอะไร และทำไมต้องทำ -->

## ประเภทของ PR (Type of Change)
- [ ] `feat`: เพิ่มฟีเจอร์ใหม่ (`feature/*` → Rebase เข้า `main`)
- [ ] `fix`: แก้ไขบั๊ก (`fix/*` → Rebase เข้า `main`)
- [ ] `release`: เตรียมปล่อยเวอร์ชัน (`release/v*`)
- [ ] `ci` / `docs` / `test`: ปรับปรุง CI, เอกสาร หรือ Unit Tests

## Checklist ก่อนขอ Review
- [ ] รัน `pre-commit run --all-files` ผ่านแล้ว
- [ ] รัน `pio test -e native` ผ่านทุกเคส
- [ ] รัน `pio run -e esp32doit-devkit-v1` คอมไพล์ผ่านไม่มี Error
- [ ] อัปเดตเอกสารหรือ Unit Test ที่เกี่ยวข้องแล้ว
