# ajyfood.com — Claude Code notes

Recipes are markdown files (`recipes.md/`) converted to HTML (`recipes/`) by
`convert_markdown_recipes_to_html.py`, deployed to an S3 static site via a
GitHub Action on push. **The site is public** — kid ratings and anything
family-specific must never appear in rendered pages.

## Reference docs
- Style guide: `docs/style-guide.md`
- Tag taxonomy: `docs/tag-taxonomy.md` (TBD)
- Shelf-life table: `docs/shelf-life.md` (TBD)

## Working agreements
- Never commit or push without explicit approval — show a diff or summary first.
- Every recipe intake includes a "what changed" list (skipped items, substitutions, merged steps).
- Small, reviewable changes. Concise answers. Ask rather than guess.
- The deploy Action commits generated HTML back to `main` — pull/rebase before pushing.
