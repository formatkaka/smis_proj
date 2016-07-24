from flask.ext.restful import abort
from flask.ext.restful import Resource

from .models import User, Posts

from flask import make_response, request, jsonify

from app import api, app

from input_schemas import user_input, post_input
from output_schemas import post_output

from helper import *

import itertools

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
		return jsonify({'status':User.add_user(email=email, password_hash=password_hash, name=data.fullname)})

		# return jsonify({'status':'true'})

class FollowFriend(Resource):
	""" Follow , unfollow """

	def get(self, user_id=None):
		pass

	def post(self, user_id):
		user = get_current_user()
		user.follow(user_id)
		return jsonify({'status':'true'})

	def put(self, user_id):
		pass

	def delete(self, user_id):
		user = get_current_user()
		user.unfollow(user_id)
		return jsonify({'status':'true'})

class UserPosts(Resource):
	""" Fetch and update Posts """

	def get(self):
		
		user = get_current_user()

		_posts = [f_user.userPosts for f_user in user.followingUser]

		posts = itertools.chain(*_posts)
		print list(posts)
		# return jsonify({'status':'trhue'})
		print post_output.dump(list(posts))


	def post(self):

		user = get_current_user()

		json_data = request.get_json()
		data, errors = post_input.load(json_data)

		if errors:
			abort(400)

		user.post_status(data.post_content)
		return jsonify({'status':'true'})

@app.route('/sid')
def hello():
	return 'Hello, World!'

api.add_resource(Testing,'/a')
api.add_resource(UserLogin,'/login')
api.add_resource(FollowFriend,'/following/<string:user_id>')
api.add_resource(UserPosts, '/post')
# if __name__ == "__main__":
# 	app.run(debug=True)