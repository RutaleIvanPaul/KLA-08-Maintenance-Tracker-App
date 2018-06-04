from flask import Flask, jsonify, abort, make_response, request

NOT_FOUND = 'Not found'
BAD_REQUEST = 'Bad request'

app = Flask(__name__)

#create list of users
users = [
    {
        'userID':1,
        'username':'Ivan',
    },
    {
        'userID':2,
        'username':'Paul',
    },
    {
        'userID':3,
        'username':'Rutale',
    },
     {
        'userID':4,
        'username':'Francis',
    }
]

#logged in users
loggedIn = [2,4]

#user requests
user_requests = [
    {
        'id': 1,
        'userID':2,
        'title': 'laptop screen blacked out',
        'description':'the screen just suddenly blacked out'
    },
     {
        'id': 2,
        'userID':4,
        'title': 'phone screen cracked',
        'description':'the phone fell down'
    },
     {
        'id': 3,
        'userID':3,
        'title': 'pc over heat',
        'description':'pc over heats even on low activity'
    },
]


def _get_request(id):
    '''Get user request basing on request id'''
    return [user_request for user_request in user_requests if user_request['id'] == id]

def _get_all_user_requests(userID):
    '''Get user requests basing on user id'''
    return [user_request for user_request in user_requests if user_request['userID'] == userID]

def _record_exists(title):
    '''Check whether request exists'''
    return [user_request for user_request in user_requests if user_request['title'] == title]

def is_logged_in(id):
    '''Check if user is logged in'''
    if id in loggedIn:
        return True
    else:
        return False

@app.errorhandler(404)
def not_found(error):
    '''Customised error message for 404 status code'''
    return make_response(jsonify({'error': NOT_FOUND}), 404)


@app.errorhandler(400)
def bad_request(error):
    '''Customised error message for 400 status code'''
    return make_response(jsonify({'error': BAD_REQUEST}), 400)


@app.route('/api/v1/requests/<int:userid>', methods=['GET'])
def get_all_requests(userid):
    '''Get all requests for given user id'''
    if is_logged_in(userid):
        logged_in_user_requests = _get_all_user_requests(userid)
        return jsonify({'requests': logged_in_user_requests}), 200
    else:
        return jsonify({'error':'User is not logged in'}), 404

@app.route('/api/v1/requests/<int:userid>/<int:requestid>', methods=['GET'])
def get_particular_request(userid,requestid):
    '''Get particular request for given user basing on request id'''
    if is_logged_in(userid):
        particular_request = _get_request(requestid)
    if not particular_request:
        abort(404)
    return jsonify({'request': particular_request})


@app.route('/api/v1/requests', methods=['POST'])
def create_request():
    '''Create new user request'''
    if not request.json or 'title' not in request.json or 'description' not in request.json:
        abort(400)
    user_request_id = user_requests[-1].get("id") + 1
    userID = request.json.get('userID')
    title = request.json.get('title')
    description = request.json.get('description')

    if _record_exists(title):
        abort(400)

    if type(title) is not str:
        abort(400)
    
    if type(description) is not str:
        abort(400)
        
    user_request = {"id": user_request_id,"userID":userID, "title": title,
            "description": description}
    user_requests.append(request)
    return jsonify({'request': user_request}), 201


@app.route('/api/v1/requests/<int:id>', methods=['PUT'])
def modify_request(id):
    '''Modify existing request'''
    user_request = _get_request(id)
    if len(user_request) == 0:
        abort(400)

    if not request.json:
        abort(400)

    title = request.json.get('title')
    description = request.json.get('description')

    if title:
        if type(title) is not str:
            abort(400)
        else:
            user_requests[id]['title'] = title
    
    if description:
        if type(description) is not str:
            abort(400)
        else:
            user_requests[id]['description'] = description

    return jsonify({'request': user_requests[id]}), 200


if __name__ == '__main__':
    app.run(host="localhost", port=8085, debug=True)