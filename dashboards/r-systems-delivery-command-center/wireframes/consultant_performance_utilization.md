# Wireframe: Consultant Performance & Utilization

Dashboard size: `1400 x 900`

```text
+--------------------------------------------------------------------------------------+
| Consultant Performance & Utilization                                  [Date] [Role]  |
| Capacity, billability, non-billable work, and skill mix                [Skill] [Level]|
+--------------------------------------------------------------------------------------+
| Consultants    | Billable Hours | Non-Billable Hours | Avg Utilization | Avg Bill Rate|
| XXX            | XX,XXX         | X,XXX              | XX.X%           | $XXX/hr      |
+--------------------------------------------------------------------------------------+
| Utilization vs Margin Scatter                          | Non-Billable Hours by Type   |
| X: Utilization Rate                                    | Bar: SUM(non_billable_hours) |
| Y: Gross Margin %                                      | by entry_type                |
| Size: billable_hours                                   | color by entry_type          |
| Color: utilization gap                                 |                             |
+--------------------------------------------------------+-----------------------------+
| Utilization by Role and Level                          | Skill Mix by Service Line    |
| Heatmap: role x level                                  | Stacked bar or highlight     |
| Color: Utilization Rate                                | table using primary_skill    |
+--------------------------------------------------------+-----------------------------+
| Consultant Detail Table                                                              |
| consultant_name | role | level | primary_skill | billable hrs | utilization | margin % |
| Sorted by utilization gap or billable hours                                           |
+--------------------------------------------------------------------------------------+
```

## Visual Intent

This page shows whether the consulting workforce is being used effectively without reducing people to a single metric. It balances utilization, margin, skill mix, and non-billable work.

## Fields Used

- `consultant_id`
- `consultant_name`
- `role`
- `level`
- `primary_skill`
- `service_line`
- `hours`
- `billable_hours`
- `non_billable_hours`
- `entry_type`
- `revenue`
- `labor_cost`
- `bill_rate`
- `cost_rate`
- `utilization_target`

## Design Notes

- Use a scatterplot because it reveals outliers better than a simple rank table.
- Use the detail table for actionability.
- Add a reference line at the utilization target.
- Color consultants below target in amber/red and above target in teal.

