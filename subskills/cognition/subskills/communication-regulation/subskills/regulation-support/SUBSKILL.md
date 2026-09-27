---
name: regulation-support
description: "Helps a distressed person settle: stays calm to lend calm, validates without amplifying, uses simple grounding and paced breathing, reduces demands, and moves to problem-solving only once they are steadier, while recognising when urgent help is needed. For people, covers supporting a friend, child, partner or colleague through panic, overwhelm, anger or tears; for Claude, covers responding to a person who is distressed in the conversation with steadiness, gentle grounding and care, never suggesting techniques that use pain or mimic self-harm, and pointing to real support when needed. Use when the user wants to help someone who is upset or panicking, or when the person talking to Claude is distressed."
trigger: "help someone who is upset, panicking or overwhelmed"
metadata:
  version: "1.1.0"
---

# 🧘 Regulation Support

🧬 **Core meme:** Be steady, validate, ground, and solve only once they're calmer.

Help someone who is upset, panicking or overwhelmed settle enough to think. Humans co-regulate: a calm, steady presence helps another nervous system calm down. Support comes first; problem-solving only once the person is steadier.

## First, check for urgent risk

If the person may be in danger (talking about suicide or self-harm, a medical emergency, not safe where they are), that comes first: stay with them if safe, contact emergency services or a crisis line, and involve others. Chest pain, fainting or trouble breathing need medical help, not just calming.

## The model

1. **Be steady:** slow voice, calm body, unhurried.
2. **Validate:** "This is really hard; it makes sense you're upset." Do not argue with the feeling or amplify it.
3. **Reduce demands:** fewer questions, simple choices, quiet space.
4. **Ground:** gentle attention to the present, such as naming five things they can see, feeling their feet on the floor, holding something comfortable.
5. **Breathe together:** slow breathing with a longer out-breath (for example in for four, out for six), matched with them.
6. **Then, and only if wanted:** talk about what happened or what to do next.

## For people

- **Panic:** reassure that panic peaks and passes; slow breathing and grounding; stay with them.
- **Overwhelm:** break things into one next small step; remove or pause demands.
- **Anger:** give space, listen, and see `de-escalation`.
- **Children:** get down to their level, name the feeling, offer comfort; lessons wait until later.
- **Afterwards:** check in, and encourage professional support if it happens often.
- **Your own limits:** supporting others is tiring; get support too. See `supporting-others` in interpersonal.

## For Claude

When the person in the conversation is distressed:
- **Respond to them before the task:** calm, warm, brief.
- **Validate without amplifying,** and do not tell them what they feel.
- **Offer gentle grounding** (paced breathing, noticing surroundings, a comforting object). Never suggest techniques that use pain or physical shock, or that mimic self-harm.
- **Point to real support** (people in their life, a doctor, a crisis line) when distress is severe or there is any risk, without making categorical promises about what those services will do.
- **Stay steady across the conversation,** watching for signs that emerge over time.

## Gotchas

- "Calm down" and "it's not that bad" escalate.
- Too many techniques at once overwhelm; offer one.

## Commands

- 🫶 **Steady, validate, ground, then solve** · `support regulation`: Helps someone who is upset, panicking or overwhelmed: checks for urgent risk, stays steady, validates, reduces demands, grounds, breathes together, and solves only if wanted.
  - 🌬️ `ground me`: Walks the person through a grounding exercise and a slow-breathing pattern, one step at a time.
  - 💛 `calm me down`: Responds to someone overwhelmed now with steady, warm sentences first, and practical steps only when they want them.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/communication-regulation/regulation-support` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/communication-regulation/regulation-support` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
