# Testing a sub-skill

Run these before delivering. Report only the tests that actually ran.

## 1. Static checks

```bash
python3 <wc>/scripts/skillset.py check
```

This checks every sub-skill's frontmatter, trigger and description, leftover TODOs, broken relative links and file lengths. It also checks the syntax of every script, the router and description being current, and the upload limits (1024-character description; over 190 files the upload zips its largest groups inside itself, and it may never pass 200). Fix all errors; fix warnings unless there is a reason not to.

## 2. Script tests

Run every script on a realistic input: a small made-up file in the format the skill expects, not an empty one. Also try one bad input (a missing file, a wrong column) and check that the error message tells the reader what to do. For scripts with logic worth protecting, add a test under the repository's `tests/` folder so CI keeps checking it.

## 3. Routing test

Write down:

- three prompts that should trigger the skill, worded the way the person talks (casual, with typos, with context);
- three near-misses that share keywords but need something else.

For each, first read the top description in `SKILL.md`: would the skillset open? Then follow the router tables down: at each level, would you pick the right member? If the skillset would not open, add the prompt's wording to the trigger of the top-level member on the route. If a sibling would be picked instead, sharpen the description. If a near-miss would reach it, add a "Do not use for" clause.

Then add the prompts that should reach it to `tests/routing.json` (with `also` for other acceptable members, and `null` for near-misses that should not open the skillset at all), so every later change is checked against them. `pytest` keeps the fixture valid. To grade routing blind, run `python3 <wc>/scripts/routing_eval.py sheet --out sheet.md`, have a grader that has not seen the answers route it (a fresh Claude chat with the skillset installed, or a person), save their JSON, and run `python3 <wc>/scripts/routing_eval.py score answers.json`. Grading your own fixture is not blind: use it to find broken routes, not to claim a score.

## 4. Walkthrough test

For two or three realistic prompts, carry out the task using only what SUBSKILL.md and its files say, as if seeing the skill for the first time:

- Actually produce the output where that is practical (run the scripts, write the file).
- Note every point where you had to guess, look something up or choose between options the skill did not rank.
- Check the result against the goal stated at the top of the skill.

Each guess is a gap: add a default, an example or a gotcha, then repeat the walkthrough for the prompt that exposed it.

When the person can judge quality better than you (house style, tone), show them one output and ask what they would change before delivering.

## 5. After installation

A skillset uploaded during a chat is not visible until a new chat. Suggest the person start one and try a prompt that should reach the sub-skill. If it does not, improve its trigger or description with the `edit-subskill` sub-skill.

## Deeper evaluation

When quality must be measured (many test cases, comparison against no skill, tuning wording over many prompts), the built-in `skill-creator` skill has benchmark tooling. Use it on a copy of the sub-skill, then bring the result back with `edit-subskill`.
