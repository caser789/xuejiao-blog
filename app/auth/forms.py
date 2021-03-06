from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, EqualTo, Regexp
from ..models import User
from wtforms import ValidationError



class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[Required(), Length(1, 64)])
    remember_me = BooleanField('Keep me logged in.')
    submit = SubmitField('Log in')

class RegistrationForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username = StringField('Username', validators=[
            Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 
                                              'Usernames must only have'
                                              'letters, numbers, dots or'
                                              'unserscores')])
    password = PasswordField('Password', validators=[Required(), Length(1, 64),
        EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use')

class ChangePasswordForm(Form):
    old_password = PasswordField('Old Password', validators=[Required()])
    password = PasswordField('New Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Upadate Password')

class PasswordResetRequestForm(Form):
    email = StringField('Email', validators=[
        Required(), Length(1, 64), Email()])
    submit = SubmitField('Reset Password')

class PasswordResetForm(Form):
    email = StringField('Email', validators=[
        Required(), Length(1, 64), Email()])
    password = PasswordField('New Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm Password', validators=[
        Required()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unkown email address.')

class ChangeEmailForm(Form):
    email = StringField('New Email', validators=[
        Required(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[
        Required(), Length(1, 64)])
    submit = SubmitField('Update Email Address')
    
    def validate_email(self, filed):
        if User.query.filter_by(email=filed.data).first():
            raise ValidationError('Email already exists.')
