from PyQt6.QtWidgets import QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QMessageBox
from PyQt6.QtCore import Qt
import os
from PyQt6.QtGui import QPixmap

class LoginWindow(QWidget):
    def __init__(self, on_success):
        super().__init__()
        self.on_success = on_success
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        # logo
        logo = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        path = os.path.join(os.path.dirname(__file__), "..", "resources", "omega_logo.png")
        pix = QPixmap(path).scaledToWidth(200, Qt.TransformationMode.SmoothTransformation)
        logo.setPixmap(pix)
        layout.addWidget(logo)

        # inputs
        self.user = QLineEdit(placeholderText="Username")
        self.pw = QLineEdit(placeholderText="Password")
        self.pw.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.user)
        layout.addWidget(self.pw)

        # buttons
        row = QHBoxLayout()
        login_btn = QPushButton("Login")
        new_btn   = QPushButton("New User")
        login_btn.clicked.connect(self.check)
        row.addWidget(login_btn)
        row.addWidget(new_btn)
        layout.addLayout(row)

    def check(self):
        if self.user.text() == 'omega' and self.pw.text() == 'vizyon':
            self.on_success()
        else:
            QMessageBox.warning(self, 'Error', 'Invalid credentials')
