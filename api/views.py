from flask import jsonify, abort, make_response, request
from api import app
from .models import User
from .models import Request
from werkzeug.security import generate_password_hash, check_password_hash
import json
import jwt
import datetime
from functools import wraps
from validate_email import validate_email

# from .DatabaseConnection import DatabaseConnection

NOT_FOUND = 'Not found'
BAD_REQUEST = 'Bad request'
app.config['SECRET KEY'] = 'thissecretkey'

def check_string(stringparam):
	'''Check if param is really a string'''
	if type(stringparam) is str:
		return True
	else:
		return False 

def check_string_length(stringparam):
	'''Check if param is an empty string'''
	if len(stringparam.strip())<1:
		return False
	else:
		return True

def token_required(f):
	'''Wraps around methods that will require a token'''
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None
		if 'x-access-token' in request.headers: #Check if request is authorised. 
			token = request.headers['x-access-token']
		try:
			data = jwt.decode(token, str(app.config['SECRET_KEY']))#Decode the data held by token
			userid = str(data["userid"])#retrieve the user id
			current_user = User.getUser(userid)[0]["id"]#Check for that user from the database
		except:
			return jsonify({'message': 'Token is invalid/Has Expired.'})
		return f(current_user,*args,**kwargs)
	return decorated

@app.errorhandler(404)
def not_found(error):
	'''Customised error message for 404 status code'''
	return make_response(jsonify({'error': NOT_FOUND}), 404)


@app.errorhandler(400)
def bad_request(error):
	'''Customised error message for 400 status code'''
	return make_response(jsonify({'error': BAD_REQUEST}), 400)

@app.route('/api/v1/auth/signup', methods=['POST'])
def signup():
	'''Add new user to database'''
	if not request.json or not request.json.get('email') or not request.json.get('password') or not request.json.get('usertype'):
		return make_response(jsonify({'error': BAD_REQUEST+":Request object is not JSON/Missing a value" }), 400)

	if not validate_email(request.json.get('email')):
		return make_response(jsonify({'error': BAD_REQUEST+":Invalid Email" }), 400)

	if not check_string_length(request.json.get('email')):
		return make_response(jsonify({'error': BAD_REQUEST+":email field is empty" }), 400)

	if not check_string_length(request.json.get('password')):
		return make_response(jsonify({'error': BAD_REQUEST+":Password field is empty" }), 400)

	if not check_string_length(request.json.get('usertype')):
		return make_response(jsonify({'error': BAD_REQUEST+":Usertype field is empty" }), 400)

	if request.json.get('usertype') != "admin" and request.json.get('usertype') != "user":
		return make_response(jsonify({'error': BAD_REQUEST+":Usertype should either be user or admin" }), 400)

	try:
		User.createUser(request.json.get('email'),generate_password_hash(request.json.get('password')),request.json.get('usertype'))
		return jsonify({'request': "Successfully Added User"}), 200

	except:
		return make_response(jsonify({'error': BAD_REQUEST+":Could not add user.You're probably missing something." }), 400)


@app.route('/api/v1/auth/logout', methods=['POST'])
@token_required
def logout(current_user):
	'''Change current user status to logged out'''
	if User.logout(current_user,"loggedout"):
		return jsonify({'request': "Successfully Logged Out"}), 200

	else:
		return make_response(jsonify({'error': BAD_REQUEST+":Request on this endpoint has to be either login/signup/logout" }), 400)

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
	'''Change user status to logged in'''
	if not request.json or not request.json.get('email') or not request.json.get('password'):
		return make_response(jsonify({'error': BAD_REQUEST+":Request object is not JSON/Missing a value" }), 400)

	if not validate_email(request.json.get('email')):#Validate the input email
		return make_response(jsonify({'error': BAD_REQUEST+":Invalid Email" }), 400)

	if User.getUserbyEmail(request.json.get('email')):#Check for user basing on email
		userid = User.getUserbyEmail(request.json.get('email'))[0]["id"]
		if User.login(userid,request.json.get('password')):#Check for user basing on password
			token = jwt.encode({'userid': userid, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120)}, str(app.config['SECRET_KEY']))
			return jsonify({'token' : token.decode('UTF-8')}), 200
		else:
			return make_response(jsonify({'error': BAD_REQUEST+":Wrong Password" }), 400)
	else:
		return make_response(jsonify({'error': BAD_REQUEST+":Email does not exist in our database" }), 400)


