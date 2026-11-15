#!/usr/bin/env python3
"""
Workshop Verification Script (Hybrid Self-Check)
ตรวจสอบความคืบหน้าและเกณฑ์ผ่านของแบบฝึกหัดทั้ง 6 Modules
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

CONVENTIONAL_RE = re.compile(
    r"^(feat|fix|docs|style|refactor|test|ci|chore|build)(\([a-zA-Z0-9_-]+\))?!?: .+"
)


def run_cmd(cmd: List[str], cwd: Path) -> Tuple[int, str, str]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
        )
        return proc.returncode, proc.stdout.strip(), proc.stderr.strip()
    except FileNotFoundError:
        return 127, "", f"Command not found: {cmd[0]}"
    except subprocess.TimeoutExpired:
        return 124, "", "Command timed out"


def find_pio() -> str:
    pio_in_path = shutil.which("pio")
    if pio_in_path:
        return pio_in_path
    home = Path.home()
    for candidate in [
        home / ".platformio" / "penv" / "Scripts" / "pio.exe",
        home / ".platformio" / "penv" / "bin" / "pio",
    ]:
        if candidate.exists():
            return str(candidate)
    return ""


def strip_comments(text: str, prefix: str = "#") -> str:
    """Remove full-line and inline comments starting with prefix so TODO hints are ignored."""
    lines = []
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(prefix):
            continue
        if f" {prefix}" in line:
            line = line.split(f" {prefix}", 1)[0]
        if line.strip():
            lines.append(line)
    return "\n".join(lines)


class Checker:
    def __init__(self, repo_root: Path, project_dir: Path):
        self.repo_root = repo_root
        self.project_dir = project_dir
        self.results: List[Tuple[str, str, str]] = []  # (status, label, detail)

    def record(self, status: str, label: str, detail: str = "") -> None:
        self.results.append((status, label, detail))
        icon = {"PASS": "[PASS]", "FAIL": "[FAIL]", "WARN": "[WARN]"}.get(status, "[INFO]")
        msg = f"  {icon} {label}"
        if detail:
            msg += f" — {detail}"
        print(msg)

    def has_remote(self) -> bool:
        code, out, _ = run_cmd(["git", "remote"], self.repo_root)
        return code == 0 and bool(out.strip())

    def gh_ready(self) -> bool:
        if not shutil.which("gh") or not self.has_remote():
            return False
        code, _, _ = run_cmd(["gh", "auth", "status"], self.repo_root)
        return code == 0

    def check_module_1(self) -> None:
        print("\n=== Module 1: Linear History (Rebase) & Conventional Commits ===")
        if not (self.repo_root / ".git").exists():
            self.record("FAIL", "Git repository", "ยังไม่พบ .git ที่ root (รัน git init หรือ clone repo ก่อน)")
            return
        self.record("PASS", "Git repository", "พบ .git")

        code, out, _ = run_cmd(["git", "branch", "--list", "main"], self.repo_root)
        branches = [b.replace("*", "").strip() for b in out.splitlines() if b.strip()]
        if "main" in branches:
            self.record("PASS", "Main branch", "พบ branch main")
        else:
            self.record("FAIL", "Main branch", "ไม่พบ branch main")

        code, merge_commits, _ = run_cmd(["git", "log", "--merges", "--oneline", "-n", "5", "main"], self.repo_root)
        if code == 0 and not merge_commits.strip():
            self.record("PASS", "Linear history", "ประวัติบน main เป็นเส้นตรง (ไม่มี merge commit)")
        elif code == 0 and merge_commits.strip():
            self.record("WARN", "Linear history", "พบ merge commit บน main (แนะนำใช้ git rebase / Rebase and merge)")

        code, log_out, _ = run_cmd(["git", "log", "-n", "10", "--pretty=format:%s"], self.repo_root)
        if code == 0 and log_out:
            subjects = log_out.splitlines()
            valid = [s for s in subjects if CONVENTIONAL_RE.match(s)]
            if valid:
                self.record("PASS", "Conventional Commits", f"พบ {len(valid)}/{len(subjects)} commits ล่าสุดที่ถูกต้อง")
            else:
                self.record("FAIL", "Conventional Commits", "ไม่พบ commit ที่ขึ้นต้นด้วย feat:/fix:/docs:/...")
        else:
            self.record("FAIL", "Git commits", "ยังไม่มี commit ใน repository")

    def check_module_2(self) -> None:
        print("\n=== Module 2: Pull Request, Issue Forms (.yml) & Collaboration ===")
        pr_tpl = self.repo_root / ".github" / "pull_request_template.md"
        if pr_tpl.exists():
            self.record("PASS", "PR Template", "พบ .github/pull_request_template.md")
        else:
            self.record("FAIL", "PR Template", "ไม่พบ .github/pull_request_template.md ที่ root")

        issue_dir = self.repo_root / ".github" / "ISSUE_TEMPLATE"
        issue_ymls = list(issue_dir.glob("*.yml")) + list(issue_dir.glob("*.yaml")) if issue_dir.exists() else []
        form_ymls = [p for p in issue_ymls if p.name != "config.yml"]
        if form_ymls:
            bug_file = issue_dir / "bug_report.yml"
            feat_file = issue_dir / "feature_request.yml"
            bug_ok = True
            feat_ok = True
            if bug_file.exists():
                bug_active = strip_comments(bug_file.read_text(encoding="utf-8", errors="ignore"))
                bug_ok = all(k in bug_active for k in ("id: version", "id: environment", "id: description", "id: checklist"))
            if feat_file.exists():
                feat_active = strip_comments(feat_file.read_text(encoding="utf-8", errors="ignore"))
                feat_ok = all(k in feat_active for k in ("id: problem", "id: solution", "id: target_branch"))
            if bug_ok and feat_ok:
                self.record("PASS", "Issue Forms (.yml)", f"พบ {len(issue_ymls)} ไฟล์ใน .github/ISSUE_TEMPLATE/ และตั้งค่า fields ครบ")
            else:
                self.record("FAIL", "Issue Forms (.yml)", "ไฟล์ Issue Form ยังมี TODO ที่ต้องเติม fields ให้ครบ (ดู docs/labs/LAB02)")
        else:
            self.record("FAIL", "Issue Forms (.yml)", "ไม่พบไฟล์ .yml ใน .github/ISSUE_TEMPLATE/ (เช่น bug_report.yml)")

        if not self.gh_ready():
            self.record("WARN", "GitHub PR check", "ข้ามการเช็ก PR ออนไลน์ (ยังไม่ได้เชื่อมต่อ remote หรือ gh auth login)")
            return

        code, out, _ = run_cmd(
            ["gh", "pr", "list", "--state", "merged", "--limit", "5", "--json", "number,baseRefName,headRefName"],
            self.repo_root,
        )
        if code == 0 and out and out != "[]":
            self.record("PASS", "Merged Pull Request", f"พบ PR ที่ Merge แล้ว: {out[:120]}")
        else:
            self.record("FAIL", "Merged Pull Request", "ยังไม่พบ PR ที่ถูก Merge บน GitHub")

    def check_module_3(self) -> None:
        print("\n=== Module 3: Pre-commit Hooks ===")
        cfg = self.repo_root / ".pre-commit-config.yaml"
        if cfg.exists():
            text = strip_comments(cfg.read_text(encoding="utf-8", errors="ignore"))
            has_cf = "clang-format" in text
            has_cc = "conventional-pre-commit" in text
            if has_cf and has_cc and "repos: []" not in text:
                self.record("PASS", ".pre-commit-config.yaml", "มีทั้ง clang-format และ conventional-pre-commit")
            else:
                self.record("FAIL", ".pre-commit-config.yaml", "ต้องกำหนด repos และมีทั้ง clang-format และ conventional-pre-commit")
        else:
            self.record("FAIL", ".pre-commit-config.yaml", "ไม่พบไฟล์ .pre-commit-config.yaml ที่ root")

        if (self.repo_root / ".clang-format").exists():
            self.record("PASS", ".clang-format", "พบไฟล์ตั้งค่าฟอร์แมต C/C++")
        else:
            self.record("FAIL", ".clang-format", "ไม่พบไฟล์ .clang-format ที่ root")

        hook_pre = self.repo_root / ".git" / "hooks" / "pre-commit"
        hook_msg = self.repo_root / ".git" / "hooks" / "commit-msg"
        if hook_pre.exists() and hook_msg.exists():
            self.record("PASS", "Git hooks installed", "ติดตั้ง pre-commit และ commit-msg hooks แล้ว")
        else:
            self.record("FAIL", "Git hooks installed", "รัน pre-commit install && pre-commit install --hook-type commit-msg")

    def check_module_4(self) -> None:
        print("\n=== Module 4: PlatformIO Unit Testing ===")
        pio_ini = self.project_dir / "platformio.ini"
        if pio_ini.exists():
            ini_active = strip_comments(strip_comments(pio_ini.read_text(encoding="utf-8", errors="ignore"), ";"), "#")
            if "[env:native]" in ini_active and "test_build_src" in ini_active:
                self.record("PASS", "platformio.ini [env:native]", "ตั้งค่า native environment แล้ว")
            else:
                self.record("FAIL", "platformio.ini [env:native]", "ยังไม่พบ [env:native] และ test_build_src = no ใน platformio.ini")
        else:
            self.record("FAIL", "platformio.ini [env:native]", "ไม่พบ workshop/platformio.ini")

        native_tests = list((self.project_dir / "test").glob("test_native/*.cpp")) if (self.project_dir / "test").exists() else []
        if native_tests:
            test_code = strip_comments(native_tests[0].read_text(encoding="utf-8", errors="ignore"), "//")
            run_count = len(re.findall(r"\bRUN_TEST\s*\(", test_code))
            if run_count >= 4:
                self.record("PASS", "Native test files", f"พบ {len(native_tests)} ไฟล์ใน test/test_native/ ({run_count} test cases)")
            else:
                self.record("FAIL", "Native test files", f"พบเพียง {run_count} test case(s) ใน test_main.cpp (ต้องมีอย่างน้อย 4 test cases)")
        else:
            self.record("FAIL", "Native test files", "ไม่พบไฟล์เทสใน test/test_native/")

        pio = find_pio()
        if not pio:
            self.record("WARN", "Run pio test -e native", "ไม่พบคำสั่ง pio ในเครื่อง")
            return
        if not shutil.which("gcc") and not shutil.which("g++"):
            self.record("WARN", "Run pio test -e native", "ไม่พบ gcc/g++ ใน PATH (บน Windows ต้องติดตั้ง MinGW/WinLibs เพื่อรัน native test)")
            return

        code, out, err = run_cmd([pio, "test", "-e", "native"], self.project_dir)
        if code == 0:
            self.record("PASS", "pio test -e native", "Unit Test ผ่านทั้งหมด!")
        else:
            self.record("FAIL", "pio test -e native", f"เทสไม่ผ่าน:\n{out[-300:]}\n{err[-200:]}")

    def check_module_5(self) -> None:
        print("\n=== Module 5: GitHub Actions CI ===")
        ci_file = self.repo_root / ".github" / "workflows" / "ci.yml"
        if ci_file.exists():
            content = strip_comments(ci_file.read_text(encoding="utf-8", errors="ignore"))
            if "pio test" in content and "pio run" in content and "starter-placeholder" not in content:
                self.record("PASS", "ci.yml", "พบ workflow ที่มีทั้ง pio test และ pio run")
            else:
                self.record("FAIL", "ci.yml", "ci.yml ยังไม่สมบูรณ์ (ต้องมีทั้ง pio test และ pio run และลบ starter-placeholder)")
        else:
            self.record("FAIL", "ci.yml", "ไม่พบ .github/workflows/ci.yml ที่ root")

        if not self.gh_ready():
            self.record("WARN", "GitHub Actions CI run", "ข้ามการเช็กออนไลน์ (ยังไม่ได้ gh auth login หรือไม่มี remote)")
            return

        code, out, _ = run_cmd(
            ["gh", "run", "list", "--workflow", "ci.yml", "--limit", "1", "--json", "status,conclusion"],
            self.repo_root,
        )
        if code == 0 and '"conclusion":"success"' in out.replace(" ", ""):
            self.record("PASS", "GitHub Actions CI run", "CI run ล่าสุดผ่าน (success)")
        else:
            self.record("FAIL", "GitHub Actions CI run", f"ยังไม่พบ CI run ที่ success: {out}")

    def check_module_6(self) -> None:
        print("\n=== Module 6: GitHub Actions Release (CD) ===")
        rel_file = self.repo_root / ".github" / "workflows" / "release.yml"
        if rel_file.exists():
            content = strip_comments(rel_file.read_text(encoding="utf-8", errors="ignore"))
            if "v*.*.*" in content and ("merge_bin" in content or "merge-bin" in content) and "starter-placeholder" not in content:
                self.record("PASS", "release.yml", "พบ workflow ที่ trigger ด้วย tag v*.*.* และรวม merged-firmware.bin")
            else:
                self.record("FAIL", "release.yml", "release.yml ยังไม่สมบูรณ์ (ต้องมี trigger 'v*.*.*', esptool merge-bin และลบ starter-placeholder)")
        else:
            self.record("FAIL", "release.yml", "ไม่พบ .github/workflows/release.yml ที่ root")

        code, tags, _ = run_cmd(["git", "tag", "-l", "v*.*.*"], self.repo_root)
        if code == 0 and tags.strip():
            self.record("PASS", "Git version tag", f"พบ Tag: {tags.splitlines()[-1]}")
        else:
            self.record("FAIL", "Git version tag", "ยังไม่พบ Tag รูปแบบ v*.*.* (เช่น v1.0.0)")

        if not self.gh_ready():
            self.record("WARN", "GitHub Release assets", "ข้ามการเช็กออนไลน์ (ยังไม่ได้ gh auth login หรือไม่มี remote)")
            return

        code, out, _ = run_cmd(["gh", "release", "list", "--limit", "1"], self.repo_root)
        if code == 0 and out.strip():
            self.record("PASS", "GitHub Release", f"พบ Release บน GitHub: {out.splitlines()[0]}")
        else:
            self.record("FAIL", "GitHub Release", "ยังไม่พบ GitHub Release ที่เผยแพร่")


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify ESP32 Git & CI/CD Workshop exercises")
    parser.add_argument("--module", type=int, choices=range(1, 7), help="ตรวจเฉพาะ Module ที่ระบุ (1-6)")
    parser.add_argument("--all", action="store_true", help="ตรวจครบทั้ง 6 Modules")
    parser.add_argument("--repo-root", default=".", help="Root ของ Git repository (ค่าเริ่มต้น: .)")
    parser.add_argument("--project-dir", default="workshop", help="โฟลเดอร์โปรเจกต์ PlatformIO (ค่าเริ่มต้น: workshop)")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    project_dir = (repo_root / args.project_dir).resolve()
    if not project_dir.exists():
        print(f"Error: ไม่พบโฟลเดอร์ {project_dir}", file=sys.stderr)
        return 2

    checker = Checker(repo_root, project_dir)
    modules = [args.module] if args.module else [1, 2, 3, 4, 5, 6]

    dispatch = {
        1: checker.check_module_1,
        2: checker.check_module_2,
        3: checker.check_module_3,
        4: checker.check_module_4,
        5: checker.check_module_5,
        6: checker.check_module_6,
    }
    for m in modules:
        dispatch[m]()

    fails = sum(1 for s, _, _ in checker.results if s == "FAIL")
    warns = sum(1 for s, _, _ in checker.results if s == "WARN")
    passes = sum(1 for s, _, _ in checker.results if s == "PASS")

    print("\n" + "=" * 50)
    print(f"Summary: {passes} PASS | {fails} FAIL | {warns} WARN")
    print("=" * 50)
    return 1 if fails > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
