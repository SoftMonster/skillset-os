---
name: sync-skillset
description: "Gets a working copy of the skillset (from the installed skill, an attached zip or an earlier step in this chat), and at the end packages it: versions it, runs the checks and tests, commits, and writes the one zip that is both the upload for Claude and the copy for GitHub, plus a patch. Use first for any change to the skillset, and on its own to download it, sync it with GitHub, refresh linked repositories or check which version is installed."
trigger: "download, sync or update the skillset or copy it to GitHub"
metadata:
  version: "1.3.0"
---

# Sync skillset

🧬 **Core meme:** Pull once, change the copy, package once, and hand over the steps.

Every change follows the same loop. Pull a working copy, change it using another sub-skill, then package it. The person uploads the zip to Claude and puts the same zip in GitHub. This sub-skill owns the first and last steps.

`<top>` is the installed skillset folder (the one holding the top `SKILL.md`). The working copy is `/home/claude/skillset-os` unless the skillset has another name. `<wc>` means the working copy.

## Rules

- **Never edit the installed folder.** It is read-only and resets each session. Work on the working copy.
- **One working copy per chat.** Pull once, make every change there, and package at the end. Each package covers everything since the pull.
- **The newest copy wins.** If the person attaches a zip and an installed copy also exists, `pull` reports both versions; start from the newer one. If they differ at the same version, ask which is current.
- **Every change raises a version.** `package` raises the top version and every changed nested skillset automatically. Changed sub-skills must be bumped with `skillset.py bump`; the editing sub-skills do this.
- **The source is the personal edition; editions flow from it, fixes flow back to it.** A copy built as an edition (the shared plugin, its repository, a shared zip) says so in `SKILL.md` (`metadata.edition`), and `pull` and `package` both say it too. Every fix made in such a copy goes back with `upstream` (step 2a) in the same chat, every time, and the source is packaged, which rebuilds the edition. Never copy an edition build over the source repository: it would erase the personal wording.
- **Claude cannot upload or push.** The person uploads the zip and updates GitHub; give them the exact steps.

## 1. Get a working copy

Pick the first that applies:

- **Already pulled in this chat**: keep using it.
- **The person attached a skillset zip** (from GitHub or an earlier package): `python3 <top>/scripts/skillset.py pull --source /mnt/user-data/uploads/<file>.zip`. If the skillset is not installed yet, extract the zip and run the `skillset.py` inside it.
- **Otherwise**, pull the installed copy: `python3 <top>/scripts/skillset.py pull`

`pull` copies the skillset to `/home/claude/<name>`, restores the dotfiles, commits a baseline and tags it `synced`. It also lists other installed copies and whether they are newer. Then install the checking tools:

```bash
pip install pyyaml pytest ruff --break-system-packages -q
```

From here on, run the working copy's own script: `python3 <wc>/scripts/skillset.py ...`. Use `tree` to see every member at every depth.

## 2. Make the change

First read `<wc>/memory/SELF.md`, the AI's self-memory: lessons, successes, failures, limitations and open maintenance for this skillset. When the change is done, record any genuinely new self-knowledge through `skillset-tools/self-memory` (candidate, screen, approve), and supersede what it replaces. It is knowledge, not a log.

Read and follow the matching member of the `skillset-tools` skillset (open it with `python3 <wc>/scripts/skillset.py open skillset-tools/<name>`): `write-subskill` (new), `edit-subskill` (change, rename), `organise-skillsets` (nest, move, pack, unpack), `import-skill` (bring in skills, skillsets, repositories or zips, or link GitHub repositories) or `retire-subskill` (remove).

To update linked GitHub repositories, run `python3 <wc>/scripts/skillset.py refresh` (or give member paths to refresh only some). For a plain download or a GitHub sync with no change, skip to step 3.

## 2a. Fixes made in the shared edition go upstream

