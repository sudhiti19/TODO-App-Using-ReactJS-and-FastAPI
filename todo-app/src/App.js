import React, { useState, useEffect } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000/todos/";

function App() {
    const [todos, setTodos] = useState([]);
    const [task, setTask] = useState("");

    useEffect(() => {
        fetchTodos();
    }, []);

    const fetchTodos = async () => {
        const response = await axios.get(API_URL);
        setTodos(response.data);
    };

    const addTodo = async () => {
        await axios.post(API_URL, { task, done: false });
        fetchTodos();
        setTask("");
    };
     // ✅ Toggle Task Completion
     const toggleDone = async (id, done) => {
        await axios.put(`${API_URL}${id}/`, { done: !done });
        fetchTodos();  // Refresh after update
    };
    return (
        <div>
            <h1>To-Do List</h1>
            <input value={task} onChange={(e) => setTask(e.target.value)} />
            <button onClick={addTodo}>Add</button>
            <ul>
                {todos.map(todo => (
                    <li key={todo.id}>
                        <input 
                            type="checkbox" 
                            checked={todo.done} 
                            onChange={() => toggleDone(todo.id, todo.done)} 
                        />
                        <span style={{ textDecoration: todo.done ? "line-through" : "none" }}>
                            {todo.task}
                        </span>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default App;
