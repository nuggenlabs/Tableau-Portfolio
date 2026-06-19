# Tableau Build Guide — SaaS RevOps Command Center

**Dashboard size:** 1400 × 900  
**Tableau version:** 2026.1  
**Data sources:** opportunities.csv · stage_history.csv · quotas.csv  
**Published to:** Tableau Public  

---

## Part 1: Data Model Setup

### Step 1 — Connect to the data sources

1. Open Tableau Desktop. Connect → Text File → `opportunities.csv`
2. On the data source canvas, drag in `stage_history.csv` and `quotas.csv`
3. Tableau will open the relationship editor

### Step 2 — Define relationships

**opportunities → stage_history**  
Relate on: `OpportunityID` = `OpportunityID`  
Cardinality: Many (opportunities) to Many (stage_history — each opp has multiple stage rows)  
Referential integrity: Some records may not match → leave as default

**opportunities → quotas**  
Add two relationship clauses:  
- `Owner` = `Owner`  
- `CloseQuarter` = `Quarter`

This is a multi-field relationship. Tableau 2020.2+ supports this natively.  
Cardinality: Many (opportunities) to One (quotas — one quota row per rep-quarter)

> **Why this model:** The relationship canvas keeps each table at its natural grain. Tableau only joins rows when a viz actually needs data from both tables, avoiding double-counting. The quota relationship on `CloseQuarter` = `Quarter` ensures each opportunity's pipeline ACV is paired with the correct rep quota for that period.

### Step 3 — Verify the connection

Create a quick test viz: drop `Owner` on Rows, `SUM(ACV)` on Columns, `SUM(Quota)` on a second axis. Both should populate per rep. If Quota shows null, double-check the `CloseQuarter` / `Quarter` relationship clause — string formatting must match exactly (both are "Q1 2024" format).

---

## Part 2: Parameters

Create these parameters before building any calculated fields.

### P1 — Quarter Selector

| Property | Value |
|----------|-------|
| Name | `[Quarter Selector]` |
| Data type | String |
| Allowable values | List |
| Values | Q1 2024, Q2 2024, Q3 2024, Q4 2024, Q1 2025, Q2 2025, Q3 2025, Q4 2025, Q1 2026, Q2 2026 |
| Current value | Q1 2026 |

### P2 — Coverage Target

| Property | Value |
|----------|-------|
| Name | `[Coverage Target]` |
| Data type | Float |
| Allowable values | Range: 1.0 – 5.0, step 0.5 |
| Current value | 3.0 |

> This feeds the reference band on the pipeline coverage chart. Changing it live updates the threshold — demonstrating dynamic targets.

### P3 — Selected Rep (for Set Actions)

| Property | Value |
|----------|-------|
| Name | `[Selected Rep]` |
| Data type | String |
| Current value | (All) |

Used as the target of the rep drill-through set action. Leave current value as "(All)".

---

## Part 3: Calculated Fields

Create all fields in the `opportunities` data source unless noted otherwise.

### Utility / type conversions

**[Is Open]**  
```
[IsClosed] = "false"
```
*Returns true for pipeline deals; false for resolved deals.*

**[Is Won]**  
```
[IsWon] = "true"
```

**[Days Since Activity]** ← use this instead of the pre-computed column  
```
DATEDIFF('day', [LastActivityDate], TODAY())
```
*Stays live as you demo. Apply to the deal aging table.*

**[Stage Sort]**  
```
CASE [StageName]
  WHEN "Prospect"    THEN 1
  WHEN "Qualified"   THEN 2
  WHEN "Demo"        THEN 3
  WHEN "Proposal"    THEN 4
  WHEN "Commit"      THEN 5
  WHEN "Closed Won"  THEN 6
  WHEN "Closed Lost" THEN 7
  ELSE 0
END
```
*Use as a sort field for any stage-ordered axis. Sort Ascending.*

**[Stage Sort (History)]**  
Create in `stage_history` data source:  
```
CASE [StageName]
  WHEN "Prospect"  THEN 1
  WHEN "Qualified" THEN 2
  WHEN "Demo"      THEN 3
  WHEN "Proposal"  THEN 4
  WHEN "Commit"    THEN 5
  ELSE 0
END
```

