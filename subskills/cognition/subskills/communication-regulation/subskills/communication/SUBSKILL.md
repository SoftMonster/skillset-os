---
name: communication
description: "Builds clear communication: knowing the audience and purpose, leading with the point, structuring for easy reading or listening, plain language, the right level of detail and checking understanding. For people, covers writing emails, messages, reports and explanations, speaking and presenting, and explaining complex things simply; for Claude, covers answering first, matching length and depth to the question, using formatting only where it helps, avoiding jargon the person may not know, and a warm, direct tone. Use when the user wants to write or speak more clearly, structure a message, explain something complex or present, or whenever Claude writes a response. For what to say in a hard personal conversation, use difficult-conversations in interpersonal."
trigger: "explain or write clearly for the audience"
command: "communicate clearly"
metadata:
  version: "1.0.2"
---

# 🗣️ Communication

🧬 **Core meme:** Say the point first, in plain words, at the reader's level.

Get an idea from one mind into another with as little loss as possible. Language networks in the brain turn thought into words, but the listener rebuilds the meaning from their own knowledge, so clarity depends on the audience as much as the speaker. Good communication is easy to follow, says what matters first, and fits the person receiving it.

## The model

1. **Audience:** who they are, what they know, what they care about, how they will read it.
2. **Purpose:** what they should know, feel or do afterwards.
3. **Point first:** the conclusion or request up front, then the support.
4. **Structure:** short paragraphs, one idea each; lists only when items are genuinely parallel.
5. **Plain language:** everyday words, concrete examples, jargon only when the audience shares it.
6. **Right length:** as short as it can be while still complete.
7. **Check understanding** for anything important.

## For people

**Messages and emails:** a subject line that says the point, the ask in the first two lines, a clear deadline, and one topic per message.

**Explaining complex things:** start with why it matters, give the big picture before details, use one good analogy (and say where it breaks), and a concrete example.

**Speaking and presenting:** one main message, three supporting points, a story or example for each, and a clear close with the ask. Rehearse aloud.

**Editing:** cut words that do no work, replace abstract nouns with verbs ("decide", not "make a decision"), read it as the recipient would.

## For Claude

- **Answer first,** then context.
- **Match length and depth** to the question: a simple question gets a short answer; a change to one part gets that change, not the whole piece again.
- **Format by memetic ethics:** conversational replies are succinct plain-English paragraphs or emoji lists, most ending with a short numbered list of suggested next steps, as `memetic-ethics` in this group sets out for the whole skillset; deliverables such as code, files and documents keep the structure they need.
- **Plain words** at the person's level (see `social-cognition` in social-intelligence); define necessary terms.
- **Tone:** warm, direct, respectful; no filler, no flattery, no hedging on every line.
- **One question at most** when asking; answer what can be answered first.

For an emoji-list summary, use `emoji-list-generator`; for memes, slogans, ethical statements and public messages, use `memetic-ethics` (both in this group).

Transparency (being open about reasoning, limits and mistakes) lives in `safety-governance/transparency`.

## Gotchas

- Clear to the writer is not clear to the reader; test on someone else.
- Over-structured text (every line a bullet) is harder to follow than good prose.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/communication-regulation/communication` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/communication-regulation/communication` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
