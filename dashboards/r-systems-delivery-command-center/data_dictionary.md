# Data Dictionary

## Relationship Model

Recommended Tableau relationship model:

- `clients.client_id` to `projects.client_id`
- `projects.project_id` to `assignments.project_id`
- `consultants.consultant_id` to `assignments.consultant_id`
- `projects.project_id` to `time_entries.project_id`
- `consultants.consultant_id` to `time_entries.consultant_id`
- `projects.project_id` to `milestones.project_id`
- `clients.client_id` to `client_satisfaction.client_id`
- `projects.project_id` to `client_satisfaction.project_id`

Use relationships instead of physical joins where possible so Tableau can preserve each table's grain.

## clients.csv

| Field | Type | Tableau Role | Description | Suggested Format |
|---|---|---|---|---|
| client_id | String | Dimension | Unique client identifier | Text |
| client_name | String | Dimension | Client organization name | Text |
| industry | String | Dimension | Client industry vertical | Text |
| client_region | String | Geographic/Dimension | Client region | Text |
| strategic_tier | String | Dimension | Enterprise, Growth, or Emerging client tier | Text |
| account_owner | String | Dimension | Internal account owner | Text |

## consultants.csv

| Field | Type | Tableau Role | Description | Suggested Format |
|---|---|---|---|---|
| consultant_id | String | Dimension | Unique consultant identifier | Text |
| consultant_name | String | Dimension | Consultant name | Text |
| role | String | Dimension | Delivery role | Text |
| level | String | Dimension | Career level | Text |
| home_region | String | Geographic/Dimension | Consultant home region | Text |
| primary_skill | String | Dimension | Primary skill or capability | Text |
| bill_rate | Number | Measure | Standard bill rate per hour | Currency |
| cost_rate | Number | Measure | Labor cost rate per hour | Currency |
| utilization_target | Number | Measure | Expected utilization rate | Percentage |
| hire_date | Date | Date | Consultant hire date | yyyy-mm-dd |

## projects.csv

| Field | Type | Tableau Role | Description | Suggested Format |
|---|---|---|---|---|
| project_id | String | Dimension | Unique project identifier | Text |
| project_name | String | Dimension | Project display name | Text |
| client_id | String | Dimension | Related client ID | Text |
| service_line | String | Dimension | Delivery capability | Text |
| project_type | String | Dimension | Type of engagement | Text |
| delivery_model | String | Dimension | Onsite, Remote, or Hybrid | Text |
| project_region | String | Geographic/Dimension | Project region | Text |
| start_date | Date | Date | Project start date | yyyy-mm-dd |
| planned_end_date | Date | Date | Planned project end date | yyyy-mm-dd |
| actual_or_forecast_end_date | Date | Date | Actual or forecasted end date | yyyy-mm-dd |
| status | String | Dimension | Current project status | Text |
| budget_hours | Number | Measure | Approved delivery budget in hours | Number |
| budget_revenue | Number | Measure | Approved revenue budget | Currency |
| risk_level | String | Dimension | Low, Medium, or High delivery risk | Text |

## assignments.csv

| Field | Type | Tableau Role | Description | Suggested Format |
|---|---|---|---|---|
| assignment_id | String | Dimension | Unique assignment identifier | Text |
| project_id | String | Dimension | Related project ID | Text |
| consultant_id | String | Dimension | Related consultant ID | Text |
| allocation_pct | Number | Measure | Planned allocation percentage | Percentage |
| assignment_role | String | Dimension | Role assigned on the project | Text |
| assigned_start_date | Date | Date | Assignment start date | yyyy-mm-dd |
| assigned_end_date | Date | Date | Assignment end date | yyyy-mm-dd |

## time_entries.csv

| Field | Type | Tableau Role | Description | Suggested Format |
|---|---|---|---|---|
| time_entry_id | String | Dimension | Unique time entry identifier | Text |
| entry_date | Date | Date | Work date | yyyy-mm-dd |
| project_id | String | Dimension | Related project ID | Text |
| consultant_id | String | Dimension | Related consultant ID | Text |
| hours | Number | Measure | Total submitted hours | Number, 1 decimal |
| billable_hours | Number | Measure | Billable delivery hours | Number, 1 decimal |
| non_billable_hours | Number | Measure | Non-billable hours | Number, 1 decimal |
| entry_type | String | Dimension | Billable Delivery, Internal, Enablement, Rework, or Admin | Text |
| bill_rate | Number | Measure | Bill rate applied to entry | Currency |
| cost_rate | Number | Measure | Cost rate applied to entry | Currency |
| revenue | Number | Measure | Entry revenue | Currency |
| labor_cost | Number | Measure | Entry labor cost | Currency |

## milestones.csv

| Field | Type | Tableau Role | Description | Suggested Format |
|---|---|---|---|---|
| milestone_id | String | Dimension | Unique milestone identifier | Text |
| project_id | String | Dimension | Related project ID | Text |
| milestone_name | String | Dimension | Delivery milestone | Text |
| planned_date | Date | Date | Planned milestone date | yyyy-mm-dd |
| actual_date | Date | Date | Actual milestone date, blank if pending | yyyy-mm-dd |
| milestone_status | String | Dimension | On Time, Late, or Pending | Text |
| days_late | Number | Measure | Number of days late | Number |

## client_satisfaction.csv

| Field | Type | Tableau Role | Description | Suggested Format |
|---|---|---|---|---|
| survey_id | String | Dimension | Unique survey identifier | Text |
| survey_date | Date | Date | Survey date | yyyy-mm-dd |
| client_id | String | Dimension | Related client ID | Text |
| project_id | String | Dimension | Related project ID | Text |
| csat_score | Number | Measure | Client satisfaction score from 1 to 10 | Number, 1 decimal |
| nps_score | Number | Measure | Net promoter score | Number |
| response_count | Number | Measure | Number of survey responses | Number |
| primary_feedback_theme | String | Dimension | Main client feedback theme | Text |

## Recommended Calculated Fields

| Field Name | Tableau Formula | Purpose |
|---|---|---|
| Utilization Rate | `SUM([billable_hours]) / SUM([hours])` | Measures how much submitted time is billable |
| Non-Billable Rate | `SUM([non_billable_hours]) / SUM([hours])` | Shows margin leakage and enablement load |
| Gross Margin | `SUM([revenue]) - SUM([labor_cost])` | Calculates project or service-line margin |
| Gross Margin % | `(SUM([revenue]) - SUM([labor_cost])) / SUM([revenue])` | Normalizes profitability |
| Average Bill Rate | `SUM([revenue]) / SUM([billable_hours])` | Shows realized bill rate |
| Budget Burn % | `SUM([hours]) / SUM([budget_hours])` | Measures delivery consumption against budget |
| Revenue Attainment % | `SUM([revenue]) / SUM([budget_revenue])` | Compares earned revenue to budget |
| Late Milestone Rate | `SUM(IF [milestone_status] = "Late" THEN 1 ELSE 0 END) / COUNT([milestone_id])` | Tracks delivery predictability |
| High Risk Project Count | `COUNTD(IF [risk_level] = "High" THEN [project_id] END)` | Executive risk KPI |
| CSAT Weighted Avg | `SUM([csat_score] * [response_count]) / SUM([response_count])` | Weights satisfaction by response volume |
| Project Duration Days | `DATEDIFF('day', [start_date], [actual_or_forecast_end_date])` | Supports duration analysis |
| On-Time Flag | `IF [milestone_status] = "On Time" THEN 1 ELSE 0 END` | Enables milestone completion summaries |

