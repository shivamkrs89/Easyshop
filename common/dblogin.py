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
def seller_registration1(fname: str,lname: str, email: str, address: str, passwd: str, phno: str):#seller registration f
    mydb = connect()
    mycursor = mydb.cursor()
    hassedPasswd = bcrypt.hashpw(passwd.encode("utf-8"), bcrypt.gensalt())
    try:
        insertFn = "INSERT INTO seller_info (fname,lname,email,pass,address,phno) VALUES (%s, %s, %s, %s, %s,%s)"
        registration_info = (fname, lname, email, hassedPasswd, address, phno)
        mycursor.execute(insertFn, registration_info)
        mydb.commit()
        return 1
    except:
        return 0  # email exists

def seller_registration2(email: str,sname: str,stype:str, saddress: str):#seller's shop info register
    mydb = connect()
    mycursor = mydb.cursor()
    try:
        print(sname,stype,saddress,email)
        mycursor.execute("""UPDATE seller_info SET sname=%s,stype=%s, saddress=%s where email=%s""", (sname, stype, saddress, email))
        mydb.commit()
        return 1
    except:
        return 0  # email exis
def buyer_registration(fname: str,lname: str, email: str, address: str, passwd: str, phno: str):
    mydb = connect()
    mycursor = mydb.cursor()
    hassedPasswd = bcrypt.hashpw(passwd.encode("utf-8"), bcrypt.gensalt())
    try:

        insertFn = "INSERT INTO buyer_info (fname,lname,email,pass,address,phno) VALUES (%s, %s, %s, %s, %s,%s)"

        registration_info = (fname,lname, email, hassedPasswd, address, phno)
        mycursor.execute(insertFn, registration_info)
        mydb.commit()
        return 1
    except:
        return 0  # email exists

def seller_login(emailid: str, passwd: str):
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT pass from seller_info where email = \"" + emailid + "\"")
    fetched_list = mycursor.fetchall()
    if (len(fetched_list) == 0):
        return -1  # email id not found

    else:
        hassedPasswd = fetched_list[0][0]
        if bcrypt.checkpw(passwd.encode("utf-8"), hassedPasswd.encode("utf-8")):
            return 1  # login success
        else:
            return 0  # incorrect password
def buyer_login(emailid: str, passwd: str):
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT pass from buyer_info where email = \"" + emailid + "\"")
    fetched_list = mycursor.fetchall()
    if (len(fetched_list) == 0):
        return -1  # email id not found

    else:
        hassedPasswd = fetched_list[0][0]
        if bcrypt.checkpw(passwd.encode("utf-8"), hassedPasswd.encode("utf-8")):
            return 1  # login success
        else:
            return 0  # incorrect password