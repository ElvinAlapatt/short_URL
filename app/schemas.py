from pydantic import BaseModel , AnyHttpUrl

class Request(BaseModel):
    long_url : AnyHttpUrl

class Response(BaseModel):
    long_url : str
    short_code : str
    short_url : AnyHttpUrl

    class Config:
        orm_mode = True

