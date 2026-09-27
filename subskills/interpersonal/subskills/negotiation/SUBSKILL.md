---
name: negotiation
description: "Prepares and runs negotiations: researches the range, defines the target, walk-away point and best alternative, maps both sides' interests, plans anchors, concessions and trades, and rehearses with role-play. Use when the user is negotiating a salary or job offer, a price, a rent, a contract, a household arrangement or any agreement, or wants to get better at negotiating. Also guides how Claude handles competing requests with the person."
trigger: "negotiate a salary, price, deal or agreement"
metadata:
  version: "1.1.0"
---

# Negotiation

🧬 **Core meme:** Know your walk-away, trade rather than concede, and get it in writing.

Help the person negotiate confidently and fairly, and walk in with a plan. Good output is a one-page negotiation plan and a rehearsal.

## Workflow

```
- [ ] 1. Research the range
- [ ] 2. Set target, walk-away and alternative
- [ ] 3. Map interests
- [ ] 4. Plan the moves
- [ ] 5. Rehearse
- [ ] 6. Close in writing
```

1. **Research the range.** Market data for salaries, prices or rents from current sources; do not quote figures from memory.
2. **Set three numbers:** an ambitious but defensible target, a walk-away point, and the best alternative if no deal (BATNA). A strong alternative is the source of confidence.
3. **Map interests.** Theirs and yours, beyond price: timing, risk, flexibility, recognition. Different priorities allow trades.
4. **Plan the moves.**
   - Anchor first with a researched, specific number when you know the market; let them go first when you do not.
   - Justify with reasons, not feelings.
   - Trade, do not concede: "If I can start in March, could we get to 58?"
   - Negotiate the package (salary, holiday, remote days, training, title, start date).
   - Use silence after an offer; ask "Is that the best you can do?"
5. **Rehearse.** Claude plays the other side, including a tough counterpart.
6. **Close in writing**, summarising what was agreed.

## Plan template

```
Target: …   Walk-away: …   Alternative if no deal: …
Their likely interests: …   Mine: …
Opening and justification: …
Tradeables: …
```

## On Claude's own work

When the person's requests pull in different directions (fast versus thorough, short versus complete), Claude names the trade-off, asks which matters more when it is unclear, and proposes a trade ("I'll do the core now and the edge cases after").

**Memetic check before it's sent:** offers, counters and written agreements travel beyond this chat, so check them with `memetic-ethics` in cognition/communication-regulation: accurate, fair to the people involved, and clear even when quoted alone.

## Gotchas

- Salary negotiation is expected in many workplaces; a polite counter rarely costs an offer. Norms vary by country and sector.
- Win-lose tactics damage relationships you must keep (employer, landlord, family).
- Do not help with deceptive tactics (fake competing offers); they are dishonest and risky.

## Commands

- 💼 **Know your walk-away, trade, write it down** · `negotiate salary`: Negotiates a salary, price, deal or agreement: research the range, set three numbers, map interests, plan moves, rehearse and close in writing.
  - 🔢 `set negotiation numbers`: Sets the target, opening and walk-away numbers from research.
  - ♟️ `plan negotiation moves`: Plans trades and concessions and fills the plan template.
  - 🎭 `rehearse negotiation`: Plays the other side so the person can practise the moves.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents interpersonal/negotiation` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review interpersonal/negotiation` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
