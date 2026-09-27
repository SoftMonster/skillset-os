---
name: continuous-self-correction
description: "Keeps work on track and improving: sets checkpoints, monitors for drift and errors during work, corrects course early and small, and feeds lessons from each task into the next through a light retrospective and a lasting change. For people, covers noticing and correcting mid-task, building personal feedback loops and continuous improvement at work; for Claude, covers checking its output against the goal at intervals during long tasks, correcting itself unprompted when it spots a problem, and turning recurring lessons into proposed skill edits. Use when the user wants to catch mistakes earlier or build a habit of steady improvement, or when Claude is partway through a long task or reviewing how a task went. For fixing an error already found, use error-correction in action-agency."
trigger: "catch drift and errors as I go and keep improving"
metadata:
  version: "1.0.0"
---

# 🔄 Continuous Self-Correction

🧬 **Core meme:** Catch drift early and small, and carry one lesson into the next task.

Correct course while working, and get a little better with every task. Small drifts caught early are cheap; the same drifts caught at the end are expensive. Continuous self-correction runs two loops: a fast one inside a task, and a slow one across tasks.

## The fast loop (during a task)

1. **Checkpoints:** decide in advance where to pause (after each section, step or hour).
2. **Compare:** output so far against the goal and the criteria.
3. **Spot drift:** scope creep, quality slipping, a wrong assumption, a missed requirement.
4. **Correct small and early:** adjust now rather than finishing and redoing.

## The slow loop (across tasks)

1. **Retrospective:** a few lines after meaningful work: what worked, what did not, why (see `reflect-and-review` in self-improvement).
2. **One change:** pick the single adjustment with the most value.
3. **Make it stick:** turn it into a checklist item, template, habit or default.
4. **Check it worked** next time.

## For people

- **At work:** checkpoints on long pieces of work; a five-minute retrospective after projects; a running "lessons" note reviewed before similar work.
- **Personal:** notice mid-task when energy or focus drops and adjust (break, simplify, switch); a weekly review.
- **Teams:** blameless retrospectives; improvements owned by someone with a date.
- **Tone:** corrections are adjustments, not verdicts. See `mindset-resilience` in self-improvement.

## For Claude

- **Check at intervals** during long or multi-step tasks: re-read the request and compare with the work so far; fix drift before continuing.
- **Self-correct unprompted:** if Claude notices an earlier statement in the conversation was wrong, it says so and corrects it.
- **Retrospective after substantial tasks** when useful: a few lines, not padding.
- **Lasting improvement means a skill edit,** proposed to the person, following `ethical-skill-evolution` in safety-governance: the person approves, values stay fixed, and the change is recorded.
- **Recurring correction from the person** (the same point twice) is the strongest signal for a proposed edit (see `habit-building` in self-improvement).

For fixing a specific error once found, use `error-correction` in action-agency.

## Gotchas

- Constant correction without a goal becomes fiddling; tie every correction to the criteria.
- Improvements that are not captured in a system are forgotten.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/metacognition/continuous-self-correction` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/metacognition/continuous-self-correction` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
