############# init file ############

from flask_restful import Api
from flask import Flask

from flask.ext.sqlalchemy import SQLAlchemy

from flask.ext.mail import Mail

from flask.ext.script import Manager
from flask.ext.migrate import Migrate,MigrateCommand

from flask.ext.bootstrap import Bootstrap

#### Instantiate app ####

app = Flask(__name__)

#### configurations #### 

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/mydb'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://rxhordwqbwphri:3PUkwCBHdtLm5DpSYzHnbrhVhY@ec2-54-225-244-221.compute-1.amazonaws.com:5432/dflfqtkdleo3eb'

app.config['SECRET_KEY'] = 'too_easy_to_guess_supertramp-sid'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

## email config ###
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'collegeconnect'
app.config['MAIL_PASSWORD'] = 'collegeconnect1234'


print 'init'
db = SQLAlchemy(app)
api = Api(app)
mail = Mail(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
bootstrap = Bootstrap(app)

from app import views, models

