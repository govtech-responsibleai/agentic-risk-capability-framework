#!/usr/bin/env python3
"""
Generate the website's views of the ARC risk register from its YAML source.

The YAML in arc-risk-register/ is the register. This module derives two files
for the website and nothing else:

- assets/risk_register_data.json: the data behind the interactive register
  page, shaped for display (each risk carries copies of its controls)
- arc_framework/crosswalks.md: the generated Crosswalks page
- arc_framework/register-full-text.md: every risk and control as plain text, one
  linkable section per entry, for readers and agents that don't run JavaScript
- llms.txt: an index of the site for LLM agents (https://llmstxt.org)
- arc_framework/capability-combinations.md: the page in docs/ of the same name, with its
  `<!-- arc:... -->` markers replaced by tables generated from the register

None of the generated output is committed. MkDocs generates them at build time through
scripts/mkdocs_hooks.py, so the site can never serve a stale copy. Run this
script directly to validate and preview, or with --out DIR to write the files.
"""

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))
import validate_risk_register  # noqa: E402

# Define paths
DATA_DIR = Path(__file__).parent.parent / 'arc-risk-register'
DOCS_DIR = Path(__file__).parent.parent / 'docs'
# Site paths (relative to docs/) of the generated files
JSON_PATH = 'assets/risk_register_data.json'
CROSSWALKS_PATH = 'arc_framework/crosswalks.md'
FULL_TEXT_PATH = 'arc_framework/register-full-text.md'
LLMS_TXT_PATH = 'llms.txt'
COMBINATIONS_PATH = 'arc_framework/capability-combinations.md'
SITE_URL = 'https://govtech-responsibleai.github.io/agentic-risk-capability-framework/'
RAW_URL = 'https://raw.githubusercontent.com/govtech-responsibleai/agentic-risk-capability-framework'


class RegisterInvalid(Exception):
    """The register failed validation, so nothing can be generated from it."""

def load_yaml(filename):
    """Load a YAML file and return the data."""
    with open(DATA_DIR / filename, 'r') as f:
        return yaml.safe_load(f)

def load_combinations():
    """combinations.yaml (roles, rules and implied capabilities), or {} if the register has none."""
    return load_yaml('combinations.yaml') if (DATA_DIR / 'combinations.yaml').exists() else {}


def combination_rules(combinations):
    """{rule_id: rule}, each with `legs`: the roles it names, in order, with their capability marks."""
    roles = combinations.get('roles') or {}
    return {rule_id: {**rule, 'legs': {r: roles[r] for r in rule.get('roles') or []}}
            for rule_id, rule in (combinations.get('rules') or {}).items()}


def live(entries):
    """Entries that have not been retired (`superseded_by`)."""
    return {k: v for k, v in entries.items() if not v.get('superseded_by')}


def _crosswalk_labels(crosswalks, references):
    """Resolve crosswalk IDs to {framework: [{id, title}]} for display."""
    resolved = {}
    for framework, ids in crosswalks.items():
        ref_ids = {str(k): v for k, v in references[framework]['ids'].items()}
        resolved[framework] = [{'id': str(i), 'title': ref_ids.get(str(i), '')} for i in ids]
    return resolved


FRAMEWORK_SHORT = {
    'owasp_asi': 'OWASP ASI',
    'owasp_agentic_threats': 'OWASP threat',
    'csa_addendum': 'CSA Addendum',
    'imda_mgf': 'IMDA MGF',
    'mitre_atlas': 'MITRE ATLAS',
    'fiveeyes_agentic': 'Five Eyes guidance',
}