---

### Tab 1: Pipeline Health

**[Open ACV]**  
```
IF [Is Open] THEN [ACV] ELSE 0 END
```

**[Won ACV]**  
```
IF [Is Won] THEN [ACV] ELSE 0 END
```

**[Lost ACV]**  
```
IF [IsClosed] = "true" AND [IsWon] = "false" THEN [ACV] ELSE 0 END
```

**[Pipeline Coverage LOD]**  
The key LOD expression. FIXED at Quarter × Segment so rep/region filters do not distort the ratio.  
```
{ FIXED [CloseQuarter], [Segment] :
    SUM(IF [Is Open] THEN [ACV] ELSE 0 END)
}
/
NULLIF(
  { FIXED [CloseQuarter], [Segment] :
      SUM([Quota])
  },
  0
)
```
*`NULLIF(..., 0)` prevents divide-by-zero when a segment has no assigned quota.*

> **How to explain in an interview:** "The FIXED clause anchors the calculation to quarter and segment. If a viewer filters to see only Mia Torres's deals, the numerator correctly shows only her pipeline, and the denominator correctly shows only her quota — because both FIXED clauses share the same dimensions. The ratio stays meaningful at any filter granularity."

**[Coverage vs Target]** — for the reference band  
```
[Pipeline Coverage LOD] / [Coverage Target]
```
*Use as the mark on a bar chart. A reference line at 1.0 = the 3x target.*

**[Coverage Status]**  
```
IF [Pipeline Coverage LOD] >= [Coverage Target] THEN "On Track"
ELSEIF [Pipeline Coverage LOD] >= [Coverage Target] * 0.67 THEN "Monitor"
ELSE "At Risk"
END
```

**[Activity Status]**  
```
IF [Days Since Activity] < 14 THEN "Active"
ELSEIF [Days Since Activity] <= 30 THEN "Monitor"
ELSE "Stale"
END
```

**[Activity Status Sort]**  
```
CASE [Activity Status]
  WHEN "Active"  THEN 1
  WHEN "Monitor" THEN 2
  WHEN "Stale"   THEN 3
  ELSE 4
END
```

**[Rep In Set]** — for the drill-through set action  
```
[Owner] = [Selected Rep] OR [Selected Rep] = "(All)"
```
*Drives visibility of the deal-detail sheet when a rep is clicked.*

---

### Tab 2: Forecast Accuracy

**[Commit ACV (Historical)]**  
ACV of deals that reached Commit stage and then resolved (won or lost).  
```
IF [IsClosed] = "true" AND [HighestStage] = "Commit"
THEN [ACV]
ELSE 0
END
```
*The "Commit" bar in the forecast vs actual chart. Compare to [Won ACV] for the same quarter.*

**[Best Case ACV (Historical)]**  
```
IF [IsClosed] = "true" AND [HighestStage] IN ("Demo", "Proposal")
THEN [ACV]
ELSE 0
END
```

**[Open Commit ACV]**  
```
IF [Is Open] AND [ForecastCategory] = "Commit"
THEN [ACV]
ELSE 0
END
```
*Current quarter's outstanding commit forecast.*

**[Forecast Accuracy %]**  
```
SUM([Won ACV]) / NULLIF(SUM([Commit ACV (Historical)]), 0)
```
*Build this as a table calc or use a fixed LOD at quarter level:*
```
{ FIXED [CloseQuarter] : SUM([Won ACV]) }
/
NULLIF({ FIXED [CloseQuarter] : SUM([Commit ACV (Historical)]) }, 0)
```

**[Win Rate %]**  
```
SUM(IF [Is Won] THEN 1 ELSE 0 END)
/
NULLIF(SUM(IF [IsClosed] = "true" THEN 1 ELSE 0 END), 0)
```

**[Win Rate Label]**  
```
STR(ROUND([Win Rate %] * 100, 1)) + "%"
```

---

### Tab 3: ARR Performance

**[New ARR]**  
```
IF [Is Won] AND [ARRType] = "New" THEN [ACV] ELSE 0 END
```

