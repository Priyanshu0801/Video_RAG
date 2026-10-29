import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import json
from pipeline.clip_embeddings import extract_clip_embeddings

# Whisper ke timestamped segments load karo
with open("transcripts/sample_segments.json", "r", encoding="utf-8") as f:
    segments = json.load(f)

embeddings = extract_clip_embeddings(segments)

print(f"Total frame embeddings: {len(embeddings)}")
print(f"Vector dimension: {len(embeddings[0]['embedding'])}")