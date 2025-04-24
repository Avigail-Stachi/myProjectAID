import os

model_path_vosk = r"C:\project\myModel\vosk-model-small-en-us-0.15"
print("Exists? ", os.path.isdir(model_path_vosk))
print("Contents:", os.listdir(model_path_vosk))
for name in os.listdir(model_path_vosk):
    full = os.path.join(model_path_vosk, name)
    print(name, "is dir?", os.path.isdir(full))
