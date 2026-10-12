"""Build ajyfood.com from the markdown recipes in recipes.md/.

    python build.py            build the site
    python build.py --serve    build, then preview it at http://localhost:8000

Output goes to _site/, which is not committed: the deploy Action builds it
fresh on every push and syncs it to S3. Each recipes.md/<slug>.md becomes a
page at recipes/<slug> (no extension; S3 serves those as HTML), and index.html
lists every recipe by its "# Title" line.

A recipe with a sibling recipes.md/<slug>.table file also gets a "View as Recipe
Table" toggle. The .table format is described in CLAUDE.md.
"""
import functools
import html
import http.server
import re
import shutil
import sys
from pathlib import Path

from markdown import markdown

ROOT = Path(__file__).resolve().parent
SOURCE_DIR = ROOT / "recipes.md"
OUTPUT_DIR = ROOT / "_site"
STATIC_FILES = ["style.css", "favicon.ico", "404.html"]
TEMPLATE_NAME = "TEMPLATE.md"
TABLE_SUFFIX = ".table"

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


TABLE_VIEW = """<h1>{title}</h1>
<button type="button" class="view-toggle" aria-pressed="false" hidden>View as Recipe Table</button>
<div class="recipe-text">
{text}
</div>
<div class="recipe-table" hidden>
<p class="rotate-hint">Turn your phone sideways to see the recipe table.</p>
<div class="table-wrap">
{table}
</div>
</div>
"""

TABLE_SCRIPT = """<script>
(function () {
  var button = document.querySelector(".view-toggle");
  var text = document.querySelector(".recipe-text");
  var table = document.querySelector(".recipe-table");
  button.hidden = false;
  button.addEventListener("click", function () {
    var on = button.getAttribute("aria-pressed") !== "true";
    button.setAttribute("aria-pressed", String(on));
    button.textContent = on ? "View as Recipe" : "View as Recipe Table";
    text.hidden = on;
    table.hidden = !on;
    document.body.classList.toggle("table-view", on);
  });
})();
</script>
"""

# Table cells are narrow, so units are abbreviated there (only there).
ABBREVIATIONS = [(re.compile(r"\btablespoons?\b"), "tbsp"), (re.compile(r"\bteaspoons?\b"), "tsp")]
AMOUNT = r"\d+(?:[ /]\d+)*(?:\s(?:cups?|tbsp|tsp|tablespoons?|teaspoons?|oz|ounces?|pounds?|lb|cloves?)\b)?"
QUANTITY = re.compile(rf"^({AMOUNT}(?:\s+plus\s+{AMOUNT})?)\s+(.*)$")


class TableNode:
    def __init__(self, text, depth):
        self.text = text
        self.depth = depth
        self.children = []
        self.parent = None


