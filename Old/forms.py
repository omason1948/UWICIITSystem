from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, IntegerField, DateField, RadioField, SelectField, TextAreaField
from wtforms.fields.html5 import EmailField  
from wtforms.validators import DataRequired

class QueryForm(FlaskForm):
    studentId = IntegerField('Student ID: ', validators=[DataRequired()])
    studentName = StringField('Name: ', validators=[DataRequired()])
    studentEmail = EmailField('Email: ', validators=[DataRequired()])
    yearOfStudy = RadioField('Year of Study: ', 
    choices=[('year1','Year 1'), ('year2', 'Year 2'), 
    ('year3', 'Year 3'), ('year4', 'Year 4')])
    semester = RadioField('Semester: ', 
    choices=[('semester1','Semester 1'), ('semester2', 'Semester 2'), 
    ('summer', 'Summer')])
    studentIssues = RadioField('Issue: ', 
    choices=[('grade','Grades'), ('finance', 'Finance'), 
    ('transcript', 'Transcript'), ('course', 'Course'), ('other', 'Other')])
    queryDesc = TextAreaField('Please state your query: ', validators=[DataRequired()])
    submit = SubmitField('Submit')


class PersonalInfoForm(FlaskForm):
    dob = DateField('Date of Birth: ', validators=[DataRequired()], format='%Y-%m-%d')
    maritalStatus = RadioField('Marital Status: ', 
    choices=[('single','Single'), ('married', 'Married'), 
    ('separated', 'Separated'), ('divorced', 'Divorced')])
    contactEmail = EmailField('Email: ', validators=[DataRequired()])
    studentAddress = TextAreaField('Address: ', validators=[DataRequired()])
    phonenum = IntegerField('Telephone Number: ', validators=[DataRequired()])
    mobilenum = IntegerField('Mobile Number: ', validators=[DataRequired()])
    emergencyCon = StringField('Emergency Contact: ', validators=[DataRequired()])
    relationship = RadioField('Relationship: ', 
    choices=[('relative','Relative'), ('spouse', 'Spouse'), 
    ('friend', 'Friend')])
    ecAddress = TextAreaField('Address: ', validators=[DataRequired()])
    ecNumber = IntegerField('Telephone Number: ', validators=[DataRequired()])
    submit = SubmitField('Submit')