def build_crosswalks_page(risks, controls, references, register):
    """Render the Crosswalks page (arc_framework/crosswalks.md) from the register."""
    risks, controls = live(risks), live(controls)
    def entries_for(section, framework):
        """external ID -> list of (entry_id, statement)"""
        table = {str(k): [] for k in references[framework]['ids']}
        for entry_id, entry in section.items():
            for ext in (entry.get('crosswalks') or {}).get(framework, []) or []:
                table[str(ext)].append((entry_id, entry['statement']))
        return table

    def cell(items):
        return '<br>'.join(f'**{eid}** {stmt}' for eid, stmt in items) if items else '—'

    lines = [
        '# Crosswalks to other frameworks',
        '',
        '<!-- Generated at build time from arc-risk-register/*.yaml by scripts/build_risk_register.py; there is no source file to edit -->',
        '',
        '!!! abstract "Page Summary"',
        '',
        '    This page maps the ARC risk register to the external frameworks organisations are most likely to be',
        '    using alongside it, so that an assessment done under one can be read in the vocabulary of another.',
        '    Each mapping points to the *nearest corresponding entries*; it is not a claim of equivalence.',
        '',
        'The crosswalks are maintained as a `crosswalks` field on every risk and control in the',
        '[register YAML](https://github.com/govtech-responsibleai/agentic-risk-capability-framework/tree/main/arc-risk-register),',
        'validated against `crosswalk_references.yaml`, and shown on each entry in the',
        '[Interactive Risk Register](risk-register.md). This page is generated from the same data',
        f"(register version {register['version']}, {register['released']}).",
        '',
        '| Framework | Version | Maps to |',
        '| --- | --- | --- |',
    ]
    for fw, ref in references.items():
        lines.append(f"| [{ref['title']}]({ref['url']}) | {ref.get('version', '')} | ARC {' and '.join(ref.get('applies_to', []))} |")
    lines += [
        '',
        '??? question "Why are some cells empty?"',
        '',
        '    ARC covers both safety and security risks. Its content-safety risks (undesirable, unqualified,',
        '    controversial, or copyrighted content) have no counterpart in OWASP\'s security-focused agentic',
        '    taxonomy, and are deliberately left unmapped rather than forced. CSA Addendum control 1.1 (conduct a',
        '    risk assessment) is the assessment process that the ARC methodology itself implements, so no single',
        '    ARC control corresponds to it. MITRE ATLAS catalogues what adversaries do, so risks that involve no',
        '    adversary, such as plain errors, hallucination and overload, are not mapped to it; only the ATLAS',
        '    techniques that an ARC risk maps to are listed. The Five Eyes guidance does not number its practice',
        '    areas, so the IDs shown for it are ARC\'s own: a prefix for the part of the document and the',
        '    practice area\'s position within it.',
        '',
    ]
    # One table per framework and the kind of entry it maps to, in the order the references are listed
    sections = [(fw, section, label) for fw, ref in references.items()
                for kind, section, label in (('risks', risks, 'ARC risks'), ('controls', controls, 'ARC controls'))
                if kind in (ref.get('applies_to') or [])]
    for fw, section, label in sections:
        ref = references[fw]
        short = FRAMEWORK_SHORT.get(fw, fw)
        lines += ['', f"## {ref['title']} → {label}", '', f"| {short} | {label} |", '| --- | --- |']
        table = entries_for(section, fw)
        for ext_id, title in ref['ids'].items():
            lines.append(f"| **{ext_id}** {title} | {cell(table[str(ext_id)])} |")
    # Reverse direction: per ARC entry, one column per framework that maps to that kind of entry
    for kind, section, label in (('risks', risks, 'ARC risk'), ('controls', controls, 'ARC control')):
        frameworks = [fw for fw, ref in references.items() if kind in (ref.get('applies_to') or [])]
        lines += ['', f'## ARC {kind} → external frameworks', '',
                  f'| {label} | ' + ' | '.join(FRAMEWORK_SHORT.get(fw, fw) for fw in frameworks) + ' |',
                  '| --- |' + ' --- |' * len(frameworks)]
        for entry_id, entry in section.items():
            cw = entry.get('crosswalks') or {}
            lines.append(f"| **{entry_id}** {entry['statement']} | "
                         + ' | '.join(', '.join(map(str, cw.get(fw, []))) or '—' for fw in frameworks) + ' |')
    return '\n'.join(lines) + '\n'


