# ajyfood.com — Claude Code notes

Recipes are markdown files (`recipes.md/`) built into a static site in `_site/`
by `build.py`, deployed to S3 by a GitHub Action on push. `_site/` is not
committed; the Action builds it fresh. Preview locally with
`python build.py --serve`. **The site is public** — kid ratings and anything
family-specific must never appear in rendered pages.

## Reference docs
- Style guide: `docs/style-guide.md`
- Tag taxonomy: `docs/tag-taxonomy.md` (not written yet)
- Shelf-life table: `docs/shelf-life.md` (not written yet)
- Open threads and decisions: `../project-tracker.md` (outside the repo)

## Recipe intake
When a recipe arrives (PDF, link, screenshot, or pasted text) with no other
instruction, treat it as an intake and start without asking:
1. Read `docs/style-guide.md` and `recipes.md/TEMPLATE.md` first.
2. Check `recipes.md/` for a similar recipe. If one exists, ask whether to update
   it or add a new one.
3. Draft the recipe in house format, with the file name from the style guide.
4. Show the draft and a "what changed" list: skipped items, substitutions,
   merged or split steps, unit conversions, and anything inferred.
5. Apply tweaks given in plain language.
6. Only on explicit approval: commit ("Add <Title> recipe"), push with
   `scripts/push.sh` in the Food Assistant folder, then check the live page.
- If a link can't be read, ask for a screenshot.
- No tags or frontmatter until the taxonomy and frontmatter decisions are made
  (`project-tracker.md` threads 1 and 2).
- If a new convention gets agreed during intake, update `docs/style-guide.md` in
  the same commit.

## Git from Claude's shell
- Ask for file-deletion permission on the Food Assistant folder at the start;
  git can't clear its own lock files without it.
- Push with `scripts/push.sh`. The GitHub token needs Contents and Workflows
  read/write.

## Working agreements
- Never commit or push without explicit approval — show a diff or summary first.
- Every recipe intake includes a "what changed" list (skipped items, substitutions, merged steps).
- Small, reviewable changes. Concise answers. Ask rather than guess.
