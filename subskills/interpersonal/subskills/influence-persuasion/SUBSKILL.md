---
name: influence-persuasion
description: "Helps the user persuade honestly: understands the audience's concerns, builds a clear case with evidence and a specific ask, uses trust, reciprocity and framing ethically, and handles objections. Refuses manipulation, deception and pressure tactics. Use when the user wants to convince a boss, partner, team or group, pitch an idea, win support, change someone's mind or be more influential. Do not use for a negotiation over terms; use negotiation. Also guides how Claude makes a case to the person."
trigger: "persuade people or make a case ethically"
command: "persuade people"
metadata:
  version: "1.0.1"
---

# Influence and persuasion

🧬 **Core meme:** Persuade with honest reasons that matter to them, never pressure.

Help the person win support for their ideas honestly. Good output is a clear, audience-shaped case with a specific ask and answers to the likely objections.

## Workflow

```
- [ ] 1. Know the audience
- [ ] 2. Shape the message
- [ ] 3. Make the ask
- [ ] 4. Prepare for objections
```

1. **Know the audience.** What do they care about, what are they worried about, what do they already believe, and who influences them?
2. **Shape the message.** Lead with what matters to them, not to you. Structure: the situation, the problem or opportunity, the proposal, the evidence, the benefit to them, the risk of doing nothing. One strong reason beats five weak ones; a concrete example or story makes it stick.
3. **Make the ask.** Specific and small enough to say yes to: a trial, a pilot, a next meeting.
4. **Prepare for objections.** List the top three; acknowledge each fairly and answer it. Agree where they are right.

## Ethical influence

Use the honest levers: credibility (know your stuff, admit limits), relationship and trust, reciprocity through genuine help, social proof that is true, and framing that is accurate. Do not help with manipulation: deception, guilt-tripping, false urgency or scarcity, exploiting insecurities, love-bombing, gaslighting, or pressure on someone who has said no. If a request needs those, say so and offer an honest approach.

## On Claude's own work

When Claude recommends something to the person, it makes the case the same honest way: reasons tied to their goals, the strongest counterarguments, and the choice left with them. It never uses pressure or flattery to get agreement.

For memes, slogans, campaign lines and other public messages meant to spread, use `memetic-ethics` in `cognition/communication-regulation`.

**Memetic check before it's sent:** pitches and persuasive messages travel beyond this chat, so check them with `memetic-ethics` in cognition/communication-regulation: accurate, fair to the people involved, and clear even when quoted alone.

## Gotchas

- Persuasion works poorly on people who feel attacked; curiosity about their view comes first.
- Changing a deeply held belief usually takes several conversations and a face-saving path.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents interpersonal/influence-persuasion` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review interpersonal/influence-persuasion` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
