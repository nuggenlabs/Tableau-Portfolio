# Tableau Build Guide — SaaS RevOps Command Center

**Dashboard size:** 1400 × 900  
**Tableau version:** 2026.1  
**Data sources:** opportunities.csv · stage_history.csv · quotas.csv  
**Published to:** Tableau Public  

---

## Part 1: Data Model Setup

### Step 1 — Connect to the data sources

> v3 note: add `quotas_by_segment.csv` in addition to `opportunities.csv`, `stage_history.csv`, and `quotas.csv`. This table acts as a one-row-per-Segment-per-Quarter scaffold and avoids unnecessary table calculations for the Manager Focus count.

1. Open Tableau Desktop. Connect → Text File → `opportunities.csv`
2. On the data source canvas, drag in `stage_history.csv` and `quotas.csv`
3. Tableau will open the relationship editor

### Step 2 — Define relationships

For `quotas_by_segment.csv`, relate it to `opportunities.csv` using:
- `Segment` = `Segment`
- `CloseQuarter` = `Quarter`

Use this relationship for the Pipeline Coverage scorecard and Manager Focus panel when you need one visible mark per Segment x Quarter combination.

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
| Name | `[p.Quarter Selector]` |
| Data type | String |
| Allowable values | List |
| Values | Q1 2024, Q2 2024, Q3 2024, Q4 2024, Q1 2025, Q2 2025, Q3 2025, Q4 2025, Q1 2026, Q2 2026 |
| Current value | Q1 2026 |

### P2 — Coverage Target

| Property | Value |
|----------|-------|
| Name | `[p.Coverage Target]` |
| Data type | Float |
| Allowable values | Range: 1.0 – 5.0, step 0.5 |
| Current value | 3.0 |

> This feeds the reference band on the pipeline coverage chart. Changing it live updates the threshold — demonstrating dynamic targets.

### P3 — Selected Rep (for Set Actions)

| Property | Value |
|----------|-------|
| Name | `[p.Selected Rep]` |
| Data type | String |
| Current value | (All) |

Used as the target of the rep drill-through set action. Leave current value as "(All)".

---

## Part 3: Calculated Fields

Create all fields in the `opportunities` data source unless noted otherwise.

### Utility / type conversions

**[Is Open]**  
```
[IsClosed] = FALSE
```
*Returns true for pipeline deals; false for resolved deals.*

**[Is Won]**  
```
[IsWon] = TRUE
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

**[Stage Benchmark]**  
Create in `stage_history` data source. This is the target number of days for each completed stage.
```
CASE [StageName]
  WHEN "Prospect"  THEN 14
  WHEN "Qualified" THEN 10
  WHEN "Demo"      THEN 7
  WHEN "Proposal"  THEN 14
  WHEN "Commit"    THEN 10
