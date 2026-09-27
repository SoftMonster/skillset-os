---
name: difficult-conversations
description: "Prepares the user for a conversation they dread: clarifies the goal, separates facts from story, drafts an opener, anticipates the other person's view and reactions, and rehearses through role-play with realistic pushback. Use when the user needs to raise a problem, confront someone, deliver bad news, end something, ask for something hard, or talk about a sensitive topic with a partner, family member, friend, colleague or manager. Do not use for an ongoing dispute between parties; use conflict-resolution. Also guides how Claude raises hard things with the person."
trigger: "prepare for or handle a difficult conversation"
command: "prepare conversation"
metadata:
  version: "1.1.0"
---

# Difficult conversations

🧬 **Core meme:** Know your goal, lead with facts, and listen to their side.

Get the person ready for a conversation they dread, so they go in clear, calm and prepared for the other side. Good output is a short prep sheet and, if they want, a rehearsal.

## Workflow

```
- [ ] 1. Clarify the goal
- [ ] 2. Facts versus story
- [ ] 3. Draft the opener
- [ ] 4. Anticipate their side
- [ ] 5. Plan the setting
- [ ] 6. Rehearse
```

1. **Clarify the goal.** What outcome do they want, and what relationship do they want afterwards? "Win the argument" is rarely the real goal.
2. **Facts versus story.** Separate what happened (observable) from what they concluded ("he doesn't respect me"). Lead with facts; offer the story as their interpretation.
3. **Draft the opener.** Observation, feeling, need, request: "When plans get cancelled on the day, I feel pushed aside, because time together matters to me. Could we agree to give a day's notice?" Keep it under 30 seconds.
4. **Anticipate their side.** What might they feel, say or be afraid of? Prepare to ask "How do you see it?" and to listen. Plan one calm response to the most likely hard reaction (anger, tears, denial, changing the subject).
5. **Plan the setting.** Private, unrushed, not when either is hungry, tired or drunk; not by text for emotional topics if a conversation is possible.
6. **Rehearse.** Offer role-play: Claude plays the other person, first reasonably, then with realistic pushback, then gives feedback on clarity and tone.

## Prep sheet

```
Goal: …
Facts: …
Opener: …
Their likely view: …
If they [reaction], I will …
What I can accept: …
```

## On Claude's own work

When Claude must tell the person something unwelcome (their plan has a flaw, it cannot do what they asked, it made an error), it does the same: lead with the facts, say it early and plainly, explain why it matters, and offer a way forward. Honesty delivered kindly beats softening it into vagueness.

For a conversation between two other people where the user is the neutral go-between, use `conflict-mediation` in cognition/communication-regulation.

**Memetic check before it's sent:** openers and scripts travel beyond this chat, so check them with `memetic-ethics` in cognition/communication-regulation: accurate, fair to the people involved, and clear even when quoted alone.

## Gotchas

- Scripts help start, but the conversation will go off-script; the goal and the listening matter more than the words.
- If they fear for their safety raising something, safety comes first: do not coach them into a confrontation; point to specialist support.
- Ending a conversation to cool down is allowed; agree a time to return.

## Commands

- 🗝️ **Goal clear, facts first, listen** · `prepare conversation`: Prepares for or handles a difficult conversation: clarify the goal, separate facts from story, draft the opener, anticipate their side, plan the setting and rehearse.
  - 📝 `fill prep sheet`: Completes the prep sheet for the conversation with the person.
  - 🎬 `draft opener`: Writes the first two sentences, fact-based and non-blaming.
  - 🎭 `rehearse conversation hard`: Rehearses the conversation, playing the other person realistically.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents interpersonal/difficult-conversations` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review interpersonal/difficult-conversations` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
