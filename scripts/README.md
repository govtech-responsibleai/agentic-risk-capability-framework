# Build Scripts

This directory contains scripts for building and processing data for the ARC Framework documentation.

## `validate_risk_register.py`

Checks the register for well-formed IDs, required fields, valid elements, hazards, failure modes and levels, inverse-consistent risk↔control links, and valid crosswalk IDs. Exits non-zero on any error. Run it directly, or let the build script run it first.

## `build_risk_register.py`

Validates the register, then converts the YAML data files into the consolidated JSON used by the interactive risk register and generates the Crosswalks page.

### Usage

```bash
# From the repository root
python scripts/build_risk_register.py
```

Or with the virtual environment:

```bash
source .venv/bin/activate
python scripts/build_risk_register.py
```

### What it does

1. Loads YAML files from `arc-risk-register/`:
   - `risks.yaml` - Risk definitions
   - `controls.yaml` - Control definitions
   - `capabilities.yaml` - Capability taxonomy
   - `components.yaml` - System components
   - `design.yaml` - Design elements
   - `hazards.yaml` - Hazard categories
   - `crosswalk_references.yaml` - External frameworks and their valid IDs

2. Merges and enriches the data by:
   - Linking risks to their elements (components, design, capabilities)
   - Attaching full control details to each risk
   - Computing metadata and statistics

3. Outputs:
   - `docs/assets/risk_register_data.json` - consolidated JSON for the interactive register
   - `docs/arc_framework/crosswalks.md` - generated Crosswalks page (do not edit by hand)

### When to run

Run this script whenever you update any of the source YAML files, and commit the regenerated outputs. CI fails a pull request whose generated files are stale.

### Integration with MkDocs

The generated JSON file is consumed by the interactive risk register page at `docs/arc_framework/risk-register.md`. After running this script, rebuild the docs:

```bash
mkdocs build
```

Or for local development:

```bash
mkdocs serve
```
