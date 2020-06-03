from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField, DateTimeField, IntegerField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, InputRequired, Required
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.fields.html5 import EmailField, DateField
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from wtforms.widgets import TextArea

############################################################
##################### GENERAL Form Classes #################
############################################################

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ForgotForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    userid = StringField('Userid', validators=[DataRequired()])
    submit = SubmitField('Sign In')


############################################################
##################### COURSES Form Classes #################
############################################################

class CourseSelectTermForm(FlaskForm):
    terms = SelectField(u'Term', choices=[('1', 'Semester I'), ('2', 'Semester II'), ('3', 'Semester III')])
    years = SelectField(u'Year', choices=[('1', 'Year 1'), ('2', 'Year 2'), ('3', 'Year 3'), ('4', 'Year 4')])
    
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
    yearOfStudy = SelectField(u'Year of Study: ', 
    choices=[('Year1','Year 1'), ('Year2', 'Year 2'), 
    ('Year3', 'Year 3'), ('Year4', 'Year 4')])
    semester = SelectField(u'Semester: ', 
    choices=[('Semester1','Semester 1'), ('Semester2', 'Semester 2'), 
    ('Summer', 'Summer')])
    studentIssues = SelectField(u'Issue: ', 
    choices=[('Grades','Grades'), ('Finance', 'Finance'), 
    ('Transcript', 'Transcript'), ('Course', 'Course'), ('Other', 'Other')])
    queryDesc = TextAreaField('Please state your query: ', validators=[DataRequired()])
    submit = SubmitField('Submit')


class PersonalInfoForm(FlaskForm):
    studentPhoto = FileField('Student Photo: ', validators=[FileRequired()])
    studentId = IntegerField('Student ID: ', validators=[DataRequired()])
    gender = SelectField(u'Gender: ', 
    choices=[('Male','Male'), ('Female', 'Female')])

    #dob = DateField('Date of Birth: ', validators=[DataRequired()], format='%Y-%m-%d')
#     dob = DateTimeField(
#         label='Date of Birth: ',
#         format='%Y-%m-%d',
#         validators = [Required('please select a valid date of birth')]
#     )
    dob = DateField('Date of Birth: ', validators=[DataRequired()], format="%d-%m-%y")
    
    maritalStatus = SelectField(u'Marital Status: ', 
    choices=[('Single','Single'), ('Married', 'Married'), 
    ('Separated', 'Separated'), ('Divorced', 'Divorced')],
        default='single', validators=[DataRequired()])
    
    studentAddress = StringField('Address: ', validators=[DataRequired()])
    mobilenum = IntegerField('Mobile Number: ', validators=[DataRequired()])
    passport = FileField('Passport Copy: ', validators=[FileRequired()])
    emergencyCon = StringField('Emergency Contact: ', validators=[DataRequired()])
    relationship = SelectField(u'Relationship: ', 
    choices=[('Relative','Relative'), ('Spouse', 'Spouse'), 
    ('Friend', 'Friend')])
    ecNumber = IntegerField('Telephone Number: ', validators=[DataRequired()])

    submit = SubmitField('Submit')

class InsuranceForm(FlaskForm):
    studentId = IntegerField('Student ID: ', validators=[DataRequired()])
    studentName = HiddenField('Name: ', validators=[DataRequired()])
    studentEmail = HiddenField('Email: ', validators=[DataRequired()])
    insurancePeriod = SelectField(u'Insurance Period: ', 
                                  choices=[('6 months','6 Months'), ('1 Year', '1 Year')])
    payment = FileField('Payement Reciept: ', validators=[FileRequired()])
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

    description = StringField('Description', widget = TextArea())

    notification = RadioField('Notify students of event',choices = [('Yes')])

    # Perhaps an end time
    # Perhaps a description - done
    # Ask to send email notification out to all of the student - radiobutton (not functional)

    # Perhaps an image - done
    photo = FileField('Photo', validators=[FileRequired()])

    location = StringField('Event Location', validators=[DataRequired()])
    submit = SubmitField('Add Event')
    
    
############################################################
#################### ADMIN SEARCH Forms Classes ##################
############################################################

class SearchForm(FlaskForm):
    course_name = StringField('Course Name or Number', validators=[DataRequired()])
    semester = SelectField(u'Semester', choices=[('1', 'I'), ('2', 'II')])
    submit = SubmitField('Search')

class SearchFormStudents(FlaskForm):
    name = StringField('Student Name or Number', validators=[DataRequired()])
    submit = SubmitField('Search')

class SearchFormQueries(FlaskForm):
    name = StringField('Query Name', validators=[DataRequired()])
   # progress = SelectField(u'Progress', choices=[('1', 'Outstanding'), ('2', 'Complete')])
    submit = SubmitField('Search')

class SearchFormTranscripts(FlaskForm):
    name = StringField('Transcript User', validators=[DataRequired()])
    submit = SubmitField('Search')

class SearchFormEvents(FlaskForm):
    name = StringField('Event Name', validators=[DataRequired()])
    submit = SubmitField('Search')

class SearchFormInsurance(FlaskForm):
    name = StringField('Student ID', validators=[DataRequired()])
    submit = SubmitField('Search')
    
class AddCourseGradeForm(FlaskForm):
    course = StringField('Course Grade', validators=[DataRequired()])
    exam = StringField('Exam Grade', validators=[DataRequired()])

    term = SelectField(u'Mid-Term or Final', choices=[('1', 'MidTerm'), ('2', 'Final')])
    submit = SubmitField('Submit Grade')
