import whisper
import json
from pathlib import Path

# GPU automatically use karega
model = whisper.load_model("base")

video_path = "videos/sample.mp4"
result = model.transcribe(video_path)

# Folder ensure
Path("transcripts").mkdir(exist_ok=True)

# Plain transcript
with open("transcripts/sample.txt", "w", encoding="utf-8") as f:
    f.write(result["text"])

# Timestamped transcript
with open("transcripts/sample_segments.json", "w", encoding="utf-8") as f:
    json.dump(result["segments"], f, indent=4)

print(f"Total segments: {len(result['segments'])}")
print("Timestamped transcript saved.")