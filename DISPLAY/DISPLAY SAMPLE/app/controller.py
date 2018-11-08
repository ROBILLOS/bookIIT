from app import app
import models
from flask import render_template, redirect, request


@app.route('/')
def index():
    users = models.Users.all()
    return render_template('index.html', data=users)