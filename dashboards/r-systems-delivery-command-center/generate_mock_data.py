import csv
import math
import random
from datetime import date, timedelta
from pathlib import Path


SEED = 20260606
random.seed(SEED)

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "mock_data"
DATA_DIR.mkdir(exist_ok=True)

REPORT_START = date(2025, 1, 1)
REPORT_END = date(2026, 5, 31)
PROJECT_START_WINDOW = date(2024, 9, 1)


def daterange(start, end):
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)


def write_csv(filename, rows):
    if not rows:
        return
    path = DATA_DIR / filename
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def clamp(value, low, high):
    return max(low, min(high, value))


regions = ["North America", "Europe", "APAC"]
industries = ["SaaS", "Healthcare", "Telecom", "Financial Services", "Manufacturing", "Media"]
service_lines = [
    "Data & AI",
    "Cloud Modernization",
    "Product Engineering",
    "CX Transformation",
    "QA Automation",
    "DevSecOps",
]
project_types = ["Implementation", "Modernization", "Managed Services", "Advisory", "Platform Build"]
delivery_models = ["Onsite", "Remote", "Hybrid"]
roles = [
    ("Lead Consultant", 175, 78),
    ("Senior Consultant", 145, 65),
    ("Consultant", 118, 52),
    ("Data Visualization Designer", 135, 58),
    ("Solution Architect", 195, 92),
    ("Project Manager", 155, 72),
    ("QA Engineer", 108, 46),
    ("Data Engineer", 152, 68),
]
skills = ["Tableau", "SQL", "Python", "Cloud", "Data Modeling", "UX/UI", "AI/ML", "DevOps", "QA Automation"]
client_names = [
    "Aster Health Network",
    "Brightline Telecom",
    "CedarPoint Financial",
    "Elevate Media Group",
    "Evergreen Manufacturing",
    "Foresight SaaS",
    "Harbor Retail Partners",
    "Juniper Insurance",
    "Lighthouse Energy",
    "Meridian Analytics",
    "Northstar Logistics",
    "OakBridge Bank",
    "Pacific Learning",
    "Pioneer Devices",
    "Riverstone Health",
    "Skyward Software",
    "Summit Mobility",
    "TerraWorks Industrial",
    "UnionSquare Payments",
    "Vertex BioTech",
    "Westhaven Hospitality",
    "BluePeak Platforms",
    "ClearPath Cloud",
    "Quantum CX Labs",
    "Nexa Manufacturing",
    "Mosaic Media",
    "HelioCare Systems",
    "Atlas Subscription Co.",
]

first_names = [
    "Maya", "Daniel", "Priya", "Jordan", "Avery", "Noah", "Sofia", "Ethan", "Lena", "Marcus",
    "Iris", "Owen", "Nina", "Caleb", "Aria", "Diego", "Zara", "Milo", "Talia", "Rohan",
    "Elena", "Samir", "Grace", "Theo", "Amara", "Julian", "Kiara", "Mateo", "Mina", "Isaac",
]
last_names = [
    "Shah", "Morgan", "Chen", "Patel", "Rivera", "Bennett", "Singh", "Garcia", "Nguyen", "Reed",
    "Khan", "Parker", "Mehta", "Brooks", "Iyer", "Cole", "Nair", "Foster", "Kim", "Hughes",
]


clients = []
for idx, name in enumerate(client_names, start=1):
    industry = industries[(idx + random.randint(0, 5)) % len(industries)]
    region = random.choices(regions, weights=[0.56, 0.26, 0.18])[0]
    clients.append({
        "client_id": f"CL{idx:03d}",
        "client_name": name,
        "industry": industry,
        "client_region": region,
        "strategic_tier": random.choices(["Enterprise", "Growth", "Emerging"], weights=[0.38, 0.44, 0.18])[0],
        "account_owner": random.choice(["N. Wallace", "T. Mehra", "S. Alvarez", "K. Romano", "D. Ellis"]),
    })

