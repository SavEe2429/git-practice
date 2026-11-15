# คู่มือสำหรับผู้สอน (Instructor Runbook)

## 1. การเตรียม Repository หลักก่อนวันเรียน (Option A: Single Public Repo + Fork)
1. สร้าง **Public Repository** บน GitHub (เช่น `esp32-git-cicd-workshop`) เพื่อให้ผู้เรียนทุกคนได้ **GitHub Actions ฟรีไม่จำกัดนาที**
2. Push โฟลเดอร์ทั้งหมด (`workshop/`, `docs/`, `exercises/`, `videos/`, `.gitignore`, `README.md`) ขึ้นเป็น branch `main`
3. แจ้งผู้เรียน **20+ คน** ให้รัน `python exercises/check_env.py` ล่วงหน้า 1 วันก่อนเข้าคลาส
4. เน้นย้ำรูปแบบ Branching ของ Workshop: **`main` เป็นเส้นตรงด้วย Rebase** และแยก branch เฉพาะตอนเตรียม **`release/v*`** เท่านั้น (ไม่มี `develop`)

---

## 2. ตารางเวลาแนะนำ (Half-Day ~4 ชั่วโมง / Full-Day ~6 ชั่วโมง)
| ช่วงเวลา | เนื้อหา | สิ่งที่ผู้เรียนต้องทำได้ |
| :--- | :--- | :--- |
| 00:00 – 00:30 | เปิดตัว & เช็กเครื่อง (`check_env.py`) | Fork Repo + Clone ลงเครื่อง + ตรวจ `main` |
| 00:30 – 01:15 | **Module 1:** Linear Git (Rebase) & Conventional Commits | แตก `feature/*` + Commit ตามมาตรฐาน + `git rebase` (`verify.py --module 1`) |
| 01:15 – 02:00 | **Module 2:** Issue Forms (`.yml`), PR & Protection | สร้าง Issue `.yml` + เปิด PR เข้า `main` + Rebase & Merge (`verify.py --module 2`) |
| 02:00 – 02:45 | **Module 3:** Pre-commit Hooks | ติดตั้ง hook + ทดลองทำผิดฟอร์แมต/ข้อความแล้วแก้ (`verify.py --module 3`) |
| 02:45 – 03:30 | **Module 4:** PlatformIO Unit Test (`native`) | รัน `pio test -e native` ผ่าน 4+ เคส (`verify.py --module 4`) |
| 03:30 – 04:30 | **Module 5:** GitHub Actions CI & YAML + Break & Fix | เขียน `ci.yml` + ทดลองทำให้ CI แดงแล้วแก้ให้เขียว (`verify.py --module 5`) |
| 04:30 – 05:30 | **Module 6:** Auto Release & Flash ด้วย `esptool` | Merge `release/v1.0.0` → `main` → Tag `v1.0.0` → โหลด `.bin` (`verify.py --module 6`) |

---

## 3. จุดที่ผู้เรียนมักติดบ่อยหน้างาน
- **Windows รัน `pio test -e native` ไม่ได้:** ลืมลง `gcc`/`g++` (ให้ลง WinLibs หรือดูผลรันบน GitHub Actions `ubuntu-latest` แทนได้)
- **`working-directory` ใน YAML:** เพราะโปรเจกต์ PlatformIO อยู่ใน `workshop/` ต้องใส่ `defaults: run: working-directory: workshop` ใน `ci.yml` และ `release.yml`
- **GitHub Actions ไม่รันใน Fork:** บางครั้ง GitHub ปิด Actions ใน Repo ที่ Fork มาชั่วคราว ให้ผู้เรียนกดเข้าไปที่แท็บ **Actions** บน Repo ตัวเองแล้วกดปุ่มสีเขียว **"I understand my workflows, go ahead and enable them"**
