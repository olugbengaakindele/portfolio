from psycopg2 import Date
from app.expense import expense
from flask import Flask, jsonify, render_template, request, url_for, flash,redirect,json
from app.expense.forms import *
from app.expense.models import Expense, Users,Settings
from flask_login import login_user,login_required,logout_user, current_user
from sqlalchemy.sql import text, func
import pandas as pd
from datetime import date, datetime

from app import db

@expense.route("/index")
def home_page():
   
    return render_template("index.html",title='Home', project = "aboutme")


###############Expense Section###########################################################
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
        return redirect(url_for('expense.do_the_login'))


    return render_template("Reg.html", title='register', project = "expense", form= form)

@expense.route("/expense/login",methods= ["GET","POST"])
def do_the_login():
    form = LoginForm()
    
    

    if form.validate_on_submit():
        password= form.password.data
        email = form.email.data
        user = Users.query.filter_by(user_email =email).first()
        if not user or not  user.check_password(password):
            flash("Invalid credential, please try again",'error')
            return redirect(url_for("expense.do_the_login"))

        login_user(user, form.stay_logged_in.data)
        return redirect(url_for("expense.expense_tracker"))
            

    return render_template("login.html" , title='login', form= form, project = "expense")
            


@expense.route("/expense/tracker", methods=["GET","POST"])
@login_required
def expense_tracker():
    form = ExpenseForm()
    all_cates = Settings.query.filter_by(user_id = current_user.id,type = "income")
    all_user_records = Expense.query.filter_by(expense_user_id = current_user.id).order_by(text("expense_entry_date")).limit(5).all() 
    form.cate.choices = [(ct.category, ct.category) for ct in all_cates]
    
    if request.method == "POST":
        type= form.item.data
        cate= form.cate.data
        amt = form.amt.data
        date = form.date.data
        comment = form.comment.data
        Expense.new_expense(type.lower(),cate.lower(),amt,date,comment, current_user.id)
        flash('A new record has been created')
        return redirect(url_for('expense.expense_tracker'))

    return render_template("tracker.html", title='tracker', form = form , project = "expense" , recent_records=all_user_records)

@expense.route("/expense/settings", methods=["GET","POST"])
@login_required
def expense_settings():
    form = SettingsForm()
    type= form.record_type.data
    category = form.category.data
    user_id = current_user.id
    all_list = False
    all_list = Settings.query.filter_by(user_id= current_user.id).order_by(text("Date desc")).limit(5).all() 

    if form.validate_on_submit():
        Settings.newSetting(type.lower(),category.lower().strip(),user_id)
        all_list = Settings.query.filter_by(user_id= current_user.id).all()
        flash(f"{category} has been added to {type} type")
        return redirect(url_for('expense.expense_settings', all_list = all_list))


    return render_template("settings.html", title='tracker',  form = form, project = "expense", all_list = all_list)

@expense.route("/expense/tracker/addnew", methods= ['GET','POST'])
@login_required
def expense_addNew():
    form = ExpenseForm()

    if form.validate_on_submit():
        flash("You have added a new record")
        return redirect(url_for('expense.epense_addNew'))
    
    return render_template("expense_add_new.html", form = form ,title="Add New Record", project = "expense")


@expense.route("/expense/home", methods=["GET","POST"])
def expense_home():

    return render_template("expense_home.html",title='home',  project = "expense")



@expense.route("/contact", methods=["GET","POST"])
def contact():

    return render_template("Contact.html",title='login',  project = "expense")

@expense.route("/logout")
@login_required
def log_out_user():
    logout_user()

    return render_template("index.html",title='login',  project = "aboutme")

@expense.route("/expense/delete/<cat_id>",methods=["GET","POST"])
@login_required
def delete_cat(cat_id):
    form = DeleteForm()
    cate = Settings.query.filter_by(id = cat_id).first()
    if request.method =="POST":
        db.session.delete(cate)
        db.session.commit()
        
        return redirect(url_for('expense.expense_settings'))
    
    return render_template("delete_cate.html",title='login',  project = "expense", cate = cate , form = form)


