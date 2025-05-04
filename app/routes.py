from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import services, schemas, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/populate')
async def populate(max_results: int = 100, db: Session = Depends(get_db)):
    try:
        count = services.populate_db(db, max_results)
        return {"imported": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/query', response_model=schemas.QueryResponse)
async def query(request: schemas.QueryRequest, db: Session = Depends(get_db)):
    try:
        return services.answer_query(request, db)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))