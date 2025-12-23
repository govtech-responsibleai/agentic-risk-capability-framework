// Risk Register Interactive Table
// This script initializes the Tabulator table for the risk register

document.addEventListener('DOMContentLoaded', async function() {
    // Only run if the risk-table element exists on this page
    if (!document.getElementById('risk-table')) {
        return;
    }

    // Load data from assets directory
    // Path is relative to arc_framework/risk-register/ page
    const response = await fetch('../../assets/risk_register_data.json');
    const data = await response.json();

    // Populate filter options
    const elementFilter = document.getElementById('element-filter');
    const failureFilter = document.getElementById('failure-filter');

    // Populate element categories
    const categories = [...new Set(data.risks.map(r => r.element_category))].sort();
    categories.forEach(cat => {
        const option = document.createElement('option');
        option.value = cat;
        option.textContent = cat;
        elementFilter.appendChild(option);
    });

    // Populate failure modes
    const failureModes = [...new Set(data.risks.map(r => r.failure_mode))].sort();
    failureModes.forEach(mode => {
        const option = document.createElement('option');
        option.value = mode;
        option.textContent = mode;
        failureFilter.appendChild(option);
    });

    // Function to update stats based on visible rows (will be defined after table initialization)
    let updateStats;

    // Custom formatter for risk types
    function typeFormatter(cell) {
        const types = cell.getValue();
        const badges = types.map(type =>
            `<span class="risk-type-badge risk-type-${type.toLowerCase()}">${type}</span>`
        ).join(' ');
        return `<div style="white-space: nowrap;">${badges}</div>`;
    }

    // Custom formatter for control count
    function controlCountFormatter(cell) {
        const count = cell.getValue();
        return `<span class="control-count-badge" style="background: #6b21a8; box-shadow: 0 2px 4px rgba(107, 33, 168, 0.3);">${count} controls</span>`;
    }

    // Custom formatter for failure mode
    function failureModeFormatter(cell) {
        let mode = cell.getValue();
        // Shorten "Tool or Resource Malfunction" to "Tool Malfunction"
        if (mode === "Tool or Resource Malfunction") {
            mode = "Tool Malfunction";
        }
        // Shorten "External Manipulation" to "Ext. Manipulation"
        if (mode === "External Manipulation") {
            mode = "Ext. Manipulation";
        }
        return `<span class="failure-mode-badge">${mode}</span>`;
    }

    // Row formatter to add expandable details
    function rowFormatter(row) {
        const data = row.getData();

        // Create element to hold expanded content
        const holderEl = document.createElement("div");
        holderEl.style.boxSizing = "border-box";
        holderEl.style.padding = "10px 20px";
        holderEl.style.borderTop = "1px solid #ddd";
        holderEl.style.borderBottom = "1px solid #ddd";
        holderEl.style.background = "#fafafa";
        holderEl.style.display = "none"; // Hidden by default

        // Description
        const descriptionDiv = document.createElement("div");
        descriptionDiv.style.wordWrap = "break-word";
        descriptionDiv.style.overflowWrap = "break-word";
        descriptionDiv.style.whiteSpace = "normal";
        descriptionDiv.style.marginBottom = "15px";
        descriptionDiv.innerHTML = `<strong>Description:</strong> ${data.description}`;
        holderEl.appendChild(descriptionDiv);

        // References (if available)
        if (data.sources && data.sources.length > 0) {
            const referencesDiv = document.createElement("div");
            referencesDiv.style.marginBottom = "15px";
            referencesDiv.style.fontSize = "0.9em";
            referencesDiv.style.color = "#555";
            const refLinks = data.sources.map(src => `<a href="${src}" target="_blank" rel="noopener">${src}</a>`).join('<br>');
            referencesDiv.innerHTML = `<strong>References:</strong><br>${refLinks}`;
            holderEl.appendChild(referencesDiv);
        }

        // Controls
        if (data.controls && data.controls.length > 0) {
            const controlsDiv = document.createElement("div");
            controlsDiv.className = "controls-list";
            controlsDiv.innerHTML = `<strong>Recommended Controls:</strong>`;

            data.controls.forEach((ctrl, index) => {
                const levelClass = `control-level-${ctrl.level}`;
                const levelLabel = ctrl.level === 0 ? 'Cardinal' : ctrl.level === 1 ? 'Standard' : 'Best Practice';

                const controlItem = document.createElement("div");
                controlItem.className = "control-item";
                controlItem.style.cursor = "pointer";
                controlItem.style.position = "relative";

                // Control header (always visible)
                const controlHeader = document.createElement("div");
                controlHeader.className = "control-header";
                controlHeader.style.display = "flex";
                controlHeader.style.alignItems = "center";
                controlHeader.innerHTML = `
                    <span class="control-expand-icon" style="display: inline-block; width: 28px; margin-right: 8px; font-weight: bold; color: #3b82f6; font-size: 2em;">▸</span>
                    <span class="control-level ${levelClass}">${levelLabel}</span>
                    <strong>${ctrl.id}:</strong> &nbsp;${ctrl.statement}
                `;
                controlItem.appendChild(controlHeader);

                // Control details (hidden by default)
                const controlDetails = document.createElement("div");
                controlDetails.className = "control-details";
                controlDetails.style.display = "none";
                controlDetails.style.marginTop = "8px";
                controlDetails.style.paddingLeft = "36px";
                controlDetails.innerHTML = `
                    <div style="font-size: 1em; color: #666; margin-bottom: 8px;">
                        <strong>Recommendations:</strong><br>
                        ${ctrl.recommendations}
                    </div>
                `;

                // Add references if available
                if (ctrl.references && ctrl.references.length > 0) {
                    const ctrlRefDiv = document.createElement("div");
                    ctrlRefDiv.style.fontSize = "0.85em";
                    ctrlRefDiv.style.color = "#555";
                    const ctrlRefLinks = ctrl.references.map(ref => `<a href="${ref}" target="_blank" rel="noopener">${ref}</a>`).join('<br>');
                    ctrlRefDiv.innerHTML = `<strong>References:</strong><br>${ctrlRefLinks}`;
                    controlDetails.appendChild(ctrlRefDiv);
                }

                controlItem.appendChild(controlDetails);

                // Toggle click handler
                controlItem.addEventListener('click', function(e) {
                    e.stopPropagation();
                    const icon = this.querySelector('.control-expand-icon');
                    const details = this.querySelector('.control-details');

                    if (details.style.display === 'none') {
                        details.style.display = 'block';
                        icon.textContent = '▾';
                    } else {
                        details.style.display = 'none';
                        icon.textContent = '▸';
                    }
                });

                controlsDiv.appendChild(controlItem);
            });

            holderEl.appendChild(controlsDiv);
        }

        row.getElement().appendChild(holderEl);

        // Add click handler to toggle row expansion
        let isExpanded = false;
        row.getElement().addEventListener('click', function(e) {
            // Don't toggle if clicking on a link or already inside expanded content
            if (e.target.tagName === 'A' || e.target.closest('.control-item')) {
                return;
            }

            isExpanded = !isExpanded;
            holderEl.style.display = isExpanded ? 'block' : 'none';

            // Update expand icon
            const expandIcon = row.getElement().querySelector('.risk-expand-icon');
            if (expandIcon) {
                expandIcon.textContent = isExpanded ? '▾' : '▸';
            }

            // Add visual indicator
            if (isExpanded) {
                row.getElement().style.backgroundColor = '#f0f7ff';
            } else {
                row.getElement().style.backgroundColor = '';
            }
        });
    }

    // Initialize Tabulator
    const table = new Tabulator("#risk-table", {
        data: data.risks,
        layout: "fitColumns",
        responsiveLayout: "collapse",
        responsiveLayoutCollapseStartOpen: false,
        pagination: true,
        paginationSize: 20,
        paginationSizeSelector: [10, 20, 50, 100],
        movableColumns: true,
        resizableRows: false,
        height: "auto",
        initialSort: [
            {column: "id", dir: "asc"}
        ],
        columns: [
            {
                title: "",
                field: "expand_icon",
                width: 40,
                responsive: 0,
                headerFilter: false,
                vertAlign: "middle",
                hozAlign: "center",
                formatter: function(cell) {
                    return '<span class="risk-expand-icon" style="font-size: 2em; font-weight: bold; color: #3b82f6; cursor: pointer;">▸</span>';
                }
            },
            {
                title: "Risk ID",
                field: "id",
                width: 100,
                responsive: 0,
                headerFilter: false,
                vertAlign: "middle"
            },
            {
                title: "Risk Statement",
                field: "statement",
                minWidth: 300,
                widthGrow: 4,
                responsive: 0,
                headerFilter: false,
                formatter: function(cell) {
                    return `<div style="font-weight: 600; font-size: 1.05em; line-height: 1.4; color: #1f2937;">${cell.getValue()}</div>`;
                },
                vertAlign: "middle"
            },
            {
                title: "Element",
                field: "element_category",
                minWidth: 180,
                widthGrow: 2,
                responsive: 1,
                headerFilter: false,
                vertAlign: "middle"
            },
            {
                title: "Failure Mode",
                field: "failure_mode",
                minWidth: 140,
                widthGrow: 1.5,
                formatter: failureModeFormatter,
                responsive: 2,
                headerFilter: false,
                vertAlign: "middle"
            },
            {
                title: "Type",
                field: "type",
                minWidth: 160,
                width: 160,
                formatter: typeFormatter,
                responsive: 3,
                headerFilter: false,
                vertAlign: "middle"
            },
            {
                title: "Controls",
                field: "control_count",
                width: 100,
                formatter: controlCountFormatter,
                hozAlign: "center",
                responsive: 4,
                headerFilter: false,
                vertAlign: "middle"
            }
        ],
        rowFormatter: rowFormatter
    });

    // Function to update stats based on visible rows
    updateStats = function() {
        const statsDiv = document.getElementById('stats-summary');
        const visibleData = table.getData("active"); // Get filtered data
        
        // Count unique elements and unique controls from visible risks
        const uniqueElements = [...new Set(visibleData.map(r => r.element_category))].length;
        
        // Count unique control IDs (not sum of control_count, since controls can be shared)
        const allControlIds = new Set();
        visibleData.forEach(risk => {
            if (risk.controls && Array.isArray(risk.controls)) {
                risk.controls.forEach(ctrl => {
                    if (ctrl.id) {
                        allControlIds.add(ctrl.id);
                    }
                });
            }
        });
        const uniqueControls = allControlIds.size;
        
        statsDiv.innerHTML = `
            <div class="stat-card">
                <h4>${uniqueElements}</h4>
                <p>System Elements</p>
            </div>
            <div class="stat-card">
                <h4>${visibleData.length}</h4>
                <p>Total Risks</p>
            </div>
            <div class="stat-card">
                <h4>${uniqueControls}</h4>
                <p>Total Controls</p>
            </div>
        `;
    };

    // Initial stats display - wait for table to fully initialize
    setTimeout(updateStats, 100);

    // Filter functions
    function applyFilters() {
        const elementCategory = document.getElementById('element-filter').value;
        const failureMode = document.getElementById('failure-filter').value;
        const riskType = document.getElementById('type-filter').value;
        const searchTerm = document.getElementById('search-filter').value.toLowerCase().trim();

        // Use a single custom filter function for all filters
        table.setFilter(function(data) {
            // Element category filter
            if (elementCategory && data.element_category !== elementCategory) {
                return false;
            }
            
            // Failure mode filter
            if (failureMode && data.failure_mode !== failureMode) {
                return false;
            }
            
            // Risk type filter
            if (riskType && (!data.type || !data.type.includes(riskType))) {
                return false;
            }
            
            // Search filter
            if (searchTerm) {
                const statement = (data.statement || '').toLowerCase();
                const description = (data.description || '').toLowerCase();
                const id = (data.id || '').toLowerCase();
                if (!statement.includes(searchTerm) && 
                    !description.includes(searchTerm) && 
                    !id.includes(searchTerm)) {
                    return false;
                }
            }
            
            return true;
        });
        
        // Update stats after filter is applied
        setTimeout(updateStats, 50);
    }

    // Add filter event listeners
    document.getElementById('element-filter').addEventListener('change', applyFilters);
    document.getElementById('failure-filter').addEventListener('change', applyFilters);
    document.getElementById('type-filter').addEventListener('change', applyFilters);
    document.getElementById('search-filter').addEventListener('input', applyFilters);

    // Clear filters
    document.getElementById('clear-filters').addEventListener('click', function() {
        document.getElementById('element-filter').value = '';
        document.getElementById('failure-filter').value = '';
        document.getElementById('type-filter').value = '';
        document.getElementById('search-filter').value = '';
        table.clearFilter();
        setTimeout(updateStats, 50);
    });
});
