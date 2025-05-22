from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

# --- model loading ---
BASE_DIR   = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "best.pt")
model      = YOLO(MODEL_PATH)

# --- class labels (0–15) ---
label_map = {
    0:  "Yelek",
    1:  "Eldiven",
    2:  "Gözlük Yok",
    3:  "Maske Yok",
    4:  "İnsan",
    5:  "Bot",
    6:  "Sigara",
    7:  "Yangın",
    8:  "Yaralı",
    9:  "Baret",
   10:  "Gözlük",
   11:  "Maske",
   12:  "Yelek Yok",
   13:  "Eldiven Yok",
   14:  "Bot Yok",
   15:  "Baret Yok"
}

# --- helper colors for each class ---
class_colors = {
    0:  (0, 255,   0),
    1:  (255, 0,   0),
    2:  (0,   0, 255),
    3:  (255,255,  0),
    4:  (255, 0, 255),
    5:  (0, 255, 255),
    6:  (128,128,  0),
    7:  (128, 0, 128),
    8:  (0, 128, 128),
    9:  (128,128,128),
   10:  (0,   0, 128),
   11:  (0, 128,   0),
   12:  (128, 0,   0),
   13:  (0,  64, 255),
   14:  (255,64,   0),
   15:  (64,255,   0)
}

# --- fonts ---
RESOURCES  = os.path.abspath(os.path.join(BASE_DIR, "..", "resources"))
FONT_FILE  = os.path.join(RESOURCES, "Montserrat-Regular.ttf")
FONT_SMALL = ImageFont.truetype(FONT_FILE, 18)
FONT_LARGE = ImageFont.truetype(FONT_FILE, 24)

def detect_objects(image_source):
    """
    Run YOLO on an image (file path or BGR array),
    draw colored boxes + Turkish labels with matching colors.
    """
    # load BGR frame
    if isinstance(image_source, (str, os.PathLike)):
        img_bgr = cv2.imread(image_source)
    else:
        img_bgr = image_source

    # inference
    results = model(img_bgr)[0]

    # switch to PIL for drawing
    rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    pil = Image.fromarray(rgb)
    draw = ImageDraw.Draw(pil)

    for box in results.boxes:
        conf = float(box.conf[0].item())
        # skip anything below 60%
        if conf < 0.6:
            continue

        cls_id     = int(box.cls[0].item())
        base_label = label_map.get(cls_id, str(cls_id))
        label      = f"{base_label} {conf:.2f}"
   
        color  = class_colors.get(cls_id, (0,255,0))
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

        # draw the bounding box
        draw.rectangle(
            [(x1, y1), (x2, y2)],
            outline=(color[0], color[1], color[2], 255),
            width=3
        )

        # figure out text size via textbbox
        text_bbox = draw.textbbox((0, 0), label, font=FONT_SMALL)
        text_w = text_bbox[2] - text_bbox[0]
        text_h = text_bbox[3] - text_bbox[1]

        # place label above box (or below if too close to top)
        ty = y1 - text_h - 4
        if ty < 0:
            ty = y1 + 4

        # draw semi-transparent background rectangle
        draw.rectangle(
            [(x1 - 1, ty - 1), (x1 + text_w + 3, ty + text_h + 3)],
            fill=(0, 0, 0, 160)
        )

        # draw the label text in the same color
        draw.text(
            (x1 + 1, ty + 1),
            label,
            font=FONT_SMALL,
            fill=(color[0], color[1], color[2], 255)
        )

    # convert back to BGR for Qt display
    return cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)