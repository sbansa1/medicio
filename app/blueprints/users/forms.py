from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, Optional, Length


class UserForm(FlaskForm):
    """Creates the user form """

    username=StringField("Username", validators=[DataRequired("Please Enter your User Name")])
    email=EmailField("Email_Address", validators=[DataRequired("This Field reuires a valid email_address"),
                                                  Email("This field requires a valid email address")])
    password=PasswordField('Password',
                           validators=[DataRequired("kindly enter your password"),
                                       Length(min=8,max=16,
                                                   message="Please make sure your password\
                                                           is atleast 8 characters long")])
    address_1=StringField('Address_1', validators=[DataRequired("please enter your address")])
    address_2=StringField('Address_2', validators=[Optional()])
    city =StringField('City',validators=[DataRequired("Please Enter your city name")])
    postal_code =StringField('Zip Code', validators=[DataRequired('Please Enter your zip Code'),
                                                     Length(min=6,max=6,
                                                                 message='The zip code shoudl be 6 digits long')])


    mobile_phone=StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=10)])



class DoctorForm(UserForm,FlaskForm):
    """Creates the Doctor Registration Form"""

    registration_number = StringField('Registration Number', validators=[DataRequired("Please Enter your registration\
                                                                                      Number")])
    state = StringField('State', validators=[DataRequired('Enter your State of Registration')])
    year_of_registration = StringField('Year Of Registration', validators=[DataRequired('Enter your year of\
                                                                                       Registration'),
                                                                           Length(min=4,max=4)])

