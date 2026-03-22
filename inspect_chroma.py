import os
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()
# Unifying with database.py path
CHROMA_PATH = "data/chroma"

embeddings = GoogleGenerativeAIEmbeddings(model=os.getenv("EMBEDDING_MODEL"))
vector_store = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embeddings
)

# Get all metadata
results = vector_store.get()
print(f"Total entries in Chroma ({CHROMA_PATH}): {len(results['ids'])}")

# Count by filename
filenames = {}
for metadata in results['metadatas']:
    fname = metadata.get('filename', 'Unknown')
    filenames[fname] = filenames.get(fname, 0) + 1

print("\nDocuments in Vector Store:")
for fname, count in filenames.items():
    print(f"- {fname}: {count} chunks")
