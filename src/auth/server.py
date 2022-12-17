#import jwt
import os
from jsontoken import createJWT
import jwt

from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

#config
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")


@server.route('/login', methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "Missing credentials", 401

        #check db for credentials
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email, password FROM user WHERE email=%s", (auth.username)
    )

    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return "Invalid credentials", 401

        else:
            return createJWT(auth.username, os.environ.get('JWT_SECRET'), True)

    else:
        return "Invalid credentials", 401

#validate JWTs sent within the client
@server.route('/validate', method=['POST'])
def validate():
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "Missing credentials", 401

    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded = jwt.decode(
            encoded_jwt, os.environ.get("JWT_SECRET"), algorithm=["H256"]
        )
    except:
        return "Not authorized", 403

    return decoded, 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)






