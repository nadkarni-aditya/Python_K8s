from pyclbr import Class

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

class PyDanticResponsePost(PyDanticMediaPost):
    title: str
    content: str
    published: bool

    class Config:
        orm_mode = True 

class PyDanticCreateUser(BaseModel):
    email: EmailStr  
    password: str  

class PyDanticResponseUser(BaseModel):
    email: EmailStr  
    password: str   