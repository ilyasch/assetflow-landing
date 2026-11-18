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

marketing_pages = {}
for section in ('explore', 'ai'):
    marketing_pages[section] = []
    for loc in LOCALES:
        path = SITE / section / loc / 'index.html'
        page = pages[path]
        assert sum(tag == 'h1' for tag, _ in page.nodes) == 1, path
        assert any(tag == 'html' and attrs.get('lang') == loc and attrs.get('dir') == ('rtl' if loc == 'ar' else 'ltr') for tag, attrs in page.nodes), path
        canonical = [attrs['href'] for tag, attrs in page.nodes if tag == 'link' and attrs.get('rel') == 'canonical']
        assert canonical == [f'https://myassetsflow.com/{section}/{loc}/'], path
        assert sum(tag == 'link' and attrs.get('hreflang') in LOCALES for tag, attrs in page.nodes) == 6, path
        canonical_urls.update(canonical)
        marketing_pages[section].append(page)

sitemap = ET.parse(SITE / 'sitemap.xml')
urls = {x.text for x in sitemap.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
index_urls = {f'https://myassetsflow.com/blog/{loc}/' for loc in LOCALES}
docs_urls = {f'https://myassetsflow.com/docs/{loc}/' for loc in LOCALES} | {f'https://myassetsflow.com/docs/{loc}/{slug}/' for loc in LOCALES for slug in ('add-an-asset', 'organize-records', 'plan-maintenance', 'connect-your-ai-assistant')}
marketing_urls = {f'https://myassetsflow.com/{section}/{loc}/' for section in ('explore', 'ai') for loc in LOCALES}
assert urls == canonical_urls | index_urls | docs_urls | marketing_urls | {f'https://myassetsflow.com/{loc}/' for loc in LOCALES} | {'https://myassetsflow.com/'}, 'Sitemap and canonical pages differ'
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
solutions = pages[SITE / 'explore/en/index.html']
assert sum(t == 'th' and a.get('scope') == 'col' for t,a in solutions.nodes) == 5, 'Expected four market columns plus row labels'
assert sum(t == 'th' and a.get('scope') == 'row' for t,a in solutions.nodes) == 5, 'Expected five market comparison rows'
assert any(a.get('class') == 'matrix-region' and a.get('tabindex') == '0' and a.get('role') == 'region' and a.get('aria-labelledby') for _,a in solutions.nodes), 'Market matrix must support keyboard scrolling and have a name'

for loc in LOCALES:
    catalog = json.loads((SITE / f'locales/{loc}.json').read_text())
    for key in keys:
        value = catalog
        for part in key.split('.'):
            value = value[part]
        assert isinstance(value,str) and value.strip(), (loc,key)
    for section in ('explore', 'ai'):
        page = pages[SITE / section / loc / 'index.html']
        page_keys = [attrs[key] for _, attrs in page.nodes for key in ('data-i18n', 'data-i18n-aria') if key in attrs]
        for key in page_keys:
            value = catalog
            for part in key.split('.'):
                value = value[part]
            assert isinstance(value, str) and value.strip(), (loc, section, key)
    index = pages[SITE / f'blog/{loc}/index.html']
    assert sum(t == 'h1' for t,_ in index.nodes) == 1, loc
    assert sum(t == 'a' and 'data-blog-id' in a for t,a in index.nodes) == 6, loc
    assert any(t == 'html' and a.get('lang') == loc for t,a in index.nodes), loc
    canonical = [a['href'] for t,a in index.nodes if t == 'link' and a.get('rel') == 'canonical']
    assert canonical == [f'https://myassetsflow.com/blog/{loc}/'], loc
    content = json.loads((ROOT / f'content/blog/{loc}.json').read_text())
    assert catalog['nav']['blogs'] == content['ui']['blogs'], f'Stale header label: {loc}'
    docs = pages[SITE / f'docs/{loc}/index.html']
    assert any(t == 'a' and a.get('href') == f'/{loc}/' for t,a in docs.nodes), f'Missing guides-to-home link: {loc}'
    assert any(t == 'a' and a.get('href') == f'/docs/{loc}/' for t,a in index.nodes), f'Missing blog-to-guides link: {loc}'
    assert sum(tag == 'a' and f'/docs/{loc}/' in attrs.get('href', '') and attrs['href'].rstrip('/').count('/') == 3 for tag, attrs in docs.nodes) == 4, f'Expected four product guides: {loc}'
    assert any(tag == 'html' and attrs.get('lang') == loc and attrs.get('dir') == ('rtl' if loc == 'ar' else 'ltr') for tag, attrs in docs.nodes)
    assert sum(tag == 'a' and attrs.get('hreflang') in LOCALES for tag, attrs in docs.nodes) == 6
    for slug in ('add-an-asset', 'organize-records', 'plan-maintenance', 'connect-your-ai-assistant'):
        doc = pages[SITE / f'docs/{loc}/{slug}/index.html']
        assert sum(tag == 'h1' for tag, _ in doc.nodes) == 1
        assert any(tag == 'html' and attrs.get('lang') == loc and attrs.get('dir') == ('rtl' if loc == 'ar' else 'ltr') for tag, attrs in doc.nodes)
        assert len([attrs for tag, attrs in doc.nodes if tag == 'link' and attrs.get('hreflang') in LOCALES]) == 6
# Rich connector guides must remain complete, localized static documents.
for loc in LOCALES:
    path = SITE / f'docs/{loc}/connect-your-ai-assistant/index.html'
    page = pages[path]
    source = path.read_text()
    content = json.loads((ROOT / f'content/guides/{loc}.json').read_text())
    assert len(content['sections']) == 13, f'Missing connector section: {loc}'
    assert len(content['sections'][3]['examples']) == 3, f'Missing prompts: {loc}'
    assert all(content['sections'][i].get('notice') for i in range(6, 10)), f'Missing verification status: {loc}'
    assert not any(tag == 'script' for tag, _ in page.nodes), f'Guide must work without JavaScript: {loc}'
    assert [a['href'] for t,a in page.nodes if t == 'link' and a.get('rel') == 'canonical'] == [f'https://myassetsflow.com/docs/{loc}/connect-your-ai-assistant/']
    assert [a['href'] for t,a in page.nodes if t == 'link' and a.get('hreflang') == 'x-default'] == ['https://myassetsflow.com/docs/en/connect-your-ai-assistant/']
    assert any(t == 'meta' and a.get('name') == 'description' and a.get('content') == content['description'] for t,a in page.nodes)
    assert any(t == 'meta' and a.get('property') == 'og:title' and a.get('content') == content['title'] for t,a in page.nodes)
    for other in LOCALES:
        assert any(t == 'a' and a.get('href') == f'/docs/{other}/connect-your-ai-assistant/' and a.get('hreflang') == other for t,a in page.nodes), f'Wrong equivalent language link: {loc}/{other}'
    assert not re.search(r'https?://[^\s<>"\']*(?:localhost|mcp-dev|run\.app|dev\.myassetsflow)', source), f'Non-production connection value: {loc}'
    for section in content['sections']:
        assert section['title'] and section['body']
        for shot in section.get('screenshots', []):
            assert shot['alt'] and shot['caption'] and shot['uiLanguage']
            assert len(shot['sources']) >= 2 and shot['width'] > 0 and shot['height'] > 0
            for variant in shot['sources']:
                assert (ROOT / variant['src'].lstrip('/')).is_file(), f'Missing source screenshot: {variant}'
    screenshots = [a for t,a in page.nodes if t == 'img' and a.get('class') != 'brand-wordmark']
    assert screenshots and all(a.get('alt') and a.get('srcset') and a.get('sizes') and a.get('loading') == 'lazy' for a in screenshots), f'Incomplete responsive screenshots: {loc}'
for loc in LOCALES:
    path = SITE / loc / 'index.html'
    page = pages[path]
    catalog = json.loads((ROOT / f'locales/{loc}.json').read_text())
    assert any(t == 'a' and a.get('href') == f'/ai/{loc}/' for t,a in page.nodes), f'Missing AI navigation: {loc}'
    assert not any('hero-ai-integration' in a.get('class', '').split() for _,a in page.nodes), f'Removed hero integration paragraph returned: {loc}'
    assert any(t == 'html' and a.get('lang') == loc and a.get('dir') == ('rtl' if loc == 'ar' else 'ltr') for t,a in page.nodes)
    ai = pages[SITE / f'ai/{loc}/index.html']
    assert {'flow-ai', 'preferred-ai', 'ai-security', 'ai-agentic'} <= ai.ids
    assert sum(t == 'a' and 'ai-nav-card' in a.get('class', '').split() for t,a in ai.nodes) == 4, f'Missing AI navigation cards: {loc}'
    assert not any(t == 'a' and a.get('data-doc-article') == 'connect-your-ai-assistant' for t,a in ai.nodes), 'AI setup guide deferred'
    for key in ('lead', 'securityTitle', 'agentTitle', 'approvalBody', 'readBody'):
        assert catalog['aiPage'][key] in (SITE / f'ai/{loc}/index.html').read_text()
    assert catalog['preferredAI']['title'] in (SITE / f'ai/{loc}/index.html').read_text()
    assert not {'flow-ai', 'preferred-ai'} & page.ids, f'AI sections must move off Home: {loc}'
    assert [a['href'] for t,a in page.nodes if t == 'link' and a.get('rel') == 'canonical'] == [f'https://myassetsflow.com/{loc}/']
    assert [a['href'] for t,a in page.nodes if t == 'link' and a.get('hreflang') == 'x-default'] == ['https://myassetsflow.com/']
    assert len([a for t,a in page.nodes if t == 'link' and a.get('hreflang') in LOCALES]) == 6
assert not {'flow-ai', 'preferred-ai'} & home.ids, 'AI sections must live on the AI page'
assert not any(t == 'a' and a.get('data-doc-article') == 'connect-your-ai-assistant' for t,a in home.nodes), 'Guide CTA deferred until guide review'
assert 'blogs' not in home.ids, 'Homepage must contain only the Blog entry link, not article previews'


for loc in LOCALES:
    path = SITE / f'explore/{loc}/index.html'
    source = path.read_text()
    assert source.index('id="editions"') < source.index('id="pricing"'), f'Solutions must precede pricing: {loc}'
    assert sum(t == 'a' and a.get('href') in ('#editions', '#pricing') for t,a in pages[path].nodes) >= 3
    assert any(t == 'a' and 'data-market-start' in a and a.get('href') == '#pricing' for t,a in pages[path].nodes), f'Home selection should lead to plans: {loc}'
    for old, anchor in (('pricing', 'pricing'), ('solutions', 'editions')):
        redirect = pages[SITE / f'{old}/{loc}/index.html']
        assert any(t == 'meta' and a.get('http-equiv') == 'refresh' and a.get('content') == f'0;url=/explore/{loc}/#{anchor}' for t,a in redirect.nodes)

for loc in LOCALES:
    ai = pages[SITE / f'ai/{loc}/index.html']
    source = (SITE / f'ai/{loc}/index.html').read_text()
    for mark in ('chatgpt.', 'claude.', 'mcp.', 'mistral.'):
        assert any(t == 'img' and mark in a.get('src', '') for t,a in ai.nodes), f'Missing official logo {mark}: {loc}'
    assert sum(t == 'div' and 'ai-provider-card' in a.get('class', '').split() for t,a in ai.nodes) == 5, f'Missing AI tool examples: {loc}'
    assert any(t == 'figure' and a.get('class') == 'ai-control-panel' for t,a in ai.nodes)
    assert any(t == 'figure' and a.get('class') == 'ai-workflow-story' for t,a in ai.nodes)
    assert source.count('class="ai-access-row') == 3, f'Missing sharing illustration: {loc}'
    for class_name in ('ai-control-panel', 'ai-workflow-story'):
        fragment = source.split(f'class="{class_name}"', 1)[1].split('</figure>', 1)[0]
        assert '<button' not in fragment and '<input' not in fragment, f'Illustration must not imply live account controls: {loc}'


for path in (ROOT / 'assets/brands').glob('*.svg'):
    mark = path.read_text().lower()
    assert not re.search(r'<script|<foreignobject|\bonload=|\bhref=', mark), f'Unexpected active SVG content: {path}'
print(f'Public artifact verified: {len(articles)} articles, {len(urls)} sitemap entries, {checked} local references, six locale catalogs.')
