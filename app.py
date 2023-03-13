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
    return render_template("loginas.html")

@app.route("/teacherlogin")
def teacherlogin():
    return render_template("teacher.html")

@app.route("/adminlogin")
def adminlogin():
    return render_template("admin.html")

@app.route("/studentlogin")
def studentlogin():
    return render_template("student.html") 

@app.route("/teacherhome")
def teacherhome():
    return render_template("teacherhome.html")

@app.route("/adminhome")
def adminhome():
    return render_template("adminhome.html")

@app.route("/studenthome")
def studenthome():
    return render_template("studenthome.html")

@app.route("/viewattendance")
def viewattendance():
    conn = sqlite3.connect('DSSP.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM attendance')
    users = cur.fetchall()
    return render_template("viewattendance.html",users=users)

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
        finally:  
            return render_template("index.html")  
            conn.close

@app.route("/checkteachersdetails",methods = ["POST","GET"])
def checkteachersdetails():
    if request.method == "POST": 
        try:  
            email = request.form["email"]  
            role="T"
            password = request.form["password"] 
            print("Values")
            print(email,password)
            conn = sqlite3.connect('DSSP.db')
            curr = conn.cursor()
            data = curr.execute("SELECT email,password FROM users WHERE email=(?)  and password=(?)  and role=(?);", (email,password,role)).fetchone()
            print("Done")
            print(data)
            if(data==None):
                flash('Wrong Credentials')
                return render_template("loginas.html")
            if len(data)>0:
                if(data[1]==password and data[0]==email):
                    #print("Re")
                    return render_template("teacherhome.html")
        except:  
            flash("Wrong")
            return render_template("teacher.html")

@app.route("/checkadmindetails",methods = ["POST","GET"])
def checkadmindetails():
    if request.method == "POST": 
        try:  
            email = request.form["email"]  
            role="A"
            password = request.form["password"] 
            print("Values")
            print(email,password)
            conn = sqlite3.connect('DSSP.db')
            curr = conn.cursor()
            data = curr.execute("SELECT email,password FROM users WHERE email=(?)  and password=(?) and role=(?);", (email,password,role)).fetchone()
            print("Done")
            print(data)
            if len(data)>0:
                if(data[1]==password and data[0]==email):
                    #print("Re")
                    return render_template("adminhome.html")
        except:  
            flash("Wrong")
            return render_template("admin.html")

@app.route("/checkstudentdetails",methods = ["POST","GET"])
def checkstudentdetails():
    if request.method == "POST": 
        try:  
            email = request.form["email"]  
            role="S"
            password = request.form["password"] 
            print("Values")
            print(email,password)
            conn = sqlite3.connect('DSSP.db')
            curr = conn.cursor()
            data = curr.execute("SELECT email,password FROM users WHERE email=(?)  and password=(?) and role=(?);", (email,password,role)).fetchone()
            print("Done")
            if len(data)>0:
                if(data[1]==password and data[0]==email):
                    #print("Re")
                    return render_template("studenthome.html")
        except:  
            flash("Wrong")
            return render_template("student.html")


if __name__ == "__main__":
	app.run(debug=True)
