# Wireframe — Tab 3: ARR Performance
# Dashboard: 1400 × 900 · dark chrome / light content canvas

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  SAAS REVOPS COMMAND CENTER                                  [Tab 1] [Tab 2] [Tab 3]    │
│  ARR Performance                                                                         │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│  FILTERS  [Segment ▾ All]  [ARR Type ▾ All]  [Region ▾ All]                           │
├───────────────────┬───────────────────┬───────────────────┬───────────────────────────  │
│  NET NEW ARR      │  NRR              │  GRR              │  CHURN ARR                  │
│  (last 8 qtrs)    │  (trailing 4 qtrs)│  (trailing 4 qtrs)│  (last 8 qtrs)             │
│  $26.7M           │  118%             │  91%              │  -$1.2M                     │
│  cumulative       │  net retention    │  gross retention  │  lost renewals              │
├───────────────────┴───────────────────┴───────────────────┴───────────────────────────  │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  ARR WATERFALL — Net New ARR by Quarter                                             │ │
│  │                                                                                     │ │
│  │  $5M ┤                                                                              │ │
│  │  $4M ┤         ████  ████                   ████                                   │ │
│  │  $3M ┤  ████  ▓▓▓▓  ▓▓▓▓  ████  ████  ████  ▓▓▓▓  ████  ─── cumulative ARR       │ │
│  │  $2M ┤  ▓▓▓▓  ████  ████  ▓▓▓▓  ▓▓▓▓  ▓▓▓▓  ████  ▓▓▓▓                           │ │
│  │  $1M ┤                     ▒▒▒▒  ▒▒▒▒  ▒▒▒▒        ▒▒▒▒                           │ │
│  │  $0  ┤──────────────────────────────────────────────────────────────────────────── │ │
│  │ -$1M ┤         ░░░░               ░░░░  ░░░░  ░░░░                                 │ │
│  │       Q1'24 Q2'24 Q3'24 Q4'24 Q1'25 Q2'25 Q3'25 Q4'25                             │ │
│  │                                                                                     │ │
│  │  ████ New ARR  ▓▓▓▓ Expansion ARR  ▒▒▒▒ Renewal  ░░░░ Churn (negative)            │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────┐  ┌───────────────────────────────────────┐  │
│  │  GRR & NRR TREND                      │  │  CLOSED ARR MIX by Segment           │  │
│  │                                       │  │                                       │  │
│  │  130% ┤           ●──●  NRR           │  │  $5M ┤ ████ ████ ████ ████ ████ ████  │  │
│  │  120% ┤  ●──●──●         ●            │  │  $4M ┤ ████ ████ ████ ████ ████ ████  │  │
│  │  110% ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─        │  │  $3M ┤ ▓▓▓▓ ▓▓▓▓ ▓▓▓▓ ▓▓▓▓ ▓▓▓▓ ▓▓▓▓ │  │
│  │  100% ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ Brkevn │  │  $2M ┤ ▒▒▒▒ ▒▒▒▒ ▒▒▒▒ ▒▒▒▒ ▒▒▒▒ ▒▒▒▒ │  │
│  │   90% ┤  ■──■──■──■──■──■  GRR        │  │  $1M ┤                               │  │
│  │   80% ┤                               │  │   $0 ┤                               │  │
│  │        Q1  Q2  Q3  Q4  Q1  Q2         │  │      Q3'24 Q4'24 Q1'25 Q2'25 Q3'25 Q4│  │
│  │        '24 '24 '24 '24 '25 '25        │  │                                       │  │
│  │                                       │  │  ████ Enterprise  ▓▓▓▓ Mid-Market     │  │
│  │  ─ ─ = Breakeven (100%)              │  │  ▒▒▒▒ SMB                             │  │
│  │  shading above 110% = healthy zone    │  │  (stacked, % label on hover)          │  │
│  └───────────────────────────────────────┘  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

## Field-to-visual mapping

| Visual element | Fields used | Calculated field |
|----------------|-------------|------------------|
| KPI — Net New ARR | ACV, IsWon, ARRType, IsClosed | [Net New ARR] |
| KPI — NRR | ACV, ARRType, IsWon, IsClosed | [NRR %] |
| KPI — GRR | ACV, ARRType, IsWon, IsClosed | [GRR %] |
| KPI — Churn ARR | ACV, ARRType, IsClosed | [Churn ARR] |
| Waterfall New bar | ACV, ARRType=New, IsWon=true | [New ARR] |
| Waterfall Expansion bar | ACV, ARRType=Expansion, IsWon=true | [Expansion ARR] |
| Waterfall Renewal bar | ACV, ARRType=Renewal, IsWon=true | [Renewal ARR] |
| Waterfall Churn bar | ACV, ARRType=Churn, IsClosed=true | [Churn ARR] (negative) |
| Cumulative ARR line | CloseQuarter, [Net New ARR] | RUNNING_SUM([Net New ARR]) |
| GRR line | CloseQuarter, ARRType, IsWon | [GRR %] |
| NRR line | CloseQuarter, ARRType, IsWon | [NRR %] |
| Segment mix bars | ACV, IsWon, Segment, CloseQuarter | [Won ACV] |

## Notes for Tableau build

### ARR Waterfall technique (Gantt bar)
1. Create a calculated field `[Waterfall Value]`:
   ```
   SUM([New ARR]) + SUM([Expansion ARR]) + SUM([Renewal ARR]) + SUM([Churn ARR])
   ```
2. Drag `[CloseQuarter]` to Columns. Drag `[ARR Waterfall Type]` also to Columns (nested).
3. Mark type: Gantt Bar.
4. Drag `[Waterfall Value]` to Rows for the bar height.
5. Create `[Waterfall Start]` using PREVIOUS_VALUE table calc to set the Gantt offset.
6. Simplest alternative: use a stacked bar with New/Expansion as positive and Churn as a negative measure. In Tableau, negative values in a stacked bar create the hanging-below-zero visual naturally. This is easier to build and still reads correctly.

### Color encoding for waterfall
- New ARR: `#008C7A` (teal)
- Expansion ARR: `#5B6ABF` (indigo)
- Renewal ARR: `#A0ABBA` (neutral gray — retained, not growth)
- Churn: `#C0392B` (red, rendered below zero)

### GRR/NRR line chart
- Reference line at 100%: label "Breakeven", color `#A0ABBA`
- Reference band: fill above 110% with `rgba(0, 140, 122, 0.12)` (very subtle teal)
- Y axis range: 70% – 135%
- Format both as percentage with 0 decimal places

### Segment mix
- Stacked bar, `[Won ACV]` on Rows, `[CloseQuarter]` on Columns, `[Segment]` on Color
- Add a percent of total table calc as a label (compute using: Pane Down)
- Enterprise = `#1A3A5C`, Mid-Market = `#2E6EA6`, SMB = `#5B9BD5` (blue gradient)

### Filter behavior
- The Segment filter on this tab should filter ALL sheets on the tab simultaneously
- ARR Type filter filters the waterfall and mix chart but NOT the GRR/NRR lines (which compute ratios internally)
- Use "Apply to Worksheets → Selected Worksheets" to control this precisely
```
