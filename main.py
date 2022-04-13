from typing import Optional

from pydantic import BaseModel

from fastapi import FastAPI
from fastapi import Body

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Status OK"}

# Models
class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    photo_url: Optional[str] = None
    is_active: Optional[bool] = True


# Request and Response body
@app.post('/user/new')
def create_user(user: User = Body(...)):
    return user
    
