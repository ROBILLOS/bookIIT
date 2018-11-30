from flask import Flask,session, request, flash, url_for, redirect, render_template, abort ,g
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/my_first_local_site_database'
db = SQLAlchemy(app)

class User(db.Model):
	_tablename_ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60),nullable=False)

	def __init__(self, username, email):
		self.username = username
		self.email = email

	def __repr__(self):
		return '<User %r>' %self.username


app.static_folder = 'static'

@app.route("/")
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)