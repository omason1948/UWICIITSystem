from app import app
from flask import jsonify
import json, os, signal
import requests
from flask import Flask, render_template, Markup, request, redirect, session, abort, url_for, flash, escape
from datetime import datetime

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from datetime import date

# generate random integer values
from random import randint

from functools import wraps

# Flask Mongo
from flask_pymongo import PyMongo, MongoClient, BSONObjectIdConverter

# Forms
from wtforms import Form, validators

# Form Classes
from app.forms import CourseSelectTermForm, NewTranscriptForm, CourseFinderForm, SearchForm, SearchFormStudents, SearchFormEvents, SearchFormQueries, SearchFormTranscripts, SearchFormInsurance, AddCourseGradeForm
from app.forms import QueryForm, PersonalInfoForm, InsuranceForm, ForgotForm
from app.forms import EventForm, LoginForm, ResetPasswordForm

from bson import Binary, Code, ObjectId
from bson.json_util import dumps

#For key generation
import binascii

#Mail
#from flask_mail import Mail, Message 
#import smptlib
#from email.mime.multipart import MIMEMultipart
#from email.mime.text import MIMEText

#easy_install Flask-Session or pip install Flask-Session
from flask import Flask, session

#include pprint for readabillity of the 
from pprint import pprint

from dotenv import load_dotenv
load_dotenv(verbose=True)

# Keys
SECRET_KEY = os.getenv("SECRET_KEY")
MONGO_URL = os.getenv("MONGO_URL")

# Mail Server Configuration
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'theuwiciit@gmail.com'
app.config['MAIL_PASSWORD'] = 'dehgyd-wuXkas-4mezty'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

#mail = Mail(app)

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
userType = 0 # Null User
username = ""

# Role Options
role_users = ""
role_events = ""
role_queries = ""
roles_grades = ""

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

# Wrapper function to prevent users from requesting unauthorized pages
def admin_login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_logged_in' in session:
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

from bson.son import SON

def getUserQuickLinks():
    
    userid = session['userid']

    collection = db.systemlog.find().limit(5)

    pipeline = [
        {"$unwind": "$tags"},
        {"$group": {"user": "$tags", "count": {"$sum": 1}}},
        {"$sort": SON([("count", -1), ("_id", -1)])}
    ]

    #collection = list(db.systemlog.aggregate(pipeline))

    return collection

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

                # Define if user is an admin or student
                global userType
                userType = UserLoggedIn['userType']
                if( userType == "2"):
                    
                    userRoles = UserLoggedIn['roles']
                    session['admin_logged_in'] = True
                    setUserRoles(userRoles)

                # Setup Session
                sessionState = setSessionInformation(form.username.data, UserLoggedIn['name'], UserLoggedIn['email'], userType)

                # Record User Activity
                loguseractvity("Login Success", "/login")
                
                if sessionState == "OK":
                    ses = "S" 

                if userType == "1":
                    return redirect('/index')
                else:
                    return redirect('/admin')

            else:
                flash('Invalid User Credentials entered. Try Again')
        else:
            flash('Invalid User Credentials entered. Try Again')

    return render_template('login.html', title='Sign In', form=form)

@app.route("/forgot", methods=['GET', 'POST'])
def forgotPassword():

    # Record User Activity
    #loguseractvity("View", "/forgotPassword")
    
    form = ForgotForm()
    if form.validate_on_submit():
        useremail = form.email.data
        userid = form.userid.data

        check_for_user = db.user.find_one({'UserID': userid, 'email': useremail})
        if check_for_user:
            sendEmail(useremail, userid)

            flash('We sent an email to your inbox.')
            return render_template('forgot_success.html', title='UWICIIT Forgot Password', form=form)
        else:
            flash('An error occured trying to reset your password. Try again later.')

    # Send user an email regarding the forgotten email

    return render_template('forgot.html', title='UWICIIT Forgot Password', form=form)

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

@app.route("/sendEmail/")
def sendEmail(useremail, userid):
    
    key = binascii.hexlify(os.urandom(24))
    link = "http://uwiciitonline.azurewebsites.net/reset-password/" + key

    mail_content = "Good Day Student, \n There has been a password request on your account, please ignore this email if you have not made this request. If this was you, please click on the link below to reset your password. \n " + link

    #The mail addresses and password
    sender_address = 'theuwiciit@gmail.com'
    sender_pass = 'dehgyd-wuXkas-4mezty'
    receiver_address = useremail
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'UWICIIT Password Reset'   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    
    db.password_resets.insert_one({"useremail": useremail,"key": key,"userid": userid})
    
    return render_template('forgot_email.html', title='UWICIIT Forgot Password Step 1')

@app.route("/reset-password/<key>", methods=['GET', 'POST'])
def resetPassword(key):

    key_available = db.password_resets.find_one({'key': key})
    if key_available:

        form = ResetPasswordForm()
        user_information = db.user.find_one({'UserID': key_available["userid"], 'email': key_available["useremail"]})
        
        if request.method == 'POST':
            password = form.data['password']
            confirmpassword = form.data['confirmpassword']

            db.user.update_one({"UserID": key_available["userid"]},{"$set":{"password": password }})
            flash('Term selection requested for user')
            return redirect('/login')
        
        return render_template('forgot_set_password.html', title='UWICIIT Forgot Password Step 2', form=form)
    else:
        return redirect('/forgot')

