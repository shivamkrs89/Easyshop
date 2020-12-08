from flask import Flask, request, session, render_template, flash, redirect, url_for

from common import dblogin
@app.route('/signup', methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        form_data = request.form.to_dict()
        name = form_data['name']
        passwd = form_data['pass']
        email = form_data['email']
        passwdchk = form_data['passcheck']
        address = form_data['address']
        phno = str(form_data['ph_no'])
        person=str(form_data['person'])
        if name == '':
            flash("Please enter your name")
            return render_template('signup_student.html')
        elif address == '':
            flash("Please enter address")
            return render_template('signup.html')
        elif phno == '':
            flash("Please enter phno")
            return render_template('signup.html')
        elif passwd == '':
            flash("Please enter a password")
            return render_template('signup.html')
        elif passwdchk == '':
            flash("Please enter confirm password")
            return render_template('signup.html')
        elif passwd != passwdchk:
            flash("Password and confirm password do not match, Please re-enter")
            return render_template('signup.html')
        success=1
        if person=="buyer":
            success = dblogin.buyer_registration(name, email, address, passwd, phno)
        elif person=="seller":
            success = dblogin.seller_registration(name, email, address, passwd, phno)
        if success == 0:
            flash("email or phone no. already exists, please login")
            return render_template('signup.html')
        elif success == 1:
            flash("Registration Successful, Please Login")
            return redirect(url_for('signin'))
    return render_template('signup.html')

