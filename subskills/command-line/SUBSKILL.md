---
name: command-line
description: "Runs Skillset-OS as a command line as well as in plain English: navigates the skills as a file system in bash, PowerShell or cmd syntax (ls, cd, cat, dir, type, Get-ChildItem, grep, tree...), remembers edits without applying them until an updated repository is requested, turns verb-noun commands like review code, plan feature or create spreadsheet into the skill, built-in skill or tool that does them, generates the most useful commands from what the skillset knows, and keeps a person's own command list only for the session or in a file they hold. Use when a message is a shell command or a short verb-noun command, when a chat opens with a greeting, \"start\" or \"I am bored\" (it offers numbered suggestions, one a review of Skillset-OS), or when asked for commands, a command list or command-line mode. Do not use for running programs on the computer; this shell never executes anything."
trigger: "use a shell (ls, cd, dir) or commands like review code; say hi, start or I am bored"
metadata:
  version: "1.1.0"
---

# Command line

🧬 **Core meme:** Type it like a shell or say it like a person; edits wait until you ask for them.

Skillset-OS answers two ways. A message that looks like a command gets a command line over its own skills. Everything else is answered in plain English, as usual. The shell is `python3 <top>/scripts/shell.py`. It keeps the working directory, history, aliases and remembered edits for this chat in `$SKILLSET_SHELL_HOME` (default `/home/claude/.skillset-shell`), and never runs programs on the computer.

## Reading a message

- **A shell command** (`ls`, `cd cognition`, `type SKILL.md`, `Get-ChildItem -Recurse`, `grep -ri meme .`, `tree -L 2`, pipes such as `cat x | head -5`, and `;` or `&&` to chain): run `shell.py run "<the command line>"` and show the output in a code block. It starts with the prompt line, so the person sees where they are.
- **A verb-noun command** ("review code", "plan feature", "negotiate salary", "create spreadsheet", "recall splitting", "inventory", "look", "go reasoning", "examine research"): run `shell.py do "<words>"`. It names the member, built-in skill or tool that does it. Then **actually do the task with that skill**, just as a plain-English request would be handled: open the member and follow it, read the built-in skill, or use the tool. Where the command is incomplete ("review code" with no code attached), ask for the missing piece.
- **Plain English:** answer normally. Don't force the shell on a conversation.
- **Mode:** `shell.py mode shell|english|auto` (default `auto`). `exit` switches to English, and any command switches back. Some verbs borrow from text adventures (`look`, `go`, `inventory`, `quests`), but replies stay plain; only when the person asks for a fantasy flavour may the wording take on role-play, and the commands stay the same.

Commands the shell understands, in bash, sh, zsh, PowerShell and cmd spellings:

- **Moving around:** `ls/dir/Get-ChildItem`, `cd/Set-Location` (with `..`, `-`, `~`, `pushd`, `popd`), `pwd`.
- **Reading and searching:** `cat/type/Get-Content/more/less/display/view`, `head`, `tail`, `Select-Object -First/-Last`, `tree`, `find -name`, `grep/Select-String/findstr` (with `-i -n -l -c -v -r`), `wc/Measure-Object`, `sort`, `uniq`, `stat`, `file`, `du`.
- **Other:** `open <member>` (its instructions), `which/Get-Command`, `man/help`, `history`, `alias`, `echo`, `env`, `whoami`, `uname`.

A member is a folder, named without the `subskills/` layer: `cd cognition/reasoning` and `cat research`, where catting a member prints its `SUBSKILL.md`. Names match without regard to case, and a file matches without its extension when only one fits, as on Windows: `more changelog` reads `CHANGELOG.md`. Wildcards work in listings (`ls *.md`, `dir *.*`, `ls cognition/m*`), and `*.*` means every entry, as in cmd. Programs such as `python`, `curl` or `sudo` are refused with a pointer to plain English.

## Apps

The `apps` sub-skill holds twenty mimic apps in one file: short commands that behave like everyday apps in the chat (`weather`, `calc`, `define`, `translate`, `sheet`, `sql`, `pdf`, `img`, `zip`, `show <url>`, `feed`, `watch`, `near`, `score`, `pkg`, `clone`, `inbox`, `drive`, `pics`, `ed`). A message that starts with an app's command word goes to that app's section: `shell.py do` names it (`→ weather  [app: apps#weather]`), and you open `apps`, read that section and the shared rules, and do the job exactly as they say. `apps` lists every app with its command words.

- **Where the words come from:** the **Command words** line under each app's heading in `apps/SUBSKILL.md` (and, for a standalone app sub-skill, its description: "Use when a message starts with `calc`…"), so a new app works as soon as its section is added.
- **Shell commands win.** `ls`, `cat`, `git status` and the rest stay with the shell. `show`, `diff` and `read` reach an app only with a URL or a number (`show bbc.co.uk`, `show 3`, `read 2`); otherwise `show changes` shows the remembered edits and `read file` is the built-in skill.
- **Apps only mimic.** They run on Claude's tools in this chat (web fetch, code execution, connectors, the weather and places tools). Nothing is installed or keeps running, and an app whose tool is missing says so rather than inventing output.

## Edits are remembered, not made

