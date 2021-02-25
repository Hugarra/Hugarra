from flask import Flask, jsonify, request
from sqlalchemy import text
from config_db import app, db, user_schema, users_schema, User
import secrets

token = secrets.token_urlsafe()
print("Current token: " + token)

@app.route("/users", methods=["POST"])
def create_user():
    username = request.json["username"]
    password = request.json["password"]
    email = request.json["email"]
    admin = False

    if(not username or not password or not email):
        return jsonify({
            "message" : "Not username or password or email"
        })

    new_user = User(username, password, email, admin)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "New user created: " + username,
        "token": token
    })

@app.route("/login", methods=["POST"])
def login_user():
    username = request.json["username"]
    password = request.json["password"]

    if(not username or not password):
        return jsonify({
            "message" : "Not username or password"
        })


    sql_query = text("SELECT * FROM hugo_prueba.usuarios where username='" + username + "' AND password='" + password + "'")
    user_query = db.engine.execute(sql_query)

    result = users_schema.dump(user_query)

    if not result:
        return jsonify({
            "message" : "El usuario " + username + " no ha sido encontrado... usuario o contraseña incorrecta.",
            "status" : "error"
        })

    return jsonify({
        "message" : "El usuario " + username + " ha sido encontrado perfectamente!",
        "user" : result,
        "token" : token,
        "status" : "success"
    })
    



@app.route("/users")
def get_users():
    """all_users = User.query.all()"""
    sql_query = text("SELECT * FROM hugo_prueba.usuarios")
    all_users = db.engine.execute(sql_query)

    result = users_schema.dump(all_users)

    num_users = User.query.count()

    return jsonify({
        "users" : result,
        "count" : num_users
    })

@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    if not user:
        return jsonify({
            "message" : "usuario no encontrado..."
        })

    return jsonify({"message" : "User deleted: " + user})

if __name__ == "__main__":
    app.run(debug=True)