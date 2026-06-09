# Insights and Interview Guide

## Example Insights To Look For

- High revenue does not always mean healthy delivery. Some large projects may show strong revenue but weak margin or high budget burn.
- High-risk projects often show a combination of late milestones, higher non-billable rework, and lower CSAT.
- Utilization varies by role and service line. Senior delivery talent may appear less utilized because of advisory, enablement, and oversight work.
- Non-billable work is not automatically bad. Enablement can be strategic, while rework and admin may indicate delivery friction.
- CSAT is more useful when weighted by response count because a single survey should not dominate the story.
- Service lines with strong utilization but weak margin may have rate leakage, staffing mix issues, or too much rework.

## The Why Behind The Design

### Color

I would explain that the palette is intentionally restrained. Most of the dashboard uses neutral ink, slate, and light gray so the viewer's attention is not scattered. Red is reserved for risk and negative exceptions, which makes it meaningful when it appears.

### Layout

The layout moves from signal to diagnosis to action:

1. KPI row for executive signal
2. Trend and risk visuals for diagnosis
3. Detail table and drilldown pages for action

This supports how leaders consume information in a meeting: first they need the headline, then the reason, then the next decision.

### Chart Selection

- Line charts are used for revenue, margin, CSAT, and NPS trends because time movement is the story.
- Scatterplots are used for project risk and consultant performance because they reveal outliers and tradeoffs.
- Bar charts are used for service-line comparisons because they are fast to scan.
- Tables are used only where precision and actionability matter.
- Milestone timelines are used because delivery predictability is easier to understand spatially than in a list.

### Spacing

White space is used as an executive design tool. The dashboard should look calm and deliberate, especially because the topic is operational risk. Dense data does not need to feel cluttered.

### Storytelling

The story is not "here are charts." The story is:

> Are our consulting teams delivering profitable, predictable, high-satisfaction outcomes?

Each dashboard page answers a different part of that question.

## Portfolio Talking Points

- I built this as a pretend R Systems-relevant professional services dashboard, aligned to digital engineering consulting delivery.
- I designed the data model before designing the visuals so that every wireframe element maps to a real field.
- I used different grains of data: projects, daily time entries, consultants, assignments, milestones, and quarterly satisfaction surveys.
- I intentionally included executive, manager, and operational views to show design range.
- I used Tableau-friendly calculated fields such as utilization, gross margin, budget burn, weighted CSAT, and LOD-style project metrics.
- I designed the dashboard to support presentation, not just exploration.

## Questions An Interviewer Might Ask

### Why did you choose this topic?

Because professional services delivery connects directly to consulting business performance: utilization, billability, project risk, and client satisfaction. It also gives me room to demonstrate analytical thinking and visual storytelling.

### Why these KPIs?

I chose KPIs that balance financial health, operational performance, and client experience. Revenue alone can be misleading, so I paired it with margin, utilization, CSAT, and risk.

### Why use a scatterplot for project risk?

The risk matrix lets leaders see which projects need attention first. A project with high budget burn and low CSAT is more urgent than a project with only one weak metric.

### How would you improve this with real data?

I would add forecasted backlog, actual invoices, write-offs, resource availability, project change requests, and delivery sentiment from qualitative feedback. I would also validate utilization logic with the finance and PMO teams.

### What Tableau skills does this demonstrate?

Relationships, calculated fields, LOD expressions, parameters, dashboard actions, tooltip design, visual hierarchy, and multi-page dashboard navigation.

### What design skills does this demonstrate?

Information hierarchy, spacing, color restraint, executive storytelling, chart selection, dashboard layout systems, and brand-aware visual direction.

## Suggested Presentation Flow

1. Start with the business question.
2. Explain the mock data model.
3. Show the executive overview.
4. Drill into one risk pattern.
5. Show how consultant utilization contributes to the story.
6. Explain your design choices.
7. Close with how you would adapt it for real R Systems delivery data.

## Short Portfolio Description

Professional Services Delivery Command Center is a Tableau dashboard concept built with deterministic mock data for a digital engineering consulting environment. It helps leaders monitor revenue, gross margin, utilization, project risk, milestone predictability, and client satisfaction across service lines and client segments.

