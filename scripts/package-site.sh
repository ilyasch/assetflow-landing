#!/usr/bin/env bash
set -euo pipefail

# Upload public files only, never the repository root or deployment credentials.
mkdir -p dist
cp index.html styles.css blog.css main.js dist/
cp -R assets locales dist/
for file in robots.txt sitemap.xml llms.txt index.md _headers _redirects 404.html; do
  if [[ -f "$file" ]]; then
    cp "$file" dist/
  fi
done
python3 scripts/build-blog.py --output dist
python3 scripts/build-docs.py --output dist
python3 scripts/build-marketing-pages.py --output dist
node --check main.js
python3 - <<'PY'
import json
from pathlib import Path

for locale in ('en', 'it', 'de', 'es', 'fr', 'ar'):
    json.loads(Path(f'dist/locales/{locale}.json').read_text())
print('Public site packaged; JavaScript syntax and six locale JSON files validated.')
PY
python3 scripts/version-assets.py
python3 scripts/verify-site.py
