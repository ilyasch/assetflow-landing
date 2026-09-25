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
- The page positions the customer as the hero: the visitor adds an asset,
  reviews a smart maintenance plan, confirms what fits their life, and builds
  a useful ownership history. Keep examples grounded in familiar household
  moments and specific assets rather than generic feature claims.
- The document-library section presents asset documents, event-linked evidence,
  receipts, and service records as part of the ownership workflow. Keep the
  wording aligned with the product's actual document and attachment behavior.
- The smart-plan section should emphasize reviewable AI drafts generated from
  the user's asset context. Calendar copy must distinguish the current
  iCalendar (`.ics`) download from connected-calendar synchronization, which is
  planned rather than currently connected.
- Supported languages mirror the app's confirmed locales (`en, it, de, es,
  fr, ar`) per the same document and
  `AssetFlow/documentation/product/capabilities-and-roadmap.md`. Do not add a
  language here until the app has actually shipped it.
- Security/privacy copy may describe the current development deployment as
  using European infrastructure, based on
  `AssetFlow/documentation/technology/solution-architecture.md`. Do not turn
  that into a certification, a GDPR/compliance guarantee, or a production
  hosting promise without verifying the target deployment and privacy
  documentation.
- Privacy/terms links point at the real app pages (`myassetsflow.app/privacy`,
  `myassetsflow.app/terms`) instead of duplicating legal text here.

## Deployed: GitHub Pages (already set up)

The site is deployed and live-building on **GitHub Pages**, for free, at:

- Repository: <https://github.com/ilyasch/assetflow-landing> (public — required
  for free GitHub Pages; contains only this static marketing site, no
  secrets)
- Default URL: <https://ilyasch.github.io/assetflow-landing/> (redirects to
  the custom domain once DNS is configured, because of the `CNAME` file at
  the repo root)
- Pages source: `main` branch, root folder — GitHub Pages serves the static
  files directly, no build step

### What's already done

1. Code pushed to `main` on the `ilyasch/assetflow-landing` GitHub repo.
2. A `CNAME` file containing `myassetsflow.com` was added at the repo root,
   which tells GitHub Pages the intended custom domain.
3. GitHub Pages was enabled via the repo's Pages API (source: `main` / `/`)
   and the first build completed successfully (`status: "built"`).

### What you still need to do: point GoDaddy DNS at GitHub Pages

In **GoDaddy → Domain → DNS → Manage DNS** for `myassetsflow.com`, add:

| Type | Name | Value |
|---|---|---|
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| CNAME | `www` | `ilyasch.github.io` |

These are GitHub's standard, stable Pages IPs for apex/root domains. Remove
any existing GoDaddy "parked domain" A record or forwarding rule for
`myassetsflow.com` first — it will conflict with these.

Then, in the GitHub repo's **Settings → Pages**, confirm the custom domain
shows `myassetsflow.com` with a green "DNS check successful" (this can take
a few minutes to a few hours after adding the records), and enable
**Enforce HTTPS** once it becomes available (GitHub issues a free
Let's Encrypt certificate automatically after DNS is verified).

### Verify

- `https://myassetsflow.com` loads over HTTPS with a valid certificate.
- Every language in the selector renders correctly, Arabic switches to RTL.
- The header, hero, pricing, and closing "Go to AssetFlow" buttons all link
  to `https://myassetsflow.app`.

### Redeploying after future changes

Any push to `main` on `ilyasch/assetflow-landing` automatically rebuilds and
republishes the Pages site — no manual redeploy step needed.

## Alternative: Cloudflare Pages

GoDaddy's own hosting requires a paid plan for a static site. If you'd
rather use Cloudflare Pages instead of GitHub Pages (for example, to later
share the same CDN/WAF setup as the real `myassetsflow.app` product domain,
per `AssetFlow/documentation/technology/solution-architecture.md`), here is
that path:

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

(You can also connect the `ilyasch/assetflow-landing` GitHub repo directly
via **Workers & Pages → Create → Pages → Connect to Git** instead of
uploading manually — no build command is needed since this is plain static
HTML/CSS/JS.)

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
