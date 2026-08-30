#!/usr/bin/env python3
"""
Validation checks for the ARC risk register YAML files.

Run standalone (`python scripts/validate_risk_register.py`) or via
build_risk_register.py, which validates before building the site JSON.
Exits non-zero if any error is found, so a broken register cannot be
built or deployed silently.

Checks:
  - IDs are well-formed (RISK-###, CTRL-####, CMP/DSN/CAP-##)
  - every risk has statement, description, element_ids, failure_mode, type, controls
  - element_ids is a non-empty list of distinct, defined components, design elements,
    or capabilities (a risk with several elements arises from their combination)
  - failure_mode and type values come from the allowed sets
  - every control has a statement, a valid level (0/1/2), and at least one risk
  - risk->control and control->risk mappings are exactly inverse-consistent
  - warnings (non-fatal) for empty sources or missing recommendations
"""

import re
import sys
from pathlib import Path

import yaml

DATA_DIR = Path(__file__).parent.parent / 'arc-risk-register'

FAILURE_MODES = {'Agent Failure', 'External Manipulation', 'Tool or Resource Malfunction'}
RISK_TYPES = {'Safety', 'Security'}
RISK_ID = re.compile(r'^RISK-\d{3}$')
CTRL_ID = re.compile(r'^CTRL-\d{4}$')
ELEMENT_ID = re.compile(r'^(CMP|DSN|CAP)-\d{2}$')


def load(filename):
    with open(DATA_DIR / filename, 'r') as f:
        return yaml.safe_load(f)


def validate():
    """Return (errors, warnings) as lists of strings."""
    errors, warnings = [], []

    risks = load('risks.yaml')
    controls = load('controls.yaml')
    elements = {**load('components.yaml'), **load('design.yaml'), **load('capabilities.yaml')}

    for element_id in elements:
        if not ELEMENT_ID.match(element_id):
            errors.append(f'{element_id}: malformed element ID')

    for risk_id, risk in risks.items():
        if not RISK_ID.match(risk_id):
            errors.append(f'{risk_id}: malformed risk ID')
        for field in ('statement', 'description', 'element_ids', 'failure_mode', 'type', 'controls'):
            if not risk.get(field):
                errors.append(f'{risk_id}: missing or empty field "{field}"')
        element_ids = risk.get('element_ids') or []
        if not isinstance(element_ids, list):
            errors.append(f'{risk_id}: element_ids must be a list')
            element_ids = []
        if len(set(element_ids)) != len(element_ids):
            errors.append(f'{risk_id}: duplicate entries in element_ids')
        for element_id in element_ids:
            if element_id not in elements:
                errors.append(f'{risk_id}: unknown element "{element_id}" in element_ids')
        if risk.get('failure_mode') and risk['failure_mode'] not in FAILURE_MODES:
            errors.append(f'{risk_id}: unknown failure_mode "{risk["failure_mode"]}"')
        for t in risk.get('type') or []:
            if t not in RISK_TYPES:
                errors.append(f'{risk_id}: unknown type "{t}"')
        for ctrl_id in risk.get('controls') or []:
            if ctrl_id not in controls:
                errors.append(f'{risk_id}: references undefined control {ctrl_id}')
        if not risk.get('sources'):
            warnings.append(f'{risk_id}: no sources listed')

    for ctrl_id, ctrl in controls.items():
        if not CTRL_ID.match(ctrl_id):
            errors.append(f'{ctrl_id}: malformed control ID')
        if not ctrl.get('statement'):
            errors.append(f'{ctrl_id}: missing statement')
        if ctrl.get('level') not in (0, 1, 2):
            errors.append(f'{ctrl_id}: level must be 0, 1, or 2 (got {ctrl.get("level")!r})')
        if not ctrl.get('risks'):
            errors.append(f'{ctrl_id}: not mapped to any risk')
        for risk_id in ctrl.get('risks') or []:
            if risk_id not in risks:
                errors.append(f'{ctrl_id}: references undefined risk {risk_id}')
        if not ctrl.get('recommendations'):
            warnings.append(f'{ctrl_id}: no recommendations text')

    forward = {(r, c) for r, risk in risks.items() for c in (risk.get('controls') or [])}
    backward = {(r, c) for c, ctrl in controls.items() for r in (ctrl.get('risks') or [])}
    for r, c in sorted(forward - backward):
        errors.append(f'{r} lists {c}, but {c} does not list {r}')
    for r, c in sorted(backward - forward):
        errors.append(f'{c} lists {r}, but {r} does not list {c}')

    return errors, warnings


def main():
    errors, warnings = validate()
    for w in warnings:
        print(f'  warning: {w}')
    if errors:
        for e in errors:
            print(f'  ERROR: {e}', file=sys.stderr)
        print(f'\n✗ Risk register validation failed with {len(errors)} error(s)', file=sys.stderr)
        sys.exit(1)
    print(f'✓ Risk register valid ({len(warnings)} warning(s))')


if __name__ == '__main__':
    main()
