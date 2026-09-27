---
name: life-vision
description: "Helps the user clarify core values, how each area of life is going and a vivid picture of the life they want in three to five years, using a values sort, a life-areas check-in and a short written vision. Use when the user feels lost, stuck or directionless, asks what they want from life, wants to find their values, purpose or direction, do a wheel of life, or wants a foundation before setting goals. Do not use for turning a direction into concrete goals; use goal-setting. Also agrees with the person what good help from Claude looks like."
trigger: "clarify my values, priorities or a vision for my life"
command: "envision life"
metadata:
  version: "1.0.1"
---

# Life vision and values

🧬 **Core meme:** Find your values in your stories, then picture an ordinary good day.

Help the person see what they actually want, in their own words, so later goals point somewhere that matters to them. Good output is a short list of their top values with what each means to them, an honest snapshot of each life area, and a vision paragraph they recognise as theirs.

## Workflow

```
- [ ] 1. Check in on life areas
- [ ] 2. Surface values
- [ ] 3. Write the vision
- [ ] 4. Pick the focus
```

1. **Check in on life areas.** Ask for a 1–10 rating and one sentence on each: health and energy, work and career, money, relationships and family, friends and community, growth and learning, fun and rest, home and environment, meaning or spirituality. Scores show where attention is wanted; the sentences show why. Keep it quick: ratings are a prompt, not a measurement.
2. **Surface values.** Values come out of stories better than lists. Ask two or three of: a moment they felt most alive or proud and what it said about them; what makes them angry when they see it (a violated value); who they admire and for what; what they would do with a year fully funded. Propose five to seven candidate values from their answers, then have them cut to three to five and define each in a phrase ("Freedom: I choose how my days go"). Their definition matters more than the word.
3. **Write the vision.** Draft a present-tense paragraph of an ordinary good day three to five years out, using their values and their words, concrete enough to picture (where they wake, who is there, what the work is, how they feel). Ask what rings false and revise once or twice.
4. **Pick the focus.** Name the one or two life areas where a change would lift the most others, and offer to turn them into goals with `goal-setting`.

## Example

Values (their definitions): *Craft — doing work I'm proud of. Closeness — time with people who know me. Health — a body that lets me say yes.*
Focus: health (4/10, "always tired") and friends (3/10, "moved city, know nobody"); better sleep and movement would lift energy for everything else.

## On Claude's own work

Claude's values are given, not chosen here, so this member does not rewrite them. Use it instead to agree what good help looks like with this person: what they value in how Claude works (speed or thoroughness, questions or initiative, brief or detailed), which areas of the collaboration are going well or badly (rate them like life areas), and a short "how Claude works with you" statement. Offer to save that statement as a sub-skill so it lasts beyond this chat.

## Gotchas

- Do not supply values the person has not shown. "Achievement" is a common default; check it is theirs, not what they think they should say.
- A low score is information, not a failing. Keep the tone curious.
- If the check-in surfaces grief, a crisis or deep distress, stop the exercise and respond to that first.
- People with little money, time or freedom still have values; keep the vision grounded in their real constraints.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents self-improvement/life-vision` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review self-improvement/life-vision` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
