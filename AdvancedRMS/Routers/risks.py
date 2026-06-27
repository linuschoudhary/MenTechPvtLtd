from fastapi import APIRouter,Depends,HTTPException,status
from Database.database import get_db
from sqlalchemy.orm import Session
from Database import risks
from sqlalchemy.orm import Session
from Authentication import role_based_access
from Schema import schema
from Log.logger import logger


router = APIRouter(
    prefix="/risk",
    tags=["risks"]
)

access = role_based_access.role_required

@router.get("")
def show_all_risks(db:Session=Depends(get_db),current_user:schema.Users=Depends(access(role_based_access.level_2,end_point="show_all_risks"))):
    """Call this tool when you need to know all the available risks in database at once."""
    logger.info(f"{current_user.user_email} with role of {current_user.user_role} get the deatils of all risks")
    result=risks.get_all(db=db)
    if result:
        return result
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No Risks available.")

@router.get("/id")
def show_risk_by_id(risk_id:int,db:Session=Depends(get_db),current_user:schema.Users=Depends(access(role_based_access.level_2,end_point="show_risk_by_risk_id"))):
    """Use this tool when you want the risk details for a particular risk id only."""
    logger.info(f"{current_user.user_email} with role of {current_user.user_role} get the deatils of risk with risk id {risk_id}")
    result=risks.get_risks_by_id(db,risk_id=risk_id)
    if result:
        return result
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Risk Not found")

@router.post("/add_risk")
def add_new_risk(details: schema.Risks, db:Session=Depends(get_db),current_user:schema.Users=Depends(access(role_based_access.level_2,end_point="add_new_risk"))):
    """Use this tool when you want to add a new risk to the database."""
    result = risks.add_risks(db=db,details=details)
    print(result)
    logger.info(f"{current_user.user_email} with role of {current_user.user_role} added a new risk with Details:\n {details}")
    return result

@router.post("/update_risk")
def update_risk(risk_id:int,details:schema.UpdateRisks,db:Session=Depends(get_db),current_user:schema.Users=Depends(access(role_based_access.level_2,end_point="update_risk"))):
    """Use this tool to update any existing risk in database using it's risk id.
    It will not need all the data to update, you can update partial details like only one column can be updated.
    """
    logger.info(f"{current_user.user_email} with role of {current_user.user_role} updated risk {risk_id} with new detail\n{details}")
    return risks.update_risks(risk_id=risk_id,details=details,db=db)

@router.post("/delete_risk")
def delete_risk(risk_id:int,db:Session=Depends(get_db),current_user:schema.Users=Depends(access(role_based_access.level_2,end_point="delete_risk"))):
    """Use this tool when you need to delete any available tool in the database using its risk id."""
    logger.info(f"{current_user.user_email} with role of {current_user.user_role} deleted risk {risk_id}")
    return risks.delete_risks(risk_id=risk_id,db=db)
