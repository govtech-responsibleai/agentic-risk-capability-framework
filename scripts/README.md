# Scripts

The YAML in `arc-risk-register/` is the register. These scripts check it and derive the website's views of it. Nothing they generate is committed.

## `validate_risk_register.py`

Checks the register for well-formed IDs, required fields, valid elements, hazards, failure modes and levels, inverse-consistent risk↔control links, and valid crosswalk IDs. Exits non-zero on any error.

```bash
python scripts/validate_risk_register.py
```

## `build_risk_register.py`

Validates the register, then derives four files for the website:

- `assets/risk_register_data.json`: the data behind the [interactive register](../docs/arc_framework/risk-register.md) page, shaped for display (each risk carries copies of its controls, with element names and hazards resolved)
- `arc_framework/crosswalks.md`: the generated Crosswalks page
- `arc_framework/register-full-text.md`: every risk and control as plain text with a link per entry, for readers, search engines, and agents that don't run JavaScript
- `llms.txt`: an index of the site for LLM agents ([llmstxt.org](https://llmstxt.org)), pinned to the register version

You don't normally run it yourself, because the site build does. Running it directly validates the register and prints a summary; `--out DIR` also writes the files under `DIR` for inspection:

```bash
python scripts/build_risk_register.py
python scripts/build_risk_register.py --out /tmp/arc-site-data
```

## `mkdocs_hooks.py`

An [MkDocs hook](https://www.mkdocs.org/user-guide/configuration/#hooks) registered in `mkdocs.yml`. On every `mkdocs build` and every `mkdocs serve` rebuild it calls `build_risk_register.generate()` and adds the files to the site in memory. As a result:

- the site always reflects the YAML it was built from, so there is no stale copy to forget to regenerate;
- an invalid register fails the build, so CI's `mkdocs build --strict` also gates on validation;
- `mkdocs serve` reloads when anything in `arc-risk-register/` or `scripts/` changes (`watch:` in `mkdocs.yml`).

The output paths are in `.gitignore`. If an older checkout left copies in `docs/`, the hook replaces them with freshly generated ones.