`touch`, `echo ... > file`, `>>`, `sed -i 's/a/b/'`, `rm`, `mv`, `ren`, `cp`, `mkdir`, `New-Item`, `Set-Content`, `Add-Content`, `Out-File`, `tee`, `Remove-Item`, `Move-Item` and `Copy-Item` are recorded in the journal. Nothing changes. Afterwards, `ls` marks changed files `~` and new ones `+`, and `cat` shows them as they would be.

- A screen editor (`nano`, `vim`, `code`) has no screen here. The person describes the change or pastes the content, and you record it with `shell.py edit <path> --content-file <file>`.
- `git status` lists the remembered edits, `git diff` shows them, and `git restore <file>` or `git reset` forgets them. `git commit` explains how to apply them.
- **Applying them happens only when the person asks for an updated repository** ("save changes", "build the updated repository"):
  1. Pull a working copy with `sync-skillset`.
  2. Run `shell.py apply --wc <working copy>`.
  3. Follow the usual edit rules (index, check, bumps when released) and package.
  
  Self-memory candidates remembered with `remember <type> <summary>` are added at the same time and still need review and approval through `skillset-tools/self-memory`.

## Verb-noun commands

`commands` (or `shell.py commands --top 20`) lists the most useful commands, `commands all` (`--all`) lists every one, and `review commands` audits this skill and its list. They are generated each time from what the skillset knows about itself:

- **Its own members:** `review code` → `software-dev/code-review`, `resolve conflict`, `build habit`, `find skills`.
- **Built-in skills installed in this environment:** `create spreadsheet`, `create presentation`, `read pdf`.
- **The model's tools:** `search web`, `summarise text`, `make chart`, which work when the chat has them.
- **The shell's own verbs:**
  - `look`, `map`, `inventory`, `examine`, `go`;
  - `stats` (self-memory in numbers and the latest exam) and `quests` (open maintenance items);
  - `recall <topic>`, `remember <type> <summary>`;
  - `save changes`, `show changes`, `run exam`.

The ranking uses the routing fixture (what realistic requests ask for) and self-memory evidence, so it improves as the skillset does. Synonyms are understood (`check`, `audit` → `review`; `fix` → `debug`; `make`, `build` → `create`; `x` → `examine`; `i` → `inventory`). When two commands fit almost equally, the shell shows a numbered menu of them (plus "something else") instead of guessing: show it to the person, and the next bare number or `first`/`last` picks that command. An unknown command with a near-miss name gets a numbered "did you mean" menu the same way. A greeting or "I am bored" (`hi`, `start`, `menu`) opens with numbered suggestions: explore (`look`), `apps`, train a skill, and `review skillset` (audit Skillset-OS for issues, version and pending edits). A word phone autocorrect likes to swap in (`is` for `ls`, `so` for `os`) gets a menu with the repaired reading first and the literal one second, unless both readings land in the same place. A bare number with no open menu is never guessed at. Every menu also offers `0. infer`: the person hands the choice back, so Claude answers its own question with the likeliest option, says in one line which it chose and why, and carries on; the menu stays open so a number still overrides. `0`, "infer", "you decide" and "your call" all pick it. Otherwise a menu answers once and expires when anything else is typed.

## The person's own command list

A list of someone's favourite commands is **information about them**, so it never goes into self-memory. Offer these ways to keep it, and let them choose:

1. **This session only:** `favourites add <command>`, `favourites list`, `favourites remove`. It is forgotten when the chat ends.
2. **A file they keep:** the person types `save favourites` and you run `shell.py favourites save`, which writes `my-commands.md` to the outputs for them to download. Later they upload it and type `load favourites` (or say "load my commands"), and you run `shell.py favourites load <file>`. In chat the verb comes first; the script's subcommand puts it second. Recall is then exactly their list, held by them.
3. **claude.ai's own memory,** if they switch it on in Settings. That is a user-controlled feature of the app, separate from Skillset-OS.

If they ask Skillset-OS to "just remember" their list permanently, explain why it doesn't, and offer option 2. What the AI may remember is about itself, for example "verb-noun commands that name the noun resolve best", through the self-memory pipeline.

## Gotchas

- `shell.py` reads the installed skill through `skillset.py`, so zipped groups in a large upload open transparently. That needs code execution; without it, answer the command in words from what you can read.
- Keep command output honest: show what `shell.py` printed. Don't invent listings or file contents.
- A command that is also an English word (`find`, `type`, `open`, `more`, `display`, `view`) is run as a shell command when its argument is a path, and as a verb-noun command otherwise ("find skills" → `skillset-tools/find-skills`). Member names count as paths, so `open research` opens the member; `open a pull request` is a verb-noun command.
- An unknown verb is never guessed: unless the noun alone strongly matches a command, the shell says it doesn't know the command rather than picking the nearest one.
- Known gaps, for a later release: generated names pair a verb with the member's folder name and can read awkwardly (`set goal-setting`, `plan and-prioritise`), about 45 fall back to a generic `use`, and `use command-line` ranks in the top 20 although it names the shell itself. Hand-picked verbs in each member's front matter would fix all three.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents command-line` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review command-line` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
