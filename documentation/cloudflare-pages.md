# Cloudflare Pages deployment

The landing site is currently served by GitHub Pages. This repository prepares
a separate Cloudflare Pages Direct Upload deployment; DNS cutover is not done.

## One-time setup

1. In Cloudflare Workers & Pages, create a **Pages Direct Upload** project named
   `assetflow-landing` with production branch `main`. Do not enable a second
   Git integration deployment path. Direct Upload projects cannot later switch
   to Git integration in place.
2. Create a custom API token with **Account → Cloudflare Pages → Edit**, scoped
   to the specific account. Use an API token rather than the Global API Key.
3. In `ilyasch/assetflow-landing` → Settings → Environments → `production`, add:
   - Secret `CLOUDFLARE_API_TOKEN`: the token from step 2.
   - Variable `CLOUDFLARE_ACCOUNT_ID`: the target account ID from Cloudflare.
   The deploy job selects this environment and follows its protection rules.
4. Merge the workflow into `main`, or run **Cloudflare Pages** manually on
   `main` after secrets are configured.

Pull requests validate JavaScript syntax, all six locale JSON files, and package
the static assets without deployment credentials. Pushes to `main` deploy that
same artifact to production. Manual runs deploy only when run from `main`.
Only public files are copied to `dist/`; `.git`, documentation, scripts, and the
GitHub Pages `CNAME` file are excluded. Pages Function source stays at the
project root so Wrangler can bundle it with the static deployment. The deploy
job checks out the source alongside the packaged artifact. There is no
application build step.

## Edition enquiry email

The Pages Function at `/api/contact` sends edition enquiries through Cloudflare
Email Service. Configure the following production Pages variables and secrets
before expecting the form to send:

- Variable `CF_ACCOUNT_ID`: the Cloudflare account ID.
- Variable `CF_EMAIL_FROM`: a sender address on a domain onboarded for Email
  Sending, such as `website@myassetsflow.com` after domain setup.
- Secret `CF_EMAIL_API_TOKEN`: a Cloudflare API token with Email Sending
  permission for the account.

Email Routing receives and forwards mail; it does not by itself enable website
sending. Email Sending is a separate service and the account must be entitled
to send to `contact@myassetsflow.com`. Cloudflare currently allows sending to
verified destination addresses on Free plans; arbitrary recipients require a
Workers Paid plan. Verify the destination and sender in Cloudflare before the
first hosted form acceptance check. The API token is read only by the Pages
Function and is never included in the static site artifact.

## Verify before moving DNS

Confirm the Actions deployment succeeds and open the project's `pages.dev` URL.
Check logo/CSS loading, all six languages including Arabic RTL, both pricing
periods, and links to `myassetsflow.app`, privacy, and terms. A packaged artifact
or a created project alone does not establish a working hosted deployment.

## Custom domain migration

The domain can remain registered with GoDaddy. For the apex `myassetsflow.com`,
Cloudflare Pages requires a Cloudflare DNS zone and Cloudflare nameservers.
Before changing nameservers, inventory and copy existing DNS records, including
MX, SPF, DKIM, DMARC, verification records, and other subdomains. Keep current
GitHub Pages website records while moving DNS authority, then confirm DNS works.
Handle DNSSEC according to the providers' nameserver migration instructions.

After the Pages URL passes verification, add `myassetsflow.com` in the project's
**Custom domains** screen and replace the conflicting GitHub Pages website
records with the Pages records Cloudflare provides. Also attach `www` if used,
and select one canonical hostname with a redirect from the other. Verify HTTPS,
language switching, pricing, and app links on the custom domain before retiring
GitHub Pages.

If keeping authoritative DNS at GoDaddy, use a subdomain such as
`www.myassetsflow.com`: associate it in Pages first, then set its GoDaddy CNAME
to the project's `pages.dev` hostname. This does not migrate the apex.

Keep a record of the former GitHub Pages DNS configuration for rollback. Before
the domain cutover, update the shared solution architecture, development visual
guide, and canonical diagram source in the separate app repository to record
the landing hosting/DNS change; the application `myassetsflow.app` edge stays
independent.

## References

- [Direct Upload CI and API-token permissions](https://developers.cloudflare.com/pages/how-to/use-direct-upload-with-continuous-integration/)
- [Direct Upload project setup](https://developers.cloudflare.com/pages/get-started/direct-upload/)
- [Custom domains and apex nameserver requirements](https://developers.cloudflare.com/pages/configuration/custom-domains/)
