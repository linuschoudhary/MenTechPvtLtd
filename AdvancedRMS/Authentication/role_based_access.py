from fastapi import Depends,HTTPException,status
from Authentication.oauth2 import get_current_user
from Log.logger import logger

level_1 = ['Admin']
level_2 = ['Admin','Manager']
level_3 = ['Admin','Manager','Employee']

def role_required(role_list:list,end_point:str="Unknown Endpoint Yet"):
    def role_checker(current_user = Depends(get_current_user)):
        if current_user.user_role not in role_list:
            logger.warning(f"{current_user.user_email} with role {current_user.user_role} tried to access {end_point} with unauthrized access.")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Access Denied")
        return current_user
    return role_checker