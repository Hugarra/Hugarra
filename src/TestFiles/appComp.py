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


db.create_all()

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password", "email", "admin")

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route("/users", methods=["POST"])
def create_user():
    username = request.json["username"]
    password = request.json["password"]
    email = request.json["email"]
    admin = request.json["admin"]

    new_user = User(username, password, email, admin)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "New user created: " + username
    })

@app.route("/users")
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify({
        "users" : result,
        "count" : 1
    })

@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message" : "User deleted: " + user})

if __name__ == "__main__":
    app.run(debug=True)