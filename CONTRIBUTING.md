# Contributing to the ARC Framework

The ARC risk register is a living document. We welcome new risks, new controls, corrections, better sources, and crosswalks to other frameworks.

## What makes a good entry

- **A risk** must be supported by academic research or a documented industry incident — not an opinion piece. It arises from one or more *elements* (a component, a design element, or one or more capabilities), through one *failure mode*, and results in one or more *hazards*. If it lists several capabilities, it applies only when a system has all of them.
- **A control** must be actionable, composable, and measurable: say what to do, to what, and how one would check it was done. Map it to at least one risk. Level 0 is reserved for controls that must be adopted as-is wherever the risk applies, with no legitimate exception.
- **IDs are never reused.** Take the next free `RISK-###` / `CTRL-####`. To retire or merge an entry, keep it and add `superseded_by`.

## Where things live

| Path | Contents |
| --- | --- |
| `arc-risk-register/risks.yaml`, `controls.yaml` | the register (source of truth for the site and ARCvisor) |
| `arc-risk-register/capabilities.yaml`, `components.yaml`, `design.yaml`, `hazards.yaml` | the elements and hazard categories |
| `arc-risk-register/crosswalk_references.yaml` | external frameworks and their valid IDs |
| `arc-risk-register/register.yaml` | register version and release date |
| `scripts/validate_risk_register.py` | validator (run by the build and by CI) |
| `scripts/build_risk_register.py` | generates `docs/assets/risk_register_data.json` and `docs/arc_framework/crosswalks.md` — **commit the regenerated files** |
| `docs/` | the MkDocs site; `app/` | ARCvisor |

Crosswalk IDs must be quoted strings (`- "2.10"`, not `- 2.10`).

## Workflow

```bash
pip install -r requirements.txt            # site + scripts
python scripts/validate_risk_register.py   # must report 0 errors
python scripts/build_risk_register.py      # regenerates JSON and crosswalks page
mkdocs build --strict                      # site must build with no warnings
pip install -r app/requirements.txt && python app/tests/test_smoke.py   # if you touched the app or the register schema
```

1. Branch from `dev` (the integration branch), not from `main`.
2. Open a pull request against `dev`. CI runs the validator, checks the generated files are fresh, builds the site strictly, and runs the ARCvisor smoke test. Describe *why* the change is right — for a risk, cite the evidence; for a control, say which risk it mitigates and why at that level.
3. Maintainers merge into `dev`; periodically `dev` is released to `main` via a pull request, which deploys the site and is tagged `v<version>`. Bump `register.yaml` and add a changelog entry (`docs/arc_framework/changelog.md`) in the PR that changes register content: MAJOR for model changes, MINOR for entries added/retired/re-tiered/re-mapped, PATCH for wording.

If you would rather describe a proposal than draft it, open an issue.
