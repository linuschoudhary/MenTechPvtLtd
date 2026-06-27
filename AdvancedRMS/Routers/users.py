from Database import users,database
from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from Schema import schema
from Authentication import role_based_access
from Log.logger import logger

access = role_based_access.role_required

router = APIRouter(
    tags=["Users"],
    prefix="/user"
)

@router.get("/")
def show_all_user(db:Session=Depends(database.get_db),current_user : schema.Users = Depends(access(role_based_access.level_1,end_point="show_all_user"))):
    """This function is called when we need to see all the available users."""
    logger.info(f"{current_user.user_email} with role of {current_user.user_role} get all user details")
    print(role_based_access.level_2)
    if current_user.user_role not in role_based_access.level_2:
        return "Not Authorised User"
    else:
        result = users.get_all_users(db)
        print(result)
        return result

@router.get("/show_by_id")
def show_user_by_id(user_id:int,db:Session=Depends(database.get_db),current_user:schema.Users=Depends(access(role_based_access.level_2,end_point="show_user_by_id"))):
    """This tool is used when we need to get access of only a particular user id's data"""
    logger.info(f"{current_user.user_email} with role of {current_user.user_role} get the deatils of user {user_id}")
    user=users.get_user_by_id(db,user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Found")
    return user

@router.post("/add_user")
def add_new_user(details:schema.Users,db:Session=Depends(database.get_db),current_user:schema.Users=Depends(access(role_based_access.level_1,end_point="add_new_user"))):
    """To add a new user to the database we will use this tool."""
    logger.info(f"{current_user.user_email} with role of {current_user.user_role} added new user with details {details}")
    return users.add_user(db,details=details)

@router.put("/update_user")
def update(user_id:int,details:schema.UpdateUser,db:Session=Depends(database.get_db),current_user:schema.Users=Depends(access(role_based_access.level_1,end_point="update_user"))):
    """To update any details (complete or partial details) of the user, we will use this tool."""
    logger.warning(f"{current_user.user_email} with role of {current_user.user_role} updated the deatils of user {user_id} with new details {details}")
    return users.update_user(details=details,db=db,user_id=user_id)

@router.delete("/delete_user")
def delete(user_id: int,db:Session=Depends(database.get_db),current_user:schema.Users=Depends(access(role_based_access.level_1,end_point="delete_user"))):
    """To delete any user from the database we will use this tool."""
    logger.warning(f"{current_user.user_email} with role of {current_user.user_role} deleted the user with user id {user_id}")
    result=users.delete_user(user_id=user_id,db=db)
    if result:
        return result
    return "User Not Found"