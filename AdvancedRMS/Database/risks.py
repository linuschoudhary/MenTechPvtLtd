from Database import model
from sqlalchemy.orm import Session

def get_all(db:Session):
    try:
        risks =db.query(model.Risk).all()
        if not risks:
            return None
        result = []
        for risk in risks:
            result.append({
                "risk_id":risk.risk_id,
                "risk_title": risk.risk_title,
                "risk_description" : risk.risk_description,
                "risk_priority" : risk.risk_priority,
                "risk_status" : risk.risk_status,
                "risk_type" : risk.risk_type,
                "created_by" : {
                    "user_id" : risk.created_by,
                    "user_name" : risk.creator.user_name if risk.creator else "Not Assigned",
                    "user_role" : risk.creator.user_role if risk.creator else "Not Assigned",
                    "user_email": risk.creator.user_email if risk.creator else "Not Assigned"
                } if risk.created_by else "Not Assigned",
                "risk_allocation" : {
                    "user_id" : risk.risk_allocation,
                    "user_name" : risk.allocator.user_name if risk.allocator else "Not Assigned",
                    "user_role" : risk.allocator.user_role if risk.allocator else "Not Assigned",
                    "user_email": risk.allocator.user_email if risk.allocator else "Not Assigned"
                } if risk.risk_allocation else "Not Assigned",
                "assigned_to" : {
                    "user_id" : risk.assigned_to,
                    "user_name" : risk.assignee.user_name if risk.assignee else "Not Assigned",
                    "user_role" : risk.assignee.user_role if risk.assignee else "Not Assigned",
                    "user_email": risk.assignee.user_email if risk.assignee else "Not Assigned"
                } if risk.assigned_to else "Not Assigned",
                "risk_category": risk.risk_category,
                "due_date": risk.due_date
                

            })

        return result
    except Exception as e:
        return f"{e}"

def get_risks_by_id(db:Session,risk_id:int):
    risk = db.query(model.Risk).filter(model.Risk.risk_id == risk_id).first()
    if not risk:
        return None
    result = {
        "risk_id":risk.risk_id,
        "risk_title": risk.risk_title,
        "risk_description" : risk.risk_description,
        "risk_priority" : risk.risk_priority,
        "risk_status" : risk.risk_status,
        "risk_type" : risk.risk_type,
        "created_by" : {
            "user_id" : risk.created_by,
            "user_name" : risk.creator.user_name if risk.creator else "Not Assigned",
            "user_role" : risk.creator.user_role if risk.creator else "Not Assigned",
            "user_email": risk.creator.user_email if risk.creator else "Not Assigned"
        } if risk.created_by else "Not Assigned",
        "risk_allocation" : {
            "user_id" : risk.risk_allocation,
            "user_name" : risk.allocator.user_name if risk.allocator else "Not Assigned",
            "user_role" : risk.allocator.user_role if risk.allocator else "Not Assigned",
            "user_email": risk.allocator.user_email if risk.allocator else "Not Assigned"
        } if risk.risk_allocation else "Not Assigned",
        "assigned_to" : {
            "user_id" : risk.assigned_to,
            "user_name" : risk.assignee.user_name if risk.assignee else "Not Assigned",
            "user_role" : risk.assignee.user_role if risk.assignee else "Not Assigned",
            "user_email": risk.assignee.user_email if risk.assignee else "Not Assigned"
        } if risk.assigned_to else "Not Assigned",
        "risk_category": risk.risk_category,
        "due_date": risk.due_date
    }

    return result





def add_risks(db:Session,details):
    try:
        new_risk = model.Risk(
            risk_title = details.risk_title,
            risk_description = details.risk_description,
            risk_priority = details.risk_priority,
            risk_status = details.risk_status,
            risk_type = details.risk_type,
            risk_category = details.risk_category,
            created_by = details.created_by,
            risk_allocation = details.risk_allocation,
            assigned_to = details.assigned_to,
            due_date = details.due_date
        )
        db.add(new_risk)
        db.commit()
        db.refresh(new_risk)
        return "Details Added."
    except Exception as e:
        return e
    

def update_risks(db: Session,risk_id:int,details):
    risk = db.query(model.Risk).filter(model.Risk.risk_id == risk_id).first()
    print(risk)
    print("risk_id",risk_id)
    if not risk:
        return None
    updated_risk = details.model_dump(exclude_unset=True)
    for key,value in updated_risk.items():
        setattr(risk,key,value)
    db.commit()
    db.refresh(risk)
    return "Risk updated successfully."

def delete_risks(db, risk_id):
    risk = db.query(model.Risk).filter(model.Risk.risk_id == risk_id).first()
    if not risk:
        return None
    db.delete(risk)
    db.commit()
    return f"Risk Deleted Successfully Risk ID {risk_id}"
