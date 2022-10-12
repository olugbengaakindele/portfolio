#app/users/__init__

from flask import Blueprint


expense = Blueprint('expense',__name__,template_folder = 'templates')

from app.expense import routes