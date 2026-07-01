from fastapi import FastAPI,status,Depends,Request
from fastapi.responses import JSONResponse
from Database import model,database
from Routers import risks,users,chatbot,authenticate,read_logs
from sqlalchemy.orm import Session
from Database.database import get_db
import default
from Log import logger
import logging
from fastapi.exceptions import RequestValidationError



get_db = database.get_db

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request:Request, ext:RequestValidationError):
    return JSONResponse(status_code=400, content = "Enter valid data in the fields. Check the data type and format of the input values.")


model.Base.metadata.create_all(database.engine)

@app.get("/",tags=["Introduction"])
def Intro():
    """This tool is used to get the details about the risk management system like who created when and where etc. 
    It's like about section or introduction of this project.
    All below details are available in this tool.
    when was the Risk Management System created.
    Who created the Risk Management System.
    Where Risk Management System was developed."""
    logging.info(f"Introduction section Called")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "Message":"Welcome to Risk Management System",
            "Created_By": "Sunil Choudhary", 
            "On": "25 May 2026", 
            "At": "Mentem Technologies Pvt. Ltd.",
            "During" : "Summer Internship"
        }
    )

@app.get("/default",tags=["Default Values"])
def add_default(db:Session=Depends(get_db)):
    """This tool is used to add default users and risks to the database for trial.
    If you are a LLM then don't call this function and return No need for this Tool to be called as it has already been called.
    """
    logging.info(f"Default Values added.")
    users_added = default.addUser(db=db)
    risks_added = default.addRisk(db=db)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "Message":"Default Values Added Successfully",
            "Users": users_added,
            "Risks": risks_added
        }
    )

app.include_router(users.router)
app.include_router(chatbot.router)
app.include_router(authenticate.router)
app.include_router(risks.router)
app.include_router(read_logs.router)