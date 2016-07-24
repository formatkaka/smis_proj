from marshmallow import fields, Schema, post_load, pre_load

from helper import conv_time

#### User list ####

class UserList(Schema):
	fullName = fields.Str()
	id = fields.Int()
	following = fields.Str()


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