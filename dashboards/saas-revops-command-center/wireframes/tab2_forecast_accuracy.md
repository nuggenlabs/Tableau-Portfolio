# Wireframe — Tab 2: Forecast Accuracy
# Dashboard: 1400 × 900 · dark chrome / light content canvas

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  SAAS REVOPS COMMAND CENTER                                  [Tab 1] [Tab 2] [Tab 3]    │
│  Forecast Accuracy                                                                       │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│  FILTERS  [Quarter ▾ Q4 2025]  [Segment ▾ All]  [Region ▾ All]                        │
├───────────────────┬───────────────────┬───────────────────┬───────────────────────────  │
│  FORECAST ACC.    │  COMMIT ACV       │  WON ACV          │  WIN RATE (closed)          │
│  (selected qtr)   │  (committed qtr)  │  (closed qtr)     │  (closed qtr)               │
│  68%              │  $4.1M            │  $2.8M            │  31%                        │
│  Commit → Closed  │  deals in Commit  │  closed won       │  closed deals               │
├───────────────────┴───────────────────┴───────────────────┴───────────────────────────  │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  FORECAST VS ACTUAL — 6-Quarter Rolling                                             │ │
│  │                                                                                     │ │
│  │  $5M ┤                                                                              │ │
│  │  $4M ┤  ██ ██    ██    ██    ██    ██                           ─── Accuracy %      │ │
│  │  $3M ┤  ■■ ■■    ■■    ■■    ■■    ■■         ●──●──●──●──●──●   (right axis)      │ │
│  │  $2M ┤                                                              80%             │ │
│  │  $1M ┤                                                              60%             │ │
│  │   $0 ┤──────────────────────────────────────────────────────────    40%             │ │
│  │       Q3'24  Q4'24  Q1'25  Q2'25  Q3'25  Q4'25                                    │ │
│  │                                                                                     │ │
│  │  ██ Commit ACV  ■■ Won ACV  ●── Forecast Accuracy %                                │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────┐  ┌───────────────────────────────────────┐  │
│  │  WIN RATE TREND by Segment            │  │  FORECAST CATEGORY FLOW              │  │
│  │                                       │  │  (selected quarter)                   │  │
│  │  50% ┤                                │  │                                       │  │
│  │  40% ┤     ──◆──Enterprise            │  │  Best Case  ████████████████  $4.1M  │  │
│  │  30% ┤  ●──●──●  Mid-Market           │  │  Commit     ████████████      $2.8M  │  │
│  │  20% ┤  ■──■──■  SMB                  │  │  Closed Won ████████          $1.9M  │  │
│  │  10% ┤                                │  │                                       │  │
│  │      Q1'25 Q2'25 Q3'25 Q4'25          │  │  Flow: Best Case → Commit → Closed   │  │
│  │                                       │  │  Movement shows forecast discipline  │  │
│  │  Reference: 50% ─ ─ ─ ─ ─ ─          │  │                                       │  │
│  └───────────────────────────────────────┘  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

## Field-to-visual mapping

| Visual element | Fields used | Calculated field |
|----------------|-------------|------------------|
| KPI — Forecast Accuracy % | ACV, IsClosed, HighestStage, IsWon, CloseQuarter | [Forecast Accuracy %] |
| KPI — Commit ACV | ACV, HighestStage, IsClosed | [Commit ACV (Historical)] |
| KPI — Won ACV | ACV, IsWon | [Won ACV] |
| KPI — Win Rate | IsWon, IsClosed (COUNT) | [Win Rate %] |
| Bar 1 (Commit) | [Commit ACV (Historical)], CloseQuarter | — |
| Bar 2 (Won) | [Won ACV], CloseQuarter | — |
| Accuracy line | IsWon, IsClosed, HighestStage | [Forecast Accuracy %] |
| Win Rate trend lines | IsWon, IsClosed, CloseQuarter, Segment | [Win Rate %] |
| Forecast flow bars | ACV, HighestStage, ForecastCategory | [Commit ACV], [Best Case ACV] |

## Notes for Tableau build

- 6-quarter rolling filter: use a relative date filter OR create a calculated field `[Last 6 Closed Quarters]` that returns true for the 6 most recent values of CloseQuarter. Sort CloseQuarter alphabetically does not work — use `[Quarter Start Date]` as the sort field.
- Dual axis on forecast vs actual: left axis = ACV bars, right axis = Accuracy % line. Synchronize axes is NOT needed (different scales). Format right axis as percentage.
- Win rate trend: filter `[IsClosed] = TRUE`. Include only complete quarters (exclude current quarter in progress).
- Forecast flow chart: this is a simplified bar chart comparing three stages' ACV. A true Sankey requires extensions. For the portfolio, use a horizontal bar chart with segment labels "% that moved from Best Case to Commit" computed as `SUM([Commit ACV]) / SUM([Best Case ACV])`.
- Quarter Selector parameter: drives the KPI row and the Forecast Category Flow chart. The rolling trend charts ignore the parameter and always show 6 most recent quarters.
```
