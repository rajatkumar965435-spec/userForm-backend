from  pydantic import BaseModel,EmailStr

class User(BaseModel):
    firstname : str
    lastname : str
    emailid : EmailStr
    phonenumber : str
    subjects : str
    about : str



