import pandas as pd
import nltk
import sys  # לנתיב של EDA

INPUT_FILE = "../data/emergency_cases_clean5.csv"
OUTPUT_FILE = "../data/emergency_cases_clean5_expend_7.csv"
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
    columns = df.columns
    for idx, row in df.iterrows():
        text = row['text']


        # הרחבת הטקסט בעזרת EDA
        augmented_texts = augment_text(text, num_aug)

        # שמירת הדוגמאות המורחבות
        for new_text in augmented_texts:
            augmented_row = {col: row[col] for col in columns}
            augmented_row['text'] = new_text
            augmented_rows.append(augmented_row)

    # שילוב הדאטה המקורי עם המורחב
    aug_df = pd.concat([df, pd.DataFrame(augmented_rows)], ignore_index=True)
    aug_df.drop_duplicates(subset='text', inplace=True)
    # שמירה לקובץ חדש
    aug_df.to_csv(output_file, index=False)
    print(f" הקובץ נשמר בהצלחה בשם: {output_file}")


augment_dataset(INPUT_FILE, OUTPUT_FILE, NUM_AUG, eda_path=EDA_PATH)