def build_risk_register_data():
    """Build the complete risk register data structure."""

    # Load all data sources
    risks = load_yaml('risks.yaml')
    controls = load_yaml('controls.yaml')
    capabilities = load_yaml('capabilities.yaml')
    components = load_yaml('components.yaml')
    design = load_yaml('design.yaml')
    references = load_yaml('crosswalk_references.yaml')
    harms = load_yaml('harms.yaml')
    register = load_yaml('register.yaml')
    rules = combination_rules(load_combinations())
    retired = [{'id': k, 'statement': v.get('statement', ''), 'superseded_by': v['superseded_by']}
               for section in (risks, controls) for k, v in section.items() if v.get('superseded_by')]
    risks, controls = live(risks), live(controls)

    # Create element lookup (components + design + capabilities)
    elements = {}

    # Add components with hierarchical category
    for comp_id, comp_data in components.items():
        comp_name = comp_data.get('name', '')
        elements[comp_id] = {
            'id': comp_id,
            'name': comp_name,
            'category': f'Component - {comp_name}',
            'description': comp_data.get('description', ''),
            'present_when': comp_data.get('present_when', ''),
        }

    # Add design elements with hierarchical category
    for design_id, design_data in design.items():
        design_name = design_data.get('name', '')
        elements[design_id] = {
            'id': design_id,
            'name': design_name,
            'category': f'Design - {design_name}',
            'description': design_data.get('description', ''),
            'present_when': design_data.get('present_when', ''),
        }

    # Add capabilities with hierarchical category
    for cap_id, cap_data in capabilities.items():
        cap_category = cap_data.get('category', 'Capability')
        elements[cap_id] = {
            'id': cap_id,
            'name': cap_data.get('name', ''),
            'category': f'Capability - {cap_category}',
            'description': cap_data.get('description', ''),
            'authority': cap_data.get('authority', []),
            'irreversible': cap_data.get('irreversible', ''),
            'external': cap_data.get('external', ''),
        }

    # Build enriched risk data
    enriched_risks = []

    for risk_id, risk_data in risks.items():
        # A risk arises from one element, or from the combination of several
        risk_elements = [elements[eid] for eid in risk_data.get('element_ids', []) if eid in elements]

        # Get control details
        control_ids = risk_data.get('controls', [])
        control_details = []
        for ctrl_id in control_ids:
            if ctrl_id in controls:
                ctrl = controls[ctrl_id]
                control_details.append({
                    'id': ctrl_id,
                    'level': ctrl.get('level', ''),
                    'level_when': ctrl.get('level_when', []),
                    'statement': ctrl.get('statement', ''),
                    'recommendations': ctrl.get('recommendations', ''),
                    'enforcement': ctrl.get('enforcement', []),
                    'owner': ctrl.get('owner', ''),
                    'phase': ctrl.get('phase', []),
                    'evidence': ctrl.get('evidence', ''),
                    'test': ctrl.get('test', ''),
                    'references': ctrl.get('references', []) if ctrl.get('references') else [],
                    'crosswalks': _crosswalk_labels(ctrl.get('crosswalks') or {}, references),
                })

        rule = rules.get(risk_data.get('combination'))
        enriched_risk = {
            'id': risk_id,
            'statement': risk_data.get('statement', ''),
            'description': risk_data.get('description', ''),
            'element_ids': [e['id'] for e in risk_elements],
            'element_names': [rule['name']] if rule else [e['name'] for e in risk_elements],
            'element_categories': ['Combination'] if rule else [e['category'] for e in risk_elements],
            'composite': bool(rule) or len(risk_elements) > 1,
            'combination': risk_data.get('combination', ''),
            'min_authority': risk_data.get('min_authority', {}),
            'failure_cause': risk_data.get('failure_cause', ''),
            'type': risk_data.get('type', []),
            'harms': [{'id': h, 'name': harms[h]['name'], 'type': harms[h]['type']}
                        for h in risk_data.get('harms', []) if h in harms],
            'controls': control_details,
            'control_count': len(control_details),
            'sources': risk_data.get('sources', []),
            'crosswalks': _crosswalk_labels(risk_data.get('crosswalks') or {}, references),
        }

        enriched_risks.append(enriched_risk)

    # Build output data structure
    output = {
        'risks': enriched_risks,
        'elements': list(elements.values()),
        'combinations': rules,
        'implies': load_combinations().get('implies', {}),
        'retired': retired,
        'crosswalk_references': {
            fw: {'title': ref['title'], 'url': ref['url'], 'version': ref.get('version', '')}
            for fw, ref in references.items()
        },
        'metadata': {
            'version': str(register['version']),
            'released': str(register['released']),
            'total_risks': len(risks),
            'total_controls': len(controls),
            'total_elements': len(elements),
            'categories': sorted(set(e['category'] for e in elements.values()) | ({'Combination'} if rules else set())),
            'failure_causes': sorted(set(r.get('failure_cause', '') for r in risks.values())),
            'harms': [{'id': h, 'name': d['name'], 'type': d['type']} for h, d in harms.items()],
            'risk_types': ['Safety', 'Security']
        }
    }

    return output

