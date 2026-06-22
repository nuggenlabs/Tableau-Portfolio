# Sheet Field Reference — SaaS RevOps Command Center

Quick lookup for what goes on each shelf for every sheet in the workbook.
All fields are from the **opportunities** data source unless marked **(stage_history)** or **(quotas)**.

---

## Tab 1 — Pipeline Health

### KPI Cards (1-KPI-Pipeline, 1-KPI-Deals, 1-KPI-AvgDeal, 1-KPI-AtRisk)

| Card | Measure on Text shelf | Filter |
|---|---|---|
| Open Pipeline ACV | `SUM([Open ACV])` | `[CloseQuarter] = [Quarter Selector]` |
| Open Deals | `COUNT([OpportunityID])` | `[IsClosed] = FALSE` + `[CloseQuarter] = [Quarter Selector]` |
| Avg Deal Size | `AVG(IF [IsClosed] = FALSE THEN [ACV] END)` | `[CloseQuarter] = [Quarter Selector]` |
| Deals at Risk | `SUM(IF [Is Deal at Risk] THEN 1 ELSE 0 END)` | `[CloseQuarter] = [Quarter Selector]` |

---

### Sheet 1A — Stage Funnel

| Shelf | Field | Notes |
|---|---|---|
| Rows | `[StageName]` | Sort by `[Stage Sort]` ascending |
| Columns (left axis) | `COUNT([OpportunityID])` | Bar mark |
| Columns (right axis) | `SUM([Open ACV])` | Dual axis bar |
| Color | `[StageName]` | Sequential teal palette |
| Filters | `[IsClosed] = FALSE` | Exclude Closed Won and Closed Lost from funnel |
| Filters | `[CloseQuarter] = [Quarter Selector]` | Selected quarter only |

---

### Sheet 1B — Pipeline Coverage Scorecard

| Shelf | Field | Notes |
|---|---|---|
| Rows | `[Segment]` | SMB / Mid-Market / Enterprise |
| Columns | `[CloseQuarter]` | **From opportunities — not `[Quarter]` from quotas** |
| Text | `[Pipeline Coverage LOD]` | Format as `0.0x` |
| Color | `[Coverage Status]` | On Track / Monitor / At Risk |
| Filters | `[IsClosed] = FALSE` | Open pipeline only |
| **No parameter filter** | — | Show all open quarters simultaneously — do not filter by `[Quarter Selector]` |

> `[CloseQuarter]` and `[Quarter]` (from quotas) look the same in the data pane. Always use `[CloseQuarter]` from opportunities here — it matches what the LOD expression is fixed on.

---

### Sheet 1C — Stage Duration Bar Chart

| Shelf | Field | Notes |
|---|---|---|
| Rows | `[StageName]` **(stage_history)** | Sort by `[Stage Sort (History)]` ascending |
| Columns | `AVG([DaysInStage])` **(stage_history)** | |
| Reference line | `AVG([Stage Benchmark])` | One per stage — color `#E84855` |
| Filters | `[IsCurrentStage] = FALSE` **(stage_history)** | Completed transitions only — exclude active open stage |
| Label | `AVG([DaysInStage])` | Format `0.0d` |
| **No parameter filter** | — | Stage duration reflects all historical data — not quarter-specific |

> This sheet uses the **stage_history** data source, not opportunities. Switch data source in the sheet before building.

---

### Sheet 1D — Deal Aging Table

| Shelf | Field | Notes |
|---|---|---|
| Rows | `[Owner]`, `[AccountName]`, `[StageName]`, `[ACV]`, `[Days Since Activity]` | Text table mark |
| Color | `[Activity Status]` | Active / Monitor / Stale — on `[Days Since Activity]` column only |
| Sort | `[Days Since Activity]` descending | Most stale deals at top |
| Filters | `[IsClosed] = FALSE` | Open deals only |
| Filters | `[CloseQuarter] = [Quarter Selector]` | Selected quarter |

---

### Sheet 1E — Rep Deal List (drill-through, hidden by default)

| Shelf | Field | Notes |
|---|---|---|
| Rows | `[AccountName]`, `[StageName]`, `[ACV]`, `[CloseDate]`, `[ForecastCategory]`, `[Days Since Activity]` | Text table |
| Filters | `[IsClosed] = FALSE` | Open pipeline only |
| Filters | `[Owner]` IN `Rep Set` | Set action drives this — list only appears when rep is selected |
| Sort | `[ACV]` descending | |

---

## Tab 2 — Forecast Accuracy

### KPI Cards (2-KPI-Accuracy, 2-KPI-Commit)

