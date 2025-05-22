import cv2
from PyQt6.QtGui import QImage, QPixmap

def cv_to_qpixmap(cv_img):
    h, w, ch = cv_img.shape
    bytes_per_line = ch * w
    qimg = QImage(cv_img.data, w, h, bytes_per_line, QImage.Format.Format_BGR888)
    return QPixmap.fromImage(qimg)