LEVEL_LABELS = {0: 'Level 0 · Cardinal', 1: 'Level 1 · Standard', 2: 'Level 2 · Best Practice'}
AUTHORITY_LABELS = {'read': 'read', 'propose': 'propose', 'act-with-approval': 'act with approval',
                    'act-alone': 'act alone'}


def describe_level_condition(condition):
    """'Level 0 when a capability is used to act alone, with effects that are irreversible and external'."""
    who = ' or '.join(condition['capabilities']) if condition.get('capabilities') else 'a capability'
    parts = []
    if condition.get('authority') == 'act-alone':
        parts.append('is used to act alone')
    elif condition.get('authority'):
        parts.append(f"is used at {AUTHORITY_LABELS[condition['authority']]} or above")
    effects = [word for field, word in (('irreversible', 'irreversible'), ('external', 'external'))
               if condition.get(field) is True]
    effects += [word for field, word in (('irreversible', 'reversible'), ('external', 'internal'))
                if condition.get(field) is False]
    if effects:
        parts.append('has effects that are ' + ' and '.join(effects))
    return f"{LEVEL_LABELS[condition['level']]} when {who} " + ' and '.join(parts)


def _crosswalk_line(crosswalks, references):
    parts = [f"{FRAMEWORK_SHORT.get(fw, fw)} {', '.join(map(str, ids))}"
             for fw, ids in (crosswalks or {}).items() if ids and fw in references]
    return '; '.join(parts)


