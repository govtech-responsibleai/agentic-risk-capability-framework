#!/usr/bin/env python3
"""
Compare the ARC incident file with the risk register.

    python scripts/incident_coverage.py                 # print the report (Markdown)
    python scripts/incident_coverage.py --out FILE      # write it to a file

The report answers two questions. Which cases does the register not describe, grouped by
theme? Those are candidates for new risks or controls. And which risks have no case behind
them? Those rest on argument or research alone, which may be fine but is worth knowing.
"""

import argparse
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))
import validate_incidents  # noqa: E402

ROOT = Path(__file__).parent.parent
INCIDENTS_DIR = ROOT / 'incidents'
REGISTER_DIR = ROOT / 'arc-risk-register'
KIND_ORDER = ('harm', 'vulnerability', 'research')


def load(directory, filename):
    return yaml.safe_load((directory / filename).read_text())


def kinds(case_ids, cases):
    count = Counter(cases[c]['kind'] for c in case_ids)
    return ', '.join(f'{count[k]} {k}' for k in KIND_ORDER if count[k]) or '—'


def build_report():
    cases = load(INCIDENTS_DIR, 'incidents.yaml') or {}
    themes = load(INCIDENTS_DIR, 'gap-themes.yaml')
    risks = load(REGISTER_DIR, 'risks.yaml')
    register = load(REGISTER_DIR, 'register.yaml')
    elements = {**load(REGISTER_DIR, 'components.yaml'), **load(REGISTER_DIR, 'design.yaml'),
                **load(REGISTER_DIR, 'capabilities.yaml')}

    by_risk, by_element, by_theme = defaultdict(list), defaultdict(list), defaultdict(list)
    for case_id, case in cases.items():
        for risk_id in case.get('risks') or []:
            by_risk[risk_id].append(case_id)
        for element_id in case.get('elements') or []:
            by_element[element_id].append(case_id)
        if case.get('gap'):
            by_theme[case['gap']['theme']].append(case_id)

    uncovered = [c for c, case in cases.items() if not case.get('risks')]
    partial = [c for c, case in cases.items() if case.get('risks') and case.get('gap')]
    years = Counter(str(case['date'])[:4] for case in cases.values())
    lines = [
        f"# Incident coverage of register {register['version']}",
        '',
        f"{len(cases)} cases: {kinds(cases, cases)}. "
        f"{sum(1 for c in cases.values() if c['evidence'] == 'primary')} rest on a primary source and "
        f"{sum(1 for c in cases.values() if c['evidence'] == 'press')} on press coverage. "
        f"{sum(1 for c in cases.values() if c['status'] == 'verified')} have been verified against their source; "
        'the rest were triaged from an upstream record. By year: '
        + ', '.join(f'{y}: {n}' for y, n in sorted(years.items())) + '.',
        '',
        f"The register describes {len(cases) - len(uncovered) - len(partial)} cases fully and {len(partial)} in part. "
        f"It has no risk for {len(uncovered)}.",
        '',
        '## Gaps, by theme',
        '',
        'A case appears here when no risk describes it, or when a risk describes only part of it.',
        '',
        '| Theme | Cases | No risk at all | Kinds | Cases (earliest first) |',
        '| --- | ---: | ---: | --- | --- |',
    ]
    for theme, case_ids in sorted(by_theme.items(), key=lambda kv: -len(kv[1])):
        none = sum(1 for c in case_ids if not cases[c].get('risks'))
        ordered = sorted(case_ids, key=lambda c: str(cases[c]['date']))
        lines.append(f"| **{theme}**: {themes.get(theme, '')} | {len(case_ids)} | {none} | {kinds(case_ids, cases)} | "
                     + ', '.join(ordered) + ' |')

    lines += ['', '## Risks, by number of cases', '', '| Risk | Cases | Kinds |', '| --- | ---: | --- |']
    live = {r: v for r, v in risks.items() if not v.get('superseded_by')}
    for risk_id in sorted(live, key=lambda r: (-len(by_risk[r]), r)):
        if by_risk[risk_id]:
            lines.append(f"| {risk_id} {live[risk_id]['statement']} | {len(by_risk[risk_id])} | {kinds(by_risk[risk_id], cases)} |")
    without = [r for r in live if not by_risk[r]]
    lines += ['', f'## Risks with no case ({len(without)} of {len(live)})', '']
    lines += [f"- {r} {live[r]['statement']} ({' + '.join(live[r]['element_ids'])})" for r in without] or ['None.']

    lines += ['', '## Elements, by number of cases', '', '| Element | Cases | Kinds |', '| --- | ---: | --- |']
    for element_id, element in elements.items():
        lines.append(f"| {element_id} {element['name']} | {len(by_element[element_id])} | {kinds(by_element[element_id], cases)} |")
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--out', type=Path, help='write the report to this file instead of printing it')
    args = parser.parse_args()
    errors, _ = validate_incidents.validate()
    if errors:
        raise SystemExit(f'✗ The incident file has {len(errors)} validation error(s); run scripts/validate_incidents.py')
    report = build_report()
    if args.out:
        args.out.write_text(report)
        print(f'wrote {args.out}')
    else:
        print(report)


if __name__ == '__main__':
    main()
