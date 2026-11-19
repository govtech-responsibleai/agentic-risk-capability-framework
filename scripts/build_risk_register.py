#!/usr/bin/env python3
"""
Build script to convert YAML data to JSON for interactive risk register.
This merges risks, controls, capabilities, components, and design elements.
"""

import yaml
import json
from pathlib import Path

# Define paths
DATA_DIR = Path(__file__).parent.parent / 'arc-risk-register'
DOCS_DIR = Path(__file__).parent.parent / 'docs'
OUTPUT_FILE = DOCS_DIR / 'assets' / 'risk_register_data.json'
CROSSWALKS_PAGE = DOCS_DIR / 'arc_framework' / 'crosswalks.md'

def load_yaml(filename):
    """Load a YAML file and return the data."""
    with open(DATA_DIR / filename, 'r') as f:
        return yaml.safe_load(f)

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
}


def build_crosswalks_page(risks, controls, references):
    """Render docs/arc_framework/crosswalks.md from the register (generated file)."""
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
        '<!-- GENERATED FILE: edit arc-risk-register/*.yaml and run scripts/build_risk_register.py -->',
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
        '[Interactive Risk Register](risk-register.md). This page is generated from the same data.',
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
        '    ARC covers both safety and security hazards. Its content-safety risks (undesirable, unqualified,',
        '    controversial, or copyrighted content) have no counterpart in OWASP\'s security-focused agentic',
        '    taxonomy, and are deliberately left unmapped rather than forced. CSA Addendum control 1.1 (conduct a',
        '    risk assessment) is the assessment process that the ARC methodology itself implements, so no single',
        '    ARC control corresponds to it.',
        '',
    ]
    sections = [
        ('owasp_asi', risks, 'ARC risks'),
        ('owasp_agentic_threats', risks, 'ARC risks'),
        ('csa_addendum', controls, 'ARC controls'),
        ('imda_mgf', controls, 'ARC controls'),
    ]
    for fw, section, label in sections:
        ref = references[fw]
        lines += ['', f"## {ref['title']} → {label}", '', f"| {FRAMEWORK_SHORT[fw]} | {label} |", '| --- | --- |']
        table = entries_for(section, fw)
        for ext_id, title in ref['ids'].items():
            lines.append(f"| **{ext_id}** {title} | {cell(table[str(ext_id)])} |")
    # Reverse direction: per ARC entry
    lines += ['', '## ARC risks → external frameworks', '', '| ARC risk | OWASP ASI | OWASP threats |', '| --- | --- | --- |']
    for rid, r in risks.items():
        cw = r.get('crosswalks') or {}
        lines.append(f"| **{rid}** {r['statement']} | {', '.join(map(str, cw.get('owasp_asi', []))) or '—'} | {', '.join(map(str, cw.get('owasp_agentic_threats', []))) or '—'} |")
    lines += ['', '## ARC controls → external frameworks', '', '| ARC control | CSA Addendum | IMDA MGF | OWASP ASI |', '| --- | --- | --- | --- |']
    for cid, c in controls.items():
        cw = c.get('crosswalks') or {}
        lines.append(f"| **{cid}** {c['statement']} | {', '.join(map(str, cw.get('csa_addendum', []))) or '—'} | {', '.join(map(str, cw.get('imda_mgf', []))) or '—'} | {', '.join(map(str, cw.get('owasp_asi', []))) or '—'} |")
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
    hazards = load_yaml('hazards.yaml')

    # Create element lookup (components + design + capabilities)
    elements = {}

    # Add components with hierarchical category
    for comp_id, comp_data in components.items():
        comp_name = comp_data.get('name', '')
        elements[comp_id] = {
            'id': comp_id,
            'name': comp_name,
            'category': f'Component - {comp_name}',
            'description': comp_data.get('description', '')
        }

    # Add design elements with hierarchical category
    for design_id, design_data in design.items():
        design_name = design_data.get('name', '')
        elements[design_id] = {
            'id': design_id,
            'name': design_name,
            'category': f'Design - {design_name}',
            'description': design_data.get('description', '')
        }

    # Add capabilities with hierarchical category
    for cap_id, cap_data in capabilities.items():
        cap_category = cap_data.get('category', 'Capability')
        elements[cap_id] = {
            'id': cap_id,
            'name': cap_data.get('name', ''),
            'category': f'Capability - {cap_category}',
            'description': cap_data.get('description', '')
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
                    'statement': ctrl.get('statement', ''),
                    'recommendations': ctrl.get('recommendations', ''),
                    'references': ctrl.get('references', []) if ctrl.get('references') else [],
                    'crosswalks': _crosswalk_labels(ctrl.get('crosswalks') or {}, references),
                })

        enriched_risk = {
            'id': risk_id,
            'statement': risk_data.get('statement', ''),
            'description': risk_data.get('description', ''),
            'element_ids': [e['id'] for e in risk_elements],
            'element_names': [e['name'] for e in risk_elements],
            'element_categories': [e['category'] for e in risk_elements],
            'composite': len(risk_elements) > 1,
            'failure_mode': risk_data.get('failure_mode', ''),
            'type': risk_data.get('type', []),
            'hazards': [{'id': h, 'name': hazards[h]['name'], 'type': hazards[h]['type']}
                        for h in risk_data.get('hazards', []) if h in hazards],
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
        'crosswalk_references': {
            fw: {'title': ref['title'], 'url': ref['url'], 'version': ref.get('version', '')}
            for fw, ref in references.items()
        },
        'metadata': {
            'total_risks': len(risks),
            'total_controls': len(controls),
            'total_elements': len(elements),
            'categories': sorted(set(e['category'] for e in elements.values())),
            'failure_modes': sorted(set(r.get('failure_mode', '') for r in risks.values())),
            'hazards': [{'id': h, 'name': d['name'], 'type': d['type']} for h, d in hazards.items()],
            'risk_types': ['Safety', 'Security']
        }
    }

    return output

def main():
    """Main execution."""
    print("Validating risk register...")
    import validate_risk_register
    errors, warnings = validate_risk_register.validate()
    for w in warnings:
        print(f'  warning: {w}')
    if errors:
        for e in errors:
            print(f'  ERROR: {e}')
        raise SystemExit(f'✗ Refusing to build: {len(errors)} validation error(s) in the risk register')

    print("Building risk register data...")

    # Ensure output directory exists
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Build data
    data = build_risk_register_data()

    # Write JSON
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(data, f, indent=2)

    # Write generated crosswalks page
    page = build_crosswalks_page(load_yaml('risks.yaml'), load_yaml('controls.yaml'), load_yaml('crosswalk_references.yaml'))
    with open(CROSSWALKS_PAGE, 'w') as f:
        f.write(page)
    print(f"✓ Generated {CROSSWALKS_PAGE}")

    print(f"✓ Generated {OUTPUT_FILE}")
    print(f"  - {data['metadata']['total_risks']} risks")
    print(f"  - {data['metadata']['total_controls']} controls")
    print(f"  - {data['metadata']['total_elements']} elements")

if __name__ == '__main__':
    main()
