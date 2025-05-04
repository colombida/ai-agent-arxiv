from pydantic_ai import Agent
from ai_agent.rag import RAGComponent
from config.settings import Settings

class ScientificAgent:
    def __init__(self):
        self.settings = Settings()
        self.rag = RAGComponent()
        self.agent = Agent(model="gpt-4o", system_prompt=self._build_prompt())

    def _build_prompt(self):
        return """Sei un agente AI specializzato in ricerca scientifica. 
        Usa il componente RAG per rispondere a domande su paper specifici."""

    def query(self, question: str):
        context = self.rag.retrieve(question)
        return self.agent.run(f"Domanda: {question}\nContesto: {context}")