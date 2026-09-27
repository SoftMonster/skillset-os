---
name: emoji-list-generator
description: "Transform information into a concise, structured emoji list that maximises clarity, information density and memorability, using emojis as semantic markers rather than decoration. Use this skill whenever the user asks for an emoji list, emoji summary, information explained with emojis, a concise visual summary, a \"memetically clear\" list, or a complex topic simplified into an emoji-based structure, even if they only say something like \"summarise this with emojis\" or \"make it scannable\"."
trigger: "summarise information as a clear emoji list"
command: "list emojis"
metadata:
  version: "1.0.1"
---

# Emoji List Generator

🧬 **Core meme:** Compress the language, not the meaning.

## Purpose

Transform information into a concise, structured emoji list that maximises clarity, information density, and memorability.

The goal is **visual compression, not decoration**. Use emojis as semantic markers that help the reader rapidly identify categories, relationships, risks, actions, conclusions, or key concepts.

If the user specifies a particular audience, complexity, length, or style, follow those requirements.

## Core Principle

🧠 **One emoji = one semantic anchor.**

Each emoji should help the reader understand the meaning of the associated point. Do not add emojis merely because they look attractive.

## Workflow

### 1. Identify the information

Extract:

- 🎯 Main subject
- 🔑 Key facts
- 🔗 Important relationships
- ⚠️ Risks or exceptions
- 📊 Numbers or comparisons
- 🧭 Actions or implications
- 💡 Important insights

Discard information that does not materially contribute to the requested understanding.

### 2. Compress the information

Convert paragraphs into discrete information units. Each bullet should ideally communicate one primary idea.

Prefer:

> 🔐 Security: Keep API keys out of source code.

over:

> 🔐 Security is very important because developers should make sure that API keys and other credentials aren't accidentally included in source code where they could potentially be exposed.

### 3. Choose semantic emojis

Choose an emoji whose conventional meaning supports the text:

| Emoji | Meaning | Emoji | Meaning |
|---|---|---|---|
| 🎯 | Goal | 🔄 | Process/change |
| 🔑 | Key point | 📈 | Increase |
| 💡 | Insight | 📉 | Decrease |
| 🧠 | Concept | ✅ | Confirmed/correct |
| 📌 | Important fact | ❌ | Incorrect/problem |
| 📊 | Data/statistic | ❓ | Unknown/question |
| 💰 | Money | 🧩 | Component |
| ⚠️ | Risk | 🔗 | Relationship |
| 🚨 | Critical problem | 🚀 | Deployment/progress |
| 🔒 | Security | 🧹 | Cleanup |
| 🛠️ | Tool/work | 📚 | Documentation |
| 🧪 | Testing | 👤 | Person/user |
| 🐛 | Bug | 🏢 | Organisation |
| ⚙️ | Configuration | 🌍 | Wider context |

Use other emojis when a more precise semantic symbol exists.

### 4. Structure the list

Use a hierarchy when useful:

- 🧠 Core idea
    - 🔑 Key fact
    - 🔗 Relationship
- ⚠️ Problem
    - 🐛 Cause
    - 🛠️ Solution
- ✅ Result
    - 📈 Effect
    - 🎯 Implication

For simple subjects, use a flat list instead. Avoid excessive nesting.

## Information Density

Prefer approximately **1 emoji + 1 bold label + 1 concise explanation**:

- 🔐 **Security** — Never store API keys directly in source code.
- 🧪 **Testing** — Verify important behaviour before declaring success.
- 📦 **Dependencies** — Avoid unnecessary external packages.
- 📝 **Documentation** — Keep instructions synchronized with the actual software.

Avoid turning every sentence into a separate bullet if several sentences express the same concept.

## Compression Rules

Prefer: `💰 Cost: £70/month → £840/year.`
Avoid: `💰 Cost: The monthly cost is £70, which means that over a twelve-month period the total amount would be £840.`

Prefer: `⚠️ Risk: Steam may rate-limit repeated inventory requests.`
Avoid: `⚠️ Risk: There is a possibility that Steam could potentially apply rate limiting if inventory requests are made repeatedly over a short period of time.`

**Remove:** redundant introductions, repeated conclusions, unnecessary qualifiers, filler phrases, obvious explanations, duplicated facts.

**Preserve:** important numbers, conditions, exceptions, uncertainty, causality, distinctions, caveats.

## Accuracy Rules

Emoji compression must not change the meaning. Do not:

- exaggerate
- convert uncertainty into certainty
- remove important qualifications
- imply causation where only correlation exists
- turn an opinion into a fact
- turn an example into a general rule
- omit a critical exception merely to make the list shorter

When information is uncertain:

