
import chromadb
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")


def build_index(segments, ocr_data):
    """
    Transcript + OCR ko merge karke
    final multimodal vector database banata hai.
    """

    client = chromadb.PersistentClient(path="multimodal_db")
    collection = client.get_or_create_collection("multimodal_segments")

    # Duplicate remove
    try:
        ids = collection.get()["ids"]
        if ids:
            collection.delete(ids=ids)
    except:
        pass

    for seg, ocr in zip(segments, ocr_data):

        combined_text = seg["text"].strip()

        if ocr["ocr_text"].strip():
            combined_text += " " + ocr["ocr_text"].strip()

        embedding = model.encode(combined_text).tolist()

        collection.add(
            ids=[str(seg["id"])],
            documents=[combined_text],
            embeddings=[embedding],
            metadatas=[{
                "start": seg["start"],
                "end": seg["end"],
                "frame": f"frame_{seg['id']:03d}.jpg"
            }]
        )

    return collection.count()