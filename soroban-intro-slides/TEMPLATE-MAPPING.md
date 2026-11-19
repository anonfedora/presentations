# Template mapping: reuse first, build only what's missing

Your site already has slide templates, so use them wherever they fit. `preview.html` shows the intended structure but **not the visual style**. Your site's theme (fonts, colours, spacing) takes priority over everything in the preview.

## Step 1: tick off what your site already has

Go through the table. For each element, write the name of the template or component you already have. Leave it blank if there isn't one.

| # | Element (`slides.json`) | Used on slides | Usually covered by | Your template | Missing? |
|---|---|---|---|---|---|
| 1 | Layout `title` | 1, 17 | Title / cover / section slide | | ☐ |
| 2 | Layout `content` + `bullets` | 2, 3, 4, 6, 7, 11 | Standard bullet slide | | ☐ |
| 3 | Bullet with bold `label` (**label** — text) | 2, 11 | Bullet slide with Markdown bold | | ☐ |
| 4 | `paragraph` | 1, 4, 17 | Any text slide | | ☐ |
| 5 | `callout` (`info` / `warning`) | 2, 5 | Note / tip / alert box | | ☐ |
| 6 | `table` | 5 | Table slide | | ☐ |
| 7 | `steps` (3 numbered cards) | 8 | Process / timeline / 3-column cards | | ☐ |
| 8 | `code` with line numbers | 9, 10 | Code slide | | ☐ |
| 9 | `code` line highlighting | 9 | Code slide option | | ☐ |
| 10 | `code` filename bar | 9, 10 | Code slide option | | ☐ |
| 11 | `links` (2 columns, label + note) | 12–16 | Resources / references slide | | ☐ |
| 12 | Speaker notes | most slides | Presenter mode | | ☐ |

## Step 2: fallbacks before building anything new

Try these first. Most gaps can be filled with templates you already have.

| Missing element | Fallback using a template you already have | Build new only if… |
|---|---|---|
| Bold-label bullet | Ordinary bullet with the label in bold in the text | Your bullets can't render bold |
| `callout` | Put the text as the last bullet, starting with "Note:" or "Heads up:" | The point needs to stand out visually (slide 2's "not EVM" and slide 5's "rent" are the key takeaways) |
| `table` | Three bullets, one per storage tier: **Instance** — use… · when the TTL runs out… | You want the comparison to read across columns (recommended) |
| `steps` | A numbered list (1. **Simulate** — …) | You want it to show a flow |
| Code line highlighting | Leave it out and point at the lines while presenting (they're listed in slide 9's notes) | You present this deck often |
| Code filename bar | Put the filename in the slide subtitle (e.g. "src/lib.rs") | — |
| Code line numbers | Leave them out | You refer to line numbers while talking |
| 2-column `links` | Your one-column list. Slide 15 has 8 links, so split it into 15a "Storage" (3 links) and 15b "Tokens" (5 links) | You want to keep 5 resource slides |
| Speaker notes | Keep them in a separate doc | — |

## Step 3: specs for any new template you build

Match your site's theme. These specs describe only structure and behaviour.

**Callout**
- Props: `variant: "info" | "warning"`, `text`.
- Full-width box below the main content, with a 4px left border. Use your accent colour for `info` and an amber/warning colour for `warning`.
- Background slightly lighter than the slide; text one size smaller than the bullets.

**Table**
- Props: `columns: string[]`, `rows: string[][]`.
- Full width, left-aligned cells, muted header row, thin dividers between rows, no vertical lines.
- Text at about 0.9× bullet size. Slide 5 must fit 3 rows plus a callout without scrolling.

**Steps**
- Props: `items: { title, text }[]` (slide 8 has 3).
- Equal-width cards side by side. Each card has a large accent-coloured number, then a bold title, then the text.
- On narrow screens, stack them vertically.

**Code block** (the most important one to get right)
- Props: `language` (`rust` | `bash`), `filename`, `content`, `highlight: number[]` (1-based line numbers).
- Monospace font at about 15px with 1.45 line height (for a 1280×720 slide). Show all 19 lines of slide 9 without scrolling.
- **No line wrapping**: scroll horizontally if needed. Keep whitespace exactly as written.
- Show line numbers in a muted gutter. Give highlighted lines a full-width tinted background.
- A thin filename bar above the code.
- Syntax colours come from your site's existing highlighter (Shiki, Prism or highlight.js). Don't add another one.
- If your code template already exists but lacks highlighting, extend it with a `highlight` prop instead of making a second code template.

**Links grid**
- Props: `items: { label, url, note }[]`.
- Two columns. The label is a bold link that opens in a new tab (`target="_blank" rel="noopener"`). The note goes on its own muted line under the label and is hidden when empty.
- Keep each item in one column; don't let it split across the column break.

## Step 4: wire it up

1. Use the slide `id` as the page slug, e.g. `/soroban/09-code-contract`.
2. For each slide, pick the template by `layout`. For each block inside it, pick the component by `type`. Use the template names you wrote in Step 1.
3. Code content is already inlined in `slides.json` (`blocks[].content`). If your code template imports from files, use `code/counter.rs` and `code/cli-workflow.sh` instead.
4. Open the original `preview.html` side by side with your site and check each slide's content and order. Expect the styling to differ, because your site's theme applies.
