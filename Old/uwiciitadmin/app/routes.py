from app import app
from flask import jsonify
import json, os, signal
import requests
from flask import Flask, render_template, Markup, request, redirect, session, abort, url_for, flash, escape
from datetime import datetime

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename

# generate random integer values
from random import randint

from functools import wraps

# Flask Mongo
from flask_pymongo import PyMongo, MongoClient, BSONObjectIdConverter

# Forms
from wtforms import Form, validators

# Form Classes
from app.forms import CourseSelectTermForm, NewTranscriptForm, CourseFinderForm
from app.forms import QueryForm, PersonalInfoForm, EmergencyContactForm
from app.forms import EventForm, LoginForm
from app.forms import NewUserForm

from bson import Binary, Code, ObjectId
from bson.json_util import dumps

#easy_install Flask-Session or pip install Flask-Session
from flask import Flask, session

#include pprint for readabillity of the 
from pprint import pprint

from dotenv import load_dotenv
load_dotenv(verbose=True)

# Keys
SECRET_KEY = os.getenv("SECRET_KEY")
MONGO_URL = os.getenv("MONGO_URL")

# Uploads
UPLOAD_FOLDER = os.path.basename('userphotos')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Setup Session to keep user logged in
app.config['SESSION_TYPE'] = 'memcached' 
app.config['SECRET_KEY'] = SECRET_KEY 

SESSION_TYPE = 'redis'
#Session(app)

# Setup Mongo Client Information
client = MongoClient(MONGO_URL)
db=client.UWICIIT

menu_type = 1
username = ""

# Wrapper function to prevent users from requesting unauthorized pages
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))

    return wrap


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def loguseractvity(activity, location):
    
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

    db.systemlog.insert_one({"user": session['userid'],"activty":activity, "location":location,"timestamp": date_time})

    return True

def getUserQuickLinks():
    
    QuickLinks = [
        {
            'title': "View Semester Grades",
            'link': "",
        },
        {
            'title': "View Profile",
            'link': "",
        },{
            'title': "View Schedule",
            'link': "",
        }
    ]

    return QuickLinks

@app.route('/')
@login_required
def home():

    global menu_type
    global username

    menu_type = 1
    #username = session['username']

    collection = db.student.find_one({'student_id': "27001022"})

    #return collection['student_id']
    return render_template('index.html', title='UWICIIT System', user = username)

@app.route('/stopServer', methods=['GET'])
def stopServer():
    os.kill(os.getpid(), signal.SIGINT)
    return jsonify({ "success": True, "message": "Server is shutting down..." })

@app.route('/index')
def index():

    global menu_type
    global username
    menu_type = 1
    username = session['username']

    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=username, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        UserLoggedIn = db.user.find_one({'UserID': form.username.data})
        if UserLoggedIn:
            
            # Check the password matches
            if( UserLoggedIn['password'] == form.password.data ):
                
                # Setup Session
                sessionState = setSessionInformation(form.username.data, UserLoggedIn['name'], UserLoggedIn['email'])

                # Record User Activity
                loguseractvity("Login Success", "/login")
                
                if sessionState == "OK":
                    ses = "S" 

                return redirect('/index')
            else:
                flash('Invalid User Credentials entered. Try Again')
        else:
            flash('Invalid User Credentials entered. Try Again')

    return render_template('login.html', title='Sign In', form=form)

def setSessionInformation(userID, name, email):

    session['username'] = name
    session['userid'] = userID
    session['email'] = email
    session['logged_in'] = True
    return 'OK'

@app.route("/logout")
@login_required
def logout():

    session['logged_in'] = False
    session.clear()
    return home()

@app.route('/forgotPassword')
@login_required
def forgotPassword():

    # Record User Activity
    loguseractvity("View", "/forgotPassword")
    
    return render_template('login.html', title='UWICIIT Forgot Password') 

@app.route('/newuser', methods=['GET', 'POST'])
def newuser():
    form = NewUserForm()
    if request.method=='POST':
        db.user.insert_one(form.data)
        
    return render_template('newuser.html', title='New User', form=form)

@app.route('/users/view', methods=['GET', 'POST'])
def allusers():
    userId = session['userid']
    db.user.aggregate([
            {
                "$lookup": {
                    "from": "systemlog",
                    "localField": "UserID",    
                    "foreignField": "user",  
                    "as": "lastlogin"
                }                
            }])
    data = list(db.user.find({}))
    return render_template('users-view.html', title='View System Users', data=data, userId=userId)