END
```

**[Avg Days in Stage]**  
Create in `stage_history` data source.
```
AVG([DaysInStage])
```

**[Stage Benchmark Variance]**  
Create in `stage_history` data source. Positive values mean the stage is taking longer than benchmark.
```
[Avg Days in Stage] - AVG([Stage Benchmark])
```

**[Stage Benchmark Status]**  
Create in `stage_history` data source.
```
IF [Avg Days in Stage] <= AVG([Stage Benchmark]) THEN "OK"
ELSEIF [Avg Days in Stage] <= AVG([Stage Benchmark]) * 1.15 THEN "Slightly Over"
ELSE "Over"
END
```

**[Stage Benchmark Status Sort]**  
Optional helper if you need a consistent legend or table sort.
```
CASE [Stage Benchmark Status]
  WHEN "Over" THEN 1
  WHEN "Slightly Over" THEN 2
  WHEN "OK" THEN 3
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
IF [IsClosed] = TRUE AND [IsWon] = FALSE THEN [ACV] ELSE 0 END
```

**[Pipeline Coverage LOD]**  
The key LOD expression. FIXED at Quarter × Segment so rep/region filters do not distort the ratio.  
```
{ FIXED [CloseQuarter], [Segment] :
    SUM(IF [Is Open] THEN [ACV] ELSE 0 END)
}
/
NULLIF(SUM([Quota]), 0)
```
*The numerator is a FIXED LOD (opportunities only — no fan-out risk). The denominator is a regular SUM so Tableau queries the quotas table independently at the view grain (Segment × Quarter), avoiding the fan-out that occurs when [Quota] is placed inside a FIXED LOD.*

> **How to explain in an interview:** "The FIXED clause anchors the numerator to quarter and segment so rep and region filters don't distort the pipeline total. The denominator uses a regular SUM so Tableau's relationship model queries quotas at the correct segment-quarter grain without duplicating values across opportunity rows."

**[Coverage vs Target]** — for the reference band  
```
[Pipeline Coverage LOD] / [p.Coverage Target]
```
*Use as the mark on a bar chart. A reference line at 1.0 = the 3x target.*

**[Coverage Status]**  
```
IF [Pipeline Coverage LOD] >= [p.Coverage Target] THEN "On Track"
ELSEIF [Pipeline Coverage LOD] >= [p.Coverage Target] * 0.67 THEN "Monitor"
ELSE "At Risk"
END
```

**[Segment Quarter Key]**  
Create this in `quotas_by_segment.csv`. It gives Manager Focus a clean one-row-per-combination count.
```
[Quarter] + "|" + [Segment]
```

**[Coverage Status - Segment Quarter]**  
Use this version on views built from the `quotas_by_segment.csv` scaffold.
```
IF SUM([Open ACV]) / SUM([Quota]) >= [p.Coverage Target] THEN "On Track"
ELSEIF SUM([Open ACV]) / SUM([Quota]) >= [p.Coverage Target] * 0.67 THEN "Monitor"
ELSE "At Risk"
END
```

Manager Focus count note: do not force this into one table calculation. Build the numerator and denominator as two simple count sheets:
- Numerator sheet: filter `[Coverage Status - Segment Quarter]` to `At Risk`, then show `COUNTD([Segment Quarter Key])`
- Denominator sheet: same quarter filters, no status filter, then show `COUNTD([Segment Quarter Key])`
- Dashboard text object between them: `of`

This produces the At Risk count out of all visible Segment x Quarter combinations while excluding Monitor combinations from the numerator. With the current mock data shown in the debug table, the expected result is `6 of 9`.

**[Segment Quarter Coverage Ratio]**  
Use the exact quarter field name from your workbook. If your field is named `[Close Quarter]`, use that instead of `[CloseQuarter]`.
```
{ FIXED [Segment], [CloseQuarter] : SUM([Open ACV]) }
/
{ FIXED [Segment], [CloseQuarter] : SUM([Quota]) }
```

**[Is At Risk Segment Quarter]**  
```
[Segment Quarter Coverage Ratio] < ([p.Coverage Target] * 0.67)
```

**[At Risk Segment Quarter Count]**  
```
COUNTD(
    IF [Is At Risk Segment Quarter]
    THEN [Segment Quarter Key]
    END
)
```

**[Total Segment Quarter Count]**  
```
COUNTD([Segment Quarter Key])
```

**[Coverage Focus Narrative]**  
Optional dynamic sentence for the Manager Focus panel. Use this only if you want a worksheet-driven narrative instead of a static dashboard text object.
```
IF [At Risk Segment Quarter Count] = 0 THEN
    "No visible segment-quarter combinations are At Risk."
ELSEIF [At Risk Segment Quarter Count] = [Total Segment Quarter Count] THEN
    "All visible segment-quarter combinations are At Risk."
ELSE
    STR([At Risk Segment Quarter Count])
    + " segment-quarter combinations are At Risk. Monitor combinations are excluded from this count."
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
[Owner] = [p.Selected Rep] OR [p.Selected Rep] = "(All)"
```
*Drives visibility of the deal-detail sheet when a rep is clicked.*

---

### Tab 2: Forecast Accuracy

**[Commit ACV (Historical)]**  
ACV of deals that reached Commit stage and then resolved (won or lost).  
```
IF [IsClosed] = TRUE AND [HighestStage] = "Commit"
THEN [ACV]
ELSE 0
END
```
*The "Commit" bar in the forecast vs actual chart. Compare to [Won ACV] for the same quarter.*

**[Best Case ACV (Historical)]**  
```
IF [IsClosed] = TRUE AND [HighestStage] IN ("Demo", "Proposal")
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
NULLIF(SUM(IF [IsClosed] = TRUE THEN 1 ELSE 0 END), 0)
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
IF [IsClosed] = TRUE AND [ARRType] = "Churn" THEN -[ACV] ELSE 0 END
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
    / NULLIF(SUM(IF [IsClosed] = TRUE THEN 1 ELSE 0 END), 0)
}
```

**Tooltip mini-chart:** Create a separate sheet (Sheet 1A-Tooltip) with:
- StageName on Rows, [Win Rate %] as a bar
- Format as a small bar with no axis titles
- Reference this sheet in the Stage Funnel tooltip via "Insert Sheet" in the tooltip editor

---

#### Sheet 1B — Pipeline Coverage Scorecard

1. Rows: `[Segment]`, Columns: `[CloseQuarter]`
2. Filter: `[IsClosed]` = false (pipeline only) + `[p.Quarter Selector]` parameter filter on CloseQuarter
3. Text: `[Pipeline Coverage LOD]` formatted as "0.0x"
4. Color: `[Coverage Status]`
   - On Track → `#008C7A`
   - Monitor → `#F2A900`
   - At Risk → `#C0392B`
