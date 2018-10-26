from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import (StringField, PasswordField, FloatField, IntegerField,
                     TextAreaField, SelectField, SubmitField, RadioField)
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import DataRequired, Email


class CredentialsForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField('Submit Form')


class LocationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    latitude = FloatField('Latitude', validators=[DataRequired()])
    longitude = FloatField('Longitude', validators=[DataRequired()])


class UniversityForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    location_id = IntegerField('Location ID')
    description = TextAreaField('Description')
    population = IntegerField('Population')
    submit_button = SubmitField('Submit Form')


class StudentInfoForm(FlaskForm):
    univid = IntegerField('University ID', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit_button = SubmitField('Submit Form')


class RSOForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    user1 = StringField('User1', validators=[DataRequired()])
    user2 = StringField('User2', validators=[DataRequired()])
    user3 = StringField('User3', validators=[DataRequired()])
    user4 = StringField('User4', validators=[DataRequired()])
    user5 = StringField('User5', validators=[DataRequired()])
    submit_button = SubmitField('Submit Form')


class EventForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    date = DateField("Date", format='%Y-%m-%d', validators=[DataRequired()])
    time = TimeField("Time", validators=[DataRequired()])
    location_id = IntegerField("Location ID", validators=[DataRequired()])
    cphone = StringField("Contact Phone", validators=[DataRequired()])
    cemail = StringField("Contact Email", validators=[DataRequired(), Email()])
    restriction = SelectField("Restriction", coerce=int)
    submit_button = SubmitField('Submit Form')


class PhotoForm(FlaskForm):
    univid = SelectField("University", coerce=int)
    photo = FileField("Images", validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    submit_button = SubmitField('Submit Form')


class RatingForm(FlaskForm):
    rating = RadioField("Rating", choices=[
        (i, str(i)) for i in range(1, 6)], coerce=int)
    submit_button = SubmitField("Submit Rating")


class CommentForm(FlaskForm):
    comment = TextAreaField("Comment")
    submit_button = SubmitField("Submit Comment")
