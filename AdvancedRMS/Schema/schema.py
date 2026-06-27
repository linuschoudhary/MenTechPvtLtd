from pydantic import BaseModel
from typing import Optional

class Users(BaseModel):
    user_name:str
    user_role: str
    user_email: str
    user_password: str

class UpdateUser(BaseModel):
    user_name: Optional[str]=None
    user_role: Optional[str]=None
    user_email:Optional[str]=None
    user_password:Optional[str]=None

class Risks(BaseModel):
    risk_title:Optional[str] = None
    risk_description:str
    risk_priority:str
    risk_status:str
    risk_type:str
    risk_category:str
    created_by:int
    risk_allocation:int
    assigned_to:int
    due_date:str

class UpdateRisks(BaseModel):
    risk_title:Optional[str]=None
    risk_description:Optional[str]=None
    risk_priority:Optional[str]=None
    risk_status:Optional[str]=None
    risk_type:Optional[str]=None
    risk_category:Optional[str]=None
    created_by:Optional[int]=None
    risk_allocation:Optional[int]=None
    assigned_to:Optional[int]=None
    due_date:Optional[str]=None

class Token(BaseModel):
    access_token : str
    token_data : str = "bearer"

class TokenData(BaseModel):
    user_email : str | None = None
    user_role : str | None = None