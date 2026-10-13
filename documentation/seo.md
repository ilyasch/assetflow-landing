# Landing SEO

The homepage uses `https://myassetsflow.com/` as its canonical URL, with a
crawlable robots.txt, a one-page sitemap, Organization/WebSite/WebPage JSON-LD,
and Open Graph/X sharing metadata. Metadata follows the six language selections;
English remains the HTML fallback. The language selector does not yet create
separate indexable URLs; do not add hreflang annotations until those URLs exist.

The header wordmark is a 652-pixel WebP (about 24 KB), down from the original
373 KB PNG. The original PNG remains available as the organization logo.
The sharing image is a 1200 × 630 PNG using the existing brand artwork.
Cache headers use bounded lifetimes; assets are not marked immutable because
filenames are not content hashes. The script query version must change when
JavaScript changes. JavaScript remains deferred.

## Post-deployment verification

- Confirm the homepage, robots.txt, sitemap.xml and social-preview image return 200.
- Check canonical and JSON-LD in the served HTML.
- Test all six languages, Arabic RTL, pricing toggles and the app links.
- Submit `https://myassetsflow.com/sitemap.xml` in Google Search Console and
  inspect the homepage. Retain the existing DNS verification TXT record.
- Validate the structured data with Google's Rich Results Test and Schema.org
  validator. Organization/WebSite markup does not guarantee a rich result.
- Run mobile PageSpeed Insights and prioritize measured bottlenecks.

## Host redirects

Pages `_redirects` does not support domain-level redirects. Configure a zone
Single Redirect from `www.myassetsflow.com` to `https://myassetsflow.com`,
preserving path and query, with status 301. Use Cloudflare's account-level Bulk
Redirect for the production `assetflow-landing.pages.dev` hostname if desired.
Keep deployment preview hostnames separate. The repository redirects the
explicit `/index.html` path to `/`.

## Subsequent work

Create static localized language URLs and matching hreflang/sitemap entries;
then develop useful maintenance content and relevant external mentions.
Analytics needs a chosen provider/configuration. Business contact details and
LocalBusiness markup need real, applicable business information. No marketing
pixels or fictitious reviews, addresses, prices or certifications are included.
`llms.txt` provides public product context and links for AI assistants, with a
Markdown overview at `/index.md`. HTML discovery links point to both files.
The existing wildcard robots.txt rule permits crawlers, including search and
assistant bots; Cloudflare's bot policies can independently restrict them.
No special agent service or privileged integration is needed for this public
landing page. Keep Cloudflare Search/Agent blocking disabled for accessibility.
These discovery files do not grant access to private application data.
Google Search does not use llms.txt for visibility or rankings.

A root `404.html` disables Pages' default single-page-app fallback. Missing
discovery manifests such as `/.well-known/ai-catalog.json` should return 404,
not the homepage with status 200. This site does not publish an MCP/A2A service
catalog; its public product information is available through llms.txt/index.md.

References:
- https://developers.google.com/search/docs/appearance/structured-data/organization
- https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- https://developers.cloudflare.com/pages/configuration/redirects/

## Performance asset delivery

The deployment package writes content-hashed CSS, JavaScript, font and logo
files under `/static/` and updates the HTML/CSS references. Those immutable
URLs receive a one-year cache lifetime; editable source URLs keep shorter
lifetimes. Fonts are self-hosted WOFF2 subsets covering the current Latin
translations, with the existing Arabic fallback behavior. Licenses are stored
under `assets/fonts/`. Responsive logo candidates cover 1x, 2x and 3x displays.
The visible design and supported languages stay the same.
