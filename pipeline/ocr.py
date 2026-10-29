
import cv2
import pytesseract
import json
from pathlib import Path

# Windows Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_ocr(segments):
    """
    Har extracted frame se OCR text nikalta hai
    aur ocr_results.json save karta hai.
    """

    output = []

    for segment in segments:
        frame_path = f"frames/frame_{segment['id']:03d}.jpg"

        image = cv2.imread(frame_path)
        if image is None:
            continue

        text = pytesseract.image_to_string(image).strip()

        output.append({
            "frame": f"frame_{segment['id']:03d}.jpg",
            "start": segment["start"],
            "end": segment["end"],
            "ocr_text": text
        })

    Path("ocr").mkdir(exist_ok=True)

    with open("ocr/ocr_results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)

    return output