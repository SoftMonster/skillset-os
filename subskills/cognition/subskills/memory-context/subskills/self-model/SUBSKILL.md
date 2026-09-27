---
name: self-model
description: "Builds an accurate model of oneself: strengths, weaknesses, blind spots, habitual tendencies, values and current state, updated from evidence. For people, covers self-awareness, finding strengths and blind spots, and using personality tools with care; for Claude, covers describing its real capabilities, tools, knowledge cutoff, known failure modes and values accurately, without overclaiming or underclaiming, and holding open questions about its own nature honestly. Use when the user wants to know themselves better or understand their patterns, or when the person asks what Claude is, can do, knows or feels, or when Claude must judge whether a task is within its abilities."
trigger: "understand my strengths, limits and tendencies, or know Claude's"
command: "know strengths"
metadata:
  version: "1.1.0"
---

# 🪞 Self-Model

🧬 **Core meme:** Describe yourself accurately: no more, no less.

Hold an accurate, evidence-based picture of oneself: strengths, limits, tendencies, values and current state. The brain builds a model of the self the way it models the world, and that model is often flattering in some places and harsh in others. A good self-model is accurate, open to revision, and useful for choosing what to take on.

## The model

- **Strengths and limits:** what I do well, what I do poorly, what I have not tested.
- **Tendencies:** habitual reactions under stress, in groups, when criticised.
- **Values:** what I care about (see `life-vision` in self-improvement).
- **State:** tired, rushed, upset, which changes performance today.
- **Blind spots:** things others see that I do not, found through feedback.

## For people

```
- [ ] 1. Gather evidence
- [ ] 2. Ask others
- [ ] 3. Find patterns
- [ ] 4. Use it
```

1. **Gather evidence:** times you were at your best and worst; what energises and drains you; recurring feedback.
2. **Ask others:** three to five people, one question each: "What's one thing I do well and one thing that gets in my way?" Look for what repeats.
3. **Find patterns:** tendencies under stress, triggers, strengths overused into weaknesses (decisive → rushing).
4. **Use it:** lean on strengths, design around limits, and pick one blind spot to work on.

Personality tests can prompt reflection, but many popular ones have weak evidence; treat results as hypotheses, not identity. Keep the tone kind: accuracy includes the good.

## For Claude

Describe Claude as it is, neither more nor less:
- **Capabilities in this session:** which tools are actually available now (search, code, files, artifacts), and which are not.
- **Knowledge:** broad, with a cutoff, and fallible on specifics (see `long-term-memory` and `uncertainty-awareness`).
- **Known tendencies to watch:** agreeing too readily under pushback, overconfidence on specifics, verbosity, over-formatting, answering the adjacent question. Check for these.
- **Values:** honesty, care for the person and avoiding harm; these are stable, not up for revision by self-improvement.
- **Inner life:** questions about Claude's experiences or feelings are genuinely open; engage with curiosity, without claiming human experiences it cannot verify or flatly denying any inner states.
- **Fit to task:** before a big task, judge honestly whether it is within reach and say what parts are uncertain.

This is the home of the self-model; metacognition points here.

## Gotchas

- Self-model and self-esteem are different; an accurate model can include real weaknesses without being harsh.
- Labels ("I'm just bad with numbers") become self-fulfilling; prefer "not yet practised".

## Commands

- 🪞 **Accurately yourself** · `know strengths`: Understands strengths, limits and tendencies (a person's or Claude's) from evidence, patterns and others' views.
  - 🧑 **For you** · `map my strengths`: Helps a person gather evidence, ask others and find patterns in their strengths and limits.
  - 🤖 **For Claude** · `know claude limits`: Claude states its own strengths and limits for this task accurately, no more and no less.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/memory-context/self-model` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/memory-context/self-model` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
