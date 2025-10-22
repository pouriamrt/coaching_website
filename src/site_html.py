# src/site_html.py
import json
from utils import html_response
from typing import Optional
import os

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "../public")

def render_html(page_name: str, replacements: Optional[dict] = None) -> str:
    """Loads an HTML template and injects placeholders."""
    path = os.path.join(TEMPLATE_DIR, f"{page_name}.html")
    try:
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
    except FileNotFoundError:
        raise ValueError(f"Template not found: {path}")

    if replacements:
        for key, val in replacements.items():
            html = html.replace(f"{{{{ {key} }}}}", str(val))

    return html
  
def base(env, title: str, body: str, description: str = "", path: str = "/"):
    site = env.SITE_NAME
    tag = env.SITE_TAGLINE
    desc = description or tag
    og_url = f"https://{getattr(env, 'CF_PAGES_URL', 'example.com')}{path}"
    ld = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": site,
        "jobTitle": "Coach",
        "description": desc,
        "url": og_url
    }
    head = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>{title} - {site}</title>
  <meta name="description" content="{desc}" />
  <meta property="og:title" content="{title} - {site}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{og_url}" />
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"/>
  <link rel="stylesheet" href="/styles.css" />
  <script type="application/ld+json">{json.dumps(ld)}</script>
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="shell">
    <a class="brand" href="/">{site}</a>
    <nav aria-label="Primary">
      <a href="/services.html">Services</a>
      <a href="/about.html">About</a>
      <a href="/intake.html">Start</a>
      <a class="cta" href="/contact.html">Contact</a>
    </nav>
  </header>
  <main class="shell" id="main">
"""
    foot = f"""
  </main>
  <footer class="shell">
    <p>(c) {site} - {tag}</p>
    <nav aria-label="Legal">
      <a href="/privacy.html">Privacy</a> · <a href="/terms.html">Terms</a>
    </nav>
  </footer>
  <script src="/app.js" defer></script>
</body>
</html>
"""
    return html_response(head + body + foot)

def page(env, name: str):
    sections = {
      "index": render_html("index", {"tagline": env.SITE_TAGLINE}),
      "services": render_html("services"),
      "about": render_html("about"),
      "contact": render_html("contact"),
      "intake": render_html("intake"),
      "privacy": render_html("privacy"),
      "terms": render_html("terms"),
    }
    body = sections.get(name, "<h1>Page</h1>")
    return base(env, name.title(), body, path=f"/{name}")
