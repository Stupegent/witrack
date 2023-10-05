from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,TextAreaField,FileField,EmailField,SelectField
from flask_wtf.file import  FileAllowed
from wtforms.validators import InputRequired, Length,DataRequired,Email




class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=80)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=120)])
    submit = SubmitField('Login')


class ClientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    email = StringField('Email', validators=[DataRequired()])
    photo = FileField('photo',validators=[DataRequired(),FileAllowed(['jpg','png','svg','jpeg','gif'], "wrong format!")])
    submit = SubmitField('Submit')


class TeamMemberForm(FlaskForm):
    label = "team"
    name = StringField('Name', validators=[DataRequired()])
    position = StringField('Position')
    bio = TextAreaField('Bio')
    photo = FileField('photo',validators=[DataRequired(),FileAllowed(['jpg','png','svg','jpeg','gif'], "wrong format!")])
    submit = SubmitField('Add Team Member')


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    subject  = StringField('Subject' , validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')



class SolutionForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    label= StringField('label', validators=[DataRequired()])
    description = TextAreaField('Description')
    photo = FileField('photo',validators=[DataRequired(),FileAllowed(['jpg','png','svg','jpeg','gif'], "wrong format!")])
    submit = SubmitField('Submit')


class QAForm(FlaskForm):
    question = StringField('Question', validators=[ DataRequired()])
    answer = TextAreaField('Answer', validators=[DataRequired()])
    submit = SubmitField('Submit')



class MailGunForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message',validators=[DataRequired()])
    photo = FileField('photo',validators=[DataRequired(),FileAllowed(['jpg','png','svg','jpeg','gif'], "wrong format!")])
    receipient = SelectField('Receipient',choices=[('client','client'),('team','team')])
    submit = SubmitField('Submit')

