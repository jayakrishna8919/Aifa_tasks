from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
app = FastAPI()
todos = []
next_id = 1

class Todo(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

@app.get("/todos/", response_model=List[Todo])
def get_todos():
    print(todos)
    return todos

@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="To-Do not found")

@app.post("/todos/", response_model=Todo)
def create_todo(title:str,description:str,completed:bool):
    global next_id
    
    d={"title":title,"description":description,"completed":completed,"id":next_id}
    todos.append(d)
    next_id += 1
    return d
 
@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated_todo: Todo):
    for todo in todos:
        if todo["id"] == todo_id:
            todo.update(updated_todo.dict())
            return todo
    raise HTTPException(status_code=404, detail="To-Do not found")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo["id"] == todo_id:
            todos.pop(index)
            return {"detail": "To-Do deleted"}
    raise HTTPException(status_code=404, detail="To-Do not found")