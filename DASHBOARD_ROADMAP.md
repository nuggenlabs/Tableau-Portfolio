# Tableau Public Dashboard Roadmap
## Calvin Nguyen — CN Portfolio Series

This file is the source document for the Tableau Public content series.
Each dashboard post follows the same format: use case, design decisions, and a Tableau feature highlight.

---

## Post Format Template

Every published dashboard and its accompanying LinkedIn post follows this structure:

**Use Case** — What business problem does this solve? Who is the audience? What decision does it support?

**Design Decisions** — 2-3 specific choices: chart type selection, color logic, layout hierarchy, filter design. Always explain the *why*, not just the *what*.

**Feature Highlight** — One Tableau feature (new or underused) that was central to solving a specific problem in this build.

---

## Published Dashboards

| # | Title | Tableau Public | LinkedIn Post | Status |
|---|-------|---------------|---------------|--------|
| 1 | Executive Delivery Analytics | [link] | [link] | Published |
| 7 | SaaS RevOps Command Center | — | — | In Progress — data + docs complete, Tableau build not started |

---

## Dashboard Backlog

### 2 — Salesforce CRM Analytics (Housing / Real Estate)
**Use case:** Full resident lifecycle tracking — lead pipeline, waitlist management, application processing, lease conversion, and occupancy. Built on Salesforce data via SOQL integration.

**Design angle:** How to design a multi-stage funnel across 5+ distinct pipeline objects without losing the user. Duration dashboards (avg days per stage) as an operational tool, not just a reporting layer.

**Feature highlight:** Salesforce SOQL connector in Tableau — how to navigate objects, relationships, and lookup fields to build a reliable data model.

**Viz types to demonstrate:** Stage duration bar charts, CRM pipeline funnel, geospatial lease revenue, operational status board (color-coded workflow states), custom CRM calendar extension.

---

### 3 — Insurance Broker Book of Business
**Use case:** Enterprise-scale book of business analytics for a benefits broker — tracking pipeline, retention, market competitiveness, and rate changes across producers, broker firms, and stop-loss carriers.

**Design angle:** How to build executive-to-policy-level drill-through so the same workbook serves a C-suite reader and an account manager without switching tools.

**Feature highlight:** Table calculations for YoY retention waterfall — how to compare cohort renewal rates across baseline years without prepping the data upstream.

**Viz types to demonstrate:** Retention waterfall, quote-to-bind funnel, dual-view pipeline (open vs closed), policy-level detail with conditional formatting.

---

