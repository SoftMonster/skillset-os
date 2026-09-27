---
name: social-intelligence
description: "Social faculties: social cognition, affective understanding, relationship modelling, cultural intelligence and intent inference (active listening lives in interpersonal). Use when the user wants to understand people, emotions, motives, group or family dynamics or other cultures, or when Claude models what the person knows and wants, reads tone or keeps track of the people involved."
trigger: "understand people, read emotions, intentions and relationships, or work across cultures"
metadata:
  version: "1.0.1"
---

# Social intelligence

A nested skillset. Pick the member whose "Use when" matches the request and read its instructions; for a nested skillset or a zip, run `python3 <top>/scripts/skillset.py open <path>` to get the file to read.

These are the social faculties: modelling minds, emotions, relationships, cultures and intentions. Each member has a "For people" and a "For Claude" half.

**👂 Active listening** belongs to this group but lives in the `interpersonal` skillset (`interpersonal/active-listening`), so there is one copy. Open it from there for listening requests.

These members cover the underlying faculty. For what to say or do in a specific relationship or conversation, use the practical members of `interpersonal`. Mapping or reading people is for understanding and acting fairly, never for manipulating them.

## Members

<!-- subskills:start -->
| Member | Kind | Version | Use when |
|---|---|---|---|
| [affective-understanding](subskills/affective-understanding/SUBSKILL.md) | skill | 1.0.1 | Explains and reads emotions: what emotions are and do, how appraisals and needs drive them, recognising them from words, voice, face and behaviour, mixed and masked emotions, and how emotions shape thinking. For people, builds emotional vocabulary and accurate reading of feelings; for Claude, covers reading emotional tone in text, responding to the feeling behind a message, and not claiming or projecting feelings. Use when the user wants to understand an emotion, why they or someone feels a certain way, or to read feelings better. Do not use for staying calm in the moment; use emotional-intelligence in interpersonal. |
| [cultural-intelligence](subskills/cultural-intelligence/SUBSKILL.md) | skill | 1.0.1 | Builds cultural intelligence: motivation, knowledge of how cultures differ (directness, hierarchy, time, context, individual and group), planning for cross-cultural situations, and adapting behaviour, while treating cultural patterns as tendencies, not stereotypes. For people, covers working in international teams, moving or travelling abroad, and cross-cultural relationships; for Claude, covers not assuming one country's defaults for spelling, units, dates, law, holidays and norms, and adapting examples and tone to the person. Use when the user works or lives across cultures, prepares for a trip or move, or wants to avoid cultural misunderstandings. |
| [intent-inference](subskills/intent-inference/SUBSKILL.md) | skill | 1.1.1 | Infers intent: the literal request, the immediate aim, the deeper goal and the unstated standards behind it, using context and evidence, and checking rather than assuming. For people, covers understanding what others want from them, reading between the lines and clarifying requests; for Claude, covers interpreting requests neither too literally nor too liberally, asking only when it matters, and weighing intent signals fairly without assuming bad intent from thin cues. Use when the user is unsure what someone wants or means, gets requests wrong, or when a request to Claude is ambiguous or could be read several ways. |
| [relationship-modelling](subskills/relationship-modelling/SUBSKILL.md) | skill | 1.0.1 | Builds a mental model of relationships: who is involved, their roles, history, trust, obligations, power and alliances, and how these change over time. For people, covers mapping a family, team or social network, spotting dynamics and patterns, and predicting how moves will land; for Claude, covers tracking the people in the person's story, the stakeholders in a task, and its own role with the person as a helpful collaborator. Use when the user is navigating a complex situation with several people, office politics, family dynamics, or asks who to involve, or when Claude must keep track of third parties. Do not use for improving one relationship; use close-relationships or workplace-relationships in interpersonal. |
| [social-cognition](subskills/social-cognition/SUBSKILL.md) | skill | 1.0.1 | Builds theory of mind: modelling what another person knows, believes, wants and can see, taking their perspective, explaining behaviour without the usual attribution errors, and understanding group dynamics and social influence. For people, covers understanding why others act as they do and seeing a situation from their side; for Claude, covers modelling what the person knows and can see, writing for their actual level and avoiding projecting its own knowledge onto them. Use when the user is puzzled by someone's behaviour, wants to see another point of view, or asks about group dynamics, or when Claude must judge what the person already knows. |
<!-- subskills:end -->

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/social-intelligence` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/social-intelligence` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
