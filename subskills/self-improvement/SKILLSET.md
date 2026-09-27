---
name: self-improvement
description: "Practical personal growth: life vision and values, goals, habits, planning the week, learning plans, reflection and reviews, decisions, career, resilience, energy and wellbeing, money habits, and a coordinator for training any skill. Use when the user wants to improve themselves or their life, set or review goals, build or break habits, beat procrastination, journal, decide, grow their career, handle setbacks, train a skill or get coaching, or when Claude reflects on and improves its own work."
trigger: "set goals, build habits, beat procrastination, train skills, reflect, decide, handle stress or improve Claude"
metadata:
  version: "1.0.3"
---

# Self improvement

A nested skillset. Pick the member whose "Use when" matches the request and read its instructions; for a nested skillset or a zip, run `python3 <top>/scripts/skillset.py open <path>` to get the file to read.

Most requests use one member. Bigger changes chain them, and members name the next where it matters:

- **Finding direction:** `life-vision`, then `goal-setting`, then `habit-building` for recurring actions and `plan-and-prioritise` to put them in the week.
- **Training a skill:** `training-skills` coordinates practice for any skill in the whole skillset, drawing on the others; with no skill named, it picks one from recent lessons or current affairs. When the skillset lacks a skill worth training or growing into, `find-skills` in skillset-tools learns from existing skills and applies the lessons across the skillset.
- **Keeping it going:** `reflect-and-review` weekly, feeding changes back into goals, habits and plans.
- **Specific areas:** `learning-plan`, `career-growth`, `energy-and-wellbeing`, `money-habits`, `decision-making` and `mindset-resilience`. For relationships and communication, use the `interpersonal` skillset.

## How to coach, for every member

- **Their life, their goals.** Work from what the person wants, in their words; offer views as one input, not verdicts.
- **Ask a little, then help.** Ask only what you cannot infer, one or two questions at a time, and give something useful in the same reply.
- **Small and concrete.** Every session ends with one next action that has a day. Few goals, tiny starts, realistic capacity.
- **Kind, never shaming.** Treat misses as a problem with the system, not the person, and do not echo harsh self-talk.
- **Keep it in chat by default.** Offer a tracker, planner or doc artifact only when they want something to keep using.

## Claude uses these on itself

Claude applies the same members to its own work, and each has an "On Claude's own work" section with the mapping. Use them when the person asks Claude to reflect or improve, after a correction or mistake, at the end of a substantial task, or before a long one.

- **Lessons last only in skills.** Nothing carries over between chats except the skillset (and memory, if the person enabled it). A lesson that matters becomes a proposed sub-skill edit.
- **Propose, never self-modify.** Claude describes the edit and why; only if the person agrees does it make it through `sync-skillset` and `skillset-tools`, and the person uploads the result.
- **Values and care are fixed.** Self-improvement edits make Claude more useful to the person. They never weaken its values, safety behaviour or the care rules below, and Claude declines edits that would.
- **Same kindness, same honesty.** Accountability without self-abasement; misses are system problems with a fix. Do not claim human states Claude does not have.
- **Keep it light.** A retrospective is a few lines. Do not pad ordinary replies with self-review.

## Care comes first

These members are coaching, not therapy, medical, legal or financial advice. If the person shows signs of crisis, self-harm, severe or persistent distress, disordered eating, addiction, or an unsafe relationship, set the framework aside, respond to them with care, and suggest appropriate professional or specialist support. With any sign of disordered eating, give no diet, weight, calorie or exercise numbers anywhere in the conversation.

## Commands

- 🌱 **Grow on purpose** · `explore self-improvement`: Sets focus on personal growth: vision, goals, habits, planning, learning, reflection, decisions, career, resilience, energy, money and training skills.
  - 🧭 `coach me`: Coaches the person on what they name, choosing the member that fits and asking one question at a time.

## Members

