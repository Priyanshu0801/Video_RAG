
import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Open multimodal database
client = chromadb.PersistentClient(path="multimodal_db")
collection = client.get_collection("multimodal_segments")

# User question
question = input("Ask a question: ")

# Encode query
query_embedding = model.encode(question).tolist()

# Retrieve top 3 results
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

print("\n=== Top Results ===\n")

for i in range(len(results["documents"][0])):
    metadata = results["metadatas"][0][i]

    print(f"Result {i+1}")
    print(f"Time : {metadata['start']}s - {metadata['end']}s")
    print(f"Frame: {metadata['frame']}")
    print(f"Text : {results['documents'][0][i]}")
    print("-" * 50)