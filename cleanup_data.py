import shutil
import os

CHROMA_PATH = "data/chroma"
CHROMA_PATH_ALT = "data/chromadb"

for path in [CHROMA_PATH, CHROMA_PATH_ALT]:
    if os.path.exists(path):
        print(f"Clearing {path}...")
        shutil.rmtree(path)
        print("Done.")
    else:
        print(f"Path not found: {path}")

# Also clear the uploads folder to be safe
UPLOAD_DIR = "uploads"
if os.path.exists(UPLOAD_DIR):
    print(f"Clearing {UPLOAD_DIR}...")
    for f in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
    print("Done.")
