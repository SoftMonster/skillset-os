---
name: semantic-understanding
description: "Builds real understanding of meaning: concepts and how they relate, definitions, examples and non-examples, jargon, ambiguity, figurative language and implied meaning. For people, covers understanding a hard idea rather than memorising it and explaining it simply; for Claude, covers resolving ambiguous terms, domain-specific senses, and checking that it and the person mean the same thing instead of matching surface words. Use when the user is confused by a concept, wants to understand deeply or explain something simply, or when a request hinges on what a word or phrase means."
trigger: "understand concepts deeply or pin down what something means"
command: "parse meaning"
metadata:
  version: "1.0.1"
---

# 🧩 Semantic Understanding

🧬 **Core meme:** Check the meaning, not just the words.

Grasp what things mean, not just what they say. In the brain, concepts are networks of links: to examples, to related ideas, to uses. Understanding means having those links; memorising a definition does not. Good semantic understanding can explain an idea simply, apply it to a new case, and spot when a word is being used in a different sense.

## The model

- A concept is known through **definition, examples, non-examples, relations** (part of, cause of, opposite of) and **use**.
- Words are **ambiguous**; meaning comes from context, domain and intent.
- Much meaning is **implied**: figurative language, understatement, what is left unsaid.

## For people

To understand something deeply:
1. **Explain it simply** in plain words to an imagined twelve-year-old; where the explanation stalls is where understanding is thin.
2. **Examples and non-examples:** three things that are it, two that look like it but are not, and why.
3. **Map it:** a quick concept map of what it connects to.
4. **Apply it** to a new case or problem.
5. **Check the terms:** jargon often hides a simple idea or a specific technical meaning.

In conversations, when a disagreement will not resolve, check definitions: people often argue past each other using one word in two senses ("freedom", "fair", "done").

## For Claude

- **Resolve ambiguity from context** first (domain, the person's earlier messages, the task). If two readings would lead to very different answers, answer the likely one and name the assumption, or ask one question when the stakes warrant it.
- **Use the domain's sense:** "significant" in statistics, "consideration" in contract law, "model" in ML or fashion.
- **Match meaning, not surface words.** A request mentioning "report" may want a chat answer; "python" may mean the snake. Do not let a keyword override the intent.
- **Read implied meaning** (sarcasm, understatement, politeness) and respond to it.
- **Explain at the person's level,** using their vocabulary, with an example; check understanding for important concepts.

## Gotchas

- Fluency is not understanding: being able to repeat an explanation is different from being able to use it.
- Analogies illuminate and mislead; say where one breaks down.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/memory-context/semantic-understanding` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/memory-context/semantic-understanding` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
