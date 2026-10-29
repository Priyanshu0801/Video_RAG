
import argparse

from pipeline.transcriber import transcribe_video
from pipeline.frame_extractor import extract_frames
from pipeline.ocr import extract_ocr
from pipeline.indexer import build_index
from pipeline.retriever import retrieve
from pipeline.hybrid_retriever import hybrid_search
from pipeline.clip_embeddings import extract_clip_embeddings
from pipeline.clip_indexer import build_clip_index


def main():
    parser = argparse.ArgumentParser(description="Multimodal Video RAG")

    parser.add_argument("--video", required=True, help="Path of input video")
    parser.add_argument("--question", required=True, help="Question to ask")
    parser.add_argument(
        "--mode",
        choices=["text", "hybrid"],
        default="hybrid",
        help="Retrieval mode"
    )

    args = parser.parse_args()

    print("\n[1/6] Transcribing video...")
    segments = transcribe_video(args.video)

    print("[2/6] Extracting frames...")
    extract_frames(args.video, segments)

    print("[3/6] Running OCR...")
    ocr_data = extract_ocr(segments)

    print("[4/6] Building text index...")
    text_count = build_index(segments, ocr_data)
    print(f"Indexed {text_count} text segments.")

    print("[5/6] Building visual index...")
    clip_embeddings = extract_clip_embeddings(segments)
    visual_count = build_clip_index(segments, clip_embeddings)
    print(f"Indexed {visual_count} visual frames.")

    print("[6/6] Retrieving answer...\n")

    print("=" * 60)
    print(f"Question: {args.question}")
    print(f"Mode     : {args.mode}")
    print("=" * 60)

    if args.mode == "text":
        results = retrieve(args.question)

        for i, item in enumerate(results, start=1):
            print(f"\nResult {i}")
            print(f"Time : {item['start']}s - {item['end']}s")
            print(f"Frame: {item['frame']}")
            print(f"Text : {item['text']}")

    else:
        hybrid_search(args.question)


if __name__ == "__main__":
    main()