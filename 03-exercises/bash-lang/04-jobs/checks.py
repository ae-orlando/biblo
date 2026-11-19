import os
from pathlib import Path
import selectors
import signal
import subprocess
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "90-tools"))
from test_support import TARGET, sandbox


class WorkerTests(unittest.TestCase):
    def exercise(self, terminate):
        with sandbox() as temporary:
            process = subprocess.Popen(["bash", str(TARGET / "main.sh"), temporary], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
            children = []
            try:
                with selectors.DefaultSelector() as selector:
                    selector.register(process.stdout, selectors.EVENT_READ)
                    self.assertTrue(selector.select(4), "no readiness message")
                fields = process.stdout.readline().decode().rstrip("\n").split("\t")
                self.assertEqual(fields[0], "READY", fields)
                self.assertEqual(len(fields), 4)
                scratch = Path(fields[1]).resolve()
                self.assertTrue(scratch.is_relative_to(Path(temporary).resolve()))
                self.assertTrue(scratch.is_dir())
                children = [int(value) for value in fields[2:]]
                for pid in children:
                    self.assertEqual(os.getpgid(pid), process.pid, "worker must belong to the isolated test process group")
                if terminate: process.send_signal(signal.SIGTERM)
                else: process.stdin.write(b"done\n"); process.stdin.flush()
                process.communicate(timeout=4)
                self.assertEqual(process.returncode, 143 if terminate else 0)
                self.assertFalse(scratch.exists())
                for pid in children:
                    with self.assertRaises(ProcessLookupError): os.kill(pid, 0)
            finally:
                if process.poll() is None:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.communicate(timeout=3)
                # Never trust reported PIDs for cleanup: signal only our own group.
                try: os.killpg(process.pid, signal.SIGTERM)
                except ProcessLookupError: pass

    def test_normal_exit(self): self.exercise(False)
    def test_term_exit(self): self.exercise(True)


if __name__ == "__main__": unittest.main()