def setUserRoles(userRoles):

    global role_users
    global role_events
    global role_queries
    global roles_grades

    role_users = userRoles["Users"]
    role_events = userRoles["Events"]
    role_queries = userRoles["Queries"]
    roles_grades = userRoles["Grades"]
    
    return "OK"

def setSessionInformation(userID, name, email, userType):

    session['username'] = name
    session['userid'] = userID
    session['email'] = email
    session['logged_in'] = True
    session['userType'] = userType

    if userType == 2:
        session['admin_logged_in'] = True

    return 'OK'

@app.route("/logout")
@login_required
def logout():

    session['logged_in'] = False
    session.clear()
    return home()


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
        },
        {
            'title': "Grades",
            'image': 'Beautiful day in Portland!',
            'description': 'View a list of your grades for the entire year broken down into exams and course work',
            'link': '/grades/view'
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
@login_required
def registrationstatus():
    
    QuickLinks = getUserQuickLinks()

    userid = session['userid']
    userProfile = db.user.find_one({'UserID': userid})
    #return userProfile['userType']

    UserProfile = [
        {
            'Level': userProfile['program'][0]['level'],
            'Program': userProfile['program'][0]['program'],
            'AdmitTerm': userProfile['program'][0]['term'],
            'AdmitType': userProfile['program'][0]['type'],
            'College': userProfile['program'][0]['college'],
            'Campus': userProfile['program'][0]['campus'],
            'Major': userProfile['program'][0]['major'],
        }
    ]

    hold_status = userProfile['hold_status']
    hold_status_message = ""
    
    if hold_status == "1":
        system_text = db.system_text.find_one({'title': "hold_status_no"})
        hold_status_message = system_text['message']
    else:
        system_text = db.system_text.find_one({'title': "hold_status_yes"})
        hold_status_message = system_text['message']

    academic_standing = userProfile['academic_status']
    academic_standing_message = ""

    if academic_standing == "1":
        system_text = db.system_text.find_one({'title': "academic_standing_good"})
        academic_standing_message = system_text['message']
    else:
        system_text = db.system_text.find_one({'title': "academic_standing_bad"})
        academic_standing_message = system_text['message']

    registration_status = userProfile['registration_status']
    registration_status_message = ""

    if registration_status == "1":
        system_text = db.system_text.find_one({'title': "registration_allowed"})
        registration_status_message = system_text['message']
    else:
        system_text = db.system_text.find_one({'title': "registration_not_allowed"})
        registration_status_message = system_text['message']


    # Record User Activity
    loguseractvity("View", "/registration/status") 
    
    return render_template('registration-status.html', QuickLinks = QuickLinks, title='Registration Status', UserProfile = UserProfile, hold_status_message = hold_status_message, academic_standing_message = academic_standing_message, registration_status_message = registration_status_message)


@app.route('/schedule')
@login_required
def schedule():

    global menu_type
    global username
    menu_type = 2
    username = session['username']
    studentid = session['userid']

    studentid = str(session['userid'])
     
    
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

    registered_list = db.course.find({'Year': "1"})
    
    Monday = ""    
    Monday2 = {"9:00":'',"10:00":"", "11:00":"", "12:00":"", "1:00":"", "2:00":"", "3:00":"", "4:00":"", "5:00":"", "6:00":""}

    Tuesday = ""
    Tuesday2 = {"9:00":'',"10:00":"", "11:00":"", "12:00":"", "1:00":"", "2:00":"", "3:00":"", "4:00":"", "5:00":"", "6:00":""}

    Wednesday = ""
    Wednesday2 = {"9:00":'',"10:00":"", "11:00":"", "12:00":"", "1:00":"", "2:00":"", "3:00":"", "4:00":"", "5:00":"", "6:00":""}

    Thursday = ""
    Thursday2 = {"9:00":'',"10:00":"", "11:00":"", "12:00":"", "1:00":"", "2:00":"", "3:00":"", "4:00":"", "5:00":"", "6:00":""}

    Friday = ""
    Friday2 = {"9:00":'',"10:00":"", "11:00":"", "12:00":"", "1:00":"", "2:00":"", "3:00":"", "4:00":"", "5:00":"", "6:00":""}

    for i in registered_list:

        if ( i['CourseActivity']["L1"]["times"][1]!= "0" ):
            Monday += i['Name'] + " - L1" + i['CourseActivity']["L1"]["times"][1]
            Monday2[ i['CourseActivity']["L1"]["times"][1] ] += i['Name'] + " L1"
        
        if ( i['CourseActivity']["P1"]["times"][1]!= "0" ):
            Monday += i['Name'] + " P1" + i['CourseActivity']["P1"]["times"][1]
            Monday2[ i['CourseActivity']["P1"]["times"][1] ] += i['Name'] + " P1"
        
        if ( i['CourseActivity']["L1"]["times"][2]!= "0" ):
            Tuesday += i['Name'] + " L1" + i['CourseActivity']["L1"]["times"][2]
            Tuesday2[ i['CourseActivity']["L1"]["times"][2] ] += i['Name'] + " L1"

        if ( i['CourseActivity']["P1"]["times"][2]!= "0" ):
            Tuesday += i['Name'] + " P1" + i['CourseActivity']["P1"]["times"][2]
            Tuesday2[ i['CourseActivity']["P1"]["times"][2] ] += i['Name'] + " P1"
        
        if ( i['CourseActivity']["L1"]["times"][3]!= "0" ):
            Wednesday += i['Name']+ " L1" + i['CourseActivity']["L1"]["times"][3]
            Wednesday2[ i['CourseActivity']["P1"]["times"][3] ] += i['Name'] + " P1"
        
        if ( i['CourseActivity']["P1"]["times"][3]!= "0" ):
            Wednesday += i['Name'] + " P1" + i['CourseActivity']["P1"]["times"][3]
            Wednesday2[ i['CourseActivity']["P1"]["times"][3] ] += i['Name'] + " P1"
        
        if ( i['CourseActivity']["L1"]["times"][4]!= "0" ):
            Thursday += i['Name'] + " L1" + i['CourseActivity']["L1"]["times"][4]
            Thursday2[ i['CourseActivity']["L1"]["times"][4] ] += i['Name'] + " L1"

        if ( i['CourseActivity']["P1"]["times"][4]!= "0" ):
            Thursday += i['Name'] + " P1" + i['CourseActivity']["P1"]["times"][4]
            Thursday2[ i['CourseActivity']["P1"]["times"][4] ] += i['Name'] + " P1"
        
        if ( i['CourseActivity']["L1"]["times"][5]!= "0" ):
            Friday += i['Name'] + " L1" + i['CourseActivity']["P1"]["times"][5]
            Friday2[ i['CourseActivity']["L1"]["times"][5] ] += i['Name'] + " L1"

        if ( i['CourseActivity']["P1"]["times"][5]!= "0" ):
            Friday += i['Name'] + " P1" + i['CourseActivity']["P1"]["times"][5]
            Friday2[ i['CourseActivity']["P1"]["times"][5] ] += i['Name'] + " P1"

    today = date.today()
    # Textual month, day and year	
    d2 = today.strftime("%B %d, %Y")
    Day_of_week = today.strftime("%A")
    Hour_of_day = today.strftime("%H")

    return render_template('schedule.html', user = username, current_date = d2, current_day = Day_of_week, current_hour = Hour_of_day, title='Schedule Details', QuickLinks = QuickLinks, Monday = Monday2, Tuesday = Tuesday2, Wednesday = Wednesday2, Thursday = Thursday2, Friday = Friday2, courses = registered_list)

@app.route('/course/grade-detail')
@login_required
def courseGradeDetail():
    return ""

@app.route('/courses/registered/<id>')
@login_required
def coursesRegistered(id):
    
    global menu_type
    menu_type = 2

    return render_template('courses-registered.html', title='My Registered Courses', keyword = id)

@app.route('/courses/add/', methods=['GET', 'POST'])
@login_required
def coursesAdd():

    global menu_type
    menu_type = 2

    form = CourseSelectTermForm()
    if form.validate_on_submit():

        # Record User Activity
        loguseractvity("Register", "/courses/add/")

        if request.method == 'POST':
            term = form.data['terms']
            year = form.data['years']

            return coursesLookup(term, year)
        
    return render_template('course-add.html', title='Add a Course / Select a Term', form=form)

@app.route('/courses/add/lookup', methods=['GET', 'POST'])
@login_required
def coursesLookup(term, year):

    global menu_type
    menu_type = 2
    studentid = session['userid']

    semester = 1

    course_list = list(db.course.find({'Year':year, 'Term': term}))
    registered_list = list(db.registration.find({'studentID': studentid}))

    # Record User Activity
    loguseractvity("Lookup", "/courses/add/lookup")
    
    return render_template('course-lookup.html', term = term, year = year, studentID = studentid, title='Add a Course / Lookup a Course', course_list=course_list, registered_list = registered_list)

@app.route('/api/register/<studentid>/<courseid>/<term>/<year>')
@login_required 
def api_register_student(studentid, courseid, term, year):

    # Check if the user exist in the registration
    registrationStatus = db.registration.find_one({'studentID': studentid, 'courseID': courseid})

    # If so create else get their course information
    if registrationStatus:

        flash("You are already registered for this course")
        return coursesLookup(term, year)

    else:

        # Get Course Name by courseID
        courseInformation = db.course.find_one({'CRN': courseid})

        now = datetime.now()
        timestamp = now.strftime("%m/%d/%Y, %H:%M:%S")

        registration_id = db.registration.insert_one({"studentID": studentid,"courseID": courseid,"courseName": courseInformation["Name"], "Term": term, "Semester": year, "registered": timestamp})
    
    return redirect('/courses/add/lookup')

@app.route('/courses/detail/<course>')
@login_required
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
@login_required
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
@login_required
def coursesFindSearch(searchkeyword, methods=['POST']):
    
    QuickLinks = getUserQuickLinks()
    global menu_type
    global username
    menu_type = 2
    username = session['username']
    
    studentData = db.course.find({"Name":{"$regex": searchkeyword}})
    
    # Record User Activity
    loguseractvity("Find", "/courses/find/" + searchkeyword)

    #print(studentData)
    #return studentData
    
    return render_template('course-search.html', title='Course Search', studentData = studentData, keyword = searchkeyword, QuickLinks = QuickLinks, user = username)


@app.route('/transcripts/view/<id>')
@login_required
def transcriptsView(id):
    
    global menu_type
    global username
    menu_type = 2
    username = session['username']

    # Record User Activity
    loguseractvity("View", "/transcripts/view/" + str(id))
    
    data = db.student_transcript.find({"_id" : ObjectId(id)})
    
    return render_template('transcripts-view-details.html', title='View Transcripts', id=id, data = data, user = username)

@app.route('/transcripts/view')
@login_required
def transcriptsViewAll():
    
    global menu_type
    global username
    menu_type = 2
    username = session['username']
    userId = session['userid']

    # Record User Activity
    loguseractvity("View All", "/transcripts/view")
    
    data = list(db.student_transcript.find({"studentId" : str(userId) }))
    return render_template('transcripts-view.html', data = data,title='View Transcripts', num = 1, user = username)

@app.route('/transcripts/request', methods=['GET', 'POST'])
@login_required
def transcriptsRequest():
    
    global menu_type
    global username
    menu_type = 2
    username = session['username']
    userId = int(session['userid'])

    form = NewTranscriptForm()

    if request.method == 'POST':

        db.student_transcript.insert_one(form.data)

        # Record User Activity
        loguseractvity("Request", "/transcripts/request")
        
        return redirect('/transcripts/view')

    return render_template('transcripts-request.html', title= userId, form=form, userId= userId, user = username)

@app.context_processor
def inject_user():
    global menu_type
    return dict(menu_type=menu_type)

@app.route('/termcourses')
@login_required
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
@login_required
def query():
    QuickLinks = getUserQuickLinks()
    global menu_type
    global username
    menu_type = 1
    username = session['username']

    form = QueryForm()
    userId = int(session['userid'])
    email = session['email']
    data = db.query.find({"studentId" : userId})

    # Record User Activity
    loguseractvity("View", "/querypage/")
    
    if request.method=='POST':
        db.query.insert_one({"studentId": userId, "studentName" : username, "studentEmail": email, "yearOfStudy": form.data['yearOfStudy'], "semester": form.data['semester'], "studentIssues": form.data['studentIssues'], "queryDesc": form.data['queryDesc']}  )
        return redirect('/queryhistory')
    return render_template('querypage.html', title='Student Query', QuickLinks = QuickLinks, form=form, userId=userId, data=data, user=username, email=email)

@app.route('/queryhistory')
@login_required
def queryhistory():
    
    QuickLinks = getUserQuickLinks()
    global menu_type
    global username
    menu_type = 1
    username = session['username']
    email = session['email']

    userId = int(session['userid'])
    data = list(db.query.find({"studentId" : userId}))
    return render_template('queryhistory.html', title='Query History', data=data, user=username, userId=userId, QuickLinks = QuickLinks)

@app.route('/personalInfo', methods=('GET', 'POST'))
@login_required
def personalinfoOptions():

    QuickLinks = getUserQuickLinks()
    global menu_type
    global username
    menu_type = 1
    username = session['username']

    # Record User Activity
    loguseractvity("View", "/personalInfo/")
    
    return render_template('personalinfo.html', title='Personal Info', user=username)

@app.route('/personalInfo/view')
@login_required
def viewpersonalInfo():

    QuickLinks = getUserQuickLinks()
    global menu_type
    global username
    menu_type = 1
    username = session['username']
    
    userId = int(session['userid'])
    data = list(db.student.find({"studentId" : userId}))
    return render_template('personalinfo-view.html', QuickLinks = QuickLinks, title='View Personal Info', data=data, user=username, userId=userId)

@app.route('/personalInfo/update', methods=('GET', 'POST'))
@login_required
def personalinfopage():

    QuickLinks = getUserQuickLinks()
    global menu_type
    global username
    menu_type = 1
    username = session['username']
    filename = ''
    filename2 = ''

    form = PersonalInfoForm()
    userId = int(session['userid'])
    studentData = db.student.find_one({'studentId': userId})

    if request.method == 'POST':
        file = request.files['studentPhoto']
        passportfile = request.files['passport']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(os.path.abspath('app/static/userphotos'
                                ))
            file.save(os.path.join(path, secure_filename(filename)))

        if passportfile and allowed_file(passportfile.filename):
            filename2 = secure_filename(passportfile.filename)
            path = os.path.join(os.path.abspath('app/static/userphotos'
                                ))
            passportfile.save(os.path.join(path,
                              secure_filename(filename2)))

        # Update the student based on their logged in ID

        db.student.update_one({'studentId': userId}, {'$set': {
            'maritalStatus': form.data['maritalStatus'],
	    'studentAddress': form.data['studentAddress'],
	    'studentAddress': form.data['studentAddress'],
	    'country': form.data['country'],
            'mobilenum': form.data['mobilenum'],
            'emergencyCon': form.data['emergencyCon'],
            'relationship': form.data['relationship'],
            'ecNumber': form.data['ecNumber'],
            'studentPhoto': filename,
            'passport': filename2,
            }})

        # Record User Activity

        loguseractvity('Edit', '/personalInfo/update/' + str(userId))
        return redirect('/personalInfo/view')
    else:

        # Pull the users current information from the database

        studentData = db.user.find_one({'studentId': userId})

        # return redirect('/personalInfo/view')

    return render_template(
        'personalinfopage.html',
        title='Update Info',
        form=form,
        userId=userId,
        user=username,
        studentData=studentData,
        QuickLinks=QuickLinks
        )

@app.route('/personalInfo/insurance',  methods=('GET', 'POST'))
@login_required
def insurance():
    
    global menu_type
    global username
    menu_type = 1
    username = session['username']
    email = session['email']
    filename = ""
    QuickLinks = getUserQuickLinks()
	
    form = InsuranceForm()
    userId = int(session['userid'])
    insurancedata = db.insurance.find_one({'studentId' : userId})
    
    # Record User Activity
    loguseractvity('Update', '/personalInfo/insurance')
    
    if request.method=='POST':
        
        file = request.files["payment"]
        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)
            path = os.path.join(os.path.abspath('app/static/userphotos'))
            file.save(os.path.join(path, secure_filename(filename)))

        db.insurance.insert_one({"studentId": userId, "insurancePeriod": form.data['insurancePeriod'], "payment": filename})
        return redirect("/personalInfo/view")

    return render_template('insurance.html', title='Insurance', QuickLinks=QuickLinks, form=form, userId=userId, insurancedata=insurancedata, user=username, email=email)


