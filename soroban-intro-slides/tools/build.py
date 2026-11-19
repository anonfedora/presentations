"""Generate slides.md, per-slide markdown, inlined JSON and preview.html from slides.json."""
import json, html, sys, pathlib

root = pathlib.Path(sys.argv[1])
deck = json.loads((root / "slides.json").read_text())

# Inline code sources so custom renderers need only one file
for s in deck["slides"]:
    for b in s["blocks"]:
        if b["type"] == "code":
            b["content"] = (root / b["source"]).read_text().rstrip("\n")
(root / "slides.json").write_text(json.dumps(deck, indent=2, ensure_ascii=False) + "\n")


def block_md(b):
    t = b["type"]
    if t == "paragraph":
        return b["text"]
    if t == "bullets":
        out = []
        for i in b["items"]:
            out.append(f"- **{i['label']}** — {i['text']}" if i.get("label") else f"- {i['text']}")
        return "\n".join(out)
    if t == "steps":
        return "\n".join(f"{n}. **{i['title']}** — {i['text']}" for n, i in enumerate(b["items"], 1))
    if t == "callout":
        return f"> **{'Note' if b['variant']=='info' else 'Heads up'}:** {b['text']}"
    if t == "table":
        rows = [b["columns"], ["---"] * len(b["columns"])] + b["rows"]
        return "\n".join("| " + " | ".join(r) + " |" for r in rows)
    if t == "code":
        hl = ""
        if b["highlight"]:
            hl = " {" + ",".join(map(str, b["highlight"])) + "}"
        return f"```{b['language']}{hl}\n{b['content']}\n```"
    if t == "links":
        return "\n".join(
            f"- [{i['label']}]({i['url']})" + (f" — {i['note']}" if i["note"] else "") for i in b["items"])
    raise ValueError(t)


def slide_md(s):
    head = f"# {s['title']}" if s["layout"] == "title" else f"## {s['title']}"
    parts = [head]
    if s.get("subtitle"):
        parts.append(f"### {s['subtitle']}")
    parts += [block_md(b) for b in s["blocks"]]
    if s.get("notes"):
        parts.append(f"<!--\nNotes: {s['notes']}\n-->")
    return "\n\n".join(parts) + "\n"


(root / "slides").mkdir(exist_ok=True)
mds = []
for s in deck["slides"]:
    md = slide_md(s)
    (root / "slides" / f"{s['id']}.md").write_text(md)
    mds.append(md)
(root / "slides.md").write_text("\n---\n\n".join(mds))


# ---------- preview.html ----------
def esc(x): return html.escape(x)

