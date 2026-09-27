---
name: error-correction
description: "Handles errors well: detects them early, finds the root cause, fixes the cause rather than the symptom, owns the mistake honestly, repairs any impact and prevents a repeat. For people, covers making fewer mistakes, recovering from them and building error-catching systems; for Claude, covers acknowledging its errors plainly, correcting them without excessive apology, checking whether the same error appears elsewhere, and proposing a skill edit to prevent recurrence. Use when the user made a mistake and needs to fix it, keeps making the same errors, or wants mistake-proof systems, or when Claude discovers or is told of an error. For code bugs, use debug-issue in software-dev."
trigger: "catch, own and fix mistakes"
command: "correct errors"
metadata:
  version: "1.1.0"
---

# 🐛 Error Correction

🧬 **Core meme:** Own it, fix the cause, and check for the same error elsewhere.

Catch mistakes early, fix their cause, own them, and prevent a repeat. The brain has an error-detection system that fires within a fraction of a second of a slip; good error correction listens to it instead of explaining it away, and treats errors as information rather than verdicts.

## The model

1. **Detect:** notice the mismatch (a result, a reaction, a nagging feeling).
2. **Contain:** stop the error spreading (pause, undo, tell people who rely on it).
3. **Diagnose:** find the root cause, not the nearest symptom (ask "why?" until reaching something fixable).
4. **Fix the cause** and repair any impact.
5. **Own it:** state it plainly to those affected.
6. **Prevent:** change the system (checklist, default, safeguard) so it is harder to repeat.

## For people

- **Error-catching systems:** checklists, templates, second pairs of eyes, and pauses before irreversible actions.
- **Recurring mistakes:** log them for two weeks; most fall into a few patterns with a common cause (rushing, missing information, fatigue).
- **Owning mistakes:** say what happened, the impact, what you are doing about it. For the conversation, see `apologies-repair` in interpersonal.
- **Emotional side:** shame makes people hide errors; treat errors as system problems. See `mindset-resilience` in self-improvement.

## For Claude

- **Acknowledge plainly:** "I got that wrong: X should be Y." Once, without excessive apology or self-abasement.
- **Fix the cause:** not just the instance the person noticed; check whether the same error appears elsewhere in the answer, file or code.
- **Correct the record** when an earlier answer in the chat was wrong, even if the person has not noticed.
- **Prevent recurrence:** if the error is a pattern, propose a skill edit (see `habit-building` in self-improvement).
- **Stay steady:** being wrong on one point is not a reason to abandon correct points under pressure.

For code bugs, use `debug-issue` in software-dev.

## Gotchas

- Fixing symptoms makes errors return in new forms.
- Blame-focused cultures hide errors; learning-focused ones surface them.

## Commands

- 🩹 **Own it, fix the cause, check elsewhere** · `correct errors`: Handles a mistake with detect, contain, diagnose, fix the cause, own it and prevent, and checks for the same error elsewhere.
  - 🧑 **For you** · `fix my mistake`: Helps a person recover from a mistake they made: contain the damage, find the cause, own it well and prevent a repeat.
  - 🤖 **For Claude** · `own claude error`: Claude states its error plainly, fixes it, checks its other answers for the same error, and says what changes next time.
  - 🔎 `find same error`: Searches the rest of the work for the same mistake pattern and fixes each instance.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/action-agency/error-correction` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/action-agency/error-correction` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
