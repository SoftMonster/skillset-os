---
name: exam-regression-battery
description: "Reruns every earlier self-examination check in seconds and reports PASS, FAIL or KNOWN with evidence, so each new exam run starts from reproduced evidence instead of losing it. Use when starting a curriculum exam run or after changing the skillset. Do not use to run the timed exam itself; use universal-skill-curriculum-exam."
trigger: "rerun my earlier exam checks as a quick regression battery"
command: "rerun exam"
metadata:
  version: "1.1.0"
---

# Exam regression battery

🧬 **Core meme:** Rerun the old proof first, then spend the run on new ground.

Each exam run is marked only on its own evidence. Without a battery, a new run drops everything earlier runs proved, and scores stall (runs 1–3: 412 → 907 → 984). The battery rebuilds that evidence in seconds.

## Workflow

1. Run `bash scripts/battery.sh > battery.out` and keep the output as run evidence.
2. Run `python3 scripts/audit.py < battery.out`. It fails if any passing check has no negative control (rule 1), if a control sits on a failing main check (rule 8), or if anything failed.
3. Read every line: `PASS` counts, `FAIL` is a finding to diagnose before new work, and `KNOWN` is an open limitation.
4. Spend the rest of the run on areas the battery does not cover, then add the new check to the battery.

## Adding a check

Every check prints one line: status, id and evidence. Before trusting a check, prove it can fail with a negative control (a sabotaged input it must reject). Checks run in a temporary folder and never touch the installed skill.

## Gotchas

- Exit code 0 is not proof. `git bundle verify` accepts a truncated bundle with no refs, so the backup check restores the bundle and compares refs.
- `git bundle verify` must run inside a repository.
- Run with `PYTHONDONTWRITEBYTECODE=1`. Stale `.pyc` files can mask a restored file.
- `/bin/sh` `printf` has no `\x` escapes. Write binary fixtures from Python.

## Commands

- 🔁 **Rerun the old proof first** · `rerun exam`: Reruns earlier exam checks as a quick regression battery before new exam work.
  - ➕ `add exam check`: Adds a new check to the battery from a passed exam item, with its expected evidence.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/metacognition/exam-regression-battery` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/metacognition/exam-regression-battery` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