- ❓ **Uncertain:** Evidence is incomplete.
- 🔎 **Needs verification:** This has not been independently confirmed.

## Comparison Lists

For comparisons, use parallel structure:

- 🟢 **Option A** — £20/month; unlimited users; local storage.
- 🔵 **Option B** — £10/month; 5 users; cloud storage.
- ⚖️ **Difference** — A costs more but supports more users.

Do not assign a "winner" unless the user explicitly asks for a non-political subjective recommendation and the evidence supports one. For political or electoral topics, present factual differences without ranking or recommending options.

## Numbers

Make important numbers visually prominent:

- 💰 **Annual cost:** £840
- 📉 **Reduction:** 30%
- ⏱️ **Time limit:** 10 minutes
- 📦 **Batch size:** 2,000 items
- 🔄 **Refresh interval:** ≥4 seconds

Do not hide important quantitative information inside long prose.

## Cause → Effect

Use arrows where they increase clarity:

> 🔄 Repeated requests → 🚦 Rate limiting → ⏳ Temporary access problem

Use arrows sparingly. They should represent a meaningful relationship, not decoration.

## Process Lists

For workflows, use numbered stages combined with emojis:

1. 🔍 **Inspect** — Understand the existing system.
2. 🧩 **Prioritise** — Identify the highest-value changes.
3. 🛠️ **Modify** — Implement the changes.
4. 🧪 **Test** — Verify behaviour.
5. 📦 **Deliver** — Produce the finished artifact.

## Decision Lists

When helping someone understand a decision, separate facts from interpretation:

- 📌 **Fact:** Product A costs £50.
- 📌 **Fact:** Product B costs £35.
- ⚠️ **Trade-off:** Product A includes feature X.
- ❓ **Unknown:** Long-term reliability has not been established.
- 🧭 **Consider:** Which feature matters most to the user's requirements?

Do not disguise a recommendation as an objective fact.

## Tone

**Use:** concise language, plain English, direct statements, concrete terminology, high information density.

**Avoid:** excessive enthusiasm, marketing language, sensationalism, emoji spam, unnecessary metaphors, repetitive conclusions.

## Emoji Density

Default target: **1 meaningful emoji per bullet.** Occasionally use a second emoji when it communicates a genuine relationship or status.

Avoid: `🚀🔥💯 AMAZING! 🎯✨💪`
Prefer: `🚀 Result: Deployment completed successfully.`

## Length

- Default: **5–15 bullets**, adjusted to complexity.
- Simple concept: **3–6 bullets**.
- Complex subject: **10–20 bullets**, potentially grouped into sections.
- "Succinct" requested: favour **3–8** high-value bullets.
- "Complete" or "comprehensive" requested: retain more nuance while keeping the emoji-list format.

## Quality Test

Before returning the list, check:

- 🎯 Does every bullet add useful information?
- 🧠 Can the topic be understood by scanning only the bold labels?
- 🔗 Are relationships and causality preserved?
- 📊 Are important numbers retained?
- ⚠️ Are important caveats preserved?
- 🧹 Has redundant wording been removed?
- 🧩 Does each emoji have a semantic purpose?
- 👁️ Is the list visually scannable?
- 🧠 Does the compression preserve the original meaning?

## Output Format

Unless the user requests another format, produce:

```
🧠 [Topic]

- 🎯 **Point:** Concise explanation.
- 🔑 **Point:** Concise explanation.
- 📊 **Point:** Important quantitative information.
- ⚠️ **Risk:** Important limitation.
- 💡 **Insight:** Useful interpretation.
- 🧭 **Next step:** Practical action.
```

Do not add a lengthy introduction or conclusion.

## Accessibility

Screen readers announce every emoji by its name ("brain", "warning sign"), so a list can become noisy or misleading when read aloud.

- 🏷️ **Words carry the meaning** — the bold label and text must make sense on their own; the emoji only reinforces it.
- 🎨 **No colour-only signals** — don't rely on 🟢/🔴 alone to mean good/bad; say it in the label too.
- 🔢 **Keep counts low** — one emoji per bullet keeps the spoken version short.

## For people and for Claude

- 👤 **For people** — use the Workflow and Quality Test above as a method for writing your own scannable summaries, notes and slides.
- 🤖 **For Claude** — this is the list format for every conversational reply in the skillset, as `memetic-ethics` sets out; files, code and documents keep their own structure.
- 🔗 **Related** — `memetic-ethics` in this group uses this format for its lists.

## Final Principle

**Compress the language, not the meaning.**

The best emoji list should allow a reader to understand the essential structure of a complex subject in seconds while retaining the facts necessary to reconstruct the fuller explanation.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/communication-regulation/emoji-list-generator` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/communication-regulation/emoji-list-generator` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
