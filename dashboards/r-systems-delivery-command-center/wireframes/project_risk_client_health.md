# Wireframe: Project Risk & Client Health

Dashboard size: `1400 x 900`

```text
+--------------------------------------------------------------------------------------+
| Project Risk & Client Health                                      [Project] [Client] |
| Delivery predictability, budget burn, milestone health, and satisfaction [Status]     |
+--------------------------------------------------------------------------------------+
| Active Projects | At-Risk Projects | Budget Burn % | Late Milestone Rate | CSAT       |
| XX              | XX               | XX.X%         | XX.X%               | X.X        |
+--------------------------------------------------------------------------------------+
| Project Risk Matrix                                      | CSAT / NPS Trend            |
| X: Budget Burn %                                         | Line: CSAT Weighted Avg      |
| Y: CSAT Weighted Avg                                     | Bar/line: NPS Score          |
| Size: revenue                                            | by QUARTER(survey_date)      |
| Color: risk_level                                        |                              |
+----------------------------------------------------------+-----------------------------+
| Milestone Timeline                                                                     |
| Rows: project_name                                                                      |
| Columns: planned_date and actual_date markers                                           |
| Color: milestone_status                                                                 |
+--------------------------------------------------------------------------------------+
| Project Detail Table                                                                    |
| project | client | service_line | status | risk | revenue | burn % | late days | csat |
+--------------------------------------------------------------------------------------+
| Feedback Theme Breakdown                                                                |
| Bar: response_count by primary_feedback_theme; color by avg CSAT                        |
+--------------------------------------------------------------------------------------+
```

## Visual Intent

This page turns the executive story into a delivery action list. It should help a leader decide where to intervene first.

## Fields Used

- `project_id`
- `project_name`
- `client_name`
- `service_line`
- `status`
- `risk_level`
- `budget_hours`
- `budget_revenue`
- `hours`
- `revenue`
- `labor_cost`
- `milestone_name`
- `planned_date`
- `actual_date`
- `milestone_status`
- `days_late`
- `survey_date`
- `csat_score`
- `nps_score`
- `response_count`
- `primary_feedback_theme`

## Design Notes

- Use the risk matrix as the centerpiece because it combines business risk and client perception.
- Use tooltips to show project name, client, service line, revenue, burn, and CSAT.
- Use a clean milestone timeline with minimal labels.
- Avoid over-coloring the detail table; reserve color for risk and late status.

