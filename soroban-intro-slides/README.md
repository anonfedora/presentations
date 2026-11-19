# Introduction to Soroban — slide pack

17 slides covering the Soroban introduction, two code slides and the reference links. They're laid out for a **16:9 deck at 1280×720**.

> **Using your site's existing templates?** Start with **`TEMPLATE-MAPPING.md`**. It lists every element the deck uses, gives fallbacks that use templates you already have, and has build specs only for the elements your site is missing. Your site's theme takes priority over the styling in `preview.html`.

## What's in the zip

| Path | What it is | Use it when |
|---|---|---|
| `TEMPLATE-MAPPING.md` | Checklist: existing template → element, fallbacks, specs for new templates. | **Start here.** |
| `preview.html` | Self-contained preview of the deck's structure (not your site's styling). Arrow keys / click to navigate. Works offline. | You want to see the intended layout before porting. |
| `slides.md` | All slides in one Markdown file, separated by `---`. | Your site uses **reveal.js, Slidev or Marp** (or any Markdown-driven deck). |
| `slides/NN-*.md` | One Markdown file per slide. | Your site renders **one page per slide** from Markdown/MDX. |
| `slides.json` | Structured source of truth: every slide as typed blocks, code inlined. | Your site is **custom (React/Vue/Svelte/Astro…)** and renders components from data. |
| `code/counter.rs`, `code/cli-workflow.sh` | The two code samples as raw files. | You import code from files instead of pasting it in. |
| `tools/build.py` | Regenerates `slides.md`, `slides/` and `preview.html` from `slides.json`. | You edited `slides.json` and want everything else back in sync: `python3 tools/build.py .` |

## Slide order

| # | id | Layout | Content |
|---|---|---|---|
| 1 | `01-title` | title | Title slide |
| 2 | `02-what-is-soroban` | content | Overview + "not EVM" callout |
| 3 | `03-rust-wasm` | content | Rust → WASM |
| 4 | `04-env` | content | The `Env` |
| 5 | `05-storage` | table | Storage tiers & state archival |
| 6 | `06-auth` | content | Authorization |
| 7 | `07-assets` | content | Stellar Asset Contract / SEP-41 |
| 8 | `08-fees` | content (steps) | Resource-based fees: Simulate → Declare → Pay |
| 9 | `09-code-contract` | code | Minimal Rust contract (lines 12, 13, 15, 16 highlighted) |
| 10 | `10-code-cli` | code | Stellar CLI workflow (bash) |
| 11 | `11-testing` | content | Testing & TypeScript bindings |
| 12–16 | `12-…` to `16-…` | links | Reference links (5 slides) |
| 17 | `17-closing` | title | Thank you / Questions |

## Formatting rules

**Layouts**
- `title`: content centred both ways. Title about 64px; the subtitle is a muted second line.
- `content`: left-aligned and vertically centred. Slide title about 40px; bullets about 24px.
- `table`: full-width table with a muted header row and thin row dividers.
- `code`: less top and bottom padding than other slides, so the code block gets most of the height.
- `links`: two columns. The label is a bold link; the optional note goes on a smaller muted line under it.

**Block types (in `slides.json`)**

| `type` | Fields | Render as |
|---|---|---|
| `paragraph` | `text` | `<p>` |
| `bullets` | `items[]` → `label?`, `text` | `<ul>`. When a `label` is present: **label** — text |
| `steps` | `items[]` → `title`, `text` | Three equal cards in a row, each numbered |
| `callout` | `variant` (`info` \| `warning`), `text` | Box with a coloured left border: accent colour for info, amber for warning |
| `table` | `columns[]`, `rows[][]` | `<table>` |
| `code` | `language`, `filename`, `content`, `highlight[]` (1-based line numbers), `source` | Code block with a filename bar, line numbers and highlighted lines |
| `links` | `items[]` → `label`, `url`, `note` | Link list. Open links in a new tab (`target="_blank" rel="noopener"`) |

**Code view**
- Languages: `rust` and `bash`. Use your site's highlighter: Shiki (Slidev and Astro use it by default), Prism or highlight.js. The preview shows layout only, with no syntax colours.
- Use a monospace font at **15px with 1.45 line height**. At 1280×720 that fits all 19 lines of the Rust sample without scrolling. If your slides are smaller, scale the font down or let the code block scroll. Don't wrap lines.
- Show line numbers. The highlighted lines on slide 9 are explained in that slide's speaker notes.
- Keep indentation exactly as written: 4 spaces in Rust, 2-space continuation lines in bash.

**Colours used in the preview** (swap in your brand's colours)
`--bg #0f1115` · `--fg #e8e8ea` · `--muted #9aa0a6` · `--accent #7c5cff` · `--code-bg #161a22` · `--hl rgba(124,92,255,.18)` · `--border #2a2f3a`

**Speaker notes**
In the Markdown files, notes are in an HTML comment at the end of each slide, starting with `Notes:`. In `slides.json` they're in each slide's `notes` field.

## Framework-specific notes

**Slidev**: `slides.md` works as is. The ` ```rust {12,13,15,16}` line-highlight syntax and the trailing HTML-comment notes are both native Slidev. Add your own headmatter at the top (theme etc.).

**Marp**: add `marp: true` front matter at the top of `slides.md`. Marp treats HTML comments as presenter notes. It doesn't support the `{12,13,15,16}` highlight suffix, so remove it or highlight lines with CSS.

**reveal.js (Markdown plugin)**: use `data-separator="^\n---\n"`. Change the highlight suffix from `{12,13,15,16}` to `[12,13,15,16]`, which is reveal's `data-line-numbers` syntax. For notes, replace `<!--\nNotes: …\n-->` with a `Note:` line, or set `data-separator-notes`.

**Custom site**: load `slides.json`, map each `layout` to a page template and each block `type` to a component, using the tables above. Use slide `id`s as URL slugs (`/soroban/09-code-contract`). Code is already inlined in each code block's `content` field.

## Before publishing

- Check every link. All URLs came from Stellar's docs or GitHub, but docs paths do change. These four were never opened directly, so check them first: Stellar Lab, Stellar Expert, the Discord invite and the RPC docs page.
- Facts were current as of **18 Nov 2026**: mainnet launch on 20 Feb 2024 with Protocol 20, SDK v28 and Protocol 28.
