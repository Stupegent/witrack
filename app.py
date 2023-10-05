from flask import Flask,render_template,flash,url_for,redirect,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,TextAreaField,FileField,EmailField
from flask_wtf.file import  FileAllowed
from wtforms.validators import InputRequired, Length,DataRequired,Email
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676df8o#5(z^p@kjakwtw-'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///netfer.db'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)



class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    logo_url = db.Column(db.String(200), nullable=True)



class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

class Solution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    photo_url = db.Column(db.String(200), nullable=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.Text, nullable=True)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)




class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=80)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=120)])
    submit = SubmitField('Login')


class ClientForm(FlaskForm):
    label = "client"
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
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



@app.route("/",methods = ['GET','POST'])
def Home():
    teammems = TeamMember.query.all()
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        subject  = form.subject.data
        message = form.message.data
        contact = Contact(name=name,email=email,subject=subject,message=message)
        send_email(subject=subject,email=email,message=message)
        print("hello123")
        
    return render_template('home.html',teammems = teammems,form=form)





@app.route("/witrack/")
def witrack():
    return render_template("witrackPlatform.html")




@app.route("/smsdz/")
def smsDz():
    return render_template("smsDz.html")




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print(request.endpoint)
    print(form.validate_on_submit())
    print(form.username.data, form.password.data)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print("saalam")
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            print("saalam2")
            flash('Logged in successfully.', 'success')
            return redirect(url_for('dashboard'))
        else:
            print("saalam3")
            flash('Login failed. Please check your username and password.', 'danger')
    return render_template('login.html', form=form)


@app.route('/team/', methods = ["GET","POST"])
@login_required
def team():
    form2= TeamMemberForm()
    print(form2.validate_on_submit())
    print(form2.name.data,form2.position.data,form2.bio.data,form2.photo.data)
    if form2.validate_on_submit():
        print("salam")
        name = form2.name.data
        position = form2.position.data
        bio = form2.bio.data
        filename = save_picture(form2.photo.data,form2.name.data,folder ="team")
        photo_url = filename
        new_client = TeamMember(name=name, position=position, photo_url=photo_url,bio=bio)
        db.session.add(new_client)
        db.session.commit()
        flash('Team member created successfully', 'success')
        return redirect(url_for('dashboard'))

    return render_template('dashboard/teamForm.html', form2 = form2)

@app.route('/dashboard/', methods = ["GET","POST"])
@login_required
def dashboard():
    # Create new client
    form = ClientForm()
    form2 = TeamMemberForm()
    
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        filename = save_picture(form.photo.data,form.name.data,folder = "clients")
        logo_url = filename
        
        new_client = Client(name=name, description=description, logo_url=logo_url)
        db.session.add(new_client)
        db.session.commit()
        flash('Client created successfully', 'success')
        return redirect(url_for('smsDz'))
    

    return render_template('dashboard/formsDashboard.html',form=form,form2=form2 )


@app.route('/profile/', methods = ["GET","POST"])
@login_required
def profile():
    return render_template('dashboard/profile.html')


@app.route('/table/', methods = ["GET","POST"])
@login_required
def clienttab():
    clients  = Client.query.all()
    team = TeamMember.query.all()
    return render_template('dashboard/clientsTable.html',clients = clients,team = team)



GMAIL_EMAIL = 'achourbensouna100@gmail.com'
GMAIL_PASSWORD = 'LMK!@#$5'



@app.route('/email')
def emails():
    return render_template('email/email.html')

@app.route('/send_emails', methods=['POST'])
def send_emails():
    recipient_list = request.form.get('recipient_list').split(',')
    subject = request.form.get('subject')
    message = request.form.get('message')

    try:
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.starttls()
        smtp_server.login(GMAIL_EMAIL, GMAIL_PASSWORD)

        for recipient in recipient_list:
            msg = MIMEMultipart()
            msg['From'] = GMAIL_EMAIL
            msg['To'] = recipient.strip()
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))
            smtp_server.sendmail(GMAIL_EMAIL, recipient.strip(), msg.as_string())

        smtp_server.quit()
        return 'Emails sent successfully!'
    except Exception as e:
        return f'Error: {str(e)}'



@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    # db.create_all()
    print("salem")
    app.run(debug=True)

from PIL import Image
from random import randint
import os


def save_picture(picture , name , folder):

    _, f_ext = os.path.splitext(picture.filename)
    picture_fn = name +str(randint(1,50)) + f_ext
    path = 'static/assets/img/' + folder
    picture_path = os.path.join(app.root_path,path,picture_fn)
    i = Image.open(picture)
    i.save(picture_path)

    return picture_fn




@app.errorhandler(404)
def error_404(error):
    return render_template('erors/404.html'),404





def send_email(subject,email, message):
    try:
        sender_email = "achourbensouna100@gmail.com"
        sender_password = "pkvf fsml fvsb mvpj"
        recipient_email = "achour.bensouna@inttic.dz"
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        SMTP_SERVER = "smtp.gmail.com"
        SMTP_PORT = 587
        # with open('templates/email/email.html', 'r') as template_file:
        #     email_content = template_file.read()
        email_content= f"""
        email: {email}:
        {message}
        """
        msg.attach(MIMEText(email_content, 'html'))
        smtp_server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        smtp_server.starttls()  # Use TLS encryption
        smtp_server.login(sender_email, sender_password)
        smtp_server.sendmail(sender_email, recipient_email, msg.as_string())
        smtp_server.quit()
        return "Email sent successfully!"
    except Exception as e:
        return str(e)