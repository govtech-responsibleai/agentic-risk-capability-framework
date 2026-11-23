#!/usr/bin/env python3
"""
Collect new leads for the ARC incident file from upstream trackers.

ARC does not run an incident database. Others do, and this script reads the ones
that publish machine-readable data, keeps the records that look like they involve
an agentic AI system, drops everything the incident file has already seen, and
writes the rest out as leads for a person (or an agent working for one) to triage.

    python scripts/harvest_incidents.py --cache /tmp/arc-harvest
    python scripts/harvest_incidents.py --cache /tmp/arc-harvest --since 2026-10 --out leads.jsonl

A lead is "seen" when one of its URLs or upstream IDs appears in
incidents/incidents.yaml (it became a case) or in incidents/triage-log.yaml (it was
reviewed and left out). Nothing here writes to those files: triage is a judgement,
recorded by whoever makes it. See incidents/README.md for the procedure.

Upstream sources are listed in incidents/sources.yaml. Only those with a `harvest`
entry are read here; the others are checked by hand each quarter.
"""

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
INCIDENTS_DIR = ROOT / 'incidents'

# Words that suggest an LLM-based system that acts through tools. Precision is not the aim:
# the filter only has to keep the leads short enough to triage.
AGENT_TERMS = re.compile(
    r'\b(ai agents?|agentic|autonomous agents?|coding (agent|assistant)s?|browser agents?|multi-agent|mcp|'
    r'model context protocol|tool[- ]call\w*|function[- ]call\w*|computer[- ]use|agent2agent|a2a|'
    r'copilot( studio)?|claude code|cursor|windsurf|codex|devin|replit agent|gemini cli|amazon q|kiro|cline|'
    r'openclaw|comet|agentforce|autogpt|langchain|langgraph|llamaindex|crewai|autogen|n8n|flowise|dify|'
    r'langflow|operator|agent mode|agent skills?|plugins?)\b', re.I)


def fetch(url, cache, name):
    """Return the text of `url`, downloading it into the cache directory on first use."""
    path = cache / name
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        request = urllib.request.Request(url, headers={'User-Agent': 'arc-incident-harvest'})
        with urllib.request.urlopen(request, timeout=300) as response:
            path.write_bytes(response.read())
    return path.read_text(errors='replace')


def normalise_url(url):
    """Reduce a URL to host and path so that the same page matches across sources."""
    url = re.sub(r'^https?://(www\.)?', '', str(url).strip().lower())
    return re.sub(r'[?#].*$', '', url).rstrip('/')


# ------------------------------------------------------------------ parsers, one per upstream format

def parse_markdown_timeline(source, cache):
    """A dated Markdown timeline: `### YYYY-MM-DD - Title`, then `- **Field:** text` bullets."""
    leads = []
    urls = list(source['harvest']['urls'])
    pattern = source['harvest'].get('archive_links')
    if pattern:  # the front page links to its own archives, e.g. incidents/2026-Q3.md; follow them
        front = fetch(urls[0], cache, f"{source['id']}/{urls[0].rsplit('/', 1)[-1]}")
        base = urls[0].rsplit('/', 1)[0]
        urls += [f'{base}/{link}' for link in dict.fromkeys(re.findall(rf'\]\(({pattern})\)', front))]
    for url in urls:
        text = fetch(url, cache, f"{source['id']}/{url.rsplit('/', 1)[-1]}")
        for block in re.split(r'^### ', text, flags=re.M)[1:]:
            head, _, body = block.partition('\n')
            m = re.match(r'(\d{4}-\d\d(?:-\d\d)?)\s*[-–—]\s*(.+)', head.strip())
            if not m:
                continue
            fields = dict(re.findall(r'^- \*\*([^:*]+):\*\*\s*(.+)$', body, flags=re.M))
            urls = re.findall(r'\]\((https?://[^)\s]+)\)', fields.get('Sources', '')) or \
                re.findall(r'\]\((https?://[^)\s]+)\)', body)
            leads.append({
                'source': source['id'], 'source_id': f"{m.group(1)} {m.group(2)[:60]}", 'date': m.group(1),
                'title': m.group(2).strip(), 'summary': fields.get('Root Cause', '').strip(),
                'detail': fields.get('Impact', '').strip()[:600], 'system': fields.get('Target', '').strip()[:160],
                'urls': urls,
            })
    return leads


