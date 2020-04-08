from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):

	firstname = StringField('Firstname', validators=[DataRequired(), Length(min=2, max=20)]) 
	lastname = StringField('Lastname', validators=[DataRequired(), Length(min=2, max=20)]) 
	utorid = StringField('Utorid', validators=[DataRequired(), Length(min=2, max=13)])
	email = StringField('Email', validators=[DataRequired(), Length(min=2, max=13), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm_Password', validators=[DataRequired(), EqualTo('password', message='Passwords do not match')])
	user_role = SelectField('User_Role', choices = [('1', 'Student'), ('2', 'Instructor')], validators=[DataRequired()])
	submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):

	utorid = StringField('Utorid', validators=[DataRequired(), Length(min=2, max=13)])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Login')