def block_html(b):
    t = b["type"]
    if t == "paragraph":
        return f"<p>{esc(b['text'])}</p>"
    if t == "bullets":
        li = "".join(
            f"<li><strong>{esc(i['label'])}</strong> — {esc(i['text'])}</li>" if i.get("label")
            else f"<li>{esc(i['text'])}</li>" for i in b["items"])
        return f"<ul>{li}</ul>"
    if t == "steps":
        li = "".join(f"<li><strong>{esc(i['title'])}</strong><span>{esc(i['text'])}</span></li>" for i in b["items"])
        return f'<ol class="steps">{li}</ol>'
    if t == "callout":
        return f'<div class="callout {b["variant"]}">{esc(b["text"])}</div>'
    if t == "table":
        th = "".join(f"<th>{esc(c)}</th>" for c in b["columns"])
        tr = "".join("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in r) + "</tr>" for r in b["rows"])
        return f"<table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>"
    if t == "code":
        lines = b["content"].split("\n")
        body = "".join(
            f'<span class="ln{" hl" if n in b["highlight"] else ""}">{esc(l) or " "}</span>'
            for n, l in enumerate(lines, 1))
        return (f'<figure class="code"><figcaption>{esc(b["filename"])}</figcaption>'
                f'<pre><code class="language-{b["language"]}">{body}</code></pre></figure>')
    if t == "links":
        li = "".join(
            f'<li><a href="{esc(i["url"])}" target="_blank" rel="noopener">{esc(i["label"])}</a>'
            + (f'<span class="note">{esc(i["note"])}</span>' if i["note"] else "") + "</li>"
            for i in b["items"])
        return f'<ul class="links">{li}</ul>'


sections = []
for n, s in enumerate(deck["slides"], 1):
    sub = f"<h2 class='sub'>{esc(s['subtitle'])}</h2>" if s.get("subtitle") else ""
    tag = "h1" if s["layout"] == "title" else "h2"
    inner = "".join(block_html(b) for b in s["blocks"])
    sections.append(
        f'<section class="slide layout-{s["layout"]}" id="{s["id"]}" data-n="{n}">'
        f"<{tag}>{esc(s['title'])}</{tag}>{sub}{inner}</section>")

page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(deck['title'])}</title>
<style>
:root{{--bg:#0f1115;--fg:#e8e8ea;--muted:#9aa0a6;--accent:#7c5cff;--code-bg:#161a22;--hl:rgba(124,92,255,.18);--border:#2a2f3a}}
*{{box-sizing:border-box}}html,body{{margin:0;height:100%;background:var(--bg);color:var(--fg);font:18px/1.5 Inter,system-ui,sans-serif}}
.slide{{display:none;position:absolute;inset:0;margin:auto;width:min(1280px,100vw);height:min(720px,100vh);padding:56px 72px;overflow:auto;flex-direction:column;justify-content:center}}
.slide.active{{display:flex}}
h1{{font-size:64px;margin:0 0 12px}}h2{{font-size:40px;margin:0 0 28px}}h2.sub{{font-size:26px;color:var(--muted);font-weight:400;margin:0 0 24px}}
.layout-title{{align-items:center;text-align:center}}
.layout-code{{padding-top:36px;padding-bottom:36px}}.layout-code h2{{margin-bottom:16px}}
ul,ol{{margin:0;padding-left:1.2em}}li{{margin:.45em 0;font-size:24px}}strong{{color:#fff}}
.callout{{margin-top:28px;padding:14px 18px;border-left:4px solid var(--accent);background:var(--code-bg);border-radius:6px;font-size:21px}}
.callout.warning{{border-color:#f5a524}}
table{{border-collapse:collapse;width:100%;font-size:21px}}th,td{{text-align:left;padding:12px 14px;border-bottom:1px solid var(--border)}}th{{color:var(--muted);font-weight:600}}
.steps{{list-style:none;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:20px;counter-reset:s}}
.steps li{{background:var(--code-bg);border:1px solid var(--border);border-radius:10px;padding:20px;counter-increment:s;font-size:20px}}
.steps li::before{{content:counter(s);display:block;color:var(--accent);font-weight:700;font-size:28px}}
.steps strong{{display:block;font-size:24px;margin-bottom:6px}}
figure.code{{margin:0;border:1px solid var(--border);border-radius:10px;overflow:hidden;background:var(--code-bg)}}
figcaption{{font:13px ui-monospace,monospace;color:var(--muted);padding:8px 16px;border-bottom:1px solid var(--border)}}
pre{{margin:0;padding:12px 0;overflow-x:auto}}code{{font:15px/1.45 "JetBrains Mono",ui-monospace,Menlo,Consolas,monospace;counter-reset:ln}}
.ln{{display:block;padding:0 16px;white-space:pre;counter-increment:ln}}
.ln::before{{content:counter(ln);display:inline-block;width:2.2em;margin-right:12px;color:#555c68;text-align:right}}
.ln.hl{{background:var(--hl)}}
.links{{list-style:none;padding:0;columns:2;column-gap:40px}}.links li{{break-inside:avoid;font-size:20px;margin:0 0 14px}}
.links a{{color:#b9a8ff;text-decoration:none;font-weight:600}}.links a:hover{{text-decoration:underline}}
.links .note{{display:block;color:var(--muted);font-size:16px}}
#count{{position:fixed;right:18px;bottom:12px;color:var(--muted);font-size:14px}}
</style></head><body>
{''.join(sections)}
<div id="count"></div>
<script>
const s=[...document.querySelectorAll('.slide')];let i=Math.max(0,s.findIndex(x=>'#'+x.id===location.hash));
function go(n){{i=Math.min(s.length-1,Math.max(0,n));s.forEach((x,k)=>x.classList.toggle('active',k===i));
document.getElementById('count').textContent=(i+1)+' / '+s.length;history.replaceState(null,'','#'+s[i].id);}}
addEventListener('keydown',e=>{{if(['ArrowRight','PageDown',' '].includes(e.key))go(i+1);if(['ArrowLeft','PageUp'].includes(e.key))go(i-1);}});
addEventListener('click',e=>{{if(e.target.closest('a'))return;go(e.clientX>innerWidth/2?i+1:i-1);}});
go(i);
</script></body></html>
"""
(root / "preview.html").write_text(page)
print("built", len(deck["slides"]), "slides")
