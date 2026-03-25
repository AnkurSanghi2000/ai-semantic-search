from flask import Flask, request, jsonify, render_template
import chromadb
from sentence_transformers import SentenceTransformer
import os

print("🚀 Starting Flask app...")
print("🔥 THIS IS THE CORRECT APP FILE 🔥")

app = Flask(__name__)

# Load model
print("📦 Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ Model loaded")

# Load DB
db_path = os.path.abspath("./chroma_db")
print(f"📁 Using DB path: {db_path}")

client = chromadb.PersistentClient(path=db_path)
collection = client.get_or_create_collection(name="documents")

print(f"📊 Documents in DB: {collection.count()}")

# -----------------------------
# Routes
# -----------------------------

@app.route("/ui")
def ui():
    return render_template("index.html")
    
@app.route("/")
def home():
    return {
        "message": "Semantic Search API is running",
        "documents_indexed": collection.count(),
        "usage": {
            "GET /search?query=your_text": "Browser-friendly",
            "POST /search": {"query": "your_text", "top_k": 5}
        }
    }

@app.route("/init-db", methods=["POST"])
def initialize_database():
    try:
        import time

        print("🚀 Initializing database with 1000 documents...")

        # Prevent duplicate ingestion
        existing_count = collection.count()
        if existing_count > 0:
            return jsonify({
                "message": "Database already initialized",
                "documents_existing": existing_count
            })

        # Prepare documents
        documents = [f"This is document {i}" for i in range(1000)]
        metadatas = [{"doc_id": i} for i in range(1000)]
        ids = [str(i) for i in range(1000)]

        print("📦 Generating embeddings...")
        start_time = time.time()

        embeddings = model.encode(documents).tolist()

        print("💾 Storing in ChromaDB...")
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids,
            embeddings=embeddings
        )

        end_time = time.time()

        return jsonify({
            "message": "✅ Database initialized successfully",
            "documents_added": len(documents),
            "total_documents": collection.count(),
            "time_taken_seconds": round(end_time - start_time, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

        
@app.route("/search", methods=["GET", "POST"])
def search():
    try:
        # -----------------------------
        # Handle GET (browser)
        # -----------------------------
        if request.method == "GET":
            query = request.args.get("query")
            top_k = int(request.args.get("top_k", 5))

        # -----------------------------
        # Handle POST (API)
        # -----------------------------
        else:
            data = request.get_json()
            if not data:
                return jsonify({"error": "JSON body required"}), 400

            query = data.get("query")
            top_k = data.get("top_k", 5)

        # -----------------------------
        # Validate input
        # -----------------------------
        if not query:
            return jsonify({"error": "Query is required"}), 400

        print(f"🔍 Query received: {query}")

        # Embed query
        query_embedding = model.encode([query]).tolist()

        # Search
        results = collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
        )

        response = []

        for i in range(len(results["documents"][0])):
            distance = results["distances"][0][i]
            similarity = 1 - distance

            response.append({
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": round(distance, 4),
                "similarity": round(similarity, 4)
            })

        return jsonify({
            "query": query,
            "top_k": top_k,
            "results": response
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/add", methods=["POST"])
def add_document():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "JSON body required"}), 400

        text = data.get("text")
        doc_id = data.get("doc_id")

        if not text:
            return jsonify({"error": "Document text is required"}), 400

        # Auto-generate ID if not provided
        if not doc_id:
            import uuid
            doc_id = str(uuid.uuid4())
        else:
            doc_id = str(doc_id)

        print(f"➕ Adding document ID: {doc_id}")

        # Generate embedding
        embedding = model.encode([text]).tolist()

        # Insert into Chroma
        collection.add(
            documents=[text],
            metadatas=[{"doc_id": doc_id}],
            ids=[doc_id],
            embeddings=embedding
        )

        return jsonify({
            "message": "Document added successfully",
            "doc_id": doc_id
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/routes")
def list_routes():
    return str(app.url_map)


# -----------------------------
# Run Server
# -----------------------------

if __name__ == "__main__":
    print("🌐 Starting server on port 5001...")
    app.run(host="0.0.0.0", port=5001, debug=True)