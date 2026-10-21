---
name: AssetFlow landing
description: Colorful ownership stories with an expressive product interface, forest green and serif type.
colors:
  bg: "#fcfcf9"
  bg-alt: "#f0f3ed"
  surface: "#fff"
  text: "#173c33"
  muted: "#56675f"
  primary: "#186b5b"
  primary-dark: "#173c33"
  accent: "#f1c975"
  gold-soft: "#fbf2d9"
  market-home: "#e5eddf"
  market-business: "#edf3f6"
  market-fleet: "#f7f0d8"
  market-hospitality: "#edf1e9"
  market-home-selected: "#a5c798"
  market-business-selected: "#a3c6d8"
  market-fleet-selected: "#ddbd62"
  market-hospitality-selected: "#9fbd9f"
  sky: "#dcebf0"
  sage: "#dce8d6"
  cobalt: "#416d92"
  border: "#dce3db"
typography:
  display:
    fontFamily: 'Georgia, "Times New Roman", serif'
    fontSize: "clamp(3.5rem, 4.7vw, 5rem)"
    fontWeight: 400
    lineHeight: 1.08
    letterSpacing: "-0.035em"
  headline:
    fontFamily: 'Georgia, "Times New Roman", serif'
    fontSize: "clamp(2.5rem, 4.3vw, 4rem)"
    fontWeight: 400
    lineHeight: 1.08
    letterSpacing: "-0.035em"
  article-title:
    fontFamily: 'Georgia, "Times New Roman", serif'
    fontSize: "clamp(2.8rem, 5.4vw, 5rem)"
    fontWeight: 400
    lineHeight: 1.12
    letterSpacing: "-0.035em"
  body:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "16px"
    lineHeight: 1.65
  article-body:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "1.04rem"
    lineHeight: 1.95
  label:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "0.8rem"
  arabic:
    fontFamily: "Tahoma, Arial, sans-serif"
rounded:
  panel: "14px"
  editorial: "12px"
  pill: "999px"
  tab: "6px"
components:
  button-primary:
    backgroundColor: "{colors.text}"
    textColor: "{colors.surface}"
    rounded: "{rounded.pill}"
    padding: "11px 24px"
  button-primary-hover:
    backgroundColor: "{colors.primary}"
  button-outline:
    textColor: "{colors.text}"
    rounded: "{rounded.pill}"
    padding: "11px 24px"
  language-select:
    textColor: "{colors.text}"
    padding: "8px"
  ownership-demo:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.panel}"
  story-visual:
    backgroundColor: "{colors.bg-alt}"
    rounded: "{rounded.editorial}"
    padding: "32px"
---

# Design System: AssetFlow landing

## Overview

**Creative North Star: "A vivid picture of what you own"**

The website combines AssetFlow's forest green and warm gold with sky blue and sage. Georgia headlines give ownership stories a human voice; local Inter keeps controls, supporting copy and records precise. The product interface leads; one realistic asset photograph replaces the line-art vehicle drawing inside the sample view. Existing AssetFlow logos remain unchanged.

Fine rules and tonal fields organize most content. A single elevated ownership demonstration provides the homepage’s concentrated product detail; articles use semantic diagrams and open reading columns. Surface strategy remains in `.impeccable/surfaces/home.md` and `.impeccable/surfaces/blog.md`.

**Key Characteristics:**
- Warm white, forest green and gold, balanced with sky blue and sage.
- Georgia display and Inter body; native Arabic typography.
- A clear product interface with one realistic asset photograph inside its sample view.
- Solid pill actions, fine dividers and open sections with color fields.

## Colors

Warm white establishes the canvas; forest green carries text and action. Sage and pale gold distinguish story panels; gold frames the photograph. Sky blue, sage and gold distinguish market columns.

### Primary
- **Forest green:** links, emphasized headline words, hover actions and focus outlines.
- **Deep forest:** body text, primary action fills, the demo rail and household section. Text and primary-dark intentionally share one source value.

### Secondary
- **Warm gold:** selection, small state accents and the offset hero frame.
- **Pale gold:** a warm story surface and secondary hero color wash.
- **Sky blue:** a cool story surface and Business matrix heading.
- **Sage:** the hero media field and first story surface.
- **Cobalt:** the Hospitality matrix heading.

### Neutral
- **Warm white:** page canvas.
- **Soft sage paper:** alternate fields and explanatory figures.
- **White:** demonstration stage and disclosure menus.
- **Muted green-gray:** supporting copy and reading metadata.
- **Pale green-gray:** fine borders and separators.

**The Shared World Rule.** Homepage, blog index and articles share the same palette and type roles.

## Typography

**Display Font:** Georgia with Times New Roman and serif fallbacks.
**Body Font:** local variable Inter with system-ui and sans-serif fallbacks, loaded through the packaged, hashed public font asset.

