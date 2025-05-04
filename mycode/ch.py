import pandas as pd

df = pd.read_csv(r"C:\project\myModel\mycode\emergency_cases_label_amb.csv")
label_mapping = {
    "CPR": "cpr",
    "Fainting": "fainting",
    "Drowning": "drowning",
    "Electrocution": "electric_shock",
    "Electric shock": "electric_shock",
    "Choking": "choking",
    "Rabies": "rabies",
    "Bee sting": "bee_sting",
    "Snake bite": "snake_bite",
    "Scorpion sting": "scorpion_sting",
    "Wounds": "wounds",
    "Burns": "burns",
    "Fractures": "fractures"
}

df["label"] = df["label"].apply(lambda x: label_mapping.get(x, x))
df.to_csv(r"C:\project\myModel\mycode\emergency_cases_label_amb_fix.csv", index=False)
