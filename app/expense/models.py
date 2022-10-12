# app/user/models

from datetime import datetime
from app import db 
from app import bcrypt

class Users(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer,primary_key =True)
    user_email = db.Column(db.String(100), nullable = False)
    user_password = db.Column(db.String(100), nullable = False)
    user_name = db.Column(db.String(100), nullable = False)
    date_signup = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self,user_email,user_name,user_password ):
        self.user_email = user_email
        self.user_name= user_name
        self.user_password =user_password
    def __repr__(self):
        return "Thanks for creating an account"

    @classmethod
    def createUser(cls, email,password,name):
        user = cls(user_email=email, 
                    user_password=bcrypt.generate_password_hash(password).decode("utf-8"),
                    user_name = name
                )
        db.session.add(user)
        db.session.commit()

        return user
    

class Expense(db.Model):
    __tablename__ = 'expenses'

    expense_id = db.Column(db.Integer,primary_key =True)
    expense_name = db.Column(db.String(100), nullable = False)
    expense_category= db.Column(db.String(100), nullable = False)
    expense_amount = db.Column(db.Float, nullable = False)
    expense_date= db.Column(db.DateTime, nullable = False)
    expense_comment = db.Column(db.String(200),nullable = True)
    expense_user_id= db.Column(db.Integer,db.ForeignKey('users.user_id'))

    def __init__(self, expense_name, expense_category,expense_amount,expense_date,expense_comment,expense_user_id):
        self.expense_name=expense_name
        self.expense_category= expense_category
        self.expense_amount = expense_amount
        self.expense_date= expense_date
        self.expense_comment= expense_comment
        self.expense_user_id = expense_user_id
    
    def __repr__(self):
        return "A record has been created"
