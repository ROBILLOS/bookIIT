import flask, time
from flask import request, flash, url_for, redirect, render_template
from forms import Registration, LogIn,AddVenue, AddEvent, Participate
from flask_login import login_user , logout_user , current_user , login_required, LoginManager
from config import app, db
from Models import User, Venue, Events, College, Admin_acc, Participant, COLLEGENAMES, participant_count
import datetime
from datetime import timedelta
from time import gmtime, strftime

strftime("%Y-%m-%d %H:%M:%S", gmtime())

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "You have logged out."

@app.route("/")

@app.route("/index", methods=['GET','POST'])
def login():
    form = LogIn(request.form)
    if form.validate_on_submit():
        #Does email exist in db?
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            #Is pass correct?
            if user.password == form.password.data:
                #If email exists and pass is correct, login.
                login_user(user)
                flash('Logged in successfully.')
                return redirect(url_for('landing'))
        flash ('Invalid email or password.', 'error')
    return render_template('index.html', form=form)

@app.route("/landing")
@login_required
def landing():
    if current_user.type == 1:
        return render_template('landing.html')
    else:
        return render_template('profile.html')

@app.route("/profile")
@login_required
def profile():
    image_file = url_for('static', filename='images/profile_pics/' + current_user.image_file)
    events = Events.query.all()
    return render_template('profile.html', events=events, image_file=image_file)

@app.route("/venue/manage", methods=['GET'])
@login_required
def venue():
    venues = Venue.query.all()
    colleges = College.query.all()
    return render_template('venue.html', venues=venues, colleges=colleges)

@app.route("/venue", methods=['GET'])
@login_required
def dispvenue():
    venues = Venue.query.all()
    colleges = College.query.all()
    return render_template('dispvenue.html', venues=venues, colleges=colleges)

