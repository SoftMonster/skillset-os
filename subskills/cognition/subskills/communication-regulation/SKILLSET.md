---
name: communication-regulation
description: "Faculties of speaking and steadying others: clear communication, de-escalation, third-party conflict mediation and regulation support, plus the emoji-list format and the memetic-ethics mode for memes, slogans and public messages (transparency lives in safety-governance). Use when the user or Claude must explain clearly, calm a heated situation, mediate between others, help someone who is distressed, or write an emoji list, meme or public message."
trigger: "communicate clearly, calm a heated situation, mediate between people or help someone settle their emotions, or write emoji lists, memes and public messages"
metadata:
  version: "1.0.1"
---

# Communication regulation

A nested skillset. Pick the member whose "Use when" matches the request and read its instructions; for a nested skillset or a zip, run `python3 <top>/scripts/skillset.py open <path>` to get the file to read.

These are the faculties of speaking and of steadying others: communicating clearly, de-escalating, mediating and supporting someone who is distressed. Each member has a "For people" and a "For Claude" half.

`emoji-list-generator` and `memetic-ethics` were imported from the person's own collection; they are communication formats and a communication mode, so they live here.

**📝 Transparency** belongs to this group but lives in safety-governance (`cognition/safety-governance/transparency`), so there is one copy. Open it from there.

For the user's own relationships and conversations, use the practical members of `interpersonal`; these members cover the underlying faculty and the third-party role. Where someone may be at risk, their safety comes before any technique.

## Members

<!-- subskills:start -->
| Member | Kind | Version | Use when |
|---|---|---|---|
| [communication](subskills/communication/SUBSKILL.md) | skill | 1.0.2 | Builds clear communication: knowing the audience and purpose, leading with the point, structuring for easy reading or listening, plain language, the right level of detail and checking understanding. For people, covers writing emails, messages, reports and explanations, speaking and presenting, and explaining complex things simply; for Claude, covers answering first, matching length and depth to the question, using formatting only where it helps, avoiding jargon the person may not know, and a warm, direct tone. Use when the user wants to write or speak more clearly, structure a message, explain something complex or present, or whenever Claude writes a response. For what to say in a hard personal conversation, use difficult-conversations in interpersonal. |
| [conflict-mediation](subskills/conflict-mediation/SUBSKILL.md) | skill | 1.0.0 | Guides neutral third-party mediation: preparing the parties, setting ground rules, letting each side be heard, reframing positions into interests, generating options together and recording agreements, while staying impartial. For people, covers mediating between colleagues, team members, friends, family members or children; for Claude, covers helping several people who disagree in a shared conversation or channel, staying even-handed and focusing on the shared problem. Use when the user is asked to mediate or is caught between others in conflict, or when Claude is working with several people who disagree. For the user's own conflicts, use conflict-resolution in interpersonal. |
| [de-escalation](subskills/de-escalation/SUBSKILL.md) | skill | 1.0.0 | Calms heated situations: stays calm and safe, listens and acknowledges feelings, lowers intensity with voice, pace and words, finds what can be agreed, offers choices and knows when to step away or get help. For people, covers angry customers, family arguments, road rage, public confrontations and tense meetings; for Claude, covers responding to frustrated, angry or abusive messages without mirroring the heat, becoming defensive or becoming submissive, and keeping the conversation constructive. Use when the user must handle an angry or aggressive person, a situation is getting heated, or when the person talking to Claude is upset with it. |
| [emoji-list-generator](subskills/emoji-list-generator/SUBSKILL.md) | skill | 1.0.1 | Transform information into a concise, structured emoji list that maximises clarity, information density and memorability, using emojis as semantic markers rather than decoration. Use this skill whenever the user asks for an emoji list, emoji summary, information explained with emojis, a concise visual summary, a "memetically clear" list, or a complex topic simplified into an emoji-based structure, even if they only say something like "summarise this with emojis" or "make it scannable". |
| [memetic-ethics](subskills/memetic-ethics/SUBSKILL.md) | skill | 1.0.4 | Memetic ethics, applied throughout the skillset: humans and AI communicate through memes (units of meaning that travel), so every reply keeps meme fidelity (meaning preserved), easy transmission (short, plain, one idea at a time) and ethics (accurate, fair to people, informing rather than inflaming), passes a memetic check, and follows a shared reply format, always within Claude's built-in values and Anthropic's guidelines. Also produces memes, ethical statements, slogans and other public messages. Use for every reply made with this skillset, and whenever the user asks for memes, captions, slogans, taglines, viral posts, values statements, codes of conduct, public messaging or campaign copy, wants to analyse how an idea or narrative affects people, invokes Memetic-Ethics mode, or asks for replies that end with numbered next-step suggestions or with Pushback or redirect? |
| [regulation-support](subskills/regulation-support/SUBSKILL.md) | skill | 1.0.0 | Helps a distressed person settle: stays calm to lend calm, validates without amplifying, uses simple grounding and paced breathing, reduces demands, and moves to problem-solving only once they are steadier, while recognising when urgent help is needed. For people, covers supporting a friend, child, partner or colleague through panic, overwhelm, anger or tears; for Claude, covers responding to a person who is distressed in the conversation with steadiness, gentle grounding and care, never suggesting techniques that use pain or mimic self-harm, and pointing to real support when needed. Use when the user wants to help someone who is upset or panicking, or when the person talking to Claude is distressed. |
<!-- subskills:end -->

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/communication-regulation` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/communication-regulation` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
