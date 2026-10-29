import chromadb
import open_clip
import torch

# GPU
device = "cuda" if torch.cuda.is_available() else "cpu"

# CLIP model
model, _, _ = open_clip.create_model_and_transforms(
    "ViT-B-32",
    pretrained="laion2b_s34b_b79k"
)
model.to(device)
model.eval()


def visual_search(query: str, top_k: int = 3):
    client = chromadb.PersistentClient(path="multimodal_db")
    collection = client.get_collection("visual_frames")

    tokenizer = open_clip.get_tokenizer("ViT-B-32")

    text = tokenizer([query]).to(device)

    with torch.no_grad():
        embedding = model.encode_text(text)
        embedding = embedding / embedding.norm(dim=-1, keepdim=True)

    results = collection.query(
        query_embeddings=[embedding.squeeze().cpu().tolist()],
        n_results=top_k
    )

    return results