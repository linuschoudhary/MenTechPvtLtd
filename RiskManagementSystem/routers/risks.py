from fastapi import APIRouter
from fastapi import Depends
from Model import database
from Schema import schema
from typing import List
from sqlalchemy.orm import Session
from Repository import risks
from Scheme.oauth2 import get_current_user
from Scheme import RoleBasedAccess

get_db = database.get_db
access = RoleBasedAccess.role_required

router = APIRouter(
    prefix="/risk",
    tags=['Risks']
)


# Risks
@router.get("/",response_model=List[schema.RiskOutput])
def showRisks(db: Session = Depends(get_db),current_user : schema.User = Depends(access(RoleBasedAccess.level_3))):
    return risks.get_all(db)


@router.get("/{risk_id}")
def showRiskByRiskID(risk_id: int,db: Session = Depends(get_db),current_user : schema.User = Depends(access(RoleBasedAccess.level_3))):
    return risks.get_risks_by_id(db,risk_id)

@router.post("/add")
def addRisk(details:schema.Risk,db : Session = Depends(get_db),current_user : schema.User = Depends(access(RoleBasedAccess.level_3))):
    return risks.add_risks(db,details)

@router.put("/update/{risk_id}",response_model=schema.RiskOutputUpdated)
def updateRisk(risk_id: int,details: schema.RiskUpdate,db : Session = Depends(get_db),current_user : schema.User = Depends(access(RoleBasedAccess.level_2))):
    return risks.update_risks(db,risk_id,details)

@router.delete("/delete/{risk_id}")
def deleteRisk(risk_id:int,db: Session = Depends(get_db),current_user : schema.User = Depends(access(RoleBasedAccess.level_2))):
    return risks.delete_risk(db, risk_id)
