# ajyfood.com — Claude Code notes

Recipes are markdown files (`recipes.md/`) built into a static site in `_site/`
by `build.py`, deployed to S3 by a GitHub Action on push. `_site/` is not
committed; the Action builds it fresh. Preview locally with
`python build.py --serve`. **The site is public** — kid ratings and anything
family-specific must never appear in rendered pages.

## Reference docs
- Style guide: `docs/style-guide.md`
- Tag taxonomy: `docs/tag-taxonomy.md` (TBD)
- Shelf-life table: `docs/shelf-life.md` (TBD)

## Working agreements
- Never commit or push without explicit approval — show a diff or summary first.
- Every recipe intake includes a "what changed" list (skipped items, substitutions, merged steps).
- Small, reviewable changes. Concise answers. Ask rather than guess.