def parse_genai_incidents(source, cache):
    """github.com/emmanuelgjr/genai_incidents: one JSON file of records with a stable `id`.

    The dataset aggregates the AI Incident Database, the OECD monitor, AIAAIC, AVID, MITRE ATLAS and
    CVE feeds, so most of it is not about agents. Keep records that mention an agentic system and are
    either not a bare CVE or GHSA entry, or are ones the dataset's curators marked as landmarks.
    """
    data = json.loads(fetch(source['harvest']['urls'][0], cache, f"{source['id']}/incidents.min.json"))
    leads = []
    for r in data['incidents']:
        tags = r.get('tags') or []
        text = ' '.join(str(r.get(k) or '') for k in ('title', 'description', 'affected')) + ' ' + ' '.join(tags)
        if r.get('attack_vector') in ('deepfake', 'misinformation') or not AGENT_TERMS.search(text):
            continue
        bare_advisory = bool(r.get('cve_ids')) or 'ghsa' in tags
        if bare_advisory and r.get('tier') != 'landmark':
            continue
        leads.append({
            'source': source['id'], 'source_id': r['id'], 'date': str(r.get('date') or r.get('year') or ''),
            'title': r.get('title', ''), 'summary': (r.get('description') or '')[:400],
            'system': (r.get('affected') or '')[:160], 'urls': [u for u in [r.get('primary_reference')] if u],
            'cve_ids': r.get('cve_ids') or [],
        })
    return leads


PARSERS = {'markdown-timeline': parse_markdown_timeline, 'genai-incidents-json': parse_genai_incidents}


# ------------------------------------------------------------------ what the incident file has already seen

def seen_keys():
    """URLs and upstream IDs already recorded as a case or as a triaged-out lead."""
    urls, ids = set(), set()
    cases = yaml.safe_load((INCIDENTS_DIR / 'incidents.yaml').read_text()) or {}
    for case in cases.values():
        urls.update(normalise_url(u) for u in case.get('sources') or [])
        for source_id, values in (case.get('external_ids') or {}).items():
            ids.update((source_id, str(v)) for v in (values if isinstance(values, list) else [values]))
    log_path = INCIDENTS_DIR / 'triage-log.yaml'
    for entry in (yaml.safe_load(log_path.read_text()) if log_path.exists() else None) or []:
        if entry.get('url'):
            urls.add(normalise_url(entry['url']))
        if entry.get('source') and entry.get('source_id'):
            ids.add((entry['source'], str(entry['source_id'])))
    return urls, ids


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--cache', type=Path, required=True, help='directory for downloaded upstream files '
                        '(delete it to fetch fresh copies)')
    parser.add_argument('--since', default='2025-01', help='ignore leads dated before this (YYYY-MM; default 2025-01)')
    parser.add_argument('--out', type=Path, help='write the new leads here as JSON Lines (default: print a summary only)')
    parser.add_argument('--all', action='store_true', help='include leads the incident file has already seen')
    args = parser.parse_args()

    sources = yaml.safe_load((INCIDENTS_DIR / 'sources.yaml').read_text())
    seen_urls, seen_ids = (set(), set()) if args.all else seen_keys()
    new, counts = [], {}
    for source_id, source in sources.items():
        harvest = source.get('harvest')
        if not harvest:
            continue
        source = {**source, 'id': source_id}
        leads = [lead for lead in PARSERS[harvest['format']](source, args.cache) if lead['date'] >= args.since]
        fresh = [lead for lead in leads
                 if (lead['source'], str(lead['source_id'])) not in seen_ids
                 and not any(normalise_url(u) in seen_urls for u in lead['urls'])]
        counts[source_id] = (len(leads), len(fresh))
        new += fresh

    new.sort(key=lambda lead: lead['date'])
    for source_id, (total, fresh) in counts.items():
        print(f'{source_id}: {total} agent-related leads since {args.since}, {fresh} not yet triaged')
    if args.out:
        args.out.write_text(''.join(json.dumps(lead, ensure_ascii=False) + '\n' for lead in new))
        print(f'wrote {len(new)} leads to {args.out}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
