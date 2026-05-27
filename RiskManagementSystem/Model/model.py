from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer,primary_key=True)
    user_name = Column(String)
    user_role = Column(String)
    user_email = Column(String)
    user_password = Column(String)

    assigned_risk = relationship(
        "Risk",
        foreign_keys="Risk.assigned_to",
        back_populates="assignee"
    )

    allocated_risk = relationship(
        "Risk",
        foreign_keys="Risk.risk_allocation",
        back_populates= "allocator"
    )

    created_risk = relationship(
        "Risk",
        foreign_keys="Risk.created_by",
        back_populates= "creator"
    )

class Risk(Base):
    __tablename__ = "risks"

    risk_id = Column(Integer, primary_key=True)
    risk_title = Column(String)
    risk_description = Column(String)
    risk_priority = Column(String)
    risk_status = Column(String)
    risk_type = Column(String)
    risk_category = Column(String)
    created_by = Column(Integer,ForeignKey("users.user_id"))
    risk_allocation = Column(Integer,ForeignKey("users.user_id"))
    assigned_to = Column(Integer, ForeignKey("users.user_id"))
    due_date = Column(String)

    assignee = relationship(
        "User", 
        foreign_keys= [assigned_to],
        back_populates= "assigned_risk"
    )
    allocator = relationship(
        "User",
        foreign_keys= [risk_allocation],
        back_populates="allocated_risk"
    )
    creator = relationship(
        "User",
        foreign_keys= [created_by],
        back_populates= "created_risk"
    )



