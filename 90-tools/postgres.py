#!/usr/bin/env python3
"""Manage ONLY the disposable PostgreSQL cluster inside this vault."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / ".practice-runtime/postgres"
DATA = BASE / "data"
SOCKET = BASE / "socket"
PORT = "55432"
USER = "vault_admin"
MARKER = BASE / "owner.json"


def safe_environment():
    return {k: v for k, v in os.environ.items() if not k.startswith("PG")}


def guard(require_marker=True):
    for path in (BASE, DATA, SOCKET, MARKER):
        if path.is_symlink() or not path.resolve().is_relative_to(ROOT):
            raise RuntimeError(f"Unsafe runtime path: {path}")
    if require_marker:
        if not MARKER.is_file() or json.loads(MARKER.read_text()) != {"vault": str(ROOT), "purpose": "disposable-practice"}:
            raise RuntimeError("Refusing to adopt an unmarked database cluster")


def connection(database="postgres", user=USER):
    guard()
    return ["-h", str(SOCKET), "-p", PORT, "-U", user, "-d", database]


def sql(text, database="postgres", user=USER, variables=None):
    command = ["psql", "-X", "-q", "-A", "-t", "-v", "ON_ERROR_STOP=1", "-v", "VERBOSITY=sqlstate", *connection(database, user)]
    for key, value in (variables or {}).items():
        command += ["-v", f"{key}={value}"]
    return subprocess.run(command, input=text, capture_output=True, text=True, env=safe_environment(), timeout=25)


def status():
    guard()
    return subprocess.run(["pg_ctl", "-D", str(DATA), "status"], capture_output=True, text=True, env=safe_environment())


def start():
    guard(False)
    for binary in ("initdb", "pg_ctl", "psql"):
        if not shutil.which(binary):
            raise RuntimeError(f"Missing {binary}; no system packages will be installed automatically")
    if not DATA.exists():
        BASE.mkdir(parents=True, exist_ok=True, mode=0o700)
        subprocess.run(["initdb", "-D", str(DATA), "--no-locale", "--encoding=UTF8", "--auth-local=trust", "--auth-host=reject", "--username=" + USER], check=True, stdout=subprocess.DEVNULL, env=safe_environment())
        MARKER.write_text(json.dumps({"vault": str(ROOT), "purpose": "disposable-practice"}))
    guard()
    if status().returncode == 0:
        print("Vault practice PostgreSQL already running (Unix socket only).")
        return
    SOCKET.mkdir(exist_ok=True, mode=0o700)
    options = shlex.join(["-k", str(SOCKET), "-p", PORT, "-c", "listen_addresses=", "-c", "unix_socket_permissions=0700"])
    subprocess.run(["pg_ctl", "-D", str(DATA), "-l", str(BASE / "server.log"), "-o", options, "-w", "start"], check=True, env=safe_environment())
    print("Started disposable vault cluster; no system service or existing database was used.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["start", "stop", "status", "psql"])
    args = parser.parse_args()
    if args.command == "start":
        start()
    elif args.command == "stop":
        guard()
        if status().returncode != 0:
            print("Vault practice cluster is not running.")
            return
        subprocess.run(["pg_ctl", "-D", str(DATA), "-m", "fast", "-w", "stop"], check=True, env=safe_environment())
    elif args.command == "status":
        result = status()
        print(result.stdout or result.stderr, end="")
        raise SystemExit(result.returncode)
    else:
        guard()
        raise SystemExit(subprocess.call(["psql", "-X", "-v", "ON_ERROR_STOP=1", *connection()], env=safe_environment()))


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, subprocess.SubprocessError) as exc:
        print(f"Practice database error: {exc}", file=sys.stderr)
        raise SystemExit(2)
