# Wireframe — Tab 1: Pipeline Health
# Dashboard: 1400 × 900 · dark chrome / light content canvas

## Current design direction

Use `../tab1_mockup_v3.html` as the visual build reference. The ASCII wireframe below is the original structure, but the final Tableau dashboard should use the v3 hierarchy:

- Pipeline Coverage by Segment is the hero visual and should occupy the wider position in the first analytic row.
- Manager Focus sits inside the Pipeline Coverage card as a right-side insight panel.
- Open Pipeline by Stage is a supporting diagnostic, not the main focal point.
- Avg Days in Stage and Stalled Deals Requiring Follow-Up sit in the secondary row.
- Stalled deals should read as a manager action queue with a small summary strip, not as an equal-weight analytical chart.
- Use the light canvas system from `../workbook_formatting_guide.md`, not a full dark-navy dashboard body.
- Use rounded custom badge shapes from `../tableau_shapes/pipeline_badges/` for coverage status cells where practical.

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  SAAS REVOPS COMMAND CENTER                                  [Tab 1] [Tab 2] [Tab 3]    │
│  Pipeline Health                                                                         │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│  FILTERS  [Quarter ▾ Q1 2026]  [Region ▾ All]  [Segment ▾ All]  [Rep ▾ All]           │
├───────────────────┬───────────────────┬───────────────────┬───────────────────────────  │
│  OPEN PIPELINE    │  OPEN DEALS       │  AVG DEAL SIZE    │  DEALS AT RISK              │
│  $37.9M           │  240              │  $158K            │  34  (>30d no activity)     │
│  total ACV        │  active opps      │  across pipeline  │  needs attention            │
├───────────────────┴───────────────────┴───────────────────┴───────────────────────────  │
│  ┌─────────────────────────────────────┐  ┌──────────────────────────────────────────┐  │
│  │  FUNNEL — Count & ACV by Stage      │  │  PIPELINE COVERAGE  (3x target)          │  │
│  │                                     │  │  Coverage = Open ACV / Quota             │  │
│  │  Prospect  ████████████████  52     │  │                                          │  │
│  │  Qualified ██████████████    52     │  │          │ SMB    │ Mid-Mkt │ Enterprise │  │
│  │  Demo      ███████████████   54     │  │  Q1 2026 │ 2.8x ● │  3.4x ■ │  5.2x ■  │  │
│  │  Proposal  ██████████████    53     │  │  Q2 2026 │ 1.9x ○ │  3.1x ■ │  4.7x ■  │  │
│  │  Commit    █████████         29     │  │  Q3 2026 │ 3.2x ■ │  2.6x ● │  3.8x ■  │  │
│  │                                     │  │                                          │  │
│  │  ← Count    ACV →                  │  │  ■ On Track (≥3x)  ● Monitor  ○ At Risk  │  │
│  │  (dual axis, both visible)          │  │  [Coverage Target: 3x ─────]             │  │
│  └─────────────────────────────────────┘  └──────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────┐  ┌──────────────────────────────────────────┐  │
│  │  STAGE DURATION  (avg days)         │  │  DEAL AGING TABLE                        │  │
│  │  vs benchmark line                  │  │                                          │  │
│  │                                     │  │  Rep          Account       Stage   ACV  │  │
│  │  Prospect  ████████████  21d ─14d  │  │  ─────────────────────────────────────── │  │
│  │  Qualified ██████████    14d ─10d  │  │  D. Fernandez  Mosaic Cloud   Proposal   │  │
│  │  Demo      ███████        9d ─7d   │  │                                 $89K  ● 5d│  │
│  │  Proposal  ██████████████ 16d ─14d │  │  M. Webb       Ironclad       Commit     │  │
│  │  Commit    ████████████   13d ─10d │  │                               $340K  ■ 2d │  │
│  │                                     │  │  A. Singh      Notion Labs    Demo       │  │
│  │  ─── = Benchmark  bar = Actual      │  │                                $22K  ○ 35d│  │
│  │                                     │  │                                          │  │
│  │                          [Stale ─ red benchmark line at right side overrun]       │  │
│  └─────────────────────────────────────┘  └──────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐  │
│  │  REP DEAL LIST  (hidden · appears when rep clicked on coverage scorecard)           │  │
│  │  Owner: Priya Kapoor   Account   Stage   ACV   Close Date   Forecast   Days Stale  │  │
│  │  ─────────────────────────────────────────────────────────────────────────────────  │  │
│  │  [deals filtered by selected rep, sorted by ACV desc]                              │  │
│  └─────────────────────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