def build_full_text_page(risks, controls, capabilities, components, design, harms, references, register):
    """Render the full-text register (arc_framework/register-full-text.md): one linkable section per entry."""
    rules = combination_rules(load_combinations())
    retired_risks = {k: v for k, v in risks.items() if v.get('superseded_by')}
    retired_controls = {k: v for k, v in controls.items() if v.get('superseded_by')}
    risks, controls = live(risks), live(controls)
    elements = {}
    for eid, e in components.items():
        elements[eid] = ('Component', e)
    for eid, e in design.items():
        elements[eid] = ('Design', e)
    for eid, e in capabilities.items():
        elements[eid] = (f"Capability ({e.get('category', '')})", e)

    def element_label(eid):
        kind, e = elements[eid]
        return f"{kind.split(' (')[0]}: {e['name']} ({eid})"

    lines = [
        '---',
        'hide:',
        '  - toc',
        '---',
        '',
        '# Risk Register (full text)',
        '',
        '<!-- Generated at build time from arc-risk-register/*.yaml by scripts/build_risk_register.py; there is no source file to edit -->',
        '',
        '!!! abstract "Page Summary"',
        '',
        f"    Every risk and control in ARC risk register **v{register['version']}** (released {register['released']}), "
        'as plain text generated from the register\'s YAML. Each entry has its own link: append its ID, '
        'e.g. [`#RISK-034`](#RISK-034) or [`#CTRL-0062`](#CTRL-0062). The [Interactive Risk Register](risk-register.md) '
        'has the same content with filters; the machine-readable source is the '
        f"[register YAML](https://github.com/govtech-responsibleai/agentic-risk-capability-framework/tree/v{register['version']}/arc-risk-register).",
        '',
        f"**Contents:** [Risks](#risks) ({len(risks)}, grouped by the element they arise from) · [Controls](#controls) ({len(controls)})",
        '',
        '## Risks { #risks }',
        '',
        'Each risk arises from one or more [elements](elements.md) with one failure cause, and results in one or more '
        'harms. A risk that lists several elements arises from their combination and applies only when all of them are present.',
    ]

    groups = {}
    for rid, r in risks.items():
        ids = r.get('element_ids') or []
        key = ids[0] if len(ids) == 1 else 'combination'
        groups.setdefault(key, []).append(rid)
    order = [eid for eid in elements if eid in groups] + (['combination'] if 'combination' in groups else [])

    for key in order:
        if key == 'combination':
            lines += ['', '### Combinations of elements', '',
                      'A risk in this group arises from several elements together, or from a '
                      '[combination rule](capability-combinations.md), which applies whenever the capabilities a '
                      'system has can between them fill every role the rule names.']
        else:
            lines += ['', f"### {element_label(key)}", '', f"*{elements[key][1].get('description', '').strip()}*"]
            if elements[key][1].get('authority'):
                e = elements[key][1]
                lines += ['', '**Authority levels:** ' + ', '.join(AUTHORITY_LABELS[a] for a in e['authority'])
                          + f". **Irreversible effects:** {e['irreversible']}. **Effects outside the organisation:** {e['external']}."]
            if elements[key][1].get('present_when'):
                lines += ['', f"**Present when:** {elements[key][1]['present_when']} These risks apply only to systems that have this element."]
        for rid in groups[key]:
            r = risks[rid]
            hz = ', '.join(f"{harms[h]['name']} ({h})" for h in r.get('harms', []) if h in harms)
            lines += [
                '',
                f"#### {rid} · {r['statement']} {{ #{rid} }}",
                '',
                ("**Arises from:** the combination rule \"" + rules[r['combination']]['name']
                 + "\" (roles: " + ', '.join(leg['name'].lower() for leg in rules[r['combination']]['legs'].values()) + ")  "
                 if r.get('combination') in rules else
                 f"**Arises from:** {' + '.join(element_label(e) for e in r.get('element_ids', []))}  "),
                f"**Failure cause:** {r.get('failure_cause', '')} · **Type:** {', '.join(r.get('type', []))} · **Harms:** {hz}",
            ]
            for cap_id, minimum in (r.get('min_authority') or {}).items():
                lines += ['', f"**Applies when:** {elements[cap_id][1]['name']} ({cap_id}) is used at "
                              f"{AUTHORITY_LABELS[minimum]} or above."]
            lines += [
                '',
                r.get('description', '').strip(),
                '',
                '**Controls:**',
                '',
            ]
            for cid in r.get('controls', []):
                c = controls[cid]
                stricter = ''.join(f'; {describe_level_condition(w)}' for w in c.get('level_when') or [])
                lines.append(f"- [{cid}](#{cid}) ({LEVEL_LABELS.get(c['level'], c['level'])}{stricter}): {c['statement']}")
            if r.get('sources'):
                lines += ['', '**Sources:** ' + ' · '.join(f'<{u}>' if str(u).startswith('http') else str(u) for u in r['sources'])]
            cw = _crosswalk_line(r.get('crosswalks'), references)
            if cw:
                lines += ['', f"**Crosswalks:** {cw}"]

    if retired_risks:
        lines += ['', '### Retired risks', '', 'These IDs are kept so that older assessments and citations still resolve.']
        for rid, r in retired_risks.items():
            lines += ['', f"#### {rid} · {r['statement']} {{ #{rid} }}", '',
                      f"Retired. Superseded by [{r['superseded_by']}](#{r['superseded_by']})."]

    lines += ['', '## Controls { #controls }', '',
              'Level 0 controls are cardinal, Level 1 standard and Level 2 best practice; '
              '[Controls → Control levels](controls.md#control-levels) defines when each applies.']
    for cid, c in controls.items():
        lines += [
            '',
            f"### {cid} · {c['statement']} {{ #{cid} }}",
            '',
            f"**{LEVEL_LABELS.get(c['level'], c['level'])}** · **Mitigates:** "
            + ', '.join(f'[{rid}](#{rid})' for rid in c.get('risks', []))
            + ''.join(f'  \n**{describe_level_condition(w)}.**' for w in c.get('level_when') or []),
            '',
            (c.get('recommendations') or '*No implementation guidance recorded.*').strip(),
        ]
        if c.get('enforcement'):
            lines += ['', f"**Enforced in:** {', '.join(c['enforcement'])} · **Owner:** {c.get('owner', '')} · "
                          f"**Phase:** {', '.join(c.get('phase') or [])}",
                      '', f"**Evidence that it is in place:** {c.get('evidence', '')}",
                      '', f"**Test that it works:** {c.get('test', '')}"]
        if c.get('references'):
            lines += ['', '**References:** ' + ' · '.join(f'<{u}>' if str(u).startswith('http') else str(u) for u in c['references'])]
        cw = _crosswalk_line(c.get('crosswalks'), references)
        if cw:
            lines += ['', f"**Crosswalks:** {cw}"]
    if retired_controls:
        lines += ['', '### Retired controls', '', 'These IDs are kept so that older assessments and citations still resolve.']
        for cid, c in retired_controls.items():
            lines += ['', f"#### {cid} · {c['statement']} {{ #{cid} }}", '',
                      f"Retired. Superseded by [{c['superseded_by']}](#{c['superseded_by']})."]
    return '\n'.join(lines) + '\n'



