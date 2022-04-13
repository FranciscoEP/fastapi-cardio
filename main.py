from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field, EmailStr, AnyHttpUrl, PaymentCardNumber

from fastapi import FastAPI
from fastapi import Body,Query, Path


app = FastAPI()

@app.get("/")
def home():
    return {"message": "Status OK"}

# Models
class Role(Enum):
    admin = "admin"
    user = "user"
    manager = 'manager'
class User(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    email: EmailStr = Field(
        ...,
    
        )
    password: str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    credit_card_number: Optional[PaymentCardNumber] = Field(default=None)
    role: Optional[Role] = Field(default='user') 
    photo_url: Optional[AnyHttpUrl] = Field(default=None)
    is_active: Optional[bool] = Field(default=True)
    class Config:
        schema_extra={
            "John":
            {"first_name": "John",
            "last_name": "Doe",
            "email": "john@doe.com",
            "password": "qwerty",
            "credit_card_number": "4241330108991234",
            "role": "user",
            "photo_url": "https://www.google.com",}
        }
class Location(BaseModel):
    city: Optional[str]= Field(default=None) 
    state: Optional[str]= Field(default=None) 
    country: Optional[str]= Field(default=None) 

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