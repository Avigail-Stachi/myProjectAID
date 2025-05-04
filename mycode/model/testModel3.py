import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import numpy as np
import tensorflow as tf

model = tf.keras.models.load_model(
    r"C:\project\myModel\mycode\model\saved_model_with_encoder.keras"
)

reverse_label_map = {0: 'Drowning', 1: 'Strangulation', 2: 'Burns'}

new_texts = [
    "I saw someone choking and gasping for air.",
    "The victim was unconscious after inhaling too much water."
]

new_texts_tensor = tf.constant(new_texts, dtype=tf.string)

#  ניבוי
pred_proba = model.predict(new_texts_tensor)
pred_classes = np.argmax(pred_proba, axis=1)  # axis=1 בשביל ניבוי על כל משפט

for text, cls in zip(new_texts, pred_classes):
    print(f"Text: {text}")
    print(f"  → Predicted class #{cls}: {reverse_label_map[cls]}\n")
