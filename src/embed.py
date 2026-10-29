
from sentence_transformers import SentenceTransformer
from pathlib import Path

# Embedding model load karo (pehli baar download hoga)
model = SentenceTransformer("all-MiniLM-L6-v2")

chunk_folder = Path("transcripts/chunks")

for file in sorted(chunk_folder.glob("*.txt")):
    text = file.read_text(encoding="utf-8")

    embedding = model.encode(text)

    print(f"{file.name} -> Vector size: {len(embedding)}")