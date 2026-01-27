from flask import Flask, request, jsonify
from ultralytics import YOLO
import cv2
import numpy as np
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Allow frontend to access backend

# -------------------------
# Load YOLO model
# -------------------------
MODEL_PATH = "best.pt"   # make sure best.pt is inside backend folder

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("best.pt not found in backend folder")

print("Loading PPE detection model...")
model = YOLO(MODEL_PATH)
print("Model loaded successfully")

# -------------------------
# Home route
# -------------------------
@app.route("/")
def home():
    return "PPE Detection Backend Running"

# -------------------------
# Detect route
# -------------------------
@app.route("/detect", methods=["POST"])
def detect():
    print("Detect API called")

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"})

    file = request.files["image"]
    img_bytes = file.read()

    # Convert bytes to OpenCV image
    img = cv2.imdecode(
        np.frombuffer(img_bytes, np.uint8),
        cv2.IMREAD_COLOR
    )

    if img is None:
        return jsonify({"error": "Invalid image file"})

    # Run YOLO inference
    results = model(img, conf=0.4)

    detections = []

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            cls_id = int(box.cls)
            confidence = float(box.conf)
            label = model.names[cls_id]

            detections.append({
                "label": label,
                "confidence": round(confidence, 2),
                "box": [
                    int(x1),
                    int(y1),
                    int(x2),
                    int(y2)
                ]
            })

    return jsonify(detections)

# -------------------------
# Run app
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
