# 🩺 Intelligent Medical RAG Assistant

A full-stack Retrieval-Augmented Generation (RAG) web application for querying a collection of medical documents and generating grounded answers using retrieved document context and a local LLM.

The project uses a text-only RAG pipeline: medical PDF documents are extracted, split into chunks, embedded into a vector store, retrieved for user questions, and passed to a local Ollama model to generate answers based only on the retrieved context.

---

## 🚀 Architecture

```text
Medical PDF Documents
        │
        ▼
Text Extraction
        │
        ▼
Chunking
(800 characters / 150 overlap)
        │
        ▼
Sentence Transformers
(all-MiniLM-L6-v2)
        │
        ▼
ChromaDB Vector Store
(medical_rag)
        │
        ▼
FastAPI Backend
        │
        ├── /health
        │
        └── /api/query
                │
                ▼
        Retrieve Relevant Chunks
                │
                ▼
        Ollama LLM
        llama3.2:3b
                │
                ▼
        Grounded Answer + Sources
                │
                ▼
        Streamlit Frontend
```

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **FastAPI** — backend REST API
- **Streamlit** — frontend interface
- **ChromaDB** — vector database
- **Sentence Transformers** — text embeddings
- **Ollama** — local LLM inference
- **llama3.2:3b** — selected local language model
- **Pydantic** — API request/response validation
- **Pytest** — backend testing
- **Docker** — backend containerization

---

## 📂 Project Structure

```text
Medical-RAG-Assistant/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       └── query.py
│   │   │
│   │   ├── core/
│   │   │   └── config.py
│   │   │
│   │   ├── schemas/
│   │   │   └── query.py
│   │   │
│   │   ├── services/
│   │   │   ├── generation.py
│   │   │   └── retrieval.py
│   │   │
│   │   ├── utils/
│   │   │   └── logging_config.py
│   │   │
│   │   └── main.py
│   │
│   ├── data/
│   │   └── vector_store/
│   │
│   ├── tests/
│   │   └── test_query.py
│   │
│   ├── .env.example
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── app.py
│   ├── api_client.py
│   └── requirements.txt
│
├── notebooks/
│   └── rag_pipeline.ipynb
│
├── .gitignore
└── README.md
```

---

## 📚 Domain & Dataset

The RAG system is designed for querying medical documents.

The final dataset contains **4 medical PDF documents**:

- `Autoimmune_disease.pdf`
- `Cardiovascular_disease.pdf`
- `Diabetes.pdf`
- `Hypertension.pdf`

The documents contain approximately **146 pages** in total.

An unrelated `Machine_learning.pdf` document was excluded from the final medical corpus.

The PDFs contain extractable text, so OCR was not required.

---

## 🔄 RAG Pipeline

### 1. Document Loading

The medical PDF documents are loaded and their text is extracted using `pypdf`.

### 2. Chunking

The extracted text is divided into chunks using:

- **Chunk size:** 800 characters
- **Overlap:** 150 characters

A word-boundary-aware approach is used to avoid unnecessarily splitting words.

The final corpus contains approximately **770 chunks**.

### 3. Embeddings

Each chunk is converted into an embedding using:

```text
all-MiniLM-L6-v2
```

The resulting embeddings have **384 dimensions**.

### 4. Vector Store

The embeddings and document chunks are stored in a persistent ChromaDB collection:

```text
medical_rag
```

The persisted vector store contains **770 items**.

### 5. Retrieval

For every user question, the system retrieves the most relevant document chunks from ChromaDB.

The backend retrieves the top **3** chunks before generating the answer.

### 6. Generation

The retrieved context is passed to the local Ollama model:

```text
llama3.2:3b
```

The generation prompt instructs the model to use only the retrieved medical context and to state that the information is unavailable when the provided context is insufficient.

---

## 🤖 Model Selection

The project uses:

```text
Ollama — llama3.2:3b
```

This model was selected for local inference and stable execution in the project environment.

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/renadaelsalamony-wq/Medical-RAG-Assistant.git
cd Medical-RAG-Assistant
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate
```

### 3. Install Backend Dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Install Frontend Dependencies

```bash
pip install -r frontend/requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file based on:

```text
backend/.env.example
```

The backend configuration includes:

```text
OLLAMA_MODEL=llama3.2:3b
VECTOR_STORE_PATH=backend/data/vector_store
```

The frontend uses:

```text
API_BASE_URL=http://127.0.0.1:8000
```

Make sure Ollama is installed and the selected model is available locally.

---

## 🏃 Running the Application

### Step 1 — Start the Backend

From the project root:

