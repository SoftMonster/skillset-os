---
name: feedback-processing
description: "Turns signals into updated behaviour: notices feedback (explicit comments, reactions, outcomes, error messages), judges its reliability, separates signal from noise, updates in proportion to the evidence, and closes the loop. For people, covers learning from results and criticism without over- or under-reacting; for Claude, covers reading tool output, test results and the person's reactions and adjusting mid-task. Use when the user repeats mistakes, overreacts to or ignores feedback, wants faster learning loops, or when Claude gets a correction, a failing test or an unexpected result. Do not use for the conversation of giving or receiving feedback; use feedback in interpersonal."
trigger: "learn from results, mistakes and reactions faster"
command: "process feedback"
metadata:
  version: "1.0.1"
---

# 👀 Feedback Processing

🧬 **Core meme:** Notice the signal, judge its weight, and update in proportion.

Turn the signals that come back from the world into better behaviour. The brain learns from prediction errors: the gap between what was expected and what happened. Good feedback processing notices those gaps, judges how much to trust them, updates in proportion, and checks the update worked.

## The loop

```
Act → Observe result → Compare with expectation → Judge the signal → Update → Act again
```

1. **Notice it.** Feedback is not only comments: results, silence, a frown, a bounced email, a failed test, a metric that did not move.
2. **Judge the signal.** How reliable is the source? One data point or a pattern? Is it about what I did, or about noise and chance?
3. **Update in proportion.** Small, noisy signals deserve small adjustments; strong, repeated signals deserve real change. Over-reacting to one bad result is as costly as ignoring a pattern.
4. **Close the loop.** Make one specific change and check whether the next result improves.

## For people

- **Shorten the loop.** Seek faster, more frequent signals: a draft shown early, a practice run, a weekly metric, a trusted person to ask.
- **Pre-register expectations.** Write down what they expect before acting; comparing later exposes real surprises instead of hindsight ("I knew it").
- **Separate outcome from decision.** A good decision can have a bad outcome from luck; judge the process as well as the result.
- **Feedback log:** date, signal, source, what it suggests, change made, whether it helped. Patterns emerge after a few weeks and pair well with `reflect-and-review` in self-improvement.
- **Emotional sting:** criticism can be both useful and painful; take the sting seriously and still extract the signal. For the conversation itself, use `feedback` in interpersonal.

## For Claude

- **Read every tool result.** Check exit codes, errors, empty output, truncation and warnings, not just the happy path, before claiming success.
- **Treat surprises as information.** If a test fails, a search returns nothing or a file looks different from expected, stop and update the plan rather than push on.
- **Read the person's reactions.** A terse reply, a repeated request or "that's not what I meant" is a signal; adjust approach, not just wording.
- **Update in proportion.** One correction on a detail is a fix, not a reason to abandon a sound approach; the same correction twice suggests a pattern worth a proposed skill edit (see `habit-building` in self-improvement).
- **Close the loop** by saying what changed.

## Gotchas

- Survivorship and silence: missing feedback (people who left, results never measured) can matter most.
- Metrics can be gamed or be the wrong measure; check they track the real goal.
- Do not wait for perfect feedback; act on the best available signal and keep watching.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/perception-sensing/feedback-processing` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/perception-sensing/feedback-processing` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
