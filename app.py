import sqlite3
import paramiko,datetime,time
from flask import Flask, render_template, request, url_for, flash, redirect, escape,redirect,Response
from werkzeug.exceptions import abort
from shelljob import proc

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/greet')
def greet():
    return 'Hello, World!'

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        agent = request.form['agent'] 
        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, agent, content) VALUES (?, ?, ?)',
                         (title, agent, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        agent = request.form['agent']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, agent = ?, content = ?'
                         ' WHERE id = ?',
                         (title, agent, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))

# @app.route('/execute')
@app.route('/<int:id>/execute')
def execute(id):
    post = get_post(id)
    conn = get_db_connection()
    result=conn.execute('SELECT * FROM posts WHERE id = ? ', (id,)  ).fetchone()
    conn.close()
    hostname=""
    username=""
    password=""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname, username=username, password=password)
    except:
        print("[!] Cannot connect to the SSH Server")
        exit()
    commands = [
        result['content']
    ]
    for command in commands:
        stdin, stdout, stderr = client.exec_command(command)
        for line in stdout:
            file = open('sh_ver.txt', 'a')
            file.write(''.join(line.strip('\n')))
            file.write('\n')
            file.close()
        for line in stderr:
            print('... ' + line.strip('\n'))
    with open("sh_ver.txt", "r") as f:
        content = f.read()
    return redirect(url_for('logs'))

    
    

@app.route('/logs')
def logs():
    with open("sh_ver.txt", "r") as f:
        content = f.read()
    return render_template("logs.html", content=content)

