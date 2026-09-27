---
name: repo-adoption
description: "Adopts other repositories and apps into the skillset so Claude can develop them: the adopt-repository member turns a zip, folder or GitHub repository into a develop-PROJECT sub-skill that keeps the project's source, its own checks and a release workflow applying the rest of the skillset, and each develop-PROJECT member then handles changes to its project. Use when the user wants to bring a codebase, app or repository into the skillset, make a develop skill for a project, or fix, change, improve or release an adopted project."
trigger: "adopt a repository or app so Claude can develop it, or develop an adopted one"
metadata:
  version: "1.0.0"
---

# Repository adoption

A nested skillset. Pick the member whose "Use when" matches the request and read its instructions; for a nested skillset or a zip, run `python3 <top>/scripts/skillset.py open <path>` to get the file to read.

It has two kinds of member:

- **`adopt-repository`** brings a project in. It stores the source in a new member's `app/` folder, writes a checker for that project's rules, and wires up routing and tests.
- **`develop-PROJECT`** members, one per adopted project (for example `develop-tally` for a project called Tally), handle every later change. Each follows the same release workflow, from `adopt-repository/templates/DEVELOP.md`, and sends the work through the rest of the skillset.

A request about a project that is already adopted goes to its develop member, even if the person attaches a newer copy of it.

## Members

<!-- subskills:start -->
| Member | Kind | Version | Use when |
|---|---|---|---|
| [adopt-repository](subskills/adopt-repository/SUBSKILL.md) | skill | 1.0.0 | Turns another repository, codebase or app (a zip, folder or GitHub repository) into a develop-PROJECT sub-skill in this skillset: its source is stored in the member's app folder and versioned with the skillset, a project checker encodes the project's runtime limits, promises and core logic, and a release workflow sends each change through the rest of the skillset. It scaffolds the member with adopt.py, writes and mutation-tests the checker, wires routing and tests, and packages. Use when the user asks to adopt, bring in, take over or make a develop skill for a repository, project or app, or to keep a project's code in the skillset. Do not use for changing an already adopted project; use its develop-PROJECT member. Do not use for importing skills; use import-skill. |
<!-- subskills:end -->

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents software-dev/repo-adoption` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review software-dev/repo-adoption` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
