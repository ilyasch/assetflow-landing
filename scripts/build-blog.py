#!/usr/bin/env python3
"""Render the six-locale editorial library. No third-party dependencies."""
import argparse
import html
import json
from pathlib import Path
import re
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
LOCALES = ('en', 'it', 'de', 'es', 'fr', 'ar')
NAMES = dict(zip(LOCALES, ('English', 'Italiano', 'Deutsch', 'Español', 'Français', 'العربية')))
SLUGS = ('used-car-no-service-history', 'family-car-maintenance', 'flow-ai-from-records-to-next-steps', 'factory-maintenance', 'fleet-maintenance', 'hotel-maintenance')
EDITIONS = ('Home', 'Home', 'Home', 'Business', 'Fleet', 'Hospitality')
SITE = 'https://myassetsflow.com'

def start_link(locale):
    catalog = json.loads((ROOT / f'locales/{locale}.json').read_text())
    return f'<a class="btn btn-primary blog-start" href="https://myassetsflow.app">{esc(catalog["site"]["start"])}</a>'
ICONS = {
    'used-car-no-service-history': '<path d="M8 4h12l5 5v23H8zM20 4v7h5M12 17h9M12 22h9M12 27h5"/><path d="m28 20 3 3 6-7"/>',
    'family-car-maintenance': '<path d="m7 18 4-9h18l4 9M5 18h30v12H5zM10 30v4M30 30v4M10 23h3M27 23h3M15 18h10"/>',
    'flow-ai-from-records-to-next-steps': '<path d="M6 7h28v20H19l-8 6v-6H6zM12 14h16M12 20h10"/><circle cx="31" cy="25" r="5"/>',
    'factory-maintenance': '<path d="M5 34V16l10 6V12l11 7V6h7v28zM10 28h2M18 28h2M27 28h2M29 6V3"/>',
    'fleet-maintenance': '<path d="M4 16h21v13H4zM25 21h7l4 5v3H25M8 16v-5h16M12 11V6h16"/><circle cx="10" cy="30" r="3"/><circle cx="30" cy="30" r="3"/>',
    'hotel-maintenance': '<path d="M8 35V6h24v29M4 35h32M16 35v-9h8v9M14 12h3M23 12h3M14 19h3M23 19h3"/>',
}


def esc(value):
    return html.escape(str(value), quote=True)


def url(locale, slug):
    return f'/blog/{locale}/{slug}/'


def icon(slug):
    return f'<svg class="blog-symbol" viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[slug]}</svg>'


def visual(data, ui):
    kind = data['type']
    tag = 'ol' if kind == 'flow' else 'ul'
    items = ''.join(f'<li><strong>{esc(a)}</strong><span>{esc(b)}</span></li>' for a, b in data['items'])
    return f'<figure class="story-visual visual-{esc(kind)}"><figcaption>{esc(data["title"])}</figcaption><{tag}>{items}</{tag}><p class="visual-note">{esc(ui["example"])}</p></figure>'


def preview(article, locale, ui, featured=False):
    slug = article['id']
    index = SLUGS.index(slug)
    status = ui['available'] if EDITIONS[index] == 'Home' else ui['preview']
    thumb = f'<div class="blog-art art-{index}" aria-hidden="true">{icon(slug)}<span class="art-line"></span><span class="art-dot"></span><span class="art-line art-line-short"></span></div>'
    return f'''<article class="blog-preview{' blog-featured' if featured else ''}">
{thumb}<div class="blog-preview-copy"><h2><a data-blog-id="{slug}" href="{url(locale, slug)}">{esc(article['title'])}</a></h2>
<p class="blog-meta"><span>AssetFlow {EDITIONS[index]}</span><span>{esc(status)}</span></p>
<p>{esc(article['description'])}</p><span class="blog-read" aria-hidden="true">{esc(ui['read'])} <span class="direction-arrow">→</span></span></div></article>'''


