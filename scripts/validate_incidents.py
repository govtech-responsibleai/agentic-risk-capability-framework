#!/usr/bin/env python3
"""
Validation checks for the ARC incident file (incidents/*.yaml).

    python scripts/validate_incidents.py

Checks:
  - case IDs are well-formed (CASE-####)
  - every case has a title, date, kind, cause, evidence, status, summary, elements, risks and sources
  - kind, cause, evidence and status come from the allowed sets; the date is YYYY, YYYY-MM or YYYY-MM-DD
  - elements and risks exist in the risk register (arc-risk-register/), and a risk that has
    been superseded is not cited
  - a case that cites no risk says what the register is missing (`gap`), and every gap theme
    is defined in gap-themes.yaml
  - sources are http(s) URLs; external_ids name sources defined in sources.yaml (or cve, ghsa)
  - every triage-log entry names a lead and gives an allowed reason
  - warnings (non-fatal) when two cases cite the same source page
"""

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
INCIDENTS_DIR = ROOT / 'incidents'
REGISTER_DIR = ROOT / 'arc-risk-register'

KINDS = {'harm', 'vulnerability', 'research'}
CAUSES = {'attack', 'agent-error', 'agent-goal-seeking', 'user-misuse', 'platform-fault'}
EVIDENCE = {'primary', 'press'}
STATUSES = {'triaged', 'verified'}
REASONS = {'not-agentic', 'offensive-use', 'no-event', 'generic-infrastructure', 'insufficient-evidence',
           'out-of-period'}
CASE_ID = re.compile(r'^CASE-\d{4}$')
DATE = re.compile(r'^\d{4}(-\d{2}(-\d{2})?)?$')
REQUIRED = ('title', 'date', 'kind', 'cause', 'evidence', 'status', 'summary', 'elements', 'sources')


def load(directory, filename):
    with open(directory / filename, 'r') as f:
        return yaml.safe_load(f)


def normalise_url(url):
    url = re.sub(r'^https?://(www\.)?', '', str(url).strip().lower())
    return re.sub(r'[?#].*$', '', url).rstrip('/')


def validate():
    """Return (errors, warnings) as lists of strings."""
    errors, warnings = [], []
    cases = load(INCIDENTS_DIR, 'incidents.yaml') or {}
    themes = load(INCIDENTS_DIR, 'gap-themes.yaml') or {}
    sources = load(INCIDENTS_DIR, 'sources.yaml') or {}
    log = load(INCIDENTS_DIR, 'triage-log.yaml') or []
    risks = load(REGISTER_DIR, 'risks.yaml')
    elements = {**load(REGISTER_DIR, 'components.yaml'), **load(REGISTER_DIR, 'design.yaml'),
                **load(REGISTER_DIR, 'capabilities.yaml')}

    cited = {}
    for case_id, case in cases.items():
        if not CASE_ID.match(str(case_id)):
            errors.append(f'{case_id}: malformed case ID')
        if not isinstance(case, dict):
            errors.append(f'{case_id}: must be a mapping')
            continue
        for field in REQUIRED:
            if not case.get(field):
                errors.append(f'{case_id}: missing or empty field "{field}"')
        if 'risks' not in case or not isinstance(case['risks'], list):
            errors.append(f'{case_id}: risks must be a list (empty if no risk in the register describes the case)')
        if case.get('kind') not in KINDS:
            errors.append(f'{case_id}: kind must be one of {sorted(KINDS)}')
        if case.get('cause') not in CAUSES:
            errors.append(f'{case_id}: cause must be one of {sorted(CAUSES)}')
        if case.get('evidence') not in EVIDENCE:
            errors.append(f'{case_id}: evidence must be one of {sorted(EVIDENCE)}')
        if case.get('status') not in STATUSES:
            errors.append(f'{case_id}: status must be one of {sorted(STATUSES)}')
        if not DATE.match(str(case.get('date', ''))):
            errors.append(f'{case_id}: date must be a quoted YYYY, YYYY-MM or YYYY-MM-DD (got {case.get("date")!r})')
        for element_id in case.get('elements') or []:
            if element_id not in elements:
                errors.append(f'{case_id}: unknown element "{element_id}"')
        for risk_id in case.get('risks') or []:
            if risk_id not in risks:
                errors.append(f'{case_id}: unknown risk "{risk_id}"')
            elif risks[risk_id].get('superseded_by'):
                errors.append(f'{case_id}: {risk_id} is superseded by {risks[risk_id]["superseded_by"]}')
        gap = case.get('gap')
        if not case.get('risks') and not gap:
            errors.append(f'{case_id}: cites no risk, so it must say what the register is missing (gap)')
        if gap is not None:
            if not isinstance(gap, dict) or not gap.get('theme') or not gap.get('note'):
                errors.append(f'{case_id}: gap needs a theme and a note')
            elif gap['theme'] not in themes:
                errors.append(f'{case_id}: unknown gap theme "{gap["theme"]}"')
        for url in case.get('sources') or []:
            if not re.match(r'^https?://\S+$', str(url)):
                errors.append(f'{case_id}: source {url!r} is not a URL')
            cited.setdefault(normalise_url(url), []).append(case_id)
        for key in (case.get('external_ids') or {}):
            if key not in sources and key not in ('cve', 'ghsa'):
                errors.append(f'{case_id}: external_ids names "{key}", which is not in sources.yaml')

    for url, case_ids in cited.items():
        if len(case_ids) > 1:
            warnings.append(f'{", ".join(case_ids)} cite the same source: {url}')

    for i, entry in enumerate(log, 1):
        where = f'triage-log.yaml entry {i}'
        if not isinstance(entry, dict) or not (entry.get('url') or (entry.get('source') and entry.get('source_id'))):
            errors.append(f'{where}: needs a url, or a source and source_id')
            continue
        if entry.get('source') and entry['source'] not in sources:
            errors.append(f'{where}: source "{entry["source"]}" is not in sources.yaml')
        if entry.get('reason') not in REASONS:
            errors.append(f'{where}: reason must be one of {sorted(REASONS)}')
    return errors, warnings


def main():
    errors, warnings = validate()
    for w in warnings:
        print(f'  warning: {w}')
    if errors:
        for e in errors:
            print(f'  ERROR: {e}', file=sys.stderr)
        print(f'\n✗ Incident file validation failed with {len(errors)} error(s)', file=sys.stderr)
        sys.exit(1)
    cases = load(INCIDENTS_DIR, 'incidents.yaml') or {}
    print(f'✓ Incident file valid: {len(cases)} cases ({len(warnings)} warning(s))')


if __name__ == '__main__':
    main()
