import sqlite3
import json
import os
import sys

DB_NAME="treat_first_aid.db"
CASE_MAP_PATH=r"C:\project\projectAID\data\cases.json"
# תתי־הדרגות של כוויות: 0 = first-degree, 1 = second-degree, 2 = third-degree
BURN_DEGREES = [0, 1, 2]

if not os.path.isfile(CASE_MAP_PATH):
    print(f"[ERROR] File not found: {CASE_MAPPING_PATH}")
    sys.exit(1)

with open(CASE_MAP_PATH, 'r', encoding='utf-8') as f:
    case_mapping = json.load(f)

treatments=[
    {
        ""
    }
]


#ליצור דאטה ביס
conn = sqlite3.connect(DB_NAME)
cur  = conn.cursor()