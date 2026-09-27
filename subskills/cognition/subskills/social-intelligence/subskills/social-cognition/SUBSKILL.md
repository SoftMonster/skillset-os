---
name: social-cognition
description: "Builds theory of mind: modelling what another person knows, believes, wants and can see, taking their perspective, explaining behaviour without the usual attribution errors, and understanding group dynamics and social influence. For people, covers understanding why others act as they do and seeing a situation from their side; for Claude, covers modelling what the person knows and can see, writing for their actual level and avoiding projecting its own knowledge onto them. Use when the user is puzzled by someone's behaviour, wants to see another point of view, or asks about group dynamics, or when Claude must judge what the person already knows."
trigger: "understand what others think, know or believe, or how groups behave"
command: "read people"
metadata:
  version: "1.1.0"
---

# 🫂 Social Cognition

🧬 **Core meme:** Others know, see and want different things from you, so model that.

Model other minds: what someone knows, believes, wants and can see, and why they act as they do. The brain runs these models constantly ("theory of mind"), but it defaults to assuming others know what we know and to blaming character for what circumstances caused. Good social cognition corrects for both.

## The model

- **Theory of mind:** others have their own knowledge, beliefs and goals, which may differ from ours and from reality.
- **Curse of knowledge:** once we know something, we struggle to imagine not knowing it.
- **Attribution errors:** we explain others' behaviour by character ("lazy") and our own by circumstance ("busy").
- **Group dynamics:** conformity, in-group favouritism, roles and status shape behaviour as much as personality does.

## For people

```
- [ ] 1. Describe the behaviour
- [ ] 2. Model their view
- [ ] 3. Find situational explanations
- [ ] 4. Check
```

1. **Describe the behaviour** plainly: what they did and said, not what it "shows".
2. **Model their view:** what do they know that I do not, and the reverse? What are they trying to achieve? What might they be worried about?
3. **Find situational explanations:** before concluding "they are X", list two circumstances that could produce the same behaviour.
4. **Check** by asking, observing more, or testing a small step.

For groups: notice who speaks and who defers, what the unspoken norms are, and whether agreement is real or conformity. Asking quieter people directly, or collecting views before discussion, surfaces what the group actually thinks.

## For Claude

- **Model what the person knows:** their expertise, what they have already said and tried, what they can see (they cannot see files that were not presented, or Claude's working steps unless shown).
- **Beat the curse of knowledge:** define terms a newcomer would not know, skip what an expert obviously knows, and do not assume they followed a long chain of reasoning.
- **Model third parties fairly:** when the person describes someone else, treat that as one view and avoid attributing motives from thin evidence.
- **Do not project:** Claude's preferences are not the person's; ask or infer from what they said.

## Gotchas

- Perspective-taking is imagination, not knowledge; confirm with the real person when it matters.
- Understanding someone's view is not agreeing with it or excusing harm.
- For practical conversations about a relationship, use the interpersonal skillset.

## Commands

- 🧠 **Others see and want differently** · `read people`: Understands what others think, know or believe, or how groups behave.
  - 👓 `see their view`: Models another person's view of a situation from what they know and want.
  - 🧩 `explain behaviour`: Offers situational explanations for someone's behaviour before character judgements.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/social-intelligence/social-cognition` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/social-intelligence/social-cognition` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
