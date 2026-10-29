import chromadb
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# -----------------------------
# Load Embedding Model
# -----------------------------
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# Load FLAN-T5 Model
# -----------------------------
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

# GPU use karo agar available hai
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# -----------------------------
# Open ChromaDB
# -----------------------------
client = chromadb.PersistentClient(path="vector_db")
collection = client.get_collection("video_chunks")

# -----------------------------
# User Question
# -----------------------------
question = input("Ask a question: ")

# -----------------------------
# Retrieve Most Relevant Chunk
# -----------------------------
query_embedding = embed_model.encode(question).tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

context = "\n".join(results["documents"][0])

# -----------------------------
# Build Prompt
# -----------------------------
prompt = f"""
You are answering questions from a video transcript.

Rules:
- Answer only from the given context.
- Reply in one complete sentence.
- If the context does not contain the answer, say "The answer is not available in the transcript."

Context:
{context}

Question:
{question}

Answer:
"""

# -----------------------------
# Generate Answer
# -----------------------------
inputs = tokenizer(prompt, return_tensors="pt", truncation=True).to(device)

outputs = model.generate(
    **inputs,
    max_new_tokens=40,
    do_sample=False
)

answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

# -----------------------------
# Display Result
# -----------------------------
print("\nQuestion :", question)
print("Context  :", context)
print("Answer   :", answer)