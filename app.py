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

		if user:
			return redirect(url_for('home'))


	return render_template('login.html', form=form)


@app.route("/labs")
def labs():

	return render_template('labs.html')
	

@app.route("/index")
def home():

	return render_template('index.html')
	


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