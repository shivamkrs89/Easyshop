import os, sys
from flask import Flask, request, session, render_template, flash, redirect, url_for
from common import dblogin, dboperations, dboperations_seller
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='template/')
app.secret_key = 'the random string'
UPLOAD_FOLDER = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# def allowed_file(filename):
# 	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# app.permanent_session_lifetime = datetime.timedelta(days=1)

@app.route('/')
def home():
    return redirect(url_for('index'))


@app.route('/index', methods=["POST", "GET"])
def index():
    if session.get('buyer_logged_in') or session.get('seller_logged_in'):
        if session.get('buyer_logged_in'):
            return redirect(url_for('buyer_dashboard'))
        elif session.get('seller_logged_in'):
            return redirect(url_for('seller_dashboard'))
    elif request.method == "POST":
        form_data = request.form.to_dict()
        email = form_data['email']
        passwd = form_data['pass']
        usertype = form_data['usertype']
        session['usertype']=usertype
        print(usertype)
        list1 = None
        if int(usertype) == 1:
            print(email, usertype)
            list1 = dblogin.buyer_login(email, passwd)
        else:
            list1 = dblogin.seller_login(email, passwd)

        print("hello", list1[0][0])

        if list1[0][0] == '0' or list1[0][0] == '2':
            print("hello", list1)
            flash("Credentials mismatched or email not not found")
            return render_template('index.html')

        else:
            session['fname'] = list1[0][0]
            session['lname'] = list1[0][1]
            session['passwd'] = list1[0][2]
            session['ph_no'] = list1[0][3]

            if int(usertype) == 1:
                session['buyer_logged_in'] = email
                session['buyer_address'] = list1[0][4]
                return redirect(url_for('buyer_dashboard'))
            else:
                session['stype'] = list1[0][4]
                session['shop_id'] = list1[0][5]
                session['sname'] = list1[0][6]
                session['seller_logged_in'] = email
                return redirect(url_for('seller_dashboard'))


    return render_template('index.html')


@app.route('/signup_shop1', methods=["POST", "GET"])
def shop1_signup():
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
            render_template('signup_shop1.html')

        session['emailid'] = email
        print(session['emailid'])

        success = dblogin.seller_registration1(fname, lname, email, address, passwd, phno)
        print(str(success))
        if success == 0:
            flash("email or phone no. already exists, please login")
            return render_template('signup_shop1.html')
        elif success == 1:
            print("success")
            session['owner_info'] = 1
            return redirect(url_for('shop2_signup'))

    return render_template('signup_shop1.html')


@app.route('/signup_shop2', methods=["POST", "GET"])
def shop2_signup():
    if session.get('owner_info'):
        if request.method == "POST":
            form_data = request.form.to_dict()
            sname = form_data['sname']
            saddress = form_data['saddress']
            stype = form_data['stype']
            email = session.get('emailid')
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
            success = dblogin.seller_registration2(email, sname, stype, saddress)
            if success == 0:
                flash("same shop name already exists, try different")
                return render_template('signup_shop2.html')
            elif success == 1:
                return redirect(url_for('index'))
        return render_template('signup_shop2.html')
    else:
        return redirect(url_for('shop1_signup'))


@app.route('/signup', methods=["POST", "GET"])
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
            return redirect(url_for('index'))  # to be filled by buyer dashboard
    return render_template('signup.html')


@app.route('/shop', methods=["POST", "GET"])
def buyer_dashboard():
    if session.get('buyer_logged_in'):
        email = session.get('buyer_logged_in')
        fname = session.get('fname')
        lname = session.get('lname')
        session['user_type'] = 1
        list1 = dboperations.getcatwise("Electronics")
        length=len(list1)
        if list1==None:
            length=0

        return render_template('shop.html', email=email, fname=fname, lname=lname, list1=list1,length=length)


@app.route('/my_shop', methods=["POST", "GET"])
def seller_dashboard():
    if session.get('seller_logged_in'):
        email = session.get('seller_logged_in')
        fname = session.get('fname')
        lname = session.get('lname')
        if session.get('user_stats') is None:
            session['user_stats']=1
            shop_id=session.get('shop_id')
            list=dboperations_seller.get_customers_details(shop_id)
            if list == None:
                session['no_users'] =0
                session['no_orders'] =0
                session['no_prods_ordered'] =0
                return render_template('my_shop.html', email=email, fname=fname, lname=lname,no_users=0,no_orders=0,no_prods_ordered=0)

            session['no_users']=list[0][0]
            session['no_orders']=list[0][1]
            session['no_prods_ordered']=list[0][2]

            return render_template('my_shop.html', email=email, fname=fname, lname=lname, no_users=list[0][0], no_orders=list[0][1],
                                   no_prods_ordered=list[0][2])

        session['user_type'] = 2
        no_users=session.get('no_users')
        no_orders=session.get('no_orders')
        no_prods_ordered=session.get('no_prods_ordered')
        print(no_prods_ordered,no_orders,no_users)
        return render_template('my_shop.html', email=email, fname=fname, lname=lname, no_users=no_users,no_orders=no_orders,no_prods_ordered=no_prods_ordered)


