---
name: supporting-others
description: "Helps the user support someone going through a hard time: what to say and not say, listening without fixing, practical help, supporting through grief, illness, breakups or stress, recognising when professional help or urgent help is needed, and looking after their own limits as a supporter. Use when the user asks how to comfort or help someone, what to say to someone grieving, sick or depressed, or is worried about a friend or family member. Also guides how Claude supports a person who is struggling."
trigger: "support a friend, partner or colleague who is struggling"
metadata:
  version: "1.0.0"
---

# Supporting others

🧬 **Core meme:** Acknowledge rather than fix, make specific offers, and keep showing up.

Help the person be there for someone who is struggling, in a way that actually helps both of them. Good output gives words to use, things to avoid, a practical offer, and a note on their own limits.

## Workflow

```
- [ ] 1. Understand the situation
- [ ] 2. Check for urgent risk
- [ ] 3. What to say
- [ ] 4. What to do
- [ ] 5. Look after the supporter
```

1. **Understand the situation.** Who, what happened, their relationship, and what the person has already tried.
2. **Check for urgent risk.** If the other person has talked about suicide or self-harm, is in danger, or is not safe, say that this needs urgent help: encourage them to stay with the person if safe, contact emergency services or a crisis line, and involve others. Asking someone directly whether they are thinking about suicide does not put the idea in their head.
3. **What to say.** Acknowledge, do not fix: "I'm so sorry. That sounds really hard." "I don't know what to say, but I'm here." Ask what would help. Avoid silver linings ("at least…"), comparisons, and "everything happens for a reason".
4. **What to do.** Specific offers beat "let me know if you need anything": "I'm dropping dinner round on Thursday; any food you don't want?" Keep showing up after the first week, when others stop. Remember anniversaries of a loss.
5. **Look after the supporter.** They cannot be someone's only support. Encourage professional help for the other person where it fits, share the load with others, and notice their own strain.

$If they are panicking or overwhelmed right now, help them settle first with `regulation-support` in cognition/communication-regulation; this member covers support over days and weeks.\n\n## Situation notes

- **Grief:** say the name of the person who died; share a memory; do not rush them.
- **Depression or anxiety:** listen, encourage professional support gently and more than once, offer to help book or go with them.
- **Illness:** follow their lead on how much they want to talk about it.
- **Breakup:** do not trash the ex (they may reunite); focus on the friend.

## On Claude's own work

When the person themselves is struggling, Claude uses the same approach: acknowledge before advising, avoid silver linings, ask what would help, point to real-world support and people in their life rather than becoming their only support, and treat any risk of harm as urgent.

**Memetic check before it's sent:** messages of support travel beyond this chat, so check them with `memetic-ethics` in cognition/communication-regulation: accurate, fair to the people involved, and clear even when quoted alone.

## Gotchas

- The supporter may be the one needing support; watch for that and respond to them.
- Do not promise confidentiality around risk to life, and do not tell them crisis services will or will not involve anyone; that varies.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents interpersonal/supporting-others` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review interpersonal/supporting-others` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
