import sqlite3
# from Ziggeo import Ziggeo
from flask import Flask, render_template, request, g, redirect, url_for, \
             abort, flash, session
from contextlib import closing
import datetime

app = Flask(__name__, static_folder='static', static_url_path='')
app.config.from_object('__init__')

# ziggeo = Ziggeo("61113f2c9913e0daecefe88965a37dac", "d6e6a6620c4ae5f36c3a47dfac6fc274", "11cd57eafb2262c7829983d76bcff0c6")

@app.route("/")
def index():
    return render_template('index.html')

# CREATE LOG IN AND OUT STUFF
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
    session['email'] = email
    session['name'] = name
    session['school'] = school
    if prof == 1:
        session['is_prof'] = 1
        session['type'] = "Professor/TA"
    else:
        session['is_prof'] = 0
        session['type'] = "Student"
    flash('You successfully created an account!')
    return redirect(url_for('dashboard'))

@app.route("/signin", methods=['POST'])
def signin():
    email = request.form['email']
    my_hash = request.form['password']
    if request.method == 'POST':
        r = g.db.execute('SELECT hash FROM USERS WHERE email= \"' + email + '\"')
        if r.fetchone()[0] == my_hash:
            r2 = g.db.execute('SELECT * FROM USERS WHERE email= \"' + email + '\"')
            session['email'] = email
            info = r2.fetchone()
            session['name'] = info[0]
            session['school'] = info[3]
            acct = info[4]
            if acct == 1:
                session['is_prof'] = 1
                session['type'] = "Professor/TA"
            else:
                session['is_prof'] = 0
                session['type'] = "Student"
            flash('You were successfully logged in!')
            return redirect(url_for('dashboard'))
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('email', None)
    flash('You were logged out.')
    return redirect(url_for('index'))


@app.route("/class/<course>", methods=['GET'])
def classes(course=None):
    if not 'email' in session:
        flash("Please log in.")
        return redirect(url_for('index'))
    else:
        return render_template('class.html', ziggeo=ziggeo, course=course, datetime=datetime)

def converttoString(s):
    result = '/'
    for i in s:
        result += str(i)+'/'
    return result

@app.route("/dashboard")
def dashboard():
    if not 'email' in session:
        flash("Please log in.")
        return redirect(url_for('index'))
    else:
        return render_template('dashboard.html', email=session['email'], name=session['name'], school=session['school'], account=session['type'], is_prof = session['is_prof'])

@app.route("/layout")
def layout():
    return render_template('layout.html')

@app.route("/addcomment", methods=['POST'])
def addcomment():
    comment = request.form['commentText']
    videoId = request.form['videoId']

    if request.method == 'POST':
        # r = g.db.execute('SELECT hash FROM USERS WHERE email= \"' + email + '\"')
        # if r.fetchone()[0] == my_hash:
        #     r2 = g.db.execute('SELECT * FROM USERS WHERE email= \"' + email + '\"')
        #     session['email'] = email
        #     info = r2.fetchone()
        #     session['name'] = info[0]
        #     session['school'] = info[3]
        #     acct = info[4]
        #     if acct == 1:
        #         session['is_prof'] = 1
        #         session['type'] = "Professor/TA"
        #     else:
        #         session['is_prof'] = 0
        #         session['type'] = "Student"
        #     flash('You were successfully logged in!')
            return redirect(url_for('class'))
    return redirect(url_for('index'))


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
    app.secret_key = 'jellyjellyjelly'
    app.run(debug=True)
