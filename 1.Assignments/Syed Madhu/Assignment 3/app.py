from flask import Flask, request, render_template, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            status INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
init_db()

@app.route('/')
def home():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return render_template('home.html', tasks=tasks)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        description = request.form['description']
        status = 0  # Default status to incomplete
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (description, status) VALUES (?, ?)', (description, status))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('create.html')

@app.route('/update/<int:task_id>', methods=['GET', 'POST'])
def update(task_id):
    if request.method == 'POST':
        description = request.form['description']
        status = int(request.form['status'])
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET description = ?, status = ? WHERE id = ?', (description, status, task_id))
        conn.commit()
        conn.close()
        return redirect('/')
    else:
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        task = cursor.fetchone()
        conn.close()
        return render_template('update.html', task=task)

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