@app.route('/signout', methods=["POST", "GET"])
def signout():
    if session.get('buyer_logged_in') or session.get('seller_logged_in'):
        session.clear()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@app.route('/update_profile', methods=["POST", "GET"])
def profile_update():
    if session.get('buyer_logged_in') or session.get('seller_logged_in'):
        email = 'none'
        if session.get('buyer_logged_in'):
            email = session.get('buyer_logged_in')
        elif session.get('seller_logged_in'):
            email = session.get('seller_logged_in')
        fname = session.get('fname')
        lname = session.get('lname')
        ph_no = session.get('ph_no')
        usertype = session.get('user_type')
        if request.method == 'POST':
            form_data = request.form.to_dict()
            new_email = form_data['new_email']
            fname = form_data['fname']
            lname = form_data['lname']
            new_mobileno = form_data['new_mobileno']
            new_pass = form_data['new_pass']
            usertype = session.get('user_type')
            success = dboperations.update_profile(fname, lname, new_email, new_pass, new_mobileno, usertype)
            flash("Profile is updated login again" + str(success))
            return redirect(url_for('signout'))
        return render_template('update_profile.html', email=email, fname=fname, lname=lname, ph_no=ph_no,
                               usertype=usertype)
    return redirect(url_for('index'))


@app.route('/shop_details/<userid>', methods=["POST", "GET"])
def display_shop(userid):
    if session.get('buyer_logged_in'):
        list = dboperations.shopbyID(userid)
        s_name=dboperations.get_shop_name(userid)
        length = len(list)
        if list==None:
            length=0
        print(list)
        return render_template('shop_details.html', list=list, length=length,sname=s_name)
    return redirect(url_for('index'))


@app.route('/cart<userid>_<prodid>_<prodname>_<price>', methods=["POST", "GET"])
def get_to_cart(userid, prodid, prodname, price):
    if session.get('buyer_logged_in'):
        emailid = session.get('buyer_logged_in')
        success = dboperations.add_to_cart(prodname, userid, prodid, price, emailid)
        if success == -1:
            flash("The product is already in the cart")
        return redirect(url_for('display_shop', userid=userid))
    return redirect(url_for('index'))


@app.route('/show_cart', methods=["POST", "GET"])
def show_cart():
    if session.get('buyer_logged_in'):
        emailid = session.get('buyer_logged_in')
        return redirect(url_for('finalise_cart'))

    return redirect(url_for('index'))


@app.route('/cart', methods=["POST", "GET"])
def finalise_cart():
    if session.get('buyer_logged_in'):
        list1 = dboperations.recieve_cart()
        length = len(list1)
        print(length)
        if length == 0:
            flash("Cart is empty!")
            return redirect(url_for('buyer_dashboard'))
        if request.method == "POST":
            emailid = session.get('buyer_logged_in')
            form = request.form.to_dict()
            qtylist = []
            for i in range(int(length)):
                qtylist.append(form[str(i)])
            ordersum = form['sum']
            dtype = form['dtype']
            print(qtylist, dtype, ordersum)
            address = session.get('buyer_address')
            success = dboperations.take_order(qtylist, emailid, dtype, ordersum, address)

            if success == 1:
                flash("Order placed succesfully")

            else:
                flash("Please try after some time")

            return redirect(url_for('buyer_dashboard'))

        return render_template('cart.html', list1=list1, len=int(length))


@app.route('/my_orders', methods=["POST", "GET"])
def get_orders():
    if session.get('buyer_logged_in'):
        email = session.get('buyer_logged_in')
        list1 = dboperations.order_given(email)
        length = len(list1)
        return render_template('my_orders.html', list=list1, length=length)
    return redirect(url_for('index'))


@app.route('/add_prod', methods=["POST", "GET"])
def product_add():
    if session.get('seller_logged_in'):
        if request.method == "POST":
            form_data = request.form.to_dict()
            pname = form_data['pname']
            price = form_data['price']
            subcategory = form_data['subcat']
            qty = form_data['qty']
            uploaded_file = request.files['pimage']
            stype = session.get('stype')
            shop_id = session.get('shop_id')
            sname = session.get('sname')

            if uploaded_file.filename != '':
                secured_filename = secure_filename(uploaded_file.filename)
                local_filename = "%s" % (secured_filename)

                uploaded_file.save(uploaded_file.filename)
                os.rename(local_filename, str(pname) + str(shop_id) + '.jpg')
                local_filename = str(pname) + str(shop_id) + '.jpg'
                success = dboperations_seller.add_product(pname, float(price), int(qty), subcategory, stype,
                                                          local_filename, int(shop_id),
                                                          sname)
                if success == 1:
                    flash("Product added successfully")
                else:
                    flash("Can't upload ensure all fields are filled properly")
        return render_template('Add_Product.html')


