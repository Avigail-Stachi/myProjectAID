import sqlite3
import json
import os

def load_case_mapping(json_path):
    with open(json_path, 'r') as f:
        return json.load(f)

def create_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS treatments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_type TEXT NOT NULL,
            degree INTEGER DEFAULT NULL,
            short_instruction TEXT NOT NULL,
            detailed_instruction TEXT NOT NULL,
            image_url TEXT NOT NULL,
            video_url TEXT NOT NULL,
            source_url TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()

def get_treatments_content(case_mapping):
    content = []

    for case_key, case_id in case_mapping.items():
        if case_key == "burns":
            for degree in range(3):  # 0, 1, 2
                content.append({
                    "case_type": case_key,
                    "degree": degree,
                    "short_instruction": f"Treat burn of degree {degree}.",
                    "detailed_instruction": f"This is a detailed treatment guide for a degree {degree} burn. If needed, the app will automatically call an ambulance to 101.",
                    "image_url": f"https://example.com/images/burn_degree_{degree}.jpg",
                    "video_url": f"https://example.com/videos/burn_degree_{degree}.mp4",
                    "source_url": "https://www.redcross.org.uk/first-aid/learn-first-aid/burns"
                })
        else:
            content.append({
                "case_type": case_key,
                "degree": None,
                "short_instruction": f"How to treat {case_key.replace('_', ' ')}.",
                "detailed_instruction": f"This is a detailed treatment guide for {case_key.replace('_', ' ')}. If needed, the app will automatically call an ambulance to 101.",
                "image_url": f"https://example.com/images/{case_key}.jpg",
                "video_url": f"https://example.com/videos/{case_key}.mp4",
                "source_url": "https://www.redcross.org.uk/first-aid"
            })
    return content

def populate_db(data, db_path="treatments.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    for entry in data:
        cursor.execute('''
            INSERT INTO treatments (
                case_type, degree, short_instruction, detailed_instruction,
                image_url, video_url, source_url
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            entry["case_type"],
            entry["degree"],
            entry["short_instruction"],
            entry["detailed_instruction"],
            entry["image_url"],
            entry["video_url"],
            entry["source_url"]
        ))
    conn.commit()
    conn.close()

json_path = "../data/cases.json"
db_path="../data/treatments.db"
case_mapping = load_case_mapping(json_path)
create_db(db_path)
treatments_data = get_treatments_content(case_mapping)
populate_db(treatments_data)

print("Database created successfully")

print(f"Inserted {len(treatments_data)} treatment records.")
