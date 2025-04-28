import tensorflow as tf
import numpy as np
import joblib  # טוען את ה־encoder

# טוען את המודל ואת ה־encoder
model = tf.keras.models.load_model(r"C:\project\myModel\mycode\model\saved_model.keras")
encoder = joblib.load(r"C:\project\myModel\mycode\model\encoder.pkl")  # טוען את ה־encoder

# טקסטים חדשים לניבוי
new_texts = ["I was burned by boiling oil", "My friend swallowed a lot of water and is gasping for breath."]
new_data = encoder(np.array(new_texts))  # הפעלת TextVectorization על הטקסטים החדשים
predictions = model.predict(new_data)  # ביצוע ניבוי

# ממיר את התוצאות לסיווגים
predicted_classes = np.argmax(predictions, axis=1)

# מציג את התוצאות
for text, pred_class in zip(new_texts, predicted_classes):
    print(f"Text: {text} -> Predicted Class: {pred_class}")
