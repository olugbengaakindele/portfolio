from email.policy import default
from tokenize import String
from flask_wtf import FlaskForm
from wtforms import DateField, FloatField,IntegerField,BooleanField, SelectField,StringField,SubmitField,DecimalField, EmailField,PasswordField, TextAreaField
from wtforms.validators import DataRequired, EqualTo,ValidationError,Email, Length
from app.expense.models import Users

def email_exist(form, field):
    email = Users.query.filter_by(user_email = field.data).first()
    if email:
        raise ValidationError("User already exist please go to login")

def email_exist(form, field):
    email = Users.query.filter_by(user_email = field.data).first()
    if email:
        raise ValidationError("User already exist please go to login")

class LoginForm(FlaskForm):

    email = EmailField("Email", validators=[DataRequired()])
    password= PasswordField("Password", validators=[DataRequired()])
    submit= SubmitField("Submit")
    stay_logged_in = BooleanField("Rememeber me")

class RegForm(FlaskForm):
    username= StringField("User Name",validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(),Email(),email_exist])
    password=PasswordField("Password",validators=[DataRequired(), Length(min= 2, max = 20),EqualTo('confirm_password',"Password must match")])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField('Submit')


class ExpenseForm(FlaskForm):

    item =SelectField("Record type", choices= [("Expense","Expense"),("Income","Income")], validators=[DataRequired()])
    cate= SelectField("Category", validators=[DataRequired()])
    amt =DecimalField("Amount", places=2,validators=[DataRequired()])
    date = DateField("Date", validators=[DataRequired()])
    comment  = TextAreaField("Comment")
    submit= SubmitField("Submit")

class EditExpenseForm(FlaskForm):

    item =StringField("Item",validators=[DataRequired()])
    cate= StringField("Category",validators=[DataRequired()])
    # amt = IntegerField("Amount", validators=[DataRequired()])
    amt= FloatField("Amount",places = 2,validators=[DataRequired()])
    date =DateField("Date", validators=[DataRequired()])
    comment  = TextAreaField("Comment")
    submit= SubmitField("Submit")

class SettingsForm(FlaskForm):
    record_type = SelectField("Choose type",choices=[("Income","Income"),("Expense","Expense")])
    category = StringField("Enter a category", validators=[DataRequired()])
    submit = SubmitField("Submit")

class DeleteForm(FlaskForm):
    submit = SubmitField("Delete")

