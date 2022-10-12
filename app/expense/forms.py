from flask_wtf import FlaskForm
from wtforms import StringField,DateField,SubmitField,DecimalField, EmailField,PasswordField
from wtforms.validators import DataRequired, EqualTo,ValidationError,Email, Length
from app.expense.models import Users


def email_exist(form, field):
    email = Users.query.filter_by(user_email = field.data).first()
    if email:
        raise ValidationError("User already exist please go to login")


class LoginForm(FlaskForm):

    email = EmailField("Email", validators=[DataRequired()])
    password= StringField("Password", validators=[DataRequired()])
    submit= SubmitField("Submit")

class RegForm(FlaskForm):
    username= StringField("User Name",validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(),Email(),email_exist])
    password=PasswordField("Password",validators=[DataRequired(), Length(min= 2, max = 20),EqualTo('confirm_password',"Password must match")])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField('Submit')


class ExpenseForm(FlaskForm):

    item = StringField("Item", validators=[DataRequired()])
    cate= StringField("Category", validators=[DataRequired()])
    amt = DecimalField("Amount", validators=[DataRequired()])
    date = DateField("Date", validators=[DataRequired()])
    comment  = StringField("Comment", validators=[DataRequired()])
    submit= SubmitField("Submit")