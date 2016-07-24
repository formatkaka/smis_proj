from app import db

from .models import User

from flask import request

from flask.ext.restful import abort

def get_current_user():
	_user = request.authorization

	if not _user:
		abort(400, message="Invalid request")

	else:
		if not _user.username or not _user.password:
			abort(400, message="Empty headers auth")

		email_or_token = _user.username
		password = _user.password

		if password == "None":
			return User.verify_auth_token(email_or_token)

		else:
			return User.check_user(email_or_token, password)

