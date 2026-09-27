---
name: organise-skillsets
description: "Organises the skillset's structure. It creates nested skillsets, moves members between them, packs members into zips and unpacks them, and shows the whole tree at every depth, including inside zips. Use when the user asks to group, nest, organise, restructure, move, pack, zip, unzip or unpack skills, or wants to see what the skillset contains. It is also the fix when the description or file count nears its limit."
trigger: "group, nest, move, pack or unpack skills, or show what the skillset contains"
metadata:
  version: "1.1.0"
---

# Organise skillsets

🧬 **Core meme:** Shape the tree so requests route cleanly and uploads stay in limits.

Shape the skillset so requests route cleanly and the upload stays within its limits, without changing what any member does.

Work in the working copy from `sync-skillset`. `<wc>` below is that folder, usually `/home/claude/skillset-os`. Just looking (`tree`, `open`) works on the installed copy too.

## When to nest, and when to pack

- **Nest** related members in a skillset when there are several of the same kind (writing, data, a team's workflows), or when the top description passes about 900 characters. Only top-level members add their triggers to the top description, so a group costs one trigger however many members it holds.
- **Pack** a member into a zip only for storage: someone else's repository to keep sealed, or a rarely used member kept for reference. A zip is not a skill: Claude's skill system never loads anything inside one, so a packed member works only where code execution can run `skillset.py open`, and `check` warns about each one. Never pack to get under the file limit; `package` splits into plain part skills instead. Packed members are read-only until unpacked.
- **Unpack** before editing a packed member, and to split a packed repository's members out.
- Keep `sync-skillset` at the top and unpacked; the tools refuse otherwise.

## Commands

```bash
python3 <wc>/scripts/skillset.py tree [--depth 2]                      # everything, including inside zips
python3 <wc>/scripts/skillset.py open <path>                           # print a member's instructions file
python3 <wc>/scripts/skillset.py new-set <path> --description "<what it groups. Use when ...>" --trigger "<phrase>"
python3 <wc>/scripts/skillset.py move <path> --into <set>              # --into "" moves to the top
python3 <wc>/scripts/skillset.py pack <path>
python3 <wc>/scripts/skillset.py unpack <path>
python3 <wc>/scripts/skillset.py rename <path> <new-name>
```

Paths name members from the top: `writing/blog-post` is `blog-post` inside the nested skillset `writing`. Every command updates the routers, the changelog and `skillsets.json`, including linked-repository records and trigger overrides, which move with their members.

## Workflow

```
- [ ] 1. Working copy (sync-skillset, step 1)
- [ ] 2. Look at the tree and plan
- [ ] 3. Restructure
- [ ] 4. Check routing
- [ ] 5. Package (sync-skillset, steps 3 and 4)
```

1. Get the working copy.
2. Run `tree` and write down the target shape in a few lines (which groups, what moves, what gets packed). If the person's request leaves the grouping open, propose one and go ahead unless it would rename things they use.
3. Create groups with `new-set`, then `move` members into them. Its `--trigger` must cover what its members do, in the words people use; its description should list the kinds of request it handles. `pack` or `unpack` as planned.
4. Run `skillset.py check`. Then take three realistic requests and route each by hand from the top description through each table to the sub-skill. Fix triggers or descriptions where the route is unclear.
5. Package with `--bump minor` (or `--bump major` if members people use by name moved or were renamed).

## Gotchas

- A moved or renamed member breaks mentions of its old path in other members; `rename` lists them, and `check` finds broken links.
- An empty nested skillset triggers a warning; move members in before packaging.
- Unpacking a repository that holds several `SKILL.md` files is refused, because the upload allows only one outside zips. Keep it packed, or import its skills individually with `import-skill`.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents skillset-tools/organise-skillsets` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review skillset-tools/organise-skillsets` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
