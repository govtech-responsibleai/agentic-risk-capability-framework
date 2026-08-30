# Changelog

!!! abstract "Page Summary"

    What changed in each version of the ARC risk register, and the versioning policy that lets you cite or pin a specific version. The current version is shown at the top of the [Interactive Risk Register](risk-register.md) and carried in the machine-readable JSON (`metadata.version`).

## Versioning policy

The register version lives in `arc-risk-register/register.yaml` and follows `MAJOR.MINOR.PATCH`:

| Change | Bump | Examples |
| --- | --- | --- |
| The model changes — elements, failure modes, hazard categories, or what the control levels mean | **MAJOR** | adding a failure mode; redefining Level 0 |
| Entries are added, retired, merged, re-tiered, or re-mapped | **MINOR** | new risks; a control moved between levels; a control attached to a different risk |
| Wording, references, or crosswalks change without altering meaning | **PATCH** | clarifying a recommendation; adding a source |

Rules that hold across versions:

- **IDs are never reused.** A retired or merged entry keeps its ID and gains a `superseded_by` pointer, so assessments and citations written against an older version remain resolvable.
- Each release to the `main` branch is tagged `v<version>` on GitHub; the YAML and JSON for any version can be retrieved from the tag.
- To cite a specific version: *GovTech Singapore (2026). Agentic Risk & Capability Framework, risk register v1.3.0.* followed by the site URL.

## 1.3.0 — August 2026 { #v1-3-0 }

Consolidation release: no change to the framework's model.

- **Data integrity.** Crosswalk IDs are quoted strings; an unquoted `2.10` had been read as `2.1`, mis-mapping three controls to the wrong CSA Addendum section. The validator now rejects non-string IDs.
- **Mappings corrected.** Twelve controls were attached to the wrong risk or missing from an obvious one (circuit breakers not on cascading errors; least privilege not on overly permissive roles; fraud detection on credential leakage instead of unauthorised transactions; and others). 23 links added, 4 moved.
- **Hazards recorded.** Every risk lists the hazards it results in (`hazards.yaml`, nine categories); a risk's Safety/Security type must agree with its hazards. The register page can be filtered by hazard.
- **Level 0 applicability stated once.** A Level 0 control attaches to every risk whose elements are present, regardless of impact/likelihood score; scoring governs Levels 1 and 2. The developer guide's worked examples were corrected to follow this.
- **Site.** The December-2025 comparison page was retired in favour of the generated Crosswalks; an [Assessment Template](../implementation/assessment-template.md) and a contributing guide were added; the register now carries a version.

## 1.2.0 — August 2026 { #v1-2-0 }

- **Eight new risks** (RISK-047 to RISK-054) from the 2026 evidence base: data exfiltration through untrusted content + sensitive data + an outbound channel (the first *composite* risk), tool/skill supply-chain compromise, sandbox escape, deceptive behaviour toward overseers, unsanctioned inter-agent coordination, automation bias, dependence on third-party agents, insecure runtime defaults.
- **Eight new controls** (CTRL-0089 to CTRL-0096): default-deny egress, deterministic data-flow policy layer, verified provenance for tools and skills, contained evaluations, an independent monitor for deception and collusion, measured oversight quality, third-party agent due diligence, runtime hardening.
- **Nine controls updated** for the 2026 landscape: MCP specification 2026-07-28, agent identity mechanisms, a generalised kill switch (CTRL-0065), approval-fatigue caveats on human-approval controls, continuous safety testing (CTRL-0038).
- Register: 54 risks, 94 controls (39 Level 0).

## 1.1.0 — August 2026 { #v1-1-0 }

- **Mapping realignment.** Risk-to-control mappings had been offset by one position from CTRL-0044 onward in the YAML, the site, and the paper appendix; corrected, and two duplicate controls merged. A validator now runs before every build.
- **Level 0 redefined as strictly unwaivable**, and ten controls that could not meet that bar re-tiered (Level 0 from 45 to 35 of 86).
- **Risks may arise from a combination of elements** (`element_ids` list); a multi-element risk applies only when all its elements are present.
- **Crosswalks** to the OWASP Top 10 for Agentic Applications, OWASP's agentic threat taxonomy, the CSA Securing Agentic AI Addendum (final, 17 June 2026), and IMDA's Model AI Governance Framework for Agentic AI, on every entry and on a generated [Crosswalks](crosswalks.md) page.
- **ARCvisor** reads this register directly instead of a stale private copy; continuous integration validates the register, builds the site, and runs the app's tests on every change.
- Register: 46 risks, 86 controls.

## December 2025 site update

Introduction with design rationale and literature review; unified Elements page; interactive risk register; ARCvisor tool and preprint; the framework paper accepted at IASEAI 2026. Register content unchanged (46 risks, 88 controls).

## 1.0.0 — August 2025 { #v1-0-0 }

Initial public release of the framework and register: three elements (components, design, twelve capabilities), three failure modes, two hazard families, 46 risks and 88 controls at three levels.
