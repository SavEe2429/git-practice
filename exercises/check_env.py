#!/usr/bin/env python3
"""
Pre-Workshop Environment Check
รันเช็กความพร้อมเครื่องก่อนเริ่มเรียน Workshop (Git, Python, pre-commit, gh, PlatformIO, gcc)
"""

import shutil
import subprocess
import sys
from pathlib import Path


def check_cmd(cmd: list) -> tuple[bool, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        out = (p.stdout or p.stderr).strip().splitlines()
        return p.returncode == 0, (out[0] if out else "")
    except Exception as exc:
        return False, str(exc)


def find_pio() -> str:
    if shutil.which("pio"):
        return shutil.which("pio") or ""
    home = Path.home()
    for c in [
        home / ".platformio" / "penv" / "Scripts" / "pio.exe",
        home / ".platformio" / "penv" / "bin" / "pio",
    ]:
        if c.exists():
            return str(c)
    return ""


def main() -> int:
    print("=== Pre-Workshop Environment Check ===\n")
    fails = 0

    # 1. Git
    ok, ver = check_cmd(["git", "--version"])
    print(f"[{'OK' if ok else 'MISSING'}] Git: {ver or 'ไม่พบ git'}")
    if not ok:
        print("   -> แก้ไข: ติดตั้ง Git จาก https://git-scm.com/")
        fails += 1

    ok_name, name = check_cmd(["git", "config", "user.name"])
    ok_mail, mail = check_cmd(["git", "config", "user.email"])
    if ok_name and ok_mail and name and mail:
        print(f"[OK] Git identity: {name} <{mail}>")
    else:
        print("[MISSING] Git identity (user.name / user.email)")
        print('   -> แก้ไข: git config --global user.name "Your Name" && git config --global user.email "you@example.com"')
        fails += 1

    # 2. pre-commit
    ok, ver = check_cmd(["pre-commit", "--version"])
    print(f"[{'OK' if ok else 'MISSING'}] pre-commit: {ver or 'ยังไม่ติดตั้ง'}")
    if not ok:
        print("   -> แก้ไข: pip install pre-commit")
        fails += 1

    # 3. GitHub CLI
    ok, ver = check_cmd(["gh", "--version"])
    if ok:
        auth_ok, _ = check_cmd(["gh", "auth", "status"])
        print(f"[OK] GitHub CLI: {ver} (auth: {'logged in' if auth_ok else 'ยังไม่ login'})")
        if not auth_ok:
            print("   -> แนะนำ: รัน gh auth login เพื่อเปิด PR และให้ verify.py เช็ก CI/Release ได้")
    else:
        print("[WARN] GitHub CLI (gh): ไม่พบ (ยังเปิด PR ผ่านเว็บ GitHub ได้ แต่ verify.py จะเช็กออนไลน์ไม่ได้)")

    # 4. PlatformIO
    pio = find_pio()
    if pio:
        ok, ver = check_cmd([pio, "--version"])
        print(f"[OK] PlatformIO: {ver} ({pio})")
    else:
        print("[MISSING] PlatformIO CLI (pio)")
        print("   -> แก้ไข: ติดตั้ง PlatformIO IDE extension ใน VS Code หรือ pip install platformio")
        fails += 1

    # 5. gcc / g++ for native tests
    gcc = shutil.which("gcc") or shutil.which("g++")
    if gcc:
        ok, ver = check_cmd([gcc, "--version"])
        print(f"[OK] C/C++ Compiler (สำหรับ pio test -e native): {ver}")
    else:
        print("[WARN] ไม่พบ gcc/g++ ใน PATH (Windows ต้องติดตั้ง WinLibs/MinGW เพื่อรัน pio test -e native ในเครื่อง)")
        print("   -> แก้ไข (Windows): winget install BrechtSanders.WinLibs.POSIX.UCRT แล้วเปิด Terminal ใหม่")

    print("\n" + "=" * 44)
    if fails == 0:
        print("พร้อมเข้าเรียน Workshop แล้ว!")
        return 0
    print(f"พบ {fails} รายการที่ต้องติดตั้งก่อนเริ่มเรียน")
    return 1


if __name__ == "__main__":
    sys.exit(main())
