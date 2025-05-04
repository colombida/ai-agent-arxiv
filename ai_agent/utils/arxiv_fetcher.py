import arxiv
from database.models import Paper
from sqlalchemy.orm import Session

def fetch_papers(topic: str, db: Session):
    search = arxiv.Search(
        query=topic,
        max_results=10,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    for result in search.results():
        paper = Paper(
            title=result.title,
            abstract=result.summary,
            url=result.link.href,
            published=result.published.isoformat()
        )
        db.merge(paper)  # Evita duplicati
    db.commit()