```bash
uvicorn backend.app.main:app --reload --port 8000
```

The backend will be available at:

```text
http://localhost:8000
```

FastAPI Swagger documentation:

```text
http://localhost:8000/docs
```

### Step 2 — Start the Frontend

Open a second terminal, activate the virtual environment, and run:

```bash
streamlit run frontend/app.py
```

The Streamlit application will open at:

```text
http://localhost:8501
```

The frontend communicates with the backend using the `API_BASE_URL` environment variable.

---

## 🔌 API Reference

### GET `/health`

Checks whether the backend is running.

Example:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "ok"
}
```

### POST `/api/query`

Sends a medical question to the RAG pipeline.

Request:

```json
{
  "question": "What are common symptoms of diabetes?"
}
```

Example using curl:

```bash
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"What are common symptoms of diabetes?\"}"
```

Response:

```json
{
  "answer": "Generated answer based on the retrieved medical context.",
  "sources": [
    "Diabetes.pdf"
  ]
}
```

---

## 🧪 Evaluation

The RAG pipeline was evaluated using **10 medical questions** covering the indexed documents.

The evaluation table in the notebook records:

- Question
- Source document
- Generated answer
- Correctness

### Evaluation Result

| Metric | Result |
|---|---:|
| Questions evaluated | 10 |
| Correct answers | 10 |
| Accuracy | **100%** |

The evaluation also identified minor relevance limitations in some retrieved results, while the manually assessed answers were marked as correct.

---

## 🧪 Backend Tests

The backend includes tests for:

### Happy Path

Verifies that a valid query is processed successfully.

### Invalid Input

Verifies that invalid input is rejected with the expected validation response.

Run the tests with:

```bash
python -m pytest backend/tests/test_query.py -v
```

Current result:

```text
2 passed
```

---

## 📓 RAG Pipeline Notebook

The complete RAG development workflow is documented in:

```text
notebooks/rag_pipeline.ipynb
```

The notebook includes:

- Loading and inspecting the medical PDFs
- Text extraction
- Chunking
- Embedding generation
- ChromaDB vector store creation
- Retrieval testing
- Prompt template
- Evaluation using 10 questions
- Failure/relevance analysis
- Vector store export and reload verification

---

## 📸 Application Screenshots

### 1. Medical Query — Happy Path

The assistant retrieves relevant medical information from the indexed documents and generates a grounded response with source information.

<img width="1600" height="863" alt="image" src="https://github.com/user-attachments/assets/44037283-9d59-4f27-933a-704858a6d74c" />

<img width="1600" height="859" alt="image" src="https://github.com/user-attachments/assets/a112a966-5e48-4194-9577-735c4afbdd7f" />

### 2. Additional Application Examples

<img width="1600" height="852" alt="image" src="https://github.com/user-attachments/assets/b500a994-2190-400a-af17-dedbc6266c0a" />

<img width="1600" height="862" alt="image" src="https://github.com/user-attachments/assets/e8767c12-ca8d-4044-9abc-a352c932fec5" />

<img width="1600" height="862" alt="image" src="https://github.com/user-attachments/assets/2da5c1bf-0b1f-4bd9-aaee-7504ddd3cee9" />

### 3. General / Out-of-Domain Query Handling

The application is designed to remain grounded in the retrieved medical document context rather than intentionally answering from outside knowledge.

<img width="1600" height="858" alt="image" src="https://github.com/user-attachments/assets/8431e11f-de2c-4fed-a7d3-718051ad0b84" />

---

## 🐳 Docker

The backend includes a Dockerfile for containerization.

Build the backend image:

```bash
docker build -f backend/Dockerfile -t medical-rag-backend .
```

Run the container:

```bash
docker run -p 8000:8000 medical-rag-backend
```

---

## 🔐 Environment Variables

| Variable | Description | Example |
|---|---|---|
| `OLLAMA_MODEL` | Ollama model used for answer generation | `llama3.2:3b` |
| `VECTOR_STORE_PATH` | Path to the persisted ChromaDB vector store | `backend/data/vector_store` |
| `API_BASE_URL` | Backend URL used by the frontend | `http://127.0.0.1:8000` |

Environment files containing secrets or local configuration should not be committed to GitHub.

---

## ⚠️ Disclaimer

This project is an educational RAG application and is not a substitute for professional medical advice, diagnosis, or treatment.

---

## 👥 Project

This project was developed as a graduation project demonstrating an end-to-end Retrieval-Augmented Generation system, including document processing, embeddings, vector search, local LLM generation, backend API development, frontend integration, testing, and deployment preparation.