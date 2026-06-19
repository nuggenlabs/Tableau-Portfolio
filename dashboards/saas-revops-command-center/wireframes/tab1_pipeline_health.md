# Wireframe — Tab 1: Pipeline Health
# Dashboard: 1400 × 900 · Dark navy background

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
| Stage duration bars | stage_history.DaysInStage (AVG), StageName | [Stage Sort (History)] |
| Stage benchmark line | [Stage Benchmark] (fixed constant) | [Stage Benchmark] |
| Deal aging rows | Owner, AccountName, ACV, DaysSinceActivity, StageName | [Days Since Activity] |
| Deal aging row color | [Activity Status] | [Activity Status] |
| Rep deal list | All fields | [Rep In Set] |

## Notes for Tableau build

- Funnel filter: `[IsClosed] = "false"` applied to both funnel sheets. Do NOT filter stage_history at dashboard level — only filter on the stage duration sheet.
- Coverage scorecard: hide row/column headers; show cell text only. Cell background color = Coverage Status.
- Deal aging table: sort descending on `[Days Since Activity]`. Conditional background color on the Days column only.
- Rep deal list: sits in a vertical layout container. Show/hide container using `COUNTD([Owner] in Rep Set) > 0` as a visibility condition (using a floating container approach or custom shape hack in Tableau 2026.1).
- Corner radius: apply to all four KPI card containers — Inner Padding 12px, Corner Radius 8px.
```
