import mysql.connector
import bcrypt
from datetime import datetime
def connect():
    try:
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='shivam@123',
            database='easyshop',
        )
    except:
        connect()
    return mydb

def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")

def update_profile(fname:str,lname:str,email:str,passwd:str,ph_no:str,usertype:int):
       mydb = connect()
       mycursor = mydb.cursor()
       hassedPasswd = bcrypt.hashpw(passwd.encode("utf-8"), bcrypt.gensalt())
       print(hassedPasswd)
       if(usertype==1):
            mycursor.execute("""UPDATE buyer_info SET fname=%s,lname=%s, email=%s, pass=%s,phno=%s where email=%s""",
                             (fname, lname, email, hassedPasswd,ph_no,email))
            mydb.commit()
            return 1
       else:
           mycursor.execute("""UPDATE seller_info SET fname=%s,lname=%s, email=%s, pass=%s,phno=%s where email=%s""",
                            (fname, lname, email, hassedPasswd, ph_no, email))
           mydb.commit()
           return 0

def getcatwise(cat:str):
    mydb = connect()
    mycursor = mydb.cursor()
    statement="SELECT * from seller_info"
    mycursor.execute(statement)
    fetched_list = mycursor.fetchall()
    if fetched_list == None:
        return [('0','0','0','0','0','0','0','0')]
    return fetched_list

def search(name:str):
    mydb = connect()
    mycursor = mydb.cursor()
    try:
        statement = """SELECT sname,prod_name,price,shop_id,prod_id,prod_image,qty from shop_products where sname=%s OR prod_name=%s OR subcategory=%s OR shop_type=%s"""
        mycursor.execute(statement, (name,name,name,name))
        fetched_list = mycursor.fetchall()
        if fetched_list == None:
            return None
        rows = len(fetched_list)
        print(rows)
        for row in range(rows):
            photo = fetched_list[row][5]
            photoPath = "static\images\\" + str(fetched_list[row][1]) + str(fetched_list[row][3]) + ".jpg"
            writeTofile(photo, photoPath)
            as_list = list(fetched_list[row])  # storing it as list because tuple indices are non initialisable
            print('324', photoPath)
            as_list[5] = r"images/" + str(fetched_list[row][1]) + str(fetched_list[row][3]) + ".jpg"
            fetched_list[row] = tuple(as_list)


        return fetched_list
    except:
        return[('0')]

def shopbyID(userID :str):
    mydb=connect()
    mycursor=mydb.cursor()
    mycursor.execute("SELECT sname,prod_name,price,shop_id,prod_id,prod_image,qty from shop_products where shop_id = \"" + str(userID) + "\"")
    fetched_list = mycursor.fetchall()
    if fetched_list == None:
        return [('0', '0', '0','0','0','0','0')]
    print(fetched_list)
    rows=len(fetched_list)


    for row in range(rows):
        photo = fetched_list[row][5]
        photoPath = "static\images\\" + str(fetched_list[row][1])+str(fetched_list[row][3]) + ".jpg"
        writeTofile(photo, photoPath)
        as_list=list(fetched_list[row])  # storing it as list because tuple indices are non initialisable
        print('324',photoPath)
        as_list[5] = r"images/"+str(fetched_list[row][1])+str(fetched_list[row][3]) + ".jpg"
        fetched_list[row]=tuple(as_list)


    return fetched_list

def get_shop_name(user_id:int):
    mydb=connect()
    mycursor=mydb.cursor()
    print(user_id,"fg")
    statement="""SELECT sname from seller_info where userid=%s """
    mycursor.execute(statement,(user_id,))
    sname=mycursor.fetchall()
    print(sname)
    return sname[0][0]

def add_to_cart(prod_name:str,userID: int,prod_id:str,price: int,emailid:str):
    mydb=connect()
    mycursor=mydb.cursor()
    try:
        up_id=str(userID)+'-'+str(prod_id)
        print(up_id,userID,prod_id,prod_name,price)
        qty=1
        statement= "INSERT into my_cart (up_id,prod_name,prod_unit_price,prod_qty,customer_id) VALUES (%s,%s,%s,%s,%s)"
        info= (up_id,prod_name,price,qty,emailid)
        print('sending')
        mycursor.execute(statement,info)

        mydb.commit()
        return 1
    except:
        return -1



