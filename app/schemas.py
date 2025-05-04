from pydantic import BaseModel
from typing import List, Optional

class PaperSchema(BaseModel):
    arxiv_id: str
    title: str
    abstract: str

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    results: List[PaperSchema]