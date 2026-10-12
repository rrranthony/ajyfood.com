# Recipe Style Guide

How every recipe in `recipes.md/` is written. Follow it for new recipes and edits;
start new recipes from `recipes.md/TEMPLATE.md`.
Older recipes don't all follow it, so don't copy them as examples. The reference
recipe is `recipes.md/lemony-chicken-and-orzo-soup.md`.

When a new convention is agreed in a chat, add it here in the same change.

## File name
- One recipe per file in `recipes.md/`, named `<slug>.md`.
- Slug = the full title in lowercase, words joined with hyphens. Keep every word,
  including "and", "with", "in". Drop apostrophes and other punctuation; write
  "&" as "and". Example: "Shepherd's Pie with Peas & Carrots" →
  `shepherds-pie-with-peas-and-carrots.md`.
- The slug becomes the page address (`ajyfood.com/recipes/<slug>`). Don't rename
  existing files; it breaks links.

## Layout
```
# Title

## Ingredients
- ...

## Steps
1. ...

## Notes
- ...
```
- Sections in this order: title, Ingredients, Steps, then Notes if needed.
  No intro paragraph, source credit, or other sections.
- Section names are exactly "Ingredients", "Steps", "Notes" (not "Instructions"
  or "Directions").
- Blank line before each heading, none after it.
- Plain markdown only: no bold, italics, images, or tables. No links, except to
  another recipe on this site, written as a site-relative path:
  `[salad dressing](/recipes/salad-dressing)`.
- No frontmatter (`---` block) yet; the site would show it as text.
- Nothing family-specific anywhere in the file: no kid ratings, names, or
  personal notes. The site is public.

## Title
- Title case, with short joining words lowercase unless first: and, with, in,
  of, or, the. Example: "Red Lentil Dill Soup with Mint".

## Components (sauce, dressing, mash)
- When a recipe has two or more distinct components, group the ingredients under
  `### Component` headings inside Ingredients: sentence case, no colon
  (`### Yogurt sauce`). Order them in the order they're made.
- Steps stay one numbered list. Name the component when a step works on it:
  "Whisk the dressing ingredients until smooth."

## Spelling
- Accented spellings: sauté, purée, jalapeño, Gruyère.
- Capitalize proper names: Dijon, Parmesan, Yukon Gold, Meyer lemon, Dutch oven.
- Dimensions with a plain "x": "8x8-inch pan".

## Ingredients
- One per line: `- {amount} {unit} {ingredient}, {prep}`.
  Examples: "1 onion, diced", "4 cups kale, de-ribbed and chopped".
- List in the order they're used.
- Everything the steps use is listed, water included. An ingredient split across
  steps is listed once with the total ("1/4 cup plus 3 tablespoons water"), and
  each step gives its portion.
- Fractions as `1/2` and `1 1/2`, never ½-style glyphs.
- Units spelled out, plural when the amount is more than 1: teaspoon, tablespoon,
  cup, pound, ounce. Never T, t, c, tbsp, tsp, lb, oz.
- Exception: can and package sizes use the label form:
  "1 14.5-oz can cannellini beans, drained".
- Garlic: "4 cloves garlic, minced". Citrus: "Juice of 1 lemon", "Zest of 1 lemon".
- Helpful conversions in parentheses: "2 cups (6 ounces) shredded cheddar cheese",
  "1/2 cucumber (1 cup), diced".
- Write "broth", not "stock", and don't specify "low-sodium" on broth or soy
  sauce (cooks salt to taste). Keep "stock" only when swapping in broth would
  meaningfully change the recipe.
- Alternatives and optional items in parentheses at the end:
  "1 teaspoon ground cumin (or Herbes de Provence)", "2 bay leaves (optional)".
- Assembly items with no real quantity (wraps, bowls) can skip the amount:
  "Romaine lettuce, chopped".
- Capitalize the first word of a line that starts with a word.
- Skip fresh herbs unless critical to the dish; use the dried equivalent instead.
- Prefer frozen corn over fresh when only kernels are needed, unless fresh really
  matters to the result.
- Leave out red pepper flakes unless the recipe depends on the heat.
- Leave salt and black pepper out of the list unless a specific quantity matters;
  mention them in the steps instead ("Season with salt to taste.").

## Steps
- Numbered list. Imperative, full sentences ending in a period.
- One action per step. A step may carry its doneness cue and time ("Cook until
  softened, about 4 minutes.") or continue the same action ("Bring to a boil,
  then reduce to a simmer."). Two separate tasks are two steps.
- Refer to ingredients by name without repeating amounts, unless an ingredient is
  split across steps ("Add 1/2 cup of the broth.").
- Temperatures as "425 degrees F". Times as "about 20 minutes"; ranges as
  "13 to 16 minutes".
- No filler steps such as "Enjoy." or "Serve and enjoy."

## Notes (optional)
- Bulleted. For yield, pan-size and bake-time variations, batch-size variations,
  make-ahead, storage, reheating, and substitutions. These go here, not in the
  Steps or a second Ingredients list.
- Yield, when known, is the first bullet: "Makes 24 cookies." or "Serves 4."
  (Interim until the frontmatter decision in project-tracker.md thread 1.)
- A substitution that changes the steps goes in Notes, spelled out by step
  number. The Ingredients and Steps are written for the primary version.

## Dropped at intake
- Headnotes and stories, source credits, nutrition info, photos, equipment lists
  (mention equipment in the step that uses it), and anything not about making the dish.
