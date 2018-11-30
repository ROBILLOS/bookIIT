import flask
from flask import request, flash, url_for, redirect, render_template
from forms import Registration, LogIn,AddVenue, AddEvent
from flask_login import login_user , logout_user , current_user , login_required, LoginManager
from config import app, db
from Models import Acc, User, Venue, Events, College, Admin_acc, COLLEGENAMES

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "You have logged out."

@app.route("/")

@app.route("/index", methods=['GET','POST'])
def main():
    return render_template('index.html')

@app.route("/landing")
@login_required
def landing():
    return render_template('landing.html')

@app.route("/profile")
@login_required
def profile():
    return render_template('profile.html')

@app.route("/venue", methods=['GET'])
@login_required
def venue():
    venues = Venue.query.all()
    colleges = College.query.all()
    return render_template('venue.html', venues=venues, colleges=colleges)

@app.route("/logout")
@login_required
def logout():
    flash('You have logged out!')
    logout_user()
    return redirect(url_for('login'))

@app.route("/register", methods=['GET','POST'])
def register():
    form = Registration()
    if form.validate_on_submit():
        print form.username.data
        #if username/email is already used
        if Acc.query.filter_by(username=form.username.data).first():
            flash('Username already exists. Try a different username.')
            return redirect(url_for('register'))
        if Acc.query.filter_by(email=form.email.data).first():
            flash('Email already used. Use a different email address.')
            return redirect(url_for('register'))
        #if user,email does not exist yet, and passwords match, register.
        newacc = Acc(username=form.username.data, password=form.password.data, email=form.email.data)
        db.session.add(newacc)
        db.session.commit()
        #user is an account. so create account first before assigning user.
        user = User(Acc.get_id(newacc),form.fname.data, form.lname.data, '')
        db.session.add(user)
        db.session.commit()
        flash('Account created for Acc.username!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LogIn(request.form)
    if form.validate_on_submit():
        #Does email exist in db?
        user = Acc.query.filter_by(email=form.email.data).first()
        if user:
            #Is pass correct?
            if user.password == form.password.data:
                #If email exists and pass is correct, login.
                login_user(user)
                flash('Logged in successfully.')
                return redirect(url_for('landing'))
        flash ('Invalid email or password.', 'error')
    return render_template('login.html', form=form)

@app.route("/addvenue", methods=['GET', 'POST'])
@login_required
def addvenue():
    form = AddVenue()
    if form.validate_on_submit():
        #Venues are now all stored in the venues table. They only differ with college id. reference the initialize college script for college ids.
        newvenue = Venue(name=form.name.data, college=form.college.data, capacity=form.capacity.data, rate=form.rate.data, equipment=form.equipment.data)
        #Note that college will accept String values, specifically only those specified in the dictionary added in Models.py
        #If string doesn't match, by default, it will take on the value of 1/ 'MSU-IIT'.
        #Those string values are converted to corresponding id numbers of those colleges in the db.
        db.session.add(newvenue)
        db.session.commit()
        flash('Venue created.')
        return redirect(url_for('venue'))
    return render_template('addvenue.html', form=form)

@app.route("/editvenue/<int:id>", methods=['GET', 'POST'])
@login_required
def editvenue(id):
    venue = Venue.query.filter_by(id=id).first()
    form = AddVenue()
    if form.validate_on_submit():
        venue.name = form.name.data
        venue.college = COLLEGENAMES.get(form.college.data)
        venue.capacity = form.capacity.data
        venue.rate = form.rate.data
        venue.equipment = form.equipment.data
        db.session.commit()
        flash('Venue created.')
        return redirect(url_for('venue'))
    return render_template('editvenue.html', form=form, venue=venue)

@app.route("/deletevenue/<int:id>", methods=['GET','POST'])
@login_required
def deletevenue(id):
    venue = Venue.query.filter_by(id=id).first()
    if venue != None:
        db.session.delete(venue)
        db.session.commit()
        flash('Event has been deleted.')
    else:
        flash('No such event exists!')
    return redirect(url_for('venue'))

@app.route("/addevent", methods=['GET', 'POST'])
@login_required
def addevent():
    form = AddEvent()
    if flask.request.method == 'POST':
        print('imong mama')
        newevent = Events(organizer=current_user.id, title=form.title.data, description=form.description.data, venue='3', tags=form.tags.data, partnum=form.partnum.data, date=form.date.data, start=form.start.data, end=form.end.data)
        db.session.add(newevent)
        db.session.commit()
        flash('Event created. An administrator will approve it later.')
    return render_template('booking.html', form=form)

@app.route("/event", methods=['GET'])
@login_required
def event():
    venues = Venue.query.all()
    events = Event.query.all()
    return render_template('events.html', venues=venues, events=events)

@app.route("/editevent/<int:id>", methods=['GET','POST'])
@login_required
def editevent(id):
    event = Event.query.filter_by(id=id).first()
    venue = Venue.query.all()
    form = AddVenue() #EditVenue()
    if form.validate_on_submit():
        event.organizer = current_user
        event.name = form.name.data
        event.date=form.date.data
        event.time=form.time.data
        event.tags=form.tags.data
        #event.status=form.status.data------------not yet tested. will implement after admin acc is properly implemented.
        event.venue=form.venue.data
        event.participantnum=form.participantnum.data
        db.session.commit()
        return redirect(url_for('events'))
    return render_template('editevent.html', form=form, event=event, venue=venue)

@app.route("/deleteevent/<int:id>", methods=['GET','POST'])
@login_required
def deleteevent(id):
    event = Event.query.filter_by(id=id).first()
    if event != None:
        db.session.delete(event)
        db.session.commit()
        flash('Event has been deleted.')
    else:
        flash('No such event exists!')
    return redirect(url_for('events'))

@login_manager.user_loader
def load_user(acc_id):
    reg_user = Acc.query.filter_by(id=acc_id).first()
    return reg_user

# db.create_all()
if __name__ == "__main__":
    app.run(debug=True)

