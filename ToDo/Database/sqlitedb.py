import sqlite3

connection = sqlite3.connect("Database//todolist.db",check_same_thread=False)

cursor = connection.cursor()

cursor.execute(
    """CREATE TABLE IF NOT EXISTS todo_list (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    todo TEXT,
    status TEXT
    )"""
)

def addTask(details):
    cursor.execute(
        """insert into todo_list (todo,status) values (?,?);""",
        (details.todo,details.status)
    )
    connection.commit()
    return True

def showTask():
    cursor.execute(
        """select * from todo_list;"""
    )
    rslt = cursor.fetchall()  
    result = []
    for row in rslt:
        result.append({
            "ID": row[0],
            "TODO": row[1],
            "STATUS": row[2]
        })
    
    return result

def deleteTask(todo_id):
    cursor.execute("""select * from todo_list where id = ?""", (todo_id,))
    checker = cursor.fetchone()
    if not checker:
        return False
    cursor.execute(
        """delete from todo_list where id = ?""",(todo_id,)
    )
    connection.commit()
    return True

def resetTask():
    cursor.execute("DELETE FROM todo_list;")
    cursor.execute(
        """DELETE FROM sqlite_sequence WHERE name='todo_list';"""
    )
    connection.commit()
    return True

def updateTaskStatus(todo_id,details):
    cursor.execute("""select * from todo_list where id = ?""", (todo_id,))
    checker = cursor.fetchone()
    if not checker:
        return False
    cursor.execute(
        """update todo_list set status = ? where id = ?;""",
        (details.status,todo_id)
    )
    connection.commit()
    return True

def updateTaskToDo(todo_id,details):
    cursor.execute("""select * from todo_list where id = ?""", (todo_id,))
    checker = cursor.fetchone()
    if not checker:
        return False
    cursor.execute(
        """update todo_list set todo = ? where id= ?;""",
        (details.todo,todo_id)
    )
    connection.commit()
    return True

def selectSingleToDo(todo_id):
    cursor.execute(
        """select * from todo_list where id = ?;""",
        (todo_id,)
    )
    rslt = cursor.fetchall()
    result = []
    for row in rslt:
        result.append(
            {"ID": row[0],
            'TODO': row[1],
            "STATUS": row[2]}
        )
    return result
