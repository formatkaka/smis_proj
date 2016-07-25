from flask.ext.restful import abort
from flask.ext.restful import Resource

from .models import User, Posts

from flask import make_response, request, jsonify

from app import api, app

from input_schemas import user_input, post_input, foll_input
from output_schemas import post_output, UsersClass, user_list_output
from output_schemas import UserList, user_schema, PostsClass

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

		token = User.add_user(email=email, password_hash=password_hash, name=data.fullname)

		### Add user to database ###
		return jsonify({'token':token})

		# return jsonify({'status':'true'})

class FollowFriend(Resource):
	""" Follow , unfollow """

	def get(self):
		user = get_current_user()
		users_list = User.query.all()
		users_list.remove(user)

		users = []

		for u in users_list:
			uC = UsersClass(u.fullName, u.id)
			users.append(uC)

		_following = [f_user.id for f_user in user.followingUser]
		# print users, _following
		# print user_schema.dump(users)[0]
		# final_obj = UserList(users=users, following=_following) 
		final_obj = dict(users=users, following=_following)
		data, errors = user_list_output.dump(final_obj)
		# print data, errors
		return data

	def post(self):
		user = get_current_user()
		json_data = request.get_json()
		data, errors = foll_input.load(json_data)			
		user.follow(data.user_id)
		return jsonify({'status':'true'})

	def put(self):
		pass

	def delete(self):
		user = get_current_user()
		json_data = request.get_json()
		data, errors = foll_input.load(json_data)	
		user.unfollow(data.user_id)
		return jsonify({'status':'true'})

class UserPosts(Resource):
	""" Fetch and update Posts """

	def get(self):
		
		user = get_current_user()

		__posts = [f_user.userPosts for f_user in user.followingUser]

		_posts = list(itertools.chain(*__posts))
		
		posts = []

		for _p in _posts:
			obj = PostsClass(_p.postContent, _p.timePosted, 
				 _p.userId)
			posts.append(obj)
		# raise OverflowError
		# return jsonify({'status':'trhue'})
		return post_output.dump(posts)[0]


	def post(self):

		user = get_current_user()

		json_data = request.get_json()
		data, errors = post_input.load(json_data)

		if errors:
			abort(400)

		user.post_status(data.post_content)
		return jsonify({'status':'true'})

	def put(self):
		pass

	def delete(self):
		pass


api.add_resource(Testing,'/')
api.add_resource(UserLogin,'/login')
api.add_resource(FollowFriend,'/follow')
api.add_resource(UserPosts, '/post')
