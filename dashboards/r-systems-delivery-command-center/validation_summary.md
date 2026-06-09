# Validation Summary

Validation run date: 2026-06-07

## Generated CSV Row Counts

| File | Rows |
|---|---:|
| `clients.csv` | 28 |
| `consultants.csv` | 120 |
| `projects.csv` | 56 |
| `assignments.csv` | 437 |
| `time_entries.csv` | 37,949 |
| `milestones.csv` | 280 |
| `client_satisfaction.csv` | 101 |

## Date Coverage

| Source | Minimum Date | Maximum Date |
|---|---:|---:|
| `time_entries.entry_date` | 2025-01-01 | 2026-05-29 |
| `projects.start_date` | 2024-09-16 | 2026-02-01 |
| `client_satisfaction.survey_date` | 2025-03-31 | 2026-03-31 |

## Checks Completed

| Check | Result |
|---|---|
| CSV files exist | Passed |
| CSV files have headers | Passed |
| Client IDs are unique in `clients.csv` | Passed |
| Consultant IDs are unique in `consultants.csv` | Passed |
| Project IDs are unique in `projects.csv` | Passed |
| `projects.client_id` values match `clients.client_id` | Passed |
| `assignments.project_id` values match `projects.project_id` | Passed |
| `assignments.consultant_id` values match `consultants.consultant_id` | Passed |
| `time_entries.project_id` values match `projects.project_id` | Passed |
| `time_entries.consultant_id` values match `consultants.consultant_id` | Passed |
| `milestones.project_id` values match `projects.project_id` | Passed |
| `client_satisfaction.client_id` values match `clients.client_id` | Passed |
| `client_satisfaction.project_id` values match `projects.project_id` | Passed |
| Core date fields parse as ISO dates | Passed |
| Core numeric fields parse as numbers | Passed |

## Notes

The dataset intentionally includes operational variation such as late milestones, non-billable work, high-risk projects, different delivery models, and mixed client satisfaction scores. These patterns are included so the Tableau dashboard can tell a realistic consulting delivery story.

The refreshed reporting window uses recent source dates. Time entries run through the latest completed month before June 2026.
