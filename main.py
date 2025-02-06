from fastapi import FastAPI, HTTPException, Depends, Header
import firebase_admin
from firebase_admin import credentials, auth
from jose import jwt, JWTError
from pydantic import BaseModel

app = FastAPI()

# Initialize Firebase
cred = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(cred)

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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)