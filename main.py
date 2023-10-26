from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware  # Import the CORSMiddleware
from pydantic import BaseModel
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import sys

sys.dont_write_bytecode = True

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class Client(BaseModel):
    id: int
    name: str
    age: int

@app.get("/clients")
def read_api(db: Session = Depends(get_db)):
    print('get clients')
    clients = db.query(models.Client).all()
    return clients

@app.post("/clients")
def create_api(client: Client, db: Session = Depends(get_db)):
    print(client)
    if db.query(models.Client).filter(models.Client.id == client.id).first():
        raise HTTPException(status_code=400, detail="Client ID already exists")
    new_client = models.Client(id=client.id, name=client.name, age=client.age)
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client
