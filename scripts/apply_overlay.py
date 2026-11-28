#!/usr/bin/env python3
"""
Build an organisation's effective register from the ARC register and an overlay.

An organisation that contextualises ARC should not copy the register and edit it: the copy
drifts as soon as ARC releases a new version. It keeps an overlay instead, a single file that
adds its own entries, changes fields of existing ones, and removes what it does not use,
all by ID. This script applies the overlay and writes the result as a directory with the
same layout as arc-risk-register/, which ARCvisor and the assessment skill can read.

    python scripts/apply_overlay.py --overlay our-overlay.yaml --out build/our-register
    python scripts/apply_overlay.py --overlay our-overlay.yaml --base path/to/arc-risk-register --out DIR

The result is validated with the same checks as the ARC register. Moving to a new ARC
version means changing `base` in the overlay and running this again: anything the overlay
changes or removes that no longer exists upstream is reported as an error to resolve.

The overlay format is described in docs/implementation/for-governance-teams.md, and
examples/overlay/example-agency.yaml is a worked example.
"""

import argparse
import shutil
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(ROOT / 'skills' / 'arc-assessment' / 'scripts'))
import arc  # noqa: E402  (the overlay logic lives with the skill, which must stay a single file)
import validate_risk_register  # noqa: E402

WRITTEN = ('register', 'risks', 'controls', 'capabilities', 'combinations')   # files an overlay can change
COPIED = ('components', 'design', 'harms', 'crosswalk_references')          # files it cannot


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--overlay', type=Path, required=True, help="the organisation's overlay file")
    parser.add_argument('--base', type=Path, default=ROOT / 'arc-risk-register',
                        help='the ARC register to apply it to (default: this repository\'s)')
    parser.add_argument('--out', type=Path, required=True, help='directory to write the effective register to')
    args = parser.parse_args()

    overlay = arc.read_overlay(str(args.overlay))
    base = {}
    for name in arc.REGISTER_FILES + arc.OPTIONAL_FILES:
        path = args.base / f'{name}.yaml'
        base[name] = yaml.safe_load(path.read_text()) if path.exists() else None
    base['harms'] = base['harms'] or {}
    wanted, have = str(overlay['overlay']['base']), str(base['register'].get('version'))
    if wanted != have:
        print(f'  warning: the overlay was written against register {wanted}; the base here is {have}')
    try:
        effective, notes = arc.apply_overlay(base, overlay)
    except arc.ArcError as e:
        raise SystemExit(f'✗ {e}')
    for note in notes:
        print(f'  note: {note}')

    args.out.mkdir(parents=True, exist_ok=True)
    for name in WRITTEN:
        if effective.get(name) is not None:
            (args.out / f'{name}.yaml').write_text(
                yaml.safe_dump(effective[name], sort_keys=False, allow_unicode=True, width=1000))
    for name in COPIED:
        if (args.base / f'{name}.yaml').exists():
            shutil.copyfile(args.base / f'{name}.yaml', args.out / f'{name}.yaml')

    validate_risk_register.DATA_DIR = args.out
    errors, warnings = validate_risk_register.validate()
    if errors:
        for e in errors:
            print(f'  ERROR: {e}', file=sys.stderr)
        raise SystemExit(f'✗ The effective register has {len(errors)} validation error(s)')
    live = lambda entries: sum(1 for v in entries.values() if not v.get('superseded_by'))
    changed = lambda entries, how: sum(1 for v in entries.values() if v.get('overlay') == how)
    print(f"✓ Wrote {args.out}: {live(effective['risks'])} risks and {live(effective['controls'])} controls "
          f"({changed(effective['risks'], 'added') + changed(effective['controls'], 'added')} added, "
          f"{changed(effective['risks'], 'changed') + changed(effective['controls'], 'changed')} changed by the overlay)")


if __name__ == '__main__':
    main()
