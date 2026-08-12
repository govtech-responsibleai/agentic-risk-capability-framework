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

def load_yaml(filename):
    """Load a YAML file and return the data."""
    with open(DATA_DIR / filename, 'r') as f:
        return yaml.safe_load(f)

def build_risk_register_data():
    """Build the complete risk register data structure."""

    # Load all data sources
    risks = load_yaml('risks.yaml')
    controls = load_yaml('controls.yaml')
    capabilities = load_yaml('capabilities.yaml')
    components = load_yaml('components.yaml')
    design = load_yaml('design.yaml')

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
        element_id = risk_data.get('element_id', '')

        # Try to find element with exact match first, then try normalized versions
        element_info = elements.get(element_id, {})
        if not element_info and element_id:
            # Try zero-padded version (CMP-1 -> CMP-01)
            if '-' in element_id:
                prefix, number = element_id.split('-')
                # Also handle DES -> DSN mapping
                if prefix == 'DES':
                    prefix = 'DSN'
                normalized_id = f"{prefix}-{number.zfill(2)}"
                element_info = elements.get(normalized_id, {})

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
                    'references': ctrl.get('references', []) if ctrl.get('references') else []
                })

        enriched_risk = {
            'id': risk_id,
            'statement': risk_data.get('statement', ''),
            'description': risk_data.get('description', ''),
            'element_id': element_id,
            'element_name': element_info.get('name', ''),
            'element_category': element_info.get('category', ''),
            'failure_mode': risk_data.get('failure_mode', ''),
            'type': risk_data.get('type', []),
            'controls': control_details,
            'control_count': len(control_details),
            'sources': risk_data.get('sources', [])
        }

        enriched_risks.append(enriched_risk)

    # Build output data structure
    output = {
        'risks': enriched_risks,
        'elements': list(elements.values()),
        'metadata': {
            'total_risks': len(risks),
            'total_controls': len(controls),
            'total_elements': len(elements),
            'categories': sorted(set(e['category'] for e in elements.values())),
            'failure_modes': sorted(set(r.get('failure_mode', '') for r in risks.values())),
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

    print(f"✓ Generated {OUTPUT_FILE}")
    print(f"  - {data['metadata']['total_risks']} risks")
    print(f"  - {data['metadata']['total_controls']} controls")
    print(f"  - {data['metadata']['total_elements']} elements")

if __name__ == '__main__':
    main()
