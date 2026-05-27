from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from Schema import schema
from sqlalchemy.orm import Session
from Model import database,model
from hashing import Hash
from Scheme.jwttoken import create_access_token
router = APIRouter(
    tags=['Authentication']
)

@router.post("/login")
def login(details: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(database.get_db)):
    user = db.query(model.User).filter(model.User.user_email == details.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials"
        )
    if not Hash.verifyPassword(details.password,user.user_password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials"
        )
    
    access_token = create_access_token(
        data = {"sub": user.user_email,"role": user.user_role}
        )
    return {"access_token": access_token,"token_type":"bearer"}
