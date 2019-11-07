from flask import Flask, Response
import logging

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return Response("Welcome Home")


@app.route("ping", methods=["GET"])
def ping():
    return Response("pong")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
