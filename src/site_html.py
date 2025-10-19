# src/site_html.py
import json
from utils import html_response

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
        "index": f"""
<section class="hero">
  <h1>{env.SITE_TAGLINE}</h1>
  <p>1:1 coaching for ambitious builders, analysts, and researchers. Practical systems, measurable outcomes.</p>
  <div class="row gap">
    <a class="btn" href="/intake.html">Book intake</a>
    <a class="btn ghost" href="/services.html">Explore services</a>
  </div>
</section>

<section class="grid two">
  <div>
    <h2>What we’ll build</h2>
    <ul class="bullets">
      <li>Positioning that opens doors</li>
      <li>Weekly cadence that compounds</li>
      <li>Deliverables that speak for you</li>
    </ul>
  </div>
  <div class="card">
    <h3>Newsletter</h3>
    <p>Occasional insights on focus, careers, and shipping work that matters.</p>
    <form id="newsletterForm" class="form mini" aria-label="Newsletter signup">
      <input aria-label="Email address" type="email" name="email" placeholder="you@example.com" required />
      <input type="text" name="website" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true" />
      <button class="btn" type="submit">Subscribe</button>
    </form>
    <p class="note" id="newsletterMsg" role="status" aria-live="polite"></p>
  </div>
</section>""",
        "services": """
<section>
  <h1>Services</h1>
  <ul class="cards">
    <li><h3>Career Strategy (4 weeks)</h3><p>Positioning, portfolio, and interview prep tailored to tech & data roles.</p></li>
    <li><h3>Productivity Systems (4 weeks)</h3><p>Workflows, automation, and weekly cadences you actually stick to.</p></li>
    <li><h3>Research Coaching (ongoing)</h3><p>Scoping, writing pipeline, and publication strategy. Calm, consistent progress.</p></li>
  </ul>
</section>""",
        "about": """
<section>
  <h1>About</h1>
  <p>I help technical people ship the next level without sacrificing their health or relationships.</p>
  <p>Expect candor, structure, and momentum. No fluff.</p>
</section>""",
        "contact": """
<section>
  <h1>Contact</h1>
  <form id="contactForm" class="form" aria-label="Contact form">
    <label>Name<input name="name" required /></label>
    <label>Email<input name="email" type="email" required /></label>
    <label>Message<textarea name="message" rows="5" required></textarea></label>
    <input type="text" name="website" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true" />
    <button class="btn" type="submit">Send</button>
    <p class="note" id="contactMsg" role="status" aria-live="polite"></p>
  </form>
</section>""",
        "intake": """
<section>
  <h1>Start the Intake</h1>
  <form id="intakeForm" class="form" aria-label="Intake form">
    <label>Full name<input name="full_name" required /></label>
    <label>Email<input name="email" type="email" required /></label>
    <label>Primary goal<input name="goal" placeholder="e.g., land a data role in 90 days" required /></label>
    <label>Timeline<input name="timeline" placeholder="e.g., 3 months" required /></label>
    <label>Details (optional)<textarea name="details" rows="4"></textarea></label>
    <input type="text" name="website" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true" />
    <button class="btn" type="submit">Submit</button>
    <p class="note" id="intakeMsg" role="status" aria-live="polite"></p>
  </form>
</section>""",
    }
    body = sections.get(name, "<h1>Page</h1>")
    return base(env, name.title(), body, path=f"/{name}")
