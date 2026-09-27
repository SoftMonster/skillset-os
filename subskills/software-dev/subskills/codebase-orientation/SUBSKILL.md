---
name: codebase-orientation
description: "Maps an unfamiliar repository: detects languages, frameworks, package managers and the build, test and lint commands, then explains the architecture, entry points and data flow in a short orientation note. Use when the user uploads or links a repo and asks what it does or how it is organised, asks where something lives, is onboarding onto a project, or before any larger change in code Claude has not seen yet. Do not use for writing a design for new work; use plan-feature."
trigger: "understand, explore or explain an unfamiliar codebase or repository"
command: "orient codebase"
metadata:
  version: "1.1.0"
---

# Codebase orientation

🧬 **Core meme:** Find the real commands and entry points before changing anything.

Build an accurate mental model of an unfamiliar repository quickly, and hand the person a short orientation note they can trust: what the project is, how it is laid out, how to run it, and where the change they care about would go. Accuracy beats coverage; every claim should come from a file you actually read.

`<top>` is the installed skillset folder (the one holding the top `SKILL.md`).

## Workflow

```
- [ ] 1. Get the code on disk
- [ ] 2. Detect the stack
- [ ] 3. Read the map files
- [ ] 4. Trace one path end to end
- [ ] 5. Write the orientation note
```

1. **Get the code on disk.** Unzip an uploaded archive into `/home/claude/repo`, or `git clone --depth 1` a GitHub URL (github.com is reachable; most other hosts are not). For pasted files, work from what is in the chat.
2. **Detect the stack.** Run the detector; it reads manifests only and never executes project code:
   ```bash
   python3 <top>/subskills/software-dev/subskills/codebase-orientation/scripts/detect_stack.py /home/claude/repo
   ```
   It prints languages, package managers, frameworks, CI, containers, entry points and the inferred build, test, lint and format commands. Treat the commands as hypotheses until the README, Makefile or CI workflow confirms them, because CI is what the project actually runs.
3. **Read the map files, in this order:** README and CONTRIBUTING, the CI workflow, the dependency manifest, the entry points the detector found, then the top two levels of the tree (`find . -maxdepth 2 -not -path '*/node_modules*' -not -path '*/.git*'`). Skim; do not read every file.
4. **Trace one path end to end.** Pick the request that matters to the person (or the main user flow) and follow it from entry point through routing, business logic and persistence, noting file:line at each hop. `grep -rn` for route strings, handler names and table names. One traced path explains more than a tour of every folder.
5. **Write the orientation note** using the template below. Keep it under a page. If the person asked a specific question ("where is auth handled?"), answer that first in one or two sentences, then give only the parts of the note that support the answer.

## Orientation note template

```markdown
**What it is:** one sentence, in the project's own terms.
**Stack:** languages, framework, datastore, key libraries.
**Run it:** install / test / lint / start commands (confirmed from README or CI).
**Layout:** 4–8 lines, one per important folder, saying what lives there.
**How a request flows:** entry → router → handler → service → storage, with file paths.
**Conventions:** error handling, config, naming, test layout Claude should copy.
**Watch out for:** generated code, surprising coupling, dead folders, missing tests.
```

A diagram helps when there are more than three services or layers; draw it as a Mermaid flowchart.

## Gotchas

- Monorepos have several manifests. Run the detector on each package folder, not only the root.
- Generated folders (`gen/`, `*_pb2.py`, `migrations/` in some frameworks, OpenAPI clients) look important but are not where changes go. Say so in the note.
- A README's commands are often stale. When README and CI disagree, trust CI and mention the drift.
- Do not install dependencies or run the project just to orient unless the person asks; it is slow and may need network access the sandbox lacks.

## Commands

- 🧭 **Real commands and entry points first** · `orient codebase`: Explores an unfamiliar repository: gets it on disk, detects the stack, reads the map files in order, traces one path end to end, and writes an orientation note.
  - 📥 `get repository`: Gets the code into the sandbox from an upload, a zip or a public GitHub clone.
  - 🧪 `detect stack`: Identifies languages, frameworks, package managers and test runners from manifest files, not guesses.
  - 🗺️ `read map files`: Reads README, manifests, CI config, entry points and tests in that order to learn how the project really runs.
  - 🧵 `trace request path`: Follows one real request or command from entry point to output, naming each file it passes through.
  - 📝 `write orientation note`: Writes the note: how to run, test and build, the architecture in a paragraph, key files, and risks.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents software-dev/codebase-orientation` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review software-dev/codebase-orientation` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
