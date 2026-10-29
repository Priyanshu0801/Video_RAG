import json
from pathlib import Path

# Load transcript
with open("transcripts/sample_segments.json", "r", encoding="utf-8") as f:
    segments = json.load(f)

# Load OCR
with open("ocr/ocr_results.json", "r", encoding="utf-8") as f:
    ocr = json.load(f)

merged = []

for seg, o in zip(segments, ocr):
    merged.append({
        "id": seg["id"],
        "start": seg["start"],
        "end": seg["end"],
        "transcript": seg["text"].strip(),
        "ocr": o["ocr_text"].strip(),
        "combined_text": (
            seg["text"].strip()
            + (" " + o["ocr_text"].strip() if o["ocr_text"].strip() else "")
        )
    })

Path("multimodal").mkdir(exist_ok=True)

with open("multimodal/multimodal_segments.json", "w", encoding="utf-8") as f:
    json.dump(merged, f, indent=4)

print(f"Merged {len(merged)} multimodal segments.")