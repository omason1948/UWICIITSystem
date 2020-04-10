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
    username = session['username']

    collection = db.student.find_one({'student_id': "27001022"})

    #return collection['student_id']
    return render_template('index.html', title='UWICIIT System', user = username)

@app.route('/stopServer', methods=['GET'])
def stopServer():
    os.kill(os.getpid(), signal.SIGINT)
    return jsonify({ "success": True, "message": "Server is shutting down..." })

@app.route('/index')
@login_required
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

# Registration Functions Section
@app.route('/academic-information')
@login_required
def registration(): 

    topOptions = [
        {
            'title': "Registration Status",
            'image': 'Beautiful day in Portland!',
            'description': 'Find out the status of your UWICIIT Registration and if you have outstanding issues / holds',
            'link': '/registration/status'
        },
        {
            'title': "Add/ Drop Courses",
            'image': 'Beautiful day in Portland!',
            'description': 'Lookup a course that you may need to add or drop for this semester.',
            'link': '/courses/add'
        },
        {
            'title': "Find a Course",
            'image': 'Beautiful day in Portland!',
            'description': 'Find courses that are related to your field of study for your entire year of study',
            'link': '/courses/find'
        },
        {
            'title': "Schedule Details",
            'image': 'Beautiful day in Portland!',
            'description': 'Get on top of your study schedule with all of the dates you have classes and exams',
            'link': '/schedule'
        },
        {
            'title': "View/Request Transcripts",
            'image': 'Beautiful day in Portland!',
            'description': 'Ready to apply for another University Course or Job. Get your transcripts.',
            'link': '/transcripts/view'
        }
    ]

    global menu_type
    global username
    menu_type = 2
    username = session['username']

    # Record User Activity
    loguseractvity("View", "/academic-information")
    
    return render_template('academic-registration.html', title='Academic Information', menus = topOptions, user = username)

# Displays the students registration status
@app.route('/registration/status')
def registrationstatus():

    UserProfile = [
        {
            'Level':"Undergraduate",
            'Program':"Software Engineering BSC C",
            'AdmitTerm':"2016/2017 Semester I",
            'AdmitType':"Normal",
            'CatalogTerm':	"2016/2017 Semester I",
            'College':"Science & Technology",
            'Campus':"Cave Hill",
            'Major':"Software Eng (Mobile App Tech), UWICIIT",
        }
    ]

    # Record User Activity
    loguseractvity("View", "/registration/status")
    
    return render_template('registration-status.html', title='Registration Status', UserProfile = UserProfile)


@app.route('/schedule')
def schedule():

    CourseList = [
        {
            'title': "Elementary Chinese Culture and Language - SWEN 2013 - L01",
            'term': '2019/2020 Semester I',
            'CRN': '11753',
            'Status': '**Registered** on 17 Oct 2019',
            'Instructor': 'John L. Charlery , Justin Seale',
            'GradeMode': 'Standard Letter',
            'Credits': '3.000',
            'Level': 'Undergraduate',
            'Campus': 'Cave Hill',
        },
        {
            'title': "Software Project Management - SWEN 3130 - L01",
            'term': '2019/2020 Semester I',
            'CRN': '11733',
            'Status': '**Registered** on 17 Oct 2019',
            'Instructor': 'John L. Charlery , Justin Seale',
            'GradeMode': 'Standard Letter',
            'Credits': '3.000',
            'Level': 'Undergraduate',
            'Campus': 'Cave Hill',
        }
    ]

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

    # Record User Activity
    loguseractvity("View", "/schedule")
    
    return render_template('schedule.html', title='Schedule Details', QuickLinks = QuickLinks, courses = CourseList)

@app.route('/course/grade-detail')
def courseGradeDetail():
    return ""

@app.route('/courses/registered/<id>')
def coursesRegistered(id):
    
    global menu_type
    menu_type = 2

    return render_template('courses-registered.html', title='My Registered Courses', keyword = id)

@app.route('/courses/add/', methods=['GET', 'POST'])
def coursesAdd():

    global menu_type
    menu_type = 2

    form = CourseSelectTermForm()
    if form.validate_on_submit():
        flash('Term selection requested for user')

        # Record User Activity
        loguseractvity("Register", "/courses/add/")
        
        return redirect('/courses/add/lookup')
    return render_template('course-add.html', title='Add a Course / Select a Term', form=form)

