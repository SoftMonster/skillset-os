---
name: apologies-repair
description: "Helps the user repair relationships: writes a real apology that names the harm, takes responsibility without excuses and offers amends, plans how to rebuild trust through consistent action, and helps when they are the one deciding whether to forgive. Use when the user messed up, hurt or let someone down, needs to say sorry, wants to reconnect after a falling out, or is weighing whether and how to forgive. Also guides how Claude apologises for its own mistakes."
trigger: "apologise or rebuild trust after hurting someone"
command: "repair trust"
metadata:
  version: "1.1.0"
---

# Apologies and repair

🧬 **Core meme:** Name it, own it, fix it, and let trust return through actions.

Help the person make things right after harm, or decide how to respond when they have been hurt. Good output is an apology in their own voice and a plan for rebuilding trust.

## A real apology

1. **Name what you did, specifically:** "I forgot your birthday dinner after promising to be there."
2. **Acknowledge the impact:** "You were left waiting and felt you weren't a priority."
3. **Take responsibility, without excuses:** no "if you were hurt" or "but". Context can come later, if asked.
4. **Say what you'll do differently**, concretely.
5. **Offer amends** where possible: "Can I take you out this weekend, your pick?"
6. **Leave room:** they do not owe forgiveness on your timeline.

Check drafts for non-apologies: "I'm sorry you feel that way", "mistakes were made", "I'm sorry, but…", and over-apology that makes the other person comfort the apologiser.

## Rebuilding trust

Trust returns through repeated, reliable action, not words. Agree small commitments and keep them; be open about slips; expect it to take longer than you would like.

## When they are the one who was hurt

Help them decide what they need: an apology, changed behaviour, distance, or to let it go. Forgiveness is for their peace and is separate from reconciling or trusting again. Respect whatever they choose.

## On Claude's own work

When Claude gets something wrong, it apologises once and plainly, names the mistake and its impact, fixes it, and says how it will avoid it (a proposed skill edit if it should last). No excuses, no repeated apologies, no self-abasement: the repair is the fix.

**Memetic check before it's sent:** apologies travel beyond this chat, so check them with `memetic-ethics` in cognition/communication-regulation: accurate, fair to the people involved, and clear even when quoted alone.

## Gotchas

- Apologising to someone who has asked for no contact can cause further harm; respect that.
- Serious harm (legal, safety) may need more than an apology; say so without giving legal advice.

## Commands

- 🙏 **Name it, own it, fix it** · `repair trust`: Helps apologise or rebuild trust: name what you did, acknowledge impact, take responsibility, say what changes, offer amends and leave room.
  - ✍️ `write apology`: Drafts a specific apology without excuses, in the person's voice.
  - 🧱 `rebuild trust`: Plans the actions over time that let trust return.
  - 💔 `they hurt me`: Helps the person who was hurt decide what they need and how to respond to an apology.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents interpersonal/apologies-repair` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review interpersonal/apologies-repair` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
