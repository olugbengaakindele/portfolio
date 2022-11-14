# app/user/models

from datetime import datetime
from email.policy import default
from unicodedata import category
from app import db 
from app import bcrypt
from app import login_manager
from flask_login import UserMixin


class Users(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key =True)
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

    def check_password(self, password):
        return bcrypt.check_password_hash(self.user_password,password)


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
    expense_user_id= db.Column(db.Integer,db.ForeignKey('users.id'))
    expense_entry_date = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, expense_name, expense_category,expense_amount,expense_date,expense_comment,expense_user_id):
        self.expense_name=expense_name
        self.expense_category= expense_category
        self.expense_amount = expense_amount
        self.expense_date= expense_date
        self.expense_comment= expense_comment
        self.expense_user_id = expense_user_id
    
    @classmethod
    def new_expense(cls,type, cate,amt,date,comment,user_id):
        new_rec = cls(expense_name = type,expense_category =cate,expense_amount = amt, 
                      expense_date = date, expense_comment = comment, expense_user_id = user_id)
        db.session.add(new_rec)
        db.session.commit()

    def __repr__(self):
        return "A record has been created"


class Settings(db.Model):
    __tablename__ = 'settings'

    id = db.Column(db.Integer,primary_key =True)
    type = db.Column(db.String(100), nullable = False)
    category= db.Column(db.String(100), nullable = False)
    date = db.Column(db.DateTime, default= datetime.now())
    user_id= db.Column(db.Integer,db.ForeignKey('users.id'))

    def __init__(self, type,category,user_id):
        self.type=type
        self.category= category
        self.user_id = user_id
            
    def __repr__(self):
        return "A record has been created"

    @classmethod
    def newSetting(cls, type, category, user_id):
        new_record = cls(type=type, category = category, user_id = user_id )
        
        db.session.add(new_record)
        db.session.commit()

        return new_record

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))