**[Expansion ARR]**  
```
IF [Is Won] AND [ARRType] = "Expansion" THEN [ACV] ELSE 0 END
```

**[Renewal ARR]**  
```
IF [Is Won] AND [ARRType] = "Renewal" THEN [ACV] ELSE 0 END
```

**[Churn ARR]** ← negative by convention  
```
IF [IsClosed] = "true" AND [ARRType] = "Churn" THEN -[ACV] ELSE 0 END
```

**[Net New ARR]**  
```
[New ARR] + [Expansion ARR] + [Churn ARR]
```
*Churn ARR is already negative, so addition is correct.*

**[ARR Waterfall Type]**  
Drives the waterfall bar chart sort and coloring.  
```
CASE [ARRType]
  WHEN "New"       THEN IF [Is Won] THEN "New ARR" ELSE "Lost New" END
  WHEN "Expansion" THEN IF [Is Won] THEN "Expansion ARR" ELSE "Lost Expansion" END
  WHEN "Renewal"   THEN IF [Is Won] THEN "Renewal (retained)" ELSE "Churn" END
  WHEN "Churn"     THEN "Churn"
  ELSE "Other"
END
```

**[GRR %]** — Gross Revenue Retention  
Requires beginning ARR as a reference point. Compute per quarter using LOD:  
```
// Beginning ARR proxy = prior quarter's Renewal + Won ARR
// In Tableau, use a running total table calc across quarter.
// Formula for a quarterly GRR point:
(
  { FIXED [CloseQuarter] : SUM([Renewal ARR]) }
  - ABS({ FIXED [CloseQuarter] : SUM([Churn ARR]) })
)
/
NULLIF({ FIXED [CloseQuarter] : SUM([Renewal ARR]) }, 0)
```

> **Simplification note:** True GRR requires a cohort beginning ARR balance, which needs a fiscal calendar join not available in this single-table model. The formula above uses same-quarter renewal base as the denominator — a practical approximation that tells the right directional story. Note this in your interview: "In a real environment I'd pull beginning ARR from the billing system; here I'm approximating with the renewal cohort in the data."

**[NRR %]** — Net Revenue Retention  
```
(
  { FIXED [CloseQuarter] : SUM([Renewal ARR]) }
  + { FIXED [CloseQuarter] : SUM([Expansion ARR]) }
  - ABS({ FIXED [CloseQuarter] : SUM([Churn ARR]) })
)
/
NULLIF({ FIXED [CloseQuarter] : SUM([Renewal ARR]) }, 0)
```

**[Retention Label]**  
```
IF [NRR %] >= 1.1 THEN "Expanding"
ELSEIF [NRR %] >= 1.0 THEN "Stable"
ELSE "Contracting"
END
```

---

## Part 4: Sheet-by-Sheet Build

### Tab 1: Pipeline Health

---

#### Sheet 1A — Stage Funnel (CRM funnel chart)

1. Rows: `[StageName]` — filter to exclude "Closed Won" and "Closed Lost"
2. Sort StageName by `[Stage Sort]` ascending
3. Columns: Dual axis — `COUNT([OpportunityID])` on left, `SUM([Open ACV])` on right
4. Mark type: Bar
5. Color: `[StageName]` — use a sequential teal palette (dark = early stage, bright = late stage)
6. Tooltip: custom — include `COUNTD([Owner])` (reps with deals at this stage), `AVG([DaysInCurrentStage])`, `[Win Rate %]` (computed via FIXED LOD for this stage)

**Stage-level win rate for tooltip (LOD):**  
```
{ FIXED [StageName] :
    SUM(IF [Is Won] THEN 1 ELSE 0 END)
    / NULLIF(SUM(IF [IsClosed] = "true" THEN 1 ELSE 0 END), 0)
}
```

**Tooltip mini-chart:** Create a separate sheet (Sheet 1A-Tooltip) with:
- StageName on Rows, [Win Rate %] as a bar
- Format as a small bar with no axis titles
- Reference this sheet in the Stage Funnel tooltip via "Insert Sheet" in the tooltip editor

