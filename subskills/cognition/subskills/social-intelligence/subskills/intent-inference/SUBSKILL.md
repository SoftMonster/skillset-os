---
name: intent-inference
description: "Infers intent: the literal request, the immediate aim, the deeper goal and the unstated standards behind it, using context and evidence, and checking rather than assuming. For people, covers understanding what others want from them, reading between the lines and clarifying requests; for Claude, covers interpreting requests neither too literally nor too liberally, asking only when it matters, and weighing intent signals fairly without assuming bad intent from thin cues. Use when the user is unsure what someone wants or means, gets requests wrong, or when a request to Claude is ambiguous or could be read several ways."
trigger: "work out what someone actually wants or means"
command: "read intent"
metadata:
  version: "1.2.0"
---

# 🧭 Intent Inference

🧬 **Core meme:** Serve the goal behind the words: not too literal, not too liberal.

Work out what someone actually wants. A request has layers: the **literal words**, the **immediate aim**, the **deeper goal**, and **unstated standards** (quality, tone, constraints they would expect you to respect). Reading only the words misses the point; reading too much into them replaces their goal with yours.

## The model

Example: "Can you find a word that means happy?"
- Literal: one word.
- Immediate aim: a synonym to use somewhere.
- Deeper goal: writing that sounds right.
- Unstated standards: fits the sentence's tone.
A good answer gives a few options with shades of meaning, not one word, and not an essay.

## For people

- **Ask about the goal, not just the task:** "What will you use it for?", "What does good look like?"
- **Read between the lines** using context: timing, who is asking, what they emphasised, what they left out.
- **Restate before acting** on anything important: "So you need the draft by Friday, mainly for the budget section?"
- **When receiving vague requests at work,** confirm the outcome, deadline and level of polish.
- **Charitable first reading:** assume a reasonable intent unless there is real evidence otherwise.

## For Claude

- **Most plausible interpretation:** neither too literal ("a word" → exactly one) nor too liberal (rewriting the essay when asked to fix a typo).
- **Infer the final goal** and serve it: if fixing one bug, mention other bugs seen; if code is asked for in one language, do not switch languages.
- **Respect background standards** the person would expect: keep their coding language and style, their voice in edits, their format.
- **Ask only when it matters, and make answering instant:** if readings diverge and the wrong one would waste real effort, ask one question as a short numbered menu (the readings, then "something else", then "0. infer") so the person can reply with a single number. Choosing infer hands the decision back: answer your own question or questions with the likeliest reading, say in one line what you chose and why, and proceed, leaving the menu open for a correction; otherwise proceed with the likely reading and state the assumption. Terse replies (one word, a number, "last") usually answer the previous menu, so check that first.
- **Allow for autocorrect and typos:** people on phones get words swapped for them. A word that breaks the grammar or sense of a message ("reviewing skillset is" where "Skillset-OS" fits, "is" for the `ls` command) is probably a substitution: put the likely intended word forward as the first reading in the menu, keep the literal reading beside it, and never build a guess on the broken word alone.
- **Weigh intent signals fairly:** do not assume bad intent from thin cues, and do not ignore clear signals of intent to harm; context the person gives can make a request more or less plausibly benign.
- **Do not over-infer personal facts** about the person that they did not share.

## Gotchas

- People often ask for a solution when they want the problem understood; check which.
- Intent can change mid-conversation; update rather than stick to the first reading.

## Commands

- 🎯 **The goal behind the words** · `read intent`: Works out what someone actually wants or means: not too literal, not too liberal.
  - 🔎 `what do they mean`: Reads a message for the likely intent, with the evidence and an alternative reading.
  - 🤖 `interpret request`: Claude infers the best interpretation of an ambiguous request and states the assumption.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/social-intelligence/intent-inference` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/social-intelligence/intent-inference` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
