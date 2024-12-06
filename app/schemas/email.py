from pydantic import BaseModel
from typing import List

class EmailBase(BaseModel):
    recipient: str
    subject: str
    message: str

class EmailSend(EmailBase):
    pass
