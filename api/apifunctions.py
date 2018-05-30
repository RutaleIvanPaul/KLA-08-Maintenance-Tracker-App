from flask import Flask, jsonify, abort, make_response, request

NOT_FOUND = 'Not found'
BAD_REQUEST = 'Bad request'

app = Flask(__name__)

requests = [
    {
        'id': 1,
        'title': 'laptop screen blacked out',
        'description':'the screen just suddenly blacked out'
    },
     {
        'id': 2,
        'title': 'phone screen cracked',
        'description':'the phone fell down'
    },
     {
        'id': 3,
        'title': 'pc over heat',
        'description':'pc over heats even on low activity'
    },
]


def _get_request(id):
    return [request for request in requests if request['id'] == id]


def _record_exists(title):
    return [request for request in requests if request["title"] == title]


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': NOT_FOUND}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': BAD_REQUEST}), 400)


@app.route('/api/v1.0/requests', methods=['GET'])
def get_requests():
    return jsonify({'requests': requests}), 200


@app.route('/api/v1.0/requests/<int:id>', methods=['GET'])
def _get_request(id):
    request = _get_request(id)
    if not request:
        abort(404)
    return jsonify({'request': request})


@app.route('/api/v1.0/requests', methods=['POST'])
def create_request():
    if not request.json or 'title' not in request.json or 'description' not in request.json:
        abort(400)
    request_id = requests[-1].get("id") + 1
    title = request.json.get('title')
    if _record_exists(title):
        abort(400)
    description = request.json.get('description')
    if type(description) is int:
        abort(400)
    request = {"id": request_id, "title": title,
            "description": description}
    requests.append(request)
    return jsonify({'request': request}), 201


@app.route('/api/v1.0/requests/<int:id>', methods=['PUT'])
def modify_request(id):
    request = _get_request(id)
    if len(request) == 0:
        abort(404)
    if not request.json:
        abort(400)
    title = request.json.get('title', requests[0]['title'])
    description = request.json.get('description', requests[0]['description'])
    if type(description) is int:
        abort(400)
    requests[0]['title'] = title
    requests[0]['description'] = description
    return jsonify({'request': requests[0]}), 200


if __name__ == '__main__':
    app.run(debug=True)