@expense.route('/expense/<type_val>')
@login_required
def expense_type(type_val):
    type_Array =[]
    types = Settings.query.filter_by(user_id = current_user.id,type = type_val).all()

    for ty in types:
        tyObj= {}
        tyObj["id"] = ty.id
        tyObj["type"]=ty.type
        tyObj["category"] = ty.category
        tyObj["user_id"] = ty.user_id
        type_Array.append(tyObj)

    return jsonify({'type': type_Array})
        
@expense.route('/allexpense/<user_id>')
@login_required
def all_expense(user_id):
    type_Array =[]
    types = Expense.query.filter_by( expense_user_id= user_id).all()

    for ty in types:
        tyObj= {}
        tyObj["id"] = ty.expense_id 
        tyObj["type"]=ty.expense_name
        tyObj["category"] = ty.expense_category
        tyObj["amount"] = ty.expense_amount
        tyObj["expense_date"] = ty.expense_date.date().strftime("%Y-%m-%d")
        tyObj["comment"] = ty.expense_comment
        tyObj["user_id"] = ty.expense_user_id
        type_Array.append(tyObj)

    return jsonify({'type': type_Array})

@expense.route("/expense/dashbaord", methods=["GET","POST"])
def expense_dashboard():

    max_date = Expense.query.filter_by(expense_user_id = current_user.id).order_by(Expense.expense_date.desc()).first()
    min_date = Expense.query.filter_by(expense_user_id = current_user.id).order_by(Expense.expense_date).first()
    min_val = min_date.expense_date
    max_val = max_date.expense_date
    # max = Expense.query(func.min(expense.expense_date)).scalar()

    return render_template("expense_dashboard.html",title='login',  project = "expense", max_date = max_val.date() ,min_date= min_val.date())

@expense.route("/expense/display")
def edit_expense():
    all_records=Expense.query.filter_by(expense_user_id = current_user.id).order_by(Expense.expense_date.desc()).all()
    inc_exp = []
    for inc,_ in all_records:
        inc_exp.append(inc.expense_amount)

    return render_template("display_expenses.html",title='login',  
                            inc_json = json.dumps(inc_exp), project = "expense", all_list= all_records)

@expense.route("/expense/record/delete/<rec_id>", methods=['GET','POST'])
def delete_record(rec_id):
    record = Expense.query.filter_by(expense_id = rec_id).first()
    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(record)
        db.session.commit()

        return redirect(url_for('expense.expense_tracker'))


    return render_template("delete_record.html",form=form, project ="expense", title="delete",rec =record)

@expense.route("/expense/record/edit/<rec_id>", methods =['GET','POST'])
@login_required
def edit_record(rec_id):
    #record= Expense.query.filter_by(expense_id=rec_id).first()
    user_setting = Settings.query.filter_by(user_id=current_user.id).all()
    record =Expense.query.get(rec_id)
    form  = ExpenseForm()
    
    all_cate = [user.category for user  in user_setting]
    all_item = [user.type for user  in user_setting]

    all_cate = list(set(all_cate))
    all_item = list(set(all_item))

    form.cate.choices = [(cate, cate) for cate in all_cate]
    form.item.choices = [(item, item) for item  in all_item]
  
    # form.cate.data = record.expense_category
    # form.item.data = record.expense_name
    form.amt.data= record.expense_amount
    form.date.data = record.expense_date
    form.comment.data = record.expense_comment
 
    if form.validate_on_submit():
        record.expense_name = request.form.get("item").lower()
        record.expense_category =  request.form.get("cate").lower()
        record.expense_amount =  request.form.get("amt")
        record.expense_date = request.form.get("date")
        record.expense_comment =  request.form.get("comment")
        record.expense_user_id = current_user.id

        db.session.merge(record)
        db.session.commit()

        flash("Your record has been edited")
        return redirect(url_for("expense.expense_tracker")) 

    return render_template("edit_expense.html",form =form,title="edit record", 
                            project = "expense", record= record)

# @expense.route("/expense/setting/<user_id>")
# def expense_setting_user(user_id):
#     seeting = []
#     user_setting = Settings.query.filter_by(user_id=current_user.id).all()
    
#     for user in user_setting:
