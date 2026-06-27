from fastapi import APIRouter, Depends,Request
from Chatbot.chatbot import main
import asyncio
from Database import model
from Authentication import role_based_access
from Log.logger import logger

router = APIRouter()

access = role_based_access.role_required

@router.post("/chatbot",tags=["ChatBot"])
def chatbot_input(message:str,request:Request,current_user : model.User = Depends(access(role_based_access.level_3,end_point="chatbot_input"))):
    logger.info(f"{current_user.user_email} called chatbot with message:\n {message}")
    # print("Request:",request.headers)
    auth_header = request.headers.get("Authorization")
    # print("auth_header:",auth_header)
    token = auth_header.split(" ")[1] if auth_header and " " in auth_header else ""
    # print("token:",token)
    return asyncio.run(main(content=message,user_token=token))

@router.get("/whoami")
def who_am_i(current_user:model.User = Depends(access(role_based_access.level_3,end_point="whoami"))):
    """This function is used to check who is currenlty logged in (current activce user) and using the database."""
    logger.info(f"{current_user.user_email} called who_am_i to know the current logged in user name")
    return f"{current_user.user_email} as {current_user.user_role}"