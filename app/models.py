from app import db
from app import app

from flask.ext.restful import abort

from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

import time

# from flask.ext.sqlalchemy import relationship

##### FOLLOWERS TABLE #####


follow = db.Table('follow',
                      db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
                      db.Column('following_id', db.Integer, db.ForeignKey('users.id'))
                      )

#################
#### MODELS #####
#################

class User(db.Model):
    """ User Registration table """

    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    fullName = db.Column(db.String, nullable=False)
    emailId = db.Column(db.String, unique=True, nullable=False)
    passwordHash = db.Column(db.String, nullable=False)
    isVerified = db.Column(db.Boolean, default=False)
    createdTime = db.Column(db.DateTime, default=datetime.now())
    updatedTime = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    userPosts = db.relationship('Posts', backref='author', lazy='dynamic')
    followingUser = db.relationship("User",
                                   secondary=follow,
                                   primaryjoin=(follow.c.follower_id==id),
                                   secondaryjoin=(follow.c.following_id==id), 
                                   backref=db.backref('followers', lazy='dynamic'),
                                   lazy='dynamic'
                                   )

    @staticmethod
    def add_user(**kwargs):
        user = User(emailId=kwargs['email'], passwordHash=kwargs['password_hash'],
                    fullName=kwargs['name'])
        try:
            db.session.add(user)
            db.session.commit()
        except Exception, e:
            print e
            # logging
            db.session.rollback()
            abort(500, message="Internal server error.")
        return user.gen_auth_token()

    # def __repr__(self):
    #     return "Email : {0} , Username : {1} ".format(self.emailId, self.fullName)

    def check_password_hash(self, password_hash):
        return (self.passwordHash == password_hash)

    def gen_auth_token(self, expiration=None):
        s = Serializer(app.config['SECRET_KEY'], expires_in=6000)
        return s.dumps([self.emailId])

    @staticmethod
    def verify_auth_token(token):
        """ Method to check token validity """

        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
            # print data
        except SignatureExpired:
            data = s.loads(token)  # valid token, but expired
        except BadSignature:
            abort(401, message="Invalid token.")  # invalid token

        user = User.query.filter_by(emailId=data[0]).first()

        if not user :
            abort(409, message="Invalid email-id") # avoid un-registered emails.

        return user    

    @staticmethod
    def check_user(email, password):
        user = User.query.filter_by(emailId=email).first()
        if not user:
            abort(401, message="Invalid email-id")
        else:
            if user.passwordHash==password:
                return user
            else:
                abort(401, message="Incorrect password")


    @staticmethod
    def unique_email(email):
        """ Check if email is unique """
        if User.query.filter_by(emailId=email).first():
            abort(409, message="Email ID already registered.")

    def follow(self, following_id):
        """ follow a user """
        f_user = User.query.filter_by(id=following_id).first()
        if not f_user:
            abort(400, message="No user with given id exists")
        self.followingUser.append(f_user)
        try:
            db.session.add(self)
            db.session.commit()
        except Exception, e:
            print e
            db.session.rollback()
            abort(500, message="Internal server error")
            # logging

    def unfollow(self, unfollowing_id):
        """ Unfollow a user """

        uf_user = User.query.filter_by(id=unfollowing_id).first()
        if not uf_user or uf_user not in self.followingUser:
            abort(400, message="Cannot unfollow")
        self.followingUser.remove(uf_user)
        try:
            db.session.add(self)
            db.session.commit()
        except Exception, e:
            print e
            db.session.rollback()
            abort(500, message="Internal server error")
            # logging      

    def post_status(self, status):
        post = Posts(postContent=status)
        self.userPosts.append(post)
        try:
            db.session.add(self)
            db.session.commit()
        except Exception, e:
            print e
            db.session.rollback()
            abort(500)
            # logging    


class Posts(db.Model):
    """ Posts by users """

    __tablename__ = 'posts'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    postContent = db.Column(db.String, nullable=False)
    timePosted = db.Column(db.Float, default=time.time())
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))

    # def __repr__(self):
    #     return "Post : {0} , Timeposted {1}".format(self.postContent, self.timePosted)
