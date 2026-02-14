from ultralytics import YOLO
import os

# Absolute path to dataset yaml
DATA_YAML = r"D:\ppe_safety_app\PPE.v2i.yolov8\data.yaml"

model = YOLO("yolov8n.pt")

model.train(
    data=DATA_YAML,
    epochs=20,
    imgsz=640,
    batch=8,
    device="cpu"
)
