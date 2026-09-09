"""Detect Chinese source changes that need English editorial review."""
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / 'locales/en/reviewed-sources.json'

def sources():
    return [ROOT / p for p in ('profile.json', 'site.json', 'locales/zh.json')] + sorted((ROOT / 'projects').glob('*.md')) + [p for p in sorted((ROOT / 'posts').glob('*.md')) if (ROOT / 'locales/en/posts' / p.name).exists()]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record', nargs='+', metavar='SOURCE', help='Record specific source files after reviewing their English translations.')
    args = parser.parse_args()
    current = {p.relative_to(ROOT).as_posix(): digest(p) for p in sources()}
    reviewed = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    if args.record:
        for name in args.record:
            if name not in current:
                parser.error(f'Not a tracked source: {name}')
            reviewed[name] = current[name]
        reviewed = {k: v for k, v in reviewed.items() if k in current}
        MANIFEST.write_text(json.dumps(reviewed, indent=2) + '\n')
    stale = [name for name, value in current.items() if reviewed.get(name) != value]
    if stale:
        print('English translations need review for: ' + ', '.join(stale))
        print('Update the English files, then record only the reviewed sources with --record.')
        raise SystemExit(1)
    print(f'English translations reviewed against {len(current)} current source files.')

if __name__ == '__main__':
    main()
