const express = require('express');
const mongoose = require('mongoose');
const path = require('path');
const app = express();

app.use(express.json());
app.use(express.static('public'));

const mongoURI = process.env.MONGO_URI;
if (!mongoURI) { console.error("No DB Connection String found!"); }

mongoose.connect(mongoURI)
    .then(() => console.log('✅ Connected to DB'))
    .catch(err => console.log(err));

// 1. UPDATE SCHEMA: Add 'completed' field
const TodoSchema = new mongoose.Schema({
    text: String,
    completed: { type: Boolean, default: false }
});
const Todo = mongoose.model('Todo', TodoSchema);

// 2. READ (Get all tasks)
app.get('/todos', async (req, res) => {
    const todos = await Todo.find();
    res.json(todos);
});

// 3. CREATE (Add task)
app.post('/todo', async (req, res) => {
    const newTodo = new Todo({ text: req.body.text });
    await newTodo.save();
    res.json(newTodo);
});

// 4. UPDATE (Toggle Complete)
app.put('/todo/:id', async (req, res) => {
    const todo = await Todo.findById(req.params.id);
    todo.completed = !todo.completed; // Flip the status
    await todo.save();
    res.json(todo);
});

// 5. DELETE (Remove task)
app.delete('/todo/:id', async (req, res) => {
    await Todo.findByIdAndDelete(req.params.id);
    res.json({ result: 'Deleted' });
});

app.get('/', (req, res) => res.sendFile(path.join(__dirname, 'public', 'index.html')));
app.listen(3000, () => console.log('🚀 Server running on port 3000'));