import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import TextVectorization, Embedding, Dropout, Bidirectional, LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping
# import matplotlib
# matplotlib.use('Agg')  #אפשר לשנות ל TkAgg
import matplotlib.pyplot as plt

# import os
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # מסתיר את כל ההודעות למעט שגיאות
# #זה עדין לא עזר אז כרגע אני מבטלת את זה

df = pd.read_csv(
    r"C:\project\myModel\mycode\model\datasetAID3_updated.csv")  # להתייחס כסטרינג עם התעלמות מטאבים לרדת שורה וכו

label_map = {
    'Drowning': 0,
    'Strangulation': 1,
    'Burns': 2
}
# df = df[df['label'].isin(label_map)]                #  להסיר את מה שלא שייך לקטגוריות אם הדאטה סט מכיל תיוגים נוספים
df['label'] = df['label'].map(label_map).astype(int)

texts = df['text'].astype(str).to_numpy()
labels = df['label'].to_numpy()

texts_train, texts_val, labels_train, labels_val = train_test_split(
    texts, labels, test_size=0.2
    # , random_state=42
)  # 20 אחוז לבדיקה
# חושב להגדיר את הרנדום כדי שיוכל להשוות את התוצאות ולא יחלק את הדאטה סט בצורה שונה כל פעם

VOCAB_SIZE = 1000
SEQUENCE_LEN = 100

encoder = TextVectorization(
    max_tokens=VOCAB_SIZE,
    output_mode='int',
    output_sequence_length=SEQUENCE_LEN
)
encoder.adapt(texts_train)  # מילון למילים הנפוצות ביותר מספר נמוך יותר כשתדיר יותר

# אימון: loss על train
# בדיקה: loss על test/validation


# הגדרה
# מה המודל עושה כשהוא מקבל קלט
model = tf.keras.Sequential([
    encoder,  # המרה למספרים
    Embedding(input_dim=VOCAB_SIZE, output_dim=64, mask_zero=True),  # המרה לוקטורים עם משמעות
    # מתעלם מאפסים של פדינג
    # ה-padding מתבצע אוטומטית בתוך שכבת TextVectorization כי אמרתי לו אורך 100
    Dropout(0.3),  # למנוע אוברפיטינג
    Bidirectional(LSTM(64, dropout=0.2)),
    Dropout(0.3),
    Dense(64, activation='relu'),
    Dropout(0.4),  # זה אחרי שכבה צפופה לכן יותר אחוזים למנוע אוברפיטינג
    Dense(3, activation='softmax')  # 3 אופציות לפלט
])

# הכנה לאימון לפי מה להתייחס ולבדוק נתונים
model.compile(
    loss='sparse_categorical_crossentropy',  # Sparse תוויות הן מספר אחד בודד (ולא רשימת אפסים ואחד בודד)
    # כנראה אני אשנה במודל של ה12 כי הוא יכול לחשוב שיש יחס למספור הקטגוריות
    # לשנות לone-hot encoding אחרי שמשנים את הקטגוריות לסוג של בינאריים
    # איך לחשב את הלוס
    optimizer='adam',  # מתאים באופן דינמי את קצב הלמידה תוך כדי אימון
    # איך לייעל
    # מומנטום עוזר למודל להתמיד בכיוון שהוא בחר בו
    # אדפטציה עוזרת למודל להתאים את קצב הלמידה
    # adam משלב את שניהם
    metrics=['accuracy']
)
# אם המודל הפסיק ללמוד חבל על הזמן וגם למנוע אוברפיטנג
early_stop = EarlyStopping(
    monitor='val_loss',
    patience=3,
    restore_best_weights=True
)

# אימון בפועל
history = model.fit(
    texts_train,
    labels_train,
    validation_data=(texts_val, labels_val),
    epochs=10,
    batch_size=32,
    callbacks=[early_stop]
)
# בודק את ביצועי המודל על הדאטה שהוא לא ראה
loss, accuracy = model.evaluate(texts_val, labels_val)
print(f"Validation Loss: {loss:.4f}, Accuracy: {accuracy:.4f}")  # לעגל 4 ספרות אחרי הנקודה

# אם Training Loss יורד חזק, אבל Validation Loss מתחיל לעלות — סימן שהמודל זוכר את הדאטה ולא מת-generalize טוב (אוברפיטינג)
# ציור Loss
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Loss over epochs')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()

# ציור Accuracy
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Accuracy over epochs')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

model.save(r"C:\project\myModel\mycode\model\saved_model_with_encoder.keras")  # לשמור את המודל
