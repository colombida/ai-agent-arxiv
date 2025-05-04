from ai_agent.utils.arxiv_fetcher import fetch_papers
from database.models import Paper
from sqlalchemy.orm import Session

class RAGComponent:
    def __init__(self):
        self.db = SessionLocal()  # Assicurati di importare SessionLocal da database/__init__.py

    def retrieve(self, query: str) -> str:
        # Cerca nel database i paper rilevanti
        results = self.db.query(Paper).filter(Paper.title.contains(query) | Paper.abstract.contains(query)).limit(3).all()
        return "\n\n".join([f"Titolo: {p.title}\nAbstract: {p.abstract}" for p in results])