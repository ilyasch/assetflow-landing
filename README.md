# AssetFlow landing page (myassetsflow.com)

A single, static, dependency-free marketing page for `myassetsflow.com`. It
acts as the portfolio hub for the AssetFlow platform across its four editions:
- **AssetFlow Home**: Personal / household assets (appliances, electronics, vehicles, equipment, home systems). Active and links to the live app at `https://myassetsflow.app`.
- **AssetFlow Business**: General organizational assets (restaurants, bakeries, offices, retail stores, workshops, factories) in a multi-tenant B2B architecture (Coming Soon).
- **AssetFlow Hospitality**: Specialized hotel and resort operations (hotels, resorts, aparthotels, accommodations) with multi-property oversight (Coming Soon).
- **AssetFlow Fleet**: Specialized vehicle and equipment operations (car rentals, delivery vans, corporate cars, trucks, machinery fleets) with interval tracking (Coming Soon).

It contains **no app screens, sign-up forms, or dashboards** — those live in the separate `AssetFlow` app repo.

This repository is intentionally independent from the other AssetFlow repos
(`AssetFlow`, `assetflow-worker`, `assetflow-infrastructure`,
`assetflow-database`). It does not touch production schema, secrets, or GCP
infrastructure.

## Structure

```
index.html        Single-page markup, portfolio hub, all sections, data-i18n keys
styles.css        All styling (mobile-first, no build step)
main.js           Locale loading/switching, RTL toggle, pricing edition & period toggle
locales/*.json    Translated copy for en, it, de, es, fr, ar (ar = RTL)
assets/           Logo/favicon (SVG, no external images)
```

No build tooling, package manager, or framework is required — this is plain
HTML/CSS/JS so it can be uploaded directly to static hosting.

## Visual blog guides

The header’s Blog link opens a separate article index, with five guides in
all six supported languages (30 static article pages and six localized
indexes). The homepage contains no article-preview section. The four edition stories cover a family car, a
food-production factory, a rental fleet, and a hotel. The featured practical
guide addresses a used car with missing service records. All records and
diagrams are illustrative; Business, Fleet, Hospitality, professional roles,
and QR workflows remain clearly labeled previews.

Article sources live in `content/blog/{en,it,de,es,fr,ar}.json`. Each article
has five sections and three semantic visual explanations. Keep evidence-based
guidance, translated labels, examples, related links, and availability notices
consistent across languages. Do not present examples as customer testimonials
or product screenshots.

After editing article content, run:

```bash
python3 scripts/build-blog.py --update-landing
bash scripts/package-site.sh
```

The first command refreshes the six landing navigation labels, local blog
indexes, article previews, and sitemap. Generated `/blog/` HTML is ignored
by Git. Packaging generates the full articles into `dist/`, versions shared
assets across all pages, and verifies links, localized indexes, article
structure, canonical URLs, language alternates, JSON-LD, and sitemap coverage.
CI runs the same package command. Publish the complete `dist/` artifact rather
than copying the source root. Article pages are readable without JavaScript;
their language links navigate directly to equivalent translated pages.

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

## Cloudflare Pages migration (prepared)

A GitHub Actions pipeline is prepared in `.github/workflows/cloudflare-pages.yml`.
Pull requests validate/package the site; pushes to `main` deploy the public
artifact after Cloudflare credentials and the Pages project are configured.
GitHub Pages remains the current host until the migration is verified.

Follow [Cloudflare Pages setup and domain cutover](documentation/cloudflare-pages.md).
The apex domain requires Cloudflare nameservers; GoDaddy can remain the registrar.

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
