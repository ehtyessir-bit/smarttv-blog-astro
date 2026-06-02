#!/usr/bin/env python3
"""
Internal Linking — Maillage interne automatique
================================================
Ajoute une section "Artikel lesen auch" à la fin de chaque article
avec 3-5 liens vers des articles sémantiquement proches.

Usage:
  python3 internal_linking.py          → analyse + aperçu (dry-run)
  python3 internal_linking.py --apply  → applique les liens
"""

import os, re, sys
from pathlib import Path

BLOG_DIR = Path('src/content/blog')
APPLY = '--apply' in sys.argv

# ─────────────────────────────────────────────
# 1. Lire tous les articles
# ─────────────────────────────────────────────

def read_article(path):
    text = path.read_text(encoding='utf-8')
    parts = text.split('---', 2)
    if len(parts) < 3:
        return None
    fm, body = parts[1], parts[2].strip()
    def fm_get(key):
        m = re.search(rf'^{key}:\s*["\']?(.+?)["\']?\s*$', fm, re.MULTILINE)
        return m.group(1).strip().strip('"\'') if m else ''
    return {
        'path': path,
        'slug': path.stem,
        'title': fm_get('title'),
        'description': fm_get('description'),
        'focusKeyword': fm_get('focusKeyword'),
        'keywords': fm_get('keywords'),
        'fm': fm,
        'body': body,
        'raw': text,
    }

articles = [a for a in (read_article(p) for p in sorted(BLOG_DIR.glob('*.md'))) if a]
print(f"📄 {len(articles)} articles chargés")

# ─────────────────────────────────────────────
# 2. Score de similarité simple (mots communs)
# ─────────────────────────────────────────────

STOPWORDS = {'der','die','das','und','in','für','von','mit','auf','ist','ein',
             'eine','zu','im','an','am','des','den','dem','als','auch','bei',
             'nicht','wie','so','oder','aus','durch','nach','über','unter'}

def tokens(art):
    text = f"{art['title']} {art['focusKeyword']} {art['keywords']} {art['description']}"
    return set(w.lower() for w in re.findall(r'\b\w{3,}\b', text) if w.lower() not in STOPWORDS)

token_map = {a['slug']: tokens(a) for a in articles}

def similarity(a, b):
    ta, tb = token_map[a['slug']], token_map[b['slug']]
    if not ta or not tb:
        return 0
    return len(ta & tb) / len(ta | tb)

# ─────────────────────────────────────────────
# 3. Pour chaque article, trouver les 4 plus proches
# ─────────────────────────────────────────────

RELATED_SECTION_MARKER = '<!-- INTERNAL_LINKS -->'

def already_has_links(art):
    return RELATED_SECTION_MARKER in art['body']

def build_links_section(art, related):
    lines = [
        '',
        RELATED_SECTION_MARKER,
        '',
        '---',
        '',
        '## Das könnte dich auch interessieren',
        '',
    ]
    for r in related:
        lines.append(f"- [{r['title']}](/blog/{r['slug']}/)")
    lines.append('')
    return '\n'.join(lines)

ok, skip = 0, 0
for art in articles:
    if already_has_links(art):
        skip += 1
        continue

    # Trouver les 4 articles les plus proches (sauf lui-même)
    scores = [(similarity(art, b), b) for b in articles if b['slug'] != art['slug']]
    scores.sort(key=lambda x: -x[0])
    related = [b for _, b in scores[:4] if _ > 0]

    if not related:
        skip += 1
        continue

    links_section = build_links_section(art, related)
    new_body = art['body'] + links_section
    new_raw = f"---{art['fm']}---\n\n{new_body}"

    if APPLY:
        art['path'].write_text(new_raw, encoding='utf-8')
        print(f"  ✅ {art['slug']} → {len(related)} liens ajoutés")
    else:
        print(f"  🔍 {art['slug']}")
        for r in related:
            print(f"      → [{r['title']}](/blog/{r['slug']}/)")
    ok += 1

print(f"\n{'─'*50}")
if APPLY:
    print(f"✅ {ok} articles mis à jour | ⏭  {skip} déjà traités ou sans liens")
else:
    print(f"DRY-RUN: {ok} articles à lier | {skip} ignorés")
    print(f"\nPour appliquer: python3 internal_linking.py --apply")
