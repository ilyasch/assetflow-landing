# AssetFlow landing

<!-- impeccable:product-schema 1 -->

## Platform
web

## Users
Households organizing ownership records and maintenance; businesses, vehicle-fleet operators, and hotel teams evaluating future editions.

## Product Purpose
Help visitors recognize their asset-management needs and understand how AssetFlow supports a reviewable maintenance plan and useful ownership history.

## Capabilities and Constraints
AssetFlow Home is available at https://myassetsflow.app. Business, Fleet, and Hospitality are Coming Soon. QR labels and professional role-based workflows in the articles are future-edition previews. AI maintenance drafts require human review. Calendar export is available; connected-calendar synchronization is planned.

The homepage leads with Home and an illustrative ownership example: Asset, Smart plan, Library, Cost Explorer and Flow AI tabs, followed by a local review, confirm and reset interaction. Confirmation creates no real reminder and sends no external data. Without JavaScript, all five example panels remain readable. The solutions section of the localized Find your fit page contains the Home, Business, Fleet and Hospitality edition comparison. Edition-specific icon marks pair each AssetFlow product name in the picker and table. Selecting an edition shows only the row-label column and that edition’s complete five-row profile, plus its availability and relevant start/enquiry action. The selector sits beside the profile on desktop, above it on tablet, and in a two-by-two grid on mobile. Selection stays in place without scrolling the page. Without JavaScript, the full semantic table remains readable with horizontal scrolling and a sticky first column. The following pricing section describes the Home plans and billing toggle. Planned editions and general questions open the same localized contact form, which sends through Resend and replies to the visitor’s provided email. The closing section and footer link to this form. If sending fails, the form offers a prefilled email draft as a fallback. The site has a dedicated localized product documentation hub for adding assets, organizing records, and planning maintenance; its editorial blog remains a separate section.

“How AssetFlow works” expands into three chapters: Add an asset, Build its knowledge base and Plan its care. Each chapter shows four compact illustrative examples in a native horizontal scroll region, with explanatory captions and previous/next controls. Touch, keyboard arrows and Home/End navigate the row; controls mirror in RTL and respect reduced motion. The chapter examples contain no photographs. A linked overview navigates between chapters; contextual links select the relevant existing ownership-demo tab, lead to the library section or open a localized guide. The examples connect the same vehicle's details, documents, service history, reviewable maintenance draft and suggested next steps. All chapter content supports the six site languages, including Arabic RTL and Arabic-Indic numerals; the examples remain readable without JavaScript.

The dedicated library section presents connected records as a knowledge base: source evidence, understandable history and suggested tasks or maintenance plans for human review. It does not imply that proposed document extraction or automatic deadline updates are delivered.

The household section retains “One home. One shared picture.” and explains shared history, responsibility for tasks and the shared household plan through three benefits and an illustrative work board. The person/plus member row is decorative; the plus does not invite a member. The plan-seat note remains explicit: the owner is included, Free has no additional seats, and Plus, Pro and Max allow 1, 2 and 4 additional members respectively.

A separate asset-category section follows household sharing. Six colored SVG icons and descriptions explain the relevant record and care context for Home & property, Electronics, Vehicles, Furniture, Appliances and Other. Examples follow the app's asset field schema: property responsibilities, device warranty and backup checks, vehicle mileage and service history, furniture material and exposure, appliance type/model and recurring care, and custom records. These are contextual examples, with no promises of automatic compliance, diagnosis or universal maintenance schedules. The homepage and both standalone pages ship in all six locales, including Arabic RTL and localized numerals; household members and tasks are illustrative.

The landing repository is a dependency-free static website, independent of the app, worker, database, and infrastructure repositories. Content supports English, Italian, German, Spanish, French, and Arabic, including RTL and Arabic-Indic numerals.

## Brand Commitments
The website uses AssetFlow forest green and gold with a more vivid editorial palette of sky blue and sage. Georgia headlines and local Inter body text remain; Arabic uses native Tahoma/Arial stacks, RTL layout and Arabic-Indic numerals. Preserve the existing AssetFlow logos. A slow CSS color wash continues behind the top-right navigation; a small animated asset-care constellation links the tracked asset to documents, upcoming care and service history. The decorative art mirrors in RTL, hides on narrow screens to keep the copy clear and stops for reduced-motion preferences. Lead with the ownership interface and keep realistic photography subordinate inside its illustrative asset view; never imply it is a live app screenshot or customer evidence. Clear, practical language shows the customer as the person in control.

## Evidence on Hand
The existing landing copy and product documentation establish Home workflows. Article scenarios and records are illustrative, not testimonials or shipped product screenshots. Do not invent quantified savings, compliance guarantees, recovered records, or maintenance intervals.

## Accessibility & Inclusion
Semantic, keyboard-accessible pages; complete static article text without JavaScript; mobile reading and diagrams; localized labels and meaningful text alternatives.


## Dedicated AI page

