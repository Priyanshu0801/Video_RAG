from pipeline.retriever import retrieve
from pipeline.visual_retriever import visual_search


def hybrid_search(question, top_k=3):
    """
    Hybrid Retrieval:
    - Text Retrieval (Transcript + OCR)
    - Visual Retrieval (CLIP)
    Returns JSON instead of printing.
    """

    text_results = retrieve(question, top_k=min(2, top_k))
    visual_results = visual_search(question, top_k=min(2, top_k))

    output = {
        "text_results": [],
        "visual_results": []
    }

    # Text results
    for item in text_results:
        output["text_results"].append({
            "start": item["start"],
            "end": item["end"],
            "frame": item["frame"],
            "text": item["text"]
        })

    # Visual results
    metas = visual_results["metadatas"][0]

    for meta in metas:
        output["visual_results"].append({
            "start": meta["start"],
            "end": meta["end"],
            "frame": meta["frame"]
        })

    return output