import cgi, os
import cgitb; cgitb.enable()

@app.route('/upload')
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_filer():
   if request.method == 'POST':
      f = request.files['file']
      #f.save(secure_filename(f.filename)) #working but saves to root
      path = os.path.join(os.path.abspath('app/userphotos'))
      f.save(os.path.join(path, secure_filename(f.filename)))
      
      return 'file uploaded successfully'

############################################################
##################### Events ROUTING  ######################
############################################################

@app.route('/events', methods = ['GET', 'POST']) 
@login_required
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
@login_required
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
            
            path = os.path.join(os.path.abspath('app/static/userphotos'))
            file.save(os.path.join(path, secure_filename(filename)))

            #file.save(os.path.join(app.config['UPLOAD_FOLDER'] + "/" + directory , filename))

        events_id = db.events.insert_one({"name": form.data["name"],"eventDate":form.data["eventDate"], "description":form.data["description"],"location":form.data["location"],"photo": filename})

        # Record User Activity
        loguseractvity("Add", "/events/add")

        return redirect(url_for('eventsview'))

    return render_template('event-add.html', title='Add Events', form = form, user = username)

@app.route('/events/edit/<id>', methods = ['GET', 'POST'])
@login_required
def eventsedit(id):
    form = EventForm()
    
    global menu_type
    global username
    menu_type = 3
    username = session['username']

    data = db.events.find({"_id" : ObjectId(id)})

    if request.method =='POST':
        file = request.files['photo']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(os.path.abspath('app/static/userphotos'
                                ))
            file.save(os.path.join(path, secure_filename(filename)))

        db.events.update_one({"_id": ObjectId(id)},{"$set":{"name": form.data["name"],"eventDate":form.data["eventDate"],"description":form.data["description"], "location":form.data["location"], "photo":filename}})
        return redirect(url_for('eventsview'))
    
    # Record User Activity
    loguseractvity("Edit", "/events/edit/" + str(id))

    return render_template('event-edit.html', title='Edit Events', data = data, form = form, user = username)

