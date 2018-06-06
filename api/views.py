from flask import jsonify, abort, make_response, request
from api import app
from .models import User
from .models import Request
from .DatabaseConnection import DatabaseConnection

NOT_FOUND = 'Not found'
BAD_REQUEST = 'Bad request'
n =User(1,'Ivan','admin','loggedin')
@app.errorhandler(404)
def not_found(error):
    '''Customised error message for 404 status code'''
    return make_response(jsonify({'error': NOT_FOUND}), 404)


@app.errorhandler(400)
def bad_request(error):
    '''Customised error message for 400 status code'''
    return make_response(jsonify({'error': BAD_REQUEST}), 400)

@app.route('/api/v1/requests', methods=['POST'])
def signup():

@app.route('/api/v1/requests/<int:userid>', methods=['GET'])
def get_all_requests(userid):
    '''Get all requests for given user id'''
    if User.is_logged_in(userid):
        logged_in_user_requests = Request._get_all_user_requests(userid)
        return jsonify({'requests': logged_in_user_requests}), 200
    else:
        return jsonify({'error':'User is not logged in'}), 404

@app.route('/api/v1/requests/<int:userid>/<int:requestid>', methods=['GET'])
def get_particular_request(userid,requestid):
    '''Get particular request for given user basing on request id'''
    if User.is_logged_in(userid):
        particular_request = Request._get_request(requestid)
    if not particular_request:
        abort(404)
    return jsonify({'request': particular_request})

@app.route('/api/v1/requests', methods=['GET'])
def get_all_requests_on_application():
    '''Get all requests from the database'''
    return jsonify({'request': Request._get_request('get_all')})


@app.route('/api/v1/requests', methods=['POST'])
def create_request():
    '''Create new user request'''
    if not request.json or 'title' not in request.json or 'description' not in request.json:
        abort(400)

    userID = request.json.get('userID')
    title = request.json.get('title')
    description = request.json.get('description')

    if type(title) is not str:
        return make_response(jsonify({'error': BAD_REQUEST+":Title should be a string" }), 400)
    
    if type(description) is not str:
        return make_response(jsonify({'error': BAD_REQUEST+":Description should be a string" }), 400)

    if Request._record_exists(title):
        return make_response(jsonify({'error': BAD_REQUEST+":Request already exists" }), 400)

    Request._create_request(str(userID),title,description)
    user_request = {"userID":userID, "title": title,
                "description": description}
    return jsonify({'request': user_request}), 201


@app.route('/api/v1/requests/<int:id>', methods=['PUT'])
def modify_request(id):
    '''Modify existing request'''
    if not request.json:
         return make_response(jsonify({'error': BAD_REQUEST+":Request object is not JSON" }), 400)

    title = request.json.get('title')
    description = request.json.get('description')

    if title:
        if type(title) is not str:
            return make_response(jsonify({'error': BAD_REQUEST+":Title should be a string" }), 400)
        else:
            Request._modify_request(id,'title',title)
    
    if description:
        if type(description) is not str:
            return make_response(jsonify({'error': BAD_REQUEST+":Description should be a string" }), 400)
        else:
            Request._modify_request(id,'description',description)

    return jsonify({'request': "Successfully modified"}), 200


@app.route('/api/v1/requests/<int:id>/<string:status>', methods=['PUT'])
def change_request_status(id,status):
    if status=="approve" or status=="resolve" or status == "disapprove":
        Request._modify_request(id,'status',status)
        return jsonify({'request': "Successfully modified"}), 200
    else:
        return make_response(jsonify({'error': BAD_REQUEST+":Keyword supplied for this endpoint is wrong" }), 400)

    