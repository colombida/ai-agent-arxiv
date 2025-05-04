import json
import os
import requests
import numpy as np
import faiss
from sqlalchemy.orm import Session
import openai
from . import models, schemas
from .config import settings

# Initialize OpenAI key
openai.api_key = settings.openai_api_key

# FAISS index global variable
# dimension will be set at runtime after first embedding
index = None
id_map = []  # map faiss internal ids to DB primary keys


def fetch_arxiv(max_results: int = 100):
    """
    Fetches recent papers from arXiv API and returns list of dicts.
    """
    url = 'http://export.arxiv.org/api/query'
    params = {
        'search_query': 'all:electron',
        'start': 0,
        'max_results': max_results
    }
    response = requests.get(url, params=params)
    # parse ATOM XML
    import xml.etree.ElementTree as ET
    root = ET.fromstring(response.content)
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    papers = []
    for entry in root.findall('atom:entry', ns):
        arxiv_id = entry.find('atom:id', ns).text.split('/')[-1]
        title = entry.find('atom:title', ns).text.strip()
        abstract = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
        papers.append({'arxiv_id': arxiv_id, 'title': title, 'abstract': abstract})
    return papers


def embed_text(texts):
    """
    Calls OpenAI to get embeddings for a list of texts.
    Returns numpy array of shape (len(texts), dim).
    """
    response = openai.Embedding.create(
        input=texts,
        engine='text-embedding-ada-002'
    )
    embeds = [datum['embedding'] for datum in response['data']]
    return np.array(embeds, dtype='float32')


def populate_db(db: Session, max_results: int = 100):
    """
    Fetch papers from arXiv, embed abstracts, store in DB and in FAISS index.
    """
    global index, id_map
    papers = fetch_arxiv(max_results)
    abstracts = [p['abstract'] for p in papers]
    embeddings = embed_text(abstracts)

    # Initialize FAISS index if first run
    dim = embeddings.shape[1]
    if index is None:
        index = faiss.IndexFlatL2(dim)
        id_map = []

    count = 0
    for p, emb in zip(papers, embeddings):
        # skip if exists
        obj = db.query(models.Paper).filter_by(arxiv_id=p['arxiv_id']).first()
        if obj:
            continue
        # create record
        record = models.Paper(
            arxiv_id=p['arxiv_id'],
            title=p['title'],
            abstract=p['abstract'],
            vector=json.dumps(emb.tolist())
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        # add to index
        index.add(np.array([emb]))
        id_map.append(record.id)
        count += 1
    return count


def answer_query(request: schemas.QueryRequest, db: Session):
    """
    Embeds user query, searches FAISS index, retrieves top-k papers and returns schema.
    """
    global index, id_map
    if index is None or len(id_map) == 0:
        raise ValueError("Index is empty, please run /populate first.")
    query_emb = embed_text([request.query])[0]
    k = 5
    D, I = index.search(np.array([query_emb]), k)
    results = []
    for idx in I[0]:
        pid = id_map[idx]
        paper = db.query(models.Paper).get(pid)
        results.append(schemas.PaperSchema(
            arxiv_id=paper.arxiv_id,
            title=paper.title,
            abstract=paper.abstract
        ))
    return schemas.QueryResponse(results=results)
