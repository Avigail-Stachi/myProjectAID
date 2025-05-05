import os
import shutil
import zipfile

# נתיב לתיקייה שבה נמצאים קבצי ה-ZIP
input_zip_path = r"C:\project\projectAID\mycode\cnn\datasetBurns.zip"
output_dir = r"C:\project\projectAID\mycode\cnn\datasetBurns_fix"
zip_output_path = os.path.join(output_dir, "burn_levels.zip")

# מיפוי קטגוריות לפי רמות כוויה
categories = {
    '0': 'Burn_Level_1',
    '1': 'Burn_Level_2',
    '2': 'Burn_Level_3'
}

# יצירת תיקיות יעד לכל רמת כוויה
for folder in categories.values():
    os.makedirs(os.path.join(output_dir, folder), exist_ok=True)

# פרוק קובץ ה-ZIP המקורי
with zipfile.ZipFile(input_zip_path, 'r') as zip_ref:
    zip_ref.extractall(output_dir)

# מעבר על קבצי טקסט בתיקיית הקלט ומיון התמונות לפי רמה
for file in os.listdir(output_dir):
    if file.endswith('.txt'):
        txt_path = os.path.join(output_dir, file)
        with open(txt_path, 'r') as f:
            first_line = f.readline().strip()
            if first_line and first_line[0] in categories:
                label = first_line[0]
                category = categories[label]
                image_name = file.replace('.txt', '.jpg')
                image_path = os.path.join(output_dir, image_name)
                if os.path.exists(image_path):
                    shutil.copy(image_path, os.path.join(output_dir, category))

# ייצור קובץ ZIP סופי עם כל התמונות בתיקיות לפי רמה
if not os.path.exists(zip_output_path):  # בדיקה אם הקובץ כבר קיים
    with zipfile.ZipFile(zip_output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(output_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if file != "burn_levels.zip":  # וודא שאתה לא מכסה את קובץ ה-ZIP עצמו
                    arcname = os.path.relpath(file_path, output_dir)
                    zipf.write(file_path, arcname)

    print("הקובץ burn_levels.zip נוצר בהצלחה ב:", zip_output_path)
else:
    print("הקובץ burn_levels.zip כבר קיים.")
