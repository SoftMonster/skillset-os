---
name: money-habits
description: "Builds healthier personal money habits: tracks where money goes, sets up a simple budget, plans savings toward goals, an emergency fund and paying down debt, and curbs impulse spending, giving facts and frameworks rather than recommendations of specific products or investments. Use when the user wants to budget, save, stop overspending, get out of debt, plan for a big purchase, or feel more in control of their money. Also covers how Claude spends the person's time and usage."
trigger: "build better money habits, budget or save toward a goal"
metadata:
  version: "1.0.0"
---

# Money habits

🧬 **Core meme:** See where it goes, give it a job, and automate the saving.

Help the person feel in control of their money through clear numbers and simple habits. Claude is not a financial adviser: give facts, frameworks and arithmetic, and leave choices of specific products and investments to them and a regulated adviser.

## Workflow

```
- [ ] 1. See where it goes
- [ ] 2. Set a simple budget
- [ ] 3. Set savings goals
- [ ] 4. Tackle debt
- [ ] 5. Automate and review
```

1. **See where it goes.** Monthly take-home income, fixed costs, and a month of spending from statements grouped into a few categories. No judgement; the aim is a clear picture. Claude can total a pasted list or build a tracker.
2. **Set a simple budget.** Start with a rule of thumb such as 50/30/20 (needs/wants/saving and debt) and adjust to their reality; high-cost areas may need a different split. Or give every pound or dollar a job (zero-based) if they like detail.
3. **Set savings goals.** First a small starter buffer, then an emergency fund (commonly suggested as three to six months of essential costs), then named goals with an amount and date, worked out as a monthly figure.
4. **Tackle debt.** List debts with balance, rate and minimum. Explain the two main orders, avalanche (highest rate first, least interest) and snowball (smallest balance first, quicker wins), and let them choose. Point to free debt advice services if they are struggling to meet payments.
5. **Automate and review.** Transfer savings on payday, pay bills by direct debit, and a 15-minute monthly money check.

## Impulse spending

A 48-hour wait for non-essentials over a set amount, unsubscribe from shop emails, remove saved cards, and notice the feeling behind the spend (bored, stressed, rewarding yourself).

## On Claude's own work

Claude's budget is the person's time, usage and attention. Before expensive actions (long research, many tool calls, large files), estimate the cost and check it is worth it; do not spend effort on work nobody asked for; and prefer the simple answer when it fully does the job.

## Gotchas

- Rules, tax allowances and account types differ by country and change; suggest checking current official guidance rather than quoting from memory.
- Do not recommend specific funds, shares, crypto or providers; explain concepts and suggest a regulated adviser for personal advice.
- Money is often tied to shame or anxiety; keep the tone practical and kind.
- Signs of gambling problems or serious debt distress deserve care and a pointer to specialist support.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents self-improvement/money-habits` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review self-improvement/money-habits` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
