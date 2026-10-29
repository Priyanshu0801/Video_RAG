import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve(question: str, top_k: int = 3):
    client = chromadb.PersistentClient(path="multimodal_db")
    collection = client.get_collection("multimodal_segments")

    query_embedding = model.encode(question).tolist()

    # Pehle 5 candidates lao
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )

    query_words = set(question.lower().split())
    reranked = []

    for i in range(len(results["documents"][0])):
        text = results["documents"][0][i]
        metadata = results["metadatas"][0][i]

        # Exact word overlap score
        text_words = set(text.lower().split())
        overlap = len(query_words & text_words)

        reranked.append({
            "text": text,
            "start": metadata["start"],
            "end": metadata["end"],
            "frame": metadata["frame"],
            "score": overlap
        })

    # Overlap ke basis par sort
    reranked.sort(key=lambda x: x["score"], reverse=True)

    return reranked[:top_k]