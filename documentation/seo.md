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
`llms.txt` is deferred: Google Search does not use it for visibility or rankings.

References:
- https://developers.google.com/search/docs/appearance/structured-data/organization
- https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- https://developers.cloudflare.com/pages/configuration/redirects/
