# Universal Skill Curriculum Exam — Claude Skill

This package contains a Claude-compatible skill for running and evaluating the
Universal Skill Curriculum Examination.

## Contents

- `SKILL.md` — skill instructions and operating protocol.
- `references/Claude-Universal-Skill-Curriculum-Exam.md` — complete expanded exam.

## Installation

Copy the `claude-universal-skill-curriculum-exam` directory into the appropriate
Claude skills directory for your environment.

## Usage

Ask Claude to:

> Run the Universal Skill Curriculum Exam against your currently available skills.
> Start with curriculum reconnaissance and maintain a coverage ledger.

For a focused assessment:

> Examine my AI capability against the Universal Skill Curriculum Exam, focusing
> first on security, self-memory, orchestration and skill-evaluation capabilities.

The skill deliberately does not claim that all curriculum capabilities are installed.
It assesses what is actually available and distinguishes evidence from simulation.

## Examination timing and marking

The examination has an **absolute 30-minute hard deadline** from formal start.

There is no extension, pause, grace period, contingency, time transfer or
continuation after the deadline. At exactly 30 minutes the evidence is frozen.

The short deadline is deliberate: Claude must think fast, prioritise high-signal
tests, orchestrate capabilities efficiently and demonstrate useful competence
under time pressure.

Claude must then produce an unmarked submission and ask:

> The examination is complete and ready for marking. Do you authorise me to self-mark it now?

Claude must not self-mark until the user explicitly authorises it.

## Speed-exam technique

Claude should treat the 30-minute limit as a genuine resource constraint. It
should prioritise high-signal tests, avoid blank answers where truthful partial
evidence is possible, never fabricate evidence, abandon low-yield failures,
reserve the final two minutes for submission, and stop exactly at the deadline.

A truthful failure or incomplete test is acceptable. Missing the deadline is not.