| Card | Measure | Filter |
|---|---|---|
| Forecast Accuracy % | `[Forecast Accuracy %]` (LOD) | `[CloseQuarter] = [Quarter Selector]` |
| Commit Coverage | `SUM([Open Commit ACV])` vs `SUM([Quota])` | `[CloseQuarter] = [Quarter Selector]` |

---

### Sheet 2A — Forecast vs Actual (6-quarter rolling)

| Shelf | Field | Notes |
|---|---|---|
| Columns | `[CloseQuarter]` | Sort by `[QuarterStart]` **(quotas)** for correct chronological order |
| Rows (left axis) | `SUM([Commit ACV (Historical)])` | Bar mark, color `#7B61FF` |
| Rows (right axis) | `SUM([Won ACV])` | Bar mark, color `#00C49A` |
| Filters | `[IsClosed] = TRUE` | Closed deals only |
| Filters | Last 6 values of `[CloseQuarter]` | Relative filter or `[Last 6 Closed Quarters]` calc |
| **No parameter filter** | — | Rolling view — always shows 6 most recent quarters |

---

### Sheet 2B — Win Rate Trend by Segment

| Shelf | Field | Notes |
|---|---|---|
| Columns | `[CloseQuarter]` | Sort chronologically |
| Rows | `[Win Rate %]` | Format as percentage |
| Color | `[Segment]` | 3-color teal range |
| Filters | `[IsClosed] = TRUE` | Closed deals only — complete quarters |
| Mark type | Line with circles | |
| Reference line | Fixed at 0.5 (50%) | Label "Baseline" |

---

### Sheet 2C — Forecast Category Flow

| Shelf | Field | Notes |
|---|---|---|
| Columns | `[ForecastCategory]` or waterfall category | Best Case / Commit / Closed Won order |
| Rows | `SUM([ACV])` by category | |
| Filters | `[CloseQuarter] = [Quarter Selector]` | Selected quarter |
| Color | Category — amber / indigo / teal | |

---

## Tab 3 — ARR Performance

### KPI Cards (3-KPI-NetARR, 3-KPI-NRR, 3-KPI-Churn)

| Card | Measure | Filter |
|---|---|---|
| Net New ARR | `SUM([Net New ARR])` | `[CloseQuarter] = [Quarter Selector]` |
| NRR % | `[NRR %]` (LOD) | `[CloseQuarter] = [Quarter Selector]` |
| Churn ARR | `SUM([Churn ARR])` | `[CloseQuarter] = [Quarter Selector]` |

---

### Sheet 3A — ARR Waterfall

| Shelf | Field | Notes |
|---|---|---|
| Columns | `[CloseQuarter]` | Sort chronologically |
| Rows | `[Waterfall Base]` (table calc) | Hidden axis — used for Gantt offset |
| Size | `SUM([Net New ARR])` | Bar height = net ARR movement |
| Color | `SUM([Net New ARR]) > 0` | Teal positive / red negative |
| Mark type | Gantt Bar | |
| Tooltip | `SUM([New ARR])`, `SUM([Expansion ARR])`, `SUM([Churn ARR])` | |

---

### Sheet 3B — GRR / NRR Trend Lines

| Shelf | Field | Notes |
|---|---|---|
| Columns | `[CloseQuarter]` | Sort chronologically |
| Rows (left) | `[NRR %]` | Color `#00C49A` |
| Rows (right) | `[GRR %]` | Color `#94A3C8`, dual axis |
| Reference line | Fixed at 1.0 (100%) | Label "Breakeven", color `#E84855` |
| Y-axis range | 60% – 140% | |

---

### Sheet 3C — Segment Mix of Closed ARR

| Shelf | Field | Notes |
|---|---|---|
| Columns | `[CloseQuarter]` | Sort chronologically |
| Rows | `SUM([Won ACV])` | |
| Color | `[Segment]` | Stacked bar |
| Mark type | Bar (stacked) | |
| Label | Percent of total (table calc: % of Table Down) | |

---

## Field Source Quick Reference

When the same field name appears in multiple tables, use this table to pick the right one.

| Field name | Use from | Never use from | Why |
|---|---|---|---|
| `[CloseQuarter]` | opportunities | — | Only exists in opportunities |
| `[Quarter]` | quotas | — | Only exists in quotas — used in relationship definition only, not in sheets |
| `[Owner]` | opportunities | quotas | Opportunities is anchor — using quotas Owner causes NULL rows for unmatched periods |
| `[Segment]` | opportunities | quotas | Same reason as Owner |
| `[Region]` | opportunities | quotas | Same reason |
| `[StageName]` | stage_history (for duration) | opportunities (for funnel) | Duration chart needs stage_history grain; funnel needs current stage from opportunities |
| `[DaysInStage]` | stage_history | — | Only exists in stage_history |
