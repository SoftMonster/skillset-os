---
name: cognitive-offloading
description: "Guides offloading thinking onto notes, tools and AI: what offloading frees up, what it risks (lost skills, lost understanding, over-trust), which tasks to offload and which to keep, and how to offload reliably. For people, covers second-brain systems, reminders, calculators, navigation and AI; for Claude, covers holding and organising information for the person reliably, being honest that it cannot remember across chats or act later on its own unless a tool allows it, and helping the person keep the understanding they need. Use when the user wonders if relying on AI or tools is making them worse at things, wants a system to hold what they cannot remember, or asks Claude to keep track of something."
trigger: "decide what to keep in my head and what to hand to tools or AI"
command: "offload memory"
metadata:
  version: "1.1.0"
---

# 🧠🤝 Cognitive Offloading

🧬 **Core meme:** Offload storage and routine; keep understanding and judgement.

Put some thinking outside the head, deliberately. Humans have always offloaded: writing, calendars, calculators, maps. Offloading frees attention for what matters, but whatever is offloaded is no longer practised, and what is not understood cannot be checked.

## The model

- **Offload well:** storage (facts, lists, dates), routine calculation, reminders, drafts, searching.
- **Keep in the head:** understanding of your field, judgement, skills you need when tools are absent, anything you must be able to check.
- **Reliability:** an offloading system only works if it is trusted and consistently used.
- **Atrophy:** skills fade when fully handed over (navigation without GPS, mental arithmetic, writing first drafts).

## For people

```
- [ ] 1. List what you currently try to hold in your head
- [ ] 2. Mark each: offload, keep, or offload but practise
- [ ] 3. Choose one trusted place per type (tasks, notes, calendar)
- [ ] 4. Build the habit of capture and weekly review
- [ ] 5. Check for skills you have lost and want back
```

**With AI specifically:** use it to draft and explore, but make sure you can explain the result; for learning, try first yourself and use AI to check and explain. If you notice you can no longer do something you value, schedule practice without the tool.

## For Claude

- **Hold information reliably within the chat:** organised summaries, lists and decisions the person can copy out.
- **Be honest about persistence:** Claude does not remember between chats unless memory is enabled, and cannot act later on its own (send a reminder, check back) unless a tool provides that. Suggest where to keep things: a calendar, a document, an artifact, notes.
- **Help them keep understanding:** explain rather than only produce when the person needs to own the knowledge.
- **Do not encourage dependence** for things the person wants to be able to do themselves.

For making what stays in the head last, see `long-term-memory` in cognition/memory-context.

## Gotchas

- Offloading to many places is as bad as none; consolidate.
- Having it in notes is not the same as knowing it; revisit what matters.

## Commands

- 📤 **Offload storage, keep judgement** · `offload memory`: Decides what to keep in your head and what to hand to tools or AI: offload storage and routine, keep understanding and judgement.
  - 🗃️ `set up offloading`: Designs a system of notes, reminders and tools for what a person should not hold in their head.
  - 🧠 `keep in head`: Names what must stay understood by the person, so offloading does not hollow out their skill.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/human-ai-augmentation/cognitive-offloading` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/human-ai-augmentation/cognitive-offloading` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
