#!/usr/bin/env python3
"""Verify the deployed artifact, including nested pages and locale navigation."""
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / 'dist'
LOCALES = ('en', 'it', 'de', 'es', 'fr', 'ar')


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.nodes = []
        self.ids = set()
        self.text = []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.nodes.append((tag, attrs))
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f'Duplicate ID in {self.path}: {attrs["id"]}'
            self.ids.add(attrs['id'])

    def handle_data(self, text):
        self.text.append(text)


pages = {path: Page(path) for path in SITE.rglob('*.html')}
articles = [p for p in pages if p.is_relative_to(SITE / 'blog') and len(p.relative_to(SITE / 'blog').parts) == 3]
assert len(articles) == 36, f'Expected 36 articles, found {len(articles)}'
checked = 0
for path, page in pages.items():
    for tag, attrs in page.nodes:
        references = [attrs[attr] for attr in ('href', 'src') if attr in attrs]
        if 'srcset' in attrs:
            references += [candidate.strip().split()[0] for candidate in attrs['srcset'].split(',')]
        for reference in references:
            target = urlsplit(reference)
            if target.scheme or target.netloc:
                continue
            dest = SITE / unquote(target.path).lstrip('/') if target.path.startswith('/') else path.parent / unquote(target.path)
            if not target.path:
                dest = path
            if dest.is_dir():
                dest /= 'index.html'
            dest = dest.resolve()
            assert dest.is_relative_to(SITE.resolve()), f'Escaping link: {reference}'
            assert dest.is_file(), f'Missing {reference} from {path}'
            if target.path.startswith('/static/'):
                digest = hashlib.sha256(dest.read_bytes()).hexdigest()[:16]
                assert dest.stem.endswith('.' + digest), f'Invalid asset hash: {reference}'
            if target.fragment and dest in pages:
                assert target.fragment in pages[dest].ids, f'Missing fragment: {reference} from {path}'
            checked += 1
        if tag == 'img':
            assert int(attrs.get('width', 0)) > 0 and int(attrs.get('height', 0)) > 0, f'Image space must be reserved: {path}'

# Check assets referenced by the active stylesheets, including hashed font URLs.
stylesheets = set()
for page in pages.values():
    for tag, attrs in page.nodes:
        if tag == 'link' and attrs.get('rel') == 'stylesheet':
            target = urlsplit(attrs['href'])
            stylesheets.add(SITE / target.path.lstrip('/') if target.path.startswith('/') else page.path.parent / target.path)
for stylesheet in stylesheets:
    for reference in re.findall(r'url\([\"\']?([^\)\"\']+)', stylesheet.read_text()):
        target = urlsplit(reference)
        if target.scheme == 'data':
            continue
        assert not target.netloc and not target.scheme, f'Unexpected external CSS asset: {reference}'
        asset = SITE / target.path.lstrip('/') if target.path.startswith('/') else stylesheet.parent / target.path
        assert asset.is_file(), f'Missing CSS asset {reference} from {stylesheet}'

canonical_urls = set()
for path in articles:
    p = pages[path]
    loc, slug = path.relative_to(SITE / 'blog').parts[:2]
    assert loc in LOCALES
    assert sum(tag == 'h1' for tag, _ in p.nodes) == 1, path
    assert sum(tag == 'figure' for tag, _ in p.nodes) == 3, path
    assert any(tag == 'html' and attrs.get('lang') == loc and attrs.get('dir') == ('rtl' if loc == 'ar' else 'ltr') for tag, attrs in p.nodes), path
    canonicals = [a['href'] for t, a in p.nodes if t == 'link' and a.get('rel') == 'canonical']
    assert canonicals == [f'https://myassetsflow.com/blog/{loc}/{slug}/'], path
    canonical_urls.update(canonicals)
    assert len([a for t,a in p.nodes if t == 'link' and a.get('hreflang') in LOCALES]) == 6, path
    assert sum(t == 'p' for t,_ in p.nodes) >= 10, f'Incomplete static text: {path}'
    assert not any(t == 'script' and a.get('src') == '/main.js' for t,a in p.nodes), path
    source = path.read_text()
    ld = source.split('<script type="application/ld+json">',1)[1].split('</script>',1)[0]
    schema = json.loads(ld)
    assert schema['inLanguage'] == loc and schema['url'] == canonicals[0]
    if loc == 'ar':
        assert '٠' in source or '١' in source or all(not c.isdigit() for c in ''.join(p.text))

