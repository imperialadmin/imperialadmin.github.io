#!/usr/bin/env python3
"""
refresh_data.py
---------------
Converts the monthly UKG Pro export into two CSVs for the web app:
  - anniversaries.csv  →  Name, HireDate (YYYY-MM-DD)
  - birthdays.csv      →  BirthDate (YYYY-MM-DD), Name

Usage:
    python scripts/refresh_data.py
    python scripts/refresh_data.py path/to/export.csv

Drop the UKG export in scripts/input/ and run without arguments,
or pass a file path explicitly.
"""

import sys
import re
import os
import glob
import pandas as pd
from datetime import date

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input")
OUTPUT_ANNIVERSARIES = os.path.join(REPO_ROOT, "anniversaries.csv")
OUTPUT_BIRTHDAYS = os.path.join(REPO_ROOT, "birthdays.csv")


def transform_name(name: str) -> str:
    m = re.match(r'^([^,]+),\s*(.+)$', str(name).strip())
    if m:
        return f"{m.group(2).strip()} {m.group(1).strip()}"
    return name.strip()


def find_input_file() -> str:
    csvs = [f for f in glob.glob(os.path.join(INPUT_DIR, "*.csv"))
            if not os.path.basename(f).startswith("processed_")]
    if not csvs:
        print(f"Error: No unprocessed CSV found in scripts/input/")
        sys.exit(1)
    if len(csvs) > 1:
        print(f"Multiple CSVs found: {[os.path.basename(f) for f in csvs]}")
        print(f"Using: {os.path.basename(csvs[0])}")
    return csvs[0]


def archive_input(input_path: str):
    dirname = os.path.dirname(input_path)
    basename = os.path.basename(input_path)
    new_name = f"processed_{date.today()}_{basename}"
    new_path = os.path.join(dirname, new_name)
    os.rename(input_path, new_path)
    print(f"✓ Input renamed to {new_name}")


def process(input_path: str):
    if not os.path.exists(input_path):
        print(f"Error: File not found: {input_path}")
        sys.exit(1)

    df = pd.read_csv(input_path)

    name_col = next((c for c in df.columns if "employee name" in c.lower()), None)
    if not name_col:
        print(f"Error: Could not find 'Employee Name' column. Columns: {df.columns.tolist()}")
        sys.exit(1)

    df["Name"] = df[name_col].apply(transform_name)
    df["Birth Date"] = pd.to_datetime(df["Birth Date"], errors="coerce").dt.strftime("%Y-%m-%d")
    df["Last Hire Date"] = pd.to_datetime(df["Last Hire Date"], errors="coerce").dt.strftime("%Y-%m-%d")

    df[["Name", "Last Hire Date"]].to_csv(OUTPUT_ANNIVERSARIES, index=False, header=False)
    print(f"✓ anniversaries.csv  ({len(df)} rows)")

    df[["Birth Date", "Name"]].to_csv(OUTPUT_BIRTHDAYS, index=False, header=False)
    print(f"✓ birthdays.csv  ({len(df)} rows)")

    archive_input(input_path)


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else find_input_file()
    print(f"Processing: {os.path.basename(input_file)}")
    process(input_file)
    print("Done.")