def parse_table(path):
    """Read a .table file. Unindented "prep: ..." lines are full-width setup rows,
    shown where they appear. The one other unindented line is the final step;
    each step's inputs are indented two spaces under it. Lines without children
    are ingredient rows; lines with children are steps. Returns the top-level
    items in order: prep strings and the final step's node."""
    items, stack, root = [], [], None
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        where = f"{path.name} line {number}"
        if indent % 2:
            raise ValueError(f"{where}: indent with 2 spaces per level")
        text = raw.strip()
        if text.startswith("prep:"):
            if indent:
                raise ValueError(f"{where}: prep rows must not be indented")
            items.append(text[len("prep:"):].strip())
            stack = []
            continue
        node = TableNode(text, indent // 2)
        while stack and stack[-1].depth >= node.depth:
            stack.pop()
        if stack:
            if node.depth != stack[-1].depth + 1:
                raise ValueError(f"{where}: indented more than one level")
            node.parent = stack[-1]
            stack[-1].children.append(node)
        elif root is None and node.depth == 0:
            root = node
            items.append(root)
        else:
            raise ValueError(f"{where}: only one unindented step (the final step) is allowed")
        stack.append(node)
    if root is None or not root.children:
        raise ValueError(f"{path.name}: no steps")
    return items


def layout_table(root):
    """Give each node its row span and column. Rows are the leaves in outline
    order; a step's column is one past its deepest input, so the final step is
    rightmost. Returns the leaves (rows) and every node."""
    leaves, nodes = [], []

    def walk(node):
        nodes.append(node)
        if node.children:
            for child in node.children:
                walk(child)
            node.height = 1 + max(child.height for child in node.children)
            node.first = node.children[0].first
            node.rows = sum(child.rows for child in node.children)
        else:
            node.height, node.first, node.rows = 0, len(leaves), 1
            leaves.append(node)

    walk(root)
    return leaves, nodes


def table_cell(node):
    colspan = node.parent.height - node.height if node.parent else 1
    attrs = ""
    if node.rows > 1:
        attrs += f' rowspan="{node.rows}"'
    if colspan > 1:
        attrs += f' colspan="{colspan}"'
    if node.children:
        action, _, detail = (part.strip() for part in node.text.partition("|"))
        inner = f'<span class="action">{html.escape(action)}</span>'
        if detail:
            inner += f'<span class="detail">{html.escape(detail)}</span>'
        return f'<td class="step"{attrs}>{inner}</td>'
    text = node.text
    for pattern, short in ABBREVIATIONS:
        text = pattern.sub(short, text)
    match = QUANTITY.match(text)
    if match:
        inner = f"<strong>{html.escape(match.group(1))}</strong> {html.escape(match.group(2))}"
    else:
        inner = html.escape(text)
    return f'<td class="ingredient"{attrs}>{inner}</td>'


def render_table(items):
    root = next(item for item in items if isinstance(item, TableNode))
    leaves, nodes = layout_table(root)
    columns = root.height + 1
    rows = []
    for item in items:
        if isinstance(item, str):
            rows.append(
                f'<tr><td class="prep" colspan="{columns}"><span class="tag">prep</span>'
                f"{html.escape(item)}</td></tr>"
            )
            continue
        for index in range(len(leaves)):
            starting = sorted((n for n in nodes if n.first == index), key=lambda n: n.height)
            rows.append("<tr>" + "".join(table_cell(n) for n in starting) + "</tr>")
    return "<table>\n" + "\n".join(rows) + "\n</table>"


def ingredient_lines(text):
    """The "- ..." lines under "## Ingredients"."""
    lines, inside = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            inside = line.strip() == "## Ingredients"
        elif inside and line.startswith("- "):
            lines.append(line[2:].strip())
    return lines


def ingredient_name(line):
    """The line without its leading amount: "1/4 cup plus 3 tablespoons water" -> "water"."""
    match = QUANTITY.match(line)
    return match.group(2) if match else line


def check_table(items, text, name):
    """Warn when the table and the recipe's Ingredients disagree:
    - a table row that isn't in Ingredients (e.g. water used in a step but never listed);
    - an Ingredients line with no table row;
    - an ingredient with one table row whose amount differs from the recipe.
    An ingredient split across steps has several rows; only its name is checked."""
    root = next(item for item in items if isinstance(item, TableNode))
    leaves, _ = layout_table(root)
    recipe = {ingredient_name(line): line for line in ingredient_lines(text)}
    rows_by_name = {}
    for leaf in leaves:
        rows_by_name.setdefault(ingredient_name(leaf.text), []).append(leaf.text)
    for row_name, rows in rows_by_name.items():
        if row_name not in recipe:
            print(f"WARNING: {name}: not in the recipe's Ingredients: {rows[0]!r}")
        elif len(rows) == 1 and rows[0] != recipe[row_name]:
            print(f"WARNING: {name}: {rows[0]!r} doesn't match the recipe's {recipe[row_name]!r}")
    for row_name, line in recipe.items():
        if row_name not in rows_by_name:
            print(f"WARNING: {name}: ingredient missing from the table: {line!r}")


def recipe_body(text, source, title):
    """The page body: plain recipe, or recipe plus table view when a .table exists."""
    table_path = source.with_suffix(TABLE_SUFFIX)
    if not table_path.exists():
        return markdown(text), ""
    items = parse_table(table_path)
    check_table(items, text, table_path.name)
    without_title = re.sub(r"^# .*\n?", "", text, count=1, flags=re.MULTILINE)
    body = TABLE_VIEW.format(
        title=html.escape(title), text=markdown(without_title), table=render_table(items)
    )
    return body, TABLE_SCRIPT


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
        body, script = recipe_body(text, source, title)
        page = PAGE.format(title=html.escape(title), body=body, footer=RECIPE_FOOTER + script)
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
