import os

def get_recipe_title(file_path):
    basename = os.path.basename(file_path)
    basename_without_extension = os.path.splitext(basename)[0]
    title = " ".join(word.capitalize() for word in basename_without_extension.split("-"))
    return title

def get_recipe_filenames(recipe_dir):
    files = os.listdir(recipe_dir)
    recipe_filenames = [
        f for f
        in files
        if (not f.startswith(".") and len(f) > 1)
    ]
    return recipe_filenames

def generate_index_html(recipe_filenames):
    href_base = "https://ajyfood.com/recipes"
    links = [
        f'<li><a href="{href_base}/{fn}">{get_recipe_title(fn)}</a></li>' for fn
        in sorted(recipe_filenames)
    ]
    html = "".join([
        "<!DOCTYPE html>\n",
        "<head>\n",
        '<meta charset="UTF-8">\n',
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n',
        "<title>Recipes</title>\n",
        '<link rel="stylesheet" href="/style.css">\n',
        "</head>\n",
        "<body>\n",
        "<h1>Recipes</h1>\n",
        "<ul>\n",
          "\n".join(links),
        "</ul>\n",
        "</body>\n",
        "</html>\n",
    ])
    return html


if __name__ == "__main__":
    recipe_dir = "recipes"
    recipe_filenames = get_recipe_filenames(recipe_dir)
    index_html = generate_index_html(recipe_filenames)
    print(f"index.html generated:\n\n{index_html}")
    with open("index.html", "w") as f:
        f.write(index_html)
