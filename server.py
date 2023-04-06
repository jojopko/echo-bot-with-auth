import sqlite3
import os
from flask import Flask, request, Response

db = sqlite3.connect("app.db", check_same_thread=False)
cursor = db.cursor()
app = Flask(__name__)

PASSWORD = os.getenv("PASSWORD")


@app.route("/check-user")
def check_user():
    args = request.args.to_dict()
    if "user_id" in args.keys():
        query = "SELECT * FROM Users WHERE user_id = ?"
        cursor.execute(query, [args["user_id"]])
        if cursor.fetchone() is not None:
            return Response("Authorized", status=200)
    return Response("Not authorized", status=200)


@app.route("/sign-up")
def sign_up():
    args = request.args.to_dict()
    if all(key in args.keys() for key in ["password", "user_name", "user_id"]):
        if args["password"] == PASSWORD:
            query = "INSERT INTO Users (user_name, user_id) VALUES (?, ?)"
            cursor.execute(query, [args["user_name"], args["user_id"]])
            db.commit()
            return Response("You have successfully registered", status=201)
    return Response("Incorrect password", status=403)


if __name__ == "__main__":
    with open("create_table.sql") as f:
        cursor.execute(f.read())
    app.run(port=5000)
