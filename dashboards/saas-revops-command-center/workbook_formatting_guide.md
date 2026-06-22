# Workbook Formatting Guide — SaaS RevOps Command Center

Reference for all font sizes, colors, and layout settings. Apply in the order listed in Quick Setup.

---

## Dashboard Size

**Dashboard pane > Size dropdown**

| Setting | Value |
|---|---|
| Size type | Fixed |
| Width | `1400 px` |
| Height | `900 px` |

---

## Color Palette

Design uses **dark chrome / light content** pattern: the tab navigation strip is dark navy for brand identity; all chart and KPI content sits on a light canvas.

This is the approved design direction for the workbook. Do not revert to a full dark-navy dashboard body. The dark navy should read as navigation chrome only; the analytic work area should stay light for readability on Tableau Public screenshots.

### Canvas & structure

| Where | Hex | Tableau setting |
|---|---|---|
| Dashboard background (canvas) | `#EEF1F8` | Dashboard > Format > Shading |
| Sheet pane background | `None` (transparent) | Format > Shading > Pane |
| Header background | `None` | Format > Shading > Header |
| KPI card container fill | `#FFFFFF` | Container > Background |
| Elevated inner areas (bar tracks, hover rows) | `#F2F5FB` | Sheet background on sub-elements |
| Container border | `#DDE4F2` | Container > Border |
| Container corner radius | `10px` | Dashboard > Format > Container (Tableau 2026.1+) |

### Tab bar / navigation chrome (dark)

| Element | Hex |
|---|---|
| Tab bar background | `#0D1B2E` |
| Active tab fill | `#EEF1F8` (matches canvas — tab "opens" into page) |
| Active tab top accent | `#6B4FFF` (2.5pt top border) |
| Tab text (inactive) | `#5E7292` |
| Tab text (active) | `#0F1C36` |

### Text scale

| Role | Hex | Usage |
|---|---|---|
| Primary (heading / values) | `#0F1C36` | KPI numbers, chart titles, table values |
| Body | `#3D4F6F` | Stage labels, table rows, filter pills |
| Secondary | `#8492B0` | Axis labels, column headers, sub-labels |
| Muted | `#A0ABC5` | Legends, descriptions, timestamps |

### Semantic (data) colors

| Signal | Hex | When to use |
|---|---|---|
| Indigo / brand | `#6B4FFF` | CN accent, KPI card left border, filter values |
| Teal / positive | `#00A87A` | On track, above target, positive variance |
| Red / alert | `#D63344` | At risk, below target, negative variance |
| Amber / caution | `#E59300` | Monitor, approaching threshold |
| Blue / neutral data | `#1B96FF` | Neutral bar series, non-semantic data |

> Color carries meaning — never use red/teal/amber decoratively. The indigo left border on KPI cards is the only decorative use of brand color.

---

## Workbook Default Font

**Format > Workbook**

| Setting | Value |
|---|---|
| Font family | `Tableau Book` (fallback: `Segoe UI`) |
| Default size | `10pt` |
| Default color | `#0F1C36` |
| Default background | `#EEF1F8` |

Set this first — it cascades to all sheets.

---

## Font Sizes — Complete Reference

All sizes in **points (pt)**. These are calibrated for 1400 × 900 at standard screen scaling. Tableau pt sizes render smaller than equivalent HTML px — do not copy HTML pixel values directly.

### Tab bar & chrome

| Element | Size | Style | Color |
|---|---|---|---|
| Workbook title | `9pt` | Bold, uppercase, tracked | `#5E7292` |
| Tab label (inactive) | `9pt` | Semibold | `#5E7292` |
| Tab label (active) | `9pt` | Semibold | `#0F1C36` |

### Filter bar

| Element | Size | Style | Color |
|---|---|---|---|
| Filter pill label | `9pt` | Regular | `#3D4F6F` |
| Filter pill value | `9pt` | Bold | `#6B4FFF` |
| Data freshness note | `8pt` | Regular | `#A0ABC5` |

