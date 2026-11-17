#!/usr/bin/env python3
"""
Pre-Workshop Environment Check
รันเช็กความพร้อมเครื่องก่อนเริ่มเรียน Workshop (Git, uv, pre-commit, gh, PlatformIO, esptool, gcc, Windows TEMP)
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def check_cmd(cmd: list[str]) -> tuple[bool, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=10)
        out = (p.stdout or p.stderr).strip().splitlines()
        return p.returncode == 0, (out[0] if out else "")
    except Exception as exc:
        return False, str(exc)


def find_pio_fallback() -> str:
    home = Path.home()
    for c in [
        home / ".platformio" / "penv" / "Scripts" / "pio.exe",
        home / ".platformio" / "penv" / "bin" / "pio",
    ]:
        if c.exists():
            return str(c)
    return ""


def find_esptool() -> str:
    for name in ("esptool", "esptool.py"):
        found = shutil.which(name)
        if found:
            return found
    return ""


def main() -> int:
    print("=== Pre-Workshop Environment Check ===\n")
    fails = 0
    warns = 0

    if not (Path.cwd() / "workshop" / "platformio.ini").exists():
        print("[WARN] ยังไม่ได้รันจากโฟลเดอร์ root ของ repo (ควร cd เข้า git-practice ก่อนรัน check_env.py)")
        warns += 1

    # 1. Git & Identity
    ok, ver = check_cmd(["git", "--version"])
    print(f"[{'OK' if ok else 'MISSING'}] Git: {ver or 'ไม่พบ git'}")
    if not ok:
        print("   -> แก้ไข (Windows): winget install Git.Git  (หรือโหลดจาก https://git-scm.com/)")
        fails += 1

    ok_name, name = check_cmd(["git", "config", "user.name"])
    ok_mail, mail = check_cmd(["git", "config", "user.email"])
    if ok_name and ok_mail and name and mail:
        print(f"[OK] Git identity: {name} <{mail}>")
    else:
        print("[MISSING] Git identity (user.name / user.email)")
        print('   -> เครื่องมหาลัย (แนะนำ): git config --local user.name "Your Name"; git config --local user.email "you@example.com"')
        print('   -> เครื่องส่วนตัว:        git config --global user.name "Your Name"; git config --global user.email "you@example.com"')
        fails += 1

    # 2. uv
    ok, ver = check_cmd(["uv", "--version"])
    print(f"[{'OK' if ok else 'WARN'}] uv: {ver or 'ไม่พบ uv (แนะนำสำหรับจัดการ pre-commit, pio, esptool และรัน verify.py)'}")
    if not ok:
        print("   -> แนะนำ: ดูวิธีติดตั้งที่ https://docs.astral.sh/uv/getting-started/installation/")
        warns += 1

    # 3. pre-commit
    ok, ver = check_cmd(["pre-commit", "--version"])
    print(f"[{'OK' if ok else 'MISSING'}] pre-commit: {ver or 'ยังไม่ติดตั้งหรือไม่อยู่ใน PATH'}")
    if not ok:
        print("   -> แก้ไข: uv tool install pre-commit; uv tool update-shell  (แล้วปิด-เปิด Terminal ใหม่)")
        fails += 1

    # 4. PlatformIO CLI (ตรวจ PATH จริงก่อน fallback)
    pio_in_path = shutil.which("pio")
    if pio_in_path:
        ok, ver = check_cmd([pio_in_path, "--version"])
        print(f"[OK] PlatformIO CLI (in PATH): {ver} ({pio_in_path})")
    else:
        pio_fb = find_pio_fallback()
        if pio_fb:
            ok, ver = check_cmd([pio_fb, "--version"])
            print(f"[WARN] PlatformIO CLI: พบที่ {pio_fb} ({ver}) แต่คำสั่ง `pio` ยังไม่อยู่ใน PATH")
            print("   -> แก้ไข: uv tool install platformio; uv tool update-shell  (แล้วปิด-เปิด Terminal ใหม่)")
            print(f'   -> ชั่วคราว: เรียกใช้ด้วย & "{pio_fb}" ...')
            warns += 1
        else:
            print("[MISSING] PlatformIO CLI (pio)")
            print("   -> แก้ไข: uv tool install platformio; uv tool update-shell  (หรือติดตั้ง VS Code PlatformIO IDE)")
            fails += 1

    # 5. esptool (ใช้ใน Lab 06)
    esptool_exe = find_esptool()
    if esptool_exe:
        ok, ver = check_cmd([esptool_exe, "version"])
        print(f"[OK] esptool: {ver or 'พร้อมใช้งาน'} ({esptool_exe})")
    else:
        print("[WARN] esptool: ยังไม่พบคำสั่ง `esptool` ใน PATH (ต้องใช้ใน Lab 06)")
        print("   -> แก้ไข: uv tool install esptool; uv tool update-shell  (แล้วปิด-เปิด Terminal ใหม่)")
        warns += 1

    # 6. GitHub CLI (Optional สำหรับดู CI/Release จาก Terminal)
    ok, ver = check_cmd(["gh", "--version"])
    if ok:
        auth_ok, _ = check_cmd(["gh", "auth", "status"])
        print(f"[OK] GitHub CLI: {ver} (auth: {'logged in' if auth_ok else 'ยังไม่ login'})")
        if not auth_ok:
            print("   -> แนะนำ: รัน `gh auth login` เพื่อดู CI/PR/Release ผ่าน Terminal (และอย่าลืม `gh auth logout` เมื่อเลิกใช้เครื่องรวม)")
    else:
        print("[WARN] GitHub CLI (gh): ไม่พบ (ยังเปิด Issue/PR ผ่านเว็บ GitHub และ VS Code ได้ แต่ verify.py จะเช็กออนไลน์ไม่ได้)")
        warns += 1

    # 7. gcc / g++ สำหรับ pio test -e native ใน Lab 04
    gcc = shutil.which("gcc") or shutil.which("g++")
    if gcc:
        ok, ver = check_cmd([gcc, "--version"])
        print(f"[OK] C/C++ Compiler (สำหรับ pio test -e native): {ver}")
    else:
        print("[WARN] ไม่พบ gcc/g++ ใน PATH (Windows ต้องติดตั้ง WinLibs เพื่อรัน `pio test -e native` ในเครื่อง)")
        print("   -> แก้ไข (Windows): winget install BrechtSanders.WinLibs.POSIX.UCRT  (เปิด Terminal ใหม่แล้วเช็ก `g++ --version`)")
        print("   -> หากเครื่องห้องแล็บล็อกสิทธิ์: ใช้ Build ESP32 ในเครื่อง แล้วตรวจผล `[env:native]` บน Cloud CI ใน Lab 05 แทนได้")
        warns += 1

    # 8. Windows TEMP probe (กันปัญหา cc1plus.exe: too many filenames / @C:\WINDOWS\TEMP\...)
    if sys.platform == "win32":
        temp_dir = os.environ.get("TEMP") or os.environ.get("TMP") or ""
        temp_warn = ""
        if not temp_dir or r"\windows\temp" in temp_dir.lower():
            temp_warn = f"TEMP ชี้ไปที่ `{temp_dir or '(ว่าง)'}` อาจทำให้ `pio run` ล้มด้วย `cc1plus.exe: too many filenames given`"
        else:
            try:
                with tempfile.NamedTemporaryFile(dir=temp_dir, delete=True):
                    pass
            except Exception as exc:
                temp_warn = f"TEMP (`{temp_dir}`) ไม่สามารถเขียนไฟล์ชั่วคราวได้: {exc}"
        if temp_warn:
            print(f"[WARN] Windows TEMP: {temp_warn}")
            print('   -> แก้ไขใน PowerShell ก่อนรัน pio: New-Item -ItemType Directory -Force C:\\Temp | Out-Null; $env:TEMP="C:\\Temp"; $env:TMP="C:\\Temp"')
            warns += 1
        else:
            print(f"[OK] Windows TEMP: {temp_dir}")

    print("\n" + "=" * 54)
    if fails == 0 and warns == 0:
        print("พร้อมเข้าเรียน Workshop ครบ 100% แล้ว!")
        return 0
    if fails == 0:
        print(f"พร้อมบางส่วน (พบ {warns} คำเตือน [WARN] — อ่านรายละเอียดด้านบนก่อนเริ่ม Lab 04 / Lab 06)")
        return 0
    print(f"พบ {fails} รายการที่ต้องติดตั้งก่อนเริ่มเรียน (และ {warns} คำเตือน)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
