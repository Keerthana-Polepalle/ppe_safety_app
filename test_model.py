from ultralytics import YOLO

# Load trained model
model = YOLO("runs/detect/train10/weights/best.pt")

# Run prediction on validation images
model.predict(
    source="PPE.v2i.yolov8/valid/images",
    conf=0.4,
    save=True
)
