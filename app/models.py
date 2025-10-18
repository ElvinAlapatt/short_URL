from sqlmodel import SQLModel , Field
from datetime import datetime
class URL(SQLModel , table=True):
    id : int | None = Field(default=None , primary_key=True)
    long_url : str
    short_code : str
    created_at : datetime = Field(default_factory=datetime.now,nullable=False)
