"""Build ajyfood.com from the markdown recipes in recipes.md/.

    python build.py            build the site
    python build.py --serve    build, then preview it at http://localhost:8000

Output goes to _site/, which is not committed: the deploy Action builds it
fresh on every push and syncs it to S3. Each recipes.md/<slug>.md becomes a
page at recipes/<slug> (no extension; S3 serves those as HTML), and index.html
lists every recipe by its "# Title" line.
"""
import functools
import html
import http.server
import shutil
import sys
from pathlib import Path

from markdown import markdown

ROOT = Path(__file__).resolve().parent
SOURCE_DIR = ROOT / "recipes.md"
OUTPUT_DIR = ROOT / "_site"
STATIC_FILES = ["style.css", "favicon.ico", "404.html"]
TEMPLATE_NAME = "TEMPLATE.md"

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="/style.css">
</head>
<body>
{body}
{footer}</body>
</html>
"""

RECIPE_FOOTER = '<footer><br><a href="/index.html">Back to all recipes</a></footer>\n'


def recipe_sources():
    """All recipe markdown files except the blank template, sorted by filename."""
    return sorted(p for p in SOURCE_DIR.glob("*.md") if p.name != TEMPLATE_NAME)


def recipe_title(text, slug):
    """The recipe's "# Title" line, or a title made from the filename if missing."""
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return " ".join(word.capitalize() for word in slug.split("-"))


def build():
    # Rebuild from scratch so deleted or renamed recipes don't leave stale pages.
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    recipes_out = OUTPUT_DIR / "recipes"
    recipes_out.mkdir(parents=True)
    for name in STATIC_FILES:
        shutil.copy2(ROOT / name, OUTPUT_DIR / name)

    entries = []
    for source in recipe_sources():
        text = source.read_text(encoding="utf-8")
        slug = source.stem
        title = recipe_title(text, slug)
        page = PAGE.format(title=html.escape(title), body=markdown(text), footer=RECIPE_FOOTER)
        (recipes_out / slug).write_text(page, encoding="utf-8")
        entries.append((title, slug))

    entries.sort(key=lambda entry: entry[0].lower())
    links = "\n".join(
        f'<li><a href="recipes/{slug}">{html.escape(title)}</a></li>' for title, slug in entries
    )
    index_body = f"<h1>Recipes</h1>\n<ul>\n{links}\n</ul>"
    (OUTPUT_DIR / "index.html").write_text(
        PAGE.format(title="Recipes", body=index_body, footer=""), encoding="utf-8"
    )
    print(f"Built {len(entries)} recipes into {OUTPUT_DIR}")


class PreviewHandler(http.server.SimpleHTTPRequestHandler):
    def guess_type(self, path):
        # Recipe pages have no extension. S3 serves them as HTML; do the same here.
        if Path(path).suffix == "":
            return "text/html; charset=utf-8"
        return super().guess_type(path)


def serve(port=8000):
    handler = functools.partial(PreviewHandler, directory=str(OUTPUT_DIR))
    print(f"Previewing at http://localhost:{port}  (Ctrl+C to stop)")
    http.server.ThreadingHTTPServer(("127.0.0.1", port), handler).serve_forever()


if __name__ == "__main__":
    build()
    if "--serve" in sys.argv:
        serve()
