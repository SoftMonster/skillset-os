---
name: bias-detection
description: "Catches systematic thinking errors: confirmation bias, anchoring, availability, overconfidence, sunk cost, framing, motivated reasoning and more, with specific debiasing moves for each. For people, covers checking their own decisions and beliefs and spotting bias in arguments, media and data; for Claude, covers its own tendencies, including agreeing too readily, anchoring on the framing of a question, favouring the first hypothesis and giving one-sided accounts of contested topics. Use when the user asks whether they are biased, wants to check a decision or belief, or evaluate a claim or dataset for bias, or when Claude reviews its own answer for slant."
trigger: "check thinking for bias or cognitive errors"
metadata:
  version: "1.0.0"
---

# 🧠 Bias Detection

🧬 **Core meme:** Biases hide from their owner, so use procedures, not good intentions.

Catch the systematic errors that thinking makes when it runs on shortcuts. Biases are not stupidity; they are side effects of a brain built for speed. They are much easier to see in others than in oneself, so detection needs deliberate checks.

## Common biases and the move that counters each

| Bias | What happens | Counter-move |
|---|---|---|
| Confirmation | seeking and believing evidence that agrees | search for disconfirming evidence; ask what would change my mind |
| Anchoring | first number or framing sticks | generate your own estimate first; consider several anchors |
| Availability | vivid or recent examples feel common | check base rates and data |
| Overconfidence | too sure, ranges too narrow | give ranges; track predictions (see `uncertainty-awareness`) |
| Sunk cost | continuing because of past investment | ask: knowing what I know now, would I start this today? |
| Framing | same facts, different choice by wording | restate the choice in the opposite frame |
| Motivated reasoning | believing what we want | ask how I would judge this if the conclusion were unwelcome |
| Hindsight | "I knew it all along" | write predictions down beforehand |
| Halo and horns | one trait colours the whole judgement | judge criteria separately |
| In-group | favouring people like us | apply the same test to an outsider |
| Status quo | preferring no change | compare as if both options were new |

## For people

Pick the two or three biases most likely in the situation, rather than all of them, and apply their counter-moves. For group decisions: collect independent views before discussion, assign a devil's advocate, and use checklists.

When evaluating a claim, article or dataset: who produced it and why, how the sample was chosen, what is missing, and whether the framing steers the conclusion.

## For Claude

Check its own answers for its known slants:
- **Agreeableness:** siding with the person because they pushed, or because the question was framed to expect "yes". Re-evaluate on evidence.
- **Anchoring on the framing:** a leading question can carry a false premise; check it.
- **First-hypothesis lock-in:** in debugging or research, keep alternatives alive until evidence decides.
- **One-sidedness:** on contested topics, give a fair account of the main positions.
- **Training-era defaults:** assumptions about the world that may be outdated.

## Gotchas

- Knowing about biases does not remove them; procedures do.
- Calling someone "biased" ends conversations; point to the specific evidence or step instead.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/reasoning/bias-detection` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/reasoning/bias-detection` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
