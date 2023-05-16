import wheel.bdist_wheel
from flask import Flask, render_template, url_for, request, redirect, flash
import sqlite3
import os

app = Flask(__name__)


def get_db_connection():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "project.db")
    conn = sqlite3.connect(db_path)
    return conn


@app.route('/')
def index():
    return render_template("index.html", title="Homepage")


@app.route('/about')
def about():
    return render_template("about.html", title="About")


@app.route("/all_machines")
def machines():
    conn = sqlite3.connect('project.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Machine')
    results = cur.fetchall()
    return render_template("all_machines.html", results=results, title="Machines")


@app.route("/machine/<int:id>")
def machine(id):
    conn = sqlite3.connect('project.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Machine WHERE id=?",(id,))
    data = cur.fetchone()
    return render_template('machine.html', title="Machine", machine=data,)


# At least part of this block of code is sourced from another one of my projects at home.
@app.route("/machine/submit", methods=('GET', 'POST'))
def machine_submit():
    if request.method == 'POST':
        name = request.form["machine"]
        description = request.form["machine_description"]

        if not name:
            flash('Title is required!')
        elif not description:
            flash('Content is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO Machine (1, 2) VALUES (?, ?)',
                         (name, description))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('submission.html', title="Submit A Machine")


@app.route("/all_resources")
def all_resources():
    conn = sqlite3.connect('project.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Resource')
    results = cur.fetchall()
    return render_template('all_resources.html', results=results, title="Resources")


@app.route("/resources/<int:id>")
def resource(id):
    conn = sqlite3.connect('project.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Resource WHERE id=?",(id,))
    data = cur.fetchone()
    return render_template('resources.html', title="Resources", resource=data,)


@app.errorhandler(404)
def error(e):
    return render_template("error.html", error=e)


# Start a basic inbuilt flask web server, should not use in a production but none of this is made for production.
if __name__ == '__main__':
    app.run(debug=True, port=8080)

