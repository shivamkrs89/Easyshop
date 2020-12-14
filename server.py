from flask import Flask, request, session, render_template, flash, redirect, url_for
from common import dblogin, dboperations
app = Flask(__name__, template_folder='template/')
app.secret_key = 'the random string'
# app.permanent_session_lifetime = datetime.timedelta(days=1)

@app.route('/')
def home():
    return redirect(url_for('index'))
@app.route('/index',methods=["POST","GET"])
def index():
    if session.get('buyer_logged_in') or session.get('seller_logged_in'):
        if session.get('buyer_logged_in'):
            return redirect(url_for('buyer_dashboard'))
    elif request.method=="POST":
        form_data=request.form.to_dict()
        email=form_data['email']
        passwd=form_data['pass']
        usertype=form_data['usertype']
        list=[]
        # if int(usertype) == 1:
        print(email, usertype)
        list = dblogin.buyer_login(email, passwd)


        if list[0][0]==0 or list[0][0]==-1:
            flash("Credentials mismatched or email not not found")
            render_template('index.html')

        else:
            session['buyer_logged_in'] = email
            session['fname']= list[0][0]
            session['lname']= list[0][1]
            session['passwd']=list[0][2]
            session['ph_no']=list[0][3]
            return redirect(url_for('buyer_dashboard'))

    list1 = dboperations.getcatwise("Electronics")


    return render_template('index.html',list1=list1)

@app.route('/signup_shop1',methods=["POST", "GET"])
def shop1_signup():
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

        session['emailid'] = email
        print(session['emailid'])



        success=dblogin.seller_registration1(fname, lname, email, address, passwd, phno)
        print(str(success))
        if success == 0:
            flash("email or phone no. already exists, please login")
            return render_template('signup_shop1.html')
        elif success == 1:
            print("success")
            session['owner_info'] = 1
            return redirect(url_for('shop2_signup'))

    return render_template('signup_shop1.html')



@app.route('/signup_shop2',methods=["POST", "GET"])
def shop2_signup():
    if session.get('owner_info'):
            if request.method == "POST":
                form_data = request.form.to_dict()
                sname=form_data['sname']
                saddress = form_data['saddress']
                stype=form_data['stype']
                email=session.get('emailid')
                # print(email)
                if sname == '':
                    flash("Please enter your shop name")
                    return render_template('signup_shop2.html')
                elif saddress == '':
                    flash("Please enter shop's address")
                    return render_template('signup_shop2.html')
                elif stype == '':
                    flash("Please specify the category of the shop")
                    return render_template('signup_shop2.html')
                success = dblogin.seller_registration2(email,sname,stype,saddress)
                if success == 0:
                    flash("same shop name already exists, try different")
                    return render_template('signup_shop2.html')
                elif success == 1:
                    return redirect(url_for('index'))
            return render_template('signup_shop2.html')
    else:
       return redirect(url_for('shop1_signup'))

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


        success = dblogin.buyer_registration(fname, lname, email, address, passwd, phno)

        if success == 0:
            flash("email or phone no. already exists, please login")
        elif success == 1:
            return redirect(url_for('index')) #to be filled by buyer dashboard
    return render_template('signup.html')

@app.route('/shop', methods=["POST","GET"])
def buyer_dashboard():
    if session.get('buyer_logged_in'):
        email = session.get('buyer_logged_in')
        fname=session.get('fname')
        lname=session.get('lname')
        session['user_type'] = 1
        list1 = dboperations.getcatwise("Electronics")
        return render_template('shop.html', email=email,fname=fname,lname=lname,list1=list1)

@app.route('/signout', methods=["POST", "GET"])
def signout():
    if session.get('buyer_logged_in') or session.get('seller_logged_in'):
        session.clear()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
@app.route('/update_profile',methods=["POST","GET"])
def profile_update():
    if session.get('buyer_logged_in') or session.get('seller_logged_in'):
        email = session.get('buyer_logged_in')
        fname = session.get('fname')
        lname = session.get('lname')
        ph_no =  session.get('ph_no')
        usertype=session.get('user_type')
        if request.method=='POST':
            form_data=request.form.to_dict()
            new_email=form_data['new_email']
            fname=form_data['fname']
            lname=form_data['lname']
            new_mobileno=form_data['new_mobileno']
            new_pass=form_data['new_pass']
            usertype=session.get('user_type')
            success = dboperations.update_profile(fname,lname,new_email,new_pass,new_mobileno,usertype)
            flash("Profile is updated login again"+str(success))
            return redirect(url_for('signout'))
        return render_template('update_profile.html',email=email,fname=fname,lname=lname,ph_no=ph_no,usertype=usertype)
    return redirect(url_for('index'))

@app.route('/shop_details/<userid>',methods=["POST","GET"])
def display_shop(userid):
    if session.get('buyer_logged_in'):
        list=dboperations.shopbyID(userid)
        length=len(list)
        return render_template('shop_details.html',list=list,length=length)
    return redirect(url_for('index'))
if __name__ == "__main__":
    app.run(debug="true")