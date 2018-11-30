from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField,DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, InputRequired
from wtforms_components import TimeField 
import config


class Registration(FlaskForm):
	fname = StringField('First Name',
							validators=[InputRequired(), Length(min=2, max=20)])
	lname = StringField('Last Name',
							validators=[InputRequired(), Length(min=2, max=20)])
	username = StringField('Username',
							validators=[InputRequired(), Length(min=5, max=16)])
	email = StringField('Email',
							validators=[InputRequired(), Email()])
	password = PasswordField('Password',
							validators=[InputRequired(), EqualTo('confirm_password', message='Passwords do not match,')])
	confirm_password = PasswordField('Confirm Password',
							validators=[InputRequired()])

#def validate_username(self, username):
	#user = User.query.filter_by(username=username.data).first()
	#if user:
		#raise ValidationError('That username already exists! Please use a different one.')

#def validate_email(self, email):
	#user = User.query.filter_by(email=email.data).first()
	#if user:
		#raise ValidationError('That e-mail is already in use! Please use a different one.')


class LogIn(FlaskForm):
	email = StringField('Email',
							validators=[InputRequired(), Email()])
	password = PasswordField('Password',
							validators=[InputRequired()])
	remember = BooleanField('Remember Me')

class AddVenue(FlaskForm):
	name = StringField('Venue Name',
							validators=[DataRequired()])
	college = SelectField('College', id='college_id',
							validators=[DataRequired()], choices=[('MSU-IIT', 'MSU-IIT'), ('College of Engineering and Technology', 'College of Engineering and Technology'), ('College of Science and Mathematics', 'College of Science and Mathematics'), ('College of Education', 'College of Education'), ('College of Arts and Social Sciences', 'College of Arts and Social Sciences'), ('College of Business Administration and Accountancy', 'College of Business Administration and Accountancy'), ('College of Nursing', 'College of Nursing'), ('School of Computer Studies', 'School of Computer Studies'), ('Integrated Developmental School', 'Integrated Developmental School'), ('PRISM', 'PRISM')])
	capacity = IntegerField('Capacity',
							validators=[Optional()])
	rate = IntegerField('Rate',
							validators=[Optional()])
	equipment = StringField('Equipment',
							validators=[Optional()])
	submit = SubmitField('Add Venue')

class AddEvent(FlaskForm):
	title = StringField('Title',
							validators=[DataRequired()])
	description = StringField('Description',
							validators=[DataRequired()])
	venue = SelectField('Venue',
							validators=[DataRequired()], choices=[('2', 'Gymnasium'), ('3','ICT 3H')])
	tags = StringField('Tags',
							validators=[Optional()])
	partnum = IntegerField('Participants',
							validators=[Optional()])
	date = DateField('Date', 
							validators=[DataRequired()])
	start = TimeField('Start Time',
							validators=[DataRequired()])
	end = TimeField('End Time',
							validators=[DataRequired()])
	submit = SubmitField('Request Event')