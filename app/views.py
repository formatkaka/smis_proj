from flask.ext.restful import abort
from flask.ext.restful import Resource

from .models import User, Posts

from flask import make_response, request, jsonify

from app import api, app

from input_schemas import user_input, post_input

from helper import *

# print 'running'

class Testing(Resource):

	""" Test if server is up """

	def get(self):
		message = '<h1> Hello, world ..Server is working </h1>'
		response = make_response(message)
		response.headers['content-type'] = 'text/html'
		return response

	def post(self):
		pass

	def put(self):	
		pass

	def delete(self):
		pass

class UserLogin(Resource):
	""" User Registration/Login and change password """

	
	def get(self):
		""" Generate token for new user """
		user = get_current_user()
		token = user.gen_auth_token(60)
		return jsonify({'token':str(token)})

	def post(self):
		""" Register a new user """

		user = request.authorization

		if not user:
			abort(400, message="Invalid Request")

		email = user.username
		password_hash = user.password

		json_data = request.get_json()
		# return json_data
		data, errors = user_input.load(json_data)

		if not email or not password_hash:
			abort(400, message="Data missing")

		User.unique_email(email)

		### Add user to database ###
		User.add_user(email=email, password_hash=password_hash, name=data.fullname)

		return jsonify({'status':'true'})

@app.route('/sid')
def hello():
	return 'Hello, World!'

api.add_resource(Testing,'/a')
api.add_resource(UserLogin,'/login')

# if __name__ == "__main__":
# 	app.run(debug=True)