@app.context_processor
def inject_user():
    global menu_type
    return dict(menu_type=menu_type)

############################################################
########## Query | Personal Information ROUTING  ###########
############################################################

@app.route('/querypage', methods = ['GET', 'POST'])
def query():
    form = QueryForm()
    userId = int(session['userid'])
    email = session['email']
    data = db.query.find({"studentId" : userId})

    global menu_type
    global username
    menu_type = 1
    username = session['username']

    # Record User Activity
    loguseractvity("View", "/querypage/")
    
    if request.method=='POST':
        db.query.insert_one(form.data)
        
    return render_template('querypage.html', title='Student Query', form=form, userId=userId, data=data,user = username, email = email)

@app.route('/personalInfo', methods=('GET', 'POST'))
@login_required
def personalinfoOptions():

    # Record User Activity
    loguseractvity("View", "/personalInfo/")
    
    return render_template('personalinfo.html', title='Personal Info')

@app.route('/personalInfo/update', methods=('GET', 'POST'))
@login_required
def personalinfopage():

    global menu_type
    global username
    menu_type = 1
    username = session['username']

    form = PersonalInfoForm()
    ecform = EmergencyContactForm()
    userId = int(session['userid'])
    
    if request.method=='POST':

        # Update the student based on their logged in ID
        db.student.update_one({"studentId": userId},{"$set":{"gender": form.data["gender"],"dob":form.data["dob"], "maritalStatus":form.data["maritalStatus"], "studentAddress":form.data["studentAddress"], "mobilenum":form.data["mobilenum"], "emergency_contact": {"emergencyCon": ecform.data["emergencyCon"], "relationship": ecform.data["relationship"], "ecNumber": ecform.data["ecNumber"] }}})
        
        # Record User Activity
        loguseractvity("Edit", "/personalInfo/update/" + ObjectId(id))

    else:

        # Pull the users current information from the database
        studentData = db.student.find_one({"studentId" : userId})

    return render_template('personalinfopage.html', title='Personal Info', form=form, ecform=ecform, userId=userId, user = username, studentData = studentData)

############################################################
##################### Events ROUTING  ######################
############################################################

@app.route('/events')    
def eventsview():
    
    global menu_type
    global username
    menu_type = 3
    username = session['username']

    # Record User Activity
    loguseractvity("View", "/events")

    data = list(db.events.find({}))
    return render_template('event-view.html', data = data,title='View Events', user = username)

@app.route('/events/add', methods = ['GET', 'POST'])
def eventsadd():

    # mydict = ["name":] 
    form = EventForm()
    
    global menu_type
    global username
    menu_type = 3
    username = session['username']
    filename = ""

    if request.method == 'POST':

        file = request.files["photo"]

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # generate some integers
            randvalue = randint(10, 10000000)

            # Directory 
            directory = form.data["name"] + "" + str(randvalue)
            directory = directory.replace(" ", "")
  
            # mode 
            mode = 0o777

            #path
            path = os.path.join(app.config['UPLOAD_FOLDER'], directory) 
            
            #create directory
            os.mkdir(path, mode)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'] + "/" + directory , filename))

        events_id = db.events.insert_one({"name": form.data["name"],"eventDate":form.data["eventDate"], "location":form.data["location"],"photo": directory + "/" + filename})

        # Record User Activity
        loguseractvity("Add", "/events/add")

        return redirect(url_for('eventsview'))

    return render_template('event-add.html', title='Add Events', form = form, user = username)

@app.route('/events/edit/<id>', methods = ['GET', 'POST'])
def eventsedit(id):
    form = EventForm()
    
    global menu_type
    global username
    menu_type = 3
    username = session['username']

    data = db.events.find({"_id" : ObjectId(id)})

    if request.method =='POST':
        db.events.update_one({"_id": ObjectId(id)},{"$set":{"name": form.data["name"],"dt":form.data["dt"], "location":form.data["location"]}})
    
    # Record User Activity
    loguseractvity("Edit", "/events/edit/" + ObjectId(id))

    return render_template('event-edit.html', title='Edit Events', data = data, form = form, user = username)

@app.route('/events/delete/<id>')
def eventsdelete(id):

    global menu_type
    global username
    menu_type = 3
    username = session['username']

    db.events.remove({"_id": ObjectId(id)})

    # Record User Activity
    loguseractvity("Delete", "/events/delete/" + ObjectId(id))

    return render_template('event-delete.html', title='Delete Events', user = username)
