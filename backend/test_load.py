from ultralytics import YOLO

print("Loading model...")
model = YOLO("best.pt")
print("Model loaded successfully")
