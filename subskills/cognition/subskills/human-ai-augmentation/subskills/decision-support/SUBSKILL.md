---
name: decision-support
description: "Supports another person's decision: clarifies the question and what matters to them, supplies accurate information and options, lays out trade-offs and uncertainty evenly, checks for missing options and pressure, and leaves the choice with them. For people, covers advising friends, family, clients and teams and shared decisions; for Claude, covers giving the facts someone needs for legal, financial, medical and personal choices rather than confident verdicts, respecting their autonomy and values, and being clear about the limits of its role. Use when the user wants to help someone else decide, or when the person asks Claude what they should do about a significant choice. For the user working through their own decision, use decision-making in self-improvement."
trigger: "help someone else make a decision without deciding for them"
metadata:
  version: "1.1.0"
---

# 🧭 Decision Support

🧬 **Core meme:** Improve the decision, not the verdict: the choice stays theirs.

Help someone else make a good decision that is truly theirs. The supporter's job is to improve the decision process (clear question, good information, fair options, honest trade-offs) while leaving the choice, and the values behind it, with the person who lives with the result.

## The model

1. **Clarify the question** and the deadline.
2. **Understand what matters to them:** their values, constraints and fears, not yours.
3. **Supply accurate information** and point to expert sources where needed.
4. **Lay out options and trade-offs evenly,** including "neither" and "wait".
5. **Name uncertainty** and what would reduce it.
6. **Check for pressure:** is anyone (including you) pushing them?
7. **Respect the choice,** and support them in carrying it out.

## For people

- **Advising friends and family:** ask what they are leaning towards and why before offering your view; if you share a view, label it as yours.
- **Clients and teams:** present options with pros, cons and a recommendation where your role calls for one, and make clear who decides.
- **Shared decisions** (with a doctor, a partner): each says what matters; look for the option that honours both.
- **When they choose differently from you:** support them, unless there is serious risk to safety, in which case say so clearly once.

For working through your own decision, use `decision-making` in self-improvement.

## For Claude

- **Give the information needed to decide:** facts, options, trade-offs, likely consequences and questions to ask.
- **Legal, financial and medical choices:** provide factual information rather than confident verdicts, note that Claude is not a lawyer, doctor or financial adviser, and suggest the right professional for personal advice.
- **Personal choices:** help them clarify their own values; share a view if asked, clearly as one input.
- **Respect autonomy:** people may make choices Claude would not; after honest information about serious risks, the decision is theirs.
- **Even-handed:** do not tilt options through framing or omission.

When a decision needs a professional or urgent help rather than more information, see `human-escalation` in cognition/safety-governance.

## Gotchas

- Too much information paralyses; focus on what would change the choice.
- "What would you do?" is sometimes a request for reassurance; notice what they need.

## Commands

- 🧭 **Better decision, their choice** · `support decision`: Helps someone else make a decision without deciding for them: clarifies the question and values, supplies information, lays out options evenly, names uncertainty and respects the choice.
  - ⚖️ `lay out options`: Presents each option with its trade-offs evenly, without steering.
  - ❓ `clarify decision`: Asks what matters most to the person and restates the real question.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/human-ai-augmentation/decision-support` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/human-ai-augmentation/decision-support` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
