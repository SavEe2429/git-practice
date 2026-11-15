# แนวทางเฉลยคำถามท้ายบท (Self-Check Answer Key: Lab 01 – Lab 06)

ผู้เรียนสามารถใช้ไฟล์นี้ตรวจคำตอบ `Q1`–`Q3` ในใบงาน [docs/LAB01–LAB06](../docs/) ได้ด้วยตัวเองทันทีหลังทำ Lab เสร็จ (และตรวจภาคปฏิบัติด้วย `uv run exercises/verify.py --module <1-6>`)

---

## Lab 01: Linear Git (Rebase), Fork Workflow & Conventional Commits
- **Q1:** แยกสิทธิ์การเขียนและพื้นที่พัฒนาออกจาก Repo หลัก (`upstream`) ป้องกันการ Push ทับกันโดยไม่ตั้งใจ และบังคับให้การรวมโค้ดทุกครั้งต้องผ่าน Pull Request + CI Gate รวมถึงช่วยให้ทดสอบ Branch Protection และ CI/CD ใน Fork ของตัวเองได้อย่างอิสระ
- **Q2:** `git rebase` นำ Commit ของเรามาต่อท้ายปลาย `main` ล่าสุด ทำให้กราฟเป็น **เส้นตรงเส้นเดียว** ส่วน `git merge` จะสร้าง Merge Commit และเห็นเส้นแตกเป็น 2 ทาง
- **Q3:** ทำให้อ่านประวัติรู้ทันทีว่า Commit นั้นทำอะไร (`feat`, `fix`, `docs`, `ci`) และนำไปใช้สร้าง Release Notes อัตโนมัติได้

## Lab 02: YAML Issue Forms, Pull Request (Rebase) & Branch Protection
- **Q1:** บังคับให้ผู้แจ้งกรอกข้อมูลสำคัญครบ (เช่น เวอร์ชัน, สภาพแวดล้อม, ขั้นตอนทำซ้ำ) ด้วย Dropdown/Required fields ลดการถามซ้ำไปมา
- **Q2:** ป้องกันไม่ให้ใครกด Create a merge commit เข้า `main` ทำให้ประวัติบน `main` เป็นเส้นตรงเสมอ
- **Q3:** เพื่อไม่ให้ Branch เก่าค้างรก Repo และป้องกันการเผลอกลับไปแก้บน Branch ที่มีประวัติไม่ตรงกับ `main` หลัง Rebase

## Lab 03: Pre-commit Hooks
- **Q1:** เพราะ `clang-format` แก้ไขไฟล์ให้ใน Working Directory เท่านั้น ยังไม่ได้ Stage ลง Staging Area จึงต้อง `git add` ไฟล์ที่จัดฟอร์แมตแล้วก่อน Commit ใหม่
- **Q2:** จับปัญหาฟอร์แมตและข้อความ Commit ผิดได้ในเครื่องภายใน ~1 วินาที ไม่ต้องรอส่งขึ้น GitHub Actions แล้วค่อย Fail

## Lab 04: PlatformIO Unit Testing
- **Q1:** เพื่อให้คอมไพล์และรันเทสบนเครื่อง PC / GitHub Actions (`[env:native]`) ได้ทันทีโดยไม่ต้องพึ่งฮาร์ดแวร์ ESP32 หรือ `Arduino.h`
- **Q2:** สั่งไม่ให้ `[env:native]` นำไฟล์ใน `src/` (ที่มี `#include <Arduino.h>`) ไปคอมไพล์ด้วยตอนรัน Native Unit Test

## Lab 05: GitHub Actions CI & YAML Deep-Dive
- **Q1:** เพราะไฟล์ `platformio.ini` อยู่ในโฟลเดอร์ย่อย `workshop/` ไม่ได้อยู่ที่ Root ของ Repo
- **Q2:** สั่งให้ Job `build-esp32` รอให้ Job `unit-test` ผ่านก่อนจึงค่อยเริ่มทำงาน (ถ้าเทสไม่ผ่านจะได้ไม่เสียเวลา Build)
- **Q3:** เก็บแพ็กเกจและ Toolchain ของ PlatformIO ไว้ใช้ซ้ำในรันถัดไป ช่วยลดเวลา Build ลงอย่างมาก

## Lab 06: Automated Release (CD), Tagging & Flashing
- **Q1:** `firmware.bin` ใช้สำหรับอัปเดตเฉพาะแอป / ทำ OTA ส่วน `merged-firmware.bin` รวม `bootloader + partitions + firmware` สำหรับ Flash ลงบอร์ดใหม่ในไฟล์เดียวที่ Address `0x0`
- **Q2:** เพราะการ Rebase จะสร้าง Commit Hash ใหม่ ถ้าติด Tag ก่อน Rebase ตัว Tag จะค้างอยู่ที่ Commit เก่า ไม่ได้อยู่บน `main`
