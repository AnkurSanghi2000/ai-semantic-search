# AI Semantic Search

A simple semantic search application built using:
- Flask (API layer)
- ChromaDB (vector database)
- Sentence Transformers (embeddings)

This project allows you to:
- Store documents with embeddings
- Perform semantic (cosine similarity) search
- Dynamically add new documents via API

---

## 🚀 Features

- 🔍 Semantic search using embeddings
- ➕ Add documents via API
- 📦 Persistent vector storage (ChromaDB)
- ⚡ Fast retrieval of top-k similar documents
- 🌐 REST API (Flask)

---

## 📁 Project Structure

ai-semantic-search/
│
├── app.py              # Flask API
├── ingest.py           # Initial ingestion script
├── requirements.txt    # Dependencies
├── chroma_db/          # Auto-created vector DB
├── venv/               # Virtual environment (ignored)
└── README.md

---

## ⚙️ Setup Instructions (Step-by-Step)

### 1. Clone the repository

```bash
git clone git@github.com:AnkurSanghi2000/ai-semantic-search.git
cd ai-semantic-search
```

### 2. Create virtual environment
```bash
python3 -m venv venv
```
### 3. Activate environment
```bash
python3 -m venv venv
```
### 4. Install dependencies
```bash
pip install -r requirements.txt
```
### 5. Run ingestion script
```bash
python ingest.py
```
### 6. Start Flask server
```bash
python app.py
```
Server runs at
http://127.0.0.1.5001

## 📡 API Usage
### 🏠 Home
```bash
GET /
```
### 🔍 Search (GET)
```bash
GET /search?query=your-text&top_k=5
```
### Example:
```bash
curl "http://127.0.0.1/search?query=Document007&top_k=5"
```
### 🔍 Search (POST)
```bash
curl -X POST http://127.0.0.1:5001/search \
-H "Content-Type: application/json" \
-d '{"query": "document 10", "top_k": 5}'
```
### ➕ Add Document
```bash
curl -X POST http://127.0.0.1:5001/add \
-H "Content-Type: application/json" \
-d '{"text": "This is a new document text being added to the db"}'
```
### 📊 Example Response
```json
{
  "query": "sepsis",
  "top_k": 5,
  "results": [
    {
      "content": "Sepsis is a life-threatening condition",
      "metadata": {"doc_id": "123"},
      "distance": 0.12,
      "similarity": 0.88
    }
  ]
}
```
### 🧠 How It Works
	1.	Convert documents → embeddings
	2.	Store embeddings in ChromaDB
	3.	Convert query → embedding
	4.	Compute cosine similarity
	5.	Return top-k closest matches

### 🗂️ Important Notes
	•	chroma_db/ is created automatically
	•	Do NOT commit:
	•	venv/
	•	chroma_db/