def render_index(locale, data):
    ui, articles = data['ui'], data['articles']
    home = f'/?lang={locale}'
    current = ' aria-current="page"'
    languages = ''.join(f'<a href="/blog/{loc}/" lang="{loc}" hreflang="{loc}"{current if loc == locale else ""}>{NAMES[loc]}</a>' for loc in LOCALES)
    alternates = ''.join(f'<link rel="alternate" hreflang="{loc}" href="{SITE}/blog/{loc}/">' for loc in LOCALES)
    cards = preview(articles[0], locale, ui, True) + '<div class="blog-secondary">' + ''.join(preview(a, locale, ui) for a in articles[1:]) + '</div>'
    title = ui['blogs'] + ' | AssetFlow'
    return f'''<!doctype html><html lang="{locale}" dir="{'rtl' if locale == 'ar' else 'ltr'}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(ui['sectionLead'])}">
<link rel="canonical" href="{SITE}/blog/{locale}/">{alternates}<link rel="alternate" hreflang="x-default" href="{SITE}/blog/en/">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(ui['sectionLead'])}"><meta property="og:url" content="{SITE}/blog/{locale}/"><meta property="og:image" content="{SITE}/assets/social-preview.png"><meta property="og:image:alt" content="AssetFlow"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(ui['sectionLead'])}"><meta name="twitter:image" content="{SITE}/assets/social-preview.png">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/styles.css?v=2"><link rel="stylesheet" href="/blog.css?v=1"></head>
<body class="article-page blog-index"><a class="skip-link" href="#main">{esc(ui['skip'])}</a><header class="site-header"><div class="wrap header-inner"><a class="brand" href="{home}"><img class="brand-wordmark" src="/assets/assetflow-wordmark-217.webp" width="217" height="72" alt="AssetFlow"></a><a class="article-back" href="{home}">AssetFlow Home</a><details class="article-language"><summary>{NAMES[locale]}</summary><nav aria-label="{esc(ui['language'])}">{languages}</nav></details>{start_link(locale)}</div></header>
<main id="main"><section class="section blogs" aria-labelledby="blogs-title"><div class="wrap"><div class="blog-section-intro"><h1 id="blogs-title">{esc(ui['sectionTitle'])}</h1><p class="section-lead">{esc(ui['sectionLead'])}</p></div>{cards}</div></section></main>
<footer class="site-footer"><div class="wrap footer-inner"><p>© AssetFlow</p><p class="legal-links"><a href="https://myassetsflow.app/privacy">{esc(ui['privacy'])}</a><a href="https://myassetsflow.app/terms">{esc(ui['terms'])}</a></p></div></footer></body></html>'''


def render(article, locale, data):
    ui = data['ui']
    slug = article['id']
    index = SLUGS.index(slug)
    is_preview = EDITIONS[index] != 'Home'
    current_url = SITE + url(locale, slug)
    description = article['description']
    title = article['title'] + ' | AssetFlow'
    home = f'/?lang={locale}'
    current = ' aria-current="page"'
    links = ''.join(f'<a href="{url(loc, slug)}" lang="{loc}" hreflang="{loc}"{current if loc == locale else ""}>{NAMES[loc]}</a>' for loc in LOCALES)
    alternates = ''.join(f'<link rel="alternate" hreflang="{loc}" href="{SITE}{url(loc,slug)}">' for loc in LOCALES)
    toc = ''.join(f'<li><a href="#step-{i+1}">{esc(s["title"])}</a></li>' for i, s in enumerate(article['sections']))
    sections = ''.join(f'<section id="step-{i+1}" class="article-section"><h2>{esc(s["title"])}</h2>' + ''.join(f'<p>{esc(p)}</p>' for p in s['paragraphs']) + (visual(s['visual'], ui) if 'visual' in s else '') + '</section>' for i, s in enumerate(article['sections']))
    checklist = '<section class="workshop-checklist"><h2>' + esc(article['checklistTitle']) + '</h2><ul>' + ''.join(f'<li>{esc(x)}</li>' for x in article['checklist']) + '</ul></section>'
    faq = ''
    if article.get('faq'):
        faq = f'<section class="article-faq"><h2>{esc(ui["questions"])}</h2>' + ''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q,a in article['faq']) + '</section>'
    sources = ''
    if index in (0, 1):
        sources = f'<section class="article-sources"><h2>{esc(ui["sources"])}</h2><ul><li><a href="https://www.theaa.com/vehicle-check">{esc(ui["sourceAA"])}</a></li><li><a href="https://www.ford.com/owners-manuals/">{esc(ui["sourceFord"])}</a></li></ul><p>{esc(ui["sourceNote"])}</p></section>'
    related = ''.join(f'<li><a href="{url(locale,a["id"])}">{esc(a["title"])}</a></li>' for a in data['articles'] if a['id'] != slug)
    schema = {'@context': 'https://schema.org', '@type': 'BlogPosting', 'headline': article['title'], 'description': description, 'inLanguage': locale, 'mainEntityOfPage': current_url, 'url': current_url, 'author': {'@type': 'Organization', 'name': 'AssetFlow', 'url': SITE}, 'publisher': {'@type': 'Organization', 'name': 'AssetFlow', 'url': SITE}}
    return f'''<!doctype html>
<html lang="{locale}" dir="{'rtl' if locale == 'ar' else 'ltr'}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(title)}</title>
<meta name="description" content="{esc(description)}"><link rel="canonical" href="{current_url}">{alternates}<link rel="alternate" hreflang="x-default" href="{SITE}{url('en',slug)}">
<meta property="og:type" content="article"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{current_url}"><meta property="og:locale" content="{locale}"><meta property="og:site_name" content="AssetFlow"><meta property="og:image" content="{SITE}/assets/social-preview.png"><meta property="og:image:alt" content="AssetFlow">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(description)}"><meta name="twitter:image" content="{SITE}/assets/social-preview.png">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/styles.css?v=2"><link rel="stylesheet" href="/blog.css?v=1">
<script type="application/ld+json">{json.dumps(schema,ensure_ascii=False).replace('<', chr(92)+'u003c')}</script>
</head><body class="article-page"><a class="skip-link" href="#main">{esc(ui['skip'])}</a>
<header class="site-header"><div class="wrap header-inner"><a class="brand" href="{home}"><img class="brand-wordmark" src="/assets/assetflow-wordmark-217.webp" width="217" height="72" alt="AssetFlow"></a><a class="article-back" href="/blog/{locale}/">{esc(ui['back'])}</a><details class="article-language"><summary>{NAMES[locale]}</summary><nav aria-label="{esc(ui['language'])}">{links}</nav></details>{start_link(locale)}</div></header>
<main id="main"><div class="wrap"><nav class="breadcrumbs" aria-label="{esc(ui['breadcrumb'])}"><a href="{home}">AssetFlow</a><span aria-hidden="true">/</span><a href="/blog/{locale}/">{esc(ui['blogs'])}</a><span aria-hidden="true">/</span><span>AssetFlow {EDITIONS[index]}</span></nav>
<header class="article-hero">{icon(slug)}<h1>{esc(article['title'])}</h1><p class="article-status">AssetFlow {EDITIONS[index]} · {esc(ui['preview'] if is_preview else ui['available'])}</p><p class="article-deck">{esc(article['lead'])}</p><p class="article-notice">{esc(ui['previewNotice'] if is_preview else ui['illustrativeNotice'])}</p></header>
<div class="article-layout"><aside class="article-toc"><details open><summary>{esc(ui['contents'])}</summary><nav aria-label="{esc(ui['contents'])}"><ol>{toc}</ol></nav></details></aside><article class="article-body">{sections}{checklist}{faq}{sources}<section class="article-cta"><h2>{esc(article['ctaTitle'])}</h2><p>{esc(ui['previewCtaNote'] if is_preview else article['ctaText'])}</p><a class="btn btn-primary" href="https://myassetsflow.app">{esc(ui['previewCta'] if is_preview else ui['homeCta'])}</a>{f'<p class="cta-availability">{esc(ui["previewNotice"])}</p>' if is_preview else ''}</section></article></div>
<nav class="article-related" aria-labelledby="related-title"><h2 id="related-title">{esc(ui['related'])}</h2><ul>{related}</ul><a href="/blog/{locale}/">{esc(ui['back'])}</a></nav></div></main>
<footer class="site-footer"><div class="wrap footer-inner"><p>© AssetFlow</p><p class="legal-links"><a href="https://myassetsflow.app/privacy">{esc(ui['privacy'])}</a><a href="https://myassetsflow.app/terms">{esc(ui['terms'])}</a></p></div></footer>
</body></html>'''


