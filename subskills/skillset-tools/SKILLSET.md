---
name: skillset-tools
description: "Tools for changing this skillset: write new sub-skills, edit or rename existing ones, organise members into nested skillsets, import skills, skillsets, zips and GitHub repositories, retire members, and publish it as a Claude plugin. Use when the user wants to add, change, reorganise, import, remove or publish skills in the skillset."
trigger: "find, write, edit, organise, import, publish or retire skills; keep self-memory"
metadata:
  version: "1.0.3"
---

# Skillset tools

The tools for changing this skillset. Each works on a working copy made by the `sync-skillset` sub-skill at the top, so read that first, then the member below that matches the request. To improve the skillset from other people's skills, `find-skills` learns from them and applies the lessons across the repository; `import-skill` copies a skill in unchanged only when that is what the person wants. Open a member with `python3 <top>/scripts/skillset.py open skillset-tools/<name>`, or read `subskills/<name>/SUBSKILL.md` beside this file.

## Commands

- 🧰 **Change the skillset itself** · `explore skillset-tools`: Sets focus on changing the skillset: write, edit, find, import, organise, publish or retire members, and keep self-memory. Every change starts with sync skillset.

## Members

<!-- subskills:start -->
| Member | Kind | Version | Use when |
|---|---|---|---|
| [edit-subskill](subskills/edit-subskill/SUBSKILL.md) | skill | 1.2.0 | Changes an existing sub-skill, a nested skillset's router text, or the skillset's own tooling. It makes the smallest edit that does what was asked, and renames the sub-skill when needed. It bumps the sub-skill's version, re-tests both the changed and unchanged behaviour, and leaves the skillset ready to package. Use when the user asks to edit, fix, improve, update, extend, tweak, rename, shorten or rewrite a skill or sub-skill, says one did the wrong thing or was not used when it should have been, or wants the skillset itself to work differently. |
| [find-skills](subskills/find-skills/SUBSKILL.md) | skill | 1.2.0 | Finds existing skills and learns from them instead of copying them in: searches skill registries, marketplaces and GitHub, studies the best candidates with the skillset's own faculties, extracts the lessons worth having (techniques, rules, gotchas, script ideas), rewrites them in the skillset's own words and structure, and applies them across every member they improve, then verifies, credits the sources and packages the whole repository. Use when the user asks to find, search for, discover or browse skills or plugins, asks whether a skill exists for something, wants to learn from or benchmark against other people's skills, or when a request needs a capability no member covers. Do not use for bringing in the person's own skill or an explicit verbatim copy; use import-skill. |
| [import-skill](subskills/import-skill/SUBSKILL.md) | skill | 1.2.0 | Brings existing skills into the skillset: a standalone skill, another skillset, a whole repository, or a collection of skills. Each can come from a folder, a zip or .skill file (zips inside zips included), an installed skill, or a GitHub repository that stays linked and can be refreshed. Use when the user asks to import, add, merge, consolidate, nest or link an existing skill, skillset, zip or repository, or to replace standalone skills with the skillset. Do not use for writing a skill from scratch; use the write-subskill sub-skill. |
| [organise-skillsets](subskills/organise-skillsets/SUBSKILL.md) | skill | 1.2.0 | Organises the skillset's structure. It creates nested skillsets, moves members between them, packs members into zips and unpacks them, and shows the whole tree at every depth, including inside zips. Use when the user asks to group, nest, organise, restructure, move, pack, zip, unzip or unpack skills, or wants to see what the skillset contains. It is also the fix when the description or file count nears its limit. |
| [publish-plugin](subskills/publish-plugin/SUBSKILL.md) | skill | 1.2.0 | Publishes the skillset as a Claude plugin and lists it in the Claude directory: checks the current directory rules, builds the shared edition (which doubles as the plugin), validates it with Claude Code's own validator, test-installs it, sets up the plugin repository, cuts the release and hands over the submission steps. Use when the user wants to share, publish, release or submit the skillset as a plugin or to the Claude directory or a marketplace. Do not use for building an upload only (sync-skillset) or for plugins of unrelated projects. |
| [retire-subskill](subskills/retire-subskill/SUBSKILL.md) | skill | 1.1.0 | Removes a member (a sub-skill, nested skillset or zip) from the skillset cleanly. It checks that nothing else depends on it, deletes it, and records a one-line restore command in the changelog, leaving the skillset ready to package. Use when the user asks to retire, remove, delete, drop, deprecate or get rid of a skill or sub-skill, says one is obsolete, unused or replaced by another, or wants a retired one back. Do not use to make a sub-skill do or trigger less; use the edit-subskill sub-skill for that. |
| [self-memory](subskills/self-memory/SUBSKILL.md) | skill | 1.2.0 | Keeps the AI's own persistent self-memory for Skillset-OS: turns a conversation's evidence into reviewed lessons, successes, failures, experiments, limitations and other self-knowledge, screens every item against the user-protection boundary, and exports or imports memory-pack.zip so another AI can carry on. Use when asked what Claude can do, what worked, what failed or what it has learned, to remember a lesson about its own work, to review or tidy its memory, to harvest lessons from memory into skill improvements, or to export, import or hand over its memory. Do not use for remembering facts about the person; those stay temporary task context. |
| [write-subskill](subskills/write-subskill/SUBSKILL.md) | skill | 1.4.0 | Writes a new sub-skill for the skillset. It captures what the sub-skill should do, picks a clear name, and writes a trigger and description that route requests to it reliably. Then it writes a lean SUBSKILL.md with any scripts or reference files and tests it against realistic prompts. Use when the user asks to create, write, draft, build or add a new skill or sub-skill, or to turn a workflow or this conversation into one. |
<!-- subskills:end -->

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents skillset-tools` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review skillset-tools` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
