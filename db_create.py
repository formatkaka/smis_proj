from app import db, app

from config import SQLALCHEMY_DATABASE_URI

# print SQLALCHEMY_DATABASE_URI

# app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db.create_all()