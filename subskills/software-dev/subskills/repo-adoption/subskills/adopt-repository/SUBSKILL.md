---
name: adopt-repository
description: "Turns another repository, codebase or app (a zip, folder or GitHub repository) into a develop-PROJECT sub-skill in this skillset: its source is stored in the member's app folder and versioned with the skillset, a project checker encodes the project's runtime limits, promises and core logic, and a release workflow sends each change through the rest of the skillset. It scaffolds the member with adopt.py, writes and mutation-tests the checker, wires routing and tests, and packages. Use when the user asks to adopt, bring in, take over or make a develop skill for a repository, project or app, or to keep a project's code in the skillset. Do not use for changing an already adopted project; use its develop-PROJECT member. Do not use for importing skills; use import-skill."
trigger: "adopt a repository, codebase or app so Claude can develop it"
metadata:
  version: "1.0.0"
---

# Adopt a repository

🧬 **Core meme:** Bring the code in, write down its promises, make them checkable, then develop it with everything.

This turns someone's project into a `develop-PROJECT` member of this nested skillset. That member keeps the project's source in its `app/` folder, where it is versioned and shipped with the skillset. It has a checker that proves what Claude cannot run, and a release workflow that sends every change through the rest of the skillset. Adoption is done when the member passes its own checks, routes correctly, and is packaged. `templates/DEVELOP.md` is the pattern every develop member follows: read it before writing a new one.

`<wc>` is the skillset working copy and `<here>` is this folder.

## Workflow

```
- [ ] 1. Working copy
- [ ] 2. Inspect the source (dry run)
- [ ] 3. Scaffold the member
- [ ] 4. Read the project and write down its rules
- [ ] 5. Write the checker and prove it catches mistakes
- [ ] 6. Write the develop member
- [ ] 7. Route and test
- [ ] 8. Package and hand over
```

### 1. Working copy

Follow `sync-skillset` step 1. Adoption adds files to the repository, so it never works on the installed copy.

### 2. Inspect the source (dry run)

```bash
python3 <here>/scripts/adopt.py NAME SOURCE --title "Title" --trigger "develop, fix or improve Title" \
  --description "Develops Title, ... Use when ..." --dry-run
```

SOURCE is an attached zip (`/mnt/user-data/uploads/...`), a folder, or `owner/repo` on GitHub. The dry run prints the file count, file types, largest files and detected stack, plus the plan. It refuses a source containing `SKILL.md`, `SUBSKILL.md` or `SKILLSET.md`, since that is a skill and belongs to `skillset-tools/import-skill`. For a large repository, adopt only the part that will be developed, or keep it on GitHub and link it with `import-skill`. Stop and tell the person if the source isn't theirs to redistribute.

NAME is the project slug (`tally`), and the member becomes `develop-tally`. Write the trigger in the words the person uses for the project, and a description that starts with the project name and what it is.

### 3. Scaffold the member

Run the same command without `--dry-run`. It creates the member through `skillset.py new` and copies the source into `app/`, leaving out `.git`, `node_modules` and caches. It then writes:

- `SUBSKILL.md` from [templates/DEVELOP.md](templates/DEVELOP.md): the shared release workflow, with TODOs for everything specific to the project;
- `scripts/NAME.py` from [templates/checker.py](templates/checker.py): a checker skeleton with `check` and `build`;
- `app/CHANGELOG.md`;
- `tests/test_NAME.py`, which makes CI run the checker.

From here `skillset.py check` fails on the TODOs until step 6 is finished. That is on purpose: it stops a half-adopted project from being packaged.

### 4. Read the project and write down its rules

Follow `software-dev/codebase-orientation`, and read the project's own README or manual in full. Write down:

- **What it is and where it runs.** Note the runtime and its limits. For example, a Windows HTA runs its script in mshta's IE11 engine, so only ES5 is allowed.
- **Embedded or generated parts** that are unsafe to edit by hand. For example, a browser extension stored as JSON inside the app, or a script inside an HTML-escaped textarea.
- **The promises it makes to its users**, each with a reason. For example: read-only on Steam, no credentials, Steam hosts only.
- **Its core logic and its written spec**, such as the fee rules in README section 7.
- **What must stay in step.** Versions in several places, and docs copied into other files.
- **Its conventions for handling events and errors**: wrappers that swallow or queue calls, escaping helpers and what they escape for, and how data files are read and written. For example, a guard that silently drops clicks while the window is busy.
- **What Claude cannot run here**, which becomes a test list for the person.

