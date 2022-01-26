from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime
import pytz

app = Flask(__name__)
db = SQLAlchemy()


IST = pytz.timezone('Asia/Kolkata')

class Resources(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    title = db.Column(db.String(128))
    url = db.Column(db.String(128), default=None)
    description = db.Column(db.Text())
    category = db.Column(db.String(128))
    filename = db.Column(db.String(128), default=None)
    link = db.Column(db.String(128), default=None)
    date = db.Column(db.String(64), default=datetime.now(IST).strftime("%d %B %Y, %H:%M %p"))
