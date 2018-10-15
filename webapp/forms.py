from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, FloatField, IntegerField,
                     TextAreaField, SelectField)
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import DataRequired, Email


class CredentialsForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class LocationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    latitude = FloatField('Latitude', validators=[DataRequired()])
    longitude = FloatField('Longitude', validators=[DataRequired()])


class UniversityForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    location_id = IntegerField('Location ID')
    description = TextAreaField('Description')
    population = IntegerField('Population')


class StudentInfoForm(FlaskForm):
    univid = IntegerField('University ID', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])


class RSOForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    user1 = StringField('User1', validators=[DataRequired()])
    user2 = StringField('User2', validators=[DataRequired()])
    user3 = StringField('User3', validators=[DataRequired()])
    user4 = StringField('User4', validators=[DataRequired()])
    user5 = StringField('User5', validators=[DataRequired()])


class EventForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    date = DateField("Date", format='%Y-%m-%d', validators=[DataRequired()])
    time = TimeField("Time", validators=[DataRequired()])
    location_id = IntegerField("Location ID", validators=[DataRequired()])
    cphone = StringField("Contact Phone", validators=[DataRequired()])
    cemail = StringField("Contact Email", validators=[DataRequired()])
    restriction = SelectField("Restriction", coerce=int)
