from app import app
from flask import jsonify
import json, os, signal
import requests
from flask import Flask, render_template, Markup, request, redirect, session, abort, url_for, flash
from functools import wraps
from app.forms import QueryForm, PersonalInfoForm
from flask_pymongo import MongoClient, PyMongo
from bson import ObjectId

from dotenv import load_dotenv
load_dotenv(verbose=True)
SECRET_KEY = os.getenv("SECRET_KEY")
# MONGO_URL = os.gr


# Setup Session to keep user logged in
app.config['SESSION_TYPE'] = 'memcached' 
app.config['SECRET_KEY'] = SECRET_KEY 
# app.config['MONGO_URI'] = MONGO_URL

menu_type = 1

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

@app.route('/')
def home():

    global menu_type
    menu_type = 1

    return render_template('index.html', title='Home')

@app.route('/personalInfo')
def personalInfo():

    global menu_type
    menu_type = 1
    
    return render_template('personalinfo.html', title='Personal Information')

@app.route('/stopServer', methods=['GET'])
def stopServer():
    os.kill(os.getpid(), signal.SIGINT)
    return jsonify({ "success": True, "message": "Server is shutting down..." })

@app.route('/index')
def index():
    user = {'username': 'Miguel'}
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
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route("/login", methods=['POST','GET'])
def login():

    tries = 0

    if request.method == "GET":
        return render_template('login.html', title='UWICIIT Login') 
    elif request.method == "POST":
        
        # Get the users credentials
        userID = request.form['userID']
        password = request.form['password']
    
        if userID == "" and password == "":
            tries = tries + 1
            return render_template("login.html", error = "Please enter valid credentials") 
            
            try:

                #user = verifyCredentials(userID,password)
                userID = userID
                displayName = "John Doe"
                token = "43543534534543534"
                
                sessionState = setSessionInformation(userID,displayName,token)
                #logAdminAction("LOGIN","LOGIN")
                if sessionState == "OK":
                    ses = "S" #Session(app)

            except requests.exceptions.HTTPError as e:
                error_json = e.args[1]
                error_json = json.loads(error_json)['error']
                return render_template("login.html",error = error_json["message"].replace('_', ' ') )
            
            except requests.exceptions.Timeout as e:
                return render_template("login.html",error = "A Timeout Error Occurred" )
            
            except requests.exceptions.ConnectionError as e:
                return render_template("login.html",error = "A Connection Error Occurred" )
            
    return redirect(url_for('home'))

def setSessionInformation(userID,name,token):

    session['userID'] = userID
    session['name'] = name
    session['token'] = token
    session['logged_in'] = True

    return 'OK'

@app.route("/logout")
@login_required
def logout():

    session['logged_in'] = False
    session.clear()
    return home()


@app.route('/forgotPassword')
def forgotPassword():
    return render_template('login.html', title='UWICIIT Forgot Password') 

# Registration Functions Section
@app.route('/registration')
def registration(): 

    topOptions = [
        {
            'title': "Registration Status",
            'image': 'Beautiful day in Portland!',
            'link': '/registration-status'
        },
        {
            'title': "Add/ Drop Courses",
            'image': 'Beautiful day in Portland!',
            'link': '/add-course'
        },
        {
            'title': "Find a Course",
            'image': 'Beautiful day in Portland!',
            'link': '/find-course'
        },
        {
            'title': "Schedule Details",
            'image': 'Beautiful day in Portland!',
            'link': '/schedule'
        }
    ]

    return render_template('registration.html', title='Course Registration', menus = topOptions)

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

    return render_template('schedule.html', title='Schedule Details', QuickLinks = QuickLinks, courses = CourseList)

@app.route('/course/grade-detail')
def courseGradeDetail():
    return ""

@app.route('/courses/find')
def coursesFind():

    UserCourses = [
        {
            'Name': "An Intro to Computing I",
            'Code': "1000",
        },
        {
            'Name': "Computing in Society",
            'Code': "1002",
        },{
            'Name': "Maths for Software Engineers",
            'Code': "1004",
        },{
            'Name': "Research Methods for Software",
            'Code': "1006",
        },{
            'Name': "Technical Writing",
            'Code': "1008",
        },{
            'Name': "An Intro to Computing II",
            'Code': "1009",
        },{
            'Name': "Intro Software Engineering",
            'Code': "2001",
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

    global menu_type
    menu_type = 2

    return render_template('find-a-course.html', title='Course Finder', QuickLinks = QuickLinks, UserCourses = UserCourses)

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

@app.route('/events')
def events():

    global menu_type
    menu_type = 3

    return render_template('events.html', title='Events')

@app.route('/querypage')
def query():
    form = QueryForm()
    return render_template('querypage.html', title='Student Query', form=form)

@app.route('/query-list')
def queryhistory():
    return render_template('query-list.html', title='Query History')

@app.route('/personalinfopage')
def personalinfopage():
    form = PersonalInfoForm()
    return render_template('personalinfopage.html', title='Personal Info', form=form)