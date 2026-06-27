from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from Schema import schema
from sqlalchemy.orm import Session
from Database import database,model
from Hashing.hashing import Hash
from Authentication.jwttoken import create_access_token
from Log.logger import logger


router = APIRouter(
    tags=['Authentication']
)

@router.post("/login")
def login(details: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(database.get_db)):
    user = db.query(model.User).filter(model.User.user_email == details.username).first()

    if not user:
        logger.warning(f"{details.username} does not exist")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials"
        )
    if not Hash.verifyPassword(details.password,user.user_password):
        logger.warning(f"{details.username} password mismatch")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials"
        )
    
    logger.info(f"{user.user_name} logged in with user role {user.user_role}")
    access_token = create_access_token(
        data = {"sub": user.user_email,"role": user.user_role}
        )
    return {"access_token": access_token,"token_type":"bearer"}
