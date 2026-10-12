# ajyfood.com — Claude Code notes

Recipes are markdown files (`recipes.md/`) built into a static site in `_site/`
by `build.py`, deployed to S3 by a GitHub Action on push. `_site/` is not
committed; the Action builds it fresh (local preview: see "Site and deploy
notes"). **The site is public** — kid ratings and anything
family-specific must never appear in rendered pages.

## Reference docs
- Style guide: `docs/style-guide.md`
- Tag taxonomy: `docs/tag-taxonomy.md` (not written yet)
- Shelf-life table: `docs/shelf-life.md` (not written yet)
- Open threads and decisions: `../project-tracker.md` (outside the repo)

Keep this file short; it is the index. Conventions go in `docs/style-guide.md`,
reference material in `docs/`, open threads in the tracker.

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
6. Only on explicit approval: commit ("Add <Title> recipe", or "Update <Title>
   recipe" for edits), push with `scripts/push.sh` in the Food Assistant folder,
   then check the live page.
- If a link can't be read, ask for a screenshot.
- No tags or frontmatter until the taxonomy and frontmatter decisions are made
  (`project-tracker.md` threads 1 and 2).
- If a new convention gets agreed during intake, update `docs/style-guide.md` in
  the same commit.
- Checking the live page: the sandbox can't reach ajyfood.com, so open
  `https://ajyfood.com/recipes/<slug>` in the built-in browser pane and read the
  text. Right after a push it shows a raw S3 "Access Denied" until the deploy
  Action finishes (about a minute in practice), so wait and reload. If it's still
  denied after a few minutes, ask the owner to check the Action run; github.com
  isn't approved in the browser pane.

## Git from Claude's shell
- Ask for file-deletion permission on the Food Assistant folder at the start;
  git can't clear its own lock files without it, and `build.py` can't clear
  `_site/` (the build fails partway with a PermissionError).
- Push with `scripts/push.sh`. The GitHub token needs Contents and Workflows
  read/write.
- The repo lives at `Food Assistant/ajyfood.com` on the Mac. Work on it there
  through the device shell. Don't clone it in Claude's cloud container: that
  side has no GitHub link, so it can't push.
- Never print or Read `.secrets/github-token`; it ends up in the chat. Load it
  into a shell variable instead.
- To re-clone: clone with the token, then reset `origin` to the plain
  `https://github.com/rrranthony/ajyfood.com.git` so the token isn't stored in
  `.git/config`, and set the local git identity (Anthony Young /
  rrranthony@users.noreply.github.com).

## Site and deploy notes
- Recipe pages have no file extension (`recipes/<slug>`). The deploy labels them
  `text/html` explicitly; `build.py --serve` does the same locally. Opening the
  files directly from disk won't render them.
- Local preview on the Mac needs the pinned markdown package first:
  `pip3 install -r requirements.txt`, then `python3 build.py --serve`.
- To remove a recipe, delete its markdown file; the next deploy removes the page.
  The sync's `--delete` is scoped to `recipes/` on purpose, so nothing else in
  the bucket can be deleted by a deploy.
- ajyfood.com is served by CloudFront in front of the S3 bucket, which is why a
  missing page returns 403 "Access Denied" (tracker thread 7). As of 2026-10-11
  CloudFront isn't caching pages, so deploys show immediately and the workflow
  has no cache-invalidation step. If stale pages appear after a deploy, add one.

## Working agreements
- Never commit or push without explicit approval — show a diff or summary first.
- Every recipe intake includes a "what changed" list (skipped items, substitutions, merged steps).
- Small, reviewable changes. Concise answers. Ask rather than guess.