@app.route('/events/delete/<id>')
@login_required
def eventsdelete(id):

    global menu_type
    global username
    menu_type = 3
    username = session['username']

    db.events.remove({"_id": ObjectId(id)})

    # Record User Activity
    loguseractvity("Delete", "/events/delete/" + str(ObjectId(id)))

    return render_template('event-delete.html', title='Delete Events', user = username)

@app.route('/events/register/<id>')
@login_required
def eventsregister(id):
   
    global menu_type
    global username
    menu_type = 3
    username = session['username']
    userid= session["userid"]
    
    check = db.event_student.find({"eventid": ObjectId(id),"studentid":userid}).count()
    
    if  check == 0:
        events_id = db.event_student.insert_one({"eventid": ObjectId(id),"studentid":userid})

    event_for_student = db.event_student.aggregate([
        {
            '$match': {
                'studentid': userid
            }
        }, {
            '$lookup': {
                'from': 'events', 
                'localField': 'eventid', 
                'foreignField': '_id', 
                'as': 'info'
            }
        }, {
            '$unwind': {
                'path': '$info'
            }
        }
    ])
    
    # Record User Activity
    loguseractvity("Register", "/events/register/" + str(ObjectId(id)))

    return render_template('event-list.html', title='Event Register', event_for_student = event_for_student, user = username)

