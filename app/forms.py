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
    queryDesc = TextAreaField('Please state your query: ', validators=[DataRequired()])
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
    ('AF', 'Afghanistan',),
    ('AX', 'Aland Islands',),
    ('AL', 'Albania',),
    ('DZ', 'Algeria',),
    ('AS', 'American Samoa',),
    ('AD', 'Andorra',),
    ('AO', 'Angola',),
    ('AI', 'Anguilla',),
    ('AQ', 'Antarctica',),
    ('AG', 'Antigua and Barbuda',),
    ('AR', 'Argentina',),
    ('AM', 'Armenia',),
    ('AW', 'Aruba',),
    ('AU', 'Australia',),
    ('AT', 'Austria',),
    ('AZ', 'Azerbaijan',),
    ('BS', 'Bahamas',),
    ('BH', 'Bahrain',),
    ('BD', 'Bangladesh',),
    ('BB', 'Barbados',),
    ('BY', 'Belarus',),
    ('BE', 'Belgium',),
    ('BZ', 'Belize',),
    ('BJ', 'Benin',),
    ('BM', 'Bermuda',),
    ('BT', 'Bhutan',),
    ('BO', 'Bolivia, Plurinational State of',),
    ('BQ', 'Bonaire, Sint Eustatius and Saba',),
    ('BA', 'Bosnia and Herzegovina',),
    ('BW', 'Botswana',),
    ('BV', 'Bouvet Island',),
    ('BR', 'Brazil',),
    ('IO', 'British Indian Ocean Territory',),
    ('BN', 'Brunei Darussalam',),
    ('BG', 'Bulgaria',),
    ('BF', 'Burkina Faso',),
    ('BI', 'Burundi',),
    ('KH', 'Cambodia',),
    ('CM', 'Cameroon',),
    ('CA', 'Canada',),
    ('CV', 'Cape Verde',),
    ('KY', 'Cayman Islands',),
    ('CF', 'Central African Republic',),
    ('TD', 'Chad',),
    ('CL', 'Chile',),
    ('CN', 'China',),
    ('CX', 'Christmas Island',),
    ('CC', 'Cocos (Keeling) Islands',),
    ('CO', 'Colombia',),
    ('KM', 'Comoros',),
    ('CG', 'Congo',),
    ('CD', 'Congo, the Democratic Republic of the',),
    ('CK', 'Cook Islands',),
    ('CR', 'Costa Rica',),
    ('CI', "Cote d'Ivoire",),
    ('HR', 'Croatia',),
    ('CU', 'Cuba',),
    ('CW', 'Curacao',),
    ('CY', 'Cyprus',),
    ('CZ', 'Czech Republic',),
    ('DK', 'Denmark',),
    ('DJ', 'Djibouti',),
    ('DM', 'Dominica',),
    ('DO', 'Dominican Republic',),
    ('EC', 'Ecuador',),
    ('EG', 'Egypt',),
    ('SV', 'El Salvador',),
    ('GQ', 'Equatorial Guinea',),
    ('ER', 'Eritrea',),
    ('EE', 'Estonia',),
    ('ET', 'Ethiopia',),
    ('FK', 'Falkland Islands (Malvinas)',),
    ('FO', 'Faroe Islands',),
    ('FJ', 'Fiji',),
    ('FI', 'Finland',),
    ('FR', 'France',),
    ('GF', 'French Guiana',),
    ('PF', 'French Polynesia',),
    ('TF', 'French Southern Territories',),
    ('GA', 'Gabon',),
    ('GM', 'Gambia',),
    ('GE', 'Georgia',),
    ('DE', 'Germany',),
    ('GH', 'Ghana',),
    ('GI', 'Gibraltar',),
    ('GR', 'Greece',),
    ('GL', 'Greenland',),
    ('GD', 'Grenada',),
    ('GP', 'Guadeloupe',),
    ('GU', 'Guam',),
    ('GT', 'Guatemala',),
    ('GG', 'Guernsey',),
    ('GN', 'Guinea',),
    ('GW', 'Guinea-Bissau',),
    ('GY', 'Guyana',),
    ('HT', 'Haiti',),
    ('HM', 'Heard Island and McDonald Islands',),
    ('VA', 'Holy See (Vatican City State)',),
    ('HN', 'Honduras',),
    ('HK', 'Hong Kong',),
    ('HU', 'Hungary',),
    ('IS', 'Iceland',),
    ('IN', 'India',),
    ('ID', 'Indonesia',),
    ('IR', 'Iran, Islamic Republic of',),
    ('IQ', 'Iraq',),
    ('IE', 'Ireland',),
    ('IM', 'Isle of Man',),
    ('IL', 'Israel',),
    ('IT', 'Italy',),
    ('JM', 'Jamaica',),
    ('JP', 'Japan',),
    ('JE', 'Jersey',),
    ('JO', 'Jordan',),
    ('KZ', 'Kazakhstan',),
    ('KE', 'Kenya',),
    ('KI', 'Kiribati',),
    ('KP', "Korea, Democratic People's Republic of",),
    ('KR', 'Korea, Republic of',),
    ('KW', 'Kuwait',),
    ('KG', 'Kyrgyzstan',),
    ('LA', "Lao People's Democratic Republic",),
    ('LV', 'Latvia',),
    ('LB', 'Lebanon',),
    ('LS', 'Lesotho',),
    ('LR', 'Liberia',),
    ('LY', 'Libya',),
    ('LI', 'Liechtenstein',),
    ('LT', 'Lithuania',),
    ('LU', 'Luxembourg',),
    ('MO', 'Macao',),
    ('MK', 'Macedonia, the former Yugoslav Republic of',),
    ('MG', 'Madagascar',),
    ('MW', 'Malawi',),
    ('MY', 'Malaysia',),
    ('MV', 'Maldives',),
    ('ML', 'Mali',),
    ('MT', 'Malta',),
    ('MH', 'Marshall Islands',),
    ('MQ', 'Martinique',),
    ('MR', 'Mauritania',),
    ('MU', 'Mauritius',),
    ('YT', 'Mayotte',),
    ('MX', 'Mexico',),
    ('FM', 'Micronesia, Federated States of',),
    ('MD', 'Moldova, Republic of',),
    ('MC', 'Monaco',),
    ('MN', 'Mongolia',),
    ('ME', 'Montenegro',),
    ('MS', 'Montserrat',),
    ('MA', 'Morocco',),
    ('MZ', 'Mozambique',),
    ('MM', 'Myanmar',),
    ('NA', 'Namibia',),
    ('NR', 'Nauru',),
    ('NP', 'Nepal',),
    ('NL', 'Netherlands',),
    ('NC', 'New Caledonia',),
    ('NZ', 'New Zealand',),
    ('NI', 'Nicaragua',),
    ('NE', 'Niger',),
    ('NG', 'Nigeria',),
    ('NU', 'Niue',),
    ('NF', 'Norfolk Island',),
    ('MP', 'Northern Mariana Islands',),
    ('NO', 'Norway',),
    ('OM', 'Oman',),
    ('PK', 'Pakistan',),
    ('PW', 'Palau',),
    ('PS', 'Palestine, State of',),
    ('PA', 'Panama',),
    ('PG', 'Papua New Guinea',),
    ('PY', 'Paraguay',),
    ('PE', 'Peru',),
    ('PH', 'Philippines',),
    ('PN', 'Pitcairn',),
    ('PL', 'Poland',),
    ('PT', 'Portugal',),
    ('PR', 'Puerto Rico',),
    ('QA', 'Qatar',),
    ('RE', 'Reunion',),
    ('RO', 'Romania',),
    ('RU', 'Russian Federation',),
    ('RW', 'Rwanda',),
    ('BL', 'Saint Barthelemy',),
    ('SH', 'Saint Helena, Ascension and Tristan da Cunha',),
    ('KN', 'Saint Kitts and Nevis',),
    ('LC', 'Saint Lucia',),
    ('MF', 'Saint Martin (French part)',),
    ('PM', 'Saint Pierre and Miquelon',),
    ('VC', 'Saint Vincent and the Grenadines',),
    ('WS', 'Samoa',),
    ('SM', 'San Marino',),
    ('ST', 'Sao Tome and Principe',),
    ('SA', 'Saudi Arabia',),
    ('SN', 'Senegal',),
    ('RS', 'Serbia',),
    ('SC', 'Seychelles',),
    ('SL', 'Sierra Leone',),
    ('SG', 'Singapore',),
    ('SX', 'Sint Maarten (Dutch part)',),
    ('SK', 'Slovakia',),
    ('SI', 'Slovenia',),
    ('SB', 'Solomon Islands',),
    ('SO', 'Somalia',),
    ('ZA', 'South Africa',),
    ('GS', 'South Georgia and the South Sandwich Islands',),
    ('SS', 'South Sudan',),
    ('ES', 'Spain',),
    ('LK', 'Sri Lanka',),
    ('SD', 'Sudan',),
    ('SR', 'Suriname',),
    ('SJ', 'Svalbard and Jan Mayen',),
    ('SZ', 'Swaziland',),
    ('SE', 'Sweden',),
    ('CH', 'Switzerland',),
    ('SY', 'Syrian Arab Republic',),
    ('TW', 'Taiwan, Province of China',),
    ('TJ', 'Tajikistan',),
    ('TZ', 'Tanzania, United Republic of',),
    ('TH', 'Thailand',),
    ('TL', 'Timor-Leste',),
    ('TG', 'Togo',),
    ('TK', 'Tokelau',),
    ('TO', 'Tonga',),
    ('TT', 'Trinidad and Tobago',),
    ('TN', 'Tunisia',),
    ('TR', 'Turkey',),
    ('TM', 'Turkmenistan',),
    ('TC', 'Turks and Caicos Islands',),
    ('TV', 'Tuvalu',),
    ('UG', 'Uganda',),
    ('UA', 'Ukraine',),
    ('AE', 'United Arab Emirates',),
    ('GB', 'United Kingdom',),
    ('US', 'United States',),
    ('UM', 'United States Minor Outlying Islands',),
    ('UY', 'Uruguay',),
    ('UZ', 'Uzbekistan',),
    ('VU', 'Vanuatu',),
    ('VE', 'Venezuela, Bolivarian Republic of',),
    ('VN', 'Viet Nam',),
    ('VG', 'Virgin Islands, British',),
    ('VI', 'Virgin Islands, U.S.',),
    ('WF', 'Wallis and Futuna',),
    ('EH', 'Western Sahara',),
    ('YE', 'Yemen',),
    ('ZM', 'Zambia',),
    ('ZW', 'Zimbabwe',)])
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
