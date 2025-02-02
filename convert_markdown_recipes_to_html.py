import os
from markdown import markdown as convert


def get_markdown_files(markdown_dir):
    files = os.listdir(markdown_dir)
    markdown_files = [
        f"{markdown_dir}/{f}" for f
        in files
        if (f.endswith(".md") and "TEMPLATE" not in f)
    ]
    return markdown_files

def get_html_filename_from_markdown_filename(markdown_filename):
    basename = os.path.basename(markdown_filename)
    basename_without_extension = os.path.splitext(basename)[0]
    html_filename = f"{basename_without_extension}"
    return html_filename

def get_recipe_title(file_path):
    basename = os.path.basename(file_path)
    basename_without_extension = os.path.splitext(basename)[0]
    title = " ".join(word.capitalize() for word in basename_without_extension.split("-"))
    return title

def convert_markdown_to_html(markdown, recipe_title):
    html = convert(markdown)
    html = "".join([
        "<!DOCTYPE html>\n",
        "<html lang="en">",
        f'<head><meta charset="UTF-8"><title>{recipe_title}</title></head>\n',
        "<body>\n",
            html,
            "\n",
            '<footer><br><a href="../index.html">Back to all recipes</a></footer>\n',
        "</body>\n",
        "</html>\n",
    ])
    return html

def convert_markdown_file_to_html_file(markdown_filename, output_dir):
    with open(markdown_filename, "r") as f:
        markdown = f.read()

    recipe_title = get_recipe_title(markdown_filename)
    html = convert_markdown_to_html(markdown, recipe_title)

    html_filename = get_html_filename_from_markdown_filename(markdown_filename)
    output_file = os.path.join(output_dir, html_filename)
    with open(output_file, "w") as f:
        f.write(html)


if __name__ == "__main__":
    markdown_dir = "recipes.md"
    html_dir = "recipes"

    # Get all markdown files, e.g., ["recipes.md/cheese-sauce.md", "recipes.md/overnight-oats.md"].
    markdown_files = get_markdown_files(markdown_dir)

    for f in markdown_files:
        convert_markdown_file_to_html_file(f, html_dir)
        print(f"Converted {f}")
