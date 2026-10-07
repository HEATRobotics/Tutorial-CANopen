from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
errors = []
for path in [root / 'README.md', root / 'CONTRIBUTING.md', *root.glob('docs/*.md')]:
    for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
        if '://' in target or target.startswith('#'):
            continue
        if not (path.parent / target.split('#')[0]).exists():
            errors.append(f'{path.relative_to(root)}: {target}')
if errors:
    raise SystemExit('\n'.join(errors))
print('Relative documentation links passed')
