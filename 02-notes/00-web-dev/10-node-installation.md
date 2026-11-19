---
created: 2026-09-26
updated: 2026-10-21
---

# Node Installation & Management

> Optional personal tooling reference. Existing Node 24 is sufficient for the labs; start with `python3 90-tools/practice.py doctor`. The rebuild does not change a global Node default, install fnm or edit shell startup files. A version manager is useful when projects require different runtimes, not mandatory for learning JavaScript.

## Why FNM (Fast Node Manager)?

Using a single global Node.js version (e.g., installed directly via system package managers like `pacman` or `apt`) can easily break older projects or team repos that require specific Node versions.

> [!tip] Key Benefits of FNM
> - **Per-Project Isolation:** Run different Node versions per project without conflicts.
> - **Convenience:** switches project versions when deliberately configured; performance depends on environment and is not a learning requirement.
> - **Auto-Switching:** Automatically switches Node versions upon entering a directory with a `.node-version` or `.nvmrc` file (`--use-on-cd`).

---

## Installation & Setup Workflow

### 1. Install & Set Up LTS

Run the following commands to install and activate the latest Long-Term Support (LTS) release:

```bash
# Install the latest LTS release
fnm install --lts

# Set LTS as the global default for all terminal sessions
fnm default lts-latest

# Switch to LTS in the current shell session
fnm use lts-latest
```

### 2. Shell integration (Zsh, auto-switch on `cd`)

```bash
# Add to ~/.zshrc
eval "$(fnm env --use-on-cd)"
```

This auto-switches Node versions when entering a directory with a `.node-version` or `.nvmrc` file.

### 3. Verify

```bash
node -v
npm -v
which node
```

Inspect `command -v node` and `node -v`. A supported system Node is not inherently wrong; choose the project's declared runtime. FNM paths matter only if deliberately using FNM. Pin project expectations rather than assuming latest LTS reproduces earlier results.

Sources: [FNM](https://github.com/Schniz/fnm), [Node releases](https://nodejs.org/en/about/previous-releases). Practice: explain which executable a shell invokes and demonstrate the version used by `js-cli` without changing global configuration.

## Related Notes

- [[00-web-foundations|Web Foundations]]
