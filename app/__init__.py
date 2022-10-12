from operator import concat
import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt

bootstrap = Bootstrap()
db= SQLAlchemy()
bcrypt = Bcrypt()


def create_app(config):

    app= Flask(__name__)
    configuration=os.path.join(os.getcwd(),'config' ,config +".py")
    
    app.config.from_pyfile(configuration)

    db.init_app(app)
    bootstrap.init_app(app)
    bcrypt.init_app(app)


    from app.expense import expense
    app.register_blueprint(expense)


    return app

