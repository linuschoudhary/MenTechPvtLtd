from sqlalchemy.orm import Session
from sqlalchemy import and_
from Database import model
from Hashing.hashing import Hash

def get_all_users(db:Session):
    users = db.query(model.User).all()
    if not users:
        return None
    result = []
    for user in users:
        result.append({
            "user_id" : user.user_id,
            "user_name" : user.user_name,
            "user_role" : user.user_role,
            "user_email": user.user_email
        })
    return result

def get_user_by_id(db: Session,user_id:int):
    user = db.query(model.User).filter(model.User.user_id == user_id).first()
    if not user:
        return None
    result = {
        "user_id" : user.user_id,
        "user_name" : user.user_name,
        "user_role" : user.user_role,
        "user_email": user.user_email
    }
    return result

def add_user(db: Session, details:dict):
    user = db.query(model.User).filter(model.User.user_email==details.user_email).first()
    if user:
        return "User with this email already exists."
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
        return f"ID: {id} added successfully."
    except Exception as e:
        return f"Error Occured :{e}"
    
def update_user(db:Session,user_id,details):
    user = db.query(model.User).filter(model.User.user_id == user_id).first()
    if not user:
        return None
    updated_user = details.model_dump(exclude_unset=True)
    for key,value in updated_user.items():
        print(key,value)
        if key == "user_password":
            setattr(user,key,Hash.bcryptPassword(value))
        else:
            setattr(user,key,value)
    db.commit()
    db.refresh(user)
    return f"Updated Successfully"

def delete_user(db:Session,user_id):
    user = db.query(model.User).filter(model.User.user_id==user_id).first()
    if not user:
        return None
    db.delete(user)
    db.commit()
    return f"User ID: {user_id}, Deleted Successfully"

def risks_assigned(db: Session,user_id):
    user = db.query(model.User).filter(model.User.user_id == user_id).first()
