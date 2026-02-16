from flask import Flask, request, send_file
from flask_cors import CORS
from ultralytics import YOLO
import cv2
import numpy as np
import os
import tempfile

# ==============================
# Flask Setup
# ==============================

app = Flask(__name__)
CORS(app)

# ==============================
# Load YOLO Model
# ==============================

model = YOLO("best.pt")   # <-- make sure best.pt is inside backend folder

# ==============================
# PPE Color Map
# ==============================

colors = {
    "Person": (255, 0, 0),
    "Helmet": (0, 255, 0),
    "Vest": (0, 0, 255),
    "Boots": (255, 255, 0),
    "Mask": (255, 0, 255),
    "Glove": (0, 255, 255),
    "Goggles": (128, 0, 255),
    "Ear-protection": (255, 128, 0)
}

# ==============================
# Home Route
# ==============================

@app.route("/")
def home():
    return "PPE Detection Backend Running ✅"

# ==============================
# Detection Route (Upload/Webcam)
# ==============================

@app.route("/detect", methods=["POST"])
def detect():

    if "file" not in request.files:
        return "No file uploaded", 400

    file = request.files["file"]

    # Read image
    file_bytes = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if img is None:
        return "Invalid image", 400

    # YOLO Detection
    results = model(img)

    for result in results:
        for box in result.boxes:

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls = int(box.cls[0])

            label = model.names[cls]

            color = colors.get(label, (255, 255, 255))

            # Draw rectangle
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

            # Draw label
            cv2.putText(
                img,
                f"{label} {conf:.2f}",
                (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2
            )

    # Save temp result
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    cv2.imwrite(temp_file.name, img)

    return send_file(temp_file.name, mimetype="image/jpeg")

# ==============================
# Run Server
# ==============================

if __name__ == "__main__":
    app.run(debug=True)
