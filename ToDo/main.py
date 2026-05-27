from fastapi import FastAPI,HTTPException
# from Database.sqlitedb import addTask,showTask,updateTaskStatus,updateTaskToDo,deleteTask,resetTask,selectSingleToDo
from fastapi.responses import JSONResponse
from schema.todo_list_format import TodoDetails,status_data,todo_data
from Database.alchemy import addTask,showTask,updateTaskStatus,updateTaskToDo,deleteTask,resetTask,selectSingleToDo


app = FastAPI()

@app.get("/")
def home():
    return {"Message": "This is a todo list."}

@app.get('/show')
def show_list():
    result = showTask()
    if not result:
        return JSONResponse(status_code=200, content="TODO is empty.")
    return result

@app.get("/show/{todo_id}")
def showOneToDo(todo_id):
    try:
        result = selectSingleToDo(todo_id)
        if result:
            return result
        raise HTTPException(status_code= 404, detail= "ID does not exists.")
    except Exception as e:
        raise HTTPException(status_code= 400, detail= f"{e}")



@app.post("/add")
def add_to_list(details: TodoDetails):
    result = addTask(details)
    if result == True:
        return JSONResponse(status_code= 200, content= "Success!")
    raise HTTPException(status_code= 400, detail= "Database not initialized.")


@app.put('/update/todo/{todo_id}')
def update_todo(todo_id: int, details: todo_data):
    result = updateTaskToDo(todo_id,details)
    if result:
        return JSONResponse(status_code=200, content='Successfully updated the todo.')
    raise HTTPException(status_code= 404, detail= "ID does not exists.")


@app.put('/update/status/{todo_id}')
def update_status(todo_id: int, details: status_data):
    result = updateTaskStatus(todo_id,details)
    if result:
        return JSONResponse(status_code=200, content="successfully updated the status.")
    raise HTTPException(status_code= 404, detail= "ID does not exist.")

@app.delete('/delete/{todo_id}')
def delete_task(todo_id: int):
    result = deleteTask(todo_id)
    if result:
        return JSONResponse(status_code=200, content= f"Successfully removed task {todo_id}")
    raise HTTPException(status_code=404, detail="ID does not exists.")

@app.delete("/reset")
def reset_todoList():
    result = resetTask()
    if result == True:
        return JSONResponse(status_code= 200, content= "Reset Successful!")
    raise HTTPException(status_code=400, detail="Database not initialized.")