import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Get the MongoDB connection string from an environment variable
# This is crucial for security and for Docker
mongo_uri = os.environ.get('MONGO_URI')

if not mongo_uri:
    print("Error: MONGO_URI environment variable not set.")
    # You could fall back to a local default here, but for Docker it's best to exit
    # or handle this error appropriately.
    # For this tutorial, we'll assume it's set when running.

client = MongoClient(mongo_uri)
db = client.todo_db  # Use or create a database named 'todo_db'
collection = db.tasks   # Use or create a collection named 'tasks'

@app.route('/')
def index():
    """Homepage: Fetch all tasks and display them."""
    tasks = collection.find()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    """Add a new task to the database."""
    task_content = request.form.get('task_content')
    if task_content:
        collection.insert_one({'content': task_content, 'completed': False})
    return redirect(url_for('index'))

@app.route('/complete/<task_id>')
def complete_task(task_id):
    """Mark a task as complete."""
    collection.update_one({'_id': ObjectId(task_id)}, {'$set': {'completed': True}})
    return redirect(url_for('index'))

@app.route('/delete/<task_id>')
def delete_task(task_id):
    """Delete a task from the database."""
    collection.delete_one({'_id': ObjectId(task_id)})
    return redirect(url_for('index'))

if __name__ == "__main__":
    # Running the app with host='0.0.0.0' makes it accessible 
    # from outside the container (which is what we want for Docker)
    app.run(debug=True, host='0.0.0.0', port=5000)