---
name: api-design
description: "Designs HTTP and RPC API contracts: resources and endpoints, request and response shapes, status codes, errors, pagination, filtering, versioning, idempotency and authentication, delivered as an OpenAPI 3.1 document or GraphQL or protobuf schema with examples. Use when the user asks to design, review or document a REST, GraphQL, gRPC or webhook API, write an OpenAPI or Swagger spec, or decide how clients should talk to a service. Do not use for implementing the handlers; use implement-feature."
trigger: "design or document an API, endpoint or interface contract"
metadata:
  version: "1.1.0"
---

# API design

🧬 **Core meme:** Design the contract clients can rely on before writing the handlers.

Design an API contract that clients find predictable: consistent naming, clear errors, safe retries, room to evolve without breaking anyone. Deliver it as a machine-readable spec with examples, so it can drive code generation, docs and contract tests.

## Workflow

```
- [ ] 1. Identify consumers and use cases
- [ ] 2. Model resources and operations
- [ ] 3. Define shapes, errors and cross-cutting rules
- [ ] 4. Write the spec with examples
- [ ] 5. Validate and review
```

1. **Consumers.** Who calls it (browser, mobile, other services, third parties) and the top five things they need to do. Design for those calls, not for the database tables.
2. **Style.** Default to REST over JSON. Choose GraphQL when many clients need different shapes of deeply related data, gRPC for internal service-to-service calls with strict latency needs, and webhooks or events for notifying others. Follow an existing API in the codebase if there is one; consistency beats local perfection.
3. **Model.** Nouns as plural resources (`/orders`, `/orders/{id}/items`), HTTP methods for verbs, and at most two levels of nesting. Use a sub-resource or an action endpoint (`POST /orders/{id}/cancel`) only for operations that are not CRUD.
4. **Rules.** Apply the conventions below unless the codebase already has others.
5. **Spec.** Write OpenAPI 3.1 YAML (or SDL, or `.proto`) with an example request and response for every operation, including one error example. Validate it: `npx @redocly/cli lint openapi.yaml`.
6. **Review** against the gotchas, then deliver the spec as a file plus a short summary of the design decisions.

## Conventions

| Topic | Default |
|---|---|
| Naming | `snake_case` or `camelCase` JSON fields (match the codebase), plural resource names, kebab-case paths |
| Status codes | 200 read/update, 201 create (with `Location`), 202 async accepted, 204 no body, 400 malformed, 401 unauthenticated, 403 forbidden, 404 not found, 409 conflict, 422 validation, 429 rate limited, 5xx server |
| Errors | RFC 9457 problem details: `type`, `title`, `status`, `detail`, `instance`, plus an `errors` array of `{field, message}` for validation |
| Pagination | cursor-based (`?limit=&cursor=`, response `next_cursor`) for feeds and large sets; offset only for small admin lists |
| Filtering and sorting | `?status=open&sort=-created_at` |
| IDs and time | opaque string IDs; RFC 3339 UTC timestamps |
| Retries | `Idempotency-Key` header on non-idempotent POSTs that create or charge |
| Concurrency | `ETag` plus `If-Match` for updates where lost writes matter |
| Versioning | additive changes without a version bump; breaking changes under `/v2` or a dated version header, with a deprecation period |
| Auth | OAuth 2.0 / OIDC bearer tokens for users; scoped API keys for server-to-server; never credentials in query strings |

## Example (OpenAPI fragment)

```yaml
paths:
  /orders/{order_id}/cancel:
    post:
      summary: Cancel an order that has not shipped
      parameters:
        - {name: order_id, in: path, required: true, schema: {type: string}}
        - {name: Idempotency-Key, in: header, required: false, schema: {type: string}}
      responses:
        "200": {description: Cancelled, content: {application/json: {schema: {$ref: "#/components/schemas/Order"}}}}
        "409":
          description: Order already shipped
          content:
            application/problem+json:
              example: {type: "https://api.example.com/errors/order-shipped", title: "Order already shipped", status: 409}
```

## Gotchas

- Returning database rows directly leaks internals and freezes the schema. Define response shapes separately.
- Booleans that will grow into states (`is_active`) should be enums from the start (`status`).
- Unbounded list endpoints become outages; always paginate with a maximum limit.
- Removing a field, renaming it or tightening validation is a breaking change, even if "nobody uses it".
- Webhooks need signing (HMAC with a timestamp), retries with backoff and idempotent receivers; document all three.

## Commands

- 🔌 **Contract before handlers** · `design api`: Designs the API from its consumers' needs: resources, style, models and rules, written as a spec and reviewed before any handler exists. Say who calls it and what they need.
  - 👥 **Consumers first** · `list api-consumers`: Names every client and the calls each needs, so the contract serves real use rather than the database shape.
  - 📐 **Shape the contract** · `shape contract`: Runs the three below in order: choose the style, model the resources, fix the rules.
    - 🎨 `choose api-style`: Picks REST, RPC, GraphQL or events for these consumers and says why, with the trade-off.
    - 🧱 `model resources`: Defines resources, fields, types and relationships with naming conventions applied consistently.
    - 📏 `set api-rules`: Fixes pagination, filtering, errors, versioning, auth and idempotency rules the whole API follows.
  - 📜 `write openapi-spec`: Writes the contract as an OpenAPI (or equivalent) spec with examples for each endpoint.
  - 🔍 `review api-contract`: Checks the design for breaking changes, inconsistency, missing errors and security gaps, ranked with fixes.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents software-dev/api-design` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review software-dev/api-design` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
