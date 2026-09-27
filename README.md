# GitHub Skillsets

A personal set of Agent Skills packaged as **one skill**, `skillset-os` (Skillset-OS), that can hold other skillsets at any depth. The repository root is the skill. You upload the whole repository to Claude as one skill, and the same zip is what goes in GitHub. The repository itself can be called `github_skillsets`; only the skill name needs hyphens.

[![Sponsor](https://img.shields.io/badge/Sponsor-Softmonster-ea4aaa?logo=githubsponsors)](https://github.com/sponsors/Softmonster)

Donationware: free under MIT, donations welcome. See [Licence and support](#licence-and-support).

> **Early access.** Skillset-OS is in early access: version 1.0.0 is being prepared but not yet released, and no GitHub release or tag exists. It works and is tested, but members, commands and file layout may still change without notice, and upgrades may need a fresh install. Feedback and issues are welcome. See [Early access](#early-access).

## How it works

A skillset is a folder with a router and a `subskills/` folder of members. Each member is one of:

| Member | Stored as |
|---|---|
| Sub-skill | `subskills/<name>/SUBSKILL.md` plus its files |
| Nested skillset | `subskills/<name>/SKILLSET.md` plus its own `subskills/` |
| Packed member | `subskills/<name>.zip`, holding a skill, a skillset or a whole repository, zips inside it included |
| Linked repository | a packed (or folder) member pinned to a GitHub commit, recorded in `skillsets.json` |

- **Routing.** Claude sees one description, generated from the top-level members' triggers. It then follows the router tables down: `SKILL.md` at the top, `SKILLSET.md` in each nested skillset. A nested skillset contributes only one trigger to its parent, so grouping keeps the description within its 1024 characters.
- **Opening members.** `scripts/skillset.py open <path>` extracts zips as needed and prints the file to read. `tree` shows everything at every depth.
- **Routing evaluation.** `tests/routing.json` holds realistic prompts and the member each should reach; `scripts/routing_eval.py` prints a blind sheet for a grader and scores the answers.
- **Tooling.** `scripts/skillset.py` does everything else: check, index, tree, open, new, new-set, bump, replace, build, rename, move, retire, pack, unpack, import, add-source, refresh, pull and package.

Members included:

| Path | What it does |
|---|---|
| `sync-skillset` | Pulls a working copy, then packages the upload zip (also the GitHub copy) and a patch |
| `skillset-tools/write-subskill` | Writes and tests a new sub-skill |
| `skillset-tools/edit-subskill` | Changes or renames a member, with versioning and re-testing |
| `skillset-tools/organise-skillsets` | Nests, moves, packs and unpacks members; shows the tree |
| `skillset-tools/find-skills` | Finds skills in registries and on GitHub and learns from them: extracts the lessons that hold up and rewrites them into every member they improve, crediting sources in `docs/LEARNED-FROM.md` |
| `skillset-tools/import-skill` | Imports skills, skillsets, repositories, collections and zips; links GitHub repositories |
| `skillset-tools/retire-subskill` | Removes a member after checking nothing depends on it |
| `software-dev` | 17 skills across the software lifecycle, with a best-practices baseline and time-boxed improvement: planning, building, debugging, testing, review, security, CI/CD and docs |
| `self-improvement` | 12 skills for personal growth: vision, goals, habits, planning, learning, reflection, decisions, career, resilience, wellbeing, money, and skill training |
| `interpersonal` | 14 skills for people skills: listening, emotional intelligence, hard conversations, conflict, boundaries, feedback, negotiation, relationships |
| `apps` | One skill with 20 mimic apps driven by short commands: archive, browse (web pages as Markdown), calc, define, drive, ed, feed, git, img, inbox, near, pdftool, pics, pkg, score, sheet, sql, translate, watch and weather, each in its own section |
| `cognition` | A brain-emulation framework of 10 groups (perception, memory, social intelligence, reasoning, executive function, action, safety and ethics, communication, human-AI augmentation, metacognition), including an emoji-list format and a memetic-ethics mode for public messages |

Every skill opens with a 🧬 core meme, its essence in one transmissible line. Memetic ethics applies throughout: humans and AI understand each other through memes, so every member keeps meaning intact, easy to pass on and fair, in succinct paragraphs or emoji lists, most replies ending with a short numbered list of suggested next steps, always within Claude's built-in values and Anthropic's guidelines.

The skillset grows by learning, not copying: other people's skills are studied with the skillset's own faculties, and their best lessons are rewritten into the members they improve (see `docs/LEARNED-FROM.md`). `import-skill` copies a skill unchanged only for your own skills or when you ask.

The personal and cognitive skillsets apply in two directions: each skill helps people strengthen a faculty, and guides Claude to apply the same faculty to its own work. Claude improves itself only by proposing skill edits that the person approves; no edit may weaken its values, safety behaviour or care rules.

## Self-memory

Skillset-OS keeps a persistent memory for the AI itself, in `memory/`. It records the AI's capabilities, skills, lessons, successes, failures, experiments, evolution, limitations, maintenance and decisions, so another AI can carry on without the one that wrote it. **It exists to improve the AI, never to accumulate knowledge about the user.**

- **Entry point:** `memory/SELF.md`, generated from the store `memory/items.jsonl`. An AI reads it first, then lists, searches and shows only what it needs.
- **Tool:** `scripts/memory.py`, with commands `add`, `review`, `approve`, `supersede`, `list`, `search`, `show`, `check`, `export`, `import` and `acceptance`.
- **How memory is made:** a conversation is evidence, not memory. A candidate becomes memory only after it passes a user-protection screen (no secrets, identifiers or facts about the person) and is approved. Capability, evolution and decision items, and replacing approved knowledge, need the person's confirmation. Approved items are never edited in place, only superseded, and status decides authority rather than recency.
- **Portable pack:** every `package` writes `memory-pack.zip`, after an acceptance test checks that a fresh AI could answer the takeover questions and that no personal dossier comes along. `memory.py import` inherits a pack.

The `skillset-tools/self-memory` member walks Claude through the process.

## Command line

Skillset-OS also works as a command line over its own skills, while plain English keeps working as usual. `scripts/shell.py` shows the skillset as a file system, with members as folders and their `SUBSKILL.md` inside. It understands bash, PowerShell and cmd spellings (`ls`/`dir`/`Get-ChildItem`, `cd`, `cat`/`type`/`more`/`Get-Content`, `grep`/`Select-String`/`findstr`, `tree`, `find`, pipes), wildcards in listings (`ls *.md`, `dir *.*`), and names without regard to case or, when only one file fits, its extension.

- **Edits are remembered, not made.** `echo > file`, `sed -i`, `rm`, `mv`, `Set-Content` and the rest are journalled and shown as if applied (`git status`, `git diff`). They are applied only when an updated repository is requested (`shell.py apply --wc <working copy>`, then package).
- **Verb-noun commands** such as `review code`, `plan feature`, `create spreadsheet`, `recall splitting`, `inventory`, `stats` and `quests` resolve to the member, built-in skill or tool that does them. `commands` generates the most useful ones from what the skillset knows. A verb the shell doesn't know gets "I don't know that command", never a guess.
- **A person's own command list** stays in the session, or in a `my-commands.md` file they keep and upload again. It is never self-memory.

- **Apps** open from their command words (`weather Staines`, `calc 2^10`, `show bbc.co.uk`), read from the command index in `apps`; `apps` lists them.

The `command-line` member walks Claude through it.

## Syncing

All changes happen in a chat with Claude:

1. Ask for the change, for example "add a skill for meeting minutes", "import this zip into the writing group", "link github.com/owner/repo", or "just give me a copy". Claude pulls a working copy of the installed skillset (or of a zip you attach), makes the change and packages it.
2. **Claude**: in Customize → Skills, remove the old `skillset-os`, upload the new `skillset-os.zip`, then start a new chat.
3. **GitHub**: replace the repository contents with the zip:

   ```bash
   cd <your-clone>
   git rm -rq .
   unzip -q <path>/skillset-os.zip -d /tmp/ss && cp -a /tmp/ss/skillset-os/. . && rm -rf /tmp/ss
   git add -A && git commit -m "skillset-os <version>" && git push
   ```

   Or apply the `.patch` Claude also provides: `git am -3 <file>.patch`.

**Building locally**: in your clone, `python3 scripts/skillset.py build` writes `skillset-os.zip` at the repository root from exactly the files git would commit (gitignored files such as `.env` stay out). The zip is gitignored and overwritten on every build; upload it in Customize → Skills.

If you change the skillset on GitHub directly, attach GitHub's zip (Code → Download ZIP) next time so Claude starts from it instead of the installed copy.

## Limits

- **Description**: 1024 characters, shared by the top-level members' triggers; the current top uses about 910, just over the warning. `check` warns at 900 and fails beyond 1024. Group members into nested skillsets to free room.
- **Files**: uploads reportedly fail above 200 files, so up to 190 files ship as they are. Beyond that, `package` still writes one upload: it zips the largest groups inside it, and `skillset.py open` unzips them with Python when a member is read (code execution must be on). The repository stays plain folders, `pull` unpacks the zips, and `PACKED.json` lets `check` confirm every zip is exact. `package --split` instead writes separate part skills plus `<name>-repo.zip`, for setups without code execution. A zip counts as one file.
- **Linked repositories** must be public; for private ones, download the zip and import it packed.
- **All or nothing**: members cannot be switched on and off one at a time in Claude.

## Development

```bash
pip install pyyaml pytest ruff
python scripts/skillset.py check
pytest
ruff check .
```

CI runs the same three commands. `.gitignore`, `.github/workflows/ci.yml` and `.github/FUNDING.yml` are generated from `scripts/templates/` (uploads may drop hidden files), so edit the templates and run `python scripts/skillset.py index`.

## Early access

Status: **early access (pre-release)**, working towards 1.0.0.

- **What works:** the whole skillset installs as one skill, routes requests to its members, and passes its checks and tests.
- **What may change:** member names, commands, triggers and folder layout, so a later upload can behave differently from this one.
- **Upgrading:** remove the old `skillset-os` skill in Claude and upload the new zip; don't rely on keeping local edits between versions.
- **Changes so far:** listed under "Unreleased" in [CHANGELOG.md](CHANGELOG.md).
- **1.0.0:** will be published as a GitHub release with the upload zip attached, and the changelog section will be dated. Until then, the version in `SKILL.md` stays 1.0.0 and means "the version being prepared".

Sponsoring is open during early access. It supports the work towards 1.0.0 and is never required.

## Editions

Every package writes two uploads from this one repository:

| Upload | Who it's for | How it behaves |
|---|---|---|
| `skillset-os.zip` | The author, and anyone who wants everything | The full personal edition: greeting menu, numbered next steps and menus, emoji lists, and at most one optional support suggestion per conversation. |
| `skillset-os-shared.zip` | Everyone else | Quiet by default: plain replies, no greeting menu, apps only on their command words (Claude's built-in tools handle plain weather, picture, place and score requests), Claude's own care guidance first, and no donation prompts in chat. |

Install only one of them. In the shared edition, say **"Skillset-OS full mode"** in a chat (or put it in your Claude preferences) to switch on the numbered lists, menus, emoji lists and greeting menu; **"Skillset-OS quiet mode"** switches back. Donation prompts stay off either way.

The repository itself is the personal edition. `editions/shared/edition.json` holds the shared edition as small, exact text patches with a reason for each. `package` applies them to a copy, regenerates the routers, checks and verifies the result, and refuses if a patch no longer matches, so the two editions can't silently drift apart. To build just the shared upload: `python scripts/skillset.py build --edition shared`.

## Disclaimers

- **No warranty.** Skillset-OS is provided "as is", without warranty of any kind, and its author accepts no liability for its use, as set out in [LICENSE](LICENSE). You use it at your own risk.
- **Not professional advice.** Its members offer general information, coaching frameworks and coding help. They are not medical, mental-health, legal, financial, tax or security advice, and they don't replace a qualified professional. Check anything important with one before relying on it.
- **In an emergency,** contact your local emergency services or a crisis line; don't rely on an AI.
- **Review before you run.** It contains scripts that Claude may run, and Claude's output can be wrong. Review code, commands and changes before you use them, especially on real systems or data.
- **Not affiliated with Anthropic.** Skillset-OS is an independent project by Andrew Wright. It is not made, endorsed or supported by Anthropic. Claude is a trademark of Anthropic, used here only to say what this skill works with.
- **Your data stays with you.** Skillset-OS collects nothing and sends nothing to its author. It runs inside your own Claude account, and any service it uses (such as Google Drive or email) is reached only through connectors you choose to enable there, under your own account and Anthropic's terms.
- **Donations buy nothing.** Sponsoring is a gift. It doesn't buy support, features, fixes, priority, a warranty or any other obligation.
- **Other people's work.** Imported members keep their own licences ([NOTICE.md](NOTICE.md)). If you believe something here infringes your rights, open an issue or a private security advisory and it will be reviewed and removed if needed.

## Licence and support

Skillset-OS is **donationware** by Andrew Wright. The tooling and the members written for this skillset are free under the MIT licence; see [LICENSE](LICENSE). Imported members keep their own licences; see [NOTICE.md](NOTICE.md).

If Skillset-OS helps you, you can support its development through [GitHub Sponsors](https://github.com/sponsors/Softmonster). Donations are voluntary and never required to use, change or share it.

When Claude uses the skillset, it may offer a support link as one numbered suggestion, at most once per conversation, never when someone is distressed and never in place of a useful next step.
