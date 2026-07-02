from pydantic import BaseModel

class PyDanticMediaPost(BaseModel):
    title: str
    content: str
    published: bool = True #setting a default value if post call doesn't have this
    # rating: Optional[int] = None