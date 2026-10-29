import chromadb

def build_clip_index(segments, clip_embeddings):
    """
    CLIP visual embeddings ko ChromaDB me store karta hai.
    """

    client = chromadb.PersistentClient(path="multimodal_db")
    collection = client.get_or_create_collection("visual_frames")

    # Purane records hata do
    try:
        ids = collection.get()["ids"]
        if ids:
            collection.delete(ids=ids)
    except:
        pass

    for seg, clip in zip(segments, clip_embeddings):
        collection.add(
            ids=[str(seg["id"])],
            embeddings=[clip["embedding"]],
            documents=[f"frame_{seg['id']:03d}.jpg"],
            metadatas=[{
                "start": seg["start"],
                "end": seg["end"],
                "frame": f"frame_{seg['id']:03d}.jpg"
            }]
        )

    return collection.count()