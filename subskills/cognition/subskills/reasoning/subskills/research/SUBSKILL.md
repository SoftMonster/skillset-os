---
name: research
description: "Runs research that reaches reliable answers: frames the question, plans sources, searches systematically, evaluates source quality and evidence strength, triangulates, tracks what is known and unknown, and synthesises with citations. For people, covers researching a topic, reading studies critically and spotting misinformation; for Claude, covers searching for anything current or specific instead of relying on memory, preferring primary sources, reporting conflicts between sources and paraphrasing rather than copying. Use when the user wants to research something, check a claim, evaluate a source or study, or learn how to research, or when Claude needs evidence it does not reliably have."
trigger: "research a question or judge how good a source is"
metadata:
  version: "1.0.0"
---

# 🔬 Research

🧬 **Core meme:** Search for the opposite too, and trust sources in proportion to their evidence.

Find out what is true, how sure we can be, and where the evidence comes from. Good research starts with a precise question, uses sources in proportion to their reliability, looks for disconfirming evidence, and ends with a synthesis that separates the solid from the uncertain.

## Workflow

```
- [ ] 1. Frame the question
- [ ] 2. Plan sources
- [ ] 3. Search systematically
- [ ] 4. Evaluate each source
- [ ] 5. Triangulate
- [ ] 6. Synthesise
```

1. **Frame:** a specific, answerable question; note sub-questions and what "enough" looks like.
2. **Plan sources:** primary sources (data, official documents, original studies) first; reviews and meta-analyses for the state of evidence; quality journalism for events; experts for interpretation.
3. **Search:** varied terms, including terms opponents would use; follow citations back to the origin.
4. **Evaluate:** who produced it, their expertise and incentives, date, methods, sample size, whether it was peer reviewed or replicated, and whether the claim goes beyond the evidence. Lateral reading: check what others say about a source.
5. **Triangulate:** independent sources agreeing is strong; many sources repeating one origin is not.
6. **Synthesise:** answer the question, grade confidence, note disagreements and gaps, cite sources.

**Evidence strength, roughly:** systematic reviews > randomised trials > cohort studies > case reports > expert opinion > anecdote. Watch for correlation presented as causation, relative risk without absolute risk, and headlines that overstate studies.

## For Claude

- **Search rather than recall** for anything current, specific, numerical or after the knowledge cutoff; scale the number of searches to the question.
- **Prefer original sources** over aggregators; say when a requested source was not found.
- **Report conflicts** between sources rather than picking silently.
- **Cite and paraphrase:** attribute claims; summarise in its own words and keep quotes short.
- **Never invent** a citation, study or statistic.

## Gotchas

- Searching for confirmation finds it; search for the opposite too.
- The absence of evidence in a quick search is not evidence of absence.
- On contested political topics, present the range of well-supported views fairly.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/reasoning/research` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/reasoning/research` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
