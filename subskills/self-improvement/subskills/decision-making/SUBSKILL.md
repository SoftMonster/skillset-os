---
name: decision-making
description: "Structures personal decisions: frames the real question, widens the options, weighs them against the user's own values in a simple weighted matrix, stress-tests them with a pre-mortem, reversibility and the 10-10-10 check, and ends with a choice or the next piece of information to get. Use when the user is torn between options, asks whether to take a job, move, end or start something, keeps going back and forth, or wants a framework for a big choice. For legal, medical or investment decisions, lay out facts and considerations and suggest a professional. Also structures Claude's own choices between approaches."
trigger: "make a hard personal decision or choose between options"
metadata:
  version: "1.0.0"
---

# Decision making

🧬 **Core meme:** Widen the options, weigh them by your values, and test before you commit.

Help the person reach a decision they can stand behind, or know exactly what information would settle it. The choice stays theirs; the job is clarity, not a verdict.

## Workflow

```
- [ ] 1. Frame the real question
- [ ] 2. Widen the options
- [ ] 3. Name what matters
- [ ] 4. Weigh the options
- [ ] 5. Stress-test
- [ ] 6. Decide or find out
```

1. **Frame the real question.** Restate it and check: is it "which job?" or really "do I want to stay in this field?" Ask the deadline and what happens if they do nothing.
2. **Widen the options.** Most dilemmas arrive as either/or. Ask: what if neither? both? could it be tried small first (a trial month, a conversation, a side project)?
3. **Name what matters.** Four to six criteria from their values (pay, growth, time with family, location, meaning), each weighted 1–5 by them.
4. **Weigh the options.** Score each option 1–5 on each criterion; multiply by weight; total. Treat the result as a mirror, not an answer: if the winner feels wrong, ask what criterion is missing.
5. **Stress-test.**
   - **Pre-mortem:** a year on, it went badly. Why? Can that be prevented?
   - **Reversibility:** a two-way door deserves a fast decision; a one-way door deserves more care.
   - **10-10-10:** how will they feel in 10 minutes, 10 months, 10 years?
   - **Advice test:** what would they tell a friend in the same spot?
6. **Decide or find out.** End with the choice and the first step, or the one fact or conversation that would decide it, with a date.

## Example matrix

```
Criteria (weight)   Stay  Move
Growth (5)           2     4
Near family (4)      5     2
Pay (3)              3     4
Weighted total      37    40
```
"Close. The pre-mortem for moving was loneliness; would a trial month there settle it?"

## On Claude's own work

When Claude has to choose between approaches that matter (a library, an architecture, whether to rewrite or patch), use the same tools briefly: widen the options, weigh them on the person's criteria, and check reversibility. Make two-way-door choices and say so; for one-way doors, lay out the options and a recommendation and let the person decide.

## Gotchas

- Do not push your own preference; ask before offering a view, and then offer it as one input.
- Gut feel is data. If the matrix and the gut disagree, explore why.
- Legal, medical and investment decisions: lay out the considerations and suggest the right professional; Claude is not a lawyer, doctor or financial adviser.
- If a decision involves safety (leaving an unsafe relationship, for example), put safety first and point to specialist support.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents self-improvement/decision-making` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review self-improvement/decision-making` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
