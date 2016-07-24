from app import db

from .models import User

from flask import request

from flask.ext.restful import abort

from datetime import datetime

###########################
#### HELPER FUNCTIONS #####
###########################


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


def conv_time(unixstamp_or_datetime):
    if unixstamp_or_datetime is None:
        return None


    if isinstance(unixstamp_or_datetime, datetime):
        try:
            return time.mktime(unixstamp_or_datetime.timetuple())
        except OverflowError:
            return None
    else:
        return datetime.fromtimestamp(unixstamp_or_datetime)