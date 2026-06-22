import csv
import random
from datetime import date, timedelta
from pathlib import Path
from collections import Counter

SEED = 20240118
random.seed(SEED)

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "mock_data"
DATA_DIR.mkdir(exist_ok=True)

TODAY = date(2026, 6, 22)

# ---------------------------------------------------------------------------
# Reference tables
# ---------------------------------------------------------------------------

ALL_STAGES = ["Prospect", "Qualified", "Demo", "Proposal", "Commit"]

STAGE_TO_FORECAST = {
    "Prospect":    "Omit",
    "Qualified":   "Best Case",
    "Demo":        "Best Case",
    "Proposal":    "Best Case",
    "Commit":      "Commit",
    "Closed Won":  "Closed",
    "Closed Lost": "Omit",
}

# Cumulative win rate: probability of closing won if the deal reaches this stage
WIN_RATE = {
    "Prospect":  0.05,
    "Qualified": 0.20,
    "Demo":      0.40,
    "Proposal":  0.60,
    "Commit":    0.80,
}

# (mean days, std dev) to transit through each stage.
# Tuned around benchmark thresholds so the stage-duration view has a mixed story:
# Demo and Prospect are healthy, Qualified is close, Proposal and Commit need focus.
STAGE_DURATION = {
    "Prospect":  (10, 3),
    "Qualified": (9,  2),
    "Demo":      (6,  2),
    "Proposal":  (16, 3),
    "Commit":    (13, 3),
}

REPS_BY_REGION = {
    "West":    ["Mia Torres", "Ethan Brooks", "Priya Kapoor", "Liam Chen", "Sofia Ramirez"],
    "Central": ["Marcus Webb", "Avery Singh", "Jordan Kelly", "Noah Patel"],
    "East":    ["Zara Mitchell", "Diego Fernandez", "Elena Okafor", "Caleb Nguyen", "Aria Stephens"],
}

REP_REGION = {
    name: region for region, names in REPS_BY_REGION.items() for name in names
}
ALL_REPS = list(REP_REGION.keys())

# Primary segment and how often the rep stays in it
REP_SEGMENT = {
    "Mia Torres":      ("SMB",        0.78),
    "Ethan Brooks":    ("Mid-Market", 0.68),
    "Priya Kapoor":    ("Enterprise", 0.80),
    "Liam Chen":       ("SMB",        0.82),
    "Sofia Ramirez":   ("Mid-Market", 0.70),
    "Marcus Webb":     ("Enterprise", 0.75),
    "Avery Singh":     ("SMB",        0.65),
    "Jordan Kelly":    ("Mid-Market", 0.72),
    "Noah Patel":      ("Enterprise", 0.70),
    "Zara Mitchell":   ("Enterprise", 0.78),
    "Diego Fernandez": ("Mid-Market", 0.70),
    "Elena Okafor":    ("SMB",        0.80),
    "Caleb Nguyen":    ("Mid-Market", 0.66),
    "Aria Stephens":   ("Mid-Market", 0.72),
}
ALL_SEGMENTS = ["SMB", "Mid-Market", "Enterprise"]

ACV_RANGE = {
    "SMB":        (8_000,   42_000),
    "Mid-Market": (42_000,  180_000),
    "Enterprise": (180_000, 900_000),
}

# Closed quarters (historical — deals resolved here)
CLOSED_QUARTERS = [
    (date(2024, 1, 1),  date(2024, 3, 31),  "Q1 2024"),
    (date(2024, 4, 1),  date(2024, 6, 30),  "Q2 2024"),
    (date(2024, 7, 1),  date(2024, 9, 30),  "Q3 2024"),
    (date(2024, 10, 1), date(2024, 12, 31), "Q4 2024"),
    (date(2025, 1, 1),  date(2025, 3, 31),  "Q1 2025"),
    (date(2025, 4, 1),  date(2025, 6, 30),  "Q2 2025"),
    (date(2025, 7, 1),  date(2025, 9, 30),  "Q3 2025"),
    (date(2025, 10, 1), date(2025, 12, 31), "Q4 2025"),
]

# All quarters including near-future (for quota table — covers open deal close dates)
FUTURE_QUARTERS = [
    (date(2026, 1, 1), date(2026, 3, 31),  "Q1 2026"),
    (date(2026, 4, 1), date(2026, 6, 30),  "Q2 2026"),
    (date(2026, 7, 1), date(2026, 9, 30),  "Q3 2026"),
]
ALL_QUARTERS = CLOSED_QUARTERS + FUTURE_QUARTERS