Display and section headings are regular-weight, tightly tracked and balanced. Compact interface headings remain in the body family. The frontmatter records the homepage hero, section headline and article title roles. The blog-index title uses `clamp(3rem, 5.8vw, 5.5rem)`; article section headings use `clamp(1.9rem, 2.6vw, 2.5rem)` with a line height of `1.25`. Navigation is compact (`0.85rem`); labels and secondary interface copy commonly use `0.8rem`.

Arabic switches both font roles to Tahoma, Arial, sans-serif, removes heading tracking and opens major-heading line height to `1.5`. Its homepage hero has a separate responsive size. Do not force Latin serif metrics onto Arabic.

**The Reading Measure Rule.** Keep sustained article text within the implemented reading column and preserve its generous line spacing.

## Layout

The centered wrapper is `min(100% - 112px, 1240px)`, expanding at `1500px` to `min(100% - 144px, 1360px)`. Insets become `32px` at `1100px`, `20px` at `620px`, and `16px` at `360px`. Sections use `108px` block padding, reducing to `80px` and then `65px`. These are observed layout values, not an invented global spacing scale.

The homepage opens with a floating pill navigation and a clear left-aligned headline over a slow gold, sky and sage color wash. On wide screens, the opening hero stays full width; a fixed left section rail fades in when Product reaches the sticky header, then tracks Product, How it works, Pricing and Solutions as the content shifts to make room. Below `1440px`, the rail gives way to the full-width layout and the mobile disclosure menu remains the section navigation. The wide product interface follows directly, with a deep-green rail, flexible stage, sky-blue context panel and a realistic vehicle photo inside the illustrative asset view. At `900px` the contextual column hides; at `620px` the demo rail becomes horizontal tabs above the stage and the header switches to its menu disclosure. Color-backed two-column chapters become a single reading sequence on mobile. Pricing is a divider-led four-column grid, becoming two columns at `900px`.

The market matrix preserves its semantic table and `950px` minimum width in an overflow region. Its labeled, keyboard-focusable region and scroll instruction support narrow screens; the instruction appears below `1014px`. Each edition uses a small branded mark with an edition-specific line icon and its AssetFlow product name. Home receives a pale-green column and an available label. Business, Fleet and Hospitality retain explicit Coming Soon labels and planned capability wording. Selecting an edition gives its full column a stronger edition-tinted fill and narrow matching edge, with the same focus also visible in the edition picker.

The blog index pairs a featured story and large semantic document illustration before a two-column story list. It stacks at `760px`. Articles pair a `220px` contents rail and flexible reading column with `64px` gap; at `1000px` these become `175px` and `36px`, and at `760px` the layout becomes one column with a native contents disclosure. Article body measure is `70ch`. At `460px`, body size becomes `1rem`, figures stack and article wrapper padding is removed inside the shared mobile wrapper.

The footer groups brand, Product, Solutions and Resources into clear link columns, stacking at narrower widths. Logical inline/block properties support RTL, including the fixed section rail. Homepage locale selection prioritizes a valid `?lang=`, saved preference, browser language, then English. Switching locale updates text, accessibility labels, metadata, blog links, document direction and visible numerals; storage is optional. Generated blog indexes and articles have six explicit locale routes, matching language links and RTL Arabic markup. Arabic flow counters use Arabic-Indic numerals.

## Elevation & Depth

Most surfaces remain flat, using spacing, thin rules and soft background changes. The ownership example carries a neutral demo shadow (`0 28px 70px -24px #2028222b`); the mobile menu and section rail use smaller neutral shadows. Primary actions are solid and have no lift or shadow. Soft radial color fields behind the hero provide atmosphere, moving slowly and stopping for reduced-motion preferences.

**The Concentrated Depth Rule.** Reserve the large ambient shadow for the ownership demonstration; use rules and tonal fields for editorial structure.

## Shapes

The main demonstration and chapter figures use the shared panel radius. Article figures, disclosures and CTA panels use the editorial radius; actions and billing controls are pills. Tabs use smaller corners and a gold inset selection rule, mirrored in RTL and moved to the bottom on mobile. Pricing, records and comparison rows use open rectangular divisions rather than individually elevated cards.

## Components

### Buttons

Solid, restrained pill controls use a minimum height of `48px`, body-family medium text and a dark-forest fill with white text. Primary hover changes to forest green. Outline actions use a transparent surface and fine green-gray border; hover adds soft sage paper and a forest border. Header actions are more compact (`42px` minimum); mobile hero actions use `46px`. Focus remains a visible `3px` outline offset by `5px`. Disabled buttons reduce opacity. Article CTA buttons use gold on deep forest and a lighter gold hover.

### Inputs / Fields

The homepage language control is a native, borderless select on the page surface with `44px` minimum height. Article language choice uses a pill-shaped native summary and a white bordered menu; the current language receives soft sage fill. There is no text-input pattern in this build.

