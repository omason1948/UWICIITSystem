from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField, DateTimeField, IntegerField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, InputRequired, Required
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.fields.html5 import EmailField, DateField
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from wtforms.widgets import TextArea
from wtforms.fields.html5 import TelField

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
    submit = SubmitField('Reset Password')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirmpassword = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Reset My Password')

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

    studentId = StringField('Student ID: ', validators=[DataRequired()])
    fullname = StringField('Full Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    #startyear = DateTimeField('Start Year', id='datepick')
    #startyear = DateField( 'Date', format = "%d%b%Y %H:%M", validators=[DataRequired()] )

    startyear = DateTimeLocalField(
        label='Start Date',
        format='%Y-%m-%d %H:%M',
        validators = [Required('please select startdate')]
    )

    #endyear = StringField('End Year', validators=[DataRequired()])
    endyear = DateTimeLocalField(
        label='End Date',
        format='%Y-%m-%d %H:%M',
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
    queryDesc = TextAreaField('Please state your query: ', validators=[DataRequired()], render_kw={"rows": 5, "cols": 70} )
    submit = SubmitField('Submit')


class PersonalInfoForm(FlaskForm):
    studentPhoto = FileField('Student Photo: ', validators=[FileRequired()])
    studentId = IntegerField('Student ID: ', validators=[DataRequired()])
    maritalStatus = SelectField(u'Marital Status: ', 
    choices=[('Single','Single'), ('Married', 'Married'), 
    ('Separated', 'Separated'), ('Divorced', 'Divorced')],
        default='single', validators=[DataRequired()])
    studentAddress = StringField('Address: ', validators=[DataRequired()])
    country = SelectField(u' Country: ', choices=[
    ('Afghanistan', 'Afghanistan',),
    ('Aland Islands', 'Aland Islands',),
    ('Albania', 'Albania',),
    ('Algeria', 'Algeria',),
    ('American Samoa', 'American Samoa',),
    ('Andorra', 'Andorra',),
    ('Angola', 'Angola',),
    ('Anguilla', 'Anguilla',),
    ('Antarctica', 'Antarctica',),
    ('Antigua and Barbuda', 'Antigua and Barbuda',),
    ('Argentina', 'Argentina',),
    ('Armenia', 'Armenia',),
    ('Aruba', 'Aruba',),
    ('Australia', 'Australia',),
    ('Austria', 'Austria',),
    ('Azerbaijan', 'Azerbaijan',),
    ('Bahamas', 'Bahamas',),
    ('Bahrain', 'Bahrain',),
    ('Bangladesh', 'Bangladesh',),
    ('Barbados', 'Barbados',),
    ('Belarus', 'Belarus',),
    ('Belgium', 'Belgium',),
    ('Belize', 'Belize',),
    ('Benin', 'Benin',),
    ('Bermuda', 'Bermuda',),
    ('Bhutan', 'Bhutan',),
    ('Bolivia, Plurinational State of', 'Bolivia, Plurinational State of',),
    ('Bonaire, Sint Eustatius and Saba', 'Bonaire, Sint Eustatius and Saba',),
    ('Bosnia and Herzegovina', 'Bosnia and Herzegovina',),
    ('Botswana', 'Botswana',),
    ('Bouvet Island', 'Bouvet Island',),
    ('Brazil', 'Brazil',),
    ('British Indian Ocean Territory', 'British Indian Ocean Territory',),
    ('Brunei Darussalam', 'Brunei Darussalam',),
    ('Bulgaria', 'Bulgaria',),
    ('Burkina Faso', 'Burkina Faso',),
    ('Burundi', 'Burundi',),
    ('Cambodia', 'Cambodia',),
    ('Cameroon', 'Cameroon',),
    ('Canada', 'Canada',),
    ('Cape Verde', 'Cape Verde',),
    ('Cayman Islands', 'Cayman Islands',),
    ('Central African Republic', 'Central African Republic',),
    ('Chad', 'Chad',),
    ('Chile', 'Chile',),
    ('China', 'China',),
    ('Christmas Island', 'Christmas Island',),
    ('Cocos (Keeling) Islands', 'Cocos (Keeling) Islands',),
    ('Colombia', 'Colombia',),
    ('Comoros', 'Comoros',),
    ('Congo', 'Congo',),
    ('Congo, the Democratic Republic of the', 'Congo, the Democratic Republic of the',),
    ('Cook Islands', 'Cook Islands',),
    ('Costa Rica', 'Costa Rica',),
    ("Cote d'Ivoire", "Cote d'Ivoire",),
    ('Croatia', 'Croatia',),
    ('Cuba', 'Cuba',),
    ('Curacao', 'Curacao',),
    ('Cyprus', 'Cyprus',),
    ('Czech Republic', 'Czech Republic',),
    ('Denmark', 'Denmark',),
    ('Djibouti', 'Djibouti',),
    ('Dominica', 'Dominica',),
    ('Dominican Republic', 'Dominican Republic',),
    ('Ecuador', 'Ecuador',),
    ('Egypt', 'Egypt',),
    ('El Salvador', 'El Salvador',),
    ('Equatorial Guinea', 'Equatorial Guinea',),
    ('Eritrea', 'Eritrea',),
    ('Estonia', 'Estonia',),
    ('Ethiopia', 'Ethiopia',),
    ('Falkland Islands (Malvinas)', 'Falkland Islands (Malvinas)',),
    ('Faroe Islands', 'Faroe Islands',),
    ('Fiji', 'Fiji',),
    ('Finland', 'Finland',),
    ('France', 'France',),
    ('French Guiana', 'French Guiana',),
    ('French Polynesia', 'French Polynesia',),
    ('French Southern Territories', 'French Southern Territories',),
    ('Gabon', 'Gabon',),
    ('Gambia', 'Gambia',),
    ('Georgia', 'Georgia',),
    ('Germany', 'Germany',),
    ('Ghana', 'Ghana',),
    ('Gibraltar', 'Gibraltar',),
    ('Greece', 'Greece',),
    ('Greenland', 'Greenland',),
    ('Grenada', 'Grenada',),
    ('Guadeloupe', 'Guadeloupe',),
    ('Guam', 'Guam',),
    ('Guatemala', 'Guatemala',),
    ('Guernsey', 'Guernsey',),
    ('Guinea', 'Guinea',),
    ('Guinea-Bissau', 'Guinea-Bissau',),
    ('Guyana', 'Guyana',),
    ('Haiti', 'Haiti',),
    ('Heard Island and McDonald Islands', 'Heard Island and McDonald Islands',),
    ('Holy See (Vatican City State)', 'Holy See (Vatican City State)',),
    ('Honduras', 'Honduras',),
    ('Hong Kong', 'Hong Kong',),
    ('Hungary', 'Hungary',),
    ('Iceland', 'Iceland',),
    ('India', 'India',),
    ('Indonesia', 'Indonesia',),
    ('Iran, Islamic Republic of', 'Iran, Islamic Republic of',),
    ('Iraq', 'Iraq',),
    ('Ireland', 'Ireland',),
    ('Isle of Man', 'Isle of Man',),
    ('Israel', 'Israel',),
    ('Italy', 'Italy',),
    ('Jamaica', 'Jamaica',),
    ('Japan', 'Japan',),
    ('Jersey', 'Jersey',),
    ('Jordan', 'Jordan',),
    ('Kazakhstan', 'Kazakhstan',),
    ('Kenya', 'Kenya',),
    ('Kiribati', 'Kiribati',),
    ("Korea, Democratic People's Republic of", "Korea, Democratic People's Republic of",),
    ('Korea, Republic of', 'Korea, Republic of',),
    ('Kuwait', 'Kuwait',),
    ('Kyrgyzstan', 'Kyrgyzstan',),
    ("Lao People's Democratic Republic", "Lao People's Democratic Republic",),
    ('Latvia', 'Latvia',),
    ('Lebanon', 'Lebanon',),
    ('Lesotho', 'Lesotho',),
    ('Liberia', 'Liberia',),
    ('Libya', 'Libya',),
    ('Liechtenstein', 'Liechtenstein',),
    ('Lithuania', 'Lithuania',),
    ('Luxembourg', 'Luxembourg',),
    ('Macao', 'Macao',),
    ('Macedonia, the former Yugoslav Republic of', 'Macedonia, the former Yugoslav Republic of',),
    ('Madagascar', 'Madagascar',),
    ('Malawi', 'Malawi',),
    ('Malaysia', 'Malaysia',),
    ('Maldives', 'Maldives',),
    ('Mali', 'Mali',),
    ('Malta', 'Malta',),
    ('Marshall Islands', 'Marshall Islands',),
    ('Martinique', 'Martinique',),
    ('Mauritania', 'Mauritania',),
    ('Mauritius', 'Mauritius',),
    ('Mayotte', 'Mayotte',),
    ('Mexico', 'Mexico',),
    ('Micronesia, Federated States of', 'Micronesia, Federated States of',),
    ('Moldova, Republic of', 'Moldova, Republic of',),
    ('Monaco', 'Monaco',),
    ('Mongolia', 'Mongolia',),
    ('Montenegro', 'Montenegro',),
    ('Montserrat', 'Montserrat',),
    ('Morocco', 'Morocco',),
    ('Mozambique', 'Mozambique',),
    ('Myanmar', 'Myanmar',),
    ('Namibia', 'Namibia',),
    ('Nauru', 'Nauru',),
    ('Nepal', 'Nepal',),
    ('Netherlands', 'Netherlands',),
    ('New Caledonia', 'New Caledonia',),
    ('New Zealand', 'New Zealand',),
    ('Nicaragua', 'Nicaragua',),
    ('Niger', 'Niger',),
    ('Nigeria', 'Nigeria',),
    ('Niue', 'Niue',),
    ('Norfolk Island', 'Norfolk Island',),
    ('Northern Mariana Islands', 'Northern Mariana Islands',),
    ('Norway', 'Norway',),
    ('Oman', 'Oman',),
    ('Pakistan', 'Pakistan',),
    ('Palau', 'Palau',),
    ('Palestine, State of', 'Palestine, State of',),
    ('Panama', 'Panama',),
    ('Papua New Guinea', 'Papua New Guinea',),
    ('Paraguay', 'Paraguay',),
    ('Peru', 'Peru',),
    ('Philippines', 'Philippines',),
    ('Pitcairn', 'Pitcairn',),
    ('Poland', 'Poland',),
    ('Portugal', 'Portugal',),
    ('Puerto Rico', 'Puerto Rico',),
    ('Qatar', 'Qatar',),
    ('Reunion', 'Reunion',),
    ('Romania', 'Romania',),
    ('Russian Federation', 'Russian Federation',),
    ('Rwanda', 'Rwanda',),
    ('Saint Barthelemy', 'Saint Barthelemy',),
    ('Saint Helena, Ascension and Tristan da Cunha', 'Saint Helena, Ascension and Tristan da Cunha',),
    ('Saint Kitts and Nevis', 'Saint Kitts and Nevis',),
    ('Saint Lucia', 'Saint Lucia',),
    ('Saint Martin', 'Saint Martin',),
    ('Saint Pierre and Miquelon', 'Saint Pierre and Miquelon',),
    ('Saint Vincent and the Grenadines', 'Saint Vincent and the Grenadines',),
    ('Samoa', 'Samoa',),
    ('San Marino', 'San Marino',),
    ('Sao Tome and Principe', 'Sao Tome and Principe',),
    ('Saudi Arabia', 'Saudi Arabia',),
    ('Senegal', 'Senegal',),
    ('Serbia', 'Serbia',),
    ('Seychelles', 'Seychelles',),
    ('Sierra Leone', 'Sierra Leone',),
    ('Singapore', 'Singapore',),
    ('Sint Maarten', 'Sint Maarten',),
    ('Slovakia', 'Slovakia',),
    ('Slovenia', 'Slovenia',),
    ('Solomon Islands', 'Solomon Islands',),
    ('Somalia', 'Somalia',),
    ('South Africa', 'South Africa',),
    ('South Georgia and the South Sandwich Islands', 'South Georgia and the South Sandwich Islands',),
    ('South Sudan', 'South Sudan',),
    ('Spain', 'Spain',),
    ('Sri Lanka', 'Sri Lanka',),
    ('Sudan', 'Sudan',),
    ('Suriname', 'Suriname',),
    ('Svalbard and Jan Mayen', 'Svalbard and Jan Mayen',),
    ('Swaziland', 'Swaziland',),
    ('Sweden', 'Sweden',),
    ('Switzerland', 'Switzerland',),
    ('Syrian Arab Republic', 'Syrian Arab Republic',),
    ('Taiwan, Province of China', 'Taiwan, Province of China',),
    ('Tajikistan', 'Tajikistan',),
    ('Tanzania, United Republic of', 'Tanzania, United Republic of',),
    ('Thailand', 'Thailand',),
    ('Timor-Leste', 'Timor-Leste',),
    ('Togo', 'Togo',),
    ('Tokelau', 'Tokelau',),
    ('Tonga', 'Tonga',),
    ('Trinidad and Tobago', 'Trinidad and Tobago',),
    ('Tunisia', 'Tunisia',),
    ('Turkey', 'Turkey',),
    ('Turkmenistan', 'Turkmenistan',),
    ('Turks and Caicos Islands', 'Turks and Caicos Islands',),
    ('Tuvalu', 'Tuvalu',),
    ('Uganda', 'Uganda',),
    ('Ukraine', 'Ukraine',),
    ('United Arab Emirates', 'United Arab Emirates',),
    ('United Kingdom', 'United Kingdom',),
    ('United States', 'United States',),
    ('United States Minor Outlying Islands', 'United States Minor Outlying Islands',),
    ('Uruguay', 'Uruguay',),
    ('Uzbekistan', 'Uzbekistan',),
    ('Vanuatu', 'Vanuatu',),
    ('Venezuela, Bolivarian Republic of', 'Venezuela, Bolivarian Republic of',),
    ('Viet Nam', 'Viet Nam',),
    ('Virgin Islands, British', 'Virgin Islands, British',),
    ('Virgin Islands, U.S.', 'Virgin Islands, U.S.',),
    ('Wallis and Futuna', 'Wallis and Futuna',),
    ('Western Sahara', 'Western Sahara',),
    ('Yemen', 'Yemen',),
    ('Zambia', 'Zambia',),
    ('Zimbabwe', 'Zimbabwe',)])
    mobilenum = TelField('Mobile Number: ', validators=[DataRequired()])
    passport = FileField('Passport Copy: ', validators=[FileRequired()])
    emergencyCon = StringField('Emergency Contact: ', validators=[DataRequired()])
    relationship = SelectField(u'Relationship: ', 
    choices=[('Relative','Relative'), ('Spouse', 'Spouse'), 
    ('Friend', 'Friend')])
    ecNumber = TelField('Telephone Number: ', validators=[DataRequired()])

    submit = SubmitField('Submit')

class InsuranceForm(FlaskForm):
    studentId = IntegerField('Student ID: ', validators=[DataRequired()])
    studentName = HiddenField('Name: ', validators=[DataRequired()])
    studentEmail = HiddenField('Email: ', validators=[DataRequired()])
    insurancePeriod = SelectField(u'Insurance Period: ', 
                                  choices=[('6 months','6 Months'), ('1 Year', '1 Year')])
    payment = FileField('Payement Reciept: ', validators=[FileRequired()])
    insuranceStatus = RadioField('Insurance Status', choices=[('Insured','Insured'),('Uninsured','Uninsured'),('Renewal Due','Renewal Due')])
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
        validators = [Required('please select a date')]
    )

    description = StringField('Description', widget = TextArea())

    notification = RadioField('Notify students of event',choices = [('Yes')])

    # Perhaps an end time
    # Perhaps a description - done
    # Ask to send email notification out to all of the student - radiobutton (not functional)

    # Perhaps an image - done
    photo = FileField('Photo')

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
    name = StringField('Student Identification Number', validators=[DataRequired()])
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
