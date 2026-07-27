#!/usr/bin/env python3
"""What the site does not reach.

Walks outward from the pages actually served, following every src, href and
url() through the HTML, CSS and JS, and prints what is left over. It moves
nothing and deletes nothing; `unused/` is where the last run's leftovers went.

Reachability from real entry points is the whole point. A search for a filename
answers the wrong question: `admits-green/adya.svg` and `admits-blue/adya.svg`
share a basename, and `mock-index.html` is itself unreachable while being the
only thing that still points at half the green theme. Both read as live to
anything that greps.

    python3 tools/find-unused.py
"""

import os
import posixpath
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# unused/ is the archive, not a source of truth: anything in it is leftover by
# definition and must not keep anything else alive.
SKIP_DIRS = {'.git', '.wrangler', 'node_modules', 'unused'}

# Not reachable from a page, and not spare either.
KEEP_PREFIX = ('docs/', 'tools/', 'apps-script/', '.claude/')
KEEP_EXACT = {'CLAUDE.md', 'PRODUCT.md', 'README.md', 'skills-lock.json',
              'favicon.svg', 'Indian_Schools_Fees_Complete_Reviewed_2026.csv'}

REF = re.compile(
    r'''(?:src|href|data-src|poster|data-calendly-url)\s*=\s*["']([^"'<>]+)["']'''
    r'''|url\(\s*["']?([^"')]+)["']?\s*\)'''
    r'''|["']([^"'<>\s]+\.(?:png|jpe?g|webp|svg|gif|avif|woff2?|ttf|otf|pdf|mp4|csv|js|css))["']''',
    re.I)


def all_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames
                       if d not in SKIP_DIRS and not d.startswith('.')]
        for name in filenames:
            if not name.startswith('.'):
                rel = os.path.relpath(os.path.join(dirpath, name), ROOT)
                yield rel.replace(os.sep, '/')


def entry_points(files):
    """The pages the site serves. Everything it needs hangs off these."""
    pages = ['index.html', 'start.html', 'next-steps.html', 'method.html',
             'results.html', 'fit.html', 'team.html', 'founder.html']
    pages += sorted(f for f in files
                    if f.startswith('case-studies/') and f.endswith('.html'))
    pages += sorted(f for f in files
                    if re.match(r'(lp|iblp)/[^/]+\.html$', f))
    return [p for p in pages if p in files]


def references(path):
    if os.path.splitext(path)[1].lower() not in {'.html', '.css', '.js'}:
        return
    try:
        text = open(os.path.join(ROOT, path), encoding='utf-8', errors='ignore').read()
    except OSError:
        return
    base = posixpath.dirname(path)
    for match in REF.finditer(text):
        raw = (match.group(1) or match.group(2) or match.group(3) or '').strip()
        if not raw or raw.startswith(('http', '//', 'data:', 'mailto:', 'tel:', '#', '{{')):
            continue
        raw = raw.split('#')[0].split('?')[0]
        if raw:
            yield posixpath.normpath(posixpath.join(base, raw) if base else raw).lstrip('./')


def main():
    files = set(all_files())
    entries = entry_points(files)

    reached, queue, missing = set(), list(entries), set()
    while queue:
        current = queue.pop()
        if current in reached:
            continue
        reached.add(current)
        for ref in references(current):
            if ref in files:
                queue.append(ref)
            elif os.path.splitext(ref)[1]:
                missing.add((current, ref))

    spare = sorted(f for f in files
                   if f not in reached
                   and not f.startswith(KEEP_PREFIX)
                   and f not in KEEP_EXACT
                   and not f.endswith('.py'))

    print('%d entry pages, %d files reached, %d spare\n'
          % (len(entries), len(reached), len(spare)))

    if spare:
        groups = {}
        for f in spare:
            groups.setdefault(f.split('/')[0] if '/' in f else '(root)', []).append(f)
        print('Spare:')
        for name, items in sorted(groups.items(), key=lambda kv: -len(kv[1])):
            print('  %-34s %4d' % (name, len(items)))
            for item in items[:6]:
                print('      %s' % item)
            if len(items) > 6:
                print('      ... and %d more' % (len(items) - 6))
        print()

    # A page pointing at a file that is not there is the opposite problem and
    # worth more than the leftovers, so it prints last.
    if missing:
        print('Referenced but not present (%d):' % len(missing))
        for src, ref in sorted(missing):
            print('  %-30s -> %s' % (src, ref))

    return 1 if missing else 0


if __name__ == '__main__':
    sys.exit(main())
