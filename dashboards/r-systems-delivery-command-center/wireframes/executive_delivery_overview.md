# Wireframe: Executive Delivery Overview

Dashboard size: `1400 x 900`

```text
+--------------------------------------------------------------------------------------+
| Professional Services Delivery Command Center                         [Date] [Region] |
| Revenue, utilization, margin, project risk, and client health          [Service Line] |
+--------------------------------------------------------------------------------------+
| Revenue        | Gross Margin % | Utilization % | Weighted CSAT | High Risk Projects |
| $XX.XM         | XX.X%          | XX.X%         | X.X           | XX                 |
+--------------------------------------------------------------------------------------+
| Monthly Revenue + Margin Trend                         | Project Risk Mix             |
| Line: SUM(revenue) by MONTH(entry_date)                 | Donut or stacked bar         |
| Line or dual axis: Gross Margin %                       | COUNTD(project_id), risk     |
|                                                        | color by risk_level          |
+--------------------------------------------------------+-----------------------------+
| Utilization by Service Line                             | CSAT by Industry             |
| Bar: Utilization Rate by service_line                   | Dot/bar: CSAT Weighted Avg   |
| Reference line: target                                  | by industry                  |
+--------------------------------------------------------+-----------------------------+
| Monthly Utilization vs Target                           | Optional Margin Leakage      |
| Line: Utilization Rate by MONTH(entry_date)             | Bar: non_billable_hours      |
| Reference line: 80% target                              | by entry_type                |
+--------------------------------------------------------+-----------------------------+
| Top 10 Delivery Engagements                                                           |
| project_name | client_name | service_line | revenue | margin % | budget burn % | risk |
| Sorted by revenue; risk shown as small colored status mark                            |
+--------------------------------------------------------------------------------------+
```

## Visual Intent

This page should read like an executive command center. The viewer should understand the business in the first 10 seconds: revenue, margin, utilization, satisfaction, and risk.

## Fields Used

- `entry_date`
- `revenue`
- `labor_cost`
- `hours`
- `billable_hours`
- `non_billable_hours`
- `entry_type`
- `project_id`
- `project_name`
- `client_name`
- `service_line`
- `industry`
- `risk_level`
- `budget_hours`
- `csat_score`
- `response_count`

## Design Notes

- Use neutral KPI cards with one red accent only on high-risk projects.
- Put the most important trend in the largest panel.
- Use the same risk colors everywhere: low teal, medium amber, high red.
- Keep gridlines light or off.
- Use a clear title and subtitle so the dashboard feels intentional.