sitemap = ET.parse(SITE / 'sitemap.xml')
urls = {x.text for x in sitemap.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
index_urls = {f'https://myassetsflow.com/blog/{loc}/' for loc in LOCALES}
docs_urls = {f'https://myassetsflow.com/docs/{loc}/' for loc in LOCALES} | {f'https://myassetsflow.com/docs/{loc}/{slug}/' for loc in LOCALES for slug in ('add-an-asset', 'organize-records', 'plan-maintenance')}
assert urls == canonical_urls | index_urls | docs_urls | {'https://myassetsflow.com/'}, 'Sitemap and canonical pages differ'
home = pages[SITE / 'index.html']
photos = [(tag, attrs) for tag, attrs in home.nodes if 'vehicle-photo' in attrs.get('src', '') or 'vehicle-photo' in attrs.get('srcset', '')]
for tag, attrs in photos:
    references = attrs['srcset'].split(',') if tag == 'source' else [attrs['src']]
    assert all(reference.strip().startswith('/static/vehicle-photo') for reference in references), 'Photos must use immutable hashed URLs'
assert (SITE / 'assets/vehicle-photo.jpg').stat().st_size < 150_000, 'JPEG fallback exceeds the 150 KB budget'
chapter_source = (SITE / 'index.html').read_text().split('id="how-it-works"', 1)[1].split('id="examples"', 1)[0]
assert '<img' not in chapter_source, 'Capability chapters must use HTML examples, not photos'
keys = [a[attr] for _, a in home.nodes for attr in ('data-i18n', 'data-i18n-aria') if attr in a]
# Confirmed/reset states are translated dynamically, so check them as well.
keys += ['site.confirmation', 'site.confirmed', 'site.draft']
# The market comparison needs real row/column semantics and explicit availability.
assert sum(t == 'th' and a.get('scope') == 'col' for t,a in home.nodes) == 5, 'Expected four market columns plus row labels'
assert sum(t == 'th' and a.get('scope') == 'row' for t,a in home.nodes) == 5, 'Expected five market comparison rows'
assert any(a.get('class') == 'matrix-region' and a.get('tabindex') == '0' and a.get('role') == 'region' and a.get('aria-labelledby') for _,a in home.nodes), 'Market matrix must support keyboard scrolling and have a name'

for loc in LOCALES:
    catalog = json.loads((SITE / f'locales/{loc}.json').read_text())
    for key in keys:
        value = catalog
        for part in key.split('.'):
            value = value[part]
        assert isinstance(value,str) and value.strip(), (loc,key)
    index = pages[SITE / f'blog/{loc}/index.html']
    assert sum(t == 'h1' for t,_ in index.nodes) == 1, loc
    assert sum(t == 'a' and 'data-blog-id' in a for t,a in index.nodes) == 6, loc
    assert any(t == 'html' and a.get('lang') == loc for t,a in index.nodes), loc
    canonical = [a['href'] for t,a in index.nodes if t == 'link' and a.get('rel') == 'canonical']
    assert canonical == [f'https://myassetsflow.com/blog/{loc}/'], loc
    content = json.loads((ROOT / f'content/blog/{loc}.json').read_text())
    assert catalog['nav']['blogs'] == content['ui']['blogs'], f'Stale header label: {loc}'
    docs = pages[SITE / f'docs/{loc}/index.html']
    assert sum(tag == 'a' and f'/docs/{loc}/' in attrs.get('href', '') and attrs['href'].rstrip('/').count('/') == 3 for tag, attrs in docs.nodes) == 3, f'Expected three product guides: {loc}'
    assert any(tag == 'html' and attrs.get('lang') == loc and attrs.get('dir') == ('rtl' if loc == 'ar' else 'ltr') for tag, attrs in docs.nodes)
    assert sum(tag == 'a' and attrs.get('hreflang') in LOCALES for tag, attrs in docs.nodes) == 6
    for slug in ('add-an-asset', 'organize-records', 'plan-maintenance'):
        doc = pages[SITE / f'docs/{loc}/{slug}/index.html']
        assert sum(tag == 'h1' for tag, _ in doc.nodes) == 1
        assert any(tag == 'html' and attrs.get('lang') == loc and attrs.get('dir') == ('rtl' if loc == 'ar' else 'ltr') for tag, attrs in doc.nodes)
        assert len([attrs for tag, attrs in doc.nodes if tag == 'link' and attrs.get('hreflang') in LOCALES]) == 6
assert 'blogs' not in home.ids, 'Homepage must contain only the Blog entry link, not article previews'
print(f'Public artifact verified: {len(articles)} articles, {len(urls)} sitemap entries, {checked} local references, six locale catalogs.')