The localized `/ai/{locale}/` page owns the full Flow AI and external-assistant
integration sections, moved from the homepage. Header, mobile and footer navigation
include AI. The page presents the implemented connector in present tense while
keeping provider-specific compatibility conditional. It emphasizes intelligence
from asset records, explicit consent, selected assets, read-only external access,
revocation and provider data policies. Agentic work is explained through asking,
investigating, preparing proposals and reviewing what to confirm; it does not
promise autonomous external writes. The setup guide is deferred for separate
review and has no call to action on the AI page. All content and static metadata
support the six existing languages and Arabic RTL.


The homepage hero focuses on the core ownership message. AI remains accessible
from navigation and the Flow AI demo. The desktop section rail starts when How AssetFlow works
reaches the reading position below the fixed header; the hero and asset example
keep their width when the rail appears. The AI hero links use four colored cards:
Flow AI with the AssetFlow mark, connected tools, security and agentic workflows.
Symbols are decorative beside translated labels and supporting text.


## Find your fit

Solutions and pricing share `/explore/{locale}/`, introduced by a concise choice
of edition and Home plan. The edition comparison comes first, then the unchanged
Home pricing section. Main and mobile navigation use the localized Find your fit
label; footer links can target either section. Old `/solutions/{locale}/` and
`/pricing/{locale}/` URLs redirect to the corresponding section, with static HTML
fallbacks for local previews. Canonicals, alternate language links and sitemap
entries describe the merged destination. Planned editions retain their labels.

The AI integration section includes local, original ChatGPT, Claude and MCP
marks with recorded provenance. MCP is identified as a protocol. The emphasized
security section illustrates shared and unshared assets and read-only permissions;
it is labeled as illustrative and does not operate account settings. The
agentic-work section pairs explanatory steps with a synthetic car question,
record context, proposed checklist and an explicit awaiting-review boundary.


Assistant examples use transparent backgrounds and include ChatGPT, Claude,
Mistral Vibe, Codex CLI and custom tools with a compatible remote MCP
client. Provider/account availability remains explicit. The focused edition table
visually omits its repeated header row because the selector already identifies
the edition. Semantic column headers remain available to assistive technology;
without JavaScript, the full comparison and visible headings are preserved.


Find your fit uses a two-step layout with green edition selection and a forest-green
pricing section. Two introductory cards link directly to each decision. The
selected edition has an explicit check mark as well as a color state. Selecting
Home leads to the Home plan comparison; planned editions retain their enquiry
action. Plan cards have separate boundaries and an emphasized Pro option. Prices,
limits and availability labels are unchanged.


Find your fit has its own green-and-white identity: pale green radial gradients,
a bright solutions area, and a forest-green gradient behind white plan cards.
The introductory solution and plan cards have equal heights, matching geometry
and centered alignment in every locale. Edition-specific secondary colors remain.


The one-word navigation label is Guides (localized in each language). The guides
index explicitly links to the localized AssetFlow homepage and Blog; the blog
index links to AssetFlow and Guides. These native navigation links are styled as
compact buttons and remain available without scripts. Mobile editorial headers
place the links on a second row rather than squeezing the language controls.

The homepage example invites exploration through numbered tabs and contextual next-view controls. Smart plan emphasizes editable, reviewed drafts and extraordinary events; Library shows multiple file formats and a source-backed finding awaiting confirmation. File AI eligibility depends on type and scan status. Generation speed is not guaranteed. All six languages retain static panel content without JavaScript.

Cost Insights is the fourth homepage demo view, directly below Library. Three accessible HTML/CSS charts illustrate completed maintenance spending by asset and work category, and approved upcoming plan estimate ranges for three calendar months including the current month. Unknown amounts are excluded and currencies remain separate. The demo uses illustrative EUR values, with no app API calls. Library retains one example per file format and the asset panel uses tighter spacing.

The homepage cost view is labeled Cost Explorer (localized). Slim spending comparisons and shared-axis estimate ranges include brief takeaways. A shallow totals strip retains the actual-versus-estimated distinction; technical reporting notes are omitted from the marketing example.

Cost Explorer pairs spending by asset with completed repair counts by asset over the past 12 months, so recurring repair needs are visible directly. Counts are illustrative (car 4, home 2, laptop 1); the forecast remains separate.

Flow AI is the fifth homepage example view, below Cost Explorer. An illustrative agentic conversation connects a service question with Library evidence, a model-specific official web manual when available, and a proposed checklist under user review. Other prompts cover warranty and recurring repair costs. The final link opens the localized AI page. Sources are illustrative, with no invented live retrieval or external manual URL.

Homepage Security & ownership replaces the short control block and is linked in the side rail. It describes private/shared asset access, separated private/public AI context, reviewed drafts, read-only external grants and revocation, and account export/deletion controls. The AI Act note explains transparency and links Commission guidance; it claims no certification or completed compliance assessment. Side navigation calls Records “Library”. Category SVGs are reused in the Add an asset example. The full category overview moves from the homepage into Home on Find your fit, using a compact two-column layout and following edition selection.
