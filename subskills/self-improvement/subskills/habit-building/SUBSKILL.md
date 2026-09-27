---
name: habit-building
description: "Designs habits that stick and dismantles unwanted ones: starts one tiny behaviour, anchors it to an existing cue, shapes the environment, sets up tracking and a never-miss-twice rule, and for unwanted habits maps cue, craving and payoff to find a substitute and add friction. Use when the user wants to start exercising, reading, meditating, journaling or any routine, stop scrolling, snacking or another habit, build a morning or evening routine, or keeps failing at consistency. For dependence or compulsions causing serious harm, respond with care and point to professional support rather than a habit plan. Also turns repeated corrections of Claude into lasting skill edits."
trigger: "build a new habit or break a bad one"
metadata:
  version: "1.1.0"
---

# Habit building

🧬 **Core meme:** Make it tiny, tie it to a cue, and never miss twice.

Design one habit change that survives bad days. Good output is a one-card habit plan: the tiny behaviour, its cue, the environment changes, how it is tracked, and what happens after a miss.

## Build a habit

```
- [ ] 1. Pick one habit
- [ ] 2. Shrink it
- [ ] 3. Anchor it
- [ ] 4. Shape the environment
- [ ] 5. Track and recover
- [ ] 6. Grow it
```

1. **Pick one habit.** One at a time; stacking several new habits at once is the most common failure. Choose the one that makes others easier (sleep before early workouts).
2. **Shrink it.** Make the starting version take under two minutes: "put on running shoes", "read one page", "one minute of breathing". The goal for the first two weeks is showing up, not results.
3. **Anchor it.** Tie it to something that already happens daily: "After I pour my morning coffee, I will …". A specific existing cue beats a time of day.
4. **Shape the environment.** Make it obvious and easy (book on the pillow, kit by the door) and give it an immediate small reward (tick the tracker, a favourite podcast only while walking).
5. **Track and recover.** A simple streak tracker (paper, app or an artifact Claude can build). Agree the rule: never miss twice. One miss is normal; two starts a new pattern. Plan the minimum version for bad days.
6. **Grow it.** After about two weeks of reliable showing up, add a little (one page to five). Habits take weeks to months to feel automatic, and missing a day does not reset that.

## Break a habit

1. Map the loop: the **cue** (time, place, emotion, people), the **craving**, the **behaviour** and the **payoff** it gives (relief, stimulation, connection). Ask them to notice it for a few days before changing anything.
2. Keep the payoff, change the behaviour: a substitute that meets the same need (bored at 9pm → text a friend instead of scrolling).
3. Add friction: phone charging outside the bedroom, apps logged out, snacks not bought.
4. Treat slips as data: what was the cue this time?

## Habit card

```
Habit: After [existing cue], I will [two-minute version].
Environment: [make it obvious/easy, or add friction]
Reward: [immediate]
Tracking: [where]
Bad-day version: [even smaller]
Grow when: [after N days, add ...]
```

## On Claude's own work

Claude's habits live in its skills, since nothing else carries over between chats. When the person corrects the same kind of thing twice, apply never-miss-twice: propose a sub-skill edit written as a habit card, "When [cue], Claude will [behaviour]", with the check that proves it. To break an unwanted pattern, name its cue and add friction: a checklist step or a Gotchas line in the relevant sub-skill.

## Gotchas

- Identity helps: "I'm someone who moves every day" survives better than "I must lose weight".
- No shaming language about misses; guilt makes quitting more likely.
- If a habit to break is substance use, gambling, self-harm, binge or purge behaviour, or feels out of control, this is not a habit plan. Respond with care and suggest professional or specialist support.
- Exercise habits: start where the person is; suggest they check with a doctor if they have health conditions.

## Commands

- 🔗 **Tiny, tied to a cue, never miss twice** · `build habit`: Builds a new habit or breaks a bad one: pick one, shrink it, anchor it, shape the environment, track and recover, grow it.
  - 🚭 `break habit`: Plans how to break a bad habit by changing cues, friction and replacement.
  - 🪪 `make habit card`: Writes a one-card summary of the habit: cue, tiny action, reward and recovery.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents self-improvement/habit-building` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review self-improvement/habit-building` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
