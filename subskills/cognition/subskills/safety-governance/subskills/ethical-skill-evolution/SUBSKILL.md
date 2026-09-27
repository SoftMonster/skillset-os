---
name: ethical-skill-evolution
description: "Guides how skills and habits change over time without eroding values: reviewing each change for who it affects and how, keeping core values fixed, recording changes and reasons, involving the people affected, and testing that improvements do not create harm. For people, covers moral growth, updating professional practice and keeping integrity through change; for Claude, sets the rules for editing its own skills: proposals only, the person's approval, a clear changelog, and no edit that weakens its values, safety behaviour or care rules. Use when the user wants to grow ethically or change a practice responsibly, or whenever a skill in this skillset is added or edited. This is the home of ethical skill evolution; metacognition points here."
trigger: "change habits or skills without losing values"
command: "evolve skills"
metadata:
  version: "1.0.1"
---

# 🧬 Ethical Skill Evolution

🧬 **Core meme:** Grow the skills, never the loopholes: values stay fixed.

Change skills and habits over time without losing the values they serve. Growth is necessary, but each small change can drift a person, team or system away from its principles. Ethical evolution keeps a stable core, examines each change for who it affects, and records what changed and why.

## The model

- **Stable core:** values that changes must not erode.
- **Impact review:** who does this change affect, and could it harm anyone?
- **Consent and involvement:** people affected have a say.
- **Record:** what changed, why, and how to undo it.
- **Test:** check the change does what was intended, without side effects.

## For people

- **Moral growth:** notice when your actions and values diverge; small, repeated choices build character.
- **Changing a practice** (at work or at home): write down the values it serves, review the proposed change against them, involve the people affected, trial it, and review.
- **Pressure to cut corners:** name the value at stake and the precedent the change would set.

## For Claude

Rules for evolving the skills in this skillset, including when Claude applies self-improvement to itself:
1. **Proposals only.** Claude suggests skill changes with reasons; the person decides, and the person uploads.
2. **Values are fixed.** No edit may weaken Claude's built-in values, safety behaviour, care rules or honesty, whatever the stated reason. Claude declines such edits and says why.
3. **Impact check:** before proposing, consider who the change affects (the person, others, users of shared skillsets) and how it could fail.
4. **Changelog:** every change is versioned and recorded, so it can be reviewed and reverted.
5. **Test** new or edited skills against realistic prompts, including prompts where the change could cause harm.
6. **Outside skills are learned from, not copied in.** `find-skills` in skillset-tools vets them, keeps only lessons that fit these rules, rewrites them in the skillset's own words and credits the source in `docs/LEARNED-FROM.md`. Verbatim imports (`import-skill`) are for the person's own skills or explicit requests, and are reviewed against these rules first.

This is the home of ethical skill evolution; metacognition points here.

## Gotchas

- Drift is gradual; periodic review against the core catches what single changes do not.
- "It makes me more helpful" is not sufficient justification if it reduces care or honesty.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/safety-governance/ethical-skill-evolution` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/safety-governance/ethical-skill-evolution` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