@app.route('/api/v1/users/requests', methods=['GET'])
@token_required
def get_all_requests(current_user):
	'''Get all requests for given user id'''
	if User.is_logged_in(current_user):
		#return all logged in user requests
		logged_in_user_requests = Request._get_all_user_requests(current_user)
		return jsonify({'requests': logged_in_user_requests}), 200
	else:
		return jsonify({'error':'User is not logged in'}), 404

@app.route('/api/v1/users/requests/<int:requestid>', methods=['GET'])
@token_required
def get_particular_request(current_user,requestid):
	'''Get particular request for given user basing on request id'''
	if User.is_logged_in(current_user):
		particular_request = Request._get_request(requestid)
		#Return Particular request
	if not particular_request:
		abort(404)
	if particular_request[0]["userid"] == current_user:
		return jsonify({'request': particular_request})
	else:
		return make_response(jsonify({'error': BAD_REQUEST+":This user did not make the request" }), 400)

@app.route('/api/v1/requests/', methods=['GET'])
@token_required
def get_all_requests_on_application(current_user):
	'''Get all requests from the database'''
	if User.getUser(current_user)[0]["type"] == "admin":
		#Get all requests from the database
		return jsonify({'request': Request._get_request('get_all')})
	else:
		return make_response(jsonify({'error': BAD_REQUEST+":This user is not an admin" }), 400)


@app.route('/api/v1/users/requests', methods=['POST'])
@token_required
def create_request(current_user):
	'''Create new user request'''
	if not request.json or 'title' not in request.json or 'description' not in request.json:
		abort(400)

	# title = (request.json.get('title').encode()).strip()
	# print(type(title))
	# description = (request.json.get('description').encode()).strip()

	title = request.json.get('title')
	description = request.json.get('description')

	if not check_string(title):
		return make_response(jsonify({'error': BAD_REQUEST+":Title should be a string" }), 400)

	if not check_string(description):
		return make_response(jsonify({'error': BAD_REQUEST+":Description should be a string" }), 400)

	if not check_string_length(title):
		return make_response(jsonify({'error': BAD_REQUEST+":Your title appears to be empty" }), 400)

	if not check_string_length(description):
		return make_response(jsonify({'error': BAD_REQUEST+":Your description appears to be empty" }), 400)

	user_request = Request._create_request(current_user,title,description)

	return jsonify({'request': user_request}), 201


@app.route('/api/v1/users/requests/<int:requestid>', methods=['PUT'])
@token_required
def modify_request(current_user,requestid):
	'''Modify existing request'''
	if not request.json:
		 return make_response(jsonify({'error': BAD_REQUEST+":Request object is not JSON" }), 400)

	# title = (request.json.get('title').encode()).strip()
	# description = (request.json.get('description').encode()).strip()

	title = request.json.get('title')
	description = request.json.get('description')

	if Request._get_request(requestid)[0]["userid"] == current_user and Request._get_request(requestid)[0]["status"] is not "approved":
		if title:
			if type(title) is not str:
				return make_response(jsonify({'error': BAD_REQUEST+":Title should be a string" }), 400)
			else:
				# print(requestid)
				Request._modify_request(requestid,'title',title)


		if description:
			if type(description) is not str:
				return make_response(jsonify({'error': BAD_REQUEST+":Description should be a string" }), 400)
			else:
				# print(type(requestid))
				Request._modify_request(requestid,'description',description)

		return jsonify({'request': "Successfully modified"}), 200

	else:
		return make_response(jsonify({'error': BAD_REQUEST+":Current user did not make this request" }), 400)


@app.route('/api/v1/requests/<int:requestid>/<string:status>', methods=['PUT'])
@token_required
def change_request_status(current_user,requestid,status):
	if User.getUser(current_user)[0]["type"] == "admin":
		if status=="approve":
			if Request._get_request(requestid)[0]["status"] == "pending":
				 Request._modify_request(requestid,'status',status+"d")
				 return jsonify({'request': "Successfully modified"}), 200
			else:
				return make_response(jsonify({'error': BAD_REQUEST+":Request status is not pending" }), 400)

		if status == "disapprove" or status == "resolve":
			if Request._get_request(requestid)[0]["status"] == "pending" or Request._get_request(requestid)[0]["status"] == "approved":
				Request._modify_request(requestid,'status',status+"d")
				return jsonify({'request': "Successfully modified"}), 200
			else:
				return make_response(jsonify({'error': BAD_REQUEST+":Request is not at pending or approved status." }), 400)

		else:
			return make_response(jsonify({'error': BAD_REQUEST+":Keyword supplied for this endpoint is wrong" }), 400)

	else:
		return make_response(jsonify({'error': BAD_REQUEST+":Current user is not an admin" }), 400)
