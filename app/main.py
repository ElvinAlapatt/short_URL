from fastapi import FastAPI, status, HTTPException, Depends, Request
from starlette.responses import RedirectResponse
from sqlmodel import Session, select
from . import schemas, logic, models
from .database import engine, create_db_and_tables, get_session
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating database and tables...")
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True ,
    allow_methods = ["*"],
    allow_headers = ["*"]
)
@app.get('/')
def root():
    return {"msg": "URL Shortener API"}

@app.post('/convert', status_code=status.HTTP_201_CREATED, response_model=schemas.Response)
def create_short_url(
    request_data: schemas.Request,
    request: Request,
    db: Session = Depends(get_session)
):

    req_url: str = str(request_data.long_url)

    
    statement = select(models.URL).where(models.URL.long_url == req_url)
    existing_url = db.exec(statement).first()
    if existing_url:
        short_url = f"{str(request.base_url)}{existing_url.short_code}"
        return schemas.Response(
            long_url=existing_url.long_url,
            short_code=existing_url.short_code,
            short_url=short_url
        )

    
    converted_code = logic.convert(6)

    
    while db.exec(select(models.URL).where(models.URL.short_code == converted_code)).first():
        converted_code = logic.convert(6)

    new_entry = models.URL(long_url=req_url, short_code=converted_code)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    
    short_url = f"{str(request.base_url)}{new_entry.short_code}"

    return schemas.Response(
        long_url=new_entry.long_url,
        short_code=new_entry.short_code,
        short_url=short_url
    )

@app.get('/{short_code}')
def get_short_url(short_code : str , db : Session = Depends(get_session)):
    statement = select(models.URL).where(models.URL.short_code == short_code)
    url_entry = db.exec(statement).first()
    if not url_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Short url not found!")
    
    return RedirectResponse(url = url_entry.long_url , status_code=status.HTTP_301_MOVED_PERMANENTLY)