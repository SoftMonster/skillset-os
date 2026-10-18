# Contributing

1. Change sub-skills under `subskills/`, or the tooling under `scripts/`.
2. Bump each changed sub-skill: `python scripts/skillset.py bump <name> --part major|minor|patch|revision|N (N is a part's position, so 5 is the fifth number) --message "..."`.
3. Run `python scripts/skillset.py index`, `python scripts/skillset.py check`, `pytest` and `ruff check .`.
4. Commit, including the regenerated `SKILL.md`.
5. Release with `python scripts/skillset.py package --message "..." --effect "..."`: every release's changelog section ends with the core-stats emoji list (effect, version, members, files, archive size, tests, self-memory, description, check), before → after.
6. If `package` or `build --edition shared` says a shared-edition patch no longer matches, update its `old` text (and `new` if needed) in `editions/shared/edition.json`.

Never add a file named `SKILL.md` below the top, never add a zip anywhere in the tree (claude.ai rejects the upload), and only import skills you have the right to redistribute. To benefit from other people's skills, prefer `find-skills`: learn from them, rewrite the lessons into existing members and credit the source in `docs/LEARNED-FROM.md`.

Contributions are released under the MIT licence in [LICENSE](LICENSE). Donations to the project go to its maintainer, Andrew Wright, through [GitHub Sponsors](https://github.com/sponsors/Softmonster); contributing does not entitle anyone to a share, and donating is never required to contribute.
