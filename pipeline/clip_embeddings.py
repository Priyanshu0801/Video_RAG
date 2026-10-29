
import open_clip
import torch
from PIL import Image
from pathlib import Path


# GPU use karo agar available hai
device = "cuda" if torch.cuda.is_available() else "cpu"

# CLIP model
model, _, preprocess = open_clip.create_model_and_transforms(
    "ViT-B-32",
    pretrained="laion2b_s34b_b79k"
)
model.to(device)
model.eval()


def extract_clip_embeddings(segments):
    """
    Har frame ka 512-dimensional CLIP embedding return karta hai.
    """

    embeddings = []

    for segment in segments:
        frame_path = f"frames/frame_{segment['id']:03d}.jpg"

        image = preprocess(Image.open(frame_path)).unsqueeze(0).to(device)

        with torch.no_grad():
            embedding = model.encode_image(image)
            embedding = embedding / embedding.norm(dim=-1, keepdim=True)

        embeddings.append({
            "id": segment["id"],
            "embedding": embedding.squeeze().cpu().tolist()
        })

    return embeddings