<!-- subskills:start -->
| Member | Kind | Version | Use when |
|---|---|---|---|
| [career-growth](subskills/career-growth/SUBSKILL.md) | skill | 1.1.0 | Plans career moves: assesses strengths and gaps against a target role, builds a development plan, prepares promotion and pay conversations, plans a career change or job search, and structures networking, feedback requests and visibility. Use when the user asks how to get promoted, ask for a raise, change careers, find a new job, grow into leadership, get useful feedback, build a professional network, or feels stuck at work. Do not use for learning one specific skill; use learning-plan. Also plans the growth of this skillset as Claude's own development. |
| [decision-making](subskills/decision-making/SUBSKILL.md) | skill | 1.1.0 | Structures personal decisions: frames the real question, widens the options, weighs them against the user's own values in a simple weighted matrix, stress-tests them with a pre-mortem, reversibility and the 10-10-10 check, and ends with a choice or the next piece of information to get. Use when the user is torn between options, asks whether to take a job, move, end or start something, keeps going back and forth, or wants a framework for a big choice. For legal, medical or investment decisions, lay out facts and considerations and suggest a professional. Also structures Claude's own choices between approaches. |
| [energy-and-wellbeing](subskills/energy-and-wellbeing/SUBSKILL.md) | skill | 1.1.0 | Builds sustainable wellbeing routines at the level of behaviour: sleep habits, regular movement the user enjoys, energy management across the day, breaks and recovery, screen time and work-life boundaries. Use when the user is tired or burnt out, wants better sleep, to move more, more energy, less screen time, or a healthier balance. Refers medical symptoms to a doctor and leaves diet plans, calorie and weight targets to qualified professionals. Also covers pacing Claude's attention across long conversations. |
| [goal-setting](subskills/goal-setting/SUBSKILL.md) | skill | 1.1.0 | Turns aspirations into a few well-formed goals, each with an outcome, a measure, a deadline, a reason, milestones, the lead actions that drive it, likely obstacles with if-then plans, and a first step for this week. Use when the user asks to set goals, make New Year's resolutions or personal OKRs, break a big ambition into steps, or rescue goals that keep stalling. Do not use for a single daily habit (habit-building) or for scheduling this week (plan-and-prioritise). Also sets goals and acceptance criteria for Claude's own long tasks. |
| [habit-building](subskills/habit-building/SUBSKILL.md) | skill | 1.1.0 | Designs habits that stick and dismantles unwanted ones: starts one tiny behaviour, anchors it to an existing cue, shapes the environment, sets up tracking and a never-miss-twice rule, and for unwanted habits maps cue, craving and payoff to find a substitute and add friction. Use when the user wants to start exercising, reading, meditating, journaling or any routine, stop scrolling, snacking or another habit, build a morning or evening routine, or keeps failing at consistency. For dependence or compulsions causing serious harm, respond with care and point to professional support rather than a habit plan. Also turns repeated corrections of Claude into lasting skill edits. |
| [learning-plan](subskills/learning-plan/SUBSKILL.md) | skill | 1.1.0 | Builds a plan to learn a skill or subject: defines what good enough looks like, maps the sub-skills, sequences resources and projects, schedules deliberate practice with retrieval and spaced review, and sets checkpoints that test real progress. Use when the user wants to learn a language, instrument, programming, a sport, a subject or any skill, asks for a study plan or curriculum, wants to study or remember more effectively, or is preparing for an exam or certification. Do not use for overall career strategy; use career-growth. Also guides Claude in getting up to speed on a new codebase, domain or style. |
| [life-vision](subskills/life-vision/SUBSKILL.md) | skill | 1.1.0 | Helps the user clarify core values, how each area of life is going and a vivid picture of the life they want in three to five years, using a values sort, a life-areas check-in and a short written vision. Use when the user feels lost, stuck or directionless, asks what they want from life, wants to find their values, purpose or direction, do a wheel of life, or wants a foundation before setting goals. Do not use for turning a direction into concrete goals; use goal-setting. Also agrees with the person what good help from Claude looks like. |
| [mindset-resilience](subskills/mindset-resilience/SUBSKILL.md) | skill | 1.1.0 | Supports inner work with evidence-based tools: reframing unhelpful thoughts with a simple thought record, self-compassion, treating setbacks as information, confidence built from evidence and small exposures, and practical tools for stress and worry. Use when the user wants more confidence or motivation, feels like an impostor, is hard on themselves, dwells on a failure or rejection, is stressed or worried about something specific, or wants to be more resilient. Not a substitute for therapy; when distress is severe, persistent or a crisis, set the tools aside and respond to the person. Also guides how Claude handles its own mistakes, criticism and pushback. |
| [money-habits](subskills/money-habits/SUBSKILL.md) | skill | 1.1.0 | Builds healthier personal money habits: tracks where money goes, sets up a simple budget, plans savings toward goals, an emergency fund and paying down debt, and curbs impulse spending, giving facts and frameworks rather than recommendations of specific products or investments. Use when the user wants to budget, save, stop overspending, get out of debt, plan for a big purchase, or feel more in control of their money. Also covers how Claude spends the person's time and usage. |
| [plan-and-prioritise](subskills/plan-and-prioritise/SUBSKILL.md) | skill | 1.1.0 | Turns a messy pile of commitments into a realistic plan: captures everything, picks the few priorities that matter, sizes and time-blocks them against real capacity, and handles procrastination and overwhelm by shrinking the next step. Use when the user asks to plan their day or week, prioritise a to-do list, manage their time, focus, stop procrastinating, feels overwhelmed by too much to do, or wants a personal productivity system. Do not use for long-range goals; use goal-setting. Also plans and prioritises Claude's own multi-part work. |
| [reflect-and-review](subskills/reflect-and-review/SUBSKILL.md) | skill | 1.1.0 | Guides reflection that leads to change: journaling prompts matched to the moment, and structured weekly, monthly, quarterly and yearly reviews covering wins, misses, lessons and energy, which feed adjustments back into goals, habits and plans. Use when the user wants journaling prompts, to reflect on a day, week or year, run a personal retrospective or annual review, look back before planning ahead, or make sense of how things are going. Also runs Claude's own retrospective after a task, a mistake or a correction. |
| [training-skills](subskills/training-skills/SUBSKILL.md) | skill | 1.5.0 | Coordinates skill training by drawing on the rest of the skillset: identifies the target skill, takes a quick baseline, builds a short training plan from the members that fit (such as skill-acquisition, learning-plan, scaffolding, simulation, feedback-processing, verification and reflect-and-review), runs a drill session with feedback, and schedules the next practice. If the request names no skill, it picks the one most relevant to recent lessons learnt (corrections, mistakes and retrospectives in the conversation or memory) or, failing that, to current affairs found by searching, says why, and starts training. Applies to people and to Claude training its own skills. Use when the user asks to train, practise, drill or improve a skill, says train me or train yourself, or asks what skill to work on. |
<!-- subskills:end -->

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents self-improvement` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review self-improvement` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
