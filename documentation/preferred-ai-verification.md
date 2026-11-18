> Final security/category review: all six languages passed home + Find your fit
> at 360/768/1135 px (36 page/viewport cases), with no document overflow.
> Business selection hides Home categories; Home restores them in every case.
> All six mini icons, Library rail labels, Security sections and localized AI
> links are present. Static Home categories and EU guidance links also verified.
> Packaging and whitespace checks pass; all changes remain uncommitted.

> Security & ownership: verified access/review/redaction controls against app and
> worker sources; legal-readiness-todo.md still requires formal AI Act review.
> Marketing therefore explains concrete controls and Article 50 transparency,
> linking the European Commission's current guidance without claiming compliance
> certification. Source checked 18 November 2026:
> https://digital-strategy.ec.europa.eu/en/policies/guidelines-ai-transparency-obligations
> Sidebar includes Security and renames Records to Library. The six original
> category SVGs are reused in the homepage mini example. The category overview
> moves to Home on Find your fit and hides for other selected editions.

> Flow AI is now the fifth homepage demo tab after Cost Explorer. Its agentic
> example connects a question, illustrative document/public-manual references,
> and a proposed checklist requiring review. Extra prompts cover warranty and
> recurring repair costs. Public research and reference support were checked in
> worker knowledge/chat/agent.py. No actual retrieval or provider acceptance is
> implied by the illustrative transcript. Six languages passed 360/768/1135 px
> checks with no page overflow. Arrow navigation, the Cost Explorer next-view
> button and the final link to /ai/en/ were verified. Static localized content
> and all six AI links were checked. Packaging passes: 2,660 local references.

> Follow-up: removed the reporting-details disclosure at user request. Totals
> now use a shallow label/value strip. Actual spending and forecast ranges retain
> their explicit periods and estimate labels; charts remain illustrative.
> Earlier disclosure and missing-cost UI notes below describe previous versions.

> Cost Explorer refinement: renamed the homepage cost view in all six languages.
> Slimmer bars, a shared forecast range axis and three translated takeaways
> replace the taller chart presentation. Native expandable notes retain missing
> cost and reporting-scope details. Six languages passed 360/768/1440 px checks;
> the exact 1135 px review width also passed without horizontal overflow.
> Keyboard Enter toggles the explanation correctly. Packaging and diff checks pass.

> Cost Insights homepage addition: checked against the app's maintenance-insights
> reporting contract. Three static, accessible charts compare completed spending
> by asset/category and forecast approved outstanding estimates. Sample totals
> reconcile to EUR 960; monthly ranges sum to EUR 240–400. Missing amounts and
> separate currencies are explicit. All six languages passed 360/768/1440 px
> checks: three charts, visible Insights panel and no page overflow. Library now
> shows one PDF plus JPG/DOCX/PNG examples; the label omits “sample data”.
> Asset details are retained in a shorter panel. No runtime API changes.

> Homepage demo refinement: numbered, outlined tabs and next-view buttons invite
> exploration. Labels are Smart plan and Library in all six languages. Library
> illustrates a source-backed finding awaiting confirmation, private files and
> conditional file eligibility. Smart plan describes editable drafts and
> extraordinary events without a fixed generation-time promise. Product basis:
> app capabilities-and-roadmap (reviewed findings) and maintenanceTypes
> (ordinary/extraordinary classification). Browser checks passed at 360, 768
> and 1440 px in six languages with no document overflow. Desktop and Arabic
> mobile arrow-key navigation and local review/confirm/reset were verified.
> Static panels remain readable without script; navigation controls require JS.
> Packaging passes. Guide remains deferred; changes remain uncommitted.

> Editorial navigation update: the site navigation uses Guides as its localized
> one-word label. The guides index links explicitly to AssetFlow's localized
> homepage, and the blog index links to Guides. Keyboard/mouse navigation between
> these pages was verified. All six languages were checked at mobile, tablet and
> desktop widths with no document overflow. Packaging passes with 91 sitemap
> entries and 2,653 local references. Changes remain uncommitted.