@app.route('/courses/add/lookup', methods=['GET', 'POST'])
def coursesLookup():

    global menu_type
    menu_type = 2
    studentid = session['userid']

    term = "2019/2020"
    semester = 1
 
    course_list = list(db.course.find({ 'Term': term }))
    registered_list = list(db.registration.find({'studentID': studentid}))

    # Record User Activity
    loguseractvity("Lookup", "/courses/add/lookup")
    
    return render_template('course-lookup.html', studentID = studentid, title='Add a Course / Lookup a Course', course_list=course_list, registered_list = registered_list)

@app.route('/api/register/<studentid>/<courseid>')
def api_register_student(studentid, courseid):

    # Get current semester information    
    term = "2019/2020"
    semester = 1

    # Check if the user exist in the registration
    registrationStatus = db.registration.find_one({'studentID': studentid, 'courseID': courseid})

    # If so create else get their course information
    if registrationStatus:

        flash("You are already registered for this course")
        return redirect('/courses/add/lookup')

    else:

        # Get Course Name by courseID
        courseInformation = db.course.find_one({'CRN': courseid})

        now = datetime.now()
        timestamp = now.strftime("%m/%d/%Y, %H:%M:%S")

        registration_id = db.registration.insert_one({"studentID": studentid,"courseID": courseid,"courseName": courseInformation["Name"],"Term": term, "Semester": semester, "registered": timestamp})
    
    return redirect('/courses/add/lookup')

@app.route('/courses/detail/<course>')
def courseDetail(course):

    global menu_type
    global username
    menu_type = 2
    username = session['username']

    form = CourseSelectTermForm()

    courseInformation = db.course.find_one({'CRN': course})

    # Record User Activity
    loguseractvity("View", "/courses/detail/" + course)
    
    return render_template('course-detail.html', title='Course Details', courseInformation=courseInformation, form=form, user = username)

@app.route('/courses/find', methods=['GET', 'POST'])
def coursesFind():

    course_list = list(db.course.find({}))
    form = CourseFinderForm()

    QuickLinks = getUserQuickLinks()

    global menu_type
    global username
    menu_type = 2
    username = session['username']

    # Record User Activity
    loguseractvity("Find", "/courses/find")
    
    if request.method == 'POST':
        return redirect('/courses/find/' + form.data['name'])
        #return studentData

    return render_template('course-find.html', title='Course Finder', QuickLinks = QuickLinks, UserCourses = course_list, form = form, user = username)


@app.route('/courses/find/<searchkeyword>')
def coursesFindSearch(searchkeyword, methods=['POST']):
    
    global menu_type
    global username
    menu_type = 2
    username = session['username']
    
    studentData = db.course.find_one({"Name" : searchkeyword})
    
    # Record User Activity
    loguseractvity("Find", "/courses/find/" + searchkeyword)
    
    return render_template('course-search.html', title='Course Search', keyword = searchkeyword, user = username)


@app.route('/transcripts/view/<id>')
def transcriptsView(id):
    
    global menu_type
    global username
    menu_type = 2
    username = session['username']

    # Record User Activity
    loguseractvity("View", "/transcripts/view/" + ObjectId(id))
    
    data = db.student_transcript.find({"_id" : ObjectId(id)})
    
    return render_template('transcripts-view-details.html', title='View Transcripts', id=id, data = data, user = username)

@app.route('/transcripts/view')
def transcriptsViewAll():
    
    global menu_type
    global username
    menu_type = 2
    username = session['username']

    # Record User Activity
    loguseractvity("View All", "/transcripts/view")
    
    data = list(db.student_transcript.find({}))
    return render_template('transcripts-view.html', data = data,title='View Transcripts', num = 1, user = username)

@app.route('/transcripts/request', methods=['GET', 'POST'])
def transcriptsRequest():
    
    global menu_type
    global username
    menu_type = 2
    username = session['username']

    form = NewTranscriptForm()

    if request.method == 'POST':
        db.student_transcript.insert_one(form.data)

        # Record User Activity
        loguseractvity("Request", "/transcripts/request")
        
        return redirect('/transcripts/view')

    return render_template('transcripts-request.html', title='Request a Transcript', form=form, user = username)

@app.context_processor
def inject_user():
    global menu_type
    return dict(menu_type=menu_type)

@app.route('/termcourses')
def termcourses():

    global menu_type
    menu_type = 2

    return "Hello, World!"

@app.route('/studentrecords')
def studentrecords():
    return "Hello, World!"

@app.route('/gradedetail')
def gradedetail():
    return "Hello, World!"

@app.route('/transcript')
def transcript():
    return "Hello, World!"

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
