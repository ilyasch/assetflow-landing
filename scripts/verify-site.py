#!/usr/bin/env python3
"""Verify the deployed artifact, including nested pages and locale navigation."""
import json
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
assert len(articles) == 30, f'Expected 30 articles, found {len(articles)}'
checked = 0
for path, page in pages.items():
    for tag, attrs in page.nodes:
        for attr in ('href', 'src'):
            if attr not in attrs:
                continue
            target = urlsplit(attrs[attr])
            if target.scheme or target.netloc:
                continue
            dest = SITE / unquote(target.path).lstrip('/') if target.path.startswith('/') else path.parent / unquote(target.path)
            if not target.path:
                dest = path
            if dest.is_dir():
                dest /= 'index.html'
            dest = dest.resolve()
            assert dest.is_relative_to(SITE.resolve()), f'Escaping link: {attrs[attr]}'
            assert dest.is_file(), f'Missing {attrs[attr]} from {path}'
            if target.fragment and dest in pages:
                assert target.fragment in pages[dest].ids, f'Missing fragment: {attrs[attr]} from {path}'
            checked += 1

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
assert urls == canonical_urls | index_urls | {'https://myassetsflow.com/'}, 'Sitemap and canonical pages differ'
home = pages[SITE / 'index.html']
keys = [a['data-i18n'] for t,a in home.nodes if 'data-i18n' in a and a['data-i18n'].startswith(('blog.','nav.blogs'))]
for loc in LOCALES:
    catalog = json.loads((SITE / f'locales/{loc}.json').read_text())
    for key in keys:
        value = catalog
        for part in key.split('.'):
            value = value[part]
        assert isinstance(value,str) and value.strip(), (loc,key)
    index = pages[SITE / f'blog/{loc}/index.html']
    assert sum(t == 'h1' for t,_ in index.nodes) == 1, loc
    assert sum(t == 'a' and 'data-blog-id' in a for t,a in index.nodes) == 5, loc
    assert any(t == 'html' and a.get('lang') == loc for t,a in index.nodes), loc
    canonical = [a['href'] for t,a in index.nodes if t == 'link' and a.get('rel') == 'canonical']
    assert canonical == [f'https://myassetsflow.com/blog/{loc}/'], loc
    content = json.loads((ROOT / f'content/blog/{loc}.json').read_text())
    assert catalog['nav']['blogs'] == content['ui']['blogs'], f'Stale header label: {loc}'
assert 'blogs' not in home.ids, 'Homepage must contain only the Blog entry link, not article previews'
print(f'Public artifact verified: {len(articles)} articles, {len(urls)} sitemap entries, {checked} local references, six locale catalogs.')
