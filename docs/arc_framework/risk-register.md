# Interactive Risk Register

Here is our baseline **Risk Register** which we developed for the ARC Framework. It identifies a total of 54 risks arising from the different elements of agentic AI systems that we identified earlier, and recommends 94 controls to mitigate these risks.

!!! note "How to use the Risk Register"

    Click any risk row to expand and view its full description, references, and recommended controls, then click individual control statements for detailed implementation guidance. Use the expand icons (▸/▾) to navigate between views and hover over elements to see visual indicators of interactivity.

<div class="risk-register-container">
    <!-- Stats Summary -->
    <div id="stats-summary" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-bottom: 20px;">
        <!-- Will be populated by JavaScript -->
    </div>
    <!-- Filter Controls -->
    <div class="filters" style="margin-bottom: 20px; padding: 15px; background: #f5f5f5; border-radius: 5px; position: relative;">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
            <div>
                <label for="element-filter" style="font-weight: 600; display: block; margin-bottom: 5px;">Element Category:</label>
                <select id="element-filter" style="width: 100%; padding: 8px; border-radius: 3px; border: 1px solid #ccc; font-size: 0.8em;">
                    <option value="">All Categories</option>
                </select>
            </div>
            <div>
                <label for="failure-filter" style="font-weight: 600; display: block; margin-bottom: 5px;">Failure Mode:</label>
                <select id="failure-filter" style="width: 100%; padding: 8px; border-radius: 3px; border: 1px solid #ccc; font-size: 0.8em;">
                    <option value="">All Failure Modes</option>
                </select>
            </div>
            <div>
                <label for="type-filter" style="font-weight: 600; display: block; margin-bottom: 5px;">Risk Type:</label>
                <select id="type-filter" style="width: 100%; padding: 8px; border-radius: 3px; border: 1px solid #ccc; font-size: 0.8em;">
                    <option value="">All Types</option>
                    <option value="Safety">Safety</option>
                    <option value="Security">Security</option>
                </select>
            </div>
            <div>
                <label for="search-filter" style="font-weight: 600; display: block; margin-bottom: 5px;">Search:</label>
                <input type="text" id="search-filter" placeholder="Search risks..." style="width: 100%; padding: 0px; border-radius: 3px; border: 1px solid #ccc; font-size: 0.8em;">
            </div>
            <div style="display: flex; align-items: flex-end;">
                <button id="clear-filters" style="width: 100%; padding: 0px; height: 36px; background: #666; color: white; border: none; border-radius: 3px; cursor: pointer; font-size: 0.9em;">Clear Filters</button>
            </div>
        </div>
    </div>
    <!-- Risk Table -->
    <div id="risk-table"></div>
</div>

<style>
.risk-register-container {
    margin: 20px 0;
}

.stat-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    border-radius: 8px;
    text-align: center;
}

.stat-card h4 {
    margin: 0 0 5px 0;
    font-size: 2em;
    font-weight: bold;
}

.stat-card p {
    margin: 0;
    opacity: 0.9;
    font-size: 0.9em;
}

.tabulator {
    font-size: 14px;
    border: 1px solid #ddd;
}

.tabulator-row {
    min-height: auto;
    cursor: pointer;
    transition: background-color 0.2s ease;
}

.tabulator-row:hover {
    background-color: #f0f7ff !important;
}

.tabulator-cell {
    white-space: normal !important;
    word-wrap: break-word !important;
    overflow-wrap: break-word !important;
    word-break: break-word !important;
    padding: 8px 6px !important;
    vertical-align: top !important;
}

.tabulator .tabulator-tableHolder .tabulator-table .tabulator-row .tabulator-cell {
    white-space: normal !important;
    overflow: visible !important;
}

.tabulator-row .tabulator-cell {
    line-height: 1.4 !important;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
    .filters {
        padding: 10px !important;
    }

    .filters > div {
        grid-template-columns: 1fr !important;
    }

    .stat-card h4 {
        font-size: 1.5em;
    }

    .tabulator {
        font-size: 12px;
    }

    #stats-summary {
        grid-template-columns: repeat(2, 1fr) !important;
    }
}

.risk-type-badge {
    display: inline-block;
    padding: 3px 8px;
    border-radius: 3px;
    font-size: 0.85em;
    margin: 2px 2px 2px 0;
    font-weight: 600;
    white-space: nowrap;
}

.risk-type-safety {
    background-color: #fef3c7;
    color: #92400e;
}

.risk-type-security {
    background-color: #dbeafe;
    color: #1e40af;
}

.control-count-badge {
    display: inline-block;
    background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
    color: white;
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 0.9em;
    font-weight: 600;
    box-shadow: 0 2px 4px rgba(139, 92, 246, 0.3);
}

.failure-mode-badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 0.85em;
    font-weight: 600;
    background: #e5e7eb;
    color: #374151;
}

.controls-list {
    margin-top: 10px;
    padding: 10px;
    background: #f9fafb;
    border-radius: 4px;
    word-wrap: break-word;
    overflow-wrap: break-word;
}

.control-item {
    padding: 8px;
    margin: 5px 0;
    background: white;
    border-left: 3px solid #3b82f6;
    border-radius: 3px;
    word-wrap: break-word;
    overflow-wrap: break-word;
    transition: all 0.2s ease;
}

.control-item:hover {
    background: #f8fafc;
    border-left-color: #2563eb;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.control-item div {
    word-wrap: break-word;
    overflow-wrap: break-word;
    white-space: normal;
}

.control-header {
    user-select: none;
}

.control-expand-icon {
    transition: transform 0.2s ease;
}

.risk-expand-icon {
    transition: transform 0.2s ease;
    display: inline-block;
}

.control-details {
    animation: slideDown 0.2s ease;
}

@keyframes slideDown {
    from {
        opacity: 0;
        max-height: 0;
    }
    to {
        opacity: 1;
        max-height: 500px;
    }
}

.crosswalk-badge {
    display: inline-block;
    padding: 2px 7px;
    border-radius: 3px;
    font-size: 0.8em;
    font-weight: 600;
    background: #ede9fe;
    color: #5b21b6;
    margin: 2px 3px 2px 0;
    white-space: nowrap;
    cursor: help;
}

.control-level {
    display: inline-block;
    padding: 2px 6px;
    border-radius: 3px;
    font-size: 0.75em;
    font-weight: 600;
    margin-right: 5px;
}

.control-level-0 {
    background: #dc2626;
    color: white;
}

.control-level-1 {
    background: #f59e0b;
    color: white;
}

.control-level-2 {
    background: #10b981;
    color: white;
}
</style>
