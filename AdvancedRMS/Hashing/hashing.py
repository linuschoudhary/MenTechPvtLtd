from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=['bcrypt'],deprecated= 'auto')

class Hash():
    def bcryptPassword(password:str):
        return pwd_cxt.hash(password)
    
    def verifyPassword(plain_password,hashed_password):
        return pwd_cxt.verify(plain_password,hashed_password)
