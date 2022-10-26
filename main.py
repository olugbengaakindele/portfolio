from app import create_app,db
from app.expense.models import *
from datetime import datetime

if __name__ == '__main__':
    flask_app =create_app('dev')

    with flask_app.app_context():
        db.create_all()
        if not Users.query.filter_by(user_email ="Akindele@gmail.com").first():
            Users.createUser(email="Akindele@gmail.com",password= "olu",name ="Olu")

        if not Settings.query.filter_by(user_id =1 ).first():
            Settings.newSetting(type="test",category= "test",user_id=1)
        
        if not Expense.query.filter_by(expense_user_id =1 ).first():
            Expense.new_expense( "income","test",0.0,datetime.now(),  "test", 1)
    
    flask_app.run(debug =True)


# from distutils.log import debug
# from flask import Flask,render_template
# from flask_sqlalchemy import SQLAlchemy

# class Users(db.Model):
#     __tablename__ = "users"
#     user_id = db.Column(db.Integer,primary_key = True)
#     username = db.Column(db.String(100),nullable = False)

#     def __init__(self,user_id, username):
#         self.user_id = user_id
#         self.username = username

#     def __repr__(self):
#         return  f"{self.user_id} has been created"

# class Sales(db.Model):
#     __tablename__ = 'sales'

#     sales_id = db.Column(db.Integer,primary_key = True)
#     sales_amount = db.Column(db.Float,nullable = False)
#     user_id = db.Column(db.Integer,db.ForeignKey('users.user_id'))

#     def __init__(self,sales_id,sales_amount,user_id):
#         self.sales_id = sales_id
#         self.sales_amount = sales_amount
#         self.user_id = user_id
    
#     def __repr__(self):
#         return f"{self.sales_id} is created"

# @app.route("/")
# @app.route("/index")
# def home():
#     return render_template("index.html", books = book)


# @app.route("/test")
# def test():
#     return render_template("test.html", data = book)


