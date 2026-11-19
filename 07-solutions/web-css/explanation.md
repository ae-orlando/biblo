# Reference: explicit constraints, not a universal design system

The reference uses border-box sizing, a fluid bounded container, wrapped flex controls, grid tracks with deliberate minimums, content wrapping and two breakpoint transitions. Focus/contrast/control sizing are explicit. It is one solution; a different implementation meeting the observed geometry/interaction contract is valid.

Verification: `python3 90-tools/practice.py check web-css --reference`. Real-browser checks cover selected outcomes but not all visual, accessibility, device or browser combinations. Manual evaluation remains required.
