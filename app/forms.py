from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField, DateTimeField, IntegerField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, InputRequired, Required
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.fields.html5 import EmailField, DateField
import datetime
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename

############################################################
##################### GENERAL Form Classes #################
############################################################

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

############################################################
##################### COURSES Form Classes #################
############################################################

class CourseSelectTermForm(FlaskForm):
    terms = SelectField(u'Terms', choices=[('2019/2020SI', '2019/2020 Semester II'), ('2019/2020SII', '2019/2020 Semester I'), ('2018/2019SII', '2018/2019 Semester II')])
    submit = SubmitField('Next')

class CourseFinderForm(FlaskForm):
    name = StringField(u'Find by Name', validators=[DataRequired()])
    submit = SubmitField('Search')

############################################################
################## TRANSCRIPT Form Classes #################
############################################################

class NewTranscriptForm(FlaskForm):
    fullname = StringField('Full Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    #startyear = DateTimeField('Start Year', id='datepick')
    #startyear = DateField( 'Date', format = "%d%b%Y %H:%M", validators=[DataRequired()] )

    startyear = DateTimeLocalField(
        label='Start Date',
        format='%Y-%m-%dT%H:%M',
        validators = [Required('please select startdate')]
    )

    #endyear = StringField('End Year', validators=[DataRequired()])
    endyear = DateTimeLocalField(
        label='End Date',
        format='%Y-%m-%dT%H:%M',
        validators = [Required('please select end date')]
    )

    faculty = SelectField(
        u'Faculty Type',
        choices = [('Humanities & Education', 'Humanities & Education'), ('Law', 'Law'), ('Medical Sciences', 'Medical Sciences'), ('Science & Technology', 'Science & Technology')]
    )

    officialcopy = RadioField('Copy Type', choices=[('Yes','Official Copy'),('No','Student Copy')])
    emailTo = StringField('Email To', validators=[DataRequired()])

    submit = SubmitField('Request')

############################################################
####### Query | Personal Information Forms Classes #########
############################################################

class QueryForm(FlaskForm):
    studentId = HiddenField('Student ID: ', validators=[DataRequired()])
    studentName = HiddenField('Name: ', validators=[DataRequired()])
    studentEmail = HiddenField('Email: ', validators=[DataRequired()])
    yearOfStudy = RadioField('Year of Study: ', 
    choices=[('year1','Year 1'), ('year2', 'Year 2'), 
    ('year3', 'Year 3'), ('year4', 'Year 4')])
    semester = RadioField('Semester: ', 
    choices=[('semester1','Semester 1'), ('semester2', 'Semester 2'), 
    ('summer', 'Summer')])
    studentIssues = RadioField('Issue: ', 
    choices=[('Grades','Grades'), ('Finance', 'Finance'), 
    ('Transcript', 'Transcript'), ('Course', 'Course'), ('Other', 'Other')])
    queryDesc = TextAreaField('Please state your query: ', validators=[DataRequired()])
    submit = SubmitField('Submit')


class PersonalInfoForm(FlaskForm):
    studentId = IntegerField('Student ID: ', validators=[DataRequired()])
    gender = RadioField('Gender: ', 
    choices=[('male','Male'), ('female', 'Female')])

    #dob = DateField('Date of Birth: ', validators=[DataRequired()], format='%Y-%m-%d')
    dob = DateTimeLocalField(
        label='Date of Birth: ',
        format='%Y-%m-%dT%H:%M',
        validators = [Required('please select a valid date of birth')]
    )
    
    maritalStatus = RadioField('Marital Status: ', 
    choices=[('single','Single'), ('married', 'Married'), 
    ('separated', 'Separated'), ('divorced', 'Divorced')],
        default='single', validators=[DataRequired()])
    
    studentAddress = TextAreaField('Address: ', validators=[DataRequired()], default='')
    mobilenum = IntegerField('Mobile Number: ', validators=[DataRequired()])
    passport = FileField('Passport Copy: ', validators=[FileRequired()])

    submit = SubmitField('Submit')

class EmergencyContactForm(FlaskForm):
    studentId = IntegerField('Student ID: ', validators=[DataRequired()])
    emergencyCon = StringField('Emergency Contact: ', validators=[DataRequired()])
    relationship = RadioField('Relationship: ', 
    choices=[('relative','Relative'), ('spouse', 'Spouse'), 
    ('friend', 'Friend')])
    ecNumber = IntegerField('Telephone Number: ', validators=[DataRequired()])
    submit = SubmitField('Submit')


############################################################
#################### Events Forms Classes ##################
############################################################

class EventForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])

    #DateTimeField does not show up calendar
    
    eventDate = DateTimeLocalField(
        label='Date',
        format='%Y-%m-%dT%H:%M',
        validators = [Required('please select startdate')]
    )

    # Perhaps an end time
    # Perhaps a description
    # Ask to send email notification out to all of the student - radiobutton

    # Perhaps an image - done
    photo = FileField('Photo', validators=[FileRequired()])

    location = StringField('Event Location', validators=[DataRequired()])
    submit = SubmitField('Add Event')
