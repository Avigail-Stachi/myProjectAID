import subprocess

command = [
    "tensorflowjs_converter",
    "--input_format=keras",
    "model.keras",
    "/path/to/tfjs_model"
]

# הרצת הפקודה
try:
    subprocess.run(command, check=True)
    print("המודל הומר בהצלחה ל-TensorFlow.js!")
except subprocess.CalledProcessError as e:
    print(f"קרתה שגיאה בעת הרצת הפקודה: {e}")
