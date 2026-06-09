# Tableau Build Guide

## Dashboard Name

Professional Services Delivery Command Center

## Dashboard Size

Use `1400 x 900` for desktop portfolio presentation. Create a simplified phone layout only if you want to demonstrate responsive thinking.

## Data Connection

Connect Tableau to the CSV files in `mock_data/`.

Recommended relationship canvas:

1. Add `projects.csv` as the central table.
2. Relate `clients.csv` on `client_id`.
3. Relate `time_entries.csv` on `project_id`.
4. Relate `consultants.csv` to `time_entries.csv` on `consultant_id`.
5. Relate `assignments.csv` to `projects.csv` on `project_id`.
6. Relate `milestones.csv` to `projects.csv` on `project_id`.
7. Relate `client_satisfaction.csv` to `projects.csv` on `project_id`.

Avoid joining all tables physically into one flat table. The grains are different: time entries are daily, milestones are project-milestone level, satisfaction is quarterly survey level, and projects are engagement level.

## Design System

### Visual Tone

Use a high-end consulting operations look: calm, precise, executive, and analytical.

### Color Palette

- Ink: `#17202A`
- Slate: `#566573`
- Cloud: `#F6F8FA`
- Line Gray: `#D6DBDF`
- R Systems-inspired Red Accent: `#D71920`
- Teal Success: `#008C7A`
- Amber Watch: `#F2A900`
- Risk Red: `#C0392B`

Use red only for risk, negative variance, and selected emphasis. Let neutral colors do most of the work.

### Typography

- Dashboard title: 24-28 pt, semibold
- Page section headers: 13-15 pt, semibold, uppercase optional
- KPI values: 24-32 pt, semibold
- KPI labels: 9-10 pt, muted gray
- Axis labels: 8-9 pt
- Tooltip labels: 9-10 pt

### Layout Rules

- Place filters in a single top bar or left rail.
- Use 4-5 KPI cards across the top.
- Keep chart titles short and action-oriented.
- Use color sparingly; avoid rainbow categorical palettes.
- Align edges precisely.
- Keep white space around KPI groups so the dashboard feels designed, not assembled.

## Dashboard 1: Executive Delivery Overview

### KPI Cards

- Revenue: `SUM([revenue])`
- Gross Margin %: `[Gross Margin %]`
- Utilization Rate: `[Utilization Rate]`
- Weighted CSAT: `[CSAT Weighted Avg]`
- High Risk Projects: `[High Risk Project Count]`

### Visuals

- Monthly revenue and gross margin trend
- Utilization rate by service line
- Monthly utilization vs target
- Project risk mix
- CSAT by industry or strategic tier
- Top 10 projects by revenue with margin and risk indicator

### Filters

- Date range using `entry_date`
- Service line
- Client region
- Industry
- Strategic tier
- Project status

### Dashboard Actions

- Click a service line to filter all project and client visuals.
- Click a project in the top 10 table to navigate to Project Risk & Client Health.
- Use highlight action from risk mix to highlight matching projects.

### Utilization KPI Support Visual

Add a small line chart titled `Monthly Utilization vs Target`.

Use:

- Columns: `MONTH([entry_date])`
- Rows: `[Utilization Rate]`
- Reference line: `0.80` or the `Utilization Target Override` parameter
- Color: teal when above target, amber/red when below target if you create a target gap calculation

This visual supports the top-level utilization KPI by showing whether utilization is consistently healthy or only elevated because of a few strong months.

## Dashboard 2: Consultant Performance & Utilization

### KPI Cards

- Total Consultants: `COUNTD([consultant_id])`
- Billable Hours: `SUM([billable_hours])`
- Non-Billable Hours: `SUM([non_billable_hours])`
- Average Utilization: `[Utilization Rate]`
- Average Bill Rate: `[Average Bill Rate]`

### Visuals

- Consultant utilization scatterplot: utilization rate vs gross margin
- Ranked consultant table with billable hours, utilization, primary skill, service line, and margin
- Non-billable hours by entry type
- Utilization by role and level
- Skill mix by service line

### Parameters

Create parameter: `Utilization Target Override`

- Data type: Float
- Current value: `0.80`
- Display format: Percentage
- Range: `0.60` to `0.95`

Calculated field:

```tableau
Utilization Gap
[Utilization Rate] - [Utilization Target Override]
```

Use this to color utilization views.

## Dashboard 3: Project Risk & Client Health

### KPI Cards

- Active Projects: `COUNTD(IF [status] = "Active" THEN [project_id] END)`
- At-Risk Projects: `COUNTD(IF [status] = "At Risk" THEN [project_id] END)`
- Budget Burn %: `[Budget Burn %]`
- Late Milestone Rate: `[Late Milestone Rate]`
- Weighted CSAT: `[CSAT Weighted Avg]`

### Visuals

- Project risk matrix: budget burn % vs CSAT, colored by risk level, sized by revenue
- Milestone timeline by project
- Project detail table with status, risk, budget burn, revenue, margin, CSAT, and late milestones
- CSAT/NPS trend by quarter
- Feedback theme breakdown

### Advanced Tableau Features To Demonstrate

- LOD expression for project-level revenue:

```tableau
{ FIXED [project_id] : SUM([revenue]) }
```

- LOD expression for project-level CSAT:

```tableau
{ FIXED [project_id] : SUM([csat_score] * [response_count]) / SUM([response_count]) }
```

- Parameter-driven target line for utilization.
- Navigation buttons between dashboard pages.
- Viz-in-tooltip for project milestone details.
- Set action or filter action for selecting high-risk service lines.

## Tooltip Structure

Use concise business-language tooltips.

Example project tooltip:

```text
Project: <Project Name>
Client: <Client Name>
Service Line: <Service Line>
Revenue: <SUM Revenue>
Gross Margin %: <Gross Margin %>
Budget Burn %: <Budget Burn %>
CSAT: <CSAT Weighted Avg>
Risk Level: <Risk Level>
```

## Formatting Notes

- Revenue: `$#,##0`
- Hours: `#,##0.0`
- Rates: `$#,##0/hr`
- Percentages: `0.0%`
- CSAT: `0.0`
- NPS: `#,##0`

## Portfolio Presentation Angle

When presenting, explain that the design intentionally separates:

- Executive signal: top KPIs and risk trend
- Diagnosis: service line, utilization, and margin patterns
- Action: project and consultant drilldowns

This shows you can design for decision-making, not just display charts.
