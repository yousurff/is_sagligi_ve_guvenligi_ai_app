# ui/main_menu.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFileDialog
from PyQt6.QtCore import Qt
from utils.image_utils import cv_to_qpixmap
import cv2

from models.object_detector import detect_objects

class DropLabel(QLabel):
    """A QLabel that you can drag & drop image files onto."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        # Accept only file URLs
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if not urls:
            return
        path = urls[0].toLocalFile()
        # call the parent widget's process()
        # (we assume parent is MainMenuWindow)
        self.parent().process(path)
        event.acceptProposedAction()


class MainMenuWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # replace your plain QLabel with our DropLabel
        self.drop_area = DropLabel("Drag & drop image here",
                                  alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.drop_area, stretch=1)

        row = QHBoxLayout()
        cam_btn = QPushButton('Camera')
        img_btn = QPushButton('Choose Image')
        cam_btn.clicked.connect(self.open_camera)
        img_btn.clicked.connect(self.choose_image)
        row.addWidget(cam_btn)
        row.addWidget(img_btn)
        layout.addLayout(row)

    def choose_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, 'Open file', '', 'Images (*.png *.jpg *.jpeg *.bmp)')
        if path:
            self.process(path)

    def open_camera(self):
        # ... your camera‐window popup logic ...
        from ui.camera_window import CameraWindow
        win = CameraWindow()
        win.setParent(self, Qt.WindowType.Window)
        win.show()

    def process(self, path_or_frame):
        # If path_or_frame is a string path, detect_objects will read it;
        # if it's a cv2 frame, detect_objects will accept it too.
        out = detect_objects(path_or_frame)
        pix = cv_to_qpixmap(out)
        self.drop_area.setPixmap(
            pix.scaled(
                self.drop_area.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )