import chromadb
from sentence_transformers import SentenceTransformer

print("Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model loaded")

# Persistent DB (this is enough now)
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(name="documents")

# Create 1000 documents
documents = [f"This is document {i}" for i in range(1000)]
metadatas = [{"doc_id": i} for i in range(1000)]
ids = [str(i) for i in range(1000)]

print("Generating embeddings...")
embeddings = model.encode(documents).tolist()

print("Storing in Chroma...")
collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids,
    embeddings=embeddings
)

print("✅ Ingestion complete!")
print("Collection count:", collection.count())