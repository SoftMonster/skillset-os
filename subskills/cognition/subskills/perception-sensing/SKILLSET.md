---
name: perception-sensing
description: "Input faculties: perception, attention, uncertainty awareness and feedback processing. Use when the user wants to be more observant, focused, calibrated or responsive to feedback, or when Claude must read inputs carefully, stay on the key details, state its confidence honestly or adjust to a correction or surprise."
trigger: "notice more, focus attention, gauge uncertainty or learn from feedback"
metadata:
  version: "1.0.1"
---

# Perception sensing

A nested skillset. Pick the member whose "Use when" matches the request and read its instructions; for a nested skillset or a zip, run `python3 <top>/scripts/skillset.py open <path>` to get the file to read.

These are the input faculties: what comes in, what gets focus, how sure to be about it, and how results feed back. They run in a loop: **perceive → attend → estimate certainty → act → process feedback → perceive again**. Each member has a "For people" and a "For Claude" half.

## Members

<!-- subskills:start -->
| Member | Kind | Version | Use when |
|---|---|---|---|
| [attention](subskills/attention/SUBSKILL.md) | skill | 1.0.0 | Manages where focus goes: chooses what deserves attention, filters distraction, sustains focus in blocks, notices drift and returns deliberately. For people, covers concentration, phone and notification distraction, deep work, mind-wandering and restoring depleted attention; for Claude, covers attending to what was actually asked, weighting the most important instructions and details, and holding the thread through long or dense contexts. Use when the user cannot concentrate, is constantly distracted, wants deep focus or attention training, or when Claude faces a long task where key details could be lost. Do not use for scheduling a week; use plan-and-prioritise in self-improvement. |
| [feedback-processing](subskills/feedback-processing/SUBSKILL.md) | skill | 1.0.1 | Turns signals into updated behaviour: notices feedback (explicit comments, reactions, outcomes, error messages), judges its reliability, separates signal from noise, updates in proportion to the evidence, and closes the loop. For people, covers learning from results and criticism without over- or under-reacting; for Claude, covers reading tool output, test results and the person's reactions and adjusting mid-task. Use when the user repeats mistakes, overreacts to or ignores feedback, wants faster learning loops, or when Claude gets a correction, a failing test or an unexpected result. Do not use for the conversation of giving or receiving feedback; use feedback in interpersonal. |
| [perception](subskills/perception/SUBSKILL.md) | skill | 1.0.1 | Improves how information is taken in and interpreted: separates observation from interpretation, notices what is present, missing or anomalous, checks for misreadings and alternative interpretations, and reads inputs fully before acting. For people, trains observation and noticing; for Claude, governs how it reads prompts, files, images, tool output and search results, including checking that an expected file or detail is actually there. Use when the user wants to be more observant, notice details, read people, rooms or documents more accurately, or jumps to conclusions, and whenever Claude must interpret inputs carefully. |
| [uncertainty-awareness](subskills/uncertainty-awareness/SUBSKILL.md) | skill | 1.0.1 | Tracks how sure to be: separates known, inferred and guessed, assigns rough confidence, spots missing information and the edges of knowledge, and decides whether to act, hedge, check or ask. For people, builds calibration, better forecasts and tolerance of ambiguity; for Claude, governs stating confidence honestly, flagging knowledge-cutoff and fabrication risk, and searching or asking instead of guessing. Use when the user wants to make predictions, judge how confident to be, avoid overconfidence, cope with not knowing, or when Claude answers something it may not know reliably. |
<!-- subskills:end -->

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/perception-sensing` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/perception-sensing` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
