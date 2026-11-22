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
  - a component or design element may carry `present_when`, a sentence saying when a system
    has it; such an element is conditional, and its risks apply only to systems that have it.
    Capabilities are always chosen per system, so they may not carry it
  - failure_mode and type values come from the allowed sets
  - every risk lists at least one hazard from hazards.yaml, and the hazard types
    (Safety/Security) agree exactly with the risk's type
  - every control has a statement, a valid level (0/1/2), and at least one risk
  - risk->control and control->risk mappings are exactly inverse-consistent
  - crosswalks (if present) reference frameworks and IDs defined in
    crosswalk_references.yaml, and only frameworks that apply to that entry type;
    IDs must be quoted strings (an unquoted 2.10 is read by YAML as the number 2.1)
  - register.yaml carries a semantic version (MAJOR.MINOR.PATCH) and a release date
  - combinations.yaml (if present): every combination names a defined control and risks that
    carry it, and has at least two legs; every leg maps defined capabilities to the quoted
    marks "yes" or "maybe", each with a note
  - warnings (non-fatal) for empty sources, missing recommendations, or missing crosswalks
"""

import re
import sys
from pathlib import Path

import yaml

DATA_DIR = Path(__file__).parent.parent / 'arc-risk-register'

FAILURE_MODES = {'Agent Error', 'Agent Misbehaviour', 'External Manipulation', 'Tool or Resource Malfunction',
                 'Safeguard Failure', 'Misuse by the Principal'}
RISK_TYPES = {'Safety', 'Security'}
RISK_ID = re.compile(r'^RISK-\d{3}$')
CTRL_ID = re.compile(r'^CTRL-\d{4}$')
ELEMENT_ID = re.compile(r'^(CMP|DSN|CAP)-\d{2}$')
HAZARD_ID = re.compile(r'^HZ-\d{2}$')
COMBINATION_ID = re.compile(r'^[a-z][a-z0-9-]*$')
MARKS = ('yes', 'maybe')
SEMVER = re.compile(r'^\d+\.\d+\.\d+$')
ISO_DATE = re.compile(r'^\d{4}-\d{2}-\d{2}$')


def load(filename):
    with open(DATA_DIR / filename, 'r') as f:
        return yaml.safe_load(f)


def _check_crosswalks(entry_id, entry, entry_type, references, errors, warnings):
    """Crosswalk IDs must exist in crosswalk_references.yaml for a framework that applies here."""
    crosswalks = entry.get('crosswalks')
    if crosswalks is None:
        warnings.append(f'{entry_id}: no crosswalks')
        return
    if not isinstance(crosswalks, dict):
        errors.append(f'{entry_id}: crosswalks must be a mapping of framework -> list of IDs')
        return
    for framework, ids in crosswalks.items():
        ref = references.get(framework)
        if ref is None:
            errors.append(f'{entry_id}: unknown crosswalk framework "{framework}"')
            continue
        if entry_type not in (ref.get('applies_to') or []):
            errors.append(f'{entry_id}: framework "{framework}" does not apply to {entry_type}')
        if not isinstance(ids, list):
            errors.append(f'{entry_id}: crosswalks.{framework} must be a list')
            continue
        for ext_id in ids:
            if not isinstance(ext_id, str):
                errors.append(f'{entry_id}: {framework} ID {ext_id!r} must be a quoted string')
                continue
            if ext_id not in {str(k) for k in ref['ids']}:
                errors.append(f'{entry_id}: unknown {framework} ID "{ext_id}"')


def _check_combinations(combinations, risks, controls, capabilities, errors):
    """combinations.yaml: legs of capabilities that, held together, call for a control."""
    if not isinstance(combinations, dict):
        errors.append('combinations.yaml: must be a mapping of combination ID -> definition')
        return
    for combo_id, combo in combinations.items():
        where = f'combinations.yaml {combo_id}'
        if not COMBINATION_ID.match(str(combo_id)):
            errors.append(f'{where}: malformed combination ID (use lower-case words joined by hyphens)')
        if not isinstance(combo, dict):
            errors.append(f'{where}: must be a mapping')
            continue
        for field in ('name', 'description', 'control', 'legs'):
            if not combo.get(field):
                errors.append(f'{where}: missing or empty field "{field}"')
        control = combo.get('control')
        if control and control not in controls:
            errors.append(f'{where}: references undefined control {control}')
        for risk_id in combo.get('risks') or []:
            if risk_id not in risks:
                errors.append(f'{where}: references undefined risk {risk_id}')
            elif control and control not in (risks[risk_id].get('controls') or []):
                errors.append(f'{where}: {risk_id} does not list the combination\'s control {control}')
        legs = combo.get('legs') or {}
        if not isinstance(legs, dict) or len(legs) < 2:
            errors.append(f'{where}: legs must be a mapping of at least two legs')
            continue
        for leg_id, leg in legs.items():
            leg_where = f'{where}, leg {leg_id}'
            if not isinstance(leg, dict):
                errors.append(f'{leg_where}: must be a mapping')
                continue
            for field in ('name', 'description', 'question', 'capabilities'):
                if not leg.get(field):
                    errors.append(f'{leg_where}: missing or empty field "{field}"')
            marks = leg.get('capabilities') or {}
            if not isinstance(marks, dict):
                errors.append(f'{leg_where}: capabilities must be a mapping of capability ID -> mark and note')
                continue
            for cap_id, entry in marks.items():
                if cap_id not in capabilities:
                    errors.append(f'{leg_where}: "{cap_id}" is not a defined capability')
                if not isinstance(entry, dict):
                    errors.append(f'{leg_where}: {cap_id} must have a mark and a note')
                    continue
                if entry.get('mark') not in MARKS:
                    errors.append(f'{leg_where}: {cap_id} mark {entry.get("mark")!r} must be the quoted string '
                                  '"yes" or "maybe"')
                if not entry.get('note'):
                    errors.append(f'{leg_where}: {cap_id} has no note')


def validate():
    """Return (errors, warnings) as lists of strings."""
    errors, warnings = [], []

    risks = load('risks.yaml')
    controls = load('controls.yaml')
    elements = {**load('components.yaml'), **load('design.yaml'), **load('capabilities.yaml')}
    references = load('crosswalk_references.yaml')
    hazards = load('hazards.yaml')
    register = load('register.yaml') or {}

    if not SEMVER.match(str(register.get('version', ''))):
        errors.append(f'register.yaml: version must be MAJOR.MINOR.PATCH (got {register.get("version")!r})')
    if not ISO_DATE.match(str(register.get('released', ''))):
        errors.append(f'register.yaml: released must be an ISO date YYYY-MM-DD (got {register.get("released")!r})')

    for element_id, element in elements.items():
        if not ELEMENT_ID.match(element_id):
            errors.append(f'{element_id}: malformed element ID')
        if 'present_when' in element:
            if element_id.startswith('CAP-'):
                errors.append(f'{element_id}: capabilities are chosen per system and may not carry present_when')
            elif not isinstance(element['present_when'], str) or not element['present_when'].strip():
                errors.append(f'{element_id}: present_when must be a sentence saying when a system has this element')
    for hazard_id, hazard in hazards.items():
        if not HAZARD_ID.match(hazard_id):
            errors.append(f'{hazard_id}: malformed hazard ID')
        if hazard.get('type') not in RISK_TYPES:
            errors.append(f'{hazard_id}: hazard type must be one of {sorted(RISK_TYPES)}')

    for risk_id, risk in risks.items():
        if not RISK_ID.match(risk_id):
            errors.append(f'{risk_id}: malformed risk ID')
        for field in ('statement', 'description', 'element_ids', 'failure_mode', 'type', 'hazards', 'controls'):
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
        risk_hazards = risk.get('hazards') or []
        if not isinstance(risk_hazards, list):
            errors.append(f'{risk_id}: hazards must be a list')
            risk_hazards = []
        for hazard_id in risk_hazards:
            if hazard_id not in hazards:
                errors.append(f'{risk_id}: unknown hazard "{hazard_id}"')
        hazard_types = {hazards[h]['type'] for h in risk_hazards if h in hazards}
        if risk_hazards and hazard_types != set(risk.get('type') or []):
            errors.append(f'{risk_id}: type {sorted(risk.get("type") or [])} does not match '
                          f'the types of its hazards {sorted(hazard_types)}')
        for ctrl_id in risk.get('controls') or []:
            if ctrl_id not in controls:
                errors.append(f'{risk_id}: references undefined control {ctrl_id}')
        if not risk.get('sources'):
            warnings.append(f'{risk_id}: no sources listed')
        _check_crosswalks(risk_id, risk, 'risks', references, errors, warnings)

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
        _check_crosswalks(ctrl_id, ctrl, 'controls', references, errors, warnings)

    if (DATA_DIR / 'combinations.yaml').exists():
        _check_combinations(load('combinations.yaml'), risks, controls, load('capabilities.yaml'), errors)

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
