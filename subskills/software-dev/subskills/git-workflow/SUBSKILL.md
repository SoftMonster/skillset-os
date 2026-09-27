---
name: git-workflow
description: "Handles version control work: writes Conventional Commit messages and pull request descriptions, plans branches and releases, resolves merge conflicts, and recovers from git mistakes (bad rebase, lost commits, wrong branch, secrets committed). Use when the user asks for a commit message, PR or MR description, changelog, release notes, branching strategy, help with a merge conflict, rebase, cherry-pick, reset or revert, or says git is in a bad state."
trigger: "write commit messages or PR descriptions, or fix git problems"
metadata:
  version: "1.0.0"
---

# Git workflow

🧬 **Core meme:** Small, focused commits with messages that say why.

Keep history readable and recoverable: commits that say why, PR descriptions reviewers can act on, and calm, safe recovery when git goes wrong. When recovering, never run a command that can destroy work without first making a backup ref.

## Commit messages

Follow Conventional Commits unless the repository clearly uses another style (check `git log --oneline -20`).

```
<type>(<optional scope>): <imperative summary, ≤ 72 chars, no full stop>

<body: what changed and why, wrapped at 72; not how — the diff shows how>

<footer: BREAKING CHANGE: …, Closes #123, Co-authored-by: …>
```

Types: `feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`. If a diff mixes unrelated changes, suggest splitting it (`git add -p`) and give one message per part.

Example:

```
fix(auth): reject expired refresh tokens

Refresh tokens were checked for signature but not expiry, so a leaked
token stayed valid forever. Check `exp` and return 401 with a
`token_expired` error code so clients can force a re-login.

Closes #482
```

## Pull request description

```markdown
## What
One or two sentences.
## Why
The problem or ticket, with a link.
## How
Key decisions and anything surprising; point reviewers at the files that matter.
## Testing
What was run and what was checked manually. Screenshots for UI.
## Risk and rollout
Migrations, flags, backward compatibility, how to roll back.
```

Release notes and changelogs follow Keep a Changelog (Added, Changed, Deprecated, Removed, Fixed, Security), written for users, not developers.

## Branching

Default to trunk-based development: short-lived branches off `main` (`feat/…`, `fix/…`), merged within a day or two, behind feature flags when incomplete. Use squash merges for small PRs and rebase merges to keep meaningful commits. Recommend release branches only for products that support several versions at once.

## Merge conflicts

1. `git status` to list conflicted files, then read both sides and the base (`git config merge.conflictstyle zdiff3` shows it).
2. Understand the intent of each side before editing; the right answer is often a combination, not a pick.
3. Resolve, remove every marker (`git diff --check`), then run the tests before `git add` and continuing.

## Recovery

Always start with a safety net: `git branch backup/$(date +%s)`. Then:

| Situation | Fix |
|---|---|
| Committed to the wrong branch | `git branch correct-branch` then `git reset --hard HEAD~N` on the wrong one (after backup) |
| Lost commits after reset or rebase | `git reflog`, find the SHA, `git branch rescue <sha>` |
| Bad rebase in progress | `git rebase --abort` |
| Undo a pushed commit on a shared branch | `git revert <sha>`, never rewrite shared history |
| Fix the last commit message (not pushed) | `git commit --amend` |
| Secret committed | Rotate the secret first. Then remove it from history with `git filter-repo` and force-push only after coordinating with the team |
| Detached HEAD with work | `git switch -c save-work` |

**Memetic check before it's sent:** commit messages, PR descriptions and release notes travel beyond this chat, so check them with `memetic-ethics` in cognition/communication-regulation: accurate, fair to the people involved, and clear even when quoted alone.

## Gotchas

- `git push --force` on a shared branch destroys other people's work. Use `--force-with-lease`, and only on your own branches.
- `git reset --hard` and `git clean -fd` delete uncommitted work permanently; the reflog does not help with files that were never committed. Suggest `git stash -u` first.
- Line-ending noise across Windows and Unix: add a `.gitattributes` with `* text=auto`.
- Large binaries belong in Git LFS or outside the repository.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents software-dev/git-workflow` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review software-dev/git-workflow` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