MARK_LABELS = {'yes': 'Yes', 'maybe': 'Maybe'}


def build_combinations_page(source, risks, controls, capabilities, components, design, combinations):
    """Fill the generated tables into the hand-written Capability combinations page.

    The page's prose lives in docs/; each `<!-- arc:NAME [ARGUMENT] -->` marker on a line of its own is
    replaced by a table built from the register, so the page cannot disagree with the YAML.
    """
    names = {eid: e['name'] for group in (components, design, capabilities) for eid, e in group.items()}

    rules = combination_rules(combinations)

    def composite_risks(_):
        rows = ['| Risk | Applies when |', '| --- | --- |']
        for rid, r in live(risks).items():
            ids = r.get('element_ids') or []
            if r.get('combination') in rules:
                rule = rules[r['combination']]
                rows.append(f"| [{rid}](register-full-text.md#{rid}) {r['statement']} | The rule \"{rule['name']}\" is "
                            'present or possible: the system\'s capabilities can supply '
                            + ', '.join(leg['name'].lower() for leg in rule['legs'].values()) + ' |')
            elif len(ids) > 1:
                rows.append(f"| [{rid}](register-full-text.md#{rid}) {r['statement']} | The system has all of: "
                            + ' + '.join(f'{names[e]} ({e})' for e in ids) + ' |')
        return rows

    def implied(_):
        rows = ['| Capability | Also gives the system | When |', '| --- | --- | --- |']
        for cap_id, others in (combinations.get('implies') or {}).items():
            for other, entry in others.items():
                target = 'Any capability' if other == 'any' else f"{capabilities[other]['name']} ({other})"
                rows.append(f"| {capabilities[cap_id]['name']} ({cap_id}) | {target} | "
                            f"{MARK_LABELS[entry['mark']]}. {entry['note']} |")
        return rows

    def combination(combo_id):
        if combo_id not in rules:
            raise RegisterInvalid(f'{COMBINATIONS_PATH}: unknown combination rule "{combo_id}"')
        return rules[combo_id]

    def legs_table(combo_id):
        legs = combination(combo_id)['legs']
        rows = ['| Capability | ' + ' | '.join(leg['name'] for leg in legs.values()) + ' |',
                '| --- |' + ' :---: |' * len(legs)]
        for cap_id, cap in capabilities.items():
            marks = [MARK_LABELS.get((leg['capabilities'].get(cap_id) or {}).get('mark'), '–') for leg in legs.values()]
            rows.append(f"| {cap['name']} ({cap_id}) | " + ' | '.join(
                f'**{m}**' if m == 'Yes' else m for m in marks) + ' |')
        return rows

    def legs_notes(combo_id):
        rows = []
        for leg in combination(combo_id)['legs'].values():
            rows += [f"**{leg['name']}.** {leg['description']}", '']
            rows += [f"- {capabilities[c]['name']} ({c}): {MARK_LABELS[e['mark']].lower()}"
                     + (f", from {AUTHORITY_LABELS[e['min_authority']]} upwards" if e.get('min_authority') else '')
                     + f". {e['note']}" for c, e in leg['capabilities'].items()]
            rows.append('')
        return rows[:-1]

    def control(combo_id):
        cid = combination(combo_id)['control']
        c = controls[cid]
        return [f"> **[{cid}](register-full-text.md#{cid}) ({LEVEL_LABELS[c['level']]}).** {c['statement']}."]

    blocks = {'composite-risks': composite_risks, 'combination-legs': legs_table,
              'combination-notes': legs_notes, 'combination-control': control, 'implied-capabilities': implied}

    def fill(match):
        indent, name, arg = match.group(1), match.group(2), match.group(3)
        if name not in blocks:
            raise RegisterInvalid(f'{COMBINATIONS_PATH}: unknown marker "arc:{name}"')
        return '\n'.join(indent + line if line else '' for line in blocks[name](arg))

    # A marker may be indented (inside an admonition); the generated lines keep its indent
    return re.sub(r'^( *)<!-- arc:([a-z-]+)(?: ([a-z0-9-]+))? -->$', fill, source, flags=re.M)


