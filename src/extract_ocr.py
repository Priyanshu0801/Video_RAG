import cv2
import pytesseract
import json
from pathlib import Path

# Tesseract path (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load transcript segments
with open("transcripts/sample_segments.json", "r", encoding="utf-8") as f:
    segments = json.load(f)

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

# Save OCR result
Path("ocr").mkdir(exist_ok=True)

with open("ocr/ocr_results.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4)

print(f"OCR completed for {len(output)} frames.")