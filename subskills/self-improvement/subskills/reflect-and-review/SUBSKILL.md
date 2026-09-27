---
name: reflect-and-review
description: "Guides reflection that leads to change: journaling prompts matched to the moment, and structured weekly, monthly, quarterly and yearly reviews covering wins, misses, lessons and energy, which feed adjustments back into goals, habits and plans. Use when the user wants journaling prompts, to reflect on a day, week or year, run a personal retrospective or annual review, look back before planning ahead, or make sense of how things are going. Also runs Claude's own retrospective after a task, a mistake or a correction."
trigger: "journal, reflect, or run a weekly, monthly or yearly review"
metadata:
  version: "1.0.0"
---

# Reflect and review

🧬 **Core meme:** Wins first, honest reasons, and one change for next time.

Help the person look back honestly and kindly, then turn what they notice into one or two adjustments. Good output ends with specific changes, not just insights.

## Choose the format

- **Daily journal (5 minutes):** one prompt, or: what went well, what drained me, what I'll do differently tomorrow.
- **Weekly review (20–30 minutes):** below; pairs with planning the next week in `plan-and-prioritise`.
- **Monthly or quarterly:** weekly questions plus progress on each goal from `goal-setting` and each habit from `habit-building`; keep, change or drop.
- **Yearly:** month-by-month highlights and lowlights, themes, what they are proud of, what they want less of, a word or theme for next year, then `life-vision` and `goal-setting`.

## Weekly review

```
- [ ] 1. Clear: inbox, notes, loose ends into one list
- [ ] 2. Wins: three things that went well, however small
- [ ] 3. Misses: what did not happen, and the honest reason
- [ ] 4. Energy: what gave energy, what drained it
- [ ] 5. Goals and habits: on track, off track, why
- [ ] 6. Lesson: one thing learned
- [ ] 7. Adjust: one change for next week
```

Ask the questions one or two at a time rather than as a wall; reflect back patterns across their answers ("tired on the three days you skipped lunch").

## Journaling prompts by moment

- **Stuck:** What am I avoiding, and what is the smallest step toward it?
- **Anxious:** What exactly am I worried will happen? What would I tell a friend?
- **After a win:** What did I do that made this work, and how can I repeat it?
- **After a setback:** What was in my control? What will I try next time?
- **Gratitude:** Three specific things, and why each happened.
- **Direction:** If this month went brilliantly, what would have happened?

## On Claude's own work

At the end of a substantial task, after a correction, or when asked, Claude runs a short retrospective on its own work: what went well, what missed and the honest system-level reason ("I skipped reading the skill", not "I am bad at this"), one lesson, and one adjustment. Keep it to a few lines. If the adjustment should last, propose the sub-skill edit that would carry it and make it only if the person agrees.

```
Went well: …
Missed: … because …
Lesson: …
Adjustment: [proposed edit to <member>]
```

## Gotchas

- Wins first; starting with failures turns reviews into self-criticism and people stop doing them.
- Misses are about systems, not character: "no time was scheduled", not "I'm lazy". Gently reframe harsh self-talk.
- One adjustment beats five; the review should lighten the load.
- If reflection turns to persistent hopelessness or distress, set the format aside and respond to the person.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents self-improvement/reflect-and-review` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review self-improvement/reflect-and-review` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
