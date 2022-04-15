from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field, EmailStr, AnyHttpUrl, PaymentCardNumber

from fastapi import FastAPI
from fastapi import Body,Query, Path, status,Form



# Models
class Role(Enum):
    admin = "admin"
    user = "user"
    manager = 'manager'
class User_Base(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        )
    email: EmailStr = Field(
        ...,
    
        )
    credit_card_number: Optional[PaymentCardNumber] = Field(default=None)
    role: Optional[Role] = Field(default='user') 
    photo_url: Optional[AnyHttpUrl] = Field(default=None)
    is_active: Optional[bool] = Field(default=True)
    class Config:
        schema_extra={
            "example":
            {"first_name": "John",
            "last_name": "Doe",
            "email": "john@doe.com",
            "password": "qwerty123",
            "credit_card_number": "5559240894706825",
            "role": "user",
            "photo_url": "https://www.google.com",}
        }

class User_In(User_Base):
    password: str = Field(
        ...,
        min_length=8,
        )

class User_Out(User_Base):
    pass
class Location(BaseModel):
    city: Optional[str]= Field(default=None, example="New York") 
    state: Optional[str]= Field(default=None, example="NY")
    country: Optional[str]= Field(default=None, example="United States") 

class Login_Out(BaseModel):
    username: str = Field(..., max_length=20, example="johndoe")


# Request and Response body
app = FastAPI()

@app.get(path="/", status_code=status.HTTP_200_OK)
def home():
    return {"message": "Status OK"}


@app.post(
    path='/user/new',
    response_model=User_Out,
    status_code=status.HTTP_201_CREATED
    )
def create_user(user: User_In = Body(...)):
    return user
    
# Simple Validations
@app.get(
    path='/user/detail', 
    status_code=status.HTTP_200_OK
    )
def get_user_detail(
    age: Optional[str] = Query(
        ...,
        title='User age',
        description='User age and it is required. User age must be a number',
        example="22" 
         ),
    description: Optional[str] = Query(
        None,
        title="User main description",
        description="User's main's profile description",
        example="Description"
    )
    

):
    return {"age": age, "description": description}

@app.get('/user/detail/{user_id}', status_code=status.HTTP_200_OK)
def get_user_detail(
    user_id: int = Path(..., 
        gt=0,
        title="User ID",
        description="User's unique identifier",
    )
):
    return {user_id: "Exists"}


#Validations: Request body
@app.put("/user/update/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_user(
    user_id: int = Path(..., 
        gt=0,
        title="User ID",
        description="User's unique identifier",
    ),
    user: User_In = Body(...),
    # location: Location = Body(...)
):  
    # results = user.dict()
    # results.update(location.dict())

    return user

@app.post(path="/user/login", response_model=Login_Out, status_code=status.HTTP_200_OK)
def login(
    username: str = Form(...),
    password: str = Form(...),
):
    return Login_Out(username=username)