@app.route("/venue-main", methods=['GET'])
@login_required
def mainvenue():
    venues = Venue.query.all()
    colleges = College.query.all()
    return render_template('venuemain.html', venues=venues, colleges=colleges)

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
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists. Try a different username.')
            return redirect(url_for('register'))
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already used. Use a different email address.')
            return redirect(url_for('register'))
        #if user,email does not exist yet, and passwords match, register.
        newacc = User(username=form.username.data, password=form.password.data, email=form.email.data, fname=form.fname.data, lname=form.lname.data)
        db.session.add(newacc)
        db.session.commit()
        flash('Account created!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login2():
    form = LogIn(request.form)
    if form.validate_on_submit():
        #Does email exist in db?
        user = User.query.filter_by(email=form.email.data).first()
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
    if current_user.type != 1:
        flash("You don't have permission to access this page.")
        return redirect(url_for('venue'))
    elif current_user.type == 1:
        form = AddVenue()
        if form.validate_on_submit():
            newvenue = Venue(name=form.name.data, college=form.college.data, capacity=form.capacity.data, rate=form.rate.data, equipment=form.equipment.data)
            db.session.add(newvenue)
            db.session.commit()
            flash('Venue created.')
            return redirect(url_for('venue'))
        return render_template('addvenue.html', form=form)

@app.route("/editvenue/<int:id>", methods=['GET', 'POST'])
@login_required
def editvenue(id):
    if current_user.type != 1:
        flash("You don't have permission to access this page.")
        return redirect(url_for('venue'))
    elif current_user.type == 1:
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
    if current_user.type != 1:
        flash("You don't have permission to access this page.")
        return redirect(url_for('venue'))
    elif current_user.type == 1:
        venue = Venue.query.filter_by(id=id).first()
        if venue != None:
            db.session.delete(venue)
            db.session.commit()
            flash('Event has been deleted.')
        else:
            flash('No such event exists!')
        return redirect(url_for('venue'))

def check_availability(start, end):
    events = Events.query.all()
    res = False
    #check if any approved dates have any overlaps
    for event in events:
        if event.status == 'Approved':
            overlap = start < event.end and event.start < end
            res = res or overlap
    return not res

@app.route("/addevent", methods=['GET', 'POST'])
@login_required
def addevent():
    form = AddEvent()
    datetimenow = datetime.datetime.now()
    weekfromnow = datetime.datetime.now() - timedelta(days=7)
    print form.validate()
    flash(form.errors)
    print form.datestart.data
    if form.validate_on_submit():
        starting = form.start.data+form.datestart.data
        print starting
        if (form.datestart.data < datetimenow):
            flash('Error. Date or Time start chosen has already passed!')
        elif(form.datestart.data < weekfromnow):
            flash('Error. You can only book dates from at least one week from today!')
        elif(check_availability(form.start.data, form.end.data) == False):
            flash('Venue has been booked for another event at this time.')
        else:
            newevent = Events(organizer=current_user.id, title=form.title.data, description=form.description.data, venue=form.venue.data, tags=form.tags.data, start=form.start.data, end=form.end.data, status='Pending')
            db.session.add(newevent)
            db.session.commit()
            flash('Event created. An administrator will approve it later.')
            return redirect(url_for('profile'))
    return render_template('booking.html', form=form)

disps = [
        { 'month':'Jan', 'color':'#781c2e', 'id':'January'},
        { 'month':'Feb', 'color':'#9966cc', 'id':'February'},
        { 'month':'March', 'color':'#7fffd4', 'id':'March'},
        { 'month':'April', 'color':'#cbe3f0', 'id':'April'},
        { 'month':'May', 'color':'#50c878', 'id':'May'},
        { 'month':'June', 'color':'#eae0c8', 'id':'June'},
        { 'month':'July', 'color':'#e0115f', 'id':'July'},
        { 'month':'Aug', 'color':'#e6e200', 'id':'August'},
        { 'month':'Sept', 'color':'#0f52ba', 'id':'September'},
        { 'month':'Oct', 'color':'#b297a0', 'id':'October'},
        { 'month':'Nov', 'color':'#ffc87c', 'id':'November'},
        { 'month':'Dec', 'color':'#40e0d0', 'id':'December'},

]

def Autorejecter():
    events = Events.query.all()
    for event in events:
        if(event.status == 'Pending' and event.start.date() < datetime.date.today()):
            event.status = 'Rejected.'
            event.admin_comment = 'Time has already lapsed. Please Rebook or Cancel this request.'
            db.session.commit()

@app.route("/event/manage", methods=['GET'])
@login_required
def event():
    if current_user.type != 1:
        flash("You don't have permission to access this page.")
        return redirect(url_for('profile'))
    elif current_user.type == 1:
        venues = Venue.query.all()
        Autorejecter()
        events = Events.query.all()
        users = User.query.all()
        return render_template('events.html', venues=venues, events=events, users=users)

@app.route("/event", methods=['GET'])
def dispevent():
    venues = Venue.query.all()
    Autorejecter()
    events = Events.query.filter_by(status='Pending')
    users = User.query.all()
    return render_template('dispevent.html', venues=venues, events=events, users=users, disps=disps)

@app.route("/editevent/<int:id>", methods=['GET','POST'])
@login_required
def editevent(id):
    event = Events.query.filter_by(id=id).first()
    venue = Venue.query.all()
    form = AddVenue() #EditVenue()
    if form.validate_on_submit():
        event.organizer = current_user.id
        event.name = form.name.data
        event.date=form.date.data
        event.time=form.time.data
        event.tags=form.tags.data
        event.venue=form.venue.data
        event.participantnum=form.participantnum.data
        db.session.commit()
        return redirect(url_for('events'))
    return render_template('editevent.html', form=form, event=event, venue=venue)

@app.route("/deleteevent/<int:id>", methods=['GET','POST'])
@login_required
def deleteevent(id):
    event = Events.query.filter_by(id=id).first()
    if event != None:
        db.session.delete(event)
        db.session.commit()
        flash('Event has been deleted.')
    else:
        flash('No such event exists!')
    return redirect(url_for('events'))

@app.route("/event/<int:id>/approved", methods=['GET', 'POST'])
@login_required
def approveevent(id):
    if current_user.type != 1:
        flash("You don't have permission to access this page.")
        return redirect(url_for('venue'))
    elif current_user.type == 1:
        event = Events.query.filter_by(id=id).first()
        event.status = 'Approved'
        db.session.commit()
        return redirect(url_for('profile'))

@app.route("/event/<int:id>/rejected", methods=['POST'])
@login_required
def rejectedevent(id):
    if current_user.type != 1:
        flash("You don't have permission to access this page.")
        return redirect(url_for('venue'))
    elif current_user.type == 1:
        event = Events.query.filter_by(id=id).first()
        event.status = 'Rejected'
        db.session.commit()
        return redirect(url_for('profile'))

@app.route("/event/<int:id>/participants", methods=['GET','POST'])
@login_required
def participant_list(id):
    event = Events.query.filter_by(id=id).first()
    if current_user.id != event.organizer or current_user.type != 1:
        flash("You don't have permission to access this page.")
        return redirect(url_for('events'))
    else:
        participants = Participant.query.filter_by(event=id)
        return render_template('events.html') #return render_template('participant_list.html', event=event, participants=participants)

@app.route("/event/<int:id>/invite")
@login_required
def invite(id):
    form = Participate()
    event = Events.query.filter_by(id=id).first()
    if event.status != 'Approved' or event == None:
        flash('No such event booked or approved.')
    else:
        newparticipant = Participant(event=id, fname=form.fname.data, lname=form.lname.data, email=form.email.data, contact=form.contact.data)
        db.session.add(newparticipant)
        db.session.commit()
        flash('Person invited to event.')
        return redirect(url_for('profile'))
    return render_template('profile.html') #return render_template('invite.html', event=event)

@app.route("/event/<int:id>/participate")
def participate(id):
    form = Participate()
    event = Events.query.filter_by(id=id).first()
    if event.status != 'Approved' or event == None:
        flash('No such event booked or approved.')
    else:
        newparticipant = Participant(event=id, fname=form.fname.data, lname=form.lname.data, email=form.email.data, contact=form.contact.data)
        db.session.add(newparticipant)
        db.session.commit()
        flash('Participant added.')
        return redirect(url_for('profile'))
    if current_user != None:
        return render_template('profile.html') #return render_template('participate.html', event=event, user=current_user)
    else:
        return render_template('profile.html') #return render_template('participate.html', event=event)

@login_manager.user_loader
def load_user(acc_id):
    reg_user = User.query.filter_by(id=acc_id).first()
    return reg_user

# db.create_all()
if __name__ == "__main__":
    app.run(debug=True)

