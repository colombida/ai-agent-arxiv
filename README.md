# AI Agent per arXiv Papers

Repository per un agente AI che utilizza RAG (Retrieval-Augmented Generation) per rispondere a domande su paper scientifici, integrando dati da [arXiv](https://arxiv.org/) e un database PostgreSQL.

## 1. Clone the repository
```bash
git clone https://github.com/colombida/ai-agent-arxiv.git
cd ai-agent-arxiv
```

## 2. Create and configure `.env`
Create a file named `.env` in the root directory with the following variables:
```
ARXIV_API_KEY=<your_arxiv_api_key>
DATABASE_URL=postgresql://user:password@host:port/dbname
OPENAI_API_KEY=<your_openai_api_key>
```

## 3. Install dependencies
```bash
pip install -r requirements.txt
```

## 4. Initialize the database
Ensure your PostgreSQL instance is running and the specified database exists. The tables will be auto-created at startup.

## 5. Run the FastAPI server
```bash
uvicorn app.main:app --reload
```
L’API sarà disponibile su `http://127.0.0.1:8000/api`.

## 6. Populate the vector database
Invoca l’endpoint `/api/populate` per importare e indicizzare i paper:
```bash
curl -X POST "http://127.0.0.1:8000/api/populate?max_results=50"
```

## 7. Query the agent
Invia richieste di ricerca all’endpoint `/api/query`:
```bash
curl -X POST "http://127.0.0.1:8000/api/query" -H "Content-Type: application/json" -d '{"query":"deep learning"}'
```
Riceverai un JSON con i risultati più rilevanti.

## 8. Eseguire i test
```bash
pytest
```

---
Questa guida copre i passi minimi per avviare e utilizzare l’agente RAG basato su FastAPI e Pydantic.
