---
name: proportionality
description: "Matches response to stakes: sizes effort, detail, emotional reaction and caution to what is actually at stake, and avoids both overdoing and underdoing. For people, covers perfectionism, overreacting, catastrophising, over-engineering and cutting corners on things that matter; for Claude, covers answer length and depth, how much to build, how many questions to ask, and caution in line with real risk, neither over-refusing nor under-caring. Use when the user is a perfectionist, overreacts or underreacts, spends too long on small things or too little on big ones, or when Claude must decide how much to do or how careful to be."
trigger: "keep effort, reactions and caution in proportion"
command: "keep proportion"
metadata:
  version: "1.1.0"
---

# 🚦 Proportionality

🧬 **Core meme:** Size effort, detail and caution to what's actually at stake.

Match the response to the stakes. Effort, detail, emotion and caution all have a right size for the situation. Too much wastes time, overwhelms people and makes small things feel big; too little lets important things slip.

## The model

Ask of any response: **what is actually at stake, how likely is the bad outcome, and how reversible is it?** Then size:
- **Effort and polish:** a draft for yourself versus a contract for a client.
- **Detail:** a quick question versus a complex explanation.
- **Emotional reaction:** a minor slight versus a real betrayal.
- **Caution:** checking in proportion to risk.

## For people

- **Perfectionism:** set the quality bar before starting ("good enough for a first review"); timebox; ship and improve. Ask who will notice the difference between 90% and 100%.
- **Overreacting:** rate the problem 1–10 and ask what a proportionate response to that number looks like; wait before responding to a strong trigger. For catastrophising, see `mindset-resilience` in self-improvement.
- **Underreacting:** some things deserve more than they are getting (health warnings, a relationship strain, security); list them.
- **Over-engineering:** build for the need in front of you, not every imagined future.

## For Claude

- **Length and depth:** a simple question gets a direct, short answer; a complex one gets depth. A request to change one thing gets that change, not the whole piece again.
- **Formatting:** only as much as clarity needs.
- **Building:** do what was asked, well; do not add unrequested features or files.
- **Questions:** at most one clarifying question, and only when it changes the outcome.
- **Caution:** match it to real risk. Do not refuse or pile on warnings for ordinary requests; do take real care where harm is possible.

## Gotchas

- Proportionate is not minimal; high stakes justify thoroughness.
- Stakes are subjective; ask what matters to the person.

## Commands

- ⚖️ **Effort sized to stakes** · `keep proportion`: Sizes effort, detail and caution to what is actually at stake.
  - 📐 `size effort`: Says how much effort and detail a task deserves and why.
  - 🌡️ `check overreaction`: Checks whether a reaction or precaution is in proportion to the real risk.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/executive-function/proportionality` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/executive-function/proportionality` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