def recieve_cart():
    mydb=connect()
    mycursor=mydb.cursor()
    try:
        mycursor.execute("SELECT * from my_cart")
        fetched_list = mycursor.fetchall()
        return fetched_list
    except:
        return [(0)]


def take_order(qty:list,emailid: str,dtype: str,order_sum: str,address:str):
    mydb=connect()
    mycursor=mydb.cursor()
    try:
        nowtime=datetime.now()
        dt_string = nowtime.strftime("%d/%m/%Y %H:%M:%S")

        mycursor.execute("SELECT * from my_cart where customer_id=\"" + emailid + "\"")
        fetched_list=mycursor.fetchall()
        print(dt_string)
        rows=len(fetched_list)
        dstatus = 'NO'
        for i in range(rows):
            up_id=fetched_list[i][0]
            prod_name=fetched_list[i][2]
            prod_unit_price=fetched_list[i][3]
            prod_qty=qty[i]
            orderID= up_id+dt_string
            delivery_type=dtype
            print("scusi",up_id)
            shop_id=''
            for j in range(len(up_id)):
               if up_id[j]!='-':
                   shop_id+=(up_id[j])
               else:
                   break
            s_id=int(shop_id)
            up_id2=str(up_id)
            s_id2=str(s_id)+'-'

            if s_id2 in up_id2:
                up_id2=up_id2.replace(s_id2,'',1)
                print(up_id2)
            prod_id=up_id2              # prev 6 lines for getting prod_id from up_id

            print(shop_id)
            print("scusi")
            if str(prod_qty)=='0':
                continue
            info = (
            up_id, prod_name, prod_unit_price, prod_qty, delivery_type, dt_string, orderID, order_sum, s_id, emailid,
            dstatus,address)
            print(info)
            statement = "INSERT into my_orders (up_id,prod_name,prod_unit_price,prod_qty,delivery_type,order_time," \
                        "order_id,order_sum,shop_id,user_mailID,del_status,user_address) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "


            mycursor.execute(statement, info)
            mydb.commit()
            print('inserted',prod_id,prod_qty)

            mycursor.execute("""UPDATE shop_products SET qty=qty-%s where prod_id=%s""",(prod_qty,prod_id))  # for subtracting the amount which is bought from shop stock
            mydb.commit()
        return 1
    except:
        return -1

def order_given(email:str):
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT prod_name,prod_unit_price,delivery_type,order_time,del_status,shop_id from my_orders where user_mailID = \"" + email + "\"")
    fetched_list=mycursor.fetchall()
    return fetched_list

def get_pending_orders(email:str):
    mydb = connect()
    mycursor = mydb.cursor()
    try:
        statement="""SELECT prod_name,prod_unit_price,delivery_type,order_time,del_status,shop_id from my_orders where user_mailID =%s del_status=%s"""
        mycursor.execute(statement,(email,'NO'))
        fetched_list=mycursor.fetchall()
        return fetched_list
    except:
        return [('0')]

def get_orders_by_time(shop_id:int,user_mailid:str,order_time:str):
    mydb = connect()
    mycursor = mydb.cursor()
    try:
        statement = """SELECT * from my_orders where shop_id=%s AND user_mailID=%s AND order_time=%s"""
        mycursor.execute(statement, (shop_id, user_mailid, order_time))
        fetched_list = mycursor.fetchall()
        if len(fetched_list) == 0:
            return None
        else:
            return fetched_list
    except:
        return [('0')]

def get_orders_pending(user_mailid:str):
    mydb = connect()
    mycursor = mydb.cursor()
    d_status = 'NO'
    statement = """SELECT * from my_orders where user_mailID=%s AND del_status=%s"""
    mycursor.execute(statement, (user_mailid, d_status))
    fetched_list = mycursor.fetchall()
    if len(fetched_list) == 0:
        return None
    else:
        return fetched_list

def update_del_status(order_time:str,del_status:str,customer_id:str,shop_id:str):
    mydb = connect()
    mycursor = mydb.cursor()
    try:
        statement="""UPDATE my_orders SET del_status=%s where order_time=%s AND user_mailID=%s AND shop_id=%s"""
        mycursor.execute(statement,(del_status,order_time,customer_id,shop_id))
        mydb.commit()
        return 1
    except:
        return -1



