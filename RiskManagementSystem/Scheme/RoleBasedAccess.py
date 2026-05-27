from fastapi import Depends,HTTPException,status
from Scheme.oauth2 import get_current_user

level_1 = ['Admin']
level_2 = ['Admin','Manager']
level_3 = ['Admin','Manager','Employee']

def role_required(role_list:list):
    def role_checker(current_user = Depends(get_current_user)):
        if current_user.user_role not in role_list:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Access Denied")
        return current_user
    return role_checker