@app.route('/events/register/view')
@login_required
def eventsregisterview():
   
    global menu_type
    global username
    menu_type = 3
    username = session['username']
    userid= session["userid"]
    

    event_for_student = db.event_student.aggregate([
        {
            '$match': {
                'studentid': userid
            }
        }, {
            '$limit': 2
        }, {
            '$lookup': {
                'from': 'events', 
                'localField': 'eventid', 
                'foreignField': '_id', 
                'as': 'info'
            }
        }, {
            '$unwind': {
                'path': '$info'
            }
        }
    ])
    
    # Record User Activity
    loguseractvity("View", "/events/register/")

    return render_template('event-list.html', title='Event Register', event_for_student = event_for_student, user = username)

@app.route('/events/deregister/<id>')
@login_required
def eventsderegister(id):
   
    global menu_type
    global username
    menu_type = 3
    username = session['username']
    events_id = db.event_student.remove({"_id": ObjectId(id)})
    

    # Record User Activity
    loguseractvity("Deregister", "/events/deregister/" + str(ObjectId(id)))

    return render_template('event-deregister.html', title = 'Event Deregister', user= username)



# Displays the students grades information
@app.route('/grades/view')
@login_required
def student_grades():

    global menu_type
    global username
    menu_type = 2
    username = session['username']
    userID = session['userid']

    student_registered_courses = db.registration.find({"studentID" : userID})
    courseList = {}

    #for course in student_registered_courses:
    #    courseList = datetime.strptime(course["registered"], '%m/%d/%y %H:%M:%S')

    # Record User Activity
    loguseractvity("View", "/grades/view/")

    #return courseList
    return render_template('grade.html', title='View Grades', user = username, registered_courses = student_registered_courses)

