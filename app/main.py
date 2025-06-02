from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
import os
from . import models, schemas, crud, database, auth

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db, user)

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not auth.pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = jwt.encode({"sub": user.username}, os.getenv("SECRET_KEY", "secret"), algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}

@app.post("/todos/", response_model=schemas.Todo)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(database.get_db), current_user=Depends(auth.get_current_user)):
    return crud.create_todo(db, todo, current_user.id)

@app.get("/todos/", response_model=list[schemas.Todo])
def read_todos(db: Session = Depends(database.get_db), current_user=Depends(auth.get_current_user)):
    return crud.get_todos(db, current_user.id)