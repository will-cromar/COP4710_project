from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, FloatField, IntegerField,
                     TextAreaField)
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
