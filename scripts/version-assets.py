"""Create content-addressed public assets and update their deployed references."""
import hashlib
import re
from pathlib import Path
from _vendor.rcssmin import cssmin

root = Path('dist')
output = root / 'static'
output.mkdir(exist_ok=True)


def publish(path, data=None):
    data = path.read_bytes() if data is None else data
    digest = hashlib.sha256(data).hexdigest()[:16]
    name = f'{path.stem}.{digest}{path.suffix}'
    (output / name).write_bytes(data)
    return '/static/' + name


pages = {path: path.read_text() for path in root.rglob('*.html')}
css = (root / 'styles.css').read_text()
assets = sorted((root / 'assets').glob('assetflow-wordmark*.webp'))
assets += sorted((root / 'assets').glob('vehicle-photo*'))
assets += sorted((root / 'assets/fonts').glob('*.woff2'))
for path in assets:
    old = path.relative_to(root).as_posix()
    new = publish(path)
    pages = {path: text.replace('/' + old, new).replace(old, new) for path, text in pages.items()}
    css = css.replace(old, new)

css_url = publish(root / 'styles.css', cssmin(css).encode())
js_url = publish(root / 'main.js')
blog_css = cssmin((root / 'blog.css').read_text()).encode()
blog_url = publish(root / 'blog.css', blog_css)
for path, text in pages.items():
    text = re.sub(r'/?styles\.css\?v=\d+', css_url, text)
    text = re.sub(r'/?main\.js\?v=\d+', js_url, text)
    text = re.sub(r'/?blog\.css\?v=\d+', blog_url, text)
    path.write_text(text)
print('Content-hashed CSS, JavaScript, fonts, logos and photos published across all HTML pages.')
