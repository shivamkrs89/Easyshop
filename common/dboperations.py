import mysql.connector
import bcrypt
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
                            (fname, lname, email, passwd, ph_no, email))
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

def searchbyname(name:str):
    mydb = connect()
    mycursor = mydb.cursor()
    statement = """SELECT * from seller_info where sname=%s"""
    mycursor.execute(statement, name)
    fetched_list = mycursor.fetchall()
    if fetched_list == None:
        return

def shopbyID(userID :str):
    mydb=connect()
    mycursor=mydb.cursor()
    mycursor.execute("SELECT sname,prod_name,price from shop_products where shop_id = \"" + userID + "\"")
    fetched_list = mycursor.fetchall()
    if fetched_list == None:
        return [('0', '0', '0')]
    return fetched_list