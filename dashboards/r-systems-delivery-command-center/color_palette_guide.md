# Tableau Color Palette Guide

Use this file with:

`r_systems_delivery_palette.tps`

## Palette Purpose

This palette is designed for the Professional Services Delivery Command Center dashboard. It is updated from RSI/R Systems visual references: deep navy and purple page sections, bright lavender calls to action, white type on dark backgrounds, and coral-red accent text for emphasis.

## Recommended Dashboard Color Assignments

| Element | Recommended Color | Hex |
|---|---|---|
| Dashboard background | Soft off-white | `#F8FAFC` |
| Dashboard outer/header band | Deep navy | `#0B1B4D` |
| Optional dark section band | Deep purple | `#24003F` |
| KPI/worksheet card background | White | `#FFFFFF` |
| Dashboard title font | White on dark header, Ink on light background | `#FFFFFF` or `#111827` |
| Subtitle/body font | Slate | `#6B7280` |
| Worksheet title font | Ink navy | `#111827` |
| Axis/header labels | Muted slate | `#6B7280` |
| Borders/dividers | Light gray | `#E5E7EB` |
| Active dashboard tab fill | Lavender | `#9B5DE5` |
| Active dashboard tab text | White | `#FFFFFF` |
| Inactive dashboard tab fill | White or very light lavender | `#FFFFFF` or `#F5ECFF` |
| Inactive dashboard tab text | Deep navy | `#0B1B4D` |
| Inactive tab border | Light lavender | `#E6D2FF` |
| Risk/exception accent | Coral red | `#FF4B6E` |

## Recommended Metric Colors

Use these consistently across the workbook.

| Metric | Line Chart Color | Bar Chart Color | Notes |
|---|---|---|---|
| Revenue | `#2F80ED` | `#2F80ED` | Strong blue reads as financial volume without implying risk |
| Gross Margin % | `#9B5DE5` | `#9B5DE5` | Lavender aligns with RSI brand visuals and works well for profitability |
| Utilization Rate | `#00A6B4` | `#00A6B4` | Cyan/teal separates capacity from financial metrics |
| Utilization Target | `#F2A900` | N/A | Use as a dashed reference line |
| Risk / late / negative variance | `#FF4B6E` | `#FF4B6E` | Use sparingly for exceptions |
| Healthy status | `#008C7A` | `#008C7A` | Use for status, not the main utilization metric if utilization already uses cyan |

For the combined trend chart:

- Revenue: `#2F80ED`
- Gross Margin %: `#9B5DE5`
- Utilization Rate: `#00A6B4`
- Target/reference line: `#F2A900`

For bar charts using the same metrics, keep the same colors. This makes the dashboard easier to learn because each metric has a stable identity.

## Included Palettes

### R Systems Delivery - Executive

Use for general categorical charts.

Recommended mapping:

| Purpose | Color |
|---|---|
| Primary ink | `#111827` |
| Deep navy | `#0B1B4D` |
| Deep purple | `#24003F` |
| RSI lavender | `#9B5DE5` |
| Light lavender | `#B26AF2` |
| Coral accent | `#FF4B6E` |
| Financial blue | `#2F80ED` |
| Capacity cyan | `#00A6B4` |
| Positive / healthy | `#008C7A` |
| Watch / medium risk | `#F2A900` |
| Muted gray | `#6B7280` |
| Divider gray | `#E5E7EB` |

### R Systems Delivery - Risk Status

Use for fields like `risk_level`, `milestone_status`, or delivery health.

Recommended mapping:

| Value | Color |
|---|---|
| Low / On Time / Healthy | `#008C7A` |
| Medium / Watch | `#F2A900` |
| High / Late / At Risk | `#FF4B6E` |
| Pending / Unknown | `#6B7280` |

### R Systems Delivery - Lines

Use for multi-line trend charts.

Recommended mapping:

| Metric | Color |
|---|---|
| Revenue | `#2F80ED` |
| Gross Margin % | `#9B5DE5` |
| Utilization % | `#00A6B4` |
| CSAT | `#008C7A` |
| NPS | `#00A6B4` |
| Target / Benchmark | `#F2A900` |

For your combined revenue, gross margin, and utilization chart, use:

- Revenue: `#2F80ED`
- Gross Margin %: `#9B5DE5`
- Utilization %: `#00A6B4`
- Target/reference line: `#F2A900`

### R Systems Delivery - Bars

Use for categorical bar charts where each bar category needs a distinct color.

Good examples:

- Revenue by service line
- CSAT by industry
- Hours by role
- Client count by strategic tier

### R Systems Delivery - Service Lines

Use when assigning fixed colors to service lines.

Recommended mapping:

| Service Line | Color |
|---|---|
| Data & AI | `#2F80ED` |
| Cloud Modernization | `#008C7A` |
| Product Engineering | `#9B5DE5` |
| CX Transformation | `#00A6B4` |
| QA Automation | `#FF4B6E` |
| DevSecOps | `#F2A900` |

### R Systems Delivery - Executive Neutral Bars

Use for ranked bars where the ranking matters more than category color.

Good examples:

- Top 10 projects by revenue
- Top clients by revenue
- Delivery team members by billable hours

Use one neutral bar color, then highlight the selected or risky item with red.

### R Systems Delivery - Sequential Red

Use for intensity charts where higher means more risk, more variance, or more delivery pressure.

Good examples:

- Late milestone count
- Budget burn %
- Non-billable rate
- Rework hours

### R Systems Delivery - Sequential Blue

Use for positive volume/intensity charts where higher is not bad.

Good examples:

- Revenue
- Billable hours
- Response count
- Project count

### R Systems Delivery - Sequential Teal

Use for health/efficiency intensity charts.

Good examples:

- Utilization rate
- Gross margin %
- CSAT
- On-time milestone rate

### R Systems Delivery - Margin Diverging

Use for positive vs negative variance.

Good examples:

- Utilization gap
- Margin variance
- Budget variance
- CSAT change

## How To Install In Tableau

1. Close Tableau Desktop.
2. Copy `r_systems_delivery_palette.tps`.
3. Paste it into your `My Tableau Repository` folder.
4. Rename it to `Preferences.tps`.
5. Reopen Tableau Desktop.
6. In a worksheet, open the color menu and choose one of the custom palettes.

If you already have a `Preferences.tps` file, do not overwrite it. Copy the `<color-palette>...</color-palette>` blocks from this file into your existing `Preferences.tps` inside the `<preferences>` section.

## Design Note For The Interview

The palette intentionally uses neutral colors for most dashboard structure and reserves saturated red, amber, and teal for interpretation. This makes color part of the data story instead of decoration.
