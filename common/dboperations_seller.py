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

def convertToBinaryData(filename):
    #Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


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



def searchbyname(name:str):
    mydb = connect()
    mycursor = mydb.cursor()
    statement = """SELECT * from seller_info where sname=%s"""
    mycursor.execute(statement, name)
    fetched_list = mycursor.fetchall()
    if fetched_list == None:
        return


def add_product(pname:str,price:float,qty:int,subcat:str,stype:str,pimage:str,shop_id:int,sname:str):
    mydb=connect()
    mycursor=mydb.cursor()
    try:
        print('in')
        bdata=convertToBinaryData(pimage)
        print('in')
        statement= "INSERT into shop_products (shop_id,prod_name,qty,price,sname,subcategory,shop_type,prod_image) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        print("sadas")
        info= (shop_id,pname,qty,price,sname,subcat,stype,bdata)
        print(info)
        mycursor.execute(statement, info)
        mydb.commit()
        return 1
    except:
        return -1

def add_more_qty(prod_id:str, new_qty:int):
    mydb = connect()
    mycursor = mydb.cursor()

    mycursor.execute("""UPDATE shop_products SET qty=qty+%s where prod_id=%s""",(new_qty,prod_id))
    mydb.commit()
    return 1

def get_customers_list(shop_id:int):
    mydb = connect()
    mycursor = mydb.cursor()
    try:
        print(shop_id)
        statement = "SELECT DISTINCT user_mailID from my_orders where shop_id=%s"
        mycursor.execute(statement, (shop_id,))
        print("df")
        fetched_list = mycursor.fetchall()
        if len(fetched_list) == 0:
            return None
        else:
            return fetched_list
    except:
        return [('0')]

def get_orders_delivered(shop_id:int,user_mailid:str):
    mydb = connect()
    mycursor = mydb.cursor()
    d_status='YES'
    statement = """SELECT * from my_orders where shop_id=%s AND user_mailID=%s AND del_status=%s"""
    mycursor.execute(statement, (shop_id,user_mailid,d_status))
    fetched_list = mycursor.fetchall()
    if len(fetched_list)==0:
        return None
    else:
        return fetched_list

def get_orders_pending(shop_id:int,user_mailid:str):
    mydb = connect()
    mycursor = mydb.cursor()
    d_status = 'NO'
    statement = """SELECT * from my_orders where shop_id=%s AND user_mailID=%s AND del_status=%s"""
    mycursor.execute(statement, (shop_id, user_mailid, d_status))
    fetched_list = mycursor.fetchall()
    if len(fetched_list) == 0:
        return None
    else:
        return fetched_list

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


def get_customers_details(shop_id:int):
    mydb = connect()
    mycursor = mydb.cursor()
    try:
        print(shop_id)
        statement = "SELECT COUNT(DISTINCT user_mailID),COUNT(DISTINCT order_id),COUNT(DISTINCT order_time) from my_orders where shop_id=%s"
        mycursor.execute(statement, (shop_id,))
        print("df")
        fetched_list = mycursor.fetchall()
        if len(fetched_list) == 0:
            return None
        else:
            return fetched_list
    except:
        return [('0')]
