import json

with open("transcripts/sample_segments.json", "r", encoding="utf-8") as f:
    segments = json.load(f)

for segment in segments:
    print(
        f"frame_{segment['id']:03d}.jpg | "
        f"{segment['start']:.2f}s - {segment['end']:.2f}s | "
        f"{segment['text'].strip()}"
    )