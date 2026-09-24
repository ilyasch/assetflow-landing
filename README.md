# AssetFlow landing page (myassetsflow.com)

A single, static, dependency-free marketing page for `myassetsflow.com`. It
explains AssetFlow, shows real pricing, and sends visitors to the actual
product at `https://myassetsflow.app`. It contains **no app screens, sign-up
forms, or dashboards** — those live in the separate `AssetFlow` app repo.

This repository is intentionally independent from the other AssetFlow repos
(`AssetFlow`, `assetflow-worker`, `assetflow-infrastructure`,
`assetflow-database`). It does not touch production schema, secrets, or GCP
infrastructure.

## Structure

```
index.html        Single-page markup, all sections, data-i18n keys
styles.css        All styling (mobile-first, no build step)
main.js           Locale loading/switching, RTL toggle, pricing toggle
locales/*.json    Translated copy for en, it, de, es, fr, ar (ar = RTL)
assets/           Logo/favicon (SVG, no external images)
```

No build tooling, package manager, or framework is required — this is plain
HTML/CSS/JS so it can be uploaded directly to static hosting.

## Local preview

Because `main.js` fetches locale JSON files, open it through a local static
server rather than a `file://` URL (browsers block `fetch` on `file://`):

```bash
cd assetflow-landing
python3 -m http.server 8080
# then open http://localhost:8080
```

Check each language in the selector (including Arabic, which should switch
the page to right-to-left), the monthly/annual pricing toggle, and that both
"Go to AssetFlow" buttons link to `https://myassetsflow.app`.

## Content sources (keep in sync)

- Pricing figures come from `AssetFlow/documentation/product/payments-and-pricing.md`.
  If the catalog changes, update `locales/en.json` (`pricing.*`) first, then
  mirror the change into every other locale file.
- Supported languages mirror the app's confirmed locales (`en, it, de, es,
  fr, ar`) per the same document and
  `AssetFlow/documentation/product/capabilities-and-roadmap.md`. Do not add a
  language here until the app has actually shipped it.
- Security/privacy copy intentionally uses bracketed placeholders
  (`[confirm hosting region]`, `[insert verified security and privacy
  details]`) because hosting region and formal certifications are not yet
  verified (see
  `AssetFlow/documentation/governance/security-and-compliance-roadmap.md`).
  Replace the placeholders only once those facts are confirmed — do not
  invent certifications, regions, or guarantees.
- Privacy/terms links point at the real app pages (`myassetsflow.app/privacy`,
  `myassetsflow.app/terms`) instead of duplicating legal text here.

## Deploying for free (recommended: Cloudflare Pages)

GoDaddy's own hosting requires a paid plan for a static site, so the
recommended path is to keep the **domain and DNS at GoDaddy** but host the
static files for free on **Cloudflare Pages** (the same platform already
used for the real `myassetsflow.app` product domain, per
`AssetFlow/documentation/technology/solution-architecture.md`).

### 1. Deploy the site to Cloudflare Pages (no Git or CLI required)

1. Create a free Cloudflare account at <https://dash.cloudflare.com/sign-up>
   if you don't have one.
2. In the dashboard, go to **Workers & Pages → Create → Pages → Upload
   assets**.
3. Give the project a name (e.g. `assetflow-landing`) and drag-and-drop the
   contents of this folder (`index.html`, `styles.css`, `main.js`,
   `assets/`, `locales/`) — keep the folder structure intact.
4. Click **Deploy site**. Cloudflare gives you a working URL like
   `https://assetflow-landing.pages.dev` — open it and confirm the page
   loads, every language works, and both CTA buttons go to
   `https://myassetsflow.app`.

(If you prefer Git-based deploys later, connect this folder as a GitHub repo
and use **Workers & Pages → Create → Pages → Connect to Git** instead — no
build command is needed since this is plain static HTML/CSS/JS.)

### 2. Point myassetsflow.com at the Cloudflare Pages project

You can do this two ways:

**Option A — keep DNS at GoDaddy (simplest, no nameserver change):**
In the Pages project, go to **Custom domains → Set up a custom domain**,
enter `myassetsflow.com` (and `www.myassetsflow.com` if wanted). Cloudflare
will show you a DNS record to add (usually a `CNAME` for `www` pointing at
`assetflow-landing.pages.dev`, and for the bare/apex domain either a CNAME
flattening record or an A record with an IP Cloudflare provides). Add that
exact record in **GoDaddy → Domain → DNS → Manage DNS** for
`myassetsflow.com`.

**Option B — move DNS to Cloudflare (full CDN/SSL, matches myassetsflow.app):**
Add `myassetsflow.com` as a site in Cloudflare, which gives you two
Cloudflare nameservers. In GoDaddy → **Domain → Manage → Nameservers**,
switch to those Cloudflare nameservers. Once propagated (can take a few
hours), attach the custom domain to the Pages project from the Cloudflare
dashboard — Cloudflare manages DNS and SSL automatically from then on.

Either way, Cloudflare issues free HTTPS automatically once the domain is
verified — no separate SSL purchase needed.

### 3. Verify

After DNS propagates (check with `dig myassetsflow.com` or just reload in a
browser — can take minutes to a few hours):

- `https://myassetsflow.com` loads over HTTPS with a valid certificate.
- Every language in the selector renders correctly, Arabic switches to RTL.
- The header, hero, pricing, and closing "Go to AssetFlow" buttons all link
  to `https://myassetsflow.app`.

## Alternative: paying for GoDaddy's own static hosting

If you'd rather keep everything inside GoDaddy (including hosting), buy a
GoDaddy **Web Hosting** plan (their cheapest "Economy"/shared plan is enough
for one static page), then follow the steps below instead of the Cloudflare
Pages steps above.


1. In your GoDaddy account, open **My Products → Web Hosting** for the plan
   attached to `myassetsflow.com` (or purchase a GoDaddy hosting plan if none
   exists yet).
2. Use GoDaddy's **File Manager** (or an SFTP client with the credentials
   shown in the hosting dashboard) to upload the contents of this folder
   (`index.html`, `styles.css`, `main.js`, `assets/`, `locales/`) into the
   site's public web root (commonly `public_html/`). Keep the folder
   structure intact — `main.js` expects `locales/` and `assets/` as
   siblings of `index.html`.
3. In GoDaddy's **Domain → DNS** settings for `myassetsflow.com`, make sure
   the domain's A record (and `www` CNAME, if you want `www.myassetsflow.com`
   to work) points at the IP/hosting target GoDaddy's hosting dashboard
   specifies for that hosting plan. GoDaddy hosting plans normally set this
   automatically when the domain and hosting plan are linked in the same
   account — check the hosting dashboard's "Manage DNS" or "Domain settings"
   link first before editing records by hand.
4. Enable free HTTPS/SSL for the domain from the hosting dashboard if it is
   not already active, and confirm `https://myassetsflow.com` loads the page
   over HTTPS before sharing the link.
5. After DNS propagates, verify: the page loads over HTTPS, every language in
   the selector renders (Arabic in RTL), and both "Go to AssetFlow" buttons
   navigate to `https://myassetsflow.app`.

DNS management stays at GoDaddy for this domain; there is no Cloudflare
migration involved (that setup is specific to `myassetsflow.app`, the actual
product domain, and is owned by `assetflow-infrastructure`).