# Displays the students grades information
@app.route('/grade/view/<id>')
@login_required
def student_course_grade(id):

    global menu_type
    global username
    menu_type = 2
    username = session['username']
    userID = session['userid']

    course_information = db.course.find({"CRN" : id})
    student_course_grade = db.student_course_grade.find({"StudentID" : userID, "CourseID": id})

    # Record User Activity
    loguseractvity("View", "/grades/view/" + str(id))

    return render_template('grade-view.html', title='View Grades', course_information = course_information, user = username, course_grade = student_course_grade)


# Admin Section

@app.route('/admin')
@login_required
def admin_dashboard():

    global menu_type
    global username
    menu_type = 3
    username = session['username']

    # Record User Activity
    loguseractvity("View", "/admin")

    collection = list(db.systemlog.find( sort=[( 'timestamp', -1 )] ).limit(6))
    queries = list(db.query.find().limit(4))

    transcripts_data = db.student_transcript.find({})
    events_data = db.events.find({})
    query_data = db.query.find({})

    transcripts_count = transcripts_data.count()
    events_count = events_data.count()
    queries_count = query_data.count()

    return render_template('admin_index.html', title = 'Admin Dashboard', queries_count = queries_count, events_count = events_count, transcripts_count = transcripts_count, user = username, queries = queries, userLogs = collection)


@app.route('/admin/students', methods = ['GET', 'POST'])
@admin_login_required
def admin_students():

    global username
    username = session['username']

    form = SearchFormStudents()
	
    searched_name = ''
    search_count = ''

    # Record User Activity

    loguseractvity('View', '/admin/students')

    if form.validate_on_submit():

        searched_name = form.data['name']
        collection = db.user.find({'name': {'$regex': searched_name},
                                  'userType': '1'})
        search_count = collection.count()
    else:

# ....collection = db.user.find({'userType': "1"})

        collection = db.user.find({'userType': "1"})
        search_count = collection.count()

    return render_template(
        'admin_students.html',
        title='Admin Student',
        search_count=search_count,
        searchName=searched_name,
        form=form,
        user=username,
        collection=collection,
        )

@app.route('/admin/student/<studentid>', methods = ['GET', 'POST'])
@admin_login_required
def admin_students_view(studentid):

    student_data = db.user.find_one({"_id" : ObjectId(studentid)})
    #return userProfile['userType']

    UserProfile = [
        {
            'Level': student_data['program'][0]['level'],
            'Program': student_data['program'][0]['program'],
            'AdmitTerm': student_data['program'][0]['term'],
            'AdmitType': student_data['program'][0]['type'],
            'College': student_data['program'][0]['college'],
            'Campus': student_data['program'][0]['campus'],
            'Major': student_data['program'][0]['major'],
        }
    ]
    
    registered_courses = db.registration.find({"studentID":student_data["UserID"]}) 
    personal_info = db.student.find_one({"studentId": int(student_data["UserID"]) })
    
    return render_template('admin_student_view.html', title = 'Admin Student Information', student_data = student_data, UserProfile = UserProfile, registered_courses = registered_courses, user = username, personal_info=personal_info)

@app.route('/admin/events', methods = ['GET', 'POST'])
@admin_login_required
def admin_events():

    global username
    username = session['username']

    form = SearchFormEvents()
    searched_name = ""
    search_count = ""

    # Record User Activity
    loguseractvity("View", "/admin/events")

    if form.validate_on_submit():

        searched_name = form.data["name"]
        collection = db.events.find({"name":{"$regex": searched_name}})
        search_count = collection.count()

    else:

        collection = db.events.find()
        search_count = collection.count()

    return render_template('admin_events.html', search_count = search_count, searchName = searched_name, title = 'Events', form = form, user = username, collection = collection)

