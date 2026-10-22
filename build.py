#!/usr/bin/env python3
"""Build paste-ready GHL embed blocks and full-page previews.

  python3 build.py                      # uses config.json
  python3 build.py --preview-base assets --preview-out somewhere/

src/      editable source; image paths use the {{ASSET_BASE}} token
dist/     paste-ready blocks for GHL (token replaced with config.json "asset_base")
preview/  one full HTML page per site page, for checking the design in a browser
"""
import argparse, json, pathlib, shutil

ROOT = pathlib.Path(__file__).resolve().parent
SRC, DIST, PREVIEW = ROOT / "src", ROOT / "dist", ROOT / "preview"

# Page order = the order to stack embed blocks in GHL.
PAGES = {
    "index":   {"title": "Home",                 "dir": "home",                 "path": "/"},
    "free-sedona-spotlight": {"title": "Free Sedona Spotlight", "dir": "free-sedona-spotlight", "path": "/free-sedona-business-interviews"},
    "nominate": {"title": "Nominate",            "dir": "nominate",             "path": "/nominate"},
    "cities":  {"title": "Cities",               "dir": "cities",               "path": "/all-businesses-by-state"},
    "contact": {"title": "Contact",              "dir": "contact",              "path": "/contact"},
    "featured-businesses": {"title": "Featured Businesses", "dir": "featured-businesses", "path": "/featured-businesses",
                "blocks": ["featured-businesses/01-hero.html", "home/04-featured.html", "home/07-cta.html"]},
    "not-found": {"title": "Page Not Found",     "dir": "not-found",            "path": "/404"},
}


def page_blocks(page):
    """A page's section files in order: an explicit 'blocks' list, else every file in its folder."""
    if "blocks" in page:
        return [SRC / "pages" / b for b in page["blocks"]]
    return sorted((SRC / "pages" / page["dir"]).glob("*.html"))


def sub(text, base):
    return text.replace("{{ASSET_BASE}}", base.rstrip("/"))


def build_dist(base):
    if DIST.exists():
        shutil.rmtree(DIST)
    for f in SRC.rglob("*.html"):
        out = DIST / f.relative_to(SRC)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(sub(f.read_text(), base))
    # One-paste versions: styles + header + every section + footer for a single Code element.
    full = DIST / "full-page"
    full.mkdir(parents=True, exist_ok=True)
    g = {n: sub((SRC / f"global/{n}.html").read_text(), base) for n in ("head", "header", "footer")}
    for key, page in PAGES.items():
        blocks = page_blocks(page)
        parts = [g["head"], g["header"]] + [sub(b.read_text(), base) for b in blocks] + [g["footer"]]
        (full / f"{page['dir']}.html").write_text(
            f"<!-- BCA | {page['title']} — FULL PAGE. Paste into ONE Code element in a full-width, 0-padding section. -->\n"
            + "\n".join(parts))
    print(f"dist/ built with asset base: {base}")


def build_preview(base, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    head = sub((SRC / "global/head.html").read_text(), base)
    header = sub((SRC / "global/header.html").read_text(), base)
    footer = sub((SRC / "global/footer.html").read_text(), base)
    routes = {p["path"]: f"{k}.html" for k, p in PAGES.items()}
    switch = " ".join(
        f'<a href="{k}.html" style="color:#E8D3A6;margin:0 10px;text-decoration:none">{p["title"]}</a>'
        for k, p in PAGES.items()
    )
    for key, page in PAGES.items():
        blocks = page_blocks(page)
        body = "\n".join(sub(b.read_text(), base) for b in blocks)
        html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{page['title']} | Best of the City Awards (preview)</title>
{head}
<style>body{{margin:0;background:#FBF8F2}}</style>
</head><body>
<div style="background:#000;color:#999;font:12px/1.4 Montserrat,system-ui,sans-serif;padding:10px 16px;text-align:center">PREVIEW ONLY &middot; {switch}</div>
{header}
<main>
{body}
</main>
{footer}
<script>
(function(){{var r={json.dumps(routes)};document.addEventListener('click',function(e){{var a=e.target.closest('a[href^="/"]');if(!a)return;var h=a.getAttribute('href'),p=h.split('#')[0]||'/',f=r[p];if(f){{e.preventDefault();location.href=f+(h.indexOf('#')>-1?h.slice(h.indexOf('#')):'');}}}});}})();
</script>
</body></html>"""
        (out_dir / f"{key}.html").write_text(html)
    print(f"preview built in {out_dir} with asset base: {base}")


if __name__ == "__main__":
    cfg = json.loads((ROOT / "config.json").read_text())
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview-base", default="../assets")
    ap.add_argument("--preview-out", default=str(PREVIEW))
    a = ap.parse_args()
    build_dist(cfg["asset_base"])
    build_preview(a.preview_base, pathlib.Path(a.preview_out))
