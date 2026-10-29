
import whisper
import json
from pathlib import Path

# Model ko ek baar load karo
model = whisper.load_model("base")


def transcribe_video(video_path: str):
    """
    Video ko transcribe karke:
    - Plain transcript
    - Timestamped transcript
    return karta hai.
    """

    result = model.transcribe(video_path)

    Path("transcripts").mkdir(exist_ok=True)

    # Plain text
    with open("transcripts/sample.txt", "w", encoding="utf-8") as f:
        f.write(result["text"])

    # Timestamped JSON
    with open("transcripts/sample_segments.json", "w", encoding="utf-8") as f:
        json.dump(result["segments"], f, indent=4)

    return result["segments"]