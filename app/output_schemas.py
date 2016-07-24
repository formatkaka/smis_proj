from marshmallow import fields, Schema, post_load, pre_load

from helper import conv_time

#### User list ####

class UsersClass(object):
	def __init__(self, fullName, user_id):
		self.fullName = fullName
		self.user_id = user_id

class UserSchema(Schema):
	fullName = fields.Str()
	user_id = fields.Int()

class UserList(Schema):
	users = fields.Nested(UserSchema, many=True)
	following = fields.List(fields.Int())


#### Posts ####


class PostsSchema(Schema):
	postContent = fields.Str()
	time_posted = fields.Float()
	userId = fields.Int()
	id = fields.Int()

	# @pre_load
	# def process_time(self, data):
	# 	time = conv_time(data.get('timePosted'))
	# 	data['time_posted'] = time
	# 	return data
	# @pre_load
	# def 
post_output = PostsSchema(many=True)
user_list_output = UserList()
user_schema = UserSchema(many=True)