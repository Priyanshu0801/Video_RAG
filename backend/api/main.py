from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles

from pathlib import Path
import shutil
import uuid
import json
import asyncio

# ---------------- Existing Project Imports ----------------
from pipeline.transcriber import transcribe_video
from pipeline.frame_extractor import extract_frames
from pipeline.ocr import extract_ocr
from pipeline.indexer import build_index
from pipeline.clip_indexer import build_clip_index
from pipeline.hybrid_retriever import hybrid_search

# ---------------- FastAPI ----------------
app = FastAPI(title="Multimodal Video RAG API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Directories ----------------
UPLOAD_DIR = Path("backend/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

Path("frames").mkdir(exist_ok=True)
Path("ocr").mkdir(exist_ok=True)

app.mount("/frames", StaticFiles(directory="frames"), name="frames")
app.mount("/videos", StaticFiles(directory="backend/uploads"), name="videos")

# ---------------- Progress Store ----------------
progress_store = {}


def update_progress(task_id: str, stage: str, percent: int):
    progress_store[task_id] = {
        "stage": stage,
        "percent": percent,
        "done": percent >= 100,
    }


# ---------------- Processing Pipeline ----------------
def process_pipeline(task_id: str, video_path: str):
    try:

        # 1. Whisper
        update_progress(task_id, "Transcribing audio", 10)
        segments = transcribe_video(video_path)

        # 2. Frames
        update_progress(task_id, "Extracting frames", 30)
        extract_frames(video_path)

        # 3. OCR
        update_progress(task_id, "Running OCR", 50)
        ocr_data = extract_ocr(segments)

        # 4. Text Index
        update_progress(task_id, "Building text index", 70)
        build_index(segments, ocr_data)

        # 5. CLIP Index
        update_progress(task_id, "Building visual index", 90)
        build_clip_index()

        update_progress(task_id, "Completed", 100)

    except Exception as e:

        progress_store[task_id] = {
            "stage": f"Error: {str(e)}",
            "percent": 100,
            "done": True,
        }


# ==========================================================
# Routes
# ==========================================================

@app.get("/")
def root():
    return {
        "message": "Multimodal Video RAG API Running 🚀"
    }


# ---------------- Upload ----------------
@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    filepath = UPLOAD_DIR / file.filename

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "Video uploaded successfully",
        "filename": file.filename,
        "path": str(filepath),
    }


# ---------------- Process ----------------
@app.post("/process")
async def process(filename: str, background_tasks: BackgroundTasks):

    video_path = UPLOAD_DIR / filename

    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Video not found.")

    task_id = str(uuid.uuid4())

    update_progress(task_id, "Queued", 0)

    background_tasks.add_task(
        process_pipeline,
        task_id,
        str(video_path),
    )

    return {
        "message": "Processing started",
        "task_id": task_id,
    }


# ---------------- Live Progress ----------------
@app.get("/progress/{task_id}")
async def progress(task_id: str):

    async def event_generator():

        while True:

            data = progress_store.get(
                task_id,
                {
                    "stage": "Waiting",
                    "percent": 0,
                    "done": False,
                },
            )

            yield f"data: {json.dumps(data)}\n\n"

            if data["done"]:
                break

            await asyncio.sleep(1)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )


# ---------------- Query ----------------
@app.get("/query")
async def query(question: str):
    """
    Returns results exactly in the format
    expected by the Next.js frontend.
    """

    try:

        results = hybrid_search(question)

        return {
            "question": question,
            "results": {
                "text_results": results.get("text_results", []),
                "visual_results": results.get("visual_results", []),
            },
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# ---------------- Health ----------------
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "Multimodal Video RAG",
    }