> Find your fit layout refinement: two equal-height journey cards introduce
> edition selection and Home plans. Home's edition action leads to pricing;
> unavailable editions retain enquiries. The palette is green and white, with
> pale gradients and forest-green pricing behind separate white plan cards.
> Prices and limits are unchanged; annual/monthly activation was checked.
> All six locales passed at 360, 768 and 1440 px (18 combinations): equal journey
> card heights and no document overflow, including Arabic RTL. Packaging passes
> with 91 sitemap entries and 2,640 local references. Changes remain uncommitted.

> Latest focused refinements: provider examples now have transparent backgrounds
> and include ChatGPT, Claude, Mistral Vibe (Le Chat), Codex CLI and custom tools
> with compatible remote MCP clients. Per-provider/account availability remains
> explicit. The selected edition table omits the repeated visual header row,
> retaining the semantic header cells and the complete no-script comparison.
> Packaging passes with 91 sitemap entries and 2,634 local references. All changes
> remain uncommitted; the setup guide remains deferred.

> Latest review: AI visuals now use the original ChatGPT/OpenAI, Claude and MCP
> marks, with provenance in `assets/brands/SOURCES.md`. The dark-green security
> section illustrates selected assets, read-only permission and revocation. The
> workflow example shows a synthetic car question, record context, a draft and
> an explicit review boundary. Neither illustration operates account settings.
>
> Solutions and pricing are merged as **Find your fit**, `/explore/{locale}/`,
> with editions first and Home pricing second. All 12 legacy-page redirects were
> verified in the local browser. Edition switching and monthly/annual controls
> were checked with keyboard activation. Layout checks covered the new AI
> sections and combined page at mobile/tablet widths, with a separate 1440 px
> desktop pass across all six languages; no document overflow was observed.
> Packaging passes: 91 sitemap entries and 2,628 local references. Earlier counts
> and separate-page notes below are historical. No publication or commit made.

> Browser-comment updates: the homepage hero now links AI integration to agentic
> work. The section rail was reproduced appearing while How AssetFlow works was
> still 675 px below the viewport top; after the fix it stays hidden there and
> activates at the 110 px reading position with How it works selected. The AI
> links now use colored cards, the existing AssetFlow mark and decorative icons.
> Updated home and AI pages were checked in six languages at 390, 768 and 1440
> pixels (36 combinations), with no horizontal overflow. Packaging passes with
> 97 sitemap entries and 2,816 local references. The guide remains deferred.

> Updated scope, 18 November 2026: the connector is presented in present tense.
> Flow AI and external-assistant integrations now live on `/ai/{locale}/`, with
> security controls and reviewable agentic-work sections. All six homepages link
> to AI instead of containing those sections. No setup-guide CTA is shown; the
> guide remains deferred. Packaging now verifies 97 sitemap entries and 2,803
> local references. The AI page was checked in all six languages at 390, 768,
> 1024 and 1440 pixels: correct language/direction, one main heading, all four
> sections present and no horizontal page overflow. Earlier homepage-section
> evidence below is historical.

# Preferred AI feature and setup guide — review evidence

Date: 18 November 2026. Repository: `assetflow-landing` only. Baseline: current
`main`, `3771380` (remote refs fetched before editing). All changes are uncommitted.
No publication, connector runtime/configuration change or release acceptance is
implied. The user requested present-tense messaging for the implemented connector.

## Scope and source of product claims

S08 in `assetflow-mcp/docs/implementation-plan.md` requires localized feature
communication and setup, examples, exclusions, controls, disconnection and
troubleshooting. The compatibility register still records unfinished provider
acceptance; the landing change does not alter that register or its gates.

Reviewed implementation sources (read-only):

- `assetflow-mcp/src/assetflow_mcp/tools.py`: `list_assets`, `get_asset`,
  `list_tasks` and `list_task_schedules` are the relevant read surface.
- `assetflow-mcp/src/assetflow_mcp/models.py` and `schedule_models.py`: structured
  asset and task/schedule fields. No document-reading or write promise is made.
- `AssetFlow/src/features/settings/ExternalAiConnections.tsx`,
  `externalAiI18n.ts` and `assets/AssetEditor.tsx`: explicit connection consent,
  asset-wide sharing for every connected assistant (including later-enabled
  assets), related tasks, disconnect and reconnect instructions.
- Real DEV asset editor and External AI connections settings in the existing
  synthetic QA account. The edit dialog was closed without saving.

