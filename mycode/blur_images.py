from nudenet import NudeDetector
import cv2
import os

detector = NudeDetector()

def blur_nude_areas(image_path, output_path):
    img = cv2.imread(image_path)
    detections = detector.detect(image_path)

    for det in detections:
        x1, y1, x2, y2 = map(int, det['box'])
        roi = img[y1:y2, x1:x2]
        blurred_roi = cv2.GaussianBlur(roi, (51, 51), 0)
        img[y1:y2, x1:x2] = blurred_roi

    cv2.imwrite(output_path, img)


# 🗂 נתיב לתיקייה הראשית של הרמות
input_root = "burn_levels"
output_root = "blurred_burn_levels"

# עוברים על כל תיקייה בתוך תיקיית המקור (למשל: level_1, level_2...)
for subdir in os.listdir(input_root):
    input_subdir = os.path.join(input_root, subdir)
    output_subdir = os.path.join(output_root, subdir)

    if os.path.isdir(input_subdir):
        os.makedirs(output_subdir, exist_ok=True)

        for filename in os.listdir(input_subdir):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                in_path = os.path.join(input_subdir, filename)
                out_path = os.path.join(output_subdir, filename)
                blur_nude_areas(in_path, out_path)
                print(f"טושטשה: {subdir}/{filename}")
