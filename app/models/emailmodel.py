from pydantic import BaseModel,EmailStr


class EmailRequest(BaseModel):
    recipiet: EmailStr
    subject: str
    body: str
    






