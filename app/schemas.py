from pyclbr import Class
from typing import Optional

from pydantic import BaseModel, EmailStr
from datetime import datetime

class PyDanticMediaPost(BaseModel):
    title: str
    content: str
    published: bool = True #setting a default value if post call doesn't have this
    # rating: Optional[int] = None

class PyDanticSendPost(PyDanticMediaPost):
    pass    

class PyDanticUpdatePost(PyDanticMediaPost):
    pass


class PyDanticCreateUser(BaseModel):
    email: EmailStr  
    password: str  

class PyDanticResponseUser(BaseModel):
    email: EmailStr  
    created_at: datetime

    class Config:
        from_attributes = True 

class userlogin(PyDanticCreateUser):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]

class PyDanticResponsePost(PyDanticMediaPost):
    id: int
    created_at: datetime
    owner_id: int
    owner: PyDanticResponseUser
    
    class Config:
        from_attributes = True 