### KPI cards

| Element | Size | Style | Color |
|---|---|---|---|
| KPI label (metric name) | `8pt` | Bold, ALL CAPS via Format | `#8492B0` |
| KPI value (primary number) | `26pt` | Semibold | `#0F1C36` |
| KPI sub-label ("total ACV", "per week") | `8pt` | Regular | `#A0ABC5` |
| KPI delta (↑ / ↓ variance) | `10pt` | Regular | `#00A87A` or `#D63344` |
| KPI card accent border (left) | `3pt` | — | `#6B4FFF` (alert cards: `#D63344`) |

### Chart titles & labels

| Element | Size | Style | Color |
|---|---|---|---|
| Chart title (sheet title) | `11pt` | Semibold | `#0F1C36` |
| Chart subtitle / description | `9pt` | Regular | `#8492B0` |
| Axis labels (tick values) | `9pt` | Regular | `#8492B0` |
| Axis title | `8pt` or hide | Regular | `#A0ABC5` |
| Reference line label | `9pt` | Regular | semantic |

### In-chart text

| Element | Size | Style | Color |
|---|---|---|---|
| Bar / mark labels | `9pt` | Regular | `#0F1C36` or semantic |
| Coverage scorecard cell value | `12–14pt` | Bold | semantic (teal / amber / red) |
| Coverage scorecard status label | `6–7pt` | Bold, uppercase | `#6C7B96` |
| Coverage scorecard header | `8pt` | Bold, uppercase | `#8492B0` |
| Stage duration day value | `9pt` | Bold | semantic |
| Stage duration status (OVER/OK) | `8pt` | Bold | semantic |
| Funnel stage label | `9pt` | Regular | `#3D4F6F` |
| Funnel count / ACV column | `9pt` | Bold | `#0F1C36` / `#3D4F6F` |
| Conversion rate label | `8pt` | Regular uppercase | `#A0ABC5` |
| Conversion rate value | `9pt` | Bold | semantic or `#3D4F6F` |

### Tables

| Element | Size | Style | Color |
|---|---|---|---|
| Table header row | `8pt` | Bold, uppercase | `#8492B0` |
| Table body — general columns | `9pt` | Regular | `#3D4F6F` |
| Table body — rep name / ACV (emphasis) | `10pt` | Semibold | `#0F1C36` |
| Days badge text | `9pt` | Bold | semantic |
| Divider line | `0.5pt` | — | `#DDE4F2` |

### Legend & tooltip

| Element | Size | Style | Color |
|---|---|---|---|
| Legend item | `9pt` | Regular | `#8492B0` |
| Tooltip body | `10pt` | Regular | `#0F1C36` |
| Tooltip header | `10pt` | Semibold | `#0F1C36` |

> Tableau tooltip background is always white — no workaround exists in Desktop. Use `#0F1C36` text color for readability on the white tooltip background.

---

## Axis Formatting

**Right-click axis > Format**

| Element | Size | Color |
|---|---|---|
| Axis title | `8pt` or hide | `#A0ABC5` |
| Axis labels (tick values) | `9pt` | `#8492B0` |
| Axis ruler | `0.5pt solid` | `#DDE4F2` |
| Grid lines | `0.5pt` | `#EEF1F8` |
| Zero line | `1pt solid` | `#DDE4F2` |

---

## Borders and Lines

**Format > Lines** (per sheet)

| Element | Setting |
|---|---|
| Row dividers | None |
| Column dividers | None |
| Sheet border | None |
| Reference lines | `1pt dashed`, semantic color |
| Table row dividers | `0.5pt`, `#DDE4F2` |

---

## Mark Labels

**Label shelf** (per sheet)

| Setting | Value |
|---|---|
| Font | `9pt`, regular |
| Color on colored bars | `#FFFFFF` |
| Color on light backgrounds | `#0F1C36` |
| Visibility | On for KPI sheets and bar-end labels only — off on trend lines |

---

## Layout Hierarchy

