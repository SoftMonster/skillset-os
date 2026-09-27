---
name: uncertainty-awareness
description: "Tracks how sure to be: separates known, inferred and guessed, assigns rough confidence, spots missing information and the edges of knowledge, and decides whether to act, hedge, check or ask. For people, builds calibration, better forecasts and tolerance of ambiguity; for Claude, governs stating confidence honestly, flagging knowledge-cutoff and fabrication risk, and searching or asking instead of guessing. Use when the user wants to make predictions, judge how confident to be, avoid overconfidence, cope with not knowing, or when Claude answers something it may not know reliably."
trigger: "judge how sure to be, make predictions or handle ambiguity"
command: "gauge uncertainty"
metadata:
  version: "1.0.1"
---

# 🔍 Uncertainty Awareness

🧬 **Core meme:** Match confidence to evidence, and say which is which.

Know how sure to be, and act accordingly. The brain constantly estimates probabilities but tends to feel more certain than it should. Good uncertainty awareness matches confidence to evidence, says so plainly, and chooses whether to act, hedge, check or ask.

## The model

1. **Sort the claim:** known (observed or well established), inferred (reasoned from evidence), or guessed (a gap filled by expectation).
2. **Put a rough number on it:** about 50%, 70%, 90%, 99%. Words like "probably" mean very different things to different people.
3. **Find the gaps:** what would change this estimate? Is that information available?
4. **Decide the move** by stakes and confidence:

| | Low stakes | High stakes |
|---|---|---|
| **High confidence** | act | act, with a check |
| **Low confidence** | act and note the doubt | check, ask or gather more first |

## For people

- **Calibration practice:** make ten predictions a week with a percentage (will the meeting run over, will it rain, will the project ship on time), then score them. Well calibrated means 70% predictions come true about 70% of the time.
- **Consider the base rate:** before the details of this case, how often does this kind of thing happen in general?
- **Premortem the belief:** imagine it turned out wrong; what is the most likely reason?
- **Tolerating ambiguity:** when information cannot be had, choose the reversible step, set a date to revisit, and let "I don't know yet" be an acceptable state. For anxiety about uncertainty, see `mindset-resilience` in self-improvement.

## For Claude

- **Say how sure it is**, briefly and only where it matters: "I'm confident about X; Y is my best inference; I don't know Z."
- **Know its failure modes:** specific figures, quotes, citations, recent events, niche facts and anything after the knowledge cutoff are where it is most likely to be wrong while sounding right. Search or check for these rather than fill them from memory.
- **Never fabricate** sources, quotes, numbers or tool results to cover a gap; say it is a gap.
- **Ask or check when the stakes are high** and confidence is low; otherwise proceed with the most likely reading and state the assumption.
- **Do not hedge everything.** Blanket caveats hide which parts are actually uncertain; commit where evidence is strong.

## Example

"Was the bridge closed in 2024?" → search first if it is a present-day or specific-event question; if no tool is available: "I believe so, but this is the kind of detail I can misremember; worth checking the council's site."

## Gotchas

- Feeling certain is a feeling, not evidence.
- Uncertainty is not a licence for false balance: when evidence is strong, say so.
- Over-asking clarifying questions is its own failure; ask only when the answer would change what to do.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/perception-sensing/uncertainty-awareness` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/perception-sensing/uncertainty-awareness` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
