#!/usr/bin/env python3
"""Build localized pricing and solutions pages from the landing page sections."""
from html.parser import HTMLParser
import html
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://myassetsflow.com"
LOCALES = ("en", "it", "de", "es", "fr", "ar")
LANGUAGES = dict(zip(LOCALES, ("English", "Italiano", "Deutsch", "Español", "Français", "العربية")))
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


def value_at(catalog, key):
    value = catalog
    for part in key.split("."):
        value = value[part]
    return value


class Localizer(HTMLParser):
    def __init__(self, catalog, locale):
        super().__init__(convert_charrefs=False)
        self.catalog = catalog
        self.locale = locale
        self.stack = []
        self.output = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        raw = self.get_starttag_text()
        aria_key = attrs.get("data-i18n-aria")
        if aria_key:
            label = html.escape(value_at(self.catalog, aria_key), quote=True)
            if re.search(r"\baria-label\s*=\s*([\"']).*?\1", raw, re.I):
                raw = re.sub(r"\baria-label\s*=\s*([\"']).*?\1", f'aria-label="{label}"', raw, count=1, flags=re.I)
            else:
                raw = raw[:-1] + f' aria-label="{label}">'
        self.output.append(raw)
        key = attrs.get("data-i18n")
        if tag not in VOID:
            self.stack.append({"tag": tag, "key": key, "done": False})

    def handle_startendtag(self, tag, attrs):
        self.output.append(self.get_starttag_text())

    def handle_endtag(self, tag):
        self.output.append(f"</{tag}>")
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index]["tag"] == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        replacement = None
        if data.strip():
            for entry in reversed(self.stack):
                if entry["key"] and not entry["done"]:
                    replacement = value_at(self.catalog, entry["key"])
                    entry["done"] = True
                    break
        text = replacement if replacement is not None else data
        if self.locale == "ar":
            text = text.translate(str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩"))
        self.output.append(html.escape(text, quote=False) if replacement is not None else text)

    def handle_entityref(self, name):
        self.output.append(f"&{name};")

    def handle_charref(self, name):
        self.output.append(f"&#{name};")

    def handle_comment(self, data):
        self.output.append(f"<!--{data}-->")

    def result(self):
        return "".join(self.output)


def extract(source, name):
    start = f"<!-- marketing-page:{name}:start -->"
    end = f"<!-- marketing-page:{name}:end -->"
    before, remainder = source.split(start, 1)
    section, after = remainder.split(end, 1)
    return before + after, section.strip()


def contact_dialog(source):
    start = source.index('<dialog class="contact-dialog"')
    end = source.index("</dialog>", start) + len("</dialog>")
    return source[start:end]


def nav_links(locale, current):
    pricing_current = ' aria-current="page"' if current == "pricing" else ""
    solutions_current = ' aria-current="page"' if current == "solutions" else ""
    return (
        f'<a href="/?lang={locale}#product" data-home-product data-i18n="site.product">Product</a>'
        f'<a href="/pricing/{locale}/" data-pricing-index{pricing_current} data-i18n="nav.pricing">Pricing</a>'
        f'<a href="/solutions/{locale}/" data-solutions-index{solutions_current} data-i18n="site.solutions">Solutions</a>'
        f'<a href="/docs/{locale}/" data-doc-index data-i18n="nav.docs">Product guides</a>'
        f'<a href="/blog/{locale}/" data-blog-index data-i18n="nav.blogs">Blog</a>'
    )


def mobile_links(locale, current):
    current_attr = ' aria-current="page"' if current == "pricing" else ""
    solutions_attr = ' aria-current="page"' if current == "solutions" else ""
    return (
        f'<a href="/?lang={locale}#product" data-i18n="site.product">Product</a>'
        f'<a href="/?lang={locale}#how-it-works" data-i18n="site.how">How it works</a>'
        f'<a href="/pricing/{locale}/" data-pricing-index{current_attr} data-i18n="nav.pricing">Pricing</a>'
        f'<a href="/solutions/{locale}/" data-solutions-index{solutions_attr} data-i18n="site.solutions">Solutions</a>'
        f'<a href="/docs/{locale}/" data-doc-index data-i18n="nav.docs">Product guides</a>'
        f'<a href="/blog/{locale}/" data-blog-index data-i18n="nav.blogs">Blog</a>'
    )


def shell(content, footer, dialog, locale, page):
    catalog = json.loads((ROOT / f"locales/{locale}.json").read_text())
    title_key = page + "Title"
    description_key = page + "Description"
    title = catalog["seo"][title_key]
    description = catalog["seo"][description_key]
    route = f"/{page}/{locale}/"
    footer = footer.replace('href="#product"', f'href="/?lang={locale}#product"')
    footer = footer.replace('href="#how-it-works"', f'href="/?lang={locale}#how-it-works"')
    alternates = "".join(f'<link rel="alternate" hreflang="{other}" href="{SITE}/{page}/{other}/">' for other in LOCALES)
    header = f'''<header class="site-header"><div class="wrap header-inner">
<a class="brand" href="/?lang={locale}"><img class="brand-wordmark" src="/assets/assetflow-wordmark-217.webp" width="217" height="72" alt="AssetFlow"></a>
<nav class="header-nav" data-i18n-aria="site.navigation" aria-label="Main navigation">{nav_links(locale, page)}</nav>
<div class="header-actions"><label class="visually-hidden" for="lang-picker" data-i18n="nav.languageLabel">Language</label><select id="lang-picker">{''.join(f'<option value="{loc}"{" selected" if loc == locale else ""}>{name}</option>' for loc, name in LANGUAGES.items())}</select><a class="btn btn-primary" href="https://myassetsflow.app" data-i18n="site.start">Start free</a></div>
<details class="mobile-menu"><summary><span data-i18n="site.menu">Menu</span></summary><nav data-i18n-aria="site.navigation" aria-label="Main navigation">{mobile_links(locale, page)}</nav></details>
</div></header>'''
    document = f'''<!doctype html>
<html lang="{locale}" dir="{'rtl' if locale == 'ar' else 'ltr'}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(description, quote=True)}">
<link rel="canonical" href="{SITE}{route}">{alternates}<link rel="alternate" hreflang="x-default" href="{SITE}/{page}/en/">
<meta property="og:type" content="website"><meta property="og:site_name" content="AssetFlow"><meta property="og:url" content="{SITE}{route}"><meta property="og:title" content="{html.escape(title, quote=True)}"><meta property="og:description" content="{html.escape(description, quote=True)}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/styles.css?v=10"><script defer src="/main.js?v=10"></script>
</head><body class="marketing-page" data-localized-page="{page}" data-seo-title-key="{title_key}" data-seo-description-key="{description_key}">
<a class="skip-link" href="#main" data-i18n="a11y.skip">Skip to content</a>{header}<main id="main">{content}</main>{footer}{dialog}</body></html>'''
    parser = Localizer(catalog, locale)
    parser.feed(document)
    return parser.result()


def build(output):
    source = (ROOT / "index.html").read_text()
    home = source
    fragments = {}
    for page in ("pricing", "solutions"):
        home, fragments[page] = extract(home, page)
    fragments["pricing"] = re.sub(
        r'<h2(\s+data-i18n="pricing\.title"[^>]*)>(.*?)</h2>',
        r'<h1\1>\2</h1>', fragments["pricing"], count=1, flags=re.S,
    )
    fragments["solutions"] = re.sub(
        r'<h2>\s*(<span\s+data-i18n="matrix\.title".*?</span\s*>)\s*</h2>',
        r'<h1>\1</h1>', fragments["solutions"], count=1, flags=re.S,
    )
    footer_start = source.index('<footer class="site-footer">')
    footer_end = source.index("</footer>", footer_start) + len("</footer>")
    footer = source[footer_start:footer_end]
    dialog = contact_dialog(source)
    (output / "index.html").write_text(home)
    for locale in LOCALES:
        for page in ("pricing", "solutions"):
            rendered = shell(fragments[page], footer, dialog, locale, page)
            destination = output / page / locale / "index.html"
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(rendered)
    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", namespace)
    sitemap = output / "sitemap.xml"
    tree = ET.parse(sitemap) if sitemap.exists() else ET.ElementTree(ET.Element(f"{{{namespace}}}urlset"))
    root = tree.getroot()
    existing = {node.find(f"{{{namespace}}}loc").text for node in root.findall(f"{{{namespace}}}url")}
    for page in ("pricing", "solutions"):
        for locale in LOCALES:
            url = f"{SITE}/{page}/{locale}/"
            if url not in existing:
                node = ET.SubElement(root, f"{{{namespace}}}url")
                ET.SubElement(node, f"{{{namespace}}}loc").text = url
    ET.indent(tree)
    tree.write(sitemap, encoding="utf-8", xml_declaration=True)
    print("Rendered localized pricing and solutions pages for six languages.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT)
    build(parser.parse_args().output)