5. Add `SUM([Open ACV])` as a secondary measure in the tooltip
6. Reference line: set at `[p.Coverage Target]` (parameter) on the row axis

> Design update: for the current v3 dashboard direction, use the badge-based setup below instead of the older text-table scorecard instructions above.

---

#### Sheet 1B v3 — Pipeline Coverage Badge Scorecard

Use this as the hero sheet on Tab 1.

1. Columns: `[Segment]`
2. Rows: `[CloseQuarter]`
3. Filter: `[IsClosed]` = false (pipeline only)
4. Optional filter: show the current and next two open quarters (`Q1 2026`, `Q2 2026`, `Q3 2026`) so the panel has 9 visible Segment x Quarter combinations
5. Mark type: Shape
6. Shape: assign the rounded badge PNGs from `tableau_shapes/pipeline_badges/` by `[Coverage Status]`
   - On Track: `coverage-badge-on-track-blank.png`
   - Monitor: `coverage-badge-monitor-blank.png`
   - At Risk: `coverage-badge-at-risk-blank.png`
7. Label: `[Pipeline Coverage LOD]` formatted as `0.00x`, plus `[Coverage Status]` on the second line
8. Label alignment: center / middle
9. Label font:
   - Coverage value: 12-14pt, bold, semantic color
   - Status label: 6-7pt, bold, uppercase, `#6C7B96`
10. Tooltip: Quarter, Segment, Pipeline ACV, Quota, Coverage Ratio, Coverage Status
11. Hide row/column headers if visible labels duplicate the view

---

#### Manager Focus v3 recommended count setup

Use this setup instead of the single-sheet table calculation approach. It is simpler and more stable because `quotas_by_segment.csv` already gives one row per Segment x Quarter combination.

Build the Manager Focus count display with two small worksheets and one dashboard text object:

**Numerator sheet: `Manager Focus At Risk Count`**

1. Use `quotas_by_segment.csv` as the scaffold table for the view.
2. Filter to the same quarters used by Sheet 1B v3.
3. Add `[Coverage Status - Segment Quarter]` to Filters and keep only `At Risk`.
4. Marks: Text.
5. Text: `COUNTD([Segment Quarter Key])`.
6. Format: 26-30pt bold, `#D63344`.
7. Tooltip: disabled.

With the current mock data in the debug table, this sheet should return `6`.

**Denominator sheet: `Manager Focus Total Count`**

1. Use `quotas_by_segment.csv` as the scaffold table for the view.
2. Filter to the same quarters used by Sheet 1B v3.
3. Do not filter by `[Coverage Status - Segment Quarter]`.
4. Marks: Text.
5. Text: `COUNTD([Segment Quarter Key])`.
6. Format: 26-30pt bold, `#0F1C36`.
7. Tooltip: disabled.

This sheet should return `9`.

**Dashboard assembly**

1. Place `Manager Focus At Risk Count`, a text object reading `of`, and `Manager Focus Total Count` in a horizontal container.
2. Add the narrative below as a dashboard text object: `Segment-quarter combinations are At Risk. Review the weakest segment averages first.`
3. With the current mock data, this produces `6 of 9` while excluding Monitor combinations from the numerator.

#### Sheet 1B-1 — Manager Focus Count

Fallback only. Prefer the v3 recommended count setup above.

Purpose: the large At Risk count callout in the Manager Focus panel.

1. New worksheet named `Manager Focus Count`
2. Filter to the same quarters used by Sheet 1B v3
3. Put `[Segment]` and `[CloseQuarter]` on Detail. These fields create the visible combinations that the table calculation counts.
4. Marks: Text
5. Text: `[Coverage Focus Label]`
6. Add `[Manager Focus Single Mark Filter]` to Filters and keep `True`
7. Edit Table Calculation for `[Coverage Focus Label]`, `[Coverage At Risk Count]`, `[Coverage Combo Count]`, and `[Manager Focus Single Mark Filter]`:
   - Compute using: Specific Dimensions
   - Check `[Segment]` and `[CloseQuarter]`
   - Restarting every: None
   - In the Nested Calculations dropdown, repeat this setting for every nested table calc listed
8. Format:
   - Font: 26-30pt, bold
   - Color: `#D63344` if `[Coverage At Risk Count] > 0`, otherwise `#00A87A`
   - Alignment: left / middle
9. Tooltip: disabled or simple explanation: "Visible segment-quarter combinations with At Risk status."

If Tableau does not allow the string calculation to format cleanly, place `[Coverage At Risk Count]`, literal text `of`, and `[Coverage Combo Count]` directly on the Text shelf and edit the label.

