from flask import Flask, request, session, render_template, flash, redirect, url_for

from common import dblogin

@app.route('/signup_shop1', methods=["POST", "GET"])
def shop1_sign_up():
    if request.method == "POST":
        form_data = request.form.to_dict()
        fname = form_data['fname']
        lname = form_data['lname']
        passwd = form_data['pass']
        email = form_data['email']
        passwdchk = form_data['passcheck']
        address = form_data['address']
        phno = str(form_data['ph_no']

        if fname == '':
            flash("Please enter your first name")
            return render_template('signup_shop1.html')
        elif address == '':
            flash("Please enter address")
            return render_template('signup_shop1.html')
        elif phno == '':
            flash("Please enter phno")
            return render_template('signup_shop1.html')
        elif passwd == '':
            flash("Please enter a password")
            return render_template('signup_shop1.html')
        elif passwdchk == '':
            flash("Please enter confirm password")
            return render_template('signup_shop1.html')
        elif passwd != passwdchk:
            flash("Password and confirm password do not match, Please re-enter")
            return render_template('signup_shop1.html')

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
        if sname == '':
            flash("Please enter your shop name")
            return render_template('signup_shop2.html')
        elif saddress == '':
            flash("Please enter shop's address")
            return render_template('signup_shop2.html')
        elif stype == '':
            flash("Please specifythe category of the shop")
            return render_template('signup_shop2.html')
        success=dblogin.seller_registration2(sname,stype,saddress)
        if success == 0:
            flash("same shop name already exists, try different")
            return render_template('signup_shop2.html')
        elif success == 1:
            return render_template('signin.html')
    return render_template('signup_shop1.html')
