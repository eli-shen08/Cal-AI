<div align="center">

```
██████╗  █████╗  ██████╗    ███████╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗
██╔══██╗██╔══██╗██╔════╝    ██╔════╝╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔════╝████╗ ████║
██████╔╝███████║██║  ███╗   ███████╗ ╚████╔╝ ███████╗   ██║   █████╗  ██╔████╔██║
██╔══██╗██╔══██║██║   ██║   ╚════██║  ╚██╔╝  ╚════██║   ██║   ██╔══╝  ██║╚██╔╝██║
██║  ██║██║  ██║╚██████╔╝   ███████║   ██║   ███████║   ██║   ███████╗██║ ╚═╝ ██║
╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚══════╝   ╚═╝   ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═╝
```

### *A production-grade Retrieval-Augmented Generation pipeline — from document ingestion to grounded AI answers*

---

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat-square&logo=fastapi&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-RAG-1C3C3C?style=flat-square&logo=chainlink&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-FF6F00?style=flat-square)
![Groq](https://img.shields.io/badge/Groq-llama--3.3--versatile-F55036?style=flat-square)
![Ollama](https://img.shields.io/badge/Ollama-nomic--embed--text-white?style=flat-square)
![n8n](https://img.shields.io/badge/n8n-Workflow-EA4B71?style=flat-square&logo=n8n&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerised-2496ED?style=flat-square&logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

</div>

---

## What Is This?

**RAG System** is a fully local, end-to-end **Retrieval-Augmented Generation** pipeline that lets you ask natural-language questions against your own documents — and get precise, grounded answers powered by a large language model.

Rather than hallucinating from its training data, the system first **retrieves the most relevant chunks** from your ingested document corpus, then hands them to an LLM as live context. The result is answers you can actually trust.

> **No cloud lock-in. No leaking your documents. Everything runs on your machine.**

---

## ✨ Highlights

| | |
|---|---|
| 🔍 **Semantic Search** | Top-7 chunk retrieval via cosine similarity on dense vector embeddings |
| 🧠 **Smart Embeddings** | `nomic-embed-text` via Ollama — a best-in-class local embedding model |
| ⚡ **Ultra-Fast Inference** | `llama-3.3-versatile` on Groq's LPU — near-instant LLM responses |
| 📄 **Robust Ingestion** | Docling parses PDFs, DOCX, HTML, and more into clean structured text |
| 🔗 **Orchestration Layer** | n8n sits between the UI and backend, enabling visual workflow control |
| 🗄️ **Persistent Vector Store** | ChromaDB persists embeddings to disk — no re-indexing on restart |
| 🎛️ **Clean Frontend** | Streamlit UI — simple, fast, no JavaScript required |
| 🐳 **Containerised** | n8n runs in Docker; everything else is local Python |

---

## 🏗️ Architecture

The system is divided into three logical layers:

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND  (localhost:8501)            │
│                      Streamlit UI                        │
│              User types query → clicks Submit            │
└──────────────────────────┬──────────────────────────────┘
                           │  POST {"query": "..."}
                           ▼
┌─────────────────────────────────────────────────────────┐
│               n8n ORCHESTRATION  (Docker :5678)          │
│                                                          │
│   [Webhook Node]  →  [HTTP Request Node]  →              │
│   Receives POST       Forwards to FastAPI                │
│   on /webhook/rag-query  (host.docker.internal:8000)     │
│                                                          │
│   [Respond to Webhook]  ←  JSON response back            │
└──────────────────────────┬──────────────────────────────┘
                           │  POST {"query": "..."}
                           ▼
┌─────────────────────────────────────────────────────────┐
│                RAG STACK  (localhost:8000)               │
│                                                          │
│   FastAPI  →  LangChain RetrievalQA  →  ChromaDB         │
│   endpoint    embeds query               vector search   │
│               (nomic-embed-text)         top-7 chunks    │
│                    │                                     │
│                    └──────────────────────────────────── │
│                    ▼                                     │
│              Groq LLM (llama-3.3-versatile)              │
│              Generates grounded answer                   │
│                                                          │
│   Response: {"response": {"content": "..."}}             │
└─────────────────────────────────────────────────────────┘
```

### Full Query-to-Response Flow

```
User Query
    │
    ▼  POST /webhook/rag-query
[n8n Webhook Node]          ← Docker :5678
    │
    ▼  $json.body.query
[n8n HTTP Request Node]     → POSTs to host.docker.internal:8000
    │
    ▼  POST {"query": "..."}
[FastAPI Endpoint]          ← @app.post("/") validates QueryModel
    │
    ▼  calls get_rag_response()
[LangChain RetrievalQA]     ← embeds the query via nomic-embed-text
    │              │
    ▼              ▼
[ChromaDB]     [Groq LLM — llama-3.3-versatile]
Top-7 chunks   Generates answer from retrieved context
    │              │
    └──── combined ┘
              │
              ▼
        Response built
   {"response": {"content": "..."}}
              │
              ▼
[n8n Respond to Webhook]    → passes JSON back to Streamlit
              │
              ▼
[Streamlit]   st.info(data["response"]["content"])
              │
              ▼
         Answer displayed ✅
```

---

## 🧰 Tech Stack

### Document Ingestion Pipeline

| Tool | Role |
|------|------|
| **Docling** | Parses raw documents (PDF, DOCX, HTML, Markdown) into clean text |
| **nomic-embed-text** (Ollama) | Generates dense vector embeddings for each text chunk |
| **Tokenizer** (from nomic-embed-text) | Splits documents into token-aware chunks — no mid-sentence cuts |
| **ChromaDB** | Stores and persists embedding vectors with metadata on disk |

### Query & Retrieval Stack

| Tool | Role |
|------|------|
| **LangChain** `RetrievalQA` | Orchestrates embed → retrieve → generate in a single chain |
| **ChromaDB** | Performs cosine similarity search; returns top-7 relevant chunks |
| **nomic-embed-text** (Ollama) | Also used at query time to embed the incoming question |

### LLM Inference

| Tool | Role |
|------|------|
| **Groq API** | Cloud LPU inference endpoint — extremely low latency |
| **llama-3.3-versatile** | Meta's Llama 3.3 model — strong reasoning, instruction-following |

### Orchestration & API

| Tool | Role |
|------|------|
| **n8n** (Docker) | Visual workflow engine; handles webhook → HTTP request → respond |
| **FastAPI** | Lightweight Python API on port 8000; validates input via Pydantic |

### Frontend

| Tool | Role |
|------|------|
| **Streamlit** | Python-native UI running on `localhost:8501` |

---

## 📁 Project Structure

```
rag-system/
│
├── ingestion/
│   ├── ingest.py            # Docling document loader + chunker
│   ├── embed_and_store.py   # Embeds chunks → stores in ChromaDB
│   └── documents/           # Drop your source documents here
│
├── api/
│   └── main.py              # FastAPI app — POST / endpoint
│
├── rag/
│   ├── chain.py             # LangChain RetrievalQA chain setup
│   ├── retriever.py         # ChromaDB retriever (top-7 chunks)
│   └── llm.py               # Groq LLM initialisation
│
├── frontend/
│   └── app.py               # Streamlit UI
│
├── n8n/
│   └── workflow.json        # Exported n8n workflow (import this)
│
├── chroma_db/               # Persisted ChromaDB vector store (git-ignored)
│
├── .env                     # API keys and config (see below)
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- [Ollama](https://ollama.ai) installed and running locally
- [Docker](https://docker.com) (for n8n)
- A [Groq API key](https://console.groq.com)

### 1 — Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/rag-system.git
cd rag-system
```

### 2 — Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3 — Pull the embedding model

```bash
ollama pull nomic-embed-text
```

### 4 — Configure environment variables

Create a `.env` file in the root:

```env
GROQ_API_KEY=your_groq_api_key_here
CHROMA_PERSIST_DIR=./chroma_db
COLLECTION_NAME=rag_documents
```

### 5 — Ingest your documents

Drop your PDFs, DOCX, or HTML files into `ingestion/documents/`, then run:

```bash
python ingestion/ingest.py
```

This will:
1. Parse each document with **Docling**
2. Chunk the text using the **nomic-embed-text tokenizer**
3. Generate embeddings via **Ollama**
4. Persist everything to **ChromaDB**

### 6 — Start the FastAPI backend

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

### 7 — Start n8n

```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  docker.n8n.io/n8nio/n8n
```

Then open `http://localhost:5678`, import `n8n/workflow.json`, and **activate** the workflow.

### 8 — Launch the Streamlit frontend

```bash
streamlit run frontend/app.py
```

Open `http://localhost:8501` — ask your first question. 🎉

---

## 🔬 How RAG Works (Under the Hood)

Retrieval-Augmented Generation solves a fundamental LLM problem: models only know what was in their training data, and they hallucinate when asked about anything outside it.

**RAG fixes this in three steps:**

**1. Index** — Before any query, documents are parsed, chunked, embedded into high-dimensional vectors, and stored in ChromaDB. Each chunk is a fixed-size, semantically coherent piece of your source text.

**2. Retrieve** — When a user asks a question, the question is embedded using the same model (`nomic-embed-text`). ChromaDB finds the 7 stored chunks whose vectors are most similar — these are the most semantically relevant passages from your documents.

**3. Generate** — The retrieved chunks are injected into the LLM prompt as context. Llama 3.3 on Groq reads both the question and the retrieved evidence, then generates a grounded answer that cites real content from your documents.

```
Query ──embed──▶ vector ──similarity search──▶ top-7 chunks
                                                     │
                                              inject as context
                                                     │
                                                     ▼
                                           LLM generates answer
```

---

## ⚙️ Configuration Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Your Groq API key | — |
| `CHROMA_PERSIST_DIR` | Where ChromaDB saves its data | `./chroma_db` |
| `COLLECTION_NAME` | ChromaDB collection name | `rag_documents` |
| `TOP_K` | Number of chunks to retrieve | `7` |
| `OLLAMA_BASE_URL` | Ollama API base URL | `http://localhost:11434` |

---

## 🗺️ Roadmap

- [ ] Multi-document source support (web scraping, Notion, Google Drive)
- [ ] Streaming LLM responses to the Streamlit UI
- [ ] Source citation display (which document chunks were used)
- [ ] Hybrid search (BM25 + dense vectors via ChromaDB)
- [ ] Evaluation harness (RAGAS metrics)
- [ ] Docker Compose for one-command startup

---

## 🤝 Contributing

Contributions are welcome. Please open an issue first to discuss what you'd like to change, then submit a pull request against `main`.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

Built with ☕ and too many vector dimensions.

*If this project helped you, please consider giving it a ⭐*

</div>
