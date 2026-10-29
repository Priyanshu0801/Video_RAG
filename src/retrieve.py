import chromadb
from sentence_transformers import SentenceTransformer

# Model load
model = SentenceTransformer("all-MiniLM-L6-v2")

# Existing database open
client = chromadb.PersistentClient(path="vector_db")
collection = client.get_collection("video_chunks")

# Test question
query = "Who is not alone?"

query_embedding = model.encode(query).tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=1
)

print("Question:", query)
print("Retrieved chunk:", results["documents"][0][0])