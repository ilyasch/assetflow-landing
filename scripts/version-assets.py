"""Create content-addressed public assets and update their deployed references."""
import hashlib
import re
from pathlib import Path

root = Path('dist')
output = root / 'static'
output.mkdir(exist_ok=True)


def publish(path, data=None):
    data = path.read_bytes() if data is None else data
    digest = hashlib.sha256(data).hexdigest()[:16]
    name = f'{path.stem}.{digest}{path.suffix}'
    (output / name).write_bytes(data)
    return '/static/' + name


html = (root / 'index.html').read_text()
css = (root / 'styles.css').read_text()
assets = sorted((root / 'assets').glob('assetflow-wordmark*.webp'))
assets += sorted((root / 'assets/fonts').glob('*.woff2'))
for path in assets:
    old = path.relative_to(root).as_posix()
    new = publish(path)
    html = html.replace(old, new)
    css = css.replace(old, new)

css_url = publish(root / 'styles.css', css.encode())
js_url = publish(root / 'main.js')
html = re.sub(r'styles\.css\?v=\d+', css_url, html)
html = re.sub(r'main\.js\?v=\d+', js_url, html)
(root / 'index.html').write_text(html)
print('Content-hashed CSS, JavaScript, fonts and logo images published.')
