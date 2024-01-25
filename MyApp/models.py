from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)

class Incident(db.Model):
    __tablename__ = 'incidents'
    incident_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    accused = db.Column(db.String(255), nullable=False)
    victim = db.Column(db.String(255), nullable=False)
    reported_by = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False)
