import sqlite3
from Ziggeo import Ziggeo
from flask import Flask, render_template, request, g, redirect, url_for, \
             abort, flash, session
from contextlib import closing
import datetime
import unicodedata
import time

app = Flask(__name__, static_folder='static', static_url_path='')
app.config.from_object('__init__')

# My key, so don't you use this. seriously
ziggeo = Ziggeo("61113f2c9913e0daecefe88965a37dac", "d6e6a6620c4ae5f36c3a47dfac6fc274", "11cd57eafb2262c7829983d76bcff0c6")

@app.route("/")
def index():
    if not 'email' in session:
        return render_template('index.html')
    return redirect(url_for('dashboard'))

# CREATE LOG IN AND OUT STUFF
@app.route("/newuser", methods=['POST'])
def new_user():
    name = request.form['name']
    my_hash = request.form['password']
    email = request.form['email']
    school = request.form['school']
    prof = int(request.form['type'])
    r = g.db.execute('''INSERT INTO USERS (name, hash, email, school, prof, courses) \
                  VALUES ('%s', '%s', '%s', '%s', '%d', '%s')''' % (name, my_hash, email, school, prof, "|"))
    # not safe at all
    g.db.commit()
    # result = g.db.execute("SELECT * FROM USERS")
    session['email'] = email
    session['name'] = name
    session['school'] = school
    session['courses'] = "|"
    if prof == 1:
        session['is_prof'] = True
        session['type'] = "Professor/TA"
    else:
        session['is_prof'] = False
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
            session['courses'] = info[5]
            if acct == 1:
                session['is_prof'] = True
                session['type'] = "Professor/TA"
            else:
                session['is_prof'] = False
                session['type'] = "Student"
            flash('You successfully logged in!')
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
        flash("Please log in to view content.")
        return redirect(url_for('index'))
    else:
        r = g.db.execute('SELECT * FROM COMMENTS').fetchall()
        print r
        if not r:
            r = []
        return render_template('class.html', ziggeo=ziggeo, course=course, datetime=datetime, comments=r)

@app.route("/dashboard")
def dashboard():
    if not 'email' in session:
        flash("Please log in to view content.")
        return redirect(url_for('index'))
    else:
        r = g.db.execute('SELECT * FROM USERS WHERE email= \"' + session['email'] + '\"')
        session['courses'] = r.fetchone()[5]
        return render_template('dashboard.html', email=session['email'], name=session['name'], school=session['school'], account=session['type'], is_prof = session['is_prof'], courses=session['courses'])

@app.route("/layout")
def layout():
    return render_template('layout.html')

@app.route("/addclass", methods=['POST'])
def addclass():
    name = session['name']
    email = session['email']
    q = g.db.execute('SELECT courses FROM USERS WHERE email= \"' + email + '\"')
    courselist = q.fetchone()[0]
    course = request.form['course']
    courselist += course + "|"
    #TODO class capacity
    cap=100
    #add to courses DB
    r = g.db.execute('''INSERT INTO COURSES (name, cap) \
                  VALUES ('%s', '%d')''' % (course, cap))
    #add to users DB
    s = g.db.execute('UPDATE USERS SET courses= \"' + courselist + '\" WHERE email= \"' + email + '\"')
    # not safe at all
    g.db.commit()
    flash('Successfully added '+ name + "!")
    return redirect(url_for('dashboard'))

@app.route("/addcomment", methods=['POST'])
def addcomment():
    comment = request.form['commentText']
    videoId = request.form['videoId']
    course = request.form['currCourse']
    # commentTime = 1
    commentTime = time.strftime("%x") + " " + time.strftime("%X")
    if request.method == 'POST':
        r = g.db.execute('''INSERT INTO COMMENTS (id, usr, time, comm) \
                  VALUES ('%s', '%s', '%s', '%s')''' % (videoId, session['name'], commentTime, comment))
        # not safe at all
        g.db.commit()
        flash("Successfully posted a comment.")
        r = g.db.execute('SELECT * FROM COMMENTS').fetchall()
        print r
        if not r:
            r = []
        return render_template('class.html', ziggeo=ziggeo, course=course, datetime=datetime, comments=(r))

@app.route("/allclasses")
def allclasses():
    if not 'email' in session:
        flash("Please log in to view content.")
        return redirect(url_for('index'))
    else:
        q = g.db.execute('SELECT * FROM USERS WHERE email= \"' + session['email'] + '\"')
        session['courses'] = q.fetchone()[5]
    r = g.db.execute('SELECT name FROM COURSES')
    courselist = [str(x)[3:-3] for x in r.fetchall()]
    mycourses = session['courses'].split('|')[1:-1]
    if not len(mycourses):
        mycourses = None
    return render_template('showall.html', courses=courselist, mycourses=mycourses)

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
