# Reference: explicit inputs and deliberate failure

The reference depends only on a mapping, never mutates it and returns a new dictionary. It distinguishes absent optional settings from malformed supplied values, parses booleans explicitly and avoids echoing the training token in errors.

This is a small configuration exercise, not a secrets manager. Keep real credentials outside examples, screenshots, logs and version control. Verification: `python3 90-tools/practice.py check python-config --reference`.