---

#### Sheet 1B — Pipeline Coverage Scorecard

1. Rows: `[Segment]`, Columns: `[CloseQuarter]`
2. Filter: `[IsClosed]` = false (pipeline only) + `[Quarter Selector]` parameter filter on CloseQuarter
3. Text: `[Pipeline Coverage LOD]` formatted as "0.0x"
4. Color: `[Coverage Status]`
   - On Track → `#008C7A`
   - Monitor → `#F2A900`
   - At Risk → `#C0392B`
5. Add `SUM([Open ACV])` as a secondary measure in the tooltip
6. Reference line: set at `[Coverage Target]` (parameter) on the row axis

---

#### Sheet 1C — Stage Duration Bar Chart

Source: `stage_history.csv` (use this sheet's data source)

1. Rows: `[StageName]` sorted by `[Stage Sort (History)]`
2. Columns: `AVG([DaysInStage])`
3. Filter: `IsCurrentStage` = "false" (exclude current open stage — only count completed stage transitions for accuracy)
4. Mark type: Bar, color single teal
5. Reference line: add a constant reference line per stage using `[Stage Sort (History)]` as band marker
   - Values: Prospect=14, Qualified=10, Demo=7, Proposal=14, Commit=10
   - Use a calculated field `[Stage Benchmark]`:  
   ```
   CASE [StageName]
     WHEN "Prospect"  THEN 14
     WHEN "Qualified" THEN 10
     WHEN "Demo"      THEN 7
     WHEN "Proposal"  THEN 14
     WHEN "Commit"    THEN 10
   END
   ```
   - Add `AVG([Stage Benchmark])` as a reference line with label "Benchmark"
   - Color the reference line `#C0392B`
6. Label: `AVG([DaysInStage])` formatted as "0.0d"

---

#### Sheet 1D — Deal Aging Table

1. Rows: `[Owner]`, `[AccountName]`, `[StageName]`, `[ACV]`, `[Days Since Activity]`
2. Filter: `[Is Open]` = true
3. Sort by `[Days Since Activity]` descending
4. Conditional formatting on `[Days Since Activity]`:
   - Color encode using `[Activity Status]`
   - Active → `#008C7A`, Monitor → `#F2A900`, Stale → `#C0392B`
5. Mark type: Text table
6. Hide row headers; use bold for `[ACV]` column, format as `$#,##0`

---

### Tab 2: Forecast Accuracy

#### Sheet 2A — Forecast vs Actual (6-quarter rolling bar)

1. Filter: `[IsClosed]` = true + last 6 quarters by CloseQuarter
2. Columns: `[CloseQuarter]` (sorted chronologically)
3. Rows: dual axis
   - Bar 1: `SUM([Commit ACV (Historical)])` — color `#5B6ABF` (indigo)
   - Bar 2: `SUM([Won ACV])` — color `#008C7A` (teal)
4. Synchronize axes, dual axis
5. Reference line: `[Forecast Accuracy %]` as a line on a third axis (right side)
   - Color: `#F2A900` amber
   - Label: percentage format

---

#### Sheet 2B — Win Rate Trend by Segment

1. Columns: `[CloseQuarter]`, Rows: `[Win Rate %]`
2. Color: `[Segment]` — use 3-color palette (SMB=light teal, MM=mid teal, Enterprise=dark navy)
3. Mark type: Line with circles
4. Filter: `[IsClosed]` = true
5. Reference line at 50% with label "Baseline"

---

#### Sheet 2C — Forecast Category Waterfall

Purpose: Show how ACV moves from Best Case → Commit → Closed Won in a given quarter.

1. Use a waterfall layout with these components on Columns:
   - "Best Case" = `SUM([Best Case ACV (Historical)])`
   - "Commit" = `SUM([Commit ACV (Historical)])`
   - "Closed Won" = `SUM([Won ACV])`
2. In Tableau, build as a Gantt bar with running total:
   - Rows: `[ARR Waterfall Type]` filtered to funnel categories
   - Columns: running SUM with Gantt bar encoding
   - Alternatively: use a simple grouped bar chart comparing all three series side-by-side per quarter — simpler to build, still tells the story
3. Filter: `[CloseQuarter]` = `[Quarter Selector]`
4. Color: Best Case=amber, Commit=indigo, Closed Won=teal

---

### Tab 3: ARR Performance

#### Sheet 3A — ARR Waterfall by Quarter

Build as a Gantt waterfall (the classic Tableau technique):

1. Create `[Running Total ARR]` table calc:
   ```
   RUNNING_SUM(SUM([New ARR]) + SUM([Expansion ARR]) + SUM([Churn ARR]))
   ```
2. Create `[Waterfall Base]` (offset for Gantt):
   ```
   PREVIOUS_VALUE(0) + SUM([Net New ARR])
   ```
   This requires Compute Using: CloseQuarter

3. Build the sheet:
   - Columns: `[CloseQuarter]`
   - Rows: `[Waterfall Base]` (continuous axis, hidden)
   - Mark type: Gantt Bar
   - Size: `SUM([Net New ARR])` on Size shelf
   - Color: `[Net New ARR] > 0` → teal; `< 0` → red

4. Overlay as a second mark type (line) for the cumulative ARR line:
   - Add `RUNNING_SUM(SUM([Net New ARR]))` as a line mark

5. Tooltip: include `SUM([New ARR])`, `SUM([Expansion ARR])`, `SUM([Churn ARR])`

---

#### Sheet 3B — GRR and NRR Trend Lines

1. Columns: `[CloseQuarter]`
2. Rows: dual axis — `[GRR %]` and `[NRR %]`
3. Mark type: Line with circles
4. GRR color: `#5B6ABF`, NRR color: `#008C7A`
5. Reference line at 100% — label "Breakeven"
6. Reference band: shade above 110% as a light green band (healthy NRR target)
7. Format Y axis as percentage, range 60% – 140%

---

#### Sheet 3C — Segment Mix of Closed ARR

1. Columns: `[CloseQuarter]`, Rows: `SUM([Won ACV])`
2. Color: `[Segment]`
3. Mark type: Bar (stacked)
4. Show percent of total as a label (table calc: percent of total along Table Down)
5. Add `COUNTD([AccountName])` in tooltip as "Accounts closed"

---

## Part 5: Set Action — Rep Drill-Through

1. Create a Set named `Rep Set`:
   - From Sheet 1B (Coverage Scorecard) or a rep summary bar chart
   - Field: `[Owner]`
   - Initial members: none (empty)

2. Create Dashboard Action:
   - Type: Set Action
   - Source: Sheet showing rep summary (e.g. coverage scorecard)
   - Target Set: `Rep Set`
   - Run on: Select
   - Clearing selection: Remove all values from set

3. Create "Rep Deal List" sheet:
   - Filter: `[Owner]` IN `Rep Set`
   - Columns: AccountName, StageName, ACV, CloseDate, ForecastCategory, DaysSinceActivity
   - Sort: ACV descending
   - Only visible when a rep is selected

4. On dashboard: wrap "Rep Deal List" in a layout container that shows/hides based on `COUNTD([Owner] in Rep Set) > 0`

> When a user clicks a rep on the coverage scorecard, the deal list appears below with that rep's open pipeline. Clicking elsewhere clears the set and hides the detail view.

---

## Part 6: Dashboard Assembly

### Tab 1 — Pipeline Health layout

```
┌─────────────────────────────────────────────────────────────┐
│  [Filter bar: Quarter, Region, Segment, Rep]                 │
├──────────────────────────────┬──────────────────────────────┤
│  Pipeline ACV (KPI)          │  Open Deals (KPI)            │
│  $XX.XM                      │  XXX                         │
├──────────────────────────────┴──────────────────────────────┤
│  Stage Funnel (1A)           │  Coverage Scorecard (1B)     │
│  [dual-axis bar, by stage]   │  [segment × quarter table]   │
├──────────────────────────────┴──────────────────────────────┤
│  Stage Duration (1C)         │  Deal Aging Table (1D)       │
│  [bar + benchmark line]      │  [conditional text table]    │
├──────────────────────────────┴──────────────────────────────┤
│  [Rep Deal List — hidden until rep clicked] (1E)             │
└─────────────────────────────────────────────────────────────┘
```

### Tab 2 — Forecast Accuracy layout

```
┌─────────────────────────────────────────────────────────────┐
│  [Filter bar: Quarter Selector, Segment, Region]             │
├───────────────────────────────────────────────────────────  │
│  Forecast Accuracy % (KPI)   │  Commit Coverage (KPI)       │
│  XX%                         │  $XX.XM vs $XX.XM quota      │
├──────────────────────────────┬──────────────────────────────┤
│  Forecast vs Actual (2A)     [6-quarter rolling bar+line]   │
│  [full width]                                               │
├──────────────────────────────┬──────────────────────────────┤
│  Win Rate Trend (2B)         │  Forecast Waterfall (2C)     │
│  [line by segment]           │  [Best Case/Commit/Won bars] │
└──────────────────────────────┴──────────────────────────────┘
```

### Tab 3 — ARR Performance layout

```
┌─────────────────────────────────────────────────────────────┐
│  [Filter bar: Segment, ARR Type, Region]                     │
├─────────────────────────────────────────────────────────────┤
│  Net New ARR (KPI)  │  NRR % (KPI)  │  Churn ARR (KPI)     │
│  $X.XM              │  XXX%         │  -$XXX K              │
├─────────────────────────────────────────────────────────────┤
│  ARR Waterfall by Quarter (3A)  [full width]                 │
├──────────────────────────────┬──────────────────────────────┤
│  GRR / NRR Trend Lines (3B)  │  Segment Mix of ARR (3C)    │
│  [dual line chart]           │  [stacked bar]               │
└──────────────────────────────┴──────────────────────────────┘
```

---

## Part 7: Formatting Standards

| Element | Setting |
|---------|---------|
| Dashboard background | `#1A1F2E` (dark navy) |
| Sheet background | `#1E2436` |
| KPI card container | White border radius 8px (Tableau 2026.1 corner radius) |
| KPI value font | 28pt semibold, white |
| KPI label font | 10pt, `#8892A8` (muted gray) |
| Chart title | 13pt semibold, white, action-oriented |
| Axis/tick labels | 9pt, `#8892A8` |
| Grid lines | Remove all; use `#2A3048` (subtle) for zero lines only |
| Tooltip background | `#0F1320`, white text, 12pt |
| Filter control background | Match sheet background |

### Color palette

| Role | Hex | Usage |
|------|-----|-------|
| Positive / on track | `#008C7A` | Won, above target, GRR/NRR healthy |
| Negative / at risk | `#C0392B` | Lost, below target, churn, stale deals |
| Watch / monitor | `#F2A900` | Approaching threshold, yellow zone |
| Accent indigo | `#5B6ABF` | Commit forecast, second data series |
| Neutral light | `#A0ABBA` | Labels, secondary text, axis ticks |
| Dark navy | `#1A1F2E` | Background |
| Card surface | `#1E2436` | Sheet containers |

---

## Part 8: Tooltip Spec

Every mark must have a tooltip. No empty tooltips.

| Sheet | Tooltip fields |
|-------|----------------|
| Stage Funnel | Stage, Count of Deals, Sum ACV, Avg Days in Stage, Win Rate % |
| Coverage Scorecard | Quarter, Segment, Pipeline ACV, Quota, Coverage Ratio, Coverage Status |
| Stage Duration | Stage, Avg Days, Benchmark Days, Delta vs Benchmark |
| Deal Aging | Account, Stage, ACV, Close Date, Days Since Activity, Activity Status |
| Forecast vs Actual | Quarter, Commit ACV, Won ACV, Forecast Accuracy % |
| Win Rate Trend | Quarter, Segment, Win Rate %, Deals Won, Deals Closed |
| ARR Waterfall | Quarter, New ARR, Expansion ARR, Churn ARR, Net New ARR |
| GRR / NRR | Quarter, GRR %, NRR %, Renewals Won, Churn ACV |
| Segment Mix | Quarter, Segment, Won ACV, % of total |
