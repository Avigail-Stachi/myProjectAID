



קוד מותאם ל-one-hot encoding:
python
Copy
Edit

from tensorflow.keras.utils import to_categorical

# המרת התוויות למערך One-Hot
labels_one_hot = to_categorical(labels, num_classes=3)  # לשנות את num_classes בהתאם לכמות הקטגוריות שלך

# הגדרת המודל
model = tf.keras.Sequential([
    encoder,  # המרת הטקסטים למספרים
    Embedding(input_dim=VOCAB_SIZE, output_dim=64, mask_zero=True),
    Dropout(0.3),
    Bidirectional(LSTM(64, dropout=0.2)),
    Dropout(0.3),
    Dense(64, activation='relu'),
    Dropout(0.4),
    Dense(3, activation='softmax')  # 3 קטגוריות
])

# קומפילציה עם Categorical Crossentropy
model.compile(
    loss='categorical_crossentropy',  # כאן בחרנו ב-Categorical Crossentropy
    optimizer='adam',
    metrics=['accuracy']
)

# אימון המודל
history = model.fit(
    texts_train,
    labels_one_hot_train,  # להשתמש ב-One-Hot במקום במספרים
    validation_data=(texts_val, labels_one_hot_val),
    epochs=10,
    batch_size=32,
    callbacks=[early_stop]
)
