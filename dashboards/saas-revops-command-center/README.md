# SaaS RevOps Command Center

## Portfolio Context

A three-tab Tableau portfolio dashboard targeting Senior Revenue Operations Analyst roles at SaaS companies. Built on a synthetic Salesforce-style opportunity export. Demonstrates RevOps-specific analytics across pipeline health, forecast accuracy, and ARR performance.

---

## Business Context

GTM leadership at a SaaS company needs to answer three questions every week without pulling manual reports: Is the pipeline healthy? Is the forecast tracking to plan? Where are we winning and losing revenue?

This dashboard replaces the weekly slide deck with a governed reporting layer. Each tab is designed around a specific decision cycle:

- **Pipeline Health** — leading indicator view for sales managers. Surfaces coverage gaps, stale deals, and funnel drop-off before the quarter closes.
- **Forecast Accuracy** — trailing performance view for CRO and VP Sales. Compares committed forecast to actual bookings across 6 rolling quarters and tracks win rate trends by segment.
- **ARR Performance** — board-level revenue view. Breaks net new ARR into its components (New, Expansion, Churn) and tracks gross and net retention trends.

---

## Target Audience

- CRO / VP Sales
- VP Revenue Operations
- VP Account Management
- Sales Managers and Directors
- Revenue Operations Analysts (the people who build and maintain this kind of reporting)

---

## Key Business Questions

**Tab 1 — Pipeline Health**
- Does each segment have at least 3x pipeline coverage against quota for the current close quarter?
- Which deals have gone dark (no activity in 30+ days)?
- Where are deals stalling in the funnel — which stages take longest vs. benchmark?
- Which reps have the thinnest pipeline coverage?

**Tab 2 — Forecast Accuracy**
- How accurately did our Commit forecast predict actual bookings over the last 6 quarters?
- Is win rate improving or declining by segment?
- How much Best Case pipeline converted to Commit, and how much Commit closed?

**Tab 3 — ARR Performance**
- What is the composition of net new ARR each quarter (New vs. Expansion vs. Churn)?
- Are we growing at a rate where NRR > 100%?
- Is Enterprise or Mid-Market driving more ARR growth? Is SMB churn rate acceptable?

---

## Data Model

Four CSV files. Connect in Tableau using the relationship canvas (not joins or blends).

```
opportunities.csv  ←─── primary table
       │
       ├── stage_history.csv   (on OpportunityID)
       ├── quotas.csv          (on Owner AND CloseQuarter = Quarter)
       └── quotas_by_segment.csv (on Segment AND CloseQuarter = Quarter)
```

| File | Rows | Grain |
|------|------|-------|
| `opportunities.csv` | 500 | One row per opportunity |
| `stage_history.csv` | ~1,675 | One row per stage per opportunity |
| `quotas.csv` | 154 | One row per rep per quarter |
| `quotas_by_segment.csv` | 33 | One row per segment per quarter |

**Outcome mix:** 148 Closed Won · 112 Closed Lost · 240 Open pipeline  
**Date range:** Q1 2024 – Q4 2025 (closed); Q1 – Q3 2026 (open pipeline close dates)  
**14 reps** across West / Central / East regions; 3 segments (SMB / Mid-Market / Enterprise)

Regenerate the same dataset:
```powershell
python .\generate_mock_data.py
```

---

## Tableau Features Demonstrated

| Feature | Where used |
|---------|-----------|
| `FIXED` LOD expression | Pipeline Coverage scorecard — anchors ratio to Segment × Quarter so rep/region filters don't distort it |
| Dashboard tooltips with mini-chart | Stage Funnel — hover shows win rate + avg days-in-stage per stage via a sheet-referenced tooltip |
| Set action (rep drill-through) | Tab 1 — click a rep to show their individual deal list; click away to clear |
| Dynamic reference band | Coverage scorecard — reference line at `[p.Coverage Target]` parameter, not hardcoded |
| Corner radius (2026.1) | All KPI and chart containers, 10px |
| Custom shapes | Tab 1 Pipeline Coverage scorecard uses rounded badge PNGs from `tableau_shapes/pipeline_badges/` |

---

## Build Status

| Asset | Status |
|-------|--------|
| `generate_mock_data.py` | Done |
| `mock_data/*.csv` | Done — 3 files generated |
| `data_dictionary.md` | Done |
| `tableau_build_guide.md` | Done — includes all calculated field formulas |
| `wireframes/` | Done — ASCII wireframes for all 3 tabs |
| `tab1_mockup_v3.html` | Done — recommended Tab 1 design direction |
| `tableau_shapes/` | Done — custom coverage badges and status markers |
| Tableau workbook build | Not started |
| Published to Tableau Public | Not started |
| LinkedIn post | Not started |

---

## Where to Start (Cold Session)

1. Read `data_dictionary.md` — understand every field and the ARRType logic table
2. Open `tableau_build_guide.md` — Part 1 sets up the data model, Part 2 creates parameters, Part 3 lists all calculated fields in dependency order
3. In Tableau Desktop: Connect → Text File → `mock_data/opportunities.csv`, then add the other two tables on the relationship canvas
4. Build calculated fields in this order: utility fields → Tab 1 fields → Tab 2 fields → Tab 3 fields
5. Test `[Pipeline Coverage LOD]` against a Segment × CloseQuarter crosstab before building any sheets — verify it holds when filtering by rep

## Design Standards

- Use the `dark chrome / light content` pattern from `workbook_formatting_guide.md`: dark navy tab navigation, light dashboard canvas, white KPI and chart cards.
- Dashboard canvas: `#EEF1F8`
- Tab/nav chrome: `#0D1B2E`
- Card fill: `#FFFFFF`
- Container border: `#DDE4F2`
- Positive / on track: `#00A87A`
- Negative / at risk: `#D63344`
- Monitor / watch: `#E59300`
- Brand accent: `#6B4FFF`
- KPI value: 26pt semibold `#0F1C36`
- Container radius: 10px for KPI and chart cards
- Tab 1 primary visual: Pipeline Coverage by Segment. Funnel, stage duration, and stalled deals are supporting diagnostics.
- Pipeline Coverage cells should use rounded badge shapes from `tableau_shapes/pipeline_badges/`, with live coverage value and status on the Label shelf.
- No axis titles where the label is self-explanatory
- Tooltip on every mark — no empty tooltips
