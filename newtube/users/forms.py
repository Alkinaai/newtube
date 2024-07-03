from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length,Email, EqualTo
from newtube.models import User
from flask_login import current_user



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[ DataRequired(), Length(min=2)])
    email = StringField('Email', validators=[DataRequired(), Email()] )
    password = PasswordField('Password', validators=[ DataRequired()], id='password' )
    confirm_password = PasswordField('Password Confirm', validators=[DataRequired(), EqualTo('password')], id='confirm_password')
    show_password = BooleanField('Show Password', id='check')
    
    submit = SubmitField('Sing Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already taken! choose different one')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already associated with an existing account!')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()] )
    password = PasswordField('Password', validators=[DataRequired()], id='password')
    show_password = BooleanField('Show Password', id='check')
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    



class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[ DataRequired(), Length(min=2)])
    email = StringField('Email', validators=[DataRequired(), Email()] )
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png','gif','TIFF'])])

    submit = SubmitField('Update')
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is already taken! choose different one')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email is already associated with an existing account!')
 
 
            
class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()] )
    submit = SubmitField('Request Password Reset') 
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first!')



class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[ DataRequired()], id='password' )
    confirm_password = PasswordField('Password Confirm', validators=[DataRequired(), EqualTo('password')], id='confirm_password')
    show_password = BooleanField('Show Password', id='check')
    submit = SubmitField('Reset Password')