Whenever the working copy is an edition copy, or the person brings fixes from one (a changed plugin repository, a shared zip they edited, a contributor's pull request), finish the change by carrying it into the source:

1. Get the source working copy too: pull the personal zip or repository into its own folder, for example `pull --source <personal>.zip --dest /home/claude/<name>-source`.
2. From the edition copy, run `python3 <source wc>/scripts/skillset.py --root <edition wc> upstream --into <source wc>`. The base is the edition as it was before the fixes: the `synced` tag of a pulled copy, or `--base <ref, folder or zip>` for a repository or zip.
3. It turns both trees back into source wording by reversing the edition's patches, diffs them and applies the diff to the source. The personal wording, `editions/` and the absence of `.claude-plugin/` are untouched.
4. A **note** means an edit touched edition-only wording: if wanted, change that patch's new text in `editions/<edition>/edition.json`. A **CONFLICT** leaves a `.rej` file to merge by hand, then delete.
5. Review `git diff` in the source, bump what changed, and package the source (step 3). Hand over both downloads; the edition is rebuilt from the source.

When the person works in the personal source and has a shared copy with unmerged fixes, bring those in first, so the next package does not overwrite them.

## 3. Package

```bash
python3 <wc>/scripts/skillset.py package --message "<what changed, in a few words>" [--bump minor]
```

It regenerates every router and every member's "This folder" section, then checks everything at every depth, including inside zips and the 1024-character description. It runs ruff and pytest, raises the versions and releases the changelog section. Until the first release (a changelog with only `## Unreleased`), the skillset is pre-release: nothing is bumped, changes collect under `## Unreleased`, and the version stays where it started. Only when the person says to release, run `package --release`, after sweeping every file for status text the release makes false ("early access", "not yet released") and rewriting it; it ships that version as it is (a fresh `1.0.0` ships as 1.0.0). Every package also writes `memory-pack.zip`, the AI's self-memory, after checking that a fresh AI could take over from it. Then it commits and writes to `/mnt/user-data/outputs/`:

- `<name>.zip`: the upload for Claude and the copy for GitHub (one top-level `<name>/` folder).
- **When the skillset has more than 190 files**, `package` splits the upload into separate part skills, each a plain folder (`<name>-<folder>.zip`, with a generated `SKILL.md` and a shared `PARTS.json`), plus `<name>-repo.zip` for GitHub. It never zips groups by default, because Claude's skill system cannot load anything inside a zip. `package --pack-groups` keeps one upload with zipped groups and `PACKED.json` for setups that knowingly rely on code execution (`skillset.py open` unzips them). Editions, and so the plugin, are refused over the limit rather than zipped.
- **The release gate:** before delivering, `package` unpacks the zips it wrote (and any zipped groups inside them), puts them back together and refuses unless the result is exactly the working copy and passes `check`.
- `<name>-<version>.patch`: every commit since the pull, for people who prefer `git am`.
- The edition with a `plugin.json` (for example `editions/shared/plugin.json`) is the Claude plugin: its `<name>-<edition>.zip` carries `.claude-plugin/plugin.json` and `marketplace.json`, generated from `SKILL.md`. One download serves as the plugin upload (Customize → Plugins → Add → Upload plugin) and the plugin repository. It is not a skill upload: the Skills page rejects any zip holding a plugin manifest.
- `<name>-<edition>.zip` for each edition in `editions/` (for example `<name>-shared.zip`): the same skillset with that edition's patches applied, checked and verified. It is a separate upload for other people, never installed alongside `<name>.zip`, and not the GitHub copy; offer it as a release asset.

It stops at the first problem and says how to fix it. Use `--bump minor` for new members or new behaviour, `--bump major` for renames or removals; the default is patch. Share the files with `present_files`, zip first.

## 4. Hand over

Keep it short: the new version, what changed, and these steps. When the upload was split, say how many skills to upload, and that **`<name>-repo.zip` is the file to review, share or archive**: `<name>.zip` alone is incomplete by design.

**Claude**: in Customize → Skills, remove the old `<name>` skill (and any old `<name>-…` parts), then upload `<name>.zip` (the personal edition; the shared edition's zip goes to Customize → Plugins → Add → Upload plugin instead, after removing any old copy there) (and, when the upload was split, every `<name>-<folder>.zip` too). Start a new chat to use it. If standalone skills were imported, delete or switch off their old copies so they do not trigger twice. If they edit their own clone later, `python3 scripts/skillset.py build` there makes the same upload zip from exactly what git would commit, as `<name>.zip` at the repository root (gitignored, overwritten each time).

**GitHub** (the repository may be named differently from the skill, for example `github_skillsets`):

```bash
# Replace the repository contents with the zip (handles deleted files too)
cd <your-clone>
git rm -rq .
unzip -q <path>/<name>.zip -d /tmp/ss && cp -a /tmp/ss/<name>/. . && rm -rf /tmp/ss   # split upload: use <name>-repo.zip
git add -A && git commit -m "<name> <version>" && git push
```

```bash
# Or apply the patch
cd <your-clone> && git am -3 <path>/<name>-<version>.patch && git push
```

The patch only applies if the clone matches what was pulled. If it fails, use the zip.

**Plugin** (when an edition has a `plugin.json`): in the plugin's own repository (for example `skillset-os-plugin`), replace the contents with those of `<name>-<edition>.zip`'s `<name>/` folder, using the same steps. To list it in the Claude directory, submit that repository through Anthropic's directory submission portal; Claude cannot submit it. Tell the person to install the plugin or an upload, not both.

## Gotchas

- If the person edited the skillset on GitHub and did not upload it, the installed copy is stale. Ask them to attach the GitHub zip (Code → Download ZIP) and pull from that.
- Uploads may drop hidden files. `pull` and `index` rebuild `.gitignore` and `.github/workflows/ci.yml` from `scripts/templates/`, so edit the templates, not the dotfiles.
- The top description is built from the triggers of the top-level members only. If `check` says it is near the 1024-character limit, group related members into a nested skillset with `organise-skillsets`: the group contributes one trigger.
- `refresh` needs github.com; the GitHub API is not used, so its rate limits do not apply.
- `package` runs the whole test suite in one tool call, which is capped at about 300 seconds. If the suite nears that, run the tests in parts first (`pytest tests/test_structure.py`, then the rest), then `package --skip-tests` only once every part has passed.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents sync-skillset` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review sync-skillset` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
