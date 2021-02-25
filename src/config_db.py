from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://root@localhost/hugo_prueba"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    admin = db.Column(db.Boolean)

    def __init__(self, username, password, email, admin):
        self.username = username
        self.password = password
        self.email = email
        self.admin = admin

"""Agregar Tablas"""

db.create_all()

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password", "email", "admin")

"""Agregar Esquemas de tablas"""

user_schema = UserSchema()
users_schema = UserSchema(many=True)