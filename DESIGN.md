---
name: AssetFlow landing
description: The incumbent AssetFlow identity and its editorial extension.
colors:
  bg: "#fbfaf6"
  bg-alt: "#f3f1e9"
  surface: "#ffffff"
  text: "#173c33"
  muted: "#5b665a"
  primary: "#186b5b"
  primary-dark: "#173c33"
  primary-light: "#fbf4df"
  accent: "#f1c975"
  border: "#e3ded0"
typography:
  display:
    fontFamily: "Manrope, Inter, system-ui, -apple-system, Segoe UI, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(2.1rem, 3.6vw, 3.1rem)"
    fontWeight: 800
    lineHeight: 1.12
    letterSpacing: "-0.02em"
  headline:
    fontFamily: "Manrope, Inter, system-ui, -apple-system, Segoe UI, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(1.9rem, 3vw, 2.6rem)"
    fontWeight: 800
    lineHeight: 1.16
    letterSpacing: "-0.035em"
  article-title:
    fontFamily: "Manrope, Inter, system-ui, -apple-system, Segoe UI, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(2rem, 4.2vw, 3.6rem)"
    lineHeight: 1.13
    letterSpacing: "-0.03em"
  body:
    fontFamily: "Inter, system-ui, -apple-system, Segoe UI, Helvetica Neue, Arial, sans-serif"
    lineHeight: 1.6
  article-body:
    fontFamily: "Inter, system-ui, -apple-system, Segoe UI, Helvetica Neue, Arial, sans-serif"
    fontSize: "1.06rem"
    lineHeight: 1.85
  navigation:
    fontFamily: "Inter, system-ui, -apple-system, Segoe UI, Helvetica Neue, Arial, sans-serif"
    fontSize: "0.94rem"
    fontWeight: 600
rounded:
  sm: "12px"
  md: "18px"
  lg: "26px"
  pill: "999px"
components:
  button-primary:
    textColor: "{colors.surface}"
    rounded: "{rounded.pill}"
    padding: "13px 26px"
  button-outline:
    textColor: "{colors.primary-dark}"
    rounded: "{rounded.pill}"
    padding: "13px 26px"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    rounded: "{rounded.pill}"
    padding: "13px 26px"
  language-select:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    rounded: "{rounded.pill}"
    padding: "8px 12px"
  card:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.md}"
    padding: "26px"
  story-visual:
    backgroundColor: "{colors.bg-alt}"
    rounded: "{rounded.sm}"
    padding: "28px"
---

# Design System: AssetFlow landing

## Overview

**Creative North Star: "The incumbent AssetFlow identity"**

This is a descriptive record of the built landing system, not a replacement identity. Warm off-white surfaces, forest green, restrained gold, Inter text and Manrope headings are confirmed brand commitments in PRODUCT.md. The composition is spacious and practical, with rounded interactive controls and lightly elevated landing cards.

The blog extends that system with reading columns, editorial dividers and semantic figures. Its page-specific story and composition remain in `.impeccable/surfaces/blog.md`.

**Key Characteristics:**
- Warm neutral surfaces and forest-green text.
- Manrope headings with Inter reading text.
- Pill buttons, rounded panels and restrained gold accents.
- Flat editorial lists and explanatory figures alongside the landing page's lifted cards.

## Colors

### Primary
- **Forest green:** primary actions, interactive text, diagram rules and focus outlines.
- **Deep forest:** text and dark feature panels; the primary-dark and text source tokens intentionally share a value.

### Secondary
- **Warm gold:** restrained highlights and the editorial CTA button.

### Neutral
- **Warm paper:** page background.
- **Soft warm paper:** alternate sections, figures and notices.
- **White:** cards and controls.
- **Muted olive-gray:** supporting copy.
- **Warm border:** separators and control boundaries.
- **Pale gold:** primary-light hover and focus surfaces.

**The Inheritance Rule.** New surfaces use the incumbent palette and existing type families; the editorial extension does not establish a second brand.

## Typography

**Display Font:** Manrope with the Inter/body fallback stack.
**Body Font:** Inter with the platform sans-serif fallback stack recorded above.

Headings use compact line heights and negative tracking; body text is more open. The frontmatter records the landing display and headline roles plus the distinct article title and reading roles. Article section headings use a responsive size (`clamp(1.4rem, 2.2vw, 1.9rem)`) and line height (`1.3`). Article text has a maximum measure (`74ch`); its mobile size becomes `1rem` at the narrowest editorial breakpoint. Local font assets are Latin subsets, so Arabic uses the declared fallback stack rather than a new display family.