@app.route('/admin/courses', methods = ['GET', 'POST'])
@admin_login_required
def admin_courses():

    global username
    username = session['username']
    form = SearchForm()
    searched_name_course_name = ""
    search_count = ""

    # Record User Activity
    loguseractvity("View", "/admin/courses")

    if form.validate_on_submit():
        searched_name_course_name = form.data["course_name"]
        semester = form.data["semester"]

        if semester == "":
            collection = list(db.course.find({"Name":{"$regex": searched_name_course_name}}))

        else:
            collection = list(db.course.find({"Name":{"$regex": searched_name_course_name},"Term": semester}))

    else:
        collection = db.course.find()
        search_count = collection.count()

    return render_template('admin_course.html', title = 'Courses', form = form, search_count = search_count, searchName = searched_name_course_name, user = username, collection = collection)

@app.route('/admin/course/<crn>', methods = ['GET', 'POST'])
@admin_login_required
def admin_course_detail(crn):
    
    global username
    username = session['username']
    
    form = SearchForm()
    searched_name_course_name = ""
    search_count = ""

    # Record User Activity
    loguseractvity("View", "/admin/course/" + str(crn))

    courseInformation = db.course.find_one({'CRN': crn})
    return render_template('admin_course_view.html', title = 'Course Details', courseInformation = courseInformation, user = username)

@app.route('/admin/reports', methods = ['GET', 'POST'])
@admin_login_required
def admin_reports():

    # Record User Activity
    loguseractvity("View", "/admin/reports/")

    return "reports"

@app.route('/admin/settings')
@admin_login_required
def admin_settings():

    global username
    username = session['username']

    # Record User Activity
    loguseractvity("View", "/admin/settings/")


    return "settings"

@app.route('/admin/grades', methods = ['GET', 'POST'])
@admin_login_required
def admin_grades():

    global username
    username = session['username']

    # Record User Activity
    loguseractvity("View", "/admin/grades/")

    collection = db.course.find()

    return render_template('admin_grades.html', title = 'Course Grade Details', collection = collection)


@app.route('/admin/grades/<courseid>', methods = ['GET'])
@admin_login_required
def admin_grades_course(courseid):

    global username
    username = session['username']

    # Record User Activity
    loguseractvity("View", "/admin/grades/" + courseid)
    collection = db.registration.find({'courseID': courseid})
    adminType = session['userType']
    
    student_registered = db.registration.aggregate([
    {
        '$match': {
            'courseID': courseid
        }
    }, {
        '$lookup': {
            'from': 'user', 
            'localField': 'studentID', 
            'foreignField': 'UserID', 
            'as': 'info'
        }
    }, {
        '$unwind': {
            'path': '$info'
        }
    }
])

    """student_registered = db.registration.aggregate([
        {
            '$match': {
                'courseID': courseid
            }
        }, {
            '$lookup': {
                'from': 'user', 
                'localField': 'studentID', 
                'foreignField': 'UserID', 
                'as': 'info'
            }
        }, {
            '$unwind': {
                'path': '$info'
            }
        }, {
            '$lookup': {
                'from': 'student_course_grade', 
                'localField': 'StudentID', 
                'foreignField': 'UserID', 
                'as': 'graded'
            }
        }, {
            '$unwind': {
                'path': '$graded'
            }
        }
    ])"""

    """ event_for_student = db.event_student.aggregate([
        {
            '$match': {
                'studentid': '123456'
            }
        }, {
            '$limit': 2
        }, {
            '$lookup': {
                'from': 'events', 
                'localField': 'eventid', 
                'foreignField': '_id', 
                'as': 'info'
            }
        }, {
            '$unwind': {
                'path': '$info'
            }
        }
    ]) """

    return render_template('admin_grades_course.html', title = 'Course Grade Details', collection = collection, student_registered= student_registered, user = username, courseid = courseid, adminType = adminType)

@app.route('/admin/grades/<courseid>/<studentid>', methods = ['GET', 'POST'])
@admin_login_required
def admin_grades_course_update(courseid, studentid):

    # Record User Activity
    loguseractvity("View", "/admin/grades/" + courseid + "/" + studentid)
    form = AddCourseGradeForm()
    username = session['username']
    collection = db.student_course_grade.find()

    if request.method == 'POST':

        db.student_course_grade.insert_one({"StudentID": studentid, "CourseID": courseid, "CourseGrades": {"course": form.data["course"], "exam": form.data["exam"]}, "ApprovalStatus": 0, "TermType": form.data["term"],"Admin": username })
        flash("Grade updated for " + studentid)
        return redirect("/admin/grades/" + courseid + "/" + studentid)

    return render_template('admin_grades_course_update.html', form=form, title = 'Add Course Grade', courseid = courseid, user = username, collection = collection)

@app.route('/admin/grades/approve/<id>/<courseid>/<studentid>', methods = ['GET'])
@admin_login_required
def admin_grades_course_approve(id, courseid, studentid):

    flash("Grade Approved Successfully")

    # Update the student based on their logged in ID
    db.student_course_grade.update_one({"StudentID": studentid},{"$set":{"ApprovalStatus": 1 }})
        
    return redirect("/admin/grades/" + courseid)


@app.route('/admin/queries', methods = ['GET', 'POST'])
@admin_login_required
def admin_queries():

    form = SearchFormQueries()
    searched_name = ""
    search_count = ""

    # Record User Activity
    loguseractvity("View", "/admin/queries/")

    if form.validate_on_submit():

        searched_name = form.data["name"]
        collection = db.query.find({"studentName":{"$regex": searched_name}})
        search_count = collection.count()

    else:

        collection = db.query.find()
        search_count = collection.count()

    return render_template('admin_queries.html', title = 'Student Queries', search_count = search_count, searchName = searched_name, form = form, user = username, collection = collection)


