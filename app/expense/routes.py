from app.expense import expense
from flask import Flask, render_template, request, url_for, flash,redirect
from app.expense.forms import LoginForm, RegForm
from app.expense.models import Users
from app import db

@expense.route("/index")
def home_page():
   
    return render_template("index.html",title='Home', project = "aboutme")




###############Expense Section###########################################################
@expense.route("/expense/login", methods=["GET","POST"])
def login_page():
    form = LoginForm()
    password= None

    # if request.method == "POST":
    #     email = form.email.data
    #     password= form.password.data

    return render_template("login.html",title='login', form= form, project = "expense")



@expense.route("/expense/registration", methods=["GET","POST"])
def expense_reg():
    form = RegForm()
    user_name = None
    user_email=None
    user_password= None

    if form.validate_on_submit():
        user_email=form.email.data
        user_password = form.password.data
        user_name = form.username.data
        Users.createUser(user_email,user_password,user_name)

        flash("You have successfully created and account, thank you")
        return redirect(url_for('expense.login_page'))

    return render_template("Reg.html",title='Register', project = "expense", form= form)



@expense.route("/expense/Tracker", methods=["GET","POST"])
def tracker():

    return render_template("Tracker.html",title='login',  project = "expense")