Product messaging names ChatGPT and Claude as examples, not a compatibility
certification. It explains approval, selected assets, read-only access, revocation
and provider policies. Imports and writes are planned. Revocation does not erase
previously transmitted information. No production MCP endpoint is invented.

## Provider documentation checked

These establish provider instructions, not successful AssetFlow integration.
Account tiers and controls can change; recheck before completing screenshots.

| Exact surface | Official source | Findings and verification gap |
| --- | --- | --- |
| ChatGPT web | [Connecting custom MCP servers](https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt) | Current Plugins flow, legacy Apps flow, Business/Enterprise/Edu workspace permissions, Pro read/fetch. No Plus/Free support promise. The available browser session initially showed Log in. Authorization, account tier and tool results unverified. |
| Claude web | [Custom connectors](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp) | Remote MCP, Free limited to one custom connector, paid and managed-plan controls. Customize → Connectors; OAuth identity choices depend on server requirements. Initial session was at login. Account-specific options and authorization unverified. |
| Mistral Le Chat / Vibe web | [MCP Connectors](https://docs.mistral.ai/vibe/work/web/connectors/mcp-connectors), [name change](https://help.mistral.ai/en/articles/682992-le-chat-is-now-vibe) | Web Work, administrator requirement; Free/Pro/Student owners are administrators by default. Connectors → Add Connector → Custom MCP Connector. The initial session required sign-in and subsequently showed a terms dialog. No terms accepted. Account-specific connection and OAuth unverified. |
| Codex CLI | [MCP CLI documentation](https://learn.chatgpt.com/docs/extend/mcp?surface=cli), [account availability](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan) | Streamable HTTP/OAuth, add/login/list/logout/remove commands. CLI model access is separate from connector authorization and Cloud availability. Installed CLI is 0.169.0; version and MCP help/add help checked. No endpoint/client configured or login attempted. |

## Screenshot coverage

One real app capture is included as two responsive JPEG variants, with six
translated captions and alt texts and an explicit English UI label. See
`assets/guides/SOURCES.md`. The frame contains a synthetic name and the existing
sharing control; no credentials, deployment addresses, private records or provider
success screen is published.

All four provider walkthroughs are intentionally **unfinished**, with visible
localized notices. Missing: exact account/tier availability, provider setup forms,
completed consent, discovered tool/result screenshots and reconnect/revocation
journeys. Provider sign-in was requested. The DEV app does not display a setup
endpoint; approved DEV endpoint/client instructions were also requested. Do not
invent client IDs, callbacks, tokens, success screens or production values.

## Site verification

`bash scripts/package-site.sh` passes, including JavaScript syntax, six locale
catalogs, full static generation, content-addressed screenshots and site verification:
36 existing blog articles, 91 sitemap entries and 2,467 local references.
`git diff --check` passes. No application or infrastructure tests were run because
only the static landing repository changes.

The verifier checks four guides per locale, equivalent article language links,
canonical/description/Open Graph metadata, source screenshots, responsive image
attributes, static guide content and absence of development endpoint values.
Static homepage routes `/en/`, `/it/`, `/de/`, `/es/`, `/fr/` and `/ar/` contain
translated content and metadata before scripts execute. Their language selection
navigates to a fully rendered route; the root keeps its existing locale behavior.
No-script visitors get native homepage language links. Guide pages contain no
scripts, and their contents, table of contents and language menu are native HTML.
No-JavaScript verification is based on generated HTML and CSS; a browser-level
JavaScript-disabled session was not available through the browser control API.

Browser layout checks covered the feature and guide in all six languages at 390,
768 and 1440 CSS pixels (36 route/viewport combinations). All had the expected
language/direction, zero horizontal document overflow and no broken loaded images.
Screenshots were captured for each combination and representative views were
reviewed. Two findings were corrected: mobile guide header labels needed two rows,
and the feature heading needed its own layout rather than the shared two-column
heading grid. A further feature pass covered all 18 locale/viewport combinations.

Keyboard checks passed on all six guides: Enter activates Skip to content,
Enter opens the native language menu, and Enter on English preserves the article
route. Existing visible focus styles are retained. This is a focused keyboard
review, not a complete WCAG audit or screen-reader certification.

Temporary review screenshots are under `/private/tmp/preferred-ai-review/`.
Provider-dependent acceptance remains open; do not mark S07/S08 complete or publish
on the strength of these static-site checks.
