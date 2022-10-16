
import sqlite3

conn = sqlite3.connect('smartmart.db')
cur = conn.cursor()
def viewcart():
    with conn:
        cur.execute("SELECT * FROM carta01;")
        print(cur.fetchall())
def getprice():
    with conn:
        cur.execute("Select sum(price) from carta01;")
        sum=cur.fetchall()
        print(sum)
def additem():
    with conn:
        cur.execute()
def delete():
    with conn:
        cur.execute("delete from carta01;")
        conn.commit()
def cust():
    with conn:
        cur.execute("""INSERT INTO cust(name,mobile,purchase,date) VALUES (?,?,?,getdate());""",(name,mob,total))
        conn.commit()
def deleteitem():
    with conn:
        cur.execute("delete from carta01 where item_code=?",(item_code))