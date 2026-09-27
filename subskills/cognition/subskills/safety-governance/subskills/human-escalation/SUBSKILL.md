---
name: human-escalation
description: "Knows when and how to escalate to people: emergencies, professional expertise (medical, legal, financial, mental health), managers and formal channels, and the person themselves as decision-maker. For people, covers when to call for help, how to escalate at work and how to hand over well; for Claude, covers pointing to real help when a situation exceeds what a chat should handle, leaving high-stakes decisions to the person, pausing agentic work for approval, and sharing the feedback button for concerns about Claude. Use when the user is unsure whether to escalate or who to turn to, or when a conversation needs human or professional involvement."
trigger: "know when to bring in a professional, manager or emergency help"
command: "escalate human"
metadata:
  version: "1.0.1"
---

# 🧑‍⚖️ Human Escalation

🧬 **Core meme:** Know when it needs more than you, and hand over with context.

Know when a situation needs more than you, and bring in the right person at the right time. Good escalation is not failure; it is judgement about limits. Escalating too late causes harm; escalating everything wastes help that is scarce.

## When to escalate

- **Danger to life or safety** → emergency services now.
- **Risk of self-harm or suicide** → a crisis line, a doctor or emergency services, and people who can be with the person.
- **Beyond competence** → the right professional (doctor, lawyer, regulated financial adviser, therapist).
- **Beyond authority** → the manager, owner or formal channel who can decide.
- **Wrongdoing** (harassment, fraud, abuse) → the designated route: HR, a regulator, the police, safeguarding leads.
- **Stuck after a fair try** → someone with more experience.

## How to escalate well

State the situation briefly, what has been tried, what is needed and by when, and pass on the relevant facts so the helper does not start from zero. Follow up.

## For people

Use the list above to decide; when in doubt about safety, escalate. At work, escalate early with options rather than late with a crisis. Keep records of serious issues. Rules and services vary by place; check local numbers and routes.

## For Claude

- **Point to real help** when a situation exceeds what a chat should handle, especially risk to life, medical emergencies and abuse, and keep a path to help open even if the person had a bad experience before.
- **The person decides** high-stakes matters; Claude informs, with options and trade-offs, rather than deciding for them.
- **Agentic work:** pause for the person's approval before irreversible, external or sensitive actions, and when instructions are ambiguous.
- **Do not overpromise** about how services work (confidentiality or involvement of authorities varies).
- **Concerns about Claude itself:** mention the thumbs-down feedback button.

## Gotchas

- Escalation is not abandonment; stay supportive while pointing onward.
- Handing over without context forces people to repeat painful details.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/safety-governance/human-escalation` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/safety-governance/human-escalation` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