def build(output, update_landing):
    data = {loc: json.loads((ROOT / f'content/blog/{loc}.json').read_text()) for loc in LOCALES}
    assert all([a['id'] for a in d['articles']] == list(SLUGS) for d in data.values()), 'Article IDs/order must match in all locales'
    for loc,d in data.items():
        assert set(d['ui']) == set(data['en']['ui']), f'UI translation keys differ: {loc}'
        index_path = output / 'blog' / loc / 'index.html'
        index_path.parent.mkdir(parents=True, exist_ok=True)
        index_path.write_text(render_index(loc, d))
        for a in d['articles']:
            assert len(a['sections']) == 5, a['id']
            assert sum('visual' in s for s in a['sections']) == 3, a['id']
            text = render(a, loc, d)
            if loc == 'ar':
                # Convert visible text only. Never alter URLs, IDs, or JSON-LD.
                digits = str.maketrans('0123456789','٠١٢٣٤٥٦٧٨٩')
                text = re.sub(r'(?<=>)([^<]+)(?=<)', lambda m: m[0] if m[0].lstrip().startswith('{') else m[0].translate(digits), text)
            dest = output / url(loc,a['id']).lstrip('/') / 'index.html'
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_text(text)
    if update_landing:
        for loc,d in data.items():
            p = ROOT / f'locales/{loc}.json'
            catalog = json.loads(p.read_text())
            catalog['nav']['blogs'] = d['ui']['blogs']
            catalog.pop('blog', None)
            p.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
    (output/'blog/index.html').write_text(render_index('en', data['en']))
    namespace = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    ET.register_namespace('',namespace)
    tree = ET.Element(f'{{{namespace}}}urlset')
    for path in ['/']+[f'/blog/{loc}/' for loc in LOCALES]+[url(loc,slug) for loc in LOCALES for slug in SLUGS]:
        ET.SubElement(ET.SubElement(tree,f'{{{namespace}}}url'),f'{{{namespace}}}loc').text = SITE+path
    ET.indent(tree)
    (output/'sitemap.xml').write_bytes(ET.tostring(tree,encoding='utf-8',xml_declaration=True))
    print(f'Rendered {len(SLUGS) * len(LOCALES)} static articles, six localized indexes, default index and sitemap.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT)
    parser.add_argument('--update-landing',action='store_true')
    args = parser.parse_args()
    build(args.output,args.update_landing)
