from fastapi import FastAPI, HTTPException
from app.config.database import users_collection
from app.models.users_models import User
from dotenv import load_dotenv
load_dotenv()
import os
import smtplib
from app.models.emailmodel import EmailRequest
EMAIL= os.getenv("EMAIL")
PASSCODE = os.getenv("PASSCODE")


app = FastAPI()

@app.get("/")
def read_root():
  return{ "fastapi "} 

@app.post("/adduser",tags=["user"])
def adduser(user: User):
 
    existing_user = users_collection.find_one({"email": user.emailid})
    if existing_user:
       
        raise HTTPException(status_code=409, detail="User already exists")
    

    users_collection.insert_one(user.model_dump(exclude_none=True))  # or user.dict() for v1
    return {"msg": "User successfully added"}

# @app.get("/getuser")
@app.get("/getuser",tags=["user"])
def get_user(emailid : str):
    euser = users_collection.find_one({"emailid": emailid})
    print("user", euser)
    if not euser:
        raise HTTPException(status_code=404, detail="User not found")
    
    euser["_id"] = str(euser["_id"])
    
    return {
        "status" : "successfully fetched",
        "data": euser
    }

@app.post("/send-email")
async def send_mail_api(request: EmailRequest):
    message=f"subject:{request.subject}\n\n{request.body}"

    with smtplib.SMTP("smtp.gmail.com",587) as connection:
        connection.starttls() 
        connection.login(user = EMAIL,password=PASSCODE)
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=request.recipiet,
            msg=message
    )
    return{"status":"success",
           "message": f"Email sent to request.recipient"}

