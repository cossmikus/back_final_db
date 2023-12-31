from datetime import datetime, timezone
import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'the_user'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    given_name = db.Column(db.String)
    surname = db.Column(db.String)
    city = db.Column(db.String)
    phone_number = db.Column(db.String)
    profile_description = db.Column(db.String)
    the_password = db.Column(db.String)


@app.route("/api/user", methods=["POST"])
def create_user():
    data = request.get_json()

    user = User(
        user_id=data.get("user_id"),
        email=data.get("email"),
        given_name=data.get("given_name"),
        surname=data.get("surname"),
        city=data.get("city"),
        phone_number=data.get("phone_number"),
        profile_description=data.get("profile_description"),
        the_password=data.get("the_password")
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"user_id": user.user_id, "message": "User created successfully"}), 201


@app.route("/api/users", methods=["GET"])
def get_all_users():
    all_users_data = User.query.all()
    if all_users_data:
        users_list = [
            {
                "user_id": user.user_id,
                "email": user.email,
                "given_name": user.given_name,
                "surname": user.surname,
                "city": user.city,
                "phone_number": user.phone_number,
                "profile_description": user.profile_description,
                "the_password": user.the_password,
            }
            for user in all_users_data
        ]
        return jsonify(users_list)
    else:
        return jsonify({"message": "No users found"}), 404


@app.route("/api/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        # Convert SQLAlchemy model to a dictionary using inspect
        user_data = {column.key: getattr(user, column.key) for column in inspect(User).columns}
        return jsonify(user_data)
    else:
        return jsonify({"message": "User not found"}), 404

@app.route("/api/user/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    user.email = data.get("email", user.email)
    user.given_name = data.get("given_name", user.given_name)
    user.surname = data.get("surname", user.surname)
    user.city = data.get("city", user.city)
    user.phone_number = data.get("phone_number", user.phone_number)
    user.profile_description = data.get("profile_description", user.profile_description)
    user.the_password = data.get("the_password", user.the_password)

    db.session.commit()

    updated_user_data = {
        "user_id": user.user_id,
        "email": user.email,
        "given_name": user.given_name,
        "surname": user.surname,
        "city": user.city,
        "phone_number": user.phone_number,
        "profile_description": user.profile_description,
        "the_password": user.the_password,
    }

    return jsonify({"message": f"User with ID {user_id} updated successfully", "user": updated_user_data})


@app.route("/api/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully", "user_id": user_id})


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", False))
