---
name: database-design
description: "Designs relational and document data models, writes safe forward and backward migrations, chooses indexes, and diagnoses slow queries from EXPLAIN plans. Use when the user asks to design or review a schema, tables, relations or an ERD, normalise data, write or review a migration, add an index, optimise a SQL query, or choose between database types. Do not use for general application slowness; use performance-tuning."
trigger: "design a database schema, write migrations or fix slow queries"
metadata:
  version: "1.1.0"
---

# Database design

🧬 **Core meme:** Model the data, migrate safely both ways, and measure before indexing.

Produce data models that keep data correct under concurrency, migrations that can run on a live system without downtime, and queries whose performance is proven by the query plan rather than guessed.

## Workflow: schema design

```
- [ ] 1. List entities, relationships and access patterns
- [ ] 2. Draft the schema with constraints
- [ ] 3. Choose indexes from the access patterns
- [ ] 4. Write the migration
- [ ] 5. Validate
```

1. **Access patterns first.** Write down the main reads and writes with rough volumes ("list a user's last 20 orders", "10k inserts/min"). Indexes and denormalisation follow from these.
2. **Draft.** Default to PostgreSQL and third normal form. Put integrity in the database, not only the application: `NOT NULL`, `UNIQUE`, `CHECK`, foreign keys with a deliberate `ON DELETE`. Use `bigint` identity or UUIDv7 keys, `timestamptz`, `numeric` for money (or integer minor units), `text` with CHECK constraints over `varchar(n)` guesses, and enums or lookup tables for states.
3. **Indexes.** Index foreign keys used in joins and columns in frequent `WHERE`, `ORDER BY` and `JOIN` clauses. Put equality columns before range columns in composite indexes. Use partial indexes for hot subsets (`WHERE status = 'open'`). Every index slows writes, so add each one for a named query.
4. **Migration.** Use the project's migration tool (Alembic, Django, Prisma, Flyway, Rails, goose). Every migration gets a working down or rollback step, or a note explaining why it cannot have one.
5. **Validate.** Apply the schema to a scratch database in the sandbox (SQLite for portable SQL, or `pip install pglast` to parse Postgres DDL), insert a few rows, and run the key queries.

Present the model as a Mermaid `erDiagram` when there are more than three tables.

## Safe migrations on live tables

Use expand–migrate–contract for anything that changes existing columns:

1. **Expand:** add the new column or table as nullable, with no default rewrite. Deploy code that writes to both.
2. **Migrate:** backfill in batches (for example 1,000–10,000 rows per transaction) to avoid long locks and replication lag.
3. **Contract:** once every reader uses the new shape, add constraints, then drop the old column in a later release.

On PostgreSQL, create indexes with `CREATE INDEX CONCURRENTLY` (outside a transaction), and add foreign keys and checks as `NOT VALID`, then `VALIDATE CONSTRAINT` separately.

## Workflow: slow query

1. Get the query and its plan: `EXPLAIN (ANALYZE, BUFFERS)` on Postgres, `EXPLAIN ANALYZE` on MySQL 8. Ask the person to run it if you cannot.
2. Find the node where time or rows explode: sequential scans on large tables, estimate vs actual row counts off by 10x or more (stale statistics, so run `ANALYZE`), nested loops over large inputs, sorts spilling to disk.
3. Fix in this order: add or adjust an index, rewrite the query (sargable predicates, `EXISTS` instead of `IN` with a subquery, avoiding `SELECT *`, keyset pagination instead of large `OFFSET`), then consider schema changes such as denormalising or a materialised view.
4. Show the plan before and after.

## Gotchas

- N+1 queries from an ORM look like "the database is slow". Check the query count per request before tuning single queries.
- Functions on indexed columns (`WHERE lower(email) = ...`) skip the index unless there is an expression index.
- `ALTER TABLE ... ADD COLUMN ... DEFAULT` with a volatile default rewrites the whole table on Postgres.
- Soft deletes (`deleted_at`) need partial unique indexes, or uniqueness breaks.
- Choose a document store only when access is mostly by key with flexible shape; relational is the safer default.

## Commands

- 🗄️ **Model, migrate both ways, measure** · `design database`: Designs schemas from access patterns, writes reversible migrations that are safe on live tables, and fixes slow queries by measuring first.
  - 🧱 **Design the schema** · `design schema`: Runs the three below in order from the application's queries.
    - 🔎 `list access-patterns`: Lists the reads and writes the application makes, with frequency and size, before drawing tables.
    - 📐 `draft tables`: Drafts tables, keys, types, constraints and relationships normalised to fit those patterns.
    - 📇 `plan indexes`: Chooses indexes for the real queries and explains the write cost of each.
  - 🔁 **Migrate safely** · `write migration`: Writes an up and down migration; for live tables uses expand, migrate, contract so nothing locks or breaks.
    - ➕ `expand schema`: Adds new columns or tables without breaking the running code.
    - 🚚 `backfill data`: Moves data in batches with a way to resume and verify.
    - ➖ `contract schema`: Removes old structures only after code no longer uses them.
  - 🐢 `fix slow query`: Runs EXPLAIN, finds the real cost, then indexes, rewrites or restructures and proves the gain with numbers.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents software-dev/database-design` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review software-dev/database-design` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
