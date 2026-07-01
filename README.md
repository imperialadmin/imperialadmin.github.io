# imperialadmin.github.io

Internal Imperial site, hosted via GitHub Pages, that displays employee birthdays and work anniversaries on the office digital signage. Also hosts an embedded Instagram feed page.

## What's in this repo

| File | Purpose |
|---|---|
| `today.html` | Today's work anniversaries — unused |
| `upcoming.html` | Upcoming work anniversaries (full year, highlights today) — shown on signage |
| `monthly.html` | Current month's work anniversaries — unused |
| `birthdays.html` | Today's/upcoming birthdays — unused |
| `instagram.html` | Embedded Imperial Instagram feed - shown on signage |
| `anniversaries.csv` | Generated data consumed by `upcoming.html` |
| `birthdays.csv` | Generated data; currently uploaded manually to Yodeck (see below), not consumed by `birthdays.html` |
| `1080p-imperial-sign.jpg` / `1080p-imperial-sign-vertical.jpg` | Imperial signage/logo images |
| `scripts/` | Python tooling that generates the two CSVs above from an HR export — see below |

All pages are static HTML with vanilla JavaScript — they `fetch()` the CSV files at the repo root and render them client-side. No build step for the site itself.

## `scripts/` — monthly data refresh

`scripts/refresh_data.py` turns a monthly UKG Pro employee export into the two CSVs the signage pages read.

**What it does:**
1. Reads the UKG export CSV and finds the "Employee Name" column.
2. Converts each name from `Last, First` to `First Last`.
3. Reformats `Birth Date` and `Last Hire Date` to `YYYY-MM-DD`.
4. Writes two files at the repo root (no header row):
   - `anniversaries.csv` → `Name,HireDate`
   - `birthdays.csv` → `BirthDate,Name`
5. Renames the processed input file in place to `processed_<date>_<original-name>.csv` so it never gets picked up again.

**`scripts/input/`** is where you drop the raw UKG export. It's gitignored — the export contains employee PII and must never be committed. Processed/archived exports pile up here over time; feel free to delete old ones locally once you're confident the data made it into the CSVs.

**Setup:**
```bash
pip install pandas
```

**Usage:**
```bash
# Auto-finds the one unprocessed CSV in scripts/input/
python scripts/refresh_data.py

# Or point it at a specific file
python scripts/refresh_data.py path/to/export.csv
```

## Birthday notifications via Yodeck

Birthdays are **not** currently displayed via `birthdays.html`. Instead, `birthdays.csv` is uploaded manually to Yodeck, which drives the birthday displays on signage.

- Yodeck app management: https://app.yodeck.com/index.html#main/app
- Apps to update: **Birthday Notification** and **Birthday Notification Vertical**
- After generating a fresh `birthdays.csv`, upload it to both apps in Yodeck to replace the existing file.

This is a temporary arrangement — the plan is to eventually retire Yodeck for this purpose and have all birthday/anniversary notifications served directly from this repo's site instead.

## Monthly refresh runbook

1. Export employee data from UKG Pro.
2. Drop the export CSV into `scripts/input/`.
3. Run `python scripts/refresh_data.py`.
4. Confirm `anniversaries.csv` and `birthdays.csv` at the repo root were updated (row counts print to the console).
5. Commit and push `anniversaries.csv` and `birthdays.csv`. The raw export in `scripts/input/` is never committed — only the generated CSVs are.
6. Upload the new `birthdays.csv` to both Yodeck apps (**Birthday Notification** and **Birthday Notification Vertical**) at https://app.yodeck.com/index.html#main/app.

## CSV format reference

Neither output file has a header row.

- `anniversaries.csv`: `Name,HireDate` — e.g. `Ashley Achten,2014-08-25`
- `birthdays.csv`: `BirthDate,Name` — e.g. `1991-11-07,Ashley Achten`
