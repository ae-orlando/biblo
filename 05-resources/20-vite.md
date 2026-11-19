---
created: 2026-09-26
---

# What is Vite?

**Vite** (French word for "fast", pronounced `/vit/`) is a modern frontend build tool created by Evan You (creator of Vue.js). It replaces older, heavier bundlers like Webpack and Create React App with a drastically faster dev setup.

---
>[!info] Core Concept
>Instead of bundling your entire codebase every time you save a file, Vite serves your code using **Native ES Modules (ESM)** in development, letting the browser do the bundling work on demand.

---

## How Vite Works

Vite split frontend build tooling into two separate phases:

1. **Development Server:** Serves raw source files over native ES Modules (`import` / `export`). It uses **`esbuild`** (written in Go) to pre-bundle dependencies 10–100x faster than traditional JS-based bundlers.
2. **Production Build:** Uses **`Rollup`** under the hood to output highly optimized static assets (HTML, CSS, JS) ready for production deployment.
## Key Features

- **Instant Server Start:** Starts instantly regardless of project size because it doesn't pre-bundle your code.
- **Lightning-Fast HMR (Hot Module Replacement):** Edits reflect in the browser instantly without losing page state.
- **Out-of-the-Box Support:** Built-in support for TypeScript, JSX, CSS Modules, Less/Sass, and Web Workers without extra config.

---

## Practical Example: Scaffolding a React + TS Project

Here is the standard workflow for initializing and running a new Vite project:

```bash
# 1. Navigate to your projects directory
cd ~/learning

# 2. Scaffold a new project using the Vite template generator
pnpm create vite@latest my-app --template react-ts

# 3. Enter the project folder
cd my-app

# 4. Install project dependencies
pnpm install

# 5. Start the instant local development server
pnpm dev
```

### Breakdown of the Example Commands

| **Command** | **What it does** |
| ----------------------------- | ------------------------------------------------------------------------------------ |
| `pnpm create vite@latest ...` | Executes Vite's initializer package (`create-vite`) without installing it globally. |
| `my-app` | Sets the project name and output directory. |
| `--template react-ts` | Bootstraps the app with **React** and **TypeScript** preconfigured. |
| `pnpm install` | Reads `package.json` and downloads React, Vite, and TypeScript types. |
| `pnpm dev` | Starts Vite's dev server (typically at `http://localhost:5173`). |

## Related Notes
- [[30-tailwind-css-integration-to-vite|Tailwind CSS Integration]]
