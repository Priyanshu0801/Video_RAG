import json
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Multimodal data load
with open("multimodal/multimodal_segments.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Final database
client = chromadb.PersistentClient(path="multimodal_db")
collection = client.get_or_create_collection("multimodal_segments")

# Purane records hata do (taaki duplicate na bane)
try:
    ids = collection.get()["ids"]
    if ids:
        collection.delete(ids=ids)
except:
    pass

# Add every multimodal segment
for item in data:
    embedding = model.encode(item["combined_text"]).tolist()

    collection.add(
        ids=[str(item["id"])],
        documents=[item["combined_text"]],
        embeddings=[embedding],
        metadatas=[{
            "start": item["start"],
            "end": item["end"],
            "frame": f"frame_{item['id']:03d}.jpg"
        }]
    )

print(f"Indexed {collection.count()} multimodal segments.")