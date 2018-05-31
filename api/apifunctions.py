from flask import Flask, jsonify, abort, make_response, request

NOT_FOUND = 'Not found'
BAD_REQUEST = 'Bad request'

app = Flask(__name__)

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

loggedIn = [2,4]

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
    return [user_request for user_request in user_requests if user_request['id'] == id]

def _get_all_user_requests(userID):
    return [user_request for user_request in user_requests if user_request['userID'] == userID]

def _record_exists(title):
    record = [user_request for user_request in user_requests if user_request["title"] == title]

def is_logged_in(id):
    if id in loggedIn:
        return True
    else:
        return False

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': NOT_FOUND}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': BAD_REQUEST}), 400)


@app.route('/api/v1/requests/<int:userid>', methods=['GET'])
def get_all_requests(userid):
    if is_logged_in(userid):
        logged_in_user_requests = _get_all_user_requests(userid)
        return jsonify({'requests': logged_in_user_requests}), 200
    else:
        return jsonify({'error':'User is not logged in'}), 404

@app.route('/api/v1/requests/<int:userid>/<int:requestid>', methods=['GET'])
def get_particular_request(userid,requestid):
    if is_logged_in(userid):
        particular_request = _get_request(id)
    if not particular_request:
        abort(404)
    return jsonify({'request': particular_request})


@app.route('/api/v1/requests', methods=['POST'])
def create_request():
    if not request.json or 'title' not in request.json or 'description' not in request.json:
        abort(400)
    user_request_id = user_requests[-1].get("id") + 1
    userID = request.json.get('userID')
    title = request.json.get('title')
    description = request.json.get('description')

    if _record_exists(title):
        abort(400)

    if type(description) is int:
        abort(400)
    user_request = {"id": user_request_id,"userID":userID, "title": title,
            "description": description}
    user_requests.append(request)
    return jsonify({'request': user_request}), 201


@app.route('/api/v1/requests/<int:id>', methods=['PUT'])
def modify_request(id):
    user_request = _get_request(id)
    if len(user_request) == 0:
        abort(404)
    if not request.json:
        abort(400)
    title = request.json.get('title', user_requests[id]['title'])
    description = request.json.get('description', user_requests[id]['description'])
    if type(description) is int:
        abort(400)
    user_requests[id]['title'] = title
    user_requests[id]['description'] = description
    return jsonify({'request': user_requests[id]}), 200


if __name__ == '__main__':
    app.run(host="localhost", port=8085, debug=True)