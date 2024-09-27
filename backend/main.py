from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from models import User 


app = FastAPI()

DATABASE_URL = "sqlite:///./test.db" 
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    nombre: str
    email: str
    password: str
    fecha_nacimiento: str
    direccion: str
    telefono: str
    is_active: bool = True
    fecha_creacion: str

class UserRead(BaseModel):
    id: int
    nombre: str
    email: str
    fecha_nacimiento: str
    direccion: str
    telefono: str
    is_active: bool
    fecha_creacion: str

    class Config:
        orm_mode = True

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=UserRead)
def create_user(user: UserCreate):
    db: Session = SessionLocal()
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user

@app.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int):
    db: Session = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=UserRead)
def update_user(user_id: int, user: UserCreate):
    db: Session = SessionLocal()
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in user.dict().items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    db: Session = SessionLocal()
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    db.close()
    return {"detail": "User deleted successfully"}
