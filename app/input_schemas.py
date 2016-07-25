from marshmallow import fields, Schema, post_load


##### User Registration Class #####

class UserRegClass(object):
	""" User Registration """

	def __init__(self, fullname):
		self.fullname = fullname

class UserReg(Schema):
	fullname = fields.Str()

	@post_load
	def make_user(self, data):
		return UserRegClass(**data)

##### Posts json by user #####

class PostsRegClass(object):
	""" Posts by user """

	def __init__(self, post_content):
		self.post_content = post_content

class PostsReg(Schema):
	post_content = fields.Str()

	@post_load
	def make_post(self, data):
		return PostsRegClass(**data)

##### Follow , unfollow user_id #####

class UserFollClass(object):

	def __init__(self, user_id):
		self.user_id = user_id

class UserFoll(Schema):
	user_id = fields.Int()

	@post_load
	def make_foll(self, data):
		return UserFollClass(**data)

user_input = UserReg()
post_input = PostsReg() 
foll_input = UserFoll()