**The Reading Measure Rule.** Keep explanatory prose within the implemented article measure and preserve the wider line spacing used for sustained reading.

## Layout

The shared centered wrapper has a maximum width (`1120px`) and horizontal padding (`24px`), reduced on the landing page to `16px` at `520px`. Landing section padding scales from `64px` to `96px`, becoming `48px` on small screens. These are observed component values, not a new global spacing scale.

The blog index has a featured two-column story followed by a two-column list with horizontal dividers. It becomes one column at `760px`. Articles pair a contents rail (`220px`) with a flexible reading column and a `64px` gap. At `1000px`, the rail and gap reduce to `175px` and `36px`; at `760px`, the layout becomes a single column with a native contents disclosure. At `460px`, the article wrapper uses `20px` inline padding and visual grids stack.

Logical inline/block properties support RTL. Directional arrows mirror in RTL, and Arabic flow figures use Arabic-Indic counters. These editorial behaviors coexist with the incumbent landing breakpoints; they do not replace them.

## Elevation & Depth

The landing uses soft ambient shadows, translucent header blur and slight hover lifts. Primary buttons retain the incumbent green gradient and colored shadow. Editorial previews and reading figures are flat: borders, color changes and spacing establish hierarchy. Do not reinterpret the flat article treatment as a ban on the landing's existing shadows or gradients.

The source shadow vocabulary (`sm`, `md`, `lg`), action shadows, transitions and breakpoints are recorded in the sidecar. Landing reveal motion already has a reduced-motion override.

## Shapes

The source radius scale has small, medium and large rounded panels. Buttons and the landing language selector are pills. Editorial figures, language disclosure panels, notices and CTA panels use the small radius. Divider-led article lists remain open rather than becoming floating cards.

## Components

### Buttons

Primary buttons use a forest-green gradient, white text, pill corners and a minimum height (`44px`). Hover lifts them (`-2px`) and increases the shadow; active returns the transform. Outline buttons retain a transparent resting surface, while secondary buttons rest on white; both use a pale-gold hover fill and a green border. The editorial CTA uses gold on deep forest. Disabled buttons lose elevation and movement and use muted colors.

### Cards / Containers

Landing cards use white, a warm border, medium corners and `26px` padding; hover adds a small lift (`-3px`). Editorial story figures use soft paper, small corners and `28px` padding, reduced to `22px` at `460px`. Flow figures use numbered rules; maps use deep forest; record and comparison figures use aligned labeled rows. These are semantic explanations, not app-screen replicas.

### Inputs / Fields

The landing language selector is a native select with pill corners and a minimum height (`44px`). Hover/focus changes the border to green and adds a pale-gold ring. Article language selection uses native details/summary with a bordered, small-radius menu. This record does not introduce a new text-input design.

### Navigation

The landing header is sticky and translucent; its ordinary navigation hides at `900px`, while the Blog link remains a separate header link. Article and index headers use normal document positioning, a return link and native language disclosure. Shared navigation text uses green text and a primary-green hover color. Editorial links keep visible focus outlines (`3px`) and underlines on hover. Footer legal links wrap with explicit gaps.

### Editorial metadata

Edition and availability labels follow the article or preview heading in normal reading order. Availability remains visible near both article title and CTA: Home is available, while Business, Fleet and Hospitality are Coming Soon. The metadata is useful content, not a decorative eyebrow pattern.

## Do's and Don'ts

### Do:
- **Do** inherit the existing warm palette, type families and rounded controls.
- **Do** preserve readable article measures, semantic figures and keyboard-visible focus.
- **Do** keep RTL layout, direction indicators and localized numbering meaningful.
- **Do** distinguish live Home workflows from future-edition previews.

### Don't:
- **Don't** replace the incumbent identity when extending an established surface.
- **Don't** turn editorial figures into invented product screenshots.
- **Don't** treat the landing's pre-existing decorative eyebrows, glyph icons or detector findings as reusable rules. They were outside this extension's repair scope and are not canonized here.

Evidence: extracted from `styles.css`, `blog.css`, `index.html`, `scripts/build-blog.py` and generated `dist/blog/` pages. The finish review supplied eight desktop/mobile/RTL captures in `.impeccable/review/`; index desktop and article Arabic mobile were additionally sampled during documentation. No UI or existing detector finding was changed by this documentation pass.
