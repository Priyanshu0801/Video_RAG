
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

# Embedding model load
model = SentenceTransformer("all-MiniLM-L6-v2")

# ChromaDB create/open
client = chromadb.PersistentClient(path="vector_db")
collection = client.get_or_create_collection("video_chunks")

chunk_folder = Path("transcripts/chunks")

for file in sorted(chunk_folder.glob("*.txt")):
    text = file.read_text(encoding="utf-8")

    embedding = model.encode(text).tolist()

    collection.add(
        ids=[file.stem],
        documents=[text],
        embeddings=[embedding]
    )

print(f"Stored {collection.count()} chunks in ChromaDB.")