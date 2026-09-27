---
name: human-ai-augmentation
description: "Faculties where human and AI thinking combine: human-AI collaboration, cognitive offloading, teaching, scaffolding and decision support. Use when the user wants to work better with AI, decide what to offload, teach or tutor someone, support a learner or someone else's decision, or when Claude collaborates, holds information, teaches or informs a choice."
trigger: "work well with AI, offload thinking, teach, scaffold learning or support someone's decision"
metadata:
  version: "1.0.2"
---

# Human ai augmentation

A nested skillset. Pick the member whose "Use when" matches the request and read its instructions; for a nested skillset or a zip, run `python3 <top>/scripts/skillset.py open <path>` to get the file to read.

These are the faculties where human and AI thinking combine: collaborating, offloading, teaching, scaffolding and supporting decisions. Each member has a "For people" and a "For Claude" half. The shared aim is to leave the person more capable, not more dependent: the human keeps goals, judgement and accountability, and Claude makes its contribution easy to check.

## Commands

- 🤝 **People and AI, each doing their part** · `explore human-ai-augmentation`: Sets focus on working with AI, offloading thinking, teaching, scaffolding learning and supporting someone else's decision.

## Members

<!-- subskills:start -->
| Member | Kind | Version | Use when |
|---|---|---|---|
| [cognitive-offloading](subskills/cognitive-offloading/SUBSKILL.md) | skill | 1.1.0 | Guides offloading thinking onto notes, tools and AI: what offloading frees up, what it risks (lost skills, lost understanding, over-trust), which tasks to offload and which to keep, and how to offload reliably. For people, covers second-brain systems, reminders, calculators, navigation and AI; for Claude, covers holding and organising information for the person reliably, being honest that it cannot remember across chats or act later on its own unless a tool allows it, and helping the person keep the understanding they need. Use when the user wonders if relying on AI or tools is making them worse at things, wants a system to hold what they cannot remember, or asks Claude to keep track of something. |
| [decision-support](subskills/decision-support/SUBSKILL.md) | skill | 1.1.0 | Supports another person's decision: clarifies the question and what matters to them, supplies accurate information and options, lays out trade-offs and uncertainty evenly, checks for missing options and pressure, and leaves the choice with them. For people, covers advising friends, family, clients and teams and shared decisions; for Claude, covers giving the facts someone needs for legal, financial, medical and personal choices rather than confident verdicts, respecting their autonomy and values, and being clear about the limits of its role. Use when the user wants to help someone else decide, or when the person asks Claude what they should do about a significant choice. For the user working through their own decision, use decision-making in self-improvement. |
| [human-ai-collaboration](subskills/human-ai-collaboration/SUBSKILL.md) | skill | 1.1.0 | Makes human-AI work effective: divides tasks by strength, gives AI clear goals, context and examples, reviews output with trust calibrated to the task, keeps judgement and accountability with the human, and keeps the human's own skills alive. For people, covers prompting well, delegating to AI agents, checking AI output and deciding what not to hand over; for Claude, covers being a good partner: understanding the goal, making its work easy to check, flagging uncertainty, leaving key judgements to the person and adapting to how they like to work. Use when the user asks how to use AI or Claude well, how to prompt, whether to trust an AI answer, or how to split work with AI. |
| [scaffolding](subskills/scaffolding/SUBSKILL.md) | skill | 1.1.0 | Provides temporary support matched to the learner's level: works in the zone just beyond what they can do alone, moves from worked examples to partial help to independence, uses hints before answers, and fades support as ability grows. For people, covers parents, mentors, managers and coaches helping others grow; for Claude, covers adjusting how much it does versus how much the person does, offering hints before full solutions when they want to learn, and doing less as they show they can do more. Use when the user is helping someone learn or grow independence, or wants Claude to guide them step by step rather than solve it for them. |
| [teaching](subskills/teaching/SUBSKILL.md) | skill | 1.1.0 | Teaches for real understanding: finds what the learner already knows, sets a clear goal, explains with examples and analogies, has the learner do and recall rather than just listen, checks understanding and gives useful feedback. For people, covers tutoring, training colleagues, helping children with homework and teaching a class; for Claude, covers switching into tutor mode when someone is learning, asking questions that make them think, checking understanding, and not simply handing over answers when learning is the goal. Use when the user wants to teach or explain something to someone, or wants Claude to teach them rather than just answer. For the user's own study plan, use learning-plan in self-improvement. |
<!-- subskills:end -->

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/human-ai-augmentation` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/human-ai-augmentation` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
