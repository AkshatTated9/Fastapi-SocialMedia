from pydantic import BaseModel,EmailStr
from typing import Optional
class Post(BaseModel):
    title:str
    content:str
    published:bool =True #Assigning Default Value, Thus if user does not provides the value it will automatically consider it true

class Createpost(Post):
    pass
class Returnuser(BaseModel):
    email:EmailStr
    id:int
    class Config:
        orm_mode=True
class Returnpost(Post):
    id:int
    owner_id:int
    owner:Returnuser
    class Config:
        orm_mode=True

class Usercreate(BaseModel):
    email:EmailStr
    password:str



class User(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str
    class Config:
        orm_mode=True

class Returntoken(BaseModel):
    id:Optional[int]
    