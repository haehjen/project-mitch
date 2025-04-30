# modules/vision.py
import cv2
import os

class VisionModule:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index

    def capture_image(self, save_path="/tmp/capture.jpg"):
        cap = cv2.VideoCapture(self.camera_index)
        if not cap.isOpened():
            raise RuntimeError(f"Cannot open camera index {self.camera_index}")

        ret, frame = cap.read()
        cap.release()

        if not ret:
            raise RuntimeError("Failed to capture image.")

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        if not cv2.imwrite(save_path, frame):
            raise RuntimeError("Failed to save image.")

        return save_path
