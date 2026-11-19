---
created: 2026-09-26
---

# Tailwind CSS Integration (Vite)

## Command Breakdown

```bash
pnpm add tailwindcss @tailwindcss/vite
```

This command uses **PNPM** to install two packages required to run **Tailwind CSS (v4+)** inside a **Vite** project:

| Package | Purpose |
| :--- | :--- |
| **`tailwindcss`** | The core Tailwind CSS engine. Provides utility classes (e.g., `flex`, `pt-4`, `bg-blue-500`) to style HTML/React elements directly. |
| **`@tailwindcss/vite`** | The official Vite plugin for Tailwind CSS. Connects Tailwind's compiler directly into Vite's build pipeline for fast bundling and HMR (Hot Module Replacement). |

> [!info] Tailwind v4 Architecture
> In Tailwind v4+, the Vite plugin replaces the traditional PostCSS setup (`postcss.config.js` and `tailwind.config.js`). Styling and theme customizations are handled directly inside CSS via standard `@theme` directives.

---

## Setup Steps

### 1. Register the Plugin in `vite.config.ts`

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
})
```

### 2. Import Tailwind in Global CSS (`src/index.css`)

```css
@import "tailwindcss";
```

### 3. Test in React (`src/App.tsx`)

```tsx
export default function App() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-900 text-white">
      <h1 className="text-3xl font-bold underline text-sky-400">
        Tailwind + Vite is working!
      </h1>
    </div>
  )
}
```

---

## Related Notes
- [[20-vite]]