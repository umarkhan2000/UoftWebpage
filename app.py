import sqlite3
from flask import Flask, g, request, render_template, redirect, url_for, session, logging, flash
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = '0a80bacbd7cbc224e26534d1ced8d99c'
DATABASE = './database.db'


#Register Page
@app.route("/register", methods=['GET', 'POST'] )
def register():
	db=get_db()
	db.row_factory = make_dicts
	form = RegistrationForm()


	if request.method == 'POST' and form.validate():	
		return redirect(url_for('home'))

	return render_template('register.html', title='Register', form=form)


#Login Page 
@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	error = None
	db=get_db()
	db.row_factory = make_dicts

	if request.method == 'POST':
		utorid=request.form['utorid']
		password=request.form['password']

		user=query_db('select * from user_info where utorid=? and password=?', [utorid, password], one=True)
		position=query_db('select position from user_info where utorid=? and password=?', [utorid, password], one=True)
		firstname=query_db('select firstname from user_info where utorid=? and password=?', [utorid, password], one=True)

		if user:
			session['user']=firstname
			#return redirect(url_for('index'))
			if position['position'] == 'Student':					#check to see whether the user is a student or instructor
				return redirect(url_for('assignments'))
			elif user['position'] == 'Instructor':
				return redirect(url_for('news'))

		return redirect(url_for('login'))

	elif 'user' in session:
		return redirect(url_for('index'))
	else:	
		return render_template('login.html', form=form)



@app.route("/assignments")
def assignments():
	if 'user' in session:
		firstname = session['user']
	else:
		return redirect(url_for('login'))

	return render_template('assignments.html')

@app.route("/labs")
def labs():
	if 'user' in session:
		firstname = session['user']
	else:
		return redirect(url_for('login'))

	return render_template('labs.html')

@app.route("/news")
def news():
	if 'user' in session:
		firstname = session['user']
	else:
		return redirect(url_for('login'))

	return render_template('news.html')

@app.route("/resources")
def resources():
	if 'user' in session:
		firstname = session['user']
	else:
		return redirect(url_for('login'))

	return render_template('resources.html')

@app.route("/syllabus")
def syllabus():
	if 'user' in session:
		firstname = session['user']
	else:
		return redirect(url_for('login'))

	return render_template('syllabus.html')

@app.route("/tests")
def tests():
	if 'user' in session:
		firstname = session['user']
	else:
		return redirect(url_for('login'))

	return render_template('tests.html')



@app.route("/index")
def index():
	if 'user' in session:
		firstname = session['user']
	else:
		return redirect(url_for('login'))

	return render_template('index.html')
	
@app.route('/logout')
def logout():
	session.pop('user', None)
	return redirect(url_for('login'))

#SQL Functions
#the function get_db is taken from here 
#https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/

def get_db():
	db=getattr(g, '_database', None)
	if db is None:
		db=g._database=sqlite3.connect(DATABASE)
	return db


#the function make_dicts is taken from here 
#https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


#the function query_db is taken from here 
#https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


#the function close_connection is taken from here 
#https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
    	# close the database if we are connected to it
        db.close()




if __name__ == '__main__':
	app.run(debug=True)
