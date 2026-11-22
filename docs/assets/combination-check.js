// Interactive capability-combination check for the Capability combinations page.
// Reads the generated register data and applies the same rule as the ARC assessment
// skill (skills/arc-assessment/scripts/arc.py, combination_checks):
//   present      every leg has a selected capability marked "yes"
//   possible     every leg is supplied, at least one only by capabilities marked "maybe"
//   not present  at least one leg is supplied by no selected capability

function checkCombination(combination, selected) {
    const legs = Object.entries(combination.legs).map(([id, leg]) => {
        const suppliers = selected
            .filter((cap) => leg.capabilities[cap])
            .map((cap) => ({ id: cap, mark: leg.capabilities[cap].mark, note: leg.capabilities[cap].note }));
        const status = suppliers.some((s) => s.mark === 'yes') ? 'yes' : suppliers.length ? 'maybe' : 'none';
        return { id, name: leg.name, status, suppliers };
    });
    const verdict = legs.some((l) => l.status === 'none')
        ? 'not present'
        : legs.every((l) => l.status === 'yes') ? 'present' : 'possible';
    return { verdict, legs };
}

if (typeof module !== 'undefined') {
    module.exports = { checkCombination };
}

if (typeof document !== 'undefined') {
    document.addEventListener('DOMContentLoaded', async function () {
        const root = document.getElementById('arc-combination-check');
        if (!root) return;

        let data;
        try {
            const response = await fetch('../../assets/risk_register_data.json');
            data = await response.json();
        } catch (error) {
            root.textContent = 'The check could not load the register data. The table above gives the same information.';
            return;
        }
        const combination = (data.combinations || {})[root.dataset.combination];
        if (!combination) return;
        const capabilities = data.elements.filter((e) => e.id.startsWith('CAP-'));
        const names = Object.fromEntries(capabilities.map((c) => [c.id, c.name]));
        const control = combination.control;

        const el = (tag, attrs = {}, children = []) => {
            const node = document.createElement(tag);
            Object.entries(attrs).forEach(([k, v]) => (k === 'text' ? (node.textContent = v) : node.setAttribute(k, v)));
            [].concat(children).forEach((c) => node.appendChild(c));
            return node;
        };

        const style = el('style', {
            text: `
            #arc-combination-check { border: 1px solid var(--md-default-fg-color--lightest); border-radius: 4px; padding: 0.8rem 1rem; }
            #arc-combination-check fieldset { border: 0; margin: 0 0 0.6rem; padding: 0; }
            #arc-combination-check legend { font-weight: 700; padding: 0; }
            #arc-combination-check .acc-caps { display: grid; grid-template-columns: repeat(auto-fill, minmax(15rem, 1fr)); gap: 0.1rem 1rem; }
            #arc-combination-check label { display: flex; gap: 0.4rem; align-items: baseline; cursor: pointer; }
            #arc-combination-check .acc-verdict { font-weight: 700; margin: 0.6rem 0 0.2rem; }
            #arc-combination-check .acc-result ul { margin-top: 0.2rem; }
            #arc-combination-check .acc-reset { margin-top: 0.4rem; }`,
        });
        root.textContent = '';
        root.appendChild(style);

        const groups = {};
        capabilities.forEach((c) => {
            const category = c.category.replace('Capability - ', '');
            (groups[category] = groups[category] || []).push(c);
        });
        const boxes = [];
        Object.entries(groups).forEach(([category, caps]) => {
            const list = el('div', { class: 'acc-caps' });
            caps.forEach((c) => {
                const box = el('input', { type: 'checkbox', value: c.id });
                boxes.push(box);
                list.appendChild(el('label', {}, [box, el('span', { text: `${c.name} (${c.id})` })]));
            });
            root.appendChild(el('fieldset', {}, [el('legend', { text: `${category} capabilities` }), list]));
        });

        const result = el('div', { class: 'acc-result', 'aria-live': 'polite' });
        const reset = el('button', { type: 'button', class: 'md-button acc-reset', text: 'Clear' });
        root.appendChild(result);
        root.appendChild(reset);

        const statusText = { yes: 'yes', maybe: 'maybe', none: 'not supplied by any ticked capability' };
        const advice = (check) => {
            const named = (status) => check.legs.filter((l) => l.status === status).map((l) => l.name.toLowerCase());
            if (check.verdict === 'present') {
                return `Every leg is present. Implement ${control}. If a review of the system finds that a leg is absent in practice, record which one and the evidence, and waive ${control}.`;
            }
            if (check.verdict === 'possible') {
                return `Whether this system has ${named('maybe').join(' and ')} depends on how it is deployed. Answer each note marked maybe. If every leg is confirmed, implement ${control}. If one is absent, waive ${control} and record the evidence.`;
            }
            return `No ticked capability supplies ${named('none').join(' or ')}. Where ${control} is listed, waive it and record this as the evidence.`;
        };

        const render = () => {
            const selected = boxes.filter((b) => b.checked).map((b) => b.value);
            result.textContent = '';
            if (!selected.length) {
                result.appendChild(el('p', { class: 'acc-verdict', text: 'Tick at least one capability to see the verdict.' }));
                return;
            }
            const check = checkCombination(combination, selected);
            result.appendChild(el('p', { class: 'acc-verdict', text: `${combination.name}: ${check.verdict}` }));
            const list = el('ul');
            check.legs.forEach((leg) => {
                const item = el('li', { text: `${leg.name}: ${statusText[leg.status]}` });
                const shown = leg.suppliers.some((s) => s.mark === 'yes')
                    ? leg.suppliers.filter((s) => s.mark === 'yes')
                    : leg.suppliers;
                if (shown.length) {
                    item.appendChild(el('ul', {}, shown.map((s) => el('li', { text: `${names[s.id]} (${s.id}), ${s.mark}: ${s.note}` }))));
                }
                list.appendChild(item);
            });
            result.appendChild(list);
            result.appendChild(el('p', { text: advice(check) }));
        };

        boxes.forEach((b) => b.addEventListener('change', render));
        reset.addEventListener('click', () => {
            boxes.forEach((b) => (b.checked = false));
            render();
        });
        render();
    });
}
