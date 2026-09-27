---
name: publish-plugin
description: "Publishes the skillset as a Claude plugin and lists it in the Claude directory: checks the current directory rules, builds the shared edition (which doubles as the plugin), validates it with Claude Code's own validator, test-installs it, sets up the plugin repository, cuts the release and hands over the submission steps. Use when the user wants to share, publish, release or submit the skillset as a plugin or to the Claude directory or a marketplace. Do not use for building an upload only (sync-skillset) or for plugins of unrelated projects."
trigger: "publish, release or submit the skillset as a Claude plugin"
command: "publish plugin"
metadata:
  version: "1.2.0"
---

# Publish plugin

🧬 **Core meme:** One zip, checked by the platform's own tools, is both the upload and the plugin.

Ship Skillset-OS as a Claude plugin that people can install and that Anthropic can list in the Claude directory. The shared edition is the plugin: `package` writes `<name>-shared.zip` with `.claude-plugin/plugin.json` and `marketplace.json` inside, so one download is both the plugin upload (Customize → Plugins → Add → Upload plugin) and the plugin repository. It is not a skill upload: the Skills page rejects any zip holding a plugin manifest. Never make a second, near-identical download for the same people.

## Workflow

```
- [ ] 1. Check the current rules
- [ ] 2. Working copy (sync-skillset, step 1)
- [ ] 3. Manifest fields
- [ ] 4. Sweep before release
- [ ] 5. Package and validate
- [ ] 6. Test-install
- [ ] 7. Hand over
```

### 1. Check the current rules

Search Anthropic's docs before answering, because plugin and directory rules change: at the time of writing the directory takes plugins (MCP connectors, skills or both, from a GitHub repository) through a submission portal on paid plans, not standalone skills. Report what the docs say now, with links, and whatever has changed.

### 2–3. Working copy and manifest fields

`editions/shared/plugin.json` holds everything except the name and version, which always come from `SKILL.md` so they cannot drift. Keep `homepage` a full URL (a bad one stops the plugin loading) and point `homepage` and `repository` at the plugin's own repository. Declare no components: a root `SKILL.md` with no `skills/` folder loads as one skill, and the build refuses `skills`, `version` or other component keys in the spec, a top-level `bin/` (claude.ai and Cowork refuse those) and a stored `.claude-plugin/`.

### 4. Sweep before release

A listing should point at a release. Before `package --release`, search every file for status text the release makes false ("early access", "pre-release", "not yet released", "being prepared") and rewrite it, in the top `SKILL.md` too, since Claude answers stability questions from it. Release only when the person says so.

### 5. Package and validate

```bash
python3 <wc>/scripts/skillset.py package --release --message "<what changed>"   # or without --release
npm i -g @anthropic-ai/claude-code                                              # the registry is reachable
mkdir -p /tmp/v && cd /tmp/v && unzip -oq /mnt/user-data/outputs/<name>-shared.zip
claude plugin validate --strict <name>/.claude-plugin/plugin.json
claude plugin validate --strict <name>/.claude-plugin/marketplace.json
```

The platform's own validator is the authority; our checks only guard what it does not see. The tests prove the zip is the shared edition byte for byte plus the two manifest files, and that it still passes `check` when installed as a skill.

### 6. Test-install

```bash
export HOME=/tmp/ptest && claude plugin marketplace add /tmp/v/<name> && claude plugin install <name>@<name> && claude plugin list
```

It should show the plugin enabled at the released version. A throwaway `HOME` keeps the sandbox clean.

### 7. Hand over

Claude cannot push, tag or submit; give the person the steps:

1. Create the plugin's own repository (for example `<name>-plugin`); the main repository stays the personal edition.
2. Put the contents of the zip's `<name>/` folder at its root and push.
3. On GitHub, create a release tagged `v<version>` in both repositories, attaching the uploads to the main one.
4. Submit the plugin repository through Anthropic's directory submission portal.
5. To use it on claude.ai before the listing, upload the zip at Customize → Plugins → Add → Upload plugin. Install the plugin or the personal upload, not both, or the skill triggers twice.

## Changes made in the plugin repository

Fixes and contributions to the plugin repository are edits to the shared edition. Carry them into the personal source with `upstream` (see `sync-skillset`, step 2a), package the source, and push the rebuilt plugin; never edit the plugin repository and leave the source behind.

## Gotchas

- `git tag` fails in the sandbox without an identity. Leave tags to the GitHub release, or pass `-c user.name=... -c user.email=...` for a local-only tag.
- A skill cannot contain a plugin manifest: the Skills page rejects any zip with `.claude-plugin/plugin.json`. A plugin zip goes to Customize → Plugins, with the manifest at `.claude-plugin/plugin.json` inside at most one top folder and nothing beside that folder.
- Test each install route in the real product before promising it works; the validator checks the manifest, not what each uploader accepts.
- Over 190 files, editions are refused rather than zipped, because Claude cannot load a zip as a skill. Trim or split the members first.
- Uploads and the plugin install into different places. Say which one the person has before debugging "it doesn't trigger".

## Commands

- 🚀 **One zip, platform-checked** · `publish plugin`: Publishes the skillset as a Claude plugin: checks current rules, sets manifest fields, sweeps before release, packages, validates with the platform's tools, test-installs and hands over.
  - ✅ `validate plugin`: Validates the plugin build with the platform's own validator.
  - 🏷️ `release skillset`: Cuts a release: sweeps status text, packages with release, and hands over the steps.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents skillset-tools/publish-plugin` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review skillset-tools/publish-plugin` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
