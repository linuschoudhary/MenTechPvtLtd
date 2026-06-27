from fastapi import FastAPI,status,Depends
from fastapi.responses import JSONResponse
from Model import model,database
import default
from routers import risks,users,authenticate
from Model.database import get_db
from sqlalchemy.orm import Session

app = FastAPI()

model.Base.metadata.create_all(database.engine)

# Introduction
@app.get("/",tags=['Introduction'])
def Intro():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content= {
            "Message":"Welcome to Risk Management System",
            "Created_By": "Sunil Choudhary", 
            "On": "25 May 2026", 
            "At": "Mentem Technologies Pvt. Ltd.",
            "During" : "Summer Internship"
        }
    )

#Adding Default values to tables for test purporse
@app.post("/default",tags = ["Default"])
def addDefault(db: Session = Depends(get_db)):
    default.addALL(db)
    return JSONResponse(
        status_code= status.HTTP_200_OK,
        content= "Default Values added successfully for test purpose."
    )

app.include_router(authenticate.router)
app.include_router(risks.router)
app.include_router(users.router)
