
import cv2
from pathlib import Path


def extract_frames(video_path: str, segments):
    """
    Har transcript segment ke start timestamp par
    ek frame extract karta hai.
    """

    cap = cv2.VideoCapture(video_path)
    Path("frames").mkdir(exist_ok=True)

    saved = 0

    for segment in segments:
        cap.set(cv2.CAP_PROP_POS_MSEC, segment["start"] * 1000)

        success, frame = cap.read()

        if success:
            filename = f"frames/frame_{segment['id']:03d}.jpg"
            cv2.imwrite(filename, frame)
            saved += 1

    cap.release()

    return saved