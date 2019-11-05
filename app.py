# Data warehouse integration server
#
# Description:
# Acts as the web entry point to fetch data from warehouses
#
# Author:
# Dylan Watt
#
# Notes:
# All http actions are posts right now as they take sensitive params (credentials), and get params have
# a habit of ending up in server logs.

import os
import json
from flask import Flask, request, jsonify, Response
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

app = Flask(__name__)


@app.route('ping', methods=['GET'])
def ping():
    return Response("pong")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
