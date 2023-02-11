from datetime import datetime, timedelta
from typing import Optional, Union
from fastapi import Depends, FastAPI, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import uvicorn
import crud, models, schemas
from database import SessionLocal, engine
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import os
from jose import JWTError, jwt
from passlib.context import CryptContext
from ML.ocr import detect_text, translate, summarize
import shutil
from pathlib import Path
serviceaccountkeys = os.environ.get('SERVICEACCOUNTKEYS')
from news.fetch_news import NewsRequest, fetch_news
import json

models.Base.metadata.create_all(bind=engine)

SECRET_KEY = "1ca41e02f535fd037babb6c4971a60cd27830ea9aec390a5dc0f2c366133aee1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300



app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# login

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return schemas.UserInDB(**user_dict)




def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    db = get_db()
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user(db, user_id=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    db = get_db()
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: schemas.User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]

@app.post("/users/register")
async def register_user(user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    user = crud.create_user(db=SessionLocal(), user=user)
    return user

def authenticate_user(email: str, password: str):
    db = SessionLocal()
    user = crud.get_user_by_email(db, email=email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user





# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root(token: str = Depends(oauth2_scheme)):
    return {"token": token}


@app.get("/translate-to-en")
async def translate_to_en(text: str):
    return {"translated_text": translate(text, "en")}

@app.get("/translate-to-ja")
async def translate_to_ja(text: str):
    return {"translated_text": translate(text, "ja")}

@app.get("/translate-to-kr")
async def translate_to_kr(text: str):
    return {"translated_text": translate(text, "kr")}


@app.post("/images-OCR/")
async def image_ocr(file: UploadFile = File(...)):
    file_location = f"files/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    text = detect_text(file_location)
    text_translated, lang = translate(text, "en")
    summary = summarize(text_translated)
    text_original = translate(summary, lang)
    return {"text": text_original, "summary": summary}

@app.post("/fetch-news")
async def fetch_news_api(news_req: NewsRequest) -> list[str]:
    titles = fetch_news(news_req)
    return titles


# ML models

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
