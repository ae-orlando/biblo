#!/usr/bin/env python3
"""Vault-local practice launcher. Never overwrites a learner workspace."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
LABS = json.loads((ROOT / "90-tools/labs.json").read_text())


def contained(path: Path) -> Path:
    resolved = path.resolve()
    if not resolved.is_relative_to(ROOT):
        raise ValueError(f"Path escapes vault: {path}")
    return resolved


def environment() -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("PG")}
    env.pop("NODE_COMPILE_CACHE", None)
    scratch = contained(ROOT / ".practice-runtime/checks")
    scratch.mkdir(parents=True, exist_ok=True, mode=0o700)
    env.update(TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE="1", TZ="UTC", LC_ALL="C.UTF-8")
    env.update(XDG_CACHE_HOME=str(ROOT / '.practice-runtime/cache'), XDG_CONFIG_HOME=str(ROOT / '.practice-runtime/config'), PYTHONNOUSERSITE='1', PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
    local_bin = contained(ROOT / ".tools/bin")
    env["PATH"] = str(local_bin) + os.pathsep + env.get("PATH", "")
    return env


def command_for(lab: dict) -> list[str]:
    """Use one runtime policy in the learner launcher and reference audit."""
    directory = contained(ROOT / lab['path'])
    if lab['runtime'] == 'node':
        return ['node', '--test', str(directory / 'checks.test.mjs')]
    interpreter = Path(sys.executable)
    kind = None
    if lab['runtime'] == 'fastapi':
        interpreter = ROOT / '.tools/fastapi-env/bin/python'
        kind = 'fastapi'
    elif lab['runtime'] == 'browser':
        interpreter = ROOT / '.tools/web-env/bin/python'
        kind = 'browser'
    if not interpreter.is_file():
        raise ValueError(f'Missing local runtime. Run: python3 90-tools/install-learning-runtime.py {kind}')
    return [str(interpreter), '-B', str(directory / 'checks.py')]


def check(lab_id: str, reference: bool) -> int:
    lab = LABS[lab_id]
    directory = contained(ROOT / lab["path"])
    target = contained(ROOT / "07-solutions" / lab_id) if reference else contained(directory / "work")
    if not target.is_dir():
        print(f"No workspace. Run: python3 90-tools/practice.py start {lab_id}", file=sys.stderr)
        return 2
    env = environment()
    env["PRACTICE_TARGET"] = str(target)
    if lab["runtime"] == "postgres" or lab.get('postgres'):
        result = subprocess.run([sys.executable, "-B", str(ROOT / "90-tools/postgres.py"), "start"], env=env)
        if result.returncode:
            return result.returncode
    command = command_for(lab)
    print(f"\n{'REFERENCE' if reference else 'LEARNER'}: {lab_id}", flush=True)
    try:
        result = subprocess.run(command, cwd=ROOT, env=env, timeout=90)
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        print(f"Check unavailable or timed out: {exc}", file=sys.stderr)
        return 2
    if result.returncode == 0 and lab.get("manual"):
        print("AUTOMATED PORTION PASSED. The browser/manual checklist is still required.")
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list")
    sub.add_parser("doctor")
    start = sub.add_parser("start")
    start.add_argument("lab", choices=LABS)
    one = sub.add_parser("check")
    one.add_argument("lab", choices=LABS)
    one.add_argument("--reference", action="store_true")
    all_checks = sub.add_parser("check-all")
    all_checks.add_argument("--reference", action="store_true", required=True)
    args = parser.parse_args()
    if args.command == "list":
        print('Catalog, not a simultaneous workload. Current start: py-basics; follow python-learning-path.md for prerequisites.')
        priority = {'python-foundations': 0, 'python': 1, 'postgres': 2, 'fastapi': 3, 'html-css': 4, 'js-lang': 5, 'bash-lang': 6, 'linux': 7}
        ordered = sorted(LABS.items(), key=lambda item: priority.get(Path(item[1]['path']).parts[1], 99))
        for key, lab in ordered:
            print(f"{key:22} {lab['title']} — {lab['path']}/README.md")
    elif args.command == "doctor":
        env = environment()
        for name, version_args in [("python3", ["--version"]), ("node", ["--version"]), ("bash", ["--version"]), ("shellcheck", ["--version"]), ("psql", ["--version"]), ("initdb", ["--version"]), ("pg_ctl", ["--version"])]:
            binary = shutil.which(name, path=env["PATH"])
            if binary:
                result = subprocess.run([binary, *version_args], capture_output=True, text=True, env=env)
                print(f"{name}: {binary}\n  " + " | ".join((result.stdout or result.stderr).splitlines()[:4]))
            else:
                print(f"{name}: MISSING (do not count dependent checks as verified)")
        for name in ['fastapi-env', 'web-env']:
            interpreter = ROOT / '.tools' / name / 'bin/python'
            print(f'{name}: {interpreter if interpreter.is_file() else "not installed; not needed for beginner Python"}')
    elif args.command == "start":
        directory = contained(ROOT / LABS[args.lab]["path"])
        work = contained(directory / "work")
        if work.exists():
            print(f"Preserved existing workspace: {work.relative_to(ROOT)}", file=sys.stderr)
            return 2
        shutil.copytree(contained(directory / "starter"), work)
        print(f"Created {work.relative_to(ROOT)}. Read {directory.relative_to(ROOT)}/README.md.")
    elif args.command == "check":
        return check(args.lab, args.reference)
    else:
        results = {lab: check(lab, True) for lab in LABS}
        print("\nSUMMARY")
        for lab, code in results.items():
            print(f"{'PASS' if code == 0 else 'FAIL/BLOCKED'} {lab}")
        return int(any(results.values()))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as exc:
        print(f"Practice error: {exc}", file=sys.stderr)
        raise SystemExit(2)
