import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

# FastAPI App
app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Connect to PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        dbname="todo_db",
        user="postgres",
        password="sudhiti",
        host="localhost",
        port="5432"
    )

# Pydantic Model (without id, as it's auto-generated)
class ToDo(BaseModel):
    task: str
    done: bool = False

# Create Table (Runs only once)
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS todos (
    id SERIAL PRIMARY KEY,
    task TEXT NOT NULL,
    done BOOLEAN DEFAULT FALSE
)
""")
conn.commit()
conn.close()

# ✅ Create a new todo
@app.post("/todos/", response_model=dict)
def create_todo(todo: ToDo):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (task, done) VALUES (%s, %s) RETURNING id", (todo.task, todo.done))
    new_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return {"id": new_id, "task": todo.task, "done": todo.done}

# ✅ Get all todos
@app.get("/todos/", response_model=List[dict])
def get_todos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, task, done FROM todos")
    todos = cursor.fetchall()
    conn.close()
    return [{"id": t[0], "task": t[1], "done": t[2]} for t in todos]

# ✅ Update a todo's completion status
@app.put("/todos/{todo_id}/")
def update_todo(todo_id: int, todo: ToDo):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE todos SET done = %s WHERE id = %s RETURNING id", (todo.done, todo_id))
    updated = cursor.fetchone()
    conn.commit()
    conn.close()

    if updated is None:
        raise HTTPException(status_code=404, detail="ToDo not found")

    return {"message": "ToDo updated"}

# ✅ Delete a todo
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id=%s RETURNING id", (todo_id,))
    deleted = cursor.fetchone()
    conn.commit()
    conn.close()

    if deleted is None:
        raise HTTPException(status_code=404, detail="ToDo not found")
    
    return {"message": "ToDo deleted"}

# ✅ Run FastAPI Server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
