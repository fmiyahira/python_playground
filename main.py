from typing import List
from fastapi import FastAPI, HTTPException, Depends, Header, UploadFile, File
import firebase_admin
from firebase_admin import credentials, auth ,storage
from jose import jwt, JWTError
from pydantic import BaseModel
from sqlalchemy import select
from sqlmodel import Session
from database import get_session
from models import Company

import uuid

app = FastAPI()

# Initialize Firebase
cred = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'python-playground-872d6.firebasestorage.app'
})

bucket = storage.bucket()

# Dependency to verify Firebase Authentication Token
def verify_token(authorization: str = Header(...)):
    try:
        # Firebase sends token in the format "Bearer <token>"
        token = authorization.split(" ")[1]
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with Firebase!"}

# Protected route - requires valid Firebase token
@app.get("/profile")
def get_profile(user=Depends(verify_token)):
    return {"user_id": user['uid'], "email": user.get('email')}

# Upload files to Firebase Storage
@app.post("/upload/")
async def upload_file(user=Depends(verify_token), file: UploadFile = File(...)):
    try:
        file_data = await file.read()
        blob = bucket.blob(f"uploads/{uuid.uuid4()}_{file.filename}")
        blob.upload_from_string(file_data, content_type=file.content_type)
        blob.make_public()

        return {"filename": file.filename, "url": blob.public_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

@app.post("/companies/", response_model=Company)
def create_company(company: Company, session: Session = Depends(get_session)):
    session.add(company)
    session.commit()
    session.refresh(company)
    return company

@app.get("/companies/", response_model=List[Company])
def get_companies(session: Session = Depends(get_session)):
    statement = select(Company)
    companies = session.exec(statement).scalars().all()
    return companies

@app.get("/companies/{id}", response_model=Company)
def get_companies(id: int, session: Session = Depends(get_session)):
    statement = select(Company).where(Company.id == id)
    company = session.exec(statement).scalars().first()
    return company

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)