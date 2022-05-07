from tokenize import String
from click import password_option
from flask_wtf import FlaskForm
from sqlalchemy import Integer
from wtforms import StringField, IntegerField, TimeField, BooleanField, PasswordField, DateField
from wtforms.validators import InputRequired, Optional

from functions import Validator


class AddLateBusForm(FlaskForm):
    
    stopNo = IntegerField("Stop number", validators=[InputRequired()])
    busNo = IntegerField("Bus number", validators=[InputRequired()])
    scheduled_arrival = TimeField("Scheduled arrival", validators=[InputRequired()])
    delay = IntegerField("Delay in minutes", validators=[Optional()])
    no_show = BooleanField("No show", validators=[Optional()])


class SignUp(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])


class Login(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])

class GetData(FlaskForm):
    busNo = IntegerField("Bus number", validators=[Optional()])
    stopNo = IntegerField("Stop number", validators=[Optional()])
    from_time = DateField("From", validators=[Optional()])
    to_time = DateField("To", validators=[Optional()])
