from datetime import datetime, timezone
import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'THE_USER'
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

    with app.app_context():
        db.session.add(user)
        db.session.commit()

    return jsonify({"user_id": user.user_id, "message": "User created successfully"}), 201

@app.route("/api/users", methods=["GET"])
def get_all_users():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM THE_USER;")
        all_users_data = cursor.fetchall()
        if all_users_data:
            columns = [desc[0] for desc in cursor.description]
            users_list = [dict(zip(columns, user)) for user in all_users_data]
            return jsonify(users_list)
        else:
            return jsonify({"message": "No users found"}), 404

@app.route("/api/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM THE_USER WHERE user_id = %s;", (user_id,))
        user_data = cursor.fetchone()
        if user_data:
            return jsonify(user_data)
        else:
            return jsonify({"message": "User not found"}), 404

@app.route("/api/user/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    with connection.cursor() as cursor:
        data = request.get_json()
        email = data.get("email")
        given_name = data.get("given_name")
        surname = data.get("surname")
        city = data.get("city")
        phone_number = data.get("phone_number")
        profile_description = data.get("profile_description")
        password = data.get("the_password")

        set_clause = []
        if email is not None:
            set_clause.append(f"email = '{email}'")
        if given_name is not None:
            set_clause.append(f"given_name = '{given_name}'")
        if surname is not None:
            set_clause.append(f"surname = '{surname}'")
        if city is not None:
            set_clause.append(f"city = '{city}'")
        if phone_number is not None:
            set_clause.append(f"phone_number = '{phone_number}'")
        if profile_description is not None:
            set_clause.append(f"profile_description = '{profile_description}'")
        if password is not None:
            set_clause.append(f"the_password = '{password}'")

        if set_clause:
            update_query = f"""
                UPDATE THE_USER 
                SET {', '.join(set_clause)} 
                WHERE user_id = %s;
            """
            cursor.execute(update_query, (user_id,))
            if cursor.rowcount > 0:
                return jsonify({"message": f"User with ID {user_id} updated successfully"})
            else:
                return jsonify({"message": "User not found"}), 404
        else:
            return jsonify({"message": "No valid fields provided for update"}), 400

@app.route("/api/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM THE_USER WHERE user_id = %s;", (user_id,))
        if cursor.rowcount > 0:
            return jsonify({"message": "User deleted successfully"})
        else:
            return jsonify({"message": "User not found"}), 404

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", False))