consultants = []
used_names = set()
for idx in range(1, 121):
    role, bill_rate, cost_rate = random.choice(roles)
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    while name in used_names:
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
    used_names.add(name)
    level = random.choices(["Principal", "Senior", "Mid", "Associate"], weights=[0.12, 0.34, 0.38, 0.16])[0]
    home_region = random.choices(regions, weights=[0.48, 0.3, 0.22])[0]
    utilization_target = {"Principal": 0.72, "Senior": 0.78, "Mid": 0.82, "Associate": 0.85}[level]
    consultants.append({
        "consultant_id": f"CN{idx:03d}",
        "consultant_name": name,
        "role": role,
        "level": level,
        "home_region": home_region,
        "primary_skill": random.choice(skills),
        "bill_rate": bill_rate + random.randint(-12, 18),
        "cost_rate": cost_rate + random.randint(-8, 10),
        "utilization_target": round(utilization_target, 2),
        "hire_date": (date(2017, 1, 1) + timedelta(days=random.randint(0, 3000))).isoformat(),
    })

projects = []
for idx in range(1, 57):
    client = random.choice(clients)
    service_line = random.choice(service_lines)
    start = PROJECT_START_WINDOW + timedelta(days=random.randint(0, 520))
    planned_days = random.randint(60, 260)
    end = start + timedelta(days=planned_days + random.randint(-20, 45))
    status = "Completed" if end <= REPORT_END else random.choices(
        ["Active", "At Risk", "On Hold"], weights=[0.68, 0.24, 0.08]
    )[0]
    budget_hours = random.randrange(700, 5600, 80)
    budget_revenue = budget_hours * random.randint(126, 182)
    projects.append({
        "project_id": f"PR{idx:04d}",
        "project_name": f"{client['client_name'].split()[0]} {service_line} {random.choice(project_types)}",
        "client_id": client["client_id"],
        "service_line": service_line,
        "project_type": random.choice(project_types),
        "delivery_model": random.choice(delivery_models),
        "project_region": client["client_region"],
        "start_date": start.isoformat(),
        "planned_end_date": (start + timedelta(days=planned_days)).isoformat(),
        "actual_or_forecast_end_date": end.isoformat(),
        "status": status,
        "budget_hours": budget_hours,
        "budget_revenue": budget_revenue,
        "risk_level": random.choices(["Low", "Medium", "High"], weights=[0.5, 0.34, 0.16])[0],
    })

assignments = []
assignment_id = 1
for project in projects:
    team_size = random.randint(4, 11)
    weighted = random.sample(consultants, team_size)
    for consultant in weighted:
        allocation = random.choice([0.25, 0.4, 0.5, 0.6, 0.75, 1.0])
        assignments.append({
            "assignment_id": f"AS{assignment_id:05d}",
            "project_id": project["project_id"],
            "consultant_id": consultant["consultant_id"],
            "allocation_pct": allocation,
            "assignment_role": consultant["role"],
            "assigned_start_date": project["start_date"],
            "assigned_end_date": project["actual_or_forecast_end_date"],
        })
        assignment_id += 1

assignments_by_project = {}
for assignment in assignments:
    assignments_by_project.setdefault(assignment["project_id"], []).append(assignment)
consultant_lookup = {c["consultant_id"]: c for c in consultants}
project_lookup = {p["project_id"]: p for p in projects}

time_entries = []
entry_id = 1
for assignment in assignments:
    project = project_lookup[assignment["project_id"]]
    consultant = consultant_lookup[assignment["consultant_id"]]
    start = max(date.fromisoformat(project["start_date"]), REPORT_START)
    end = min(date.fromisoformat(project["actual_or_forecast_end_date"]), REPORT_END)
    if end < start:
        continue
    utilization_target = consultant["utilization_target"]
    for day in daterange(start, end):
        if day.weekday() >= 5:
            continue
        if random.random() > 0.78:
            continue
        seasonal = 1 + 0.08 * math.sin((day.timetuple().tm_yday / 365) * math.tau)
        hours = round(clamp(random.gauss(7.8 * assignment["allocation_pct"] * seasonal, 1.3), 0.5, 10.5), 2)
        billable_probability = clamp(0.74 + utilization_target * 0.18 - (0.1 if project["risk_level"] == "High" else 0), 0.58, 0.94)
        is_billable = random.random() < billable_probability
        entry_type = "Billable Delivery" if is_billable else random.choice(["Internal", "Enablement", "Rework", "Admin"])
        bill_rate = consultant["bill_rate"] if is_billable else 0
        cost_rate = consultant["cost_rate"]
        time_entries.append({
            "time_entry_id": f"TE{entry_id:07d}",
            "entry_date": day.isoformat(),
            "project_id": project["project_id"],
            "consultant_id": consultant["consultant_id"],
            "hours": hours,
            "billable_hours": hours if is_billable else 0,
            "non_billable_hours": 0 if is_billable else hours,
            "entry_type": entry_type,
            "bill_rate": bill_rate,
            "cost_rate": cost_rate,
            "revenue": round(hours * bill_rate, 2),
            "labor_cost": round(hours * cost_rate, 2),
        })
        entry_id += 1

