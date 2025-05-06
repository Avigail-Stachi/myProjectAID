import pandas as pd
import nltk
import sys  # לנתיב של EDA

INPUT_FILE = r"C:\project\projectAID\data\data_not_updated\emergency_cases_label_amb_fix_updated.csv"
OUTPUT_FILE = r"C:\project\projectAID\data\emergency_cases_expend7.csv"
# כמה גרסאות לכל טקסט
NUM_AUG = 7
EDA_PATH = r"C:\project\projectAID\exsist"
sys.path.append(EDA_PATH)
from eda import eda

# הורדת משאבי WordNet רק פעם אחת
nltk.download('wordnet')
nltk.download('omw-1.4')


def augment_text(text, num_aug=3):
    return eda(text, num_aug=num_aug)


# קריאת הדאטה והרחבה
def augment_dataset(input_file, output_file, num_aug=3, eda_path=None):
    df = pd.read_csv(input_file)

    augmented_rows = []

    for idx, row in df.iterrows():
        text = row['text']
        label = row['label']
        need_ambulance = row['need_ambulance']

        # הרחבת הטקסט בעזרת EDA
        augmented_texts = augment_text(text, num_aug)

        # שמירת הדוגמאות המורחבות
        for new_text in augmented_texts:
            augmented_rows.append({
                'text': new_text,
                'label': label,
                'need_ambulance': need_ambulance
            })

    # שילוב הדאטה המקורי עם המורחב
    aug_df = pd.concat([df, pd.DataFrame(augmented_rows)], ignore_index=True)

    # שמירה לקובץ חדש
    aug_df.to_csv(output_file, index=False)
    print(f" הקובץ נשמר בהצלחה בשם: {output_file}")


augment_dataset(INPUT_FILE, OUTPUT_FILE, NUM_AUG, eda_path=EDA_PATH)
