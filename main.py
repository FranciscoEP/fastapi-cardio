from typing import Optional

from pydantic import BaseModel

from fastapi import FastAPI
from fastapi import Body,Query, Path


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

class Location(BaseModel):
    city: str
    state: str
    country: str

# Request and Response body
@app.post('/user/new')
def create_user(user: User = Body(...)):
    return user
    
# Simple Validations
@app.get('/user/detail')
def get_user_detail(
    age: Optional[str] = Query(
        ...,
        title='User age',
        description='User age and it is required. User age must be a number',
         ),
    description: Optional[str] = Query(
        None,
        title="User main description",
        description="User's main's profile description"
    )
    

):
    return {"age": age, "description": description}

@app.get('/user/detail/{user_id}')
def get_user_detail(
    user_id: int = Path(..., 
        gt=0,
        title="User ID",
        description="User's unique identifier",
    )
):
    return {user_id: "Exists"}


#Validations: Request body
@app.put("/user/update/{user_id}")
def update_user(
    user_id: int = Path(..., 
        gt=0,
        title="User ID",
        description="User's unique identifier",
    ),
    user: User = Body(...),
    location: Location = Body(...)
):  
    results = user.dict()
    results.update(location.dict())

    return results