from fastapi import APIRouter,Depends
from Authentication import role_based_access
from Schema import schema
from Log.logger import logger

access = role_based_access.role_required

router = APIRouter()

@router.get("/logs",tags=["LOG DATA"])
def read_logs(current_user:schema.Users=Depends(access(role_based_access.level_1,end_point="read_logs"))):
    """This function is called when log data is to be needed. It will return complete log file data."""
    logger.info(f"{current_user.user_email} with role {current_user.user_role} accessed 'Log Records'")
    with open (r"Log\activity.log") as f:
        return f.read()