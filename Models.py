
from config import db

COLLEGENAMES = {
    'MSU-IIT': 1,
    'College of Engineering': 2,
    'College of Science and Mathematics': 3,
    'College of Education': 4,
    'College of Arts and Social Science': 5,
    'College of Business Administration and Accountancy': 6,
    'College of Nursing': 7,
    'School of Computer Studies': 8,
    'Integrated Developmental School': 9,
    'PRISM': 10
}

class Acc(db.Model):
    __tablename__ = "account"
    id = db.Column('acc_id', db.Integer , primary_key=True)
    type = db.Column('acc_type', db.Integer)
    username = db.Column('username', db.String(), unique=True, index=True)
    password = db.Column('password', db.String())
    email = db.Column('email', db.String(), unique=True, index=True)

    def __init__(self, username, password, email):
        self.username = username
        self.type = 0;
        self.password = password
        self.email = email

    def is_authenticated(self):
        return True

    def is_admin(self):
        return type == 1

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<Acc %r>' % (self.username)

class User(db.Model):
    __tablename__ = "user_acc"
    id = db.Column('user_id', db.Integer , primary_key=True)
    fname = db.Column('fname', db.String())
    lname = db.Column('lname', db.String())
    contact = db.Column('contact', db.String())

    def __init__(self, id, fname, lname, contact):
        self.id = id
        self.fname = fname
        self.lname = lname
        self.contact = contact

class Admin_acc(db.Model):
    __tablename__ = "admin_acc"
    id = db.Column('admin_id', db.Integer , primary_key=True)
    college = db.Column('college_id', db.Integer , primary_key=True)
    fname = db.Column('fname', db.String())
    lname = db.Column('lname', db.String())
    contact = db.Column('contact', db.String())

    def __init__(self, id, fname, lname, college, contact):
        self.id = id
        self.fname = fname
        self.lname = lname
        self.college = COLLEGENAMES.get(college, 1)
        self.contact = contact

class Venue(db.Model):
    __tablename__ = "venue"
    id = db.Column('venue_id', db.Integer , primary_key=True)
    college = db.Column('college_id', db.Integer , primary_key=True)
    name = db.Column('venue_name', db.String())
    capacity = db.Column('capacity', db.Integer())
    rate = db.Column('rate', db.Integer)
    equipment = db.Column('equipment', db.String())

    def __init__(self, name, college, capacity, rate, equipment):
        self.name = name
        self.college = COLLEGENAMES.get(college, 1)
        self.capacity = capacity
        self.rate = rate
        self.equipment = equipment

    def get_id(self):
        return unicode(self.id)

class College(db.Model):
    __tablename__ = "college"
    id = db.Column('college_id', db.Integer , primary_key=True)
    name = db.Column('college_name', db.String())
    abb = db.Column('college_abb', db.String())

    def __init__(self, name, abb):
        self.id = id
        self.name = name
        self.abb = abb

class Events(db.Model):
    __tablename__ = "events"
    organizer = db.Column('organizer_id', db.Integer)
    venue = db.Column('venue_id', db.Integer)
    id = db.Column('event_id', db.Integer , primary_key=True)
    title = db.Column('event_name', db.String())
    description = db.Column('event_desc', db.String())
    tags = db.Column('event_tags', db.String())
    date = db.Column('event_date', db.Date())
    start = db.Column('event_time_s', db.Time())
    end = db.Column('event_time_e', db.Time())
    partnum = db.Column('expected_participants', db.Integer())
    status = db.Column('event_status', db.String())

    def __init__(self, organizer, venue, title, description, tags, date, start, end, partnum, status ):
        self.organizer = organizer
        self.title = title
        self.description = description
        self.venue = venue
        self.tags = tags
        self.date = date
        self.start = start
        self.end = end
        self.partnum = partnum
        self.status = status




