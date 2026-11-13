#!/usr/bin/env python3
"""Build GHL blog-post bodies for Spotlights from spotlights/content/<slug>.txt.

  python3 spotlights/build_posts.py

Each content file has a header (key: value lines), a line with ---, then the article:
blank-line-separated paragraphs, "## " for section headings. See content/_TEMPLATE.txt.
Output: dist/spotlights/posts/<slug>.html — paste into the post's Custom Code block in GHL.
"""
import html, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "spotlights" / "content"
OUT = ROOT / "dist" / "spotlights" / "posts"

STYLE = """<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Montserrat:wght@400;500;600;700&display=swap">
<style>
.bca-post{--ink:#151515;--gold:#C49A55;--gold-deep:#835E1E;--ivory:#FBF8F2;--line:#E3D9C7;--muted:#5A534B;
  font-family:'Montserrat',system-ui,sans-serif;font-size:17px;line-height:1.8;color:#2B2723;max-width:760px;margin:0 auto;text-align:left}
.bca-post *{box-sizing:border-box}
.bca-post p{margin:0 0 20px}
.bca-post a{color:var(--gold-deep)!important;text-decoration:none!important;border-bottom:1px solid #E8D3A6}
.bca-post a:hover{color:var(--ink)!important}
.bca-post__kicker{font-size:11px;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:var(--gold-deep);margin:0 0 10px!important}
.bca-post__tagline{font-family:'Libre Baskerville',Georgia,serif;font-style:italic;font-size:22px;line-height:1.5;color:var(--ink);margin:0 0 32px!important}
.bca-post__video{position:relative;padding-top:56.25%;background:#000;margin:0 0 32px}
.bca-post__video iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.bca-post__facts{background:var(--ivory);border-top:3px solid var(--gold);padding:22px 26px;margin:0 0 40px;display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px 28px}
.bca-post__facts dt{font-size:10px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);margin:0 0 4px}
.bca-post__facts dd{margin:0;font-size:15px;line-height:1.5;color:var(--ink)}
.bca-post__facts dd a{margin-right:16px;display:inline-block}
.bca-post__facts .bca-post__wide{grid-column:1/-1}
.bca-post h2{font-family:'Libre Baskerville',Georgia,serif;font-weight:400;font-size:28px;line-height:1.3;color:var(--ink);margin:48px 0 18px}
.bca-post__lead{font-size:19px;line-height:1.75;color:var(--ink)}
.bca-post blockquote{margin:44px 0;padding:6px 0 6px 28px;border-left:3px solid var(--gold);font-family:'Libre Baskerville',Georgia,serif;font-style:italic;font-size:22px;line-height:1.55;color:var(--ink)}
.bca-post blockquote cite{display:block;margin-top:14px;font-family:'Montserrat',system-ui,sans-serif;font-style:normal;font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--gold-deep)}
.bca-post__byline{margin-top:44px!important;padding-top:22px;border-top:1px solid var(--line);font-size:14px;color:var(--muted)}
.bca-post__byline strong{color:var(--ink);font-weight:600}
@media(max-width:600px){.bca-post{font-size:16px}.bca-post h2{font-size:24px}.bca-post__tagline,.bca-post blockquote{font-size:19px}}
</style>"""


def parse(path):
    head, body = path.read_text().split("\n---\n", 1)
    meta = {}
    for line in head.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    blocks = [b.strip() for b in re.split(r"\n\s*\n", body.strip()) if b.strip()]
    return meta, blocks


def esc(s):
    return html.escape(s, quote=False).replace("'", "&rsquo;")


def build(meta, blocks):
    out = [STYLE, '<div class="bca-post">',
           f'<p class="bca-post__tagline">{esc(meta["tagline"])}</p>']
    if meta.get("video"):
        out.append(f'<div class="bca-post__video"><iframe src="https://www.youtube-nocookie.com/embed/{meta["video"]}?rel=0" '
                   f'title="{esc(meta["business"])} video spotlight" loading="lazy" '
                   'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>')
    facts = [("Business", esc(meta["business"])), ("Location", esc(meta["location"]))]
    if meta.get("people"):
        facts.append(("Meet", "<br>".join(esc(p.strip()) for p in meta["people"].split(";"))))
    if meta.get("links"):
        links = []
        for item in meta["links"].split(";"):
            label, url = item.strip().split("|", 1)
            links.append(f'<a href="{url}" target="_blank" rel="noopener">{esc(label)}</a>')
        facts.append(("Connect", "".join(links)))
    cells = []
    for k, v in facts:
        cls = ' class="bca-post__wide"' if k == "Connect" else ""
        cells.append(f"<div{cls}><dt>{k}</dt><dd>{v}</dd></div>")
    out.append('<dl class="bca-post__facts">' + "".join(cells) + "</dl>")

    quote = meta.get("quote", "")
    h2s = [i for i, b in enumerate(blocks) if b.startswith("## ")]
    quote_at = h2s[-1] if quote and h2s else None  # pull quote goes before the last section
    first_para = True
    for i, b in enumerate(blocks):
        if i == quote_at:
            text, who = quote.split("|", 1)
            out.append(f"<blockquote>&ldquo;{esc(text)}&rdquo;<cite>{esc(who)}</cite></blockquote>")
        if b.startswith("## "):
            out.append(f"<h2>{esc(b[3:])}</h2>")
        else:
            cls = ' class="bca-post__lead"' if first_para else ""
            out.append(f"<p{cls}>{esc(b)}</p>")
            first_para = False
    out.append("</div>")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for f in sorted(CONTENT.glob("*.txt")):
        if f.name.startswith("_"):
            continue
        meta, blocks = parse(f)
        problems = [k for k in ("title", "slug", "meta") if not meta.get(k)]
        if len(meta.get("title", "")) > 60: problems.append(f"title {len(meta['title'])} chars (max 60)")
        if len(meta.get("meta", "")) > 160: problems.append(f"meta {len(meta['meta'])} chars (max 160)")
        (OUT / f"{meta['slug']}.html").write_text(build(meta, blocks))
        print(f"{meta['slug']}: {len(blocks)} blocks, title {len(meta['title'])}c, meta {len(meta['meta'])}c" + (f"  ! {problems}" if problems else ""))