## Field-to-visual mapping

| Visual element | Fields used | Calculated field |
|----------------|-------------|------------------|
| Funnel bar (count) | OpportunityID (COUNT), StageName | [Stage Sort] |
| Funnel bar (ACV) | ACV (SUM), StageName | [Open ACV] |
| Funnel tooltip | Owner (COUNTD), DaysInCurrentStage (AVG), IsWon | [Win Rate per Stage LOD] |
| Coverage scorecard cells | ACV, Quota, CloseQuarter, Segment | [Pipeline Coverage LOD] |
| Coverage cell color | [Coverage Status] | [Coverage Status] |
| Coverage badge shape | [Coverage Status] | custom PNGs in `tableau_shapes/pipeline_badges/` |
| Coverage badge label | [Pipeline Coverage LOD], [Coverage Status] | centered Shape mark label |
| Manager Focus numerator | quotas_by_segment.[Segment Quarter Key] filtered to At Risk | COUNTD([Segment Quarter Key]) |
| Manager Focus denominator | quotas_by_segment.[Segment Quarter Key] without status filter | COUNTD([Segment Quarter Key]) |
| Manager Focus narrative | Dashboard text object | Static action sentence |
| Manager Focus segment averages | [Pipeline Coverage LOD], Segment, CloseQuarter | AVG or WINDOW_AVG of coverage |
| Stage duration bars | stage_history.DaysInStage (AVG), StageName | [Stage Sort (History)] |
| Stage benchmark line | [Stage Benchmark] (fixed constant) | [Stage Benchmark] |
| Stage benchmark status | [Avg Days in Stage], [Stage Benchmark] | [Stage Benchmark Status] |
| Deal aging rows | Owner, AccountName, ACV, DaysSinceActivity, StageName | [Days Since Activity] |
| Deal aging row color | [Activity Status] | [Activity Status] |
| Rep deal list | All fields | [Rep In Set] |

## Notes for Tableau build

- Funnel filter: `[IsClosed] = FALSE` applied to both funnel sheets. Do NOT filter stage_history at dashboard level — only filter on the stage duration sheet.
- Coverage scorecard: build as the hero visual. Hide row/column headers if they duplicate visible labels. Use custom rounded badge shapes by `[Coverage Status]`, then center the coverage value and status label over the shape.
- Coverage labels: value should be bold semantic color, status should be small uppercase muted blue-gray.
- Manager Focus: build as a compact vertical panel inside the Pipeline Coverage card. Use `quotas_by_segment.csv` as the Segment x Quarter scaffold. Count At Risk combinations only; Monitor combinations remain visible in the matrix but are not included in the focus count.
- Manager Focus panel styling: `#F2F5FB` fill, `#DDE4F2` border, 8px corner radius, 12px inner padding.
- Deal aging table: sort descending on `[Days Since Activity]`. Conditional color belongs on the Days column only. Include a small action-summary strip above the table if space allows.
- Stage duration status: color bars by `[Stage Benchmark Status]`; Over = red, Slightly Over = amber, OK = teal. Use the benchmark line as the visual reference, not as a fourth color category.
- Rep deal list: sits in a vertical layout container. Show/hide container using `COUNTD([Owner] in Rep Set) > 0` as a visibility condition (using a floating container approach or custom shape hack in Tableau 2026.1).
- Corner radius: apply 10px to KPI and chart containers. Use 12px inner padding on KPI cards.
```
