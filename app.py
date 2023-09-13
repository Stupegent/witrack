from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)


app.config['SECRET_KEY'] = '5791628bb0b13ce0c676df8o#5(z^p@kjakwtw-'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///netfer.db'


db = SQLAlchemy(app)

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
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)




@app.route("/")
def Home():
    clients = Client.query.all()
    for client in clients:
        print(client.logo_url)
    return render_template('index.html',clients = clients)


if __name__ == "__main__":
    app.run(host='192.168.157.1',debug=True)


@app.route("/witrack/")
def witrack():
    return render_template("witrackPlatform.html")




@app.route("/smsdz/")
def smsDz():
    return render_template("smsDz.html")