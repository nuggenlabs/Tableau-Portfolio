# Professional Services Delivery Command Center

## Portfolio Context

This is a Tableau portfolio dashboard concept tailored for a Lead Design Analyst interview with R Systems. It uses pretend/demo data to tell a professional services delivery story around project health, consultant utilization, billable hours, margin performance, and client satisfaction.

R Systems positions itself around digital product engineering, cloud, data, AI, CX, and professional services delivery. This concept is designed to feel relevant to that environment while staying clearly mock-data based.

Sources used for positioning:

- [R Systems Digital Product Engineering](https://eu.rsystems.com/digital-product-engineering/)
- [R Systems About Us](https://stageweb.rsystems.com/about-us/)

## Business Context

Consulting leaders need to balance delivery quality, revenue, utilization, margin, and client experience. A project can look healthy by revenue but still carry risk through late milestones, over-allocation, rework, low CSAT, or margin leakage.

This dashboard gives executives and delivery managers a single place to understand:

- Which projects are creating the most delivery risk
- Whether consultant capacity is being used effectively
- Where non-billable work is reducing margin
- Which service lines are strongest or weakest
- How client sentiment tracks against delivery performance

## Target Audience

- Executive leadership
- Consulting delivery directors
- Project management office
- Practice leads
- Account leaders
- Data visualization design reviewers

## Key Business Questions

- Are we meeting utilization and billability targets?
- Which service lines are driving the most revenue and margin?
- Which projects are at risk and why?
- Where are teams over-allocated or under-utilized?
- Which clients have declining satisfaction or delivery friction?
- Are late milestones connected to lower CSAT or margin leakage?

## Recommended Tableau Dashboard Pages

1. Executive Delivery Overview
   - Top-level KPIs, revenue trend, margin trend, utilization, client sentiment, and risk mix.

2. Consultant Performance & Utilization
   - Consultant-level productivity, billability, non-billable categories, utilization gaps, and skill/service-line patterns.

3. Project Risk & Client Health
   - Project drilldown with milestone status, budget burn, CSAT/NPS, delivery model, service line, and risk flags.

## Mock Data Files

All generated CSVs live in `mock_data/`.

The refreshed reporting window is recent for the portfolio scenario:

- Time entries: January 1, 2025 through May 29, 2026
- Client satisfaction surveys: March 31, 2025 through March 31, 2026
- Project starts: September 16, 2024 through February 1, 2026

- `clients.csv`
- `consultants.csv`
- `projects.csv`
- `assignments.csv`
- `time_entries.csv`
- `milestones.csv`
- `client_satisfaction.csv`

The data is deterministic. To regenerate the same dataset, run:

```powershell
& 'C:\Users\calvi\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' .\generate_mock_data.py
```

## Recommended First Step

Open `tableau_build_guide.md` first, then connect Tableau to the CSV files in `mock_data/`.
