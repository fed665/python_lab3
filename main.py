from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# Хранилище задач (в реальном приложении лучше использовать базу данных)
tasks = []
next_id = 1

class Task:
    def __init__(self, id, title, completed=False):
        self.id = id
        self.title = title
        self.completed = completed

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    global next_id
    title = request.form.get('title')
    if title:
        task = Task(next_id, title)
        tasks.append(task)
        next_id += 1
    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    for task in tasks:
        if task.id == task_id:
            task.completed = not task.completed
            break
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task.id != task_id]
    return redirect(url_for('index'))

# API для работы с задачами (JSON)
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify([{'id': t.id, 'title': t.title, 'completed': t.completed} for t in tasks])

@app.route('/api/tasks', methods=['POST'])
def create_task():
    global next_id
    data = request.get_json()
    if data and data.get('title'):
        task = Task(next_id, data['title'])
        tasks.append(task)
        next_id += 1
        return jsonify({'id': task.id, 'title': task.title, 'completed': task.completed}), 201
    return jsonify({'error': 'Title is required'}), 400

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    for task in tasks:
        if task.id == task_id:
            if 'title' in data:
                task.title = data['title']
            if 'completed' in data:
                task.completed = data['completed']
            return jsonify({'id': task.id, 'title': task.title, 'completed': task.completed})
    return jsonify({'error': 'Task not found'}), 404

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task_api(task_id):
    global tasks
    tasks = [task for task in tasks if task.id != task_id]
    return jsonify({'message': 'Task deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)