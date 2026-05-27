from Model import model
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from hashing import Hash
from sqlalchemy import and_


def all_users(db:Session):
    users = db.query(model.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No Users Found.")
    result = []
    for user in users:
        result.append({
            "user_id" : user.user_id,
            "user_name" : user.user_name,
            "user_role" : user.user_role,
            "user_email": user.user_email
        })
    return result

def user_by_id(db: Session,user_id:int):
    user = db.query(model.User).filter(model.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No Users Found.")
    result = {
        "user_id" : user.user_id,
        "user_name" : user.user_name,
        "user_role" : user.user_role,
        "user_email": user.user_email
    }
    return result

def add_user(db: Session, details):
    try:
        new_user = model.User(
            user_name = details.user_name,
            user_role = details.user_role,
            user_email = details.user_email,
            user_password = Hash.bcryptPassword(details.user_password)
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        id = db.query(model.User).filter(and_(model.User.user_email == details.user_email, model.User.user_name == details.user_name)).first().user_id
        return JSONResponse(status_code=status.HTTP_200_OK,content = f"User added successfully and user ID is allocated is: {id}")
    except Exception as e:
        raise HTTPException(status_code=status.WS_1007_INVALID_FRAME_PAYLOAD_DATA,detail = "Please Fill Required Field Email, Name and Password.")

def update_user(db:Session,user_id,details):
    user = db.query(model.User).filter(model.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User not found for user id {user_id}")
    updated_user = details.model_dump(exclude_unset=True)
    for key,value in updated_user.items():
        setattr(user,key,value)
    db.commit()
    db.refresh(user)
    return JSONResponse(status_code=status.HTTP_200_OK,content= "User updated successfully")

def delete_user(db:Session,user_id):
    user = db.query(model.User).filter(model.User.user_id==user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Found")
    db.delete(user)
    db.commit()
    return JSONResponse(status_code=status.HTTP_200_OK,content={"Message": "Deleted Successfully","User ID": user_id})

def risks_assigned(db: Session,user_id):
    user = db.query(model.User).filter(model.User.user_id == user_id).first()