milestones = []
milestone_id = 1
milestone_names = ["Discovery Complete", "Design Approved", "Build Complete", "UAT Complete", "Production Launch"]
for project in projects:
    start = date.fromisoformat(project["start_date"])
    planned_end = date.fromisoformat(project["planned_end_date"])
    span = max((planned_end - start).days, 1)
    for idx, milestone_name in enumerate(milestone_names, start=1):
        planned = start + timedelta(days=round(span * idx / 5))
        slip = random.choices([-5, -2, 0, 2, 5, 9, 14, 21], weights=[0.06, 0.08, 0.28, 0.2, 0.16, 0.1, 0.08, 0.04])[0]
        actual = planned + timedelta(days=slip)
        if actual > REPORT_END and project["status"] in ["Active", "At Risk", "On Hold"]:
            actual_value = ""
            state = "Pending"
        else:
            actual_value = actual.isoformat()
            state = "Late" if slip > 3 else "On Time"
        milestones.append({
            "milestone_id": f"MS{milestone_id:05d}",
            "project_id": project["project_id"],
            "milestone_name": milestone_name,
            "planned_date": planned.isoformat(),
            "actual_date": actual_value,
            "milestone_status": state,
            "days_late": max(slip, 0) if state != "Pending" else "",
        })
        milestone_id += 1

satisfaction = []
survey_id = 1
for project in projects:
    client = next(c for c in clients if c["client_id"] == project["client_id"])
    base = {"Low": 8.7, "Medium": 7.8, "High": 6.9}[project["risk_level"]]
    for quarter_start in [date(2025, 3, 31), date(2025, 6, 30), date(2025, 9, 30), date(2025, 12, 31), date(2026, 3, 31)]:
        if quarter_start < date.fromisoformat(project["start_date"]):
            continue
        if quarter_start > date.fromisoformat(project["actual_or_forecast_end_date"]) + timedelta(days=45):
            continue
        csat = round(clamp(random.gauss(base, 0.85), 4.8, 9.9), 1)
        nps = int(round((csat - 7.2) * 18 + random.gauss(15, 8)))
        satisfaction.append({
            "survey_id": f"SV{survey_id:05d}",
            "survey_date": quarter_start.isoformat(),
            "client_id": client["client_id"],
            "project_id": project["project_id"],
            "csat_score": csat,
            "nps_score": clamp(nps, -35, 82),
            "response_count": random.randint(4, 24),
            "primary_feedback_theme": random.choices(
                ["Delivery Quality", "Communication", "Speed", "Technical Expertise", "Change Management", "Responsiveness"],
                weights=[0.24, 0.18, 0.16, 0.2, 0.1, 0.12],
            )[0],
        })
        survey_id += 1

write_csv("clients.csv", clients)
write_csv("consultants.csv", consultants)
write_csv("projects.csv", projects)
write_csv("assignments.csv", assignments)
write_csv("time_entries.csv", time_entries)
write_csv("milestones.csv", milestones)
write_csv("client_satisfaction.csv", satisfaction)

print(f"Generated mock data in {DATA_DIR}")
print(f"clients.csv: {len(clients)} rows")
print(f"consultants.csv: {len(consultants)} rows")
print(f"projects.csv: {len(projects)} rows")
print(f"assignments.csv: {len(assignments)} rows")
print(f"time_entries.csv: {len(time_entries)} rows")
print(f"milestones.csv: {len(milestones)} rows")
print(f"client_satisfaction.csv: {len(satisfaction)} rows")
