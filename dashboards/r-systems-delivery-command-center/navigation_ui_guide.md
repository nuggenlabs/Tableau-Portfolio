# Tableau Navigation UI Guide

Use this guide to create a polished 3-dashboard navigation system for the Professional Services Delivery Command Center.

## Dashboard Pages

Use these three dashboard names in Tableau:

1. `Executive Overview`
2. `Consultant Performance`
3. `Project Risk & Client Health`

## Recommended Navigation Style

Use a horizontal tab bar across the top of every dashboard, directly below the main title.

This style works well for a portfolio review because it looks intentional, is easy to understand during a presentation, and lets you move between pages without breaking the story.

## Layout

```text
+--------------------------------------------------------------------------------------+
| Professional Services Delivery Command Center                                         |
| Revenue, utilization, delivery risk, and client satisfaction                          |
+--------------------------------------------------------------------------------------+
| [ Executive Overview ] [ Consultant Performance ] [ Project Risk & Client Health ]    |
+--------------------------------------------------------------------------------------+
| Filters                                                                              |
+--------------------------------------------------------------------------------------+
| Dashboard content                                                                     |
+--------------------------------------------------------------------------------------+
```

## Tab Design

### Active Tab

Use this style for the page the viewer is currently on:

- Fill: `#17202A`
- Text: White
- Font: Aptos Semibold, 10-11 pt
- Border: none
- Padding: 10-14 px left/right

### Inactive Tabs

Use this style for the other pages:

- Fill: `#F6F8FA`
- Text: `#566573`
- Font: Aptos, 10-11 pt
- Border: `#D6DBDF`
- Padding: 10-14 px left/right

### Hover/Selected Feeling

Tableau does not support true CSS-style hover for dashboard objects, so use strong active/inactive states. The active tab should be visually obvious.

## Recommended Labels

Keep labels short enough to scan:

- `Executive Overview`
- `Consultant Performance`
- `Project Risk & Client Health`

If space gets tight, use:

- `Overview`
- `Consultants`
- `Project Risk`

## Tableau Build Method

### Option A: Navigation Buttons

This is the fastest clean method.

1. Open the first dashboard.
2. Add a horizontal container below the title.
3. Add three `Navigation` button objects.
4. Set each button to navigate to one dashboard page.
5. Format each button to match the active/inactive tab style.
6. Copy the full navigation container to the other two dashboards.
7. On each dashboard, change the active tab styling to match the current page.

Use this if you want speed and consistency.

### Option B: Shape-Based Navigation

Use this if you want the most custom-designed look.

1. Create a small worksheet named `Nav - Executive Overview`.
2. Create one worksheet per nav item.
3. Use a calculated field for each label.
4. Format each worksheet as a single text mark.
5. Place the nav worksheets in a horizontal container.
6. Add dashboard navigation actions from each nav worksheet.

Use this if you want more visual control, but it takes longer.

## Navigation Button Setup

Create these objects on every dashboard:

| Button Label | Destination Dashboard |
|---|---|
| Executive Overview | `Executive Overview` |
| Consultant Performance | `Consultant Performance` |
| Project Risk & Client Health | `Project Risk & Client Health` |

## Active State By Dashboard

### Executive Overview

```text
[ Executive Overview ] active
[ Consultant Performance ] inactive
[ Project Risk & Client Health ] inactive
```

### Consultant Performance

```text
[ Executive Overview ] inactive
[ Consultant Performance ] active
[ Project Risk & Client Health ] inactive
```

### Project Risk & Client Health

```text
[ Executive Overview ] inactive
[ Consultant Performance ] inactive
[ Project Risk & Client Health ] active
```

## Header + Navigation Wireframe

Use this same header structure on all three dashboards.

```text
+--------------------------------------------------------------------------------------+
| Professional Services Delivery Command Center                                         |
| Delivery performance across revenue, utilization, project risk, and client health     |
+--------------------------------------------------------------------------------------+
|  Executive Overview  |  Consultant Performance  |  Project Risk & Client Health       |
+--------------------------------------------------------------------------------------+
| Date Range | Service Line | Region | Industry | Client Tier | Project Status          |
+--------------------------------------------------------------------------------------+
```

## Recommended Filter Placement

Place filters below the navigation bar, not above it.

This creates a clean hierarchy:

1. What product am I in?
2. What page am I viewing?
3. What slice of data am I filtering?
4. What insight am I reading?

## Page-Specific Subtitle

Under the main title, use a subtle page-specific subtitle.

| Dashboard | Subtitle |
|---|---|
| Executive Overview | `Executive signal across financial performance, delivery health, and client sentiment` |
| Consultant Performance | `Capacity, billability, role mix, and utilization gaps across the consulting team` |
| Project Risk & Client Health | `Milestone predictability, budget burn, satisfaction, and intervention priorities` |

## Interview Talking Point

The navigation is designed like a product UI rather than a collection of worksheets. It gives the portfolio piece a more executive, application-like feel and shows that the dashboard is built as a guided analytical experience.

The three tabs follow the user journey:

1. `Executive Overview`: What is happening?
2. `Consultant Performance`: What is driving capacity and margin?
3. `Project Risk & Client Health`: Where should leaders intervene?