def build_llms_txt(register):
    """Render llms.txt (https://llmstxt.org): an index of the site for LLM agents, pinned to the register version."""
    v = register['version']
    site = SITE_URL
    raw = f"{RAW_URL}/v{v}/arc-risk-register"
    return f"""# Agentic Risk & Capability (ARC) Framework

> A technical governance framework from GovTech Singapore for identifying, assessing, and mitigating safety and security risks in agentic AI systems. ARC derives a system's risks from its components, design, and capabilities, and maps each risk to technical controls. Risk register version {v}.

ARC describes an agentic system by three kinds of element: components (LLM, instructions, tools, memory, protocols), design (agentic architecture, roles and access controls, monitoring and traceability), and twelve capabilities, such as code execution, internet and search access, official communication, and business transactions. Each risk in the register arises from one or more elements, has one of six failure causes, results in safety or security harms, and is mapped to controls at Level 0 (cardinal), Level 1 (standard), or Level 2 (best practice).

ARC is meant to be adapted: an organisation contextualises the baseline register to its own setting, and teams then assess individual systems against that version. When citing ARC, give the register version and the entry ID (for example RISK-034 or CTRL-0062).

## Framework

- [Introduction]({site}arc_framework/introduction/): motivation, the capability-based approach, and related work
- [Elements]({site}arc_framework/elements/): definitions of the components, design elements, and twelve capabilities
- [Risks]({site}arc_framework/risks/): failure causes and harms
- [Capability combinations]({site}arc_framework/capability-combinations/): risks that arise only when capabilities are held together, and the check for the lethal trifecta
- [Controls]({site}arc_framework/controls/): what the control levels mean and when they apply
- [Risk Register (full text)]({site}arc_framework/register-full-text/): every risk and control, one linkable section per entry

## Implementation

- [Implementing ARC]({site}implementation/): the two-stage methodology
- [For governance teams]({site}implementation/for-governance-teams/): contextualising ARC for an organisation
- [For AI developers]({site}implementation/for-ai-developers/): assessing a system, with worked examples
- [Assessment template]({site}implementation/assessment-template/)

## Register data

- [risks.yaml]({raw}/risks.yaml) and [controls.yaml]({raw}/controls.yaml): the machine-readable register at v{v}
- [capabilities.yaml]({raw}/capabilities.yaml), [components.yaml]({raw}/components.yaml), [design.yaml]({raw}/design.yaml), [harms.yaml]({raw}/harms.yaml): elements and harm categories
- [combinations.yaml]({raw}/combinations.yaml): which capabilities supply each leg of a checked combination
- [Changelog]({site}arc_framework/changelog/): what changed in each version, and the versioning policy
- [Keeping the register current]({site}arc_framework/keeping-current/): the incident file, the quarterly review, and how changes are proposed

## Optional

- [Crosswalks]({site}arc_framework/crosswalks/): mappings to the OWASP Top 10 for Agentic Applications, OWASP's agentic threat taxonomy, MITRE ATLAS, the CSA Securing Agentic AI Addendum, IMDA's Model AI Governance Framework for Agentic AI, and the Five Eyes guidance on agentic AI
- [Paper](https://arxiv.org/abs/2512.22211): "With Great Capabilities Come Great Responsibilities", IASEAI'26 main track
- [ARCvisor]({site}resources/#arcvisor): an assistant that walks a team through an assessment
- [ARC assessment skill](https://github.com/govtech-responsibleai/agentic-risk-capability-framework/tree/main/skills): an Agent Skill that lets a coding agent assess the system it is building with ARC
"""


