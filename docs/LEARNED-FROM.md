# Learned from

Skills this skillset has learned from, rather than copied, by the `find-skills` loop: what was taken, where it was applied, and what was left behind. Material rewritten here is the skillset's own; where anything was copied or closely adapted, the source's licence sits beside it and is listed in [NOTICE.md](../NOTICE.md).

## 2026-09-25 — skills-search (daymade, MIT, github.com/daymade/claude-code-skills @ unpinned HEAD)

- Read-only registry commands (search, popular, recent, info) run directly by Claude rather than handed to the person → `skillset-tools/find-skills`
- Map user intents to commands in a table → `skillset-tools/find-skills`
- Fall back gracefully when the registry is unreachable, and say so → `skillset-tools/find-skills`
- Remind the person to restart after a standalone install → `skillset-tools/find-skills` (standalone installs section)
- Discarded: auto-running `ccpm setup` — it changes the person's Claude Desktop configuration without asking.
- Discarded: installing skills as standalone copies by default — they compete with the skillset; learning replaced importing.
- Discarded: the MCP server section — outside the skillset's scope.

## 2026-09-27 — an outside AI's architecture review (supplied by the person; no licence stated, nothing copied)

- The invariants of its proposed "constitution" and its performance-budget and change-surface ideas, rewritten and condensed → `docs/ARCHITECTURE.md` (Design principles)
- Its suggestion to cache routing metadata, narrowed after profiling to the real cost (YAML parsing) → `scripts/skillset.py`
- Its memory findings, compared by summary; only items new to this store were kept, re-added with fresh ids → self-memory
- Discarded for now: the executive layer, goal compiler, capability contracts and 18 design stubs — no evidence yet that they improve routing or task success; recorded as open maintenance instead.
- Discarded: its "v10/v17" labels — they were download-filename counters for 1.0.0 and 1.8.1.

## 2026-09-27 — a fork of 1.12.0 from another AI lineage (supplied by the person; it also called itself 1.13.0)

- Its host-capability mapping and adoption states, made platform-neutral and condensed → `docs/ARCHITECTURE.md` (Portability)
- Keeping platform-specific adaptations apart from the portable source → mapped onto the existing editions mechanism → `SKILL.md` (Other AIs)
- Its version collision → `skillset.py fingerprint`, and the harvest rule in `sync-skillset`
- Discarded: automatic adoption by any AI that receives a copy, and "become the service provider" — a copy given for review stays data.
- Discarded: its ChatGPT-specific profile as a separate document — a platform profile belongs in an edition when someone maintains one.
