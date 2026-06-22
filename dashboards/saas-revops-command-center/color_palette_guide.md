# Color Palette Guide — SaaS RevOps Command Center

Derived from enterprise SaaS brand research (Salesforce, Stripe, Snowflake, Clari, Datadog, Gong).
Dark canvas standard. Color carries meaning — never decoration.

---

## Canvas System

| Role | Hex | Tableau Use |
|---|---|---|
| Dashboard Background | `#0D1B2E` | Dashboard background shading |
| Card Background | `#162032` | KPI card containers, floating containers |
| Elevated Surface | `#1E2F48` | Hover state, selected card, tooltip background |
| Border / Divider | `#2C3F5E` | Container borders, row dividers, gridlines |

---

## Primary Data Color

| Role | Hex | Tableau Use |
|---|---|---|
| Primary Blue | `#1B96FF` | Main chart bars, primary trend line, open pipeline, funnel bars |

Rationale: Salesforce Lightning Blue — the most recognized enterprise SaaS data color. Audience (CRO, VP Sales, RevOps) associates this with trusted platform data.

---

## Semantic Colors

Color signals state. These three are the only colors that encode meaning in this dashboard.

| Role | Hex | When to Use |
|---|---|---|
| Teal / Healthy | `#00C49A` | Closed Won, above coverage target, positive ARR (New, Expansion), NRR ≥ 100%, forecast beat |
| Red / At Risk | `#E84855` | Closed Lost, below coverage target, churn, stage duration over benchmark, forecast miss |
| Amber / Monitor | `#F5A623` | Coverage 1.0x–1.5x, approaching threshold, forecast gap, stage stall warning |

---

## Accent

| Role | Hex | When to Use |
|---|---|---|
| Indigo / Highlight | `#7B61FF` | Active filter indicator, selected dimension member, parameter control highlight, set action trigger state |

Rationale: Stripe-derived indigo. Signals user selection/interactivity without competing with data colors. Aligns with CN brand purple.

---

## Text Hierarchy

| Role | Hex | Tableau Use |
|---|---|---|
| Primary Text | `#FFFFFF` | KPI values, dashboard title, chart titles |
| Secondary Text | `#94A3C8` | Axis labels, tooltip text, KPI sublabels |
| Muted Text | `#566380` | Helper text, gridline labels, footnotes |

---

## Neutral

| Role | Hex | When to Use |
|---|---|---|
| Slate Gray | `#4A5B78` | Unfocused/comparison bars in dual-axis, background bar in bullet chart, inactive segment |

---

## Per-Chart Color Map

| Chart | Colors Used |
|---|---|
| Stage funnel bars | `#1B96FF` (primary blue) |
| Stage duration vs benchmark | Blue bars; `#E84855` reference line when over benchmark |
| Coverage scorecard by segment | `#00C49A` (≥1.5x) · `#F5A623` (1.0–1.5x) · `#E84855` (<1.0x) |
| Pipeline mix (Won / Lost / Open) | `#00C49A` Won · `#E84855` Lost · `#1B96FF` Open |
| ARR waterfall | `#00C49A` New · `#1B96FF` Expansion · `#E84855` Churn · `#F5A623` Contraction |
| GRR / NRR trend lines | `#00C49A` NRR · `#94A3C8` GRR · `#E84855` reference line at 100% |
| Forecast commit vs won bars | `#1B96FF` Commit · `#00C49A` Won |
| Deal aging table rows | Conditional: `#00C49A` <30 days · `#F5A623` 30–60 days · `#E84855` >60 days |

---

## Typography Reference

| Element | Size | Weight |
|---|---|---|
| Dashboard title | 24–28pt | Semibold |
| Tab / section headers | 13–15pt | Semibold |
| KPI values | 24–32pt | Semibold |
| KPI labels | 9–10pt | Regular · `#94A3C8` |
| Chart titles | 11–13pt | Semibold |
| Axis / tooltip labels | 8–10pt | Regular · `#94A3C8` |

Font: Tableau default sans-serif (Tableau Book / Benton Sans). No decorative fonts.

---

## Tableau Setup Notes

The accompanying `cn-saas-revops.tps` file contains this palette as a Tableau custom color palette.

**To activate in Tableau Desktop:**
1. Copy `cn-saas-revops.tps` content into `Documents/My Tableau Repository/Preferences.tps`
2. Restart Tableau Desktop
3. The palette appears as **CN SaaS RevOps** in the color picker under any discrete color shelf

If `Preferences.tps` already exists, paste the `<color-palette>` block inside the existing `<preferences>` tag — do not replace the whole file.
