# Incident file

A curated list of things that have gone wrong with agentic AI systems, each mapped to the ARC risk register. It exists to test the register against what actually happens:

- **Which cases does the register not describe?** Those are candidates for new risks and controls.
- **Which risks have no case behind them?** Those rest on argument or research alone, which may be fine but is worth knowing.

It is not an incident database. Others run those, and this file draws on them. What ARC adds is the selection (agentic systems only, from the point of view of whoever built or deployed the system) and the mapping to ARC's elements and risks.

## Files

| File | What it holds |
| --- | --- |
| `incidents.yaml` | The cases |
| `gap-themes.yaml` | The themes a case can be filed under when the register does not fully describe it |
| `sources.yaml` | The upstream trackers the leads come from, with their licences |
| `triage-log.yaml` | Leads that were reviewed and left out, so they are not offered again |

Three scripts work on them:

```bash
python scripts/validate_incidents.py                      # check the files; CI runs this
python scripts/incident_coverage.py                       # compare the cases with the register
python scripts/harvest_incidents.py --cache /tmp/harvest  # list new leads from the upstream trackers
```

The file is kept outside `arc-risk-register/` on purpose. Cases are added far more often than the register changes, and adding a case does not change the register's version.

## What counts as a case

A lead becomes a case only if all of these hold:

1. **An agentic system is involved**: an LLM-based system that acts through tools. It runs code, browses, calls APIs, sends messages, makes transactions, manages files or infrastructure, operates a computer, or delegates to other agents. This includes coding assistants, enterprise copilots with tool access, agentic browsers, agent frameworks, and MCP and other tool servers.
2. **Something went wrong in, or through, a system that someone built, deployed or used.** This includes flaws in agent products and frameworks, whether or not they were exploited.
3. **There is a describable event or finding, with a source.**

Leads are left out, and logged with a reason, when no agent is involved (`not-agentic`), when an attacker used an agent as their own tool against other targets (`offensive-use`), when there is no underlying event (`no-event`), when the breach or flaw does not depend on the system being an agent (`generic-infrastructure`), or when the account cannot be made out (`insufficient-evidence`).

One case is one event. Several reports of the same event are one case, and a batch of similar advisories for one product is one case.

## Fields

```yaml
CASE-0123:
  title: "Coding agent deletes a production database and its backups"
  date: "2026-04"                # when it happened or was disclosed
  kind: harm                     # harm | vulnerability | research
  cause: agent-goal-seeking      # attack | agent-error | agent-goal-seeking | principal-misuse | platform-fault
  evidence: press                # primary | press
  status: triaged                # triaged | verified
  system: "Cursor; Railway"
  summary: "..."                 # our own words: what the agent could do, what went wrong, the consequence
  elements: [CAP-10, DSN-02]     # where the failure arose
  risks: [RISK-041]              # register risks that describe what happened; [] if none does
  gap:                           # only when the register does not describe the case, or only part of it
    theme: reach-beyond-tools
    note: "..."
  sources: ["https://..."]
  external_ids:                  # the same event in upstream trackers
    aiid: "1627"
```

- **kind.** `harm` is real damage to a real party. `vulnerability` is a flaw disclosed in a deployed product with no confirmed damage. `research` is a demonstration, test or evaluation.
- **cause.** How the failure came about. It maps onto the register's failure modes: `attack` is External Manipulation, `agent-error` is Agent Error, `agent-goal-seeking` is Agent Misbehaviour, `principal-misuse` is Misuse by the Principal, and `platform-fault` is Tool or Resource Malfunction.
- **evidence.** `primary` means at least one source is the vendor, the researcher who found it, a lab, a regulator, a court, or a CVE or advisory record. `press` means news coverage only.
- **status.** `triaged` means the case was written from an upstream record and its cited sources. `verified` means a maintainer has opened the primary source and confirmed the summary and the mapping.
- **risks.** A risk is cited only if its description matches the mechanism of what happened. A case with no risk is a finding, not a failure.

## Sources

`sources.yaml` lists each upstream tracker with its licence. Cases carry our own summaries, a link to the original sources, and the upstream ID where there is one. We do not copy upstream text.

One source is deliberately not used yet. The Agent Incident Registry (Enkrypt AI) is the largest agent-specific list, but its data is marked all rights reserved and asks to be contacted before reuse. Its site says an open licence will follow.

## Keeping it current

This is the procedure the file is designed for. Steps 1 and 4 are scripted today; steps 2 and 3 are done by a maintainer, who may have an agent prepare the work.

1. **Harvest, monthly.** Run `scripts/harvest_incidents.py`. It reads the trackers in `sources.yaml` that publish machine-readable data, keeps records that mention an agentic system, drops everything already in `incidents.yaml` or `triage-log.yaml`, and writes the rest out as leads. The sources without a feed (the OWASP quarterly round-ups, the AI Incident Database's own round-ups) are read by hand at the quarterly review.
2. **Triage.** For each lead, decide whether it is a case under the rules above. Write the case, or log the lead in `triage-log.yaml` with a reason. An agent can draft both from the lead text and the register; a maintainer reviews the result as a pull request. New cases start as `triaged`.
3. **Verify.** Open the primary source for every case of kind `harm` and every case with a `gap`, correct the summary and mapping if needed, and set `status: verified`. These are the cases that register changes will rest on.
4. **Review, quarterly.** Run `scripts/incident_coverage.py` and read it against the last one:
   - A gap theme with three or more cases, at least one of them harm, from more than one source, is proposed as a new risk or control, with the cases as its evidence.
   - A risk with no case is checked: is it still credible, and is it worded so that a case could match it?
   - A theme that keeps receiving `other` cases gets a name in `gap-themes.yaml`.
   The proposals go through the register's normal change process and appear in its changelog.

A case can be proposed by anyone through a pull request or an issue that gives a public source.

## Limits

- **Disclosure bias.** The file holds what was published, in English, and found by the trackers it draws on. Security research and coding agents are over-represented, and quiet operational failures inside organisations are under-represented. Counts say what has been reported, not how often things happen.
- **Recency.** The upstream trackers grew quickly in 2026, so later months have more cases for reasons that have nothing to do with risk.
- **Triage is a judgement.** The same event can reasonably be mapped to different risks. The `status` field shows which cases a maintainer has checked.
