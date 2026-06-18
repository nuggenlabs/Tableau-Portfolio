# CLAUDE.md — Tableau Portfolio Project Context

## What This Project Is

This is Calvin Nguyen's Tableau Public portfolio repository. It contains source materials for dashboard builds published at public.tableau.com — mock data, wireframes, build guides, and design assets. Each dashboard is a portfolio piece demonstrating real analytics use cases with synthetic data.

This is NOT a career management repository. Resumes, job applications, and career strategy live in a separate project (Career-Master-Profile).

---

## Who Calvin Is

**Calvin Nguyen** — Tableau Certified Architect (highest Tableau certification), Analytics Consultant and Manager at Accelerize360 (2023–2026). 6+ years across healthcare analytics (Cerner/Oracle), revenue operations, and Tableau consulting delivery across industries including military housing, health insurance, automotive F&I, telecom retail, and manufacturing.

**Personal brand:** CN — logo mark using purple/teal palette on dark navy background.

**Certifications:**
- Tableau Certified Architect
- Tableau Consultant
- Tableau Data Analyst
- Tableau Desktop Specialist
- Salesforce Data Cloud Consultant

**Tool honesty rules — never overclaim:**
- SQL: intermediate level only
- Power BI: basic exposure (learned during client escalation)
- Python: not a primary skill — used for data generation scripts with AI assistance
- SAS / R: academic/limited exposure only
- Epic / VBC: no experience

---

## Repository Structure

```
Tableau-Portfolio/
  dashboards/
    [dashboard-folder-name]/     ← one folder per dashboard
      README.md                  ← business context, audience, key questions
      tableau_build_guide.md     ← step-by-step Tableau build instructions
      data_dictionary.md         ← field definitions, types, Tableau roles
      insights_guide.md          ← talking points, interview prep, example insights
      wireframes/                ← ASCII/markdown layout wireframes per tab
      mock_data/                 ← CSV files for Tableau connection
      generate_mock_data.py      ← deterministic data generation script
      color_palette_guide.md     ← colors, hex codes, usage rules
      [name].tps                 ← Tableau color palette file
  resources/
    tableau_mock_dashboard_prompt.md  ← reusable prompt for new dashboard packages
  CLAUDE.md                          ← this file
  DASHBOARD_ROADMAP.md               ← content backlog and series format
  README.md                          ← public-facing repo overview
```

**Dashboard folder naming convention:** lowercase, hyphen-separated, descriptive of use case — not named after specific companies or clients.

Example: `consulting-delivery-analytics`, `housing-crm-pipeline`, `insurance-book-of-business`

---

## Published Dashboards

| Folder | Tableau Public Title | Status |
|--------|---------------------|--------|
| `dashboards/r-systems-delivery-command-center` | Executive Delivery Analytics | Published |

> Note: The folder name references R Systems because it was originally built for that interview context. The published dashboard and all future references use the title "Executive Delivery Analytics" with no company branding.

---

## Design Standards

These apply to every dashboard in this portfolio.

### Color Logic
Color carries meaning — never decoration.
- **Red / #C0392B** — at risk, below target, negative variance
- **Green / #008C7A or teal** — healthy, above target, positive
- **Amber / #F2A900** — monitor, approaching threshold
- **Neutral palette** — does the heavy lifting; color is accent only

### Typography
- Dashboard title: 24–28pt, semibold
- Section headers: 13–15pt, semibold
- KPI values: 24–32pt, semibold
- KPI labels: 9–10pt, muted gray
- Axis/tooltip labels: 8–10pt
- No decorative fonts — clean sans-serif only

### Layout Rules
- Filters in a single top bar or left rail — never scattered
- 4–5 KPI cards across the top of executive views
- Short, action-oriented chart titles
- Precise edge alignment
- White space around KPI groups — dashboards should feel designed, not assembled
- Corner radius on KPI card containers (Tableau 2026.1 native feature)

### Dashboard Size
- Standard: 1400 × 900 for desktop portfolio presentation
- Phone layout only if demonstrating responsive design intentionally

### Tableau Version
Calvin uses Tableau Desktop (limited publish access). Publishing to Tableau Public requires the separate Tableau Public Desktop app. Workbooks are built in Tableau Desktop and exported/published via Tableau Public Desktop.

---

## Content Series Format

Every dashboard and its LinkedIn post follow this structure:

**Use Case** — What business problem does this solve? Who is the audience? What decision does it enable?

**Design Decisions** — 2–3 specific choices explained with *why*, not just *what*. Chart type selection, color logic, layout hierarchy, filter design.

**Feature Highlight** — One Tableau feature (new or underused) that solved a specific problem in this build. Must be earned by the build, not gratuitous.

LinkedIn post tone: direct, no em dashes, no overclaiming, no company name-dropping. Frame as sharing knowledge from consulting experience, not as a job application post.

---

## Workflow — Creating a New Dashboard

Follow this order for every new dashboard project:

1. Define the use case, audience, and key business questions
2. Design the data model (what tables, what grain, what relationships)
3. Generate mock data using `generate_mock_data.py` (deterministic seed)
4. Write the data dictionary
5. Create ASCII wireframes per dashboard tab
6. Write the Tableau build guide (connections, calcs, parameters, actions)
7. Build in Tableau Desktop
8. Write the insights guide (talking points, interview prep)
9. Export screenshots for portfolio
10. Publish to Tableau Public via Tableau Public Desktop
11. Draft LinkedIn post using the series format
12. Update DASHBOARD_ROADMAP.md with published status and links

---

## How Claude Should Help in This Project

**Data generation:** Write or update `generate_mock_data.py` with realistic, deterministic mock data. Use named entities (real-sounding company names, cities, roles) — never placeholder values like "Company A" or "Region 1."

**Wireframes:** Create ASCII layout wireframes showing KPI card placement, filter bar, chart positions, and tab structure. Match every field in the wireframe to the data dictionary.

**Calculated fields:** Provide Tableau formula syntax, purpose, and placement. Only include calcs that serve the specific use case.

**Build guides:** Step-by-step Tableau instructions — data connection, relationship canvas, sheet builds, dashboard assembly, actions, and formatting.

**LinkedIn posts:** Follow the series format. No em dashes. No company names. Explain design choices, not just features. Under 3,000 characters.

**Insights guides:** Frame talking points for interviews. Anticipate recruiter questions. Explain why design decisions were made, not just what was built.

**What Claude should NOT do:**
- Name dashboards after specific companies (use descriptive use-case names)
- Overclaim Calvin's SQL, Python, or Power BI proficiency
- Add features, charts, or calcs not needed for the use case
- Write long docstrings or multi-paragraph comments in Python scripts
- Suggest publishing to Tableau Server or Tableau Online (not available)

---

## Resources

`resources/tableau_mock_dashboard_prompt.md` — master prompt for generating a complete new dashboard package (data, wireframes, build guide, insights). Use this as the starting point when creating a new dashboard from scratch.
