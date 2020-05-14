from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, Form, TextAreaField, RadioField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


class SignupForm(FlaskForm):
    """User Signup Form."""
    full_name = StringField('full_name', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired(),Length(min=6, message='username should have more thant 6 car.'),DataRequired()])
    email = StringField('Email', validators=[Length(min=6),Email(message='Enter a valid email.'),DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=6, message='Select a stronger password.')])
    confirm = PasswordField('Confirm Your Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """User Login Form."""
    email = StringField('Email', validators=[DataRequired(), Email(message='Enter a valid email.')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class SearchForm(FlaskForm):
    search = StringField('search', validators=[DataRequired()])
    submit = SubmitField('search')

class ReviewForm(FlaskForm):
    review = TextAreaField('Add a Review', validators=[DataRequired(), Length(min=6, message='enter a valid review')])
    rating = RadioField ('Please Rate this Book',choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5') ],validators=[DataRequired('Please Select a rate.')])
    submit = SubmitField('Post')

    def getFields(self):
        """Returns both the textfield and ratefield data"""
        return self.textfield.data, self.ratefield.data

'''
class searchForm(FlaskForm):
    """User Login Form."""
    search = StringField('search', validators=[DataRequired(), search(message='title, year, author or isbn.')])
    submit = SubmitField('search')
'''