def generate():
    """Validate the register and return ({site path: content}, validator warnings).

    Raises RegisterInvalid if the register has validation errors.
    """
    errors, warnings = validate_risk_register.validate()
    if errors:
        raise RegisterInvalid(
            f'{len(errors)} validation error(s) in the risk register:\n'
            + '\n'.join(f'  - {e}' for e in errors))
    data = build_risk_register_data()
    page = build_crosswalks_page(load_yaml('risks.yaml'), load_yaml('controls.yaml'),
                                 load_yaml('crosswalk_references.yaml'), load_yaml('register.yaml'))
    full_text = build_full_text_page(
        load_yaml('risks.yaml'), load_yaml('controls.yaml'), load_yaml('capabilities.yaml'),
        load_yaml('components.yaml'), load_yaml('design.yaml'), load_yaml('harms.yaml'),
        load_yaml('crosswalk_references.yaml'), load_yaml('register.yaml'))
    files = {JSON_PATH: json.dumps(data, indent=2), CROSSWALKS_PATH: page, FULL_TEXT_PATH: full_text,
             LLMS_TXT_PATH: build_llms_txt(load_yaml('register.yaml'))}
    combinations_source = DOCS_DIR / COMBINATIONS_PATH
    if combinations_source.exists():
        files[COMBINATIONS_PATH] = build_combinations_page(
            combinations_source.read_text(), load_yaml('risks.yaml'), load_yaml('controls.yaml'),
            load_yaml('capabilities.yaml'), load_yaml('components.yaml'), load_yaml('design.yaml'),
            load_combinations())
    return files, warnings


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--out', type=Path, help='write the generated files under this directory')
    args = parser.parse_args()

    try:
        files, warnings = generate()
    except RegisterInvalid as e:
        raise SystemExit(f'✗ {e}')
    for w in warnings:
        print(f'  warning: {w}')

    meta = json.loads(files[JSON_PATH])['metadata']
    print(f"✓ Register {meta['version']} is valid and builds: {meta['total_risks']} risks, "
          f"{meta['total_controls']} controls, {meta['total_elements']} elements")
    if args.out:
        for rel, content in files.items():
            target = args.out / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
            print(f'  wrote {target}')


if __name__ == '__main__':
    main()
