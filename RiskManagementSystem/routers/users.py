from fastapi import APIRouter
from fastapi import Depends
from Model import database
from Schema import schema
from typing import List
from sqlalchemy.orm import Session
from Repository import users
from Scheme import RoleBasedAccess

access = RoleBasedAccess.role_required

get_db = database.get_db

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

# Users
@router.get("/",response_model=List[schema.UserOutput])
def showUser(db: Session = Depends(get_db),current_user : schema.User = Depends(access(RoleBasedAccess.level_2))):
    return users.all_users(db)

@router.get("/{user_id}")
def showUserByUserID(user_id: int,db: Session = Depends(get_db),current_user : schema.User = Depends(access(RoleBasedAccess.level_3))):
    return users.user_by_id(db,user_id)

@router.post("/add")
def addUser(details: schema.User,db : Session = Depends(get_db),current_user : schema.User = Depends(access(RoleBasedAccess.level_2))):
    return users.add_user(db, details)
    
@router.put("/update/{user_id}",response_model = schema.UserOutputUpdated)
def updateUser(user_id: int,details : schema.UserUpdate, db: Session = Depends(get_db),current_user : schema.User = Depends(access(RoleBasedAccess.level_2))):
    return users.update_user(db,user_id,details)

@router.delete("/delete/{user_id}")
def deleteUser(user_id: int,db: Session = Depends(get_db),current_user : schema.User = Depends(access(RoleBasedAccess.level_1))):
    return users.delete_user(db, user_id)