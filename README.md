# Tafsell landing page

Standalone marketing site for Tafsell, powered by NewMux, in English (`/`)
and Arabic (`/ar/`, right-to-left). Plain HTML/CSS/JS, no build step.
Tafsell is sold through demos and service agreements: prospects book a demo
here (there is no sign-up), and existing customers use the "Sign in" link to
the app at `https://app.tafsell.com/`.

## Editing

- `index.html` — English page content and structure.
- `ar/index.html` — **generated**; don't edit it by hand. After any change to
  `index.html`, run `python3 tools/make-ar.py`. Arabic copy lives in that
  script as English → Arabic pairs; it stops with an error if an English
  string it expects has changed, so the two pages can't drift apart.
- `styles.css` — all styling. Uses logical properties (`padding-inline-start`,
  not `padding-left`) so the same rules work right-to-left; RTL-only tweaks
  are at the end.
- `script.js` — the "Book a demo" form and the sales contact email
  (`SALES_EMAIL`).
- `assets/` — logo files and `og-image.png` (1200×630, the preview card
  shown when the site is shared on WhatsApp, LinkedIn, X, etc.).
- `robots.txt`, `sitemap.xml` — for search engines; list both languages.

## "Book a demo" form

The form posts JSON to `https://app.tafsell.com/api/public/demo-request`
(Tailor-saas, `server/_core/demoRequests.ts`), which stores the request and
emails it to the sales inbox with Reply-To set to the prospect. Only
`tafsell.com` and `www.tafsell.com` are allowed to call it, so the form fails
on Vercel preview URLs (it then shows the sales email instead). On a local
preview it calls `http://localhost:3000`, i.e. a local copy of the app.

## Analytics

`/_vercel/insights/script.js` is Vercel Web Analytics (no cookies). Turn it
on under the Vercel project → **Analytics**. Each successful form submission
is recorded as a "Demo request" custom event, split by page language.

## Local preview

```bash
python3 -m http.server 5000   # or: npx serve .
```

## Deploy

Vercel project `tafsell-landing`; pushing to `main` deploys `tafsell.com`.
`vercel.json` sets the security headers and Content-Security-Policy;
`.vercelignore` keeps `tools/` and this README off the site.