Troubleshooting:
- If the view shows repeated labels like `1 of 1 0 of 1 0 of 1`, Tableau is partitioning the numerator and denominator by each Segment x Quarter mark.
- If the view shows `5 of 1` repeated 9 times, the numerator is computing across the full grid, but `[Coverage Combo Count]` and/or `[Manager Focus Single Mark Filter]` are still partitioned per mark.
- Right-click each table-calc pill, including nested calculations, and set Specific Dimensions to address across both `[Segment]` and `[CloseQuarter]`.
- For `[Manager Focus Single Mark Filter]`, use `LAST() = 0` and keep only `True`. This leaves one visible label after the table calculations have already computed across the full 3 x 3 grid.
- The correct view should render one label such as `6 of 9` for the current mock data.

---

#### Sheet 1B-2 — Manager Focus Narrative

Optional. Prefer the static dashboard text object in the v3 recommended setup unless you want this sentence to change dynamically.

1. New worksheet named `Manager Focus Narrative`
2. Apply the same quarter filter as Sheet 1B v3
3. Marks: Text
4. Text: `[Coverage Focus Narrative]`
5. Format:
   - Font: 9pt regular
   - Color: `#3D4F6F`
   - Alignment: left / top
6. Fit: Entire View

Keep this sentence short. It should explain where to look next, not repeat the whole chart.

---

#### Sheet 1B-3 — Manager Focus Segment Averages

Purpose: the three-line list showing average coverage by segment in the Manager Focus panel.

1. New worksheet named `Manager Focus Segment Averages`
2. Rows: `[Segment]`
3. Detail: `[CloseQuarter]`
4. Text: `WINDOW_AVG(AVG([Pipeline Coverage LOD]))`, formatted as `0.00x`
5. Filter to the same quarters used by Sheet 1B v3
6. Sort segments in business order: SMB, Mid-Market, Enterprise
7. Edit Table Calculation:
   - Compute using: `[CloseQuarter]`
   - Restart every: `[Segment]`
8. Format:
   - Segment label: 9-10pt, `#3D4F6F`
   - Value: 9-10pt bold, `#0F1C36`
   - Remove grid lines, row dividers, and headers where possible

Build note: because `[Pipeline Coverage LOD]` is fixed at Segment x Quarter, keep `[CloseQuarter]` on Detail while computing the average. This prevents the average from being weighted by opportunity row count.

---

#### Sheet 1C — Stage Duration Bar Chart

Source: `stage_history.csv` (use this sheet's data source)

1. Rows: `[StageName]` sorted by `[Stage Sort (History)]`
2. Columns: `[Avg Days in Stage]`
3. Filter: `IsCurrentStage` = FALSE (exclude current open stage — only count completed stage transitions for accuracy)
4. Mark type: Bar
5. Color: `[Stage Benchmark Status]`
   - Over: `#D63344`
   - Slightly Over: `#E59300`
   - OK: `#00A87A`
6. Reference line: add `AVG([Stage Benchmark])` with label "Benchmark"
   - Color: `#8492B0`
   - Line: 1pt dashed
7. Label: `[Avg Days in Stage]` formatted as `0.0d`
8. Tooltip: Stage, Avg Days in Stage, Stage Benchmark, Stage Benchmark Variance, Stage Benchmark Status

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
3. Filter: `[CloseQuarter]` = `[p.Quarter Selector]`
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

#### Tab 1 v3 assembly notes

Use `tab1_mockup_v3.html` as the visual reference. The key change from the original sketch is that Pipeline Coverage becomes the hero object, and Manager Focus sits inside the same hero card as a right-side insight panel.

Recommended container structure:

1. Create a horizontal container for the hero row.
2. Set the hero row width split to roughly 60/40:
   - Left/wide card: Pipeline Coverage by Segment
   - Right/narrow card: Open Pipeline by Stage
3. Inside the Pipeline Coverage card, create a horizontal inner container:
   - Left section, about 75% width: `Sheet 1B v3 - Pipeline Coverage Badge Scorecard`
   - Right section, about 25% width: Manager Focus panel
4. Build the Manager Focus panel as a vertical container:
   - Text object: `MANAGER FOCUS`, 8pt bold uppercase, `#8492B0`
   - `Sheet 1B-1 - Manager Focus Count`
   - `Sheet 1B-2 - Manager Focus Narrative`
   - `Sheet 1B-3 - Manager Focus Segment Averages`
5. Manager Focus panel formatting:
   - Background: `#F2F5FB`
   - Border: `#DDE4F2`
   - Corner radius: 8px
   - Inner padding: 12px
6. Keep the panel compact. It should summarize where managers should look, not compete with the coverage matrix.

Manager Focus should answer: "How many visible segment-quarter combinations are At Risk, and which segment has the weakest average coverage?" Monitor combinations are not included in this count.

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
