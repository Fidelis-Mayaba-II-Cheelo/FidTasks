from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from flask_login import LoginManager
from flask_mail import Mail
from fidtasks.config import Config


#Creating sql instance
db = SQLAlchemy()

#Password Hashing
bcrypt = Bcrypt()

#Login functionality
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

#Mail functionality
mail = Mail()



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from fidtasks import models
    from fidtasks.users.routes import users
    from fidtasks.goals.routes import goals
    from fidtasks.tasks.routes import tasks
    from fidtasks.main.routes import main
    from fidtasks.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(goals)
    app.register_blueprint(tasks)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app


