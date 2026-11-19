---
created: 2026-09-26
updated: 2026-10-21
---

# Web Development Foundations

> Outcome: trace one HTTP request and distinguish transport, response status, representation and persistence. Practice: `linux-network`, `js-http` and `js-dom` in [[practice-catalog]]. These are local fake-data labs, not a prerequisite to deploying a server.

## 1. Client-Server Architecture

Web applications operate on a **client-server model**, which separates the user interface from the data and business logic.

* **Client (Frontend):** The application interface running on the user's device (browser, mobile app). It collects user input, renders UI components, and asks the server for data.
* **Server (Backend):** A process or service that handles requests and returns responses. It can run locally, on shared infrastructure or on demand; being a server does not inherently mean one computer runs continuously or that every request queries a database.

---

## 2. HTTP Basics: Request & Response

Communication between client and server happens via **HTTP (Hypertext Transfer Protocol)**. Think of it as a structured dialogue: the client asks a question, and the server returns an answer.

### The HTTP Request

Sent by the client. It contains:

- **Method (Verb):** Defines the intended action.
  - `GET`: Fetch data (e.g., load a profile).
  - `POST`: Send new data (e.g., submit a signup form).
  - `PUT` / `PATCH`: Update existing data.
  - `DELETE`: Remove data.
- **URL/Endpoint:** The target location (e.g., `https://api.example.com/users`).
- **Headers:** Metadata about the request (e.g., authentication tokens, content format).
- **Body:** The payload data being sent (used with `POST`, `PUT`, `PATCH`).

### The HTTP Response

Returned by the server. It contains:

- **Status Code:** Indicates the result of the request.
  - `200 OK`: Success.
  - `201 Created`: Resource successfully created.
  - `400 Bad Request`: Client sent invalid data.
  - `401 Unauthorized`: authentication is required or failed; HTTP authentication semantics include an appropriate challenge.
  - `403 Forbidden`: the server refuses the operation; often an authenticated identity lacks permission, but not exclusively an authentication issue.
  - `404 Not Found`: Requested resource doesn't exist.
  - `500 Internal Server Error`: Backend crashed or encountered a bug.
- **Headers:** Response metadata (e.g., cache controls, content type).
- **Body:** The actual data payload (often HTML or JSON).

---

## 3. What is JSON?

**JSON (JavaScript Object Notation)** is a lightweight, human-readable text format used to exchange data between client and server.

Even though it originated from JavaScript syntax, **JSON is language-agnostic**—a Python backend can send JSON, and a React frontend can read it instantly.

```json
{
  "userId": 102,
  "username": "orlando",
  "isDeveloper": true,
  "skills": ["HTML", "CSS", "TypeScript"]
}
```

## 4. Databases vs. Plain Files

A **database** is a specialized software system designed to store, manage, and retrieve application data efficiently.

### Why not just store data in plain JSON or text files?

| Feature | Plain Files (data.json) | Database (PostgreSQL, MongoDB) |
|---|---|---|
| **Concurrency** | Applications must coordinate locking and writes; naive concurrent writes are unsafe. | The DBMS provides concurrency mechanisms; the application still needs appropriate transaction/isolation choices. |
| **Performance** | Format, indexing and access patterns determine work; not every lookup is a line scan. | Indexes help eligible queries; scans may be optimal and no fixed latency is guaranteed. |
| **Data Integrity** | Validation, write protocol and recovery are application responsibilities. | Configured constraints/transactions enforce specific invariants; missing rules and incorrect writes still matter. |
| **Security** | OS permissions and application controls apply; encryption is a separate choice. | Roles and controls depend on product/configuration. PostgreSQL does not automatically encrypt data at rest merely because it is a database. |

## 5. Localhost & Ports

When developing locally, your personal computer acts as both the **Client** (your browser) and the **Server** (your running app).

### Localhost (`127.0.0.1`)

`localhost` is a loopback hostname pointing directly back to your own computer. When you navigate to `http://localhost`, your browser sends requests to your local machine instead of the internet.

### Port Numbers (e.g., `:5173`, `:3000`)

A computer can run dozens of backend servers simultaneously. A **port** acts as a specific channel or apartment number directing traffic to a specific running application:

- `localhost:5173` → Vite React frontend dev server.

- `localhost:3000` or `localhost:8080` → Node.js / Express backend server.

- `localhost:5432` → PostgreSQL database server.

## Summary Checklist

- [ ] **Client vs. Server:** Client requests UI/data; Server processes and delivers it.

- [ ] **HTTP:** Stateless request/response cycle using methods (`GET`, `POST`) and status codes (`200`, `404`).

- [ ] **JSON:** Universal key-value text format for web data transport.

- [ ] **Database:** High-performance, concurrent, indexed storage (unlike flat files).

- [ ] **Localhost & Ports:** Machine self-address (`127.0.0.1`) + per-process channel (`:5173`).

### Related Notes

- [[10-node-installation|Node Installation]]

## Practice and retrieval

In `linux-network`, show why a 503 proves an HTTP exchange occurred while connection refusal does not. In `js-http`, assert method/status/content type and invalid-body behavior. In `js-dom`, inspect actual asset/API requests in Network rather than attributing every failure to CORS.

Explain method semantics (safe/idempotent are not synonyms), request versus response headers, and why valid JSON is not necessarily valid application input. JSON represents arrays, objects and primitives, not only key-value objects. Continue into [[25-http-security-boundaries]].

Sources: [MDN HTTP overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview), [HTTP semantics](https://www.rfc-editor.org/rfc/rfc9110), [JSON](https://www.rfc-editor.org/rfc/rfc8259).
