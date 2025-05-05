# import pandas as pd
#
# df = pd.read_csv(r"C:\project\myModel\mycode\emergency_cases_label_amb.csv")
# label_mapping = {
#     "CPR": "cpr",
#     "Fainting": "fainting",
#     "Drowning": "drowning",
#     "Electrocution": "electric_shock",
#     "Electric shock": "electric_shock",
#     "Choking": "choking",
#     "Rabies": "rabies",
#     "Bee sting": "bee_sting",
#     "Snake bite": "snake_bite",
#     "Scorpion sting": "scorpion_sting",
#     "Wounds": "wounds",
#     "Burns": "burns",
#     "Fractures": "fractures"
# }
#
# df["label"] = df["label"].apply(lambda x: label_mapping.get(x, x))
# df.to_csv(r"C:\project\myModel\mycode\emergency_cases_label_amb_fix.csv", index=False)
import pandas as pd

# שלב 1: טוענים את הדאטה סט
df = pd.read_csv(r"C:\project\projectAID\data\emergency_cases_label_amb_fix.csv")

# שלב 2: שינוי כל הערכים 'Fracture' ל-'fractures' בעמודת ה-label
df['label'] = df['label'].replace('Fracture', 'fractures')

# שלב 3: בדיקה שהתווית שונתה בהצלחה
print(df['label'].unique())  # מציג את כל התוויות בעמודת 'label'

# שלב 4: שמירה של הדאטה סט המעודכן
df.to_csv(r"C:\project\projectAID\data\emergency_cases_label_amb_fix_updated.csv", index=False)

print("הדאטה סט שודרג ונשמר כ-emergency_cases_label_amb_updated.csv")
