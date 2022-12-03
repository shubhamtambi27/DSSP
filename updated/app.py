from flask import Flask, render_template, request, url_for, flash, redirect
import os
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('DSSP.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET","POST"])
def index():
    return render_template("index.html")

@app.route("/loginas")
def loginas():
    return render_template("login.html")

@app.route("/teacherlogin")
def teacherlogin():
    return render_template("teacher.html")

@app.route("/adminlogin")
def adminlogin():
    return render_template("admin.html")

@app.route("/studentlogin")
def studentlogin():
    return render_template("student.html") 

@app.route("/savedetails",methods = ["POST","GET"])  
def saveDetails():  
    if request.method == "POST": 
        try:  
            name = request.form["name"]  
            email = request.form["email"]  
            subject = request.form["subject"]
            message = request.form["message"] 
            conn = sqlite3.connect('DSSP.db')
            cur = conn.cursor()
            cur.execute("INSERT into Feedback (name, email, subject, message) values (?,?,?,?)",(name, email, subject, message))  
            conn.commit()  
            print("Success")  
        except:  
            conn.rollback()  
            msg = "We can not add the employee to the list"  
        finally:  
            return render_template("index.html")  
            conn.close

if __name__ == "__main__":
	app.run()
