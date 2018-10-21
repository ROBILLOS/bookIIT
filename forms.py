from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional

class Registration(FlaskForm):
	fname = StringField('First Name',
							validators=[DataRequired(), Length(min=5, max=20)])
	lname = StringField('Last Name',
							validators=[DataRequired(), Length(min=2, max=20)])
	username = StringField('Username', 
							validators=[DataRequired(), Length(min=5, max=16)])
	email = StringField('Email',
							validators=[DataRequired(), Email()])
	password = PasswordField('Password',
							validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password',
							validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Create Account')

def validate_username(self, username):
	user = User.query.filter_by(username=username.data).first()
	if user:
		raise ValidationError('That username already exists! Please use a different one.')

def validate_email(self, email):
	user = User.query.filter_by(email=email.data).first()
	if user:
		raise ValidationError('That e-mail is already in use! Please use a different one.')


class LogIn(FlaskForm):
	email = StringField('Email',
							validators=[DataRequired(), Email()])
	password = PasswordField('Password',
							validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Log In')

class AddVenue(FlaskForm):
	room = StringField('Room Name',
							validators=[DataRequired()])
	college = StringField('Password',
							validators=[DataRequired()])
	location = StringField('Location',
							validators=[Optional()])
	capacity = StringField('Capacity',
							validators=[Optional()])
	rate = StringField('Rate',
							validators=[Optional()])
	equipment = StringField('Equipment',
							validators=[Optional()])
	submit = SubmitField('Add Venue')


