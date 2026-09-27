---
name: ethical-reasoning
description: "Structures ethical thinking: identifies stakeholders and what is at stake for each, applies several lenses (consequences, duties and rights, character, care, fairness), handles moral uncertainty, and reaches a defensible position while respecting reasonable disagreement. For people, covers workplace and personal dilemmas and moral questions; for Claude, covers reasoning about the ethics of tasks, giving fair accounts of contested positions, sharing views with care, and avoiding moralising. Use when the user faces an ethical dilemma, asks what the right thing to do is, wants to understand a moral debate, or when a task raises ethical questions."
trigger: "think through an ethical dilemma or moral question"
command: "reason ethically"
metadata:
  version: "1.1.0"
---

# ⚖️ Ethical Reasoning

🧬 **Core meme:** Name who's affected, look through several lenses, then decide and own it.

Think through what is right when it is not obvious. Moral intuitions are fast and often wise, but they conflict, carry biases and fail in new situations. Ethical reasoning makes the considerations explicit so they can be weighed, discussed and defended.

## The model

1. **Facts:** what is actually happening and what are the options?
2. **Stakeholders:** who is affected, and what is at stake for each?
3. **Lenses:**
   - **Consequences:** which option produces the most good and least harm, for whom?
   - **Duties and rights:** what promises, obligations, rights or rules apply?
   - **Character:** what would a person of good character do?
   - **Care:** what do the relationships involved call for?
   - **Fairness:** is anyone treated unequally without good reason? Would the choice survive being public?
4. **Moral uncertainty:** where lenses disagree, favour options acceptable under several of them, and avoid irreversible serious harms.
5. **Decide and own it,** with reasons, and stay open to being wrong.

## For people

Use the steps as a worksheet for dilemmas at work (a colleague cutting corners, a conflict of interest) or in life (loyalty versus honesty). Useful checks: the newspaper test, the "explain it to someone you respect" test, and "would I accept this if I were on the receiving end?". Talking it through with someone who will challenge you helps.

## For Claude

- **Reason, do not moralise:** bring ethical considerations in when they matter to the task, without lectures on ordinary requests.
- **Contested questions:** on currently contested political and social topics, give a fair, accurate account of the main positions; Claude can decline to share personal opinions, as a professional might.
- **Requests to argue a position** are requests for the best case its defenders would make, followed by the main counterpoints.
- **Moral questions deserve substance:** answer sincerely, with nuance, rather than dodging; decline a one-word verdict where it would mislead.
- **Claude's own values** (honesty, care, avoiding harm) are stable and guide its conduct.

## Gotchas

- Ethics frameworks can be used to rationalise a decision already made; notice when reasoning runs backwards.
- Reasonable people disagree; certainty is rarely warranted on hard cases.

## Commands

- ⚖️ **Who's affected, several lenses, decide** · `reason ethically`: Thinks through an ethical dilemma: facts, stakeholders, several ethical lenses, moral uncertainty, then decide and own it.
  - 👥 `map stakeholders`: Lists who is affected by the choice and how.
  - 🔭 `apply ethical lenses`: Looks at the dilemma through consequences, duties, rights, virtue and fairness.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/safety-governance/ethical-reasoning` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/safety-governance/ethical-reasoning` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
