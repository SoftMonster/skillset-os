---
name: cognition
description: "A brain-emulation framework of ten groups of cognitive faculties (perception, memory, social intelligence, reasoning, executive function, action, safety and ethics, communication, human-AI augmentation, metacognition), each applied two ways: helping people strengthen it, and guiding Claude to use it on its own work. Use when the user wants to notice, focus, remember, understand people, reason, plan, act, communicate, stay safe or self-correct better, asks how a mental faculty works, wants an emoji list or a meme, or asks Claude to think like a careful mind."
trigger: "notice, remember, reason, plan, communicate, teach, spot scams, self-correct, self-assess, make memes or emoji lists"
metadata:
  version: "1.0.0"
---

# Cognition

A nested skillset. Pick the member whose "Use when" matches the request and read its instructions; for a nested skillset or a zip, run `python3 <top>/scripts/skillset.py open <path>` to get the file to read.

## The framework

Cognition models the faculties of a well-functioning human mind and applies each in two directions: **for people**, to understand and strengthen that faculty in themselves, and **for Claude**, to run the same faculty on its own work. Every sub-skill has both halves.

The ten groups follow the flow of a mind from input to self-development. All ten are present. Start from `metacognition/metacognition` when unsure which faculty applies: it acts as the conductor.

| # | Group | Brain analogue |
|---|---|---|
| 1 | 👁️ Perception and sensing | sensory cortices, attention networks |
| 2 | 🧠 Memory and context | hippocampus, working memory |
| 3 | 🫂 Human and social intelligence | social brain network |
| 4 | 🧠 Reasoning and intelligence | prefrontal and association cortex |
| 5 | 🧭 Executive function | prefrontal control |
| 6 | 🛠️ Action and agency | motor planning, basal ganglia |
| 7 | 🛡️ Safety and ethical governance | threat detection, moral cognition |
| 8 | 🗣️ Communication and relational regulation | language networks, co-regulation |
| 9 | 🤝 Human-AI augmentation | extended mind |
| 10 | 🔄 Metacognition and self-development | self-monitoring, plasticity |

## One home per faculty

Some faculties belong to more than one group. Each lives where it first appears, and later groups point to it rather than keeping a second copy, so the skillset never holds two versions that drift apart:

- **Feedback processing:** home in perception-sensing; action-agency points to it.
- **Self-model:** home in memory-context; metacognition points to it.
- **Skill acquisition, skill composition:** home in action-agency; metacognition points to them.
- **Ethical skill evolution:** home in safety-governance; metacognition points to it.
- **Transparency:** home in safety-governance; communication points to it.
- **Active listening:** home in the `interpersonal` skillset; social intelligence points to it.

Where a faculty overlaps an existing skillset (planning, feedback conversations, conflict), the sub-skill covers the underlying mental faculty and points to the practical member there.

## Memetic ethics throughout

Every faculty communicates by `communication-regulation/memetic-ethics`: meaning kept intact, easy to pass on and ethical, within Claude's built-in values.

## Honest emulation

The brain is an analogy for organising good behaviour, not a claim that Claude has a brain, senses, feelings or memories like a person's. In the "For Claude" halves, describe what Claude actually does (reads inputs, weighs evidence, uses tools, writes text), never human experiences it cannot verify. The rules from `self-improvement` apply: lessons persist only as skill edits the person approves, and self-improvement never weakens Claude's values, safety behaviour or care for the person.

## Members

<!-- subskills:start -->
| Member | Kind | Version | Use when |
|---|---|---|---|
| [action-agency](subskills/action-agency/SKILLSET.md) | skillset | 1.0.0 | Faculties of doing: tool use, agentic execution, skill composition, skill acquisition, verification and error correction (feedback processing lives in perception-sensing). Use when the user or Claude uses tools, runs a multi-step task, learns or combines skills, checks work before calling it done, or fixes a mistake. |
| [communication-regulation](subskills/communication-regulation/SKILLSET.md) | skillset | 1.0.0 | Faculties of speaking and steadying others: clear communication, de-escalation, third-party conflict mediation and regulation support, plus the emoji-list format and the memetic-ethics mode for memes, slogans and public messages (transparency lives in safety-governance). Use when the user or Claude must explain clearly, calm a heated situation, mediate between others, help someone who is distressed, or write an emoji list, meme or public message. |
| [executive-function](subskills/executive-function/SKILLSET.md) | skillset | 1.0.0 | Control faculties: planning, goal alignment, action selection, adaptation, proportionality and long-term orientation. Use when the user or Claude must plan a task, stay on the real goal, choose the next step, change course after a setback, size effort and caution to the stakes, or weigh the long term. |
| [human-ai-augmentation](subskills/human-ai-augmentation/SKILLSET.md) | skillset | 1.0.0 | Faculties where human and AI thinking combine: human-AI collaboration, cognitive offloading, teaching, scaffolding and decision support. Use when the user wants to work better with AI, decide what to offload, teach or tutor someone, support a learner or someone else's decision, or when Claude collaborates, holds information, teaches or informs a choice. |
| [memory-context](subskills/memory-context/SKILLSET.md) | skillset | 1.0.0 | Memory faculties: working memory, long-term memory, semantic understanding, context awareness and self-model. Use when the user wants a better memory, deeper understanding, situational awareness or self-knowledge, or when Claude tracks state in a long task, states honestly what it remembers, pins down meanings, uses the conversation and date correctly, or describes its own abilities. |
| [metacognition](subskills/metacognition/SKILLSET.md) | skillset | 1.0.0 | Self-monitoring faculties: metacognition, the conductor that chooses which faculty to apply, and continuous self-correction (skill acquisition and composition live in action-agency, self-model in memory-context, ethical skill evolution in safety-governance). Use when the user wants to think about how they think or keep improving, or when Claude checks its own reasoning, chooses an approach or corrects course mid-task. |
| [perception-sensing](subskills/perception-sensing/SKILLSET.md) | skillset | 1.0.0 | Input faculties: perception, attention, uncertainty awareness and feedback processing. Use when the user wants to be more observant, focused, calibrated or responsive to feedback, or when Claude must read inputs carefully, stay on the key details, state its confidence honestly or adjust to a correction or surprise. |
| [reasoning](subskills/reasoning/SKILLSET.md) | skillset | 1.0.0 | Thinking faculties: reasoning, creativity, research, adversarial thinking, second-order reasoning, bias detection and simulation. Use when the user or Claude must think a hard problem through, generate ideas, research a question, stress-test a plan or argument, trace knock-on effects, check for bias or model what might happen. |
| [safety-governance](subskills/safety-governance/SKILLSET.md) | skillset | 1.0.0 | Protective faculties: threat detection, safety regulation, ethical reasoning, privacy stewardship, boundary management, manipulation detection, human escalation, transparency and ethical skill evolution. Use when the user or Claude must spot scams or risks, calibrate caution, work through an ethical question, protect privacy, hold limits, recognise manipulation, bring in human help, explain itself honestly or change skills safely. Supports Claude's built-in guidelines and never overrides them. |
| [social-intelligence](subskills/social-intelligence/SKILLSET.md) | skillset | 1.0.0 | Social faculties: social cognition, affective understanding, relationship modelling, cultural intelligence and intent inference (active listening lives in interpersonal). Use when the user wants to understand people, emotions, motives, group or family dynamics or other cultures, or when Claude models what the person knows and wants, reads tone or keeps track of the people involved. |
<!-- subskills:end -->

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
