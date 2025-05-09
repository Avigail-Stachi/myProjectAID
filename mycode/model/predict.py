import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
import json
import numpy as np

model_path = "./saved_model1.keras"

map_json_path = "../../data/cases.json"

UNCERTAINTY_THRESHOLD = 0.6
CLOSE_CONFIDENCE_DIFF = 0.05


def load_and_predict(new_sentence, model_path="./saved_model.keras"):
    # טעינת המודל
    model = tf.keras.models.load_model(model_path)
    input_tensor = tf.constant([new_sentence], dtype=tf.string)
    # המודל מצפה למחרוזות טקסט ישירות (לא רשימות)
    prediction = model.predict(input_tensor)
    predicted_class = prediction.argmax()  # המחלקה עם ההסתברות הגבוהה ביותר

    return predicted_class, prediction[0]  # מחזיר את המחלקה ואת מערך ההסתברויות


cpr1 = "My grandfather collapsed and isn’t breathing—what should I do"
cpr2 = "Someone just passed out at the gym and has no pulse—I think I need to start chest compressions"

fainting1 = "My friend suddenly lost consciousness after standing up too fast"
fainting2 = "She fainted while waiting in line and regained consciousness a minute later"

drowning1 = "A child fell into the pool and now he's gasping for air and coughing up water"
drowning2 = "I saw someone underwater for too long at the beach—they’re unresponsive"

electric_shock1 = "He touched a live wire and now he’s shaking and can’t move his arm"
electric_shock2 = "My sister got an electric shock from a faulty charger—she’s disoriented and in pain"

choking1 = "My baby is turning red and can’t breathe after putting something in his mouth"
choking2 = "He was eating steak and suddenly grabbed his throat and stopped talking"

rabies1 = "A stray dog bit me yesterday and now I’m getting headaches and feel feverish"
rabies2 = "I got scratched by a bat and the doctor said it might carry rabies"

bee_sting1 = "She got stung by a bee and now her arm is swelling up badly"
bee_sting2 = "After the bee sting, he’s having trouble breathing and his lips are swelling"

snake_bite1 = "While hiking, he was bitten by a snake—his leg is turning purple"
snake_bite2 = "I think it was a rattlesnake that bit her, and she’s feeling dizzy and nauseous"

scorpion_sting1 = "My little brother stepped on a scorpion and now he’s crying and his foot is swelling"
scorpion_sting2 = "She was stung by a scorpion and her whole leg is tingling and numb"

wounds1 = "He fell on the sidewalk and there’s a deep cut on his knee bleeding a lot"
wounds2 = "She got slashed by broken glass—there’s blood everywhere"

burns1 = "My hand touched the stove and now there’s a blister forming"
burns2 = "Hot oil splashed on his chest and the skin is peeling and red"

fractures1 = "He fell off his bike and his arm looks bent and swollen—it might be broken"
fractures2 = "I heard a crack when I twisted my ankle and now I can’t walk on it"
new_sentence = "There's a knife here, my child is bleeding from his hand."
drowning_choking = "He suddenly collapsed while eating and isn't responding"
burns_fainting = "She fell into the campfire but says it doesn’t hurt much"
drowning_fainting = "My cousin passed out and hit his head near the pool"
bee_sting_wounds = "After touching something in the garden, his hand started swelling quickly"
scorpion_sting_fractures = "He screamed after stepping on something and now his foot is numb"
choking_burns = "My brother inhaled smoke and now he’s coughing and can’t breathe well"
rabies_snake_bite = "She was playing outside, got bitten by something, and now has fever and muscle pain"
electric_shock_burns = "He was helping fix the power box and now he’s unconscious with burn marks"
fractures_wounds = "The boy fell from the tree and his wrist looks deformed, but he can move his fingers"
choking_fainting = "She started choking, then fainted, and now she’s breathing again"
rabies_wounds = "He found a scratch on his leg after walking near the dog shelter, and it looks infected"
bee_sting_snake_bite = "Her lips are swelling and she's dizzy after a hike in the woods"

new_sentence = drowning1
class_idx, probabilities = load_and_predict(new_sentence, model_path)

with open(map_json_path, 'r', encoding='utf-8') as f:
    label_map = json.load(f)
reverse_label_map = {v: k for k, v in label_map.items()}

class_name = reverse_label_map.get(class_idx, "Unknown")
np.set_printoptions(precision=3, suppress=True)
print(f"\nsentence: {new_sentence}")

print(f"\nPredicted class index: {class_idx}")
print(f"Class name: {reverse_label_map[class_idx]}")
print("\nClass probabilities:")
for i, prob in enumerate(probabilities):
    label_name = reverse_label_map.get(i, f"Label {i}")
    print(f"{i:2d} - {label_name:16s}: {prob:.3f}")

# בדיקה האם המודל בטוח בתחזית
sorted_probs = sorted(probabilities, reverse=True)
if sorted_probs[0] - sorted_probs[1] > 0.3:
    print("\nThe model is confident in its prediction.")
else:
    print("\nThe model might be uncertain.")
