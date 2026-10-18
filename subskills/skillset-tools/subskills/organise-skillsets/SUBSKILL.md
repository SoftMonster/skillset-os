---
name: organise-skillsets
description: "Organises the skillset's structure. It creates nested skillsets, moves members between them, unpacks zipped members left by older copies, and shows the whole tree at every depth. Use when the user asks to group, nest, organise, restructure, move or unpack skills, or wants to see what the skillset contains. It is also the fix when the description or file count nears its limit."
trigger: "group, nest, move or unpack skills, or show what the skillset contains"
metadata:
  version: "2.0.0"
---

# Organise skillsets

🧬 **Core meme:** Shape the tree so requests route cleanly and uploads stay in limits.

Shape the skillset so requests route cleanly and the upload stays within its limits, without changing what any member does.

Work in the working copy from `sync-skillset`. `<wc>` below is that folder, usually `/home/claude/skillset-os`. Just looking (`tree`, `open`) works on the installed copy too.

## When to nest, and why never zip

- **Nest** related members in a skillset when there are several of the same kind (writing, data, a team's workflows), or when the top description passes about 900 characters. Only top-level members add their triggers to the top description, so a group costs one trigger however many members it holds.
- **Never zip a member.** claude.ai rejects any skill upload that holds a zip ("Zip cannot contain nested zip files"), and Claude cannot load a zip as a skill anyway. Zipped members were retired in 2.0.0; `check` refuses any zip in the tree. Over the file limit, merge small files or let `package` split into plain part skills.
- **Unpack** a zipped member left by a 1.x copy with `skillset.py unpack <path>`. It unpacks any zipped members inside it too.
- Keep `sync-skillset` at the top; the tools refuse otherwise.

## Commands

- 🌲 **Shape the tree for clean routes** · `organise skillsets`: Groups, nests or moves members, unpacks old zipped ones, or shows what the skillset contains, keeping routing clean and uploads within limits.
  - 🪺 `nest members`: Groups related members into a nested skillset so the top description stays short.
  - 📂 `unpack zipped member`: Turns a zipped member from a 1.x copy into a plain folder, inner zips included.
  - 🗺️ `show skillset layout`: Shows the whole tree of members with versions and triggers.

## Workflow

```
- [ ] 1. Working copy (sync-skillset, step 1)
- [ ] 2. Look at the tree and plan
- [ ] 3. Restructure
- [ ] 4. Check routing
- [ ] 5. Package (sync-skillset, steps 3 and 4)
```

1. Get the working copy.
2. Run `tree` and write down the target shape in a few lines (which groups, what moves, what needs unpacking). If the person's request leaves the grouping open, propose one and go ahead unless it would rename things they use.
3. Create groups with `new-set`, then `move` members into them. Its `--trigger` must cover what its members do, in the words people use; its description should list the kinds of request it handles. `unpack` any zipped members.
4. Run `skillset.py check`. Then take three realistic requests and route each by hand from the top description through each table to the sub-skill. Fix triggers or descriptions where the route is unclear.
5. Package with `--bump minor` (or `--bump major` if members people use by name moved or were renamed).

## Gotchas

- A moved or renamed member breaks mentions of its old path in other members; `rename` lists them, and `check` finds broken links.
- An empty nested skillset triggers a warning; move members in before packaging.
- Unpacking a repository that holds several `SKILL.md` files is refused, because the upload allows only one. Import it as a collection, or its skills one by one, with `import-skill`, then retire the zipped copy.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents skillset-tools/organise-skillsets` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review skillset-tools/organise-skillsets` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