@app.route('/my_shop_products', methods=["POST", "GET"])
def add_More():
    if session.get('seller_logged_in'):
        if request.method == 'POST':
            form_data = request.form.to_dict()
            prod_id = form_data['prod_id']
            new_qty = form_data['new_qty']
            success = dboperations_seller.add_more_qty(prod_id, new_qty)

        shop_id = session.get('shop_id')
        list = dboperations.shopbyID(shop_id)
        length = len(list)
        return render_template('my_shop_products.html', list=list, length=length)


@app.route('/recieved_customers', methods=["POST", "GET"])
def get_customers():
    if session.get('seller_logged_in'):
        shop_id = session.get('shop_id')
        list = dboperations_seller.get_customers_list(shop_id)
        if list == None or list[0][0] == '0':
            flash('No products ordered from your shop yet :<')
        length = len(list)
        return render_template('recieved_orders.html', list=list, len=length)


@app.route('/orders_delivered/<customer_id>', methods=["POST", "GET"])
def order_delivered(customer_id):
    if session.get('seller_logged_in'):
        shop_id = session.get('shop_id')
        list = dboperations_seller.get_orders_delivered(shop_id, customer_id)
        if list == None:
            flash('No orders delivered to this customer from your shop yet :<')
            return redirect(url_for('seller_dashboard'))
        length = len(list)
        return render_template('display_delivered.html', list=list, len=length)


@app.route('/orders_pending/<customer_id>', methods=["POST", "GET"])
def order_pending(customer_id):
    if session.get('seller_logged_in'):
        shop_id = session.get('shop_id')
        list = dboperations_seller.get_orders_pending(shop_id, customer_id)
        if list == None:
            flash('No orders pending to this customer from your shop yet :<')
            return redirect(url_for('seller_dashboard'))
        length = len(list)
        return render_template('display_pending.html', list=list, len=length)


@app.route('/orders_by_time', methods=["POST","GET"])
def orders_by_time():
    print("FGH")
    if session.get('buyer_logged_in'):
        if request.method == 'POST':
            form_data = request.form.to_dict()
            order_time = form_data['order_time']
            customer_id=form_data['customer_id']
            order_status=form_data['order_status']
            print(order_time)
            shop_id = form_data['shop_id']
            print(shop_id)
            success=dboperations.update_del_status(order_time,order_status,customer_id,shop_id)

            print(success)
            list = dboperations.get_orders_by_time(shop_id, customer_id, order_time)
            if list == None:
                flash('No product ordered on this date :<')
                return redirect(url_for('buyer_dashboard'))
            length = len(list)
            return render_template('display_orders.html', list=list, len=length)
    if session.get('seller_logged_in'):
        if request.method == 'POST':
            form_data = request.form.to_dict()
            order_time = form_data['order_time']
            customer_id=form_data['customer_id']
            print(order_time)
            shop_id = session.get('shop_id')
            print(shop_id)
            list = dboperations_seller.get_orders_by_time(shop_id, customer_id, order_time)
            if list == None:
                flash('No product ordered on this date :<')
                return redirect(url_for('seller_dashboard'))
            length = len(list)
            return render_template('display_orders.html', list=list, len=length)
    return redirect(url_for('index'))

@app.route('/search_query',methods=["POST","GET"])
def search():
    if session.get('buyer_logged_in') or session.get('seller_logged_in'):
        if request.method=='POST':
            form_data = request.form.to_dict()
            query = form_data['query']
            list=dboperations.search(query)
            if list == None:
                flash('No results matched:<')
                return redirect(url_for('search'))
            length = len(list)
            print(list)
            usertype=int(session.get('usertype'))

            return render_template('display_search_results.html', list=list, len=length,query=query,user_type=usertype)
        if session.get('buyer_logged_in'):
            return redirect(url_for('buyer_dashboard'))
        elif session.get('buyer_logged_in'):
            return redirect(url_for('seller_dashboard'))
    flash('Please Login or register to see results')
    return redirect(url_for('index'))

@app.route('/buyer_orders_pending', methods=["POST", "GET"])
def buyer_order_pending():
    if session.get('buyer_logged_in'):
        email_id= session.get('buyer_logged_in')
        list = dboperations.get_orders_pending(email_id)
        if list == None:
            flash('No orders pending:<')
            return redirect(url_for('buyer_dashboard'))
        length = len(list)
        return render_template('buyer_pending_orders.html', list=list, len=length)


if __name__ == "__main__":
    app.run(debug="true")