### 4 — Retail Field Execution — Interactive Parameter Dashboard
**Use case:** Field rep visit tracking across national retail stores (Best Buy, Lowe's, Walmart, Home Depot, Target) — training outcomes, visit frequency, and geographic coverage.

**Design angle:** Interactive parameter dashboards where the user selects the question and the entire viz updates. Question hierarchy drill-down as a UX pattern for survey/field data.

**Feature highlight:** Parameter actions + dynamic zone visibility — how to build a single dashboard that behaves like multiple dashboards depending on the user's selection.

**Viz types to demonstrate:** Interactive parameter viz, question hierarchy treemap, geospatial visit map, training outcome tracking.

---

### 5 — Workforce Analytics — Labor Efficiency Suite
**Use case:** Multi-region workforce tracking — scheduled hours vs actuals, labor budget efficiency, staffing gap analysis, and 3-week forward scheduling compliance.

**Design angle:** Operational dashboards designed for daily use by field managers, not executives. Red/green grid logic for instant pass/fail reads without needing to interpret numbers.

**Feature highlight:** Reference lines and bands for budget thresholds — how to build dynamic color alerts that update based on a calculated target rather than a hardcoded value.

**Viz types to demonstrate:** Red/green compliance grid, geospatial staffing map, forward-looking schedule view (NW / 2W / 3W), labor budget efficiency scorecard.

---

### 6 — Store Issue Tracker with Photo Integration
**Use case:** Field display issue tracking at retail store locations — logging headphone, fixture, and graphics issues with before/after photo documentation tied to the data row.

**Design angle:** When and how to integrate photos into a Tableau dashboard without making it feel like a file viewer. The photo panel is secondary to the data; it validates and explains, not leads.

**Feature highlight:** URL actions for image display — how to surface external photos stored in a cloud location (S3, SharePoint, etc.) directly inside a Tableau sheet using URL actions and web objects.

**Viz types to demonstrate:** Issue tracker with photo integration, store-level detail table, issue category breakdown, fix rate tracking.

---

### 7 — SaaS Revenue Operations — Pipeline and Forecast Command Center
**Use case:** GTM leadership visibility into pipeline health, forecast accuracy, and revenue performance for a SaaS business. Audience: CRO, VP Sales, VP Account Management, RevOps leadership. Replaces weekly manual slide decks with a governed, self-refreshing reporting layer that answers three questions: Is the pipeline healthy? Is forecast tracking to plan? Where are we losing revenue?

**Design angle:** Three-tab architecture separating pipeline health (leading indicators), forecast accuracy (trailing performance), and revenue waterfall (ARR composition). Each tab is executive-first: one dominant number, supporting context, and one click to the rep or deal level. Operational detail lives in tooltips and a drill-through sheet rather than on the summary view.

**Feature highlight:** LOD expressions for pipeline coverage ratios — using FIXED to calculate coverage per quota segment so the ratio holds correctly when users filter by region, segment, or rep without double-counting deals. Secondary: dashboard tooltips on the stage funnel showing average days-in-stage and historical win rate per stage on hover, eliminating the need for a separate operational table.

**Viz types to demonstrate:** CRM pipeline funnel (multi-stage), stage duration bar chart (avg days vs benchmark), ARR waterfall (New + Expansion - Churn - Contraction = Net ARR), forecast vs actual trend (6-quarter rolling), pipeline coverage scorecard by segment, deal aging table with conditional formatting.

---

## Capabilities Checklist

Use this to ensure new dashboards don't repeat the same viz types. Each new build should demonstrate something not yet covered.

### Visualization Types
- [x] KPI cards with health status labels
- [x] Multi-line trend (revenue, margin, utilization)
- [x] Scatter plot (utilization vs gross margin)
- [x] Utilization heatmap (role x seniority level)
- [x] Bubble chart (CSAT vs budget burn, size = revenue)
- [x] Gantt milestone timeline
- [x] Feedback theme bar chart
- [ ] Retention waterfall
- [ ] Funnel chart (quote-to-bind)
- [ ] Geospatial map (staffing, visit coverage)
- [ ] Treemap (question hierarchy, dealer performance)
- [x] CRM pipeline funnel (multi-stage) — Dashboard 7
- [x] Stage duration bar chart — Dashboard 7
- [ ] Red/green compliance grid
- [ ] Photo-integrated reporting (URL actions)
- [ ] Forward-looking schedule view
- [ ] Interactive parameter dashboard

### Tableau Features
- [x] Corner radius (2026.1)
- [x] Viz extensions
- [x] Multi-tab workbook navigation
- [ ] Salesforce SOQL connector
- [ ] Parameter actions + dynamic zone visibility
- [ ] Table calculations (YoY retention)
- [x] Reference lines/bands with dynamic targets — Dashboard 7
- [ ] URL actions for image display
- [x] Level of Detail (LOD) expressions — Dashboard 7
- [x] Set actions — Dashboard 7
- [x] Dashboard tooltips — Dashboard 7

### Industries Covered
- [x] Analytics consulting / professional services
- [ ] Real estate / property management (CRM)
- [ ] Health insurance / employee benefits
- [ ] Automotive F&I
- [ ] Telecom / consumer electronics retail
- [ ] Manufacturing / production operations
- [x] SaaS / Revenue Operations — Dashboard 7

---

## Design Standards

These apply to every dashboard in this series.

**Color logic:** Color carries meaning, never decoration. Red = at risk / below target. Green = healthy / above target. Yellow/orange = monitor. Neutral palette for everything else.

**Audience first:** Define the audience before opening Tableau. Executive views are minimal and fast. Operational views are dense and filterable. Never mix the two in the same sheet.

**Drill-through pattern:** Every suite has a summary view and a detail view. The summary answers "what." The detail answers "why." One click between them.

**Feature callouts:** Every dashboard highlights one Tableau feature in the LinkedIn post. The feature must solve a real problem in that build — not a gratuitous showcase.

**Corner radius:** Applied to all KPI card containers (2026.1 native). Consistent 8–12px radius across all builds for visual consistency.
