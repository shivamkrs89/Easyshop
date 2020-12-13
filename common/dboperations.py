import mysql.connector
import bcrypt
def connect():
    try:
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Somya@123',
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
       else:
           mycursor.execute("""UPDATE seller_info SET fname=%s,lname=%s, email=%s, pass=%s,phno=%s where email=%s""",
                            (fname, lname, email, passwd, ph_no, email))
           mydb.commit()

def getcatwise(cat:str):
    mydb = connect()
    mycursor = mydb.cursor()
    statement="SELECT * from seller_info"
    mycursor.execute(statement)
    fetched_list = mycursor.fetchall()

    return fetched_list