### Navigation

The homepage header is sticky and opaque, with a fine bottom rule. At `900px`, ordinary navigation gives way to a native details menu. At `620px`, the header CTA hides while language and menu controls remain. Menu links close the disclosure; Escape closes it and returns focus. Article/index headers use normal document flow, a return link, language disclosure and an app action that hides at `620px`. Footer links wrap; the skip link becomes visible on focus.

### Ownership demonstration

The illustration is explicitly a local example. JavaScript adds tab semantics, roving tab focus, arrow-key navigation, Home/End navigation and responsive tab orientation. Selected panels receive a brief blur-to-clear transition. Review reveals the explanation and focuses Confirm; confirmation updates an `aria-live` status and state label, then focuses Reset. Reset restores the draft and returns focus to Review. No external reminder is created. Without JavaScript, all three panels remain readable and inert review/tab controls are hidden.

Tab motion uses `0.4s` with the source easing; ordinary action color changes use `0.2s`, and tab backgrounds use `0.25s`. Reduced motion disables all animations and transitions and restores automatic scrolling.

### Feature chapters

The homepage's three capability chapters use open, divider-separated sections with serif action headings, short explanations and contextual links. A compact three-column linked overview leads to each chapter and becomes one column at `700px` and below. Each chapter contains two semantic figures in a two-column grid with a `28px` gap; at `700px` and below, the figures stack with a `32px` gap. Both examples stay visible without carousel controls or JavaScript. Each figure pairs a tonal preview with its own title, explanation and illustrative-data caption. Sage, sky and pale gold distinguish the chapters without adding elevation.

Asset and maintenance links select the corresponding ownership-demo tab before following the product anchor; the knowledge-base link leads to the library section, and guide links follow the active locale. Figures preserve logical spacing for Arabic RTL, native Arabic heading metrics and Arabic-Indic review-list counters. Maintenance examples keep review, adjustment and confirmation explicit; the knowledge-base examples connect source evidence, understandable history and suggested next actions. Flow AI retains its separate later section. Chapter actions use a consistent `290px` desktop column and stack below the explanation at `1000px` and below.

The library illustration uses a flat soft-sage figure with distinct source, understanding and suggestion areas. Its captions and human-review language remain localized across all six languages.

### Household sharing and asset categories

The household section uses a soft-sage field around a contained forest feature with the existing serif heading, a decorative person/plus member row and a white illustrative work board. The feature pairs copy and board in two columns, stacking at `1000px` and below. Three divider-led benefits follow in a three-column row, stacking at `620px` and below, with the plan-seat note beneath. Member and task SVGs support the example without implying actual people, tasks or interactive invitation controls; the plus is decorative.

Asset categories occupy their own warm-white section after household sharing and before pricing. Six open, rule-separated entries pair a colored `64px` icon field with a category name and description; each inline SVG is `36px` and decorative. Category-specific record and care context distinguishes the entries rather than repeating generic benefits. The grid uses three columns on desktop, two at `1000px` and below, and one at `620px` and below. Both sections retain localized labels, native Arabic typography and logical spacing for RTL.

### Pricing and availability

A pill billing switch updates monthly/annual price visibility and pressed states locally. Without JavaScript the switch hides and the default prices remain. Plans use fine rules, aligned action footers and a subtle featured-plan fill. Availability labels are content, appearing in the market matrix and near article headings and CTAs for planned editions.

### Editorial figures and reading controls

Article figures are semantic explanations: step sequences, maps, evidence rows and comparison worksheets. Their captions use the body family, while article headings use display type. Figures rest on soft fields with fine separators; they contain no simulated app controls. FAQ and contents use native details/summary. Related links follow the reading body. Print hides navigation, contents, CTAs and related links while keeping figures together where possible. Existing logo and social rasters are retained; the generated vehicle photo and its provenance are recorded in `assets/IMAGE-SOURCES.md`.

## Do's and Don'ts

### Do:
- **Do** use the approved serif/sans pairing and native Arabic override.
- **Do** preserve semantic figures, visible focus, readable measures and reduced-motion behavior.
- **Do** keep Home availability and planned-edition notices visible.
- **Do** label the ownership example as illustrative and keep confirmation local.

### Don't:
- **Don't** reinstate Manrope headings, gradient action buttons or the former floating-card layout.
- **Don't** present illustrative diagrams or local demo state as live product records.
- **Don't** hide matrix columns on small screens; preserve the named scroll region and its scroll hint.

Evidence: extracted from `styles.css`, `blog.css`, `main.js`, `index.html` and `scripts/build-blog.py`, with the approved surface contracts. The independent finish review inspected all 13 supplied valid captures in `.impeccable/review/` and reported no material visual issues. No UI or assets were changed by this documentation pass.
