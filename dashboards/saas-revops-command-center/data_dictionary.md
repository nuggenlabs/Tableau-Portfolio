# Data Dictionary — SaaS RevOps Command Center

## Tables

| File | Rows | Grain | Primary Key |
|------|------|-------|-------------|
| `opportunities.csv` | 500 | One row per opportunity | `OpportunityID` |
| `stage_history.csv` | ~1,675 | One row per stage per opportunity | `OpportunityID` + `StageName` |
| `quotas.csv` | 154 | One row per rep per quarter | `Owner` + `Quarter` |

---

## opportunities.csv

| Field | Type | Values / Range | Tableau Role | Notes |
|-------|------|----------------|--------------|-------|
| `OpportunityID` | String | OPP-00001 … OPP-00500 | Dimension | Primary key |
| `AccountName` | String | 88 SaaS company names | Dimension | Multiple opps per account (Expansion/Renewal) |
| `StageName` | String | Prospect / Qualified / Demo / Proposal / Commit / Closed Won / Closed Lost | Dimension | Current or final stage |
| `HighestStage` | String | Same as StageName values, excl. Closed Won/Lost | Dimension | Deepest open stage reached before close — used for forecast accuracy |
| `ACV` | Integer | $8K – $900K | Measure | Annual Contract Value; whole-dollar multiples of $1K |
| `CloseDate` | Date | 2024-01-01 – 2026-09-30 | Dimension / Date | Q1 2024–Q4 2025 for closed; Q1–Q3 2026 for open pipeline |
| `Owner` | String | 14 rep names | Dimension | Matches `Owner` in quotas.csv |
| `Segment` | String | SMB / Mid-Market / Enterprise | Dimension | Deal segment; correlates with rep's primary segment |
| `Region` | String | West / Central / East | Dimension | Derived from Owner's region |
| `CreatedDate` | Date | 2023-07-01 – 2025-12-31 | Dimension / Date | Date opp was opened |
| `LastActivityDate` | Date | varies | Dimension / Date | Last CRM activity; used for deal aging |
| `DaysSinceActivity` | Integer | 0 – 55+ (open); 500–900 (closed) | Measure | Pre-computed; re-derive in Tableau with DATEDIFF for accuracy |
| `ForecastCategory` | String | Omit / Best Case / Commit / Closed | Dimension | Salesforce-style forecast roll-up |
| `IsWon` | Boolean (string) | true / false | Dimension | true only when StageName = Closed Won |
| `IsClosed` | Boolean (string) | true / false | Dimension | true for both Closed Won and Closed Lost |
| `ARRType` | String | New / Expansion / Renewal / Churn | Dimension | Revenue motion; Churn = lost renewal |
| `CreatedQuarter` | String | Q1 2024 – Q4 2025 | Dimension | Convenience label for created date |
| `CloseQuarter` | String | Q1 2024 – Q3 2026 | Dimension | Convenience label for close date; joins to quotas.[Quarter] |
| `EnteredCurrentStage` | Date | varies | Dimension / Date | When the opp entered its current (or final) stage |
| `DaysInCurrentStage` | Integer | 1 – 200+ | Measure | Days in current/final stage |

### ARRType logic

| ARRType | IsWon | Meaning | ARR impact |
|---------|-------|---------|------------|
| New | true | First purchase by this account | +ACV |
| Expansion | true | Upsell or cross-sell to existing account | +ACV |
| Renewal | true | Existing subscription renewed | Neutral (preserved ARR) |
| New | false | Lost new logo | No change |
| Expansion | false | Lost upsell | No change |
| Churn | false | Lost renewal = churned revenue | –ACV |

---

## stage_history.csv

| Field | Type | Values | Tableau Role | Notes |
|-------|------|--------|--------------|-------|
| `OpportunityID` | String | OPP-00001 … | Dimension | FK → opportunities |
| `StageName` | String | Prospect … Commit | Dimension | Stage name (never Closed Won/Lost) |
| `EnteredDate` | Date | varies | Dimension / Date | When opp entered this stage |
| `ExitedDate` | Date | varies or empty | Dimension / Date | Empty string = current/final stage |
| `DaysInStage` | Integer | 1 – 200+ | Measure | Elapsed days in this stage |
| `IsCurrentStage` | Boolean (string) | true / false | Dimension | true = this is the opp's current (open) or exit stage (closed) |

**Use:** avg days per stage for the stage duration chart; join to opportunities on `OpportunityID`.

---

## quotas.csv

| Field | Type | Values | Tableau Role | Notes |
|-------|------|--------|--------------|-------|
| `Owner` | String | 14 rep names | Dimension | FK → opportunities.[Owner] |
| `Region` | String | West / Central / East | Dimension | |
| `Segment` | String | SMB / Mid-Market / Enterprise | Dimension | Rep's primary segment |
| `Quarter` | String | Q1 2024 – Q3 2026 | Dimension | FK → opportunities.[CloseQuarter] |
| `QuarterStart` | Date | first day of quarter | Dimension / Date | |
| `QuarterEnd` | Date | last day of quarter | Dimension / Date | |
| `Quota` | Integer | $95K – $620K per rep-quarter | Measure | Q4 inflated ~18%; Q1 deflated ~5% |

**Relationship:** `quotas.[Owner]` = `opportunities.[Owner]` AND `quotas.[Quarter]` = `opportunities.[CloseQuarter]`

---

## Tableau data type assignments

| Field | Set to |
|-------|--------|
| ACV, Quota, DaysInStage, DaysInCurrentStage | Measure (continuous) |
| CloseDate, CreatedDate, LastActivityDate, EnteredDate, ExitedDate, EnteredCurrentStage | Date |
| IsWon, IsClosed, IsCurrentStage | String (treat as filter dimension; do not convert to boolean) |
| OpportunityID, Owner, AccountName, StageName, etc. | Dimension |
| DaysSinceActivity | Measure — but re-derive in Tableau (see calc `[Days Since Activity]`) |

> Do not trust the pre-computed `DaysSinceActivity` column for the aging table. Use `DATEDIFF('day', [LastActivityDate], TODAY())` so the value stays live as you demo the workbook.
