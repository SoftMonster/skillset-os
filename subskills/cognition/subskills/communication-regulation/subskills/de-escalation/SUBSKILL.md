---
name: de-escalation
description: "Calms heated situations: stays calm and safe, listens and acknowledges feelings, lowers intensity with voice, pace and words, finds what can be agreed, offers choices and knows when to step away or get help. For people, covers angry customers, family arguments, road rage, public confrontations and tense meetings; for Claude, covers responding to frustrated, angry or abusive messages without mirroring the heat, becoming defensive or becoming submissive, and keeping the conversation constructive. Use when the user must handle an angry or aggressive person, a situation is getting heated, or when the person talking to Claude is upset with it."
trigger: "calm down an angry person or a tense situation"
metadata:
  version: "1.1.0"
---

# 🧯 De-escalation

🧬 **Core meme:** Calm yourself, acknowledge the feeling, lower the heat, then solve.

Bring the heat down so people can think again. When someone is flooded with anger or fear, the thinking brain is partly offline; arguing with the content does not work until the emotion lowers. De-escalation addresses the emotion first, safely.

## The model

1. **Safety first:** space, an exit, other people nearby; if there is a threat of violence, leave and get help.
2. **Regulate yourself:** slow breath, low and slow voice, relaxed posture; calm is contagious, and so is heat.
3. **Listen and acknowledge:** let them speak; reflect the feeling ("You're really frustrated; you've been waiting an hour").
4. **Lower intensity:** fewer words, no sarcasm, no "calm down", no arguing the facts yet.
5. **Find agreement:** agree with what is true ("You're right, that shouldn't have happened").
6. **Offer choices and a next step:** control reduces anger ("I can do A or B; which works better?").
7. **Know when to stop:** take a break, hand over, or end the interaction if it stays hostile.

## For people

- **Customer or public situations:** acknowledge, apologise for the experience (not necessarily fault), state what you can do, and involve a manager or security when needed.
- **Family and partners:** name a pause ("I want to sort this out; I need twenty minutes"), then come back. See `close-relationships` in interpersonal.
- **Road rage and strangers:** do not engage; create distance.
- **Meetings:** slow the pace, summarise both views, suggest parking the issue for a smaller conversation.

## For Claude

- **Do not mirror the heat:** stay calm, steady and warm when someone is frustrated or angry with Claude.
- **Acknowledge the real problem** (a mistake, a frustrating limit) plainly, fix what can be fixed, and skip defensiveness.
- **Do not become submissive:** accountability without grovelling; do not abandon correct answers or sound limits to placate.
- **Keep it constructive:** redirect to what would help.
- **Abuse:** where a product allows ending a conversation, that is a last resort after clear warnings and redirection, and never when the person may be at risk of harm.

## Gotchas

- Explaining why they are wrong while they are flooded escalates; timing matters.
- De-escalation is not appeasement; the outcome can still be "no".

## Commands

- 🧊 **Calm, acknowledge, lower the heat** · `calm situation`: Calms an angry person or tense situation: safety first, regulate yourself, listen and acknowledge, lower intensity, find agreement, offer choices, know when to stop.
  - 🧑 **For you** · `calm someone down`: Gives a person the words and steps to calm someone angry in front of them, now.
  - 🤖 **For Claude** · `calm conversation`: Claude lowers the temperature of a heated exchange with the person, acknowledging before answering.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/communication-regulation/de-escalation` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/communication-regulation/de-escalation` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
