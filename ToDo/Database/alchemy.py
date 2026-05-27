from sqlalchemy import create_engine, Integer, Column, String
from sqlalchemy.orm import declarative_base,sessionmaker

engine = create_engine("sqlite:///Database/newdb.db",echo = False)

Session = sessionmaker(bind= engine)
session = Session()

Base = declarative_base()

class TODO(Base):
    __tablename__ = "todo_list"

    id = Column(Integer, primary_key= True)
    todo = Column(String(500))
    status = Column(String(30))

    def __repr__(self):
        return f"ID: {self.id}, TODO: {self.todo}, STATUS: {self.status}"

#Create tables
Base.metadata.create_all(engine)

def addTask(details):
    new_details = TODO(todo = details.todo, status = details.status)
    session.add(new_details)
    session.commit()
    return True

def showTask():
    data = session.query(TODO).all()
    if not data:
        return False
    result = []
    for row in data:
        result.append({
            "ID": row.id,
            "TODO": row.todo,
            "STATUS": row.status
        })
    
    return result

def deleteTask(todo_id):
    data = session.query(TODO).filter(TODO.id == todo_id).first()
    if not data:
        return False
    session.delete(data)
    session.commit()
    return True

def resetTask():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return True

def updateTaskStatus(todo_id,details):
    data = session.query(TODO).filter(TODO.id == todo_id).first()
    if not data:
        return False
    data.status = details.status
    session.commit()
    return True

def updateTaskToDo(todo_id,details):
    data = session.query(TODO).filter(TODO.id == todo_id).first()
    if not data:
        return False
    data.todo = details.todo
    session.commit()
    return True

def selectSingleToDo(todo_id):
    data = session.query(TODO).filter(TODO.id== todo_id).all()
    if not data:
        return False
    
    result = []
    for row in data:
        result.append(
            {"ID": row.id,
            'TODO': row.todo,
            "STATUS": row.status}
        )
    return result
