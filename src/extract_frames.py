import cv2
import json
from pathlib import Path

video_path = "videos/sample.mp4"

# Timestamped transcript load
with open("transcripts/sample_segments.json", "r", encoding="utf-8") as f:
    segments = json.load(f)

cap = cv2.VideoCapture(video_path)

# Output folder
Path("frames").mkdir(exist_ok=True)

saved = 0

for segment in segments:
    start_time = segment["start"]

    # Video ko us timestamp par le jao
    cap.set(cv2.CAP_PROP_POS_MSEC, start_time * 1000)

    success, frame = cap.read()

    if success:
        filename = f"frames/frame_{segment['id']:03d}.jpg"
        cv2.imwrite(filename, frame)
        saved += 1

cap.release()

print(f"Frames extracted: {saved}")