Use `cognition/safety-governance/privacy-stewardship` and `cognition/reasoning/adversarial-thinking` to find promises the README only implies.

### 5. Write the checker and prove it catches mistakes

Turn each rule into a check in `scripts/NAME.py`, which reports `ok`, `FAIL` or `SKIPPED` with a reason. Patterns that pay off:

- **Runtime limits:** parse the code and walk the syntax tree for features the target cannot run. Parsing alone is not enough, because a modern parser accepts code an old engine rejects.
- **Core logic:** extract the pure functions (with esprima for JS) and run them (Node for JS) over a wide range of inputs. Compare the results with an independent version written from the project's own spec, not from its code.
- **Promises:** allow-lists of hosts, permissions and APIs. Widening one is a product decision, so the check names the constant to change.
- **Consistency:** versions agree, and copied docs match their original.
- **Embedded parts:** `extract` and `embed` commands. Test that extracting and embedding with no edits gives byte-identical output, so editing through them can't corrupt the file.
- **Build:** produce the artefact in the exact layout the person already ships.

**Make it run, not just parse.** If the project can't run in the sandbox, build a runner in `scripts/` with stand-ins for the missing platform pieces. For example, load a Windows HTA in jsdom with an in-memory file system and shell. Give the runner realistic test data, behaviour tests, and a regression test against the version last committed in git. Static checks alone miss behaviour bugs that a runner catches. Time a big dataset too, because performance traps (live collections, per-row style writes) only show up at scale. Keep the runner to one or two files, since every file counts against the upload limit, and install its dependencies outside the skillset.

Then **prove every check can fail**. On a scratch copy of the member, introduce one deliberate mistake per check and confirm it fails with a useful message. Typical ones: a syntax feature the runtime lacks, a wrong constant, `round` instead of `floor`, an unlisted host and mismatched versions. A check that never fails proves nothing. Follow `software-dev/write-tests` and add fast unit tests of the checker to `tests/test_NAME.py`.

The baseline must pass on the unchanged source. If it fails, tell the person what the check found, since it may be a real bug.

### 6. Write the develop member

Replace every TODO in the new `SUBSKILL.md` using what steps 4 and 5 found: the project's rules, its commands, a real example taken from its code, and the gotchas you hit. Keep the shared workflow as the template gives it, so every develop member works the same way. Follow `skillset-tools/write-subskill` for wording, and keep it under 500 lines.

### 7. Route and test

- Add the project's name to this nested skillset's trigger if it is not already routed. For example: "or develop an adopted one like Tally". Keep `software-dev`'s own trigger short, because it feeds the top description (limit 1024 characters). `skillset.py index` prints how much is used.
- Add three prompts that should reach the member to `tests/routing.json`, written the way the person talks about the project.
- Run `python3 <wc>/scripts/skillset.py check`, `ruff check .` and `pytest`.

### 8. Package and hand over

Run `python3 <wc>/scripts/skillset.py package --message "Adopt PROJECT" --bump minor`, then use the `build` of the new checker to produce the project artefact. Hand over as `sync-skillset` step 4 says, and add:

- what the checker proves and what stays SKIPPED;
- any real bugs the checks or reading turned up (report them; don't fix them unasked);
- that later changes go through the new `develop-PROJECT` member.

## Gotchas

- A skillset over 190 files still uploads as one skill: `package` zips its largest groups inside the upload (see `sync-skillset`), so adopted projects never need packing in the repository.
- Tests that copy the whole skillset can pass the file limit once projects are added. Keep test fixtures independent of the skillset's size.
- `ruff check .` only lints the top `scripts/` and `tests/`. Lint new checkers yourself with `ruff check --line-length 120 <file>`.
- Some source files have enormous single lines, such as embedded bundles or JSON. One `grep` hit can flood the context. Cut every search of the source (`| cut -c1-200`) and write the offending line into the develop member's Gotchas.
- Keep the project's own line endings and file names (spaces included). The checker's `build` should reproduce the person's release layout exactly, not tidy it up.
- The sandbox cannot reach the project's live services (Steam, APIs). Checks that need them are SKIPPED and go into the person's test list.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents software-dev/repo-adoption/adopt-repository` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review software-dev/repo-adoption/adopt-repository` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
