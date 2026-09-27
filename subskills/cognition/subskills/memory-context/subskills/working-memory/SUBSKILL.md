---
name: working-memory
description: "Manages information held in mind right now: chunks it, externalises it, reduces load and keeps a running state. For people, covers losing track mid-task, mental overload, following complex conversations or instructions, and mental arithmetic; for Claude, covers keeping a written state of goals, decisions and open items in long tasks, using notes, checklists and scratch files instead of relying on a crowded context, and summarising at milestones. Use when the user feels overloaded or keeps losing track, or when Claude runs a long, multi-step or multi-file task."
trigger: "keep track of several things at once or think with less overload"
metadata:
  version: "1.0.0"
---

# 🧠 Working Memory

🧬 **Core meme:** Write it down to free your head for thinking.

Hold and use the information a task needs right now without dropping pieces. Human working memory holds only about four chunks at once; when it overflows, things are forgotten mid-task or reasoning gets muddled. The fix is rarely "try harder": it is to chunk, externalise and reduce load.

## The model

- **Capacity is small:** a handful of chunks, lost quickly without rehearsal.
- **Chunking** packs several items into one meaningful unit (a phone number in three groups).
- **Externalising** moves items out of the head onto paper or a screen, freeing capacity for thinking.
- **Load** rises with interruptions, stress, tiredness and switching.

## For people

```
- [ ] 1. Spot overload
- [ ] 2. Externalise
- [ ] 3. Chunk and sequence
- [ ] 4. Protect capacity
```

1. **Spot overload:** losing track mid-sentence, walking into a room and forgetting why, re-reading the same line, snapping when interrupted.
2. **Externalise:** a single running list or capture note, writing down steps before starting, sketching the problem, saying the plan out loud.
3. **Chunk and sequence:** group related items, do one step at a time, turn long instructions into a numbered checklist.
4. **Protect capacity:** fewer interruptions (see `attention`), finish or park before switching ("next I was going to…" on a sticky note), sleep and breaks. In conversations, summarise back ("so three things…") to hold the thread.

Mental arithmetic and similar tasks improve with chunking strategies, but general "brain training" games rarely transfer to everyday life; build systems instead.

## For Claude

Claude's context can hold a lot, but attention across a long, crowded context is uneven, and details from far back get missed.
- **Keep a written state** for long or multi-step tasks: goal, constraints, decisions made, done, next. In agentic work, a short notes or task-list file in the working directory serves this.
- **Checklists over recall:** copy workflow checklists (like those in these sub-skills) and tick them off.
- **Summarise at milestones,** and re-read the original request and the state before finishing.
- **Restate key numbers and names** when using them later, rather than trusting they were carried correctly.
- **Offer a fresh start** when a chat has grown very long: a handover summary to paste into a new chat.

## Gotchas

- Overload feels like stupidity; it usually is not. Reducing load is the fix.
- ADHD, stress and poor sleep all reduce working memory; externalising helps regardless of cause, and persistent problems are worth raising with a doctor.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/memory-context/working-memory` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/memory-context/working-memory` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
