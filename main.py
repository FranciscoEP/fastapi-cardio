from typing import Optional

from pydantic import BaseModel

from fastapi import FastAPI
from fastapi import Body
from fastapi import Query

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
    
# Simple Validations
@app.get('/user/detail')
def get_user_detail(
    age: Optional[str] = Query(None, min_length=1, max_length=50),
    description: str = Query(...)
):
    return {"age": age, "description": description}
