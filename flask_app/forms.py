from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import (
    InputRequired,
    DataRequired,
    NumberRange,
    Length,
    Email,
    EqualTo,
    ValidationError,
)

from .models import User

class SearchForm(FlaskForm):
    search_query = StringField(
        "Query", validators=[InputRequired(), Length(min=1, max=100)]
    )
    submit = SubmitField("Search")

class PokeReviewForm(FlaskForm):
    text = TextAreaField(
        "Comment", validators=[InputRequired(), Length(min=5, max=500)]
    )
    submit = SubmitField("Enter Comment")

class PokeInputForm(FlaskForm):
    text = TextAreaField(
        "Comment", validators=[InputRequired(), Length(min=5, max=500)]
    )
    submit = SubmitField("Enter Comment")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=32)])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), Length(min=8, max=32), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")

    def validate_password(self, password):
        if password.data.islower():
            raise ValidationError('Use at least one capital letter in your password.')
        if password.data.isalpha():
            raise ValidationError('Please include at least one number (0-9) or special character (such as # @ $ & among others) in your password')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=40)]) 
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField("Log In")


class UpdateUsernameForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])  

    def validate_username(self, username):        
        strlen =len(username.data)
        if strlen <1 or strlen >40:
            raise ValidationError('Invalid username length')

        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    submit = SubmitField("Update Username")