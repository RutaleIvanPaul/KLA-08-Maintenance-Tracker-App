# from flask import Flask, jsonify, abort, make_response, request
from api import app


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)
