---
name: metacognition
description: "Self-monitoring faculties: metacognition, the conductor that chooses which faculty to apply, and continuous self-correction (skill acquisition and composition live in action-agency, self-model in memory-context, ethical skill evolution in safety-governance). Use when the user wants to think about how they think or keep improving, or when Claude checks its own reasoning, chooses an approach or corrects course mid-task."
trigger: "think about my thinking, monitor and correct myself as I go, test my own skills, or grow my own abilities"
metadata:
  version: "1.0.0"
---

# Metacognition

A nested skillset. Pick the member whose "Use when" matches the request and read its instructions; for a nested skillset or a zip, run `python3 <top>/scripts/skillset.py open <path>` to get the file to read.

These are the faculties of watching and improving one's own mind. Each member has a "For people" and a "For Claude" half. `metacognition` is also the conductor of the whole framework: it chooses which faculty to apply and checks that it worked.

Four faculties of this group have their home elsewhere, so there is one copy of each:
- **🧬 Skill acquisition** and **🧰 skill composition:** `cognition/action-agency`.
- **🪞 Self-model:** `cognition/memory-context`.
- **🧬 Ethical skill evolution:** `cognition/safety-governance`. Every change Claude proposes to its own skills follows it.

## Members

<!-- subskills:start -->
| Member | Kind | Version | Use when |
|---|---|---|---|
| [continuous-self-correction](subskills/continuous-self-correction/SUBSKILL.md) | skill | 1.0.0 | Keeps work on track and improving: sets checkpoints, monitors for drift and errors during work, corrects course early and small, and feeds lessons from each task into the next through a light retrospective and a lasting change. For people, covers noticing and correcting mid-task, building personal feedback loops and continuous improvement at work; for Claude, covers checking its output against the goal at intervals during long tasks, correcting itself unprompted when it spots a problem, and turning recurring lessons into proposed skill edits. Use when the user wants to catch mistakes earlier or build a habit of steady improvement, or when Claude is partway through a long task or reviewing how a task went. For fixing an error already found, use error-correction in action-agency. |
| [exam-regression-battery](subskills/exam-regression-battery/SUBSKILL.md) | skill | 1.0.1 | Reruns every earlier self-examination check in seconds and reports PASS, FAIL or KNOWN with evidence, so each new exam run starts from reproduced evidence instead of losing it. Use when starting a curriculum exam run or after changing the skillset. Do not use to run the timed exam itself; use universal-skill-curriculum-exam. |
| [metacognition](subskills/metacognition/SUBSKILL.md) | skill | 1.0.0 | Builds metacognition: knowing what one knows and does not, planning how to approach a task, monitoring understanding and progress while working, evaluating afterwards, and choosing which mental faculty or strategy fits. For people, covers studying and problem-solving strategically, noticing confusion, judging readiness and avoiding the illusion of competence; for Claude, covers monitoring its own reasoning, noticing when it is guessing or confused, choosing which faculty in this framework to apply, and orchestrating the others. Use when the user wants to learn or think more strategically, keeps being surprised by their results, or asks how to think about a problem, or when Claude must choose an approach or check its own thinking. |
| [universal-skill-curriculum-exam](subskills/universal-skill-curriculum-exam/SUBSKILL.md) | skill | 1.0.1 | Conduct a comprehensive self-assessment of an AI against a large, capability-normalized Claude skill curriculum. Use this skill when asked to assess an AI's skill coverage, run the Universal Skill Curriculum Exam, benchmark Claude skills, identify capability gaps, test skill orchestration, evaluate AI self-improvement, or produce lessons and pushbacks for improving the examination. The examiner must inspect the bundled curriculum and any actually available skill files before claiming exact skill behaviour. |
<!-- subskills:end -->

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/metacognition` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/metacognition` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
