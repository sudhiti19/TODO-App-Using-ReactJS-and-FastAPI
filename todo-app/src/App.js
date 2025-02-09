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

    return (
        <div>
            <h1>To-Do List</h1>
            <input value={task} onChange={(e) => setTask(e.target.value)} />
            <button onClick={addTodo}>Add</button>
            <ul>
                {todos.map(todo => (
                    <li key={todo.id}>
                        {todo.task} 
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default App;