@app.route('/admin/transcripts', methods = ['GET', 'POST'])
@admin_login_required
def admin_transcripts():

    global username
    username = session['username']
    form = SearchFormTranscripts()
    searched_name = ""
    search_count = ""

    # Record User Activity
    loguseractvity("View", "/admin/transcripts")

    if form.validate_on_submit():

        searched_name = form.data["name"]
        collection = db.student_transcript.find({"studentName":{"$regex": searched_name}})
        search_count = collection.count()

    else:

        collection = db.student_transcript.find()
        search_count = collection.count()

    return render_template('admin_transcripts.html', title = 'Courses', search_count = search_count, searchName = searched_name, form = form, user = username, collection = collection)

@app.route('/admin/insurance', methods = ['GET', 'POST'])
@admin_login_required
def admin_insurance():
    global username
    username = session['username']
    form = SearchFormInsurance()
    searched_id = ''
    search_count = ''

    # Record User Activity

    loguseractvity('View', '/admin/insurance')
    if form.validate_on_submit():

        searched_id = form.data['name']
        collection = db.insurance.find({'studentId': {'$regex': searched_id}})
        search_count = collection.count()
    else:

        collection = db.insurance.find()
        search_count = collection.count()

    return render_template(
        'admin_insurance.html',
        title='Insurance',
        search_count=search_count,
        searchId=searched_id,
        form=form,
        user=username,
        collection=collection,
        )

@app.route('/admin/insurance/<studentId>', methods = ['GET', 'POST'])
@admin_login_required
def admin_insurance_status_update(studentId):
    insuranceform = InsuranceForm()
    insurance_details = db.insurance.find_one({'_id': ObjectId(studentId)})
    if request.method == 'POST':
        db.insurance.update_one({'studentId': userId,
                                'insuranceStatus': {"$set":insuranceform.insurancedata['insuranceStatus'
                                ]}})

    return render_template(
        'admin_insurance_status_update.html',
        title='Insurance Details',
        student_data=student_data,
        user=username,
        insurance_details=insurance_details,
        insuranceform=insuranceform,
        )
	
@app.route('/admin/usermanager', methods = ['GET', 'POST'])
@admin_login_required
def admin_user_manager():

    global username
    menu_type = 1
    username = session['username']
    userid = session['userid']

    loguseractvity("View", "/admin/usermanager")

    collection = db.user.find_one({'UserID': userid})

    return render_template('admin_user_manager.html', title = 'User Manager', collection = collection, user = username, userid = userid)



@app.route('/admin/view/users', methods = ['GET', 'POST'])
@admin_login_required
def admin_user_view():

    global username
    menu_type = 1
    username = session['username']
    userid = session['userid']

    form = SearchFormQueries()
    searched_name = ""
    search_count = ""

    # Record User Activity
    loguseractvity("View", "/admin/view/users")

    if form.validate_on_submit():

        searched_name = form.data["name"]
        collection = db.query.find({"studentName":{"$regex": searched_name}})
        search_count = collection.count()

    else:

        collection = db.user.find({'userType': "2"})
        search_count = collection.count()

    return render_template('admin_user_view.html', title = 'View Users', search_count = search_count, searchName = searched_name, form = form, user = username, collection = collection)

@app.route('/admin/view/users/<userid>', methods = ['GET', 'POST'])
@admin_login_required
def admin_user_view_by_id(userid):

    global username
    username = session['username']

    loguseractvity("View", "/admin/view/users/" + str(userid))

    collection = db.user.find_one({ "_id": ObjectId(userid) })

    return render_template('admin_user_view_id.html', title = 'View User', user = username, collection = collection)


@app.route('/admin/add/user', methods = ['GET', 'POST'])
@admin_login_required
def admin_user_add():

    global username
    menu_type = 1
    username = session['username']
    userid = session['userid']

    return render_template('admin_user_add.html', title = 'Add New User', user = username, userid = userid)


@app.route('/admin/deregister/<courseID>/<studentID>', methods = ['GET', 'POST'])
@admin_login_required
def admin_deregister_student(courseID, studentID):

    global username
    menu_type = 1
    username = session['username']
    userid = session['userid']

    loguseractvity("View", "/admin/deregister/" + str(courseID) + "/" + str(studentID)  )

    collection = db.student_course_grade.find_one({ "StudentID": studentID, "CourseID":courseID })

    return render_template('admin_student_deregister.html', title = 'Deregister Student', collection = collection, user = username, userid = userid, courseID = courseID, studentID = studentID)

@app.route('/admin/deregister/<studentID>/<courseID>/confirmed', methods = ['GET', 'POST'])
@admin_login_required
def admin_deregister_student_confirm(studentID, courseID):

    StudentIDIDArr = db.user.find_one({ "UserID": studentID })
    db.registration.remove({ "studentID": studentID, "courseID":courseID })

    loguseractvity("View", "/admin/deregister/" + str(courseID) + "/" + str(studentID) + "/confirm"  )
    return redirect("/admin/student/" + str(StudentIDIDArr["_id"]) )
