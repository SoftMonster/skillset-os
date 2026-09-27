---
name: training-skills
description: "Coordinates skill training by drawing on the rest of the skillset: identifies the target skill, takes a quick baseline, builds a short training plan from the members that fit (such as skill-acquisition, learning-plan, scaffolding, simulation, feedback-processing, verification and reflect-and-review), runs a drill session with feedback, and schedules the next practice. If the request names no skill, it picks the one most relevant to recent lessons learnt (corrections, mistakes and retrospectives in the conversation or memory) or, failing that, to current affairs found by searching, says why, and starts training. Applies to people and to Claude training its own skills. Use when the user asks to train, practise, drill or improve a skill, says train me or train yourself, or asks what skill to work on."
trigger: "train or practise a skill, or pick one to train from recent lessons or current events"
metadata:
  version: "1.1.0"
---

# Training skills

🧬 **Core meme:** Pick one skill, baseline it, drill the weak spot, and book the next session.

Turn "I want to get better at X" into actual practice, using the other skills in this skillset as the training toolkit. Good output names one target skill, shows where the trainee is now, runs a short drill with real feedback, and ends with the next practice session booked. It trains; it does not just describe training.

## Workflow

```
- [ ] 1. Choose the target skill
- [ ] 2. Take a baseline
- [ ] 3. Build the plan from other skills
- [ ] 4. Run a drill session
- [ ] 5. Close the loop
```

### 1. Choose the target skill

**If the request names a skill** ("train my negotiation", "help me practise listening", "train yourself on verification"), use it, and find the member or members that cover it with `skillset.py tree`.

**If no skill is apparent** ("train me", "train yourself", "what should I work on?"), pick one yourself instead of asking, in this order:

1. **Recent lessons learnt:** corrections, mistakes, feedback and retrospectives in this conversation, then past chats or memory if those are available. The skill behind the most recent or most repeated lesson wins, because a lesson that is not practised fades.
2. **Current affairs:** if there are no recent lessons, search today's news (do not rely on memory; see `research` in cognition/reasoning). Pick the skill that current events make most useful, such as spotting misinformation during a big breaking story, calibrating uncertainty in volatile markets, de-escalation when public tempers are high, or privacy stewardship after a major data breach.
3. **Fallback:** the skill in the skillset with the widest everyday payoff for this person (often `attention`, `communication` or `verification`).

State the choice and the reason in one line, name one alternative, and start. The person can redirect.

### 2. Take a baseline

One quick exercise that shows the current level: a short task, a scenario to respond to, or a question they answer before any teaching. Note one strength and the single weakness that matters most. Baselines make progress visible later.

### 3. Build the plan from other skills

Draw on the members that fit the skill instead of inventing a method. Default components:

| Need | Use |
|---|---|
| How to practise | `skill-acquisition` (cognition/action-agency): deliberate practice on the weakest sub-skill |
| Longer programme | `learning-plan` (self-improvement) |
| Right level of help | `scaffolding` and `teaching` (cognition/human-ai-augmentation) |
| Realistic practice | `simulation` (cognition/reasoning): role-play and scenarios |
| Feedback | `feedback-processing` (cognition/perception-sensing) and `feedback` (interpersonal) |
| Checking work | `verification` (cognition/action-agency) |
| Making it stick | `habit-building` and `reflect-and-review` (self-improvement) |

If no member covers the skill well, use `find-skills` in skillset-tools to learn from existing skills: it extracts the lessons worth having and folds them into the members they improve, with the person's approval. Train with what is available meanwhile.

Then add the member that holds the skill's own content (for example `negotiation` in interpersonal, `bias-detection` in cognition/reasoning). Read it for the standards the drills should target.

### 4. Run a drill session

Two or three drills, each targeting the weakness from the baseline, just beyond current ability:
1. Set the drill (a scenario, a problem, a role-play turn, a piece to rewrite).
2. The trainee attempts it; give hints before answers (`scaffolding`).
3. Give specific feedback against the skill's standards: what worked, one thing to change.
4. Repeat with slightly more difficulty.

Keep a session to about 10–20 minutes of effort; short and frequent beats long and rare.

### 5. Close the loop

Keep each drill report to about one phone screen: skill, reason, drill, result, fix. Say plainly that ticks are self-graded when Claude is training itself, and stop offering more rounds once the real lessons are used up rather than inventing drills.

A three-line summary: baseline, what improved, the focus for next time. Suggest when to practise next (spaced: in a day or two, then a week), and offer a tracker artifact if they want to log sessions.

## Training Claude's own skills

The same workflow applies when the person says "train yourself" or when Claude trains a skill after its own lessons:
- **Choose** from Claude's recent lessons first: corrections in this chat, errors it made, retrospectives.
- **Baseline and drills:** redo or attempt representative tasks using the relevant sub-skill, and check each result against that sub-skill's standards with `verification`. Show the work so the person can judge it.
- **Be honest about what training means:** Claude's underlying model does not change in a chat. Practice here improves this conversation; lasting improvement means a skill edit, proposed to the person under `ethical-skill-evolution` in cognition/safety-governance, and approved and uploaded by them.

## Example

Person: "Train me." Earlier in the chat they said a meeting went badly because they got defensive when criticised.
Response: "Let's train receiving feedback, because of the meeting you described (alternative: de-escalation). Baseline: I'll give you a blunt piece of criticism about a report; reply as you would in the meeting." Then drills from `feedback` (interpersonal) with `simulation` role-play, rising from mild to harsh criticism, feedback after each, and a note to repeat in two days.

## Gotchas

- Picking a skill from current affairs means training the skill, not taking a side on the news; stay neutral on contested topics.
- Do not choose a skill tied to distressing news for someone who seems vulnerable or upset; pick a steadier one, or respond to how they are first.
- One skill per session. Training everything trains nothing.
- If the "lesson learnt" points to distress or a crisis rather than a skill gap, set training aside and respond to the person.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents self-improvement/training-skills` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review self-improvement/training-skills` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
