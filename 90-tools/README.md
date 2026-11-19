# Vault practice tools

The launcher and beginner Python checks use the standard library (source baseline Python 3.11+). Other tracks use their declared runtimes: Bash 5+/GNU/Linux, Node 24, PostgreSQL 15+, and marked local FastAPI/browser environments for the new framework/web checks. ShellCheck is optional for practice but required for the `--code` lint gate. Actual tested versions/results: [base rebuild](../01-roadmap/implementation-status.md), [Python/FastAPI expansion](../01-roadmap/python-fastapi-expansion-status.md).

Start with `py-basics`; no framework/database/browser package installation is required for beginner Python. The following optional installers affect only this vault:

```bash
python3 90-tools/install-learning-runtime.py fastapi
python3 90-tools/install-learning-runtime.py browser
```

They use reviewed package inputs/resolved version pins in 90-tools/requirements-*.txt and *.lock, with caches/temp files under the vault. Existing marked environments are reused, unmarked ones refused. Pins are not artifact hashes or a universal cross-platform lock. Browser checks use existing Chromium and do not install a system package or download a browser automatically. Full installed versions are recorded inside each environment.

Run these commands from `/home/orlando/Documents/Notes`, not from this tools folder:

| Command | Effect |
| --- | --- |
| `python3 90-tools/practice.py list` | List stable lab IDs and specifications |
| `python3 90-tools/practice.py doctor` | Report runtimes; create only local scratch support |
| `python3 90-tools/practice.py start LAB-ID` | Copy an unfinished starter to work/; refuse existing work |
| `python3 90-tools/practice.py check LAB-ID` | Check learner implementation; SQL labs can start the local cluster |
| `python3 90-tools/practice.py check LAB-ID --reference` | Audit supplied reference, not learner progress |
| `python3 90-tools/practice.py check-all --reference` | Run every reference suite |
| `python3 90-tools/audit-practice.py` | References, expected starter failures and representative mutations; local logs/results |
| `python3 90-tools/check-vault.py --code` | Local links/assets/JSON plus standalone syntax/shell lint |
| `python3 90-tools/check-tooling.py` | Six smoke tests: preservation, connection isolation, demo fixture, corrected semantics and restricted local web serving |
| `python3 90-tools/postgres.py start` / `stop` / `status` / `psql` | Manage only the marked vault-local cluster |
| `python3 90-tools/serve-dom.py` | Serve only js-dom/work and fake API on 127.0.0.1:8000 |
| `python3 90-tools/serve-dom.py --reference --port 8001` | Inspect reference page at a chosen loopback port |
| `python3 90-tools/serve-web.py web-html` | Serve only the selected HTML work directory and fake local form preview |
| `python3 90-tools/serve-web.py web-css --reference --port 8001` | Inspect the CSS reference on a chosen loopback port |
| `python3 90-tools/check-git-training.py PATH` | Read selected final artifacts from an explicitly marked learner repo under 03-exercises/git; never initialize/commit/repair |
| `python3 90-tools/verify-backup.py` | Verify original snapshot; no restoration |

The optional pinned ShellCheck installer is `python3 90-tools/install-shellcheck.py`. It verifies the official release digest, installs only under .tools/ and refuses to overwrite an existing binary. The launcher adds that binary directory only to its child process environment, not your global PATH. For a direct check, use `.tools/bin/shellcheck PATH-TO-SCRIPT`.

Tests are not a security sandbox: they execute chosen learner/reference code with your permissions. Read unfamiliar code. New web checks observe selected real-browser behavior, while broader visual/accessibility/assistive-technology judgment remains manual. Git operations, plan interpretation, real identity integration, VM/deployment and independent capstones are separate evidence gates. Stop owned practice services when finished.

Implementation: `90-tools/practice.py:1`, `90-tools/labs.json:1`, `90-tools/postgres.py:1`, `90-tools/test_support.py:1`. Recovery and migration details: [vault maintenance](../01-roadmap/vault-maintenance.md).
