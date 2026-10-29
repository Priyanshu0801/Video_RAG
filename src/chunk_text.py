
from pathlib import Path

# Transcript file read karo
text = Path("transcripts/sample.txt").read_text(encoding="utf-8")

# Har chunk me 8 words honge
chunk_size = 8
words = text.split()

chunks = []

# 8-8 words ke chunks banao
for i in range(0, len(words), chunk_size):
    chunk = " ".join(words[i:i+chunk_size])
    chunks.append(chunk)

# Output folder
Path("transcripts/chunks").mkdir(parents=True, exist_ok=True)

# Har chunk alag file me save karo
for i, chunk in enumerate(chunks):
    Path(f"transcripts/chunks/chunk_{i}.txt").write_text(chunk, encoding="utf-8")

print(f"Total chunks created: {len(chunks)}")