# Median sales cycle by segment (days created → closed)
SALES_CYCLE = {"SMB": 42, "Mid-Market": 82, "Enterprise": 130}

SAAS_ACCOUNTS = [
    "Lattice Software", "Mosaic Cloud", "Kinetica Labs", "Velo Systems", "Apexon Digital",
    "Ironclad Platforms", "Seismic Analytics", "Pulsar Systems", "Vertex SaaS", "Helix Data",
    "Clearbit Technologies", "Runway Financial", "Rippling Networks", "Notion Labs",
    "Figment Cloud", "Cobalt Security", "Amplitude Systems", "Brex Platform", "Ramp Analytics",
    "Retool Software", "Grafana Ops", "Temporal Cloud", "Airbyte Data", "dbt Labs",
    "Fivetran Systems", "Monte Carlo Data", "Atlan Platform", "Selectstar Inc",
    "Alation Analytics", "Secoda Data", "Castor Analytics", "Metaphor Networks",
    "Bigeye Solutions", "Anomalo Systems", "GreatX Corp", "Soda Analytics",
    "Quolum SaaS", "Blissfully Cloud", "Torii Platform", "Productboard Systems",
    "Aha Software", "Roadmunk Analytics", "Craft Platform", "Airfocus Cloud",
    "Chisel Analytics", "Correlated SaaS", "Endgame Platform", "Pocus Systems",
    "Warmly Cloud", "Common Room", "Orbit Platform", "Devrev Systems",
    "Vitally CS", "ChurnZero Analytics", "Gainsight Cloud", "Planhat Systems",
    "Catalyst Platform", "ClientSuccess Data", "Totango Analytics",
    "ProfitWell Systems", "Baremetrics Cloud", "Chartmogul Analytics", "Maxio Platform",
    "Recurly Systems", "Chargebee Cloud", "Zuora Platform", "Paddle Analytics",
    "Avalara Systems", "TaxJar Cloud", "Sovos Analytics", "Synder Platform",
    "HighSpot Systems", "Gong Revenue", "Chorus Analytics", "Salesloft Platform",
    "Outreach Systems", "Apollo Cloud", "ZoomInfo Data", "Cognism Platform",
    "Lusha Analytics", "Bombora Systems", "Qualified Platform", "Mutiny Systems",
    "Drift Cloud", "Intercom Platform", "Front Systems", "Kustomer Analytics",
    "Gladly Cloud", "Ada Support", "Tidio Platform", "Freshdesk Systems",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def pick_segment(rep):
    primary, bias = REP_SEGMENT[rep]
    if random.random() < bias:
        return primary
    others = [s for s in ALL_SEGMENTS if s != primary]
    return random.choice(others)


def gen_acv(segment):
    lo, hi = ACV_RANGE[segment]
    raw = random.triangular(lo, hi, lo + (hi - lo) * 0.28)
    return max(int(round(raw / 1000) * 1000), lo)


def get_quarter_label(d):
    q = (d.month - 1) // 3 + 1
    return f"Q{q} {d.year}"


def rand_date_in_range(start, end):
    delta = (end - start).days
    if delta <= 0:
        return start
    return start + timedelta(days=random.randint(0, delta))


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def stage_dur(stage):
    mu, sigma = STAGE_DURATION[stage]
    return max(1, int(random.gauss(mu, sigma)))


def write_csv(filename, rows):
    if not rows:
        return
    path = DATA_DIR / filename
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


# ---------------------------------------------------------------------------
# Quota table  (rep × quarter)
# ---------------------------------------------------------------------------

REP_QUOTA_ANNUAL = {}
for rep in ALL_REPS:
    primary_seg = REP_SEGMENT[rep][0]
    if primary_seg == "SMB":
        REP_QUOTA_ANNUAL[rep] = random.randint(420_000, 620_000)
    elif primary_seg == "Mid-Market":
        REP_QUOTA_ANNUAL[rep] = random.randint(750_000, 1_150_000)
    else:
        REP_QUOTA_ANNUAL[rep] = random.randint(1_300_000, 2_100_000)

quota_rows = []
for rep in ALL_REPS:
    region = REP_REGION[rep]
    annual = REP_QUOTA_ANNUAL[rep]
    for qstart, qend, qlabel in ALL_QUARTERS:
        if "Q4" in qlabel:
            mult = 1.18
        elif "Q3" in qlabel:
            mult = 1.06
        elif "Q1" in qlabel:
            mult = 0.95
        else:
            mult = 1.00
        quota_rows.append({
            "Owner":        rep,
            "Region":       region,
            "Segment":      REP_SEGMENT[rep][0],
            "Quarter":      qlabel,
            "QuarterStart": qstart.isoformat(),
            "QuarterEnd":   qend.isoformat(),
            "Quota":        int(annual / 4 * mult),
        })


# ---------------------------------------------------------------------------
# Opportunity + stage history generation
# ---------------------------------------------------------------------------
# Pre-assign outcome categories so the mix is controlled:
#   ~30% Closed Won   (historical bookings to drive ARR waterfall)
#   ~22% Closed Lost  (historical losses to drive win-rate & churn story)
#   ~48% Open         (live pipeline to drive Tab 1 pipeline health)

TARGET_TOTAL = 500
N_WON  = 148
N_LOST = 112
N_OPEN = TARGET_TOTAL - N_WON - N_LOST  # 240

# Closed-quarter weights (end-of-year quarters win more deals)
CLOSED_Q_WEIGHTS = [0.85, 0.90, 0.95, 1.25, 0.85, 0.90, 1.00, 1.30]

# For Closed Lost: distribution of which stage the deal exited at
# Reflects win rates: most losses happen early (Prospect/Qualified)
LOST_STAGE_WEIGHTS = [0.38, 0.27, 0.18, 0.11, 0.06]

# For Open deals: current stage distribution
# (more deals deeper in funnel = healthier-looking pipeline coverage)
OPEN_STAGE_WEIGHTS = [0.20, 0.22, 0.23, 0.22, 0.13]

opportunities      = []
stage_history_rows = []
opp_id             = 1

# Track accounts that have closed-won deals (drives Expansion / Renewal ARR type)
account_won_dates: dict[str, list[date]] = {}


def build_opp(outcome: str):
    """Return a fully-populated opportunity dict + its stage_history rows."""
    global opp_id
    closed_stage_alloc = None

    owner   = random.choice(ALL_REPS)
    region  = REP_REGION[owner]
    segment = pick_segment(owner)
    account = random.choice(SAAS_ACCOUNTS)
    acv     = gen_acv(segment)

    # --- ARR type ---
    prior_wins = account_won_dates.get(account, [])
    if prior_wins:
        arr_type_raw = random.choices(
            ["New", "Expansion", "Renewal"],
            weights=[0.15, 0.50, 0.35]
        )[0]
        if arr_type_raw == "Expansion":
            acv = max(int(acv * random.uniform(0.25, 0.55)), 5_000)
    else:
        arr_type_raw = random.choices(
            ["New", "Expansion"],
            weights=[0.84, 0.16]
        )[0]

    # --- Dates ---
    if outcome in ("won", "lost"):
        # Pick a close quarter from historical 8 quarters
        q_idx = random.choices(range(8), weights=CLOSED_Q_WEIGHTS)[0]
        qstart, qend, _ = CLOSED_QUARTERS[q_idx]
        close_date = rand_date_in_range(qstart, qend)

        cycle_mu   = SALES_CYCLE[segment]
        cycle_days = max(14, int(random.gauss(cycle_mu, cycle_mu * 0.20)))
        created_date = close_date - timedelta(days=cycle_days)
        # Don't let created date go before Jan 2023
        created_date = max(created_date, date(2023, 1, 1))

        if outcome == "won":
            stage           = "Closed Won"
            is_won          = True
            is_closed       = True
            final_arr_type  = arr_type_raw
            stages_traversed = ALL_STAGES[:]
            if account not in account_won_dates:
                account_won_dates[account] = []
            account_won_dates[account].append(close_date)

        else:  # lost
            lost_stage_idx   = random.choices(range(5), weights=LOST_STAGE_WEIGHTS)[0]
            lost_stage       = ALL_STAGES[lost_stage_idx]
            partial_frac     = (lost_stage_idx + 1) / len(ALL_STAGES)
            partial_days     = max(7, int(cycle_days * partial_frac) + random.randint(-3, 5))
            close_date       = created_date + timedelta(days=partial_days)
            # Clamp close_date to not exceed TODAY
            close_date       = min(close_date, TODAY - timedelta(days=1))
            stage            = "Closed Lost"
            is_won           = False
            is_closed        = True
            final_arr_type   = "Churn" if arr_type_raw == "Renewal" else arr_type_raw
            stages_traversed = ALL_STAGES[: lost_stage_idx + 1]

        closed_stage_alloc = [stage_dur(s) for s in stages_traversed]
        created_date       = max(close_date - timedelta(days=sum(closed_stage_alloc)), date(2023, 1, 1))
        last_activity = close_date + timedelta(days=random.randint(0, 3))

    else:  # open
        # Active pipeline: close dates spread across Q1–Q3 2026
        open_close_quarters = [
            (date(2026, 1, 1), date(2026, 3, 31)),
            (date(2026, 4, 1), date(2026, 6, 30)),
            (date(2026, 7, 1), date(2026, 9, 30)),
        ]
        oq_weights = [0.30, 0.42, 0.28]
        oq_start, oq_end = random.choices(open_close_quarters, weights=oq_weights)[0]
        close_date = rand_date_in_range(oq_start, oq_end)

        cycle_mu   = SALES_CYCLE[segment]
        cycle_days = max(14, int(random.gauss(cycle_mu, cycle_mu * 0.20)))
        created_date = close_date - timedelta(days=cycle_days)
        created_date = max(created_date, date(2024, 7, 1))  # not older than Q3 2024

        # Current stage weighted toward mid-funnel
        stage_idx        = random.choices(range(5), weights=OPEN_STAGE_WEIGHTS)[0]
        stage            = ALL_STAGES[stage_idx]
        is_won           = False
        is_closed        = False
        final_arr_type   = arr_type_raw
        stages_traversed = ALL_STAGES[: stage_idx + 1]

        # Keep stale pipeline visible without making half the book look inactive.
        days_ago    = random.choices(
            [random.randint(1, 10), random.randint(11, 26), random.randint(27, 55)],
            weights=[0.63, 0.27, 0.10]
        )[0]
        last_activity = TODAY - timedelta(days=days_ago)

    days_since_activity = (TODAY - last_activity).days

    # --- Stage history rows ---
    # For closed deals, distribute total elapsed days proportionally across stages
    # so the cursor never overshoots close_date.
    cursor = created_date
    entered_current_stage = created_date
    sh_rows = []

    if is_closed:
        stage_alloc = closed_stage_alloc[:]
    else:
        stage_alloc = [stage_dur(s) for s in stages_traversed]

    for i, s in enumerate(stages_traversed):
        is_last = (i == len(stages_traversed) - 1)
        days_in  = stage_alloc[i]
        if is_last:
            entered_current_stage = cursor
            if is_closed:
                exit_date = close_date
                days_in   = max((close_date - cursor).days, 1)
            else:
                exit_date = None
                days_in   = max((TODAY - cursor).days, 0)
            sh_rows.append({
                "OpportunityID":  f"OPP-{opp_id:05d}",
                "StageName":      s,
                "EnteredDate":    cursor.isoformat(),
                "ExitedDate":     exit_date.isoformat() if exit_date else "",
                "DaysInStage":    days_in,
                "IsCurrentStage": "false" if is_closed else "true",
            })
        else:
            exit_date = cursor + timedelta(days=days_in)
            sh_rows.append({
                "OpportunityID":  f"OPP-{opp_id:05d}",
                "StageName":      s,
                "EnteredDate":    cursor.isoformat(),
                "ExitedDate":     exit_date.isoformat(),
                "DaysInStage":    days_in,
                "IsCurrentStage": "false",
            })
            cursor = exit_date

    # --- Opportunity row ---
    highest_stage = stages_traversed[-1]  # deepest open stage before close
    opp = {
        "OpportunityID":       f"OPP-{opp_id:05d}",
        "HighestStage":        highest_stage,
        "AccountName":         account,
        "StageName":           stage,
        "ACV":                 acv,
        "CloseDate":           close_date.isoformat(),
        "Owner":               owner,
        "Segment":             segment,
        "Region":              region,
        "CreatedDate":         created_date.isoformat(),
        "LastActivityDate":    last_activity.isoformat(),
        "DaysSinceActivity":   days_since_activity,
        "ForecastCategory":    STAGE_TO_FORECAST[stage],
        "IsWon":               str(is_won).lower(),
        "IsClosed":            str(is_closed).lower(),
        "ARRType":             final_arr_type,
        "CreatedQuarter":      get_quarter_label(created_date),
        "CloseQuarter":        get_quarter_label(close_date),
        "EnteredCurrentStage": entered_current_stage.isoformat(),
        "DaysInCurrentStage":  (
            max((TODAY - entered_current_stage).days, 0) if not is_closed
            else max((close_date - entered_current_stage).days, 1)
        ),
    }

    opp_id += 1
    return opp, sh_rows


# Build all opportunities in shuffled outcome order
outcome_list = (
    ["won"]  * N_WON  +
    ["lost"] * N_LOST +
    ["open"] * N_OPEN
)
random.shuffle(outcome_list)

for outcome in outcome_list:
    opp, sh = build_opp(outcome)
    opportunities.append(opp)
    stage_history_rows.extend(sh)


# ---------------------------------------------------------------------------
# Write output
# ---------------------------------------------------------------------------

write_csv("opportunities.csv", opportunities)
write_csv("stage_history.csv", stage_history_rows)
write_csv("quotas.csv", quota_rows)


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

won_list  = [o for o in opportunities if o["IsWon"] == "true"]
lost_list = [o for o in opportunities if o["IsClosed"] == "true" and o["IsWon"] == "false"]
open_list = [o for o in opportunities if o["IsClosed"] == "false"]

print(f"Generated mock data -> {DATA_DIR}")
print(f"\nopportunities.csv : {len(opportunities):>5} rows")
print(f"stage_history.csv : {len(stage_history_rows):>5} rows")
print(f"quotas.csv        : {len(quota_rows):>5} rows")

print("\n--- Outcome breakdown ---")
print(f"  Closed Won  : {len(won_list):>4}  ({len(won_list)/len(opportunities)*100:.1f}%)")
print(f"  Closed Lost : {len(lost_list):>4}  ({len(lost_list)/len(opportunities)*100:.1f}%)")
print(f"  Open        : {len(open_list):>4}  ({len(open_list)/len(opportunities)*100:.1f}%)")

print("\n--- Open deal stage distribution ---")
for s, n in Counter(o["StageName"] for o in open_list).most_common():
    print(f"  {s:<15}: {n}")

print("\n--- ARR type (Closed Won) ---")
for k, v in Counter(o["ARRType"] for o in won_list).most_common():
    print(f"  {k:<12}: {v}")

print("\n--- ARR type (Closed Lost) ---")
for k, v in Counter(o["ARRType"] for o in lost_list).most_common():
    print(f"  {k:<12}: {v}")

print("\n--- Closed Won ACV by quarter ---")
from collections import defaultdict
won_by_q: dict[str, int] = defaultdict(int)
for o in won_list:
    won_by_q[o["CloseQuarter"]] += o["ACV"]
for _, _, qlabel in CLOSED_QUARTERS:
    print(f"  {qlabel}: ${won_by_q.get(qlabel, 0):>12,.0f}")

total_open_acv   = sum(o["ACV"] for o in open_list)
total_q1q2_quota = sum(r["Quota"] for r in quota_rows if r["Quarter"] in ("Q1 2026", "Q2 2026"))
q_quota_all      = sum(r["Quota"] for r in quota_rows if r["Quarter"] == "Q1 2025")
print(f"\n--- Pipeline health snapshot ---")
print(f"  Total open pipeline ACV : ${total_open_acv:>12,.0f}")
print(f"  Example quarterly quota : ${q_quota_all:>12,.0f}  (Q1 2025, all reps)")
print(f"  Coverage vs Q1 2025     : {total_open_acv / q_quota_all:.1f}x")

print("\n--- Deal aging (open deals) ---")
green  = sum(1 for o in open_list if o["DaysSinceActivity"] <  15)
yellow = sum(1 for o in open_list if 15 <= o["DaysSinceActivity"] <= 29)
red    = sum(1 for o in open_list if o["DaysSinceActivity"] >= 30)
print(f"  Green  (<15d) : {green}")
print(f"  Yellow (15-29): {yellow}")
print(f"  Red    (30d+) : {red}")
