from flask import Flask, jsonify, abort, make_response, request
from api import views


if __name__ == '__main__':
    app.run(host="localhost", port=8085, debug=True)