Each tab should have one dominant analytic object. Avoid making every chart card the same size and weight.

| Tab | Primary visual | Supporting visuals |
|---|---|---|
| Pipeline Health | Pipeline Coverage by Segment | Open Pipeline by Stage, Avg Days in Stage, Stalled Deals action queue |
| Forecast Accuracy | Forecast vs Actual — 6-quarter rolling | Win Rate Trend, Forecast Category Flow |
| ARR Performance | ARR Waterfall — Net New ARR by Quarter | GRR/NRR Trend, Closed ARR Mix |

### Tab 1 recommended proportions

Use the `tab1_mockup_v3.html` composition as the build reference:

- KPI row: 4 cards across the top
- Hero row: Pipeline Coverage takes roughly 60% of the width; Open Pipeline by Stage takes roughly 40%
- Inside the Pipeline Coverage card, reserve roughly 25% of the card width for the Manager Focus panel
- Secondary row: Avg Days in Stage and Stalled Deals Requiring Follow-Up split evenly
- The stalled deals table is an action queue, not the main story. Keep it visually lighter than the coverage scorecard.

### Manager Focus panel

| Element | Setting |
|---|---|
| Panel fill | `#F2F5FB` |
| Panel border | `#DDE4F2` |
| Panel corner radius | `8px` |
| Inner padding | `12px` |
| Eyebrow label | `8pt`, bold, uppercase, `#8492B0` |
| Main count | `26–30pt`, bold, red if any visible combos are At Risk, teal if none are At Risk |
| Narrative | `9pt`, regular, `#3D4F6F` |
| Segment average labels | `9–10pt`, regular, `#3D4F6F` |
| Segment average values | `9–10pt`, bold, `#0F1C36` |

---

## Custom Shape Badges

Pipeline Coverage should use rounded badge shapes instead of Tableau's default square where possible.

Shape assets:
- `tableau_shapes/pipeline_badges/coverage-badge-at-risk-blank.png`
- `tableau_shapes/pipeline_badges/coverage-badge-monitor-blank.png`
- `tableau_shapes/pipeline_badges/coverage-badge-on-track-blank.png`
- `tableau_shapes/pipeline_badges/coverage-badge-neutral-blank.png`

Tableau setup:
1. Copy the blank PNG files to `Documents\My Tableau Repository\Shapes\SaaS RevOps\Pipeline Badges`.
2. Set the Pipeline Coverage scorecard mark type to Shape.
3. Assign the badge shape by `[Coverage Status]`.
4. Put the dynamic coverage value and status text on Label.
5. Center-align the label over the shape.

Use the sample PNG files only for visual reference. Do not use sample files with baked-in numbers for the real worksheet.

Recommended badge colors:

| Status | Fill | Border | Value text |
|---|---|---|---|
| On Track | `#EAF8F4` | `#8CD8C4` | `#00A87A` |
| Monitor | `#FFF6E6` | `#F4C56A` | `#E59300` |
| At Risk | `#FBEDEF` | `#F2B8BE` | `#D63344` |

---

## Quick Setup Order

Follow this sequence at the start of every new workbook before building any sheets.

1. **Format > Workbook** — font: `Tableau Book`, size: `10pt`, color: `#0F1C36`, background: `#EEF1F8`
2. **Dashboard > Size** — `1400 × 900` fixed
3. Set dashboard canvas background to `#EEF1F8`
4. Per sheet: **Format > Shading** — pane: transparent, header: transparent
5. Per sheet: **Format > Lines** — remove row/column dividers, remove sheet border
6. Per sheet: **Worksheet > Tooltip** — font `10pt`, color `#0F1C36`, command buttons off
7. After layout: KPI container fill `#FFFFFF`, border `#DDE4F2`, corner radius `10px`
8. KPI card left border accent: `3pt solid #6B4FFF` (alert cards: `#D63344`)
9. Install custom badge shapes before building Tab 1 Pipeline Coverage
10. Build Tab 1 with Pipeline Coverage as the hero visual, not the funnel
