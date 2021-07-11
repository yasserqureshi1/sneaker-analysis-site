from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Brands(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    link = db.Column(db.String)
    img = db.Column(db.String)
    description = db.Column(db.String)