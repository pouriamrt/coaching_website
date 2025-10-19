# Coachsite — Python Worker on Cloudflare
Elegant coaching website using Cloudflare Workers (Python beta) + static assets + D1 (leads) + KV (newsletter + rate limit).

## Features
- Accessible, responsive UI with dark palette
- SEO: meta tags, OpenGraph, JSON-LD, robots.txt, sitemap.xml, favicon
- Forms: Contact, Intake, Newsletter (with honeypot anti-spam)
- API: `/api/contact`, `/api/intake`, `/api/newsletter`
- Storage: D1 tables; KV for newsletter & rate-limit counters
- Security: Simple IP rate-limiting via KV, CORS for APIs
- CI/CD: GitHub Action -> Cloudflare Workers
- Pure stdlib Python for portability

## Local dev
```bash
npm i -g wrangler
wrangler dev
```

## Cloudflare setup
- Create a D1 database named `coaching_db` and replace `database_id` in `wrangler.toml`.
- Create a KV namespace and replace its `id` in `wrangler.toml`.
- Initialize tables once:
```bash
wrangler d1 execute coaching_db --file=schema.sql
```
- Add GitHub repo secrets: `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`.
- Push to `main` to deploy.

## Env vars (wrangler.toml [vars])
- `SITE_NAME`, `SITE_TAGLINE`, `CONTACT_EMAIL`
- `RATE_LIMIT_WINDOW_SECONDS` (default 600), `RATE_LIMIT_MAX_REQUESTS` (default 10)

## Notes
- To add email notifications, integrate an Email API in `Router` and store credentials in secrets.
