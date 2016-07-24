from flask.ext.restful import abort
from flask.ext.restful import Resource

from .models import User, Posts

from flask import make_response

class Testing(Resource):

	""" Test if server is up """

	def get(self):
		message = '<h1> Hello, world ..Server is working </h1>'
		response = make_response(message)
		response.headers['content-type'] = 'text/html'
		return response

	def post(self):
		pass

	def put(self);
		pass

	def delete(self):
		pass

class UserLogin(Resource):
	""" User Registration/Login and change password """

	def get()
