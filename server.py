from flask import Flask, request, session, render_template, flash, redirect, url_for
import datetime
from common import dblogin
app = Flask(__name__, template_folder='template/')
app.secret_key = 'the random string'
app.permanent_session_lifetime = datetime.timedelta(days=1)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/signup_shop1', methods=["POST", "GET"])
def shop1_sign_up():
    if request.method == "POST":
        form_data = request.form.to_dict()

        fname=form_data['fname']
        lname=form_data['lname']
        passwd=form_data['pass']
        email=form_data['email']
        passwdchk=form_data['passcheck']
        address=form_data['address']
        phno=form_data['ph_no']

        if passwd != passwdchk:
            flash("Password doesn't match!")
            render_template('signup_shop1.html')

        if session[email]==0:
            session[emaiid]=email

        success=dblogin.seller_registration1(fname, lname, email, address, passwd, phno)

        if success == 0:
            flash("email or phone no. already exists, please login")
            return render_template('signup_shop1.html')
        elif success == 1:
            return render_template('signup_shop2.html')

    return render_template('signup_shop1.html')



@app.route('/signup_shop2', methods=["POST", "GET"])
def sign_up_shop2():
    if request.method == "POST":
        form_data = request.form.to_dict()
        sname=form_data['snmae']
        saddress = form_data['saddress']
        stype=form_data['stype']
        email=session.get('emailid')
        if sname == '':
            flash("Please enter your shop name")
            return render_template('signup_shop2.html')
        elif saddress == '':
            flash("Please enter shop's address")
            return render_template('signup_shop2.html')
        elif stype == '':
            flash("Please specifythe category of the shop")
            return render_template('signup_shop2.html')
        success=dblogin.seller_registration2(email,sname,stype,saddress)
        if success == 0:
            flash("same shop name already exists, try different")
            return render_template('signup_shop2.html')
        elif success == 1:
            return render_template('signin.html')
    return render_template('signup_shop1.html')

@app.route('/signup',methods=["POST","GET"])
def buyer_signup():
    if request.method == "POST":
        form_data = request.form.to_dict()
        fname = form_data['fname']
        lname = form_data['lname']
        passwd = form_data['pass']
        email = form_data['email']
        passwdchk = form_data['passcheck']
        address = form_data['address']
        phno = form_data['ph_no']

        if passwd != passwdchk:
            flash("Password doesn't match!")
            render_template('signup.html')
        if session[email] == 0:
            session[emaiid] = email

        success = dblogin.buyer_registration(fname, lname, email, address, passwd, phno)

        if success == 0:
            flash("email or phone no. already exists, please login")
            return render_template('signup.html')
        elif success == 1:
            return render_template('#') #to be filled by buyer dashboard
    return render_template('signup.html')

if __name__ == "__main__":
    app.run(debug="true")