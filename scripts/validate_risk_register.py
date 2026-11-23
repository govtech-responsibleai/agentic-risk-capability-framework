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
  - every control says where it is enforced (`enforcement`: one or two of prompt, model, harness,
    infrastructure, organisation), who owns it (`owner`), when in the lifecycle it applies
    (`phase`), what shows it is in place (`evidence`) and how to check that it works (`test`)
  - risk->control and control->risk mappings are exactly inverse-consistent
  - crosswalks (if present) reference frameworks and IDs defined in
    crosswalk_references.yaml, and only frameworks that apply to that entry type;
    IDs must be quoted strings (an unquoted 2.10 is read by YAML as the number 2.1)
  - register.yaml carries a semantic version (MAJOR.MINOR.PATCH) and a release date
  - context: a capability may list the `authority` levels it can be used at (read, propose,
    act-with-approval, act-alone) and say whether its effects are `irreversible` and `external`
    (always, never, or ask); a risk's `min_authority` names one of its own capabilities and a
    level that capability offers; a control's `level_when` lists stricter levels and the
    context in which each applies
  - combinations.yaml (if present): every role maps defined capabilities to the quoted marks
    "yes" or "maybe", each with a note; every rule names at least one defined role, a defined
    control, and risks that carry that control and name the rule in their `combination` field;
    `implies` maps a capability to the capabilities it gives a system
  - a risk arises either from elements (`element_ids`) or from a combination rule (`combination`)
  - a retired entry carries `superseded_by`, naming a live entry of the same kind, and is no longer
    linked to controls or risks
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
RISK_ID = re.compile(r'^(?:[A-Z][A-Z0-9]{1,7}-)?RISK-\d{3}$')     # an overlay's own entries carry a namespace: ORG-RISK-001
CTRL_ID = re.compile(r'^(?:[A-Z][A-Z0-9]{1,7}-)?CTRL-\d{4}$')
ELEMENT_ID = re.compile(r'^(?:[A-Z][A-Z0-9]{1,7}-)?(CMP|DSN|CAP)-\d{2}$')
HAZARD_ID = re.compile(r'^HZ-\d{2}$')
COMBINATION_ID = re.compile(r'^[a-z][a-z0-9-]*$')
AUTHORITY = ('read', 'propose', 'act-with-approval', 'act-alone')   # least to most
CONTEXT_ANSWERS = ('always', 'never', 'ask')
ENFORCEMENT = ('prompt', 'model', 'harness', 'infrastructure', 'organisation')
OWNERS = ('developer', 'platform', 'security', 'governance', 'business')
PHASES = ('design', 'build', 'deploy', 'operate', 'retire')   # in lifecycle order
MARKS = ('yes', 'maybe')
# MAJOR.MINOR.PATCH, with an optional pre-release label for a draft published for review (2.0.0-draft.1)
SEMVER = re.compile(r'^\d+\.\d+\.\d+(-[a-z]+\.\d+)?$')
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


def _check_marks(where, marks, capabilities, errors, allow_any=False):
    if not isinstance(marks, dict) or not marks:
        errors.append(f'{where}: must map capability IDs to a mark and a note')
        return
    for cap_id, entry in marks.items():
        if cap_id not in capabilities and not (allow_any and cap_id == 'any'):
            errors.append(f'{where}: "{cap_id}" is not a defined capability')
        if not isinstance(entry, dict):
            errors.append(f'{where}: {cap_id} must have a mark and a note')
            continue
        if entry.get('mark') not in MARKS:
            errors.append(f'{where}: {cap_id} mark {entry.get("mark")!r} must be the quoted string "yes" or "maybe"')
        if not entry.get('note'):
            errors.append(f'{where}: {cap_id} has no note')
        minimum = entry.get('min_authority')
        if minimum is not None and minimum not in (capabilities.get(cap_id, {}).get('authority') or []):
            errors.append(f'{where}: min_authority {minimum!r} is not an authority level of {cap_id}')


def _check_combinations(combinations, risks, controls, capabilities, errors):
    """combinations.yaml: roles, the rules that combine them, and the capabilities that imply others."""
    if not isinstance(combinations, dict) or not isinstance(combinations.get('rules'), dict):
        errors.append('combinations.yaml: must have `roles` and `rules` mappings')
        return
    roles = combinations.get('roles') or {}
    for role_id, role in roles.items():
        where = f'combinations.yaml role {role_id}'
        if not COMBINATION_ID.match(str(role_id)):
            errors.append(f'{where}: malformed ID (use lower-case words joined by hyphens)')
        if not isinstance(role, dict):
            errors.append(f'{where}: must be a mapping')
            continue
        for field in ('name', 'description', 'question'):
            if not role.get(field):
                errors.append(f'{where}: missing or empty field "{field}"')
        _check_marks(where, role.get('capabilities'), capabilities, errors)
    for rule_id, rule in combinations['rules'].items():
        where = f'combinations.yaml rule {rule_id}'
        if not COMBINATION_ID.match(str(rule_id)):
            errors.append(f'{where}: malformed ID (use lower-case words joined by hyphens)')
        if not isinstance(rule, dict):
            errors.append(f'{where}: must be a mapping')
            continue
        for field in ('name', 'description', 'roles', 'control'):
            if not rule.get(field):
                errors.append(f'{where}: missing or empty field "{field}"')
        for role_id in rule.get('roles') or []:
            if role_id not in roles:
                errors.append(f'{where}: role "{role_id}" is not defined')
        control = rule.get('control')
        if control and (control not in controls or controls[control].get('superseded_by')):
            errors.append(f'{where}: references undefined or retired control {control}')
        for risk_id in rule.get('risks') or []:
            if risk_id not in risks or risks[risk_id].get('superseded_by'):
                errors.append(f'{where}: references undefined or retired risk {risk_id}')
                continue
            if control and control not in (risks[risk_id].get('controls') or []):
                errors.append(f"{where}: {risk_id} does not list the rule's control {control}")
            if risks[risk_id].get('combination') != rule_id:
                errors.append(f'{where}: {risk_id} must name this rule in its `combination` field')
    for cap_id, implied in (combinations.get('implies') or {}).items():
        if cap_id not in capabilities:
            errors.append(f'combinations.yaml implies: "{cap_id}" is not a defined capability')
        _check_marks(f'combinations.yaml implies {cap_id}', implied, capabilities, errors, allow_any=True)


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
        errors.append(f'register.yaml: version must be MAJOR.MINOR.PATCH, optionally with a pre-release label such as -draft.1 (got {register.get("version")!r})')
    if not ISO_DATE.match(str(register.get('released', ''))):
        errors.append(f'register.yaml: released must be an ISO date YYYY-MM-DD (got {register.get("released")!r})')

    for element_id, element in elements.items():
        if not ELEMENT_ID.match(element_id):
            errors.append(f'{element_id}: malformed element ID')
        if 'present_when' in element:
            if 'CAP-' in element_id:
                errors.append(f'{element_id}: capabilities are chosen per system and may not carry present_when')
            elif not isinstance(element['present_when'], str) or not element['present_when'].strip():
                errors.append(f'{element_id}: present_when must be a sentence saying when a system has this element')
        if any(k in element for k in ('authority', 'irreversible', 'external')):
            if 'CAP-' not in element_id:
                errors.append(f'{element_id}: only capabilities carry authority, irreversible and external')
            levels = element.get('authority')
            if not isinstance(levels, list) or not levels or any(a not in AUTHORITY for a in levels) \
                    or levels != sorted(levels, key=AUTHORITY.index):
                errors.append(f'{element_id}: authority must list levels from {list(AUTHORITY)}, least first')
            for field in ('irreversible', 'external'):
                if element.get(field) not in CONTEXT_ANSWERS:
                    errors.append(f'{element_id}: {field} must be one of {list(CONTEXT_ANSWERS)}')
    for hazard_id, hazard in hazards.items():
        if not HAZARD_ID.match(hazard_id):
            errors.append(f'{hazard_id}: malformed hazard ID')
        if hazard.get('type') not in RISK_TYPES:
            errors.append(f'{hazard_id}: hazard type must be one of {sorted(RISK_TYPES)}')

    combinations = load('combinations.yaml') if (DATA_DIR / 'combinations.yaml').exists() else {}
    rules = (combinations or {}).get('rules') or {}

    for risk_id, risk in risks.items():
        if not RISK_ID.match(risk_id):
            errors.append(f'{risk_id}: malformed risk ID')
        if 'superseded_by' in risk:   # retired: kept so that old citations resolve, and nothing else
            target = risks.get(risk['superseded_by'])
            if target is None or target.get('superseded_by'):
                errors.append(f'{risk_id}: superseded_by must name a live risk (got {risk["superseded_by"]!r})')
            if risk.get('controls'):
                errors.append(f'{risk_id}: a retired risk lists no controls')
            if not risk.get('statement'):
                errors.append(f'{risk_id}: missing statement')
            continue
        origin = 'combination' if 'combination' in risk else 'element_ids'
        if 'combination' in risk:
            if risk.get('element_ids'):
                errors.append(f'{risk_id}: arises from a combination rule, so it lists no element_ids')
            if risk['combination'] not in rules:
                errors.append(f'{risk_id}: combination "{risk["combination"]}" is not a rule in combinations.yaml')
            elif risk_id not in (rules[risk['combination']].get('risks') or []):
                errors.append(f'{risk_id}: rule "{risk["combination"]}" does not list this risk')
        for field in ('statement', 'description', origin, 'failure_mode', 'type', 'hazards', 'controls'):
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
        for cap_id, minimum in (risk.get('min_authority') or {}).items():
            if cap_id not in element_ids:
                errors.append(f'{risk_id}: min_authority names {cap_id}, which is not one of its elements')
            elif minimum not in (elements.get(cap_id, {}).get('authority') or []):
                errors.append(f'{risk_id}: min_authority {minimum!r} is not an authority level of {cap_id}')
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
            elif controls[ctrl_id].get('superseded_by'):
                errors.append(f'{risk_id}: lists retired control {ctrl_id}; use {controls[ctrl_id]["superseded_by"]}')
        if not risk.get('sources'):
            warnings.append(f'{risk_id}: no sources listed')
        _check_crosswalks(risk_id, risk, 'risks', references, errors, warnings)

    for ctrl_id, ctrl in controls.items():
        if not CTRL_ID.match(ctrl_id):
            errors.append(f'{ctrl_id}: malformed control ID')
        if 'superseded_by' in ctrl:   # retired
            target = controls.get(ctrl['superseded_by'])
            if target is None or target.get('superseded_by'):
                errors.append(f'{ctrl_id}: superseded_by must name a live control (got {ctrl["superseded_by"]!r})')
            if ctrl.get('risks'):
                errors.append(f'{ctrl_id}: a retired control is linked to no risks')
            if not ctrl.get('statement'):
                errors.append(f'{ctrl_id}: missing statement')
            continue
        if not ctrl.get('statement'):
            errors.append(f'{ctrl_id}: missing statement')
        if ctrl.get('level') not in (0, 1, 2):
            errors.append(f'{ctrl_id}: level must be 0, 1, or 2 (got {ctrl.get("level")!r})')
        for i, condition in enumerate(ctrl.get('level_when') or [], 1):
            where = f'{ctrl_id}: level_when entry {i}'
            if not isinstance(condition, dict) or condition.get('level') not in (0, 1, 2) \
                    or not condition['level'] < (ctrl.get('level') if ctrl.get('level') in (0, 1, 2) else 3):
                errors.append(f'{where} must give a level stricter than the control\'s own')
                continue
            if not any(k in condition for k in ('authority', 'irreversible', 'external')):
                errors.append(f'{where} must state a context: authority, irreversible or external')
            if 'authority' in condition and condition['authority'] not in AUTHORITY:
                errors.append(f'{where}: authority must be one of {list(AUTHORITY)}')
            for field in ('irreversible', 'external'):
                if field in condition and not isinstance(condition[field], bool):
                    errors.append(f'{where}: {field} must be true or false')
            for cap_id in condition.get('capabilities') or []:
                if 'CAP-' not in str(cap_id) or cap_id not in elements:
                    errors.append(f'{where}: "{cap_id}" is not a capability')
        enforcement = ctrl.get('enforcement')
        if not isinstance(enforcement, list) or not 1 <= len(enforcement) <= 2 \
                or any(e not in ENFORCEMENT for e in enforcement) or len(set(enforcement)) != len(enforcement):
            errors.append(f'{ctrl_id}: enforcement must list one or two of {list(ENFORCEMENT)}, the main one first')
        if ctrl.get('owner') not in OWNERS:
            errors.append(f'{ctrl_id}: owner must be one of {list(OWNERS)}')
        phase = ctrl.get('phase')
        if not isinstance(phase, list) or not phase or any(x not in PHASES for x in phase) \
                or phase != sorted(set(phase), key=PHASES.index):
            errors.append(f'{ctrl_id}: phase must list lifecycle phases from {list(PHASES)}, in that order')
        for field in ('evidence', 'test'):
            if not isinstance(ctrl.get(field), str) or not ctrl[field].strip():
                errors.append(f'{ctrl_id}: missing {field}')
        if not ctrl.get('risks'):
            errors.append(f'{ctrl_id}: not mapped to any risk')
        for risk_id in ctrl.get('risks') or []:
            if risk_id not in risks:
                errors.append(f'{ctrl_id}: references undefined risk {risk_id}')
            elif risks[risk_id].get('superseded_by'):
                errors.append(f'{ctrl_id}: lists retired risk {risk_id}; use {risks[risk_id]["superseded_by"]}')
        if not ctrl.get('recommendations'):
            warnings.append(f'{ctrl_id}: no recommendations text')
        _check_crosswalks(ctrl_id, ctrl, 'controls', references, errors, warnings)

    if (DATA_DIR / 'combinations.yaml').exists():
        _check_combinations(combinations, risks, controls, load('capabilities.yaml'), errors)

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
