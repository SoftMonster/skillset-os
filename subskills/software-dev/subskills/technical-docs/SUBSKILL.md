---
name: technical-docs
description: "Writes developer documentation that matches the code: READMEs with quick start, docstrings and comments that explain why, architecture overviews with diagrams, runbooks, contribution guides and changelogs. Use when the user asks to document code, write or improve a README, add docstrings or comments, explain setup, or write a runbook, onboarding or architecture doc for a repository. Do not use for commit or PR text; use git-workflow."
trigger: "write a README, docstrings, code comments, a runbook or developer docs"
metadata:
  version: "1.0.0"
---

# Technical docs

🧬 **Core meme:** Docs that match the code, starting with how to run it.

Write documentation that gets its reader to their goal quickly and stays true to the code. Know the reader (new user, contributor, operator at 3 a.m.) and cut everything they do not need. Every command and code sample must be one you have run or checked against the code.

## Workflow

1. **Identify the doc type and reader** from the table below.
2. **Gather facts from the code, not memory**: run `codebase-orientation` for commands and layout, and read the functions you document. Run the quick-start commands in the sandbox when possible.
3. **Write** using the matching template. Lead with the task, keep sentences short, use code blocks for anything the reader types.
4. **Check**: every command runs, every link resolves, every name matches the code, and nothing duplicates what another doc already says (link to it instead).
5. **Deliver.** Docstrings and comments go into the code files; READMEs and runbooks go into the repository as Markdown. Offer a Claude Doc only if the person wants a shared, editable page outside the repository.

| Doc | Reader | Must answer |
|---|---|---|
| README | someone deciding whether and how to use it | what it is, quick start, common usage, where to go next |
| Docstrings | a caller | what it does, parameters, return value, errors raised, one example for non-obvious APIs |
| Comments | a future maintainer | why the code is this way (constraints, trade-offs, bug references), never what it does |
| Architecture overview | a new contributor | components, how they talk, where data lives, key decisions (link ADRs) |
| Runbook | an on-call engineer under stress | symptoms, checks, fixes, escalation, as copy-paste commands |
| CONTRIBUTING | a contributor | setup, tests, style, PR process |

## README template

````markdown
# name
One sentence on what it does and for whom.

## Quick start
```bash
<install>
<smallest useful run>
```
## Usage
The two or three most common tasks, each with a runnable example.
## Configuration
Table: variable, default, meaning.
## Development
Setup, test, lint commands. Link CONTRIBUTING.
## Licence
````

## Docstring style

Follow the style the codebase uses. If there is none: Google style for Python, JSDoc/TSDoc for JavaScript and TypeScript, standard Go doc comments starting with the name, and `///` with `# Examples` in Rust.

```python
def retry(fn: Callable[[], T], attempts: int = 3, backoff: float = 0.5) -> T:
    """Call ``fn`` until it succeeds, sleeping with exponential backoff between tries.

    Args:
        fn: Zero-argument callable to invoke.
        attempts: Maximum number of calls, including the first. Must be >= 1.
        backoff: Seconds to wait after the first failure; doubles after each failure.

    Returns:
        Whatever ``fn`` returns on its first success.

    Raises:
        ValueError: If ``attempts`` is less than 1.
        Exception: The last exception from ``fn`` if every attempt fails.
    """
```

## Runbook entry template

```markdown
### Alert: <name>
**Means:** what is broken, in one line. **Impact:** who notices.
**Check:** 1. `<command>` → expect … 2. dashboard link …
**Fix:** numbered, copy-paste steps, safest first.
**Escalate:** who and when.
```

**Memetic check before it's sent:** READMEs, runbooks and developer docs travel beyond this chat, so check them with `memetic-ethics` in cognition/communication-regulation: accurate, fair to the people involved, and clear even when quoted alone.

## Gotchas

- Docs rot where they repeat the code. Document intent and contracts; let signatures and types carry the details.
- Diagrams should be text (Mermaid) so they are reviewed and updated with the code.
- Avoid "simply" and "just"; they hide steps and discourage readers who get stuck.
- Commit messages, PR descriptions and changelogs belong to `git-workflow`.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents software-dev/technical-docs` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review software-dev/technical-docs` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
