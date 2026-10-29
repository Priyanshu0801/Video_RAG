import sys
import json
from pathlib import Path

# Root folder ko Python path me add karo
sys.path.append(str(Path(__file__).resolve().parent.parent))

from pipeline.clip_embeddings import extract_clip_embeddings
from pipeline.clip_indexer import build_clip_index

# Whisper ke timestamped segments load karo
with open("transcripts/sample_segments.json", "r", encoding="utf-8") as f:
    segments = json.load(f)

# CLIP embeddings banao
clip_embeddings = extract_clip_embeddings(segments)

# ChromaDB me store karo
count = build_clip_index(segments, clip_embeddings)

print(f"Indexed {count} visual frames.")