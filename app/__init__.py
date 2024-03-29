from operator import concat
import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


bootstrap = Bootstrap()
db= SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'expense.do_the_login'
login_manager.session_protection = 'strong'

def create_app(config):

    app= Flask(__name__)
    configuration=os.path.join(os.getcwd(),'config' ,config +".py")
    
    app.config.from_pyfile(configuration)

    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    bcrypt.init_app(app)


    from app.expense import expense
    app.register_blueprint(expense)


    return app

