# ui/camera_window.py
import cv2
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
)
from utils.image_utils import cv_to_qpixmap
from models.object_detector import detect_objects

class CameraWindow(QWidget):
    def __init__(self):
        super().__init__()
        # enforce a minimum window size so the video feed isn’t tiny
        self.setMinimumSize(800, 500)
        self.setWindowTitle("Live Camera Feed")
        self.cap = None

        # --- UI ---
        self.video_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        self.video_label.setText("Starting camera…")
        self.stop_btn = QPushButton("Stop Camera")
        self.stop_btn.clicked.connect(self.close)

        layout = QVBoxLayout(self)
        layout.addWidget(self.video_label, stretch=1)
        layout.addWidget(self.stop_btn)

        # --- Timer to pull frames every 30ms ---
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_frame)
        self.start_camera()

    def start_camera(self):
        # Open default webcam (index 0). Change to 1,2,… for other devices.
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            QMessageBox.critical(self, "Error", "Could not open camera")
            self.close()
            return
        self.timer.start(30)

    def next_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return
        # run your detection on the BGR frame
        annotated = detect_objects(frame)
        # convert and display
        pix = cv_to_qpixmap(annotated)
        self.video_label.setPixmap(
            pix.scaled(
                self.video_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )

    def closeEvent(self, event):
        # cleanup on window close
        if self.timer.isActive():
            self.timer.stop()
        if self.cap and self.cap.isOpened():
            self.cap.release()
        event.accept()