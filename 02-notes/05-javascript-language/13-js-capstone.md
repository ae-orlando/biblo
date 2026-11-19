# JavaScript capstone — one coherent system

## Prerequisites and goal

Complete the six JavaScript labs in [[00-js-how-to-use]], including the browser checklist, plus [[10-testing-and-debugging]] and [[00-web-foundations]]. Integrate the mechanisms independently; do not paste three unrelated demos beside each other and call it a system.

Create your implementation under `04-projects/js-todo-capstone/` when you do the work. No learner implementation or completion is supplied by this note.

## Required contracts

1. **Pure logic:** validate todo text, assign an injected ID, toggle/filter without mutating input. A clock timestamp alone is not a unique identifier. Test invalid shapes, blank input, duplicate IDs and input preservation.
2. **API:** preserve the tested `js-http` GET/POST/PATCH/DELETE contract, content types, body-size limit and error behavior. Use a server factory so tests select loopback port 0 and close it reliably.
3. **Serving:** explicitly serve `/`, `/app.mjs` and `/ui.mjs` with correct types from a dedicated public directory. Do not expose the vault, allow arbitrary filesystem paths or assume serving only index.html serves its imported modules.
4. **Client:** consume the actual API, not an unrelated localStorage copy. Implement add/toggle/delete/search, validation, loading/error/empty states, safe text insertion, labels and keyboard use. Show retries and stale-request handling.
5. **Persistence:** choose either explicitly ephemeral memory for the first checkpoint or a documented durable adapter. If using a JSON file, serialize writes and explain atomic replacement, crash limits and concurrency scope. A multi-process production store needs stronger guarantees.
6. **CLI:** reuse pure logic and the chosen persistence interface without simultaneously competing with an unsafe file-writing server. State the allowed writer model. Help/misuse/runtime failures have explicit streams/statuses.

## Acceptance evidence

- Node tests exercise logic and API, including malformed JSON, primitive JSON, oversized multibyte body, missing resources and unsupported methods.
- An integration test loads the page and both module assets and performs a complete create/toggle/delete flow through the same server.
- Browser evidence covers keyboard use, literal injection payload, slow/failing requests, empty/search states and reload semantics.
- State survives restart **only if** persistence is in scope. Server-side persistence does not automatically generate browser storage events or synchronize tabs. Design polling, refetch, SSE or another explicit mechanism if cross-tab freshness is required.
- Save a bug caught by tests, one design tradeoff, and what remains unsafe for deployment.

## Independent change request

Add due dates as calendar dates (not timezone-dependent instants), deterministic sorting and a filter for overdue incomplete todos. Update contracts, tests and UI together. Then explain what ownership/authentication would require without representing this unauthenticated teaching API as an auth platform.

Use [[study-and-review]] to assess correctness, robustness, tests, design, safety and transfer. Passing the supplied lab references is not completion evidence for this project.
