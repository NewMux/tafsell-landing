# Tafsell landing page

Standalone marketing site for Tafsell. Plain HTML/CSS/JS, no build step, no
dependency on the ERP codebase — visitors can only book a demo here, they
never reach any ERP login.

## Editing

- `index.html` — page content and structure.
- `styles.css` — all styling (light/dark aware).
- `script.js` — the "Book a demo" form and the sales contact email
  (`SALES_EMAIL` — update this before launch).
- `assets/` — logo files. Replace `tafsell-logo-192.jpg` /
  `tafsell-logo-512.jpg` with a real logo when you have one.

## Local preview

Any static file server works, e.g.:

```bash
npx serve .
```

## Deploy

This is a static site — connect the repo to Vercel, Netlify, GitHub Pages,
or any static host, point your domain at it, and it just works. No build
command or output directory needed (or set them to a no-op / this
directory, depending on the host).
