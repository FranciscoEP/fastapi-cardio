from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field, EmailStr, AnyHttpUrl, PaymentCardNumber

from fastapi import (
    FastAPI, 
    Body,
    Query,
    Path, 
    status,
    Form,
    Header,
    Cookie, 
    UploadFile, 
    File,
    HTTPException,
    )




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

@app.get(
    path="/", 
    status_code=status.HTTP_200_OK,
    tags=['Home']
)
def home():
    return {"message": "Status OK"}


@app.post(
    path='/user/new',
    response_model=User_Out,
    status_code=status.HTTP_201_CREATED,
    tags=['Users'],
    summary="Create user in the app"
)
def create_user(user: User_In = Body(...)):
    """
    Create a new user

    This path operation creates a user in the app and store the information in the database.

    Parameters:
    - Request body parameter:
        - **user: User** -> User model with first_name, last_name, email, password, credit_card_number, role, photo_url, is_active

    Returns a user created with first_name, last_name, email, credit_card_number, role, photo_url, is_active attributes.
    
    
    """
    return user
    
# Simple Validations
users = [1, 2, 3, 4, 5] 

@app.get(
    path='/user/detail', 
    status_code=status.HTTP_200_OK,
    tags=['Users']
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
    """
    Show user's information

    This path operation display the user's information the app.

    Parameters:
    - Request body parameter:
        - **age: Str** -> Attribute that returns user's Age. String type.
        - **description: Str** -> Attribute that returns user's description. String type.

    Returns user's description and age.
    """
    return {"age": age, "description": description}

@app.get(
    path='/user/detail/{user_id}', 
    status_code=status.HTTP_200_OK,
    tags=['Users'])
def get_user_detail(
    user_id: int = Path(..., 
        gt=0,
        title="User ID",
        description="User's unique identifier",
    )
):
    """
    Show user's information

    This path operation display the user's information in the app.

    Parameters:
    - Request body parameter:
        - **user_id: Int** Mandatory-> Attribute that identifies the user by Id. Int type. Primary key.

    Returns user's id.
    """
    if user_id not in users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {user_id: "Exists"}


#Validations: Request body
@app.put(
    path="/user/update/{user_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    tags=['Users'])
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
    """
    Update user's information

    This path operation updates the user's information in the app.

    Parameters:
    - Request body parameter:
        - **user_id: Int** Mandatory-> Attribute that identifies the user by Id. Int type. Primary key.
        - **user: User** Mandatory-> Attributes that are going to be updated. User model with first_name, last_name, email, password, credit_card_number, role, photo_url, is_active

    Returns User Information updated.
    """
    return user

@app.post(
    path="/user/login",
    response_model=Login_Out,
    status_code=status.HTTP_200_OK,
    tags=['Users']
    )
def login(
    username: str = Form(...),
    password: str = Form(...),
):  
    """
    Log in the user in App

    This path operation log in the user in the app.

    Parameters:
    - Request body parameter:
        - **username: Str** Mandatory-> Attribute that identifies the user by username. String type.
        - **password: User** Mandatory-> Attribute that let user get in the app. String type.

    Returns username.
    """
    return Login_Out(username=username)

# Cookies and headers parameters
@app.post(
    path="/contact", 
    status_code=status.HTTP_200_OK,
    tags=['Contact'])
def contact(
    first_name: str = Form(
    ...,
    max_length=20,
    min_length=1
    ),
    last_name: str = Form(
    ...,
    max_length=20,
    min_length=1
    ),
    email: EmailStr = Form(
    ...,
    ),
    message: str = Form(
    ..., 
    min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str]= Cookie(default=None)

):
    """
    Input a possible user information from a Contact Form.

    This path operation obtain possible user information from a Contact Form.

    Parameters:
    - Request body parameter:
        - **first_name: Str** Mandatory-> Attribute that identifies the user by its first name. String type.
        - **last_name: Str** Mandatory->  Attribute that identifies the user by its last name. String type.
        - **email: Str** Mandatory-> Attribute that identifies the user by its email. String type.
        - **user_agent: Header** Mandatory-> Attribute that displays the user_agent generated by user. Header type.
        - **ads: Cookie** Mandatory-> Attribute that displays cookies information. Cookie type.

    Returns the user_agent.
    """
    return user_agent


@app.post(
    path="/post-image",
    status_code=status.HTTP_200_OK,
    tags=['Images']
)
def post_image(
    image: UploadFile = File(...)
):
    """
    Receives an image file.

    This path operation obtain an image file and returns the name, the format and its size.

    Parameters:
    - Request body parameter:
        - **image: Upload File** Mandatory-> Attribute thet receives an image file. File type.

    Returns the image name, the format and its size.
    """
    return {"Filename": image.filename,
    "Format": image.content_type,
    "Size(kb)": round(len(image.file.read()) / 1024, 2)
    }

    