import sqlite3
from Ziggeo import Ziggeo
from flask import Flask, render_template, request, g, redirect, url_for, \
             abort, flash, session
from contextlib import closing

app = Flask(__name__, static_folder='static', static_url_path='')
app.config.from_object('__init__')

ziggeo = Ziggeo("61113f2c9913e0daecefe88965a37dac", "d6e6a6620c4ae5f36c3a47dfac6fc274", "11cd57eafb2262c7829983d76bcff0c6")

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/newuser", methods=['POST'])
def new_user():
    name = request.form['name']
    my_hash = request.form['password']
    email = request.form['email']
    school = request.form['school']
    prof = int(request.form['type'])
    r = g.db.execute('''INSERT INTO USERS (name, hash, email, school, prof) \
                  VALUES ('%s', '%s', '%s', '%s', '%d')''' % (name, my_hash, email, school, prof))
    # not safe at all
    g.db.commit()
    # result = g.db.execute("SELECT * FROM USERS")
    return render_template('dashboard.html')

@app.route("/class/<course>", methods=['GET'])
def classes(course=None):
    return render_template('class.html', ziggeo=ziggeo, course=course)

@app.route("/signin", methods=['POST'])
def signin():
    email = request.form['email']
    my_hash = request.form['password']
    if request.method == 'POST':
        r = g.db.execute('SELECT hash FROM USERS WHERE email= \"' + email + '\"')
        if r.fetchone()[0] == my_hash:
            return redirect(url_for('dashboard'))
    return redirect(url_for('index'))

def converttoString(s):
    result = '/'
    for i in s:
        result += str(i)+'/'
    return result

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

@app.route("/layout")
def layout():
    return render_template('layout.html')

# initializes DB
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

if __name__ == "__main__":
    app.run(debug=True)
