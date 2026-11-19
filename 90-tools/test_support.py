"""Shared test fixtures. All writes stay in the vault-local runtime directory."""
from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import uuid
import sys

ROOT = Path(__file__).resolve().parents[1]
TARGET = Path(os.environ["PRACTICE_TARGET"]).resolve()
if not TARGET.is_relative_to(ROOT):
    raise RuntimeError("Test target escapes vault")


def run(args, **kwargs):
    return subprocess.run(args, capture_output=True, timeout=8, **kwargs)


def sandbox():
    directory = ROOT / ".practice-runtime/checks"
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    return tempfile.TemporaryDirectory(prefix="lab-", dir=directory)


def module(name="main.py"):
    spec = importlib.util.spec_from_file_location("learner_module", TARGET / name)
    result = importlib.util.module_from_spec(spec)
    # dataclasses and sibling imports need a normally registered module.
    sys.modules[spec.name] = result
    if str(TARGET) not in sys.path:
        sys.path.insert(0, str(TARGET))
    spec.loader.exec_module(result)
    return result


class Database:
    def __init__(self):
        import postgres
        self.pg = postgres
        self.name = "vault_lab_" + uuid.uuid4().hex

    def __enter__(self):
        self.execute(f'CREATE DATABASE "{self.name}";', database="postgres")
        return self

    def execute(self, text, *, database=None, variables=None, user=None, ok=True):
        result = self.pg.sql(text, database or self.name, user or self.pg.USER, variables)
        if ok and result.returncode:
            raise AssertionError(result.stderr)
        return result

    def answer(self, variables=None):
        return self.execute((TARGET / "answer.sql").read_text(), variables=variables)

    def __exit__(self, *exc):
        self.execute(f'DROP DATABASE "{self.name}" WITH (FORCE);', database="postgres")
