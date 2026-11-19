# Fullstack repository layouts and public boundaries

## Outcome

Distinguish a static site, a frontend/backend split and a deployment boundary. Prerequisites: HTML asset URLs, Python modules and a working API. Do not start by building multiple services.

## Static/vanilla frontend

An illustrative small frontend might contain index.html, styles/, src/app.js and src/api-client.js, public/ for deliberate assets and tests/. With no build tool, the browser must receive actual importable files/URLs. With a bundler, source and generated output differ. Never assume an arbitrary src tree is automatically served or built.

## A modest fullstack repository

```text
product/
  README.md
  .gitignore
  frontend/
    package.json               # only when a JS toolchain is actually selected
    dependency-lock-file
    index.html
    src/
    public/
    tests/
  backend/
    pyproject.toml
    dependency-lock-file
    src/product_api/
    migrations/
    tests/
    .env.example
  docs/
    api-contract.md
    decisions/
    runbook.md
  deployment/                  # deliberate deployment config, no real credentials
```

This is a design example, not a promise those tools/files already exist. A server-rendered or static app may not need a separate JS package at all. A frontend framework's own conventions should be learned when chosen, not guessed from this generic tree.

## Tradeoffs and contracts

One repository can simplify coordinated changes, shared review and local setup; separate repositories can support genuinely independent ownership/releases but add coordination/versioning work. Neither choice implies microservices.

Define API request/response/error schemas, base URL/configuration, origin/cookie/CSRF policy, pagination and compatibility. Generated client artifacts can help but need a version/update policy; they do not replace understanding the request.

Only expose a deliberate public directory/build output. Keep .env values, source-only configuration, runtime databases, backups, local environments and internal logs out of that boundary. A gitignore rule and an HTTP static-file policy are different controls.

## Exercise

Draw the path from a browser asset URL to the served file and from an API request to a transaction. Choose a deployment same-origin/proxy or intentional cross-origin contract; do not “fix CORS” by allowing every origin with credentials. Explain what can be released independently and what must change together.

Sources: [[25-http-security-boundaries]], [FastAPI frontend guidance](https://fastapi.tiangolo.com/tutorial/frontend/), [MDN modules](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules).
