from flask import Flask, render_template, request, url_for, flash, redirect, Response
import os
import datetime
import sqlite3
import pywhatkit
import smtplib
import pandas as pd
import cv2
from flask_mail import Mail, Message
x = str(datetime.datetime.now())

app = Flask(__name__)
mail= Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = '2019pietcssalvader144@poornima.org'
app.config['MAIL_PASSWORD'] = 'AMDRyzen7'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

conn = sqlite3.connect('DSSP.db')
cur = conn.cursor()
cur.execute('SELECT Name, Section FROM attendance where Present="P" ')
stu_att1 = cur.fetchall()
cur.execute('SELECT Name, Section FROM attendance where Present="A" ')
stu_att2 = cur.fetchall()

def get_db_connection():
    conn = sqlite3.connect('DSSP.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/sendpresent")
def sendpresent():
   msg = Message('Present Students Attendance', sender = '2019pietcssalvader144@poornima.org', recipients = ['s.r.nathaniel01@gmail.com'])
   msg.body = stu_att1
   df = pd.DataFrame(stu_att1)
   print(df)
   msg.body=str(df)
   mail.send(msg)
   return "Sent"

@app.route("/sendabsent")
def sendabsent():
   msg = Message('Absent Student Attendance', sender = '2019pietcssalvader144@poornima.org', recipients = ['s.r.nathaniel01@gmail.com'])
   msg.body = stu_att2
   df = pd.DataFrame(stu_att2)
   print(df)
   msg.body=str(df)
   mail.send(msg)
   return "Sent"

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

@app.route("/updatestudent")
def updatestudent():
    return render_template("updatestudent.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_faces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return frame

def generate_frames():
    camera = cv2.VideoCapture(0)  # Access the webcam (0 represents the default camera)

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Detect faces and draw rectangles around them
            frame_with_faces = detect_faces(frame)

            # Encode the frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame_with_faces)

            # Convert the frame to bytes
            frame_bytes = buffer.tobytes()

            # Yield the frame to the client
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/viewattendance")
def viewattendance():
    conn = sqlite3.connect('DSSP.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM attendance')
    users = cur.fetchall()
    return render_template("viewattendance.html",users=users)

@app.route("/viewusers")
def viewusers():
    conn = sqlite3.connect('DSSP.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    return render_template("viewusers.html",users=users)

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
                #flash('Wrong Credentials')
                return render_template("loginas.html")
            if len(data)>0:
                if(data[1]==password and data[0]==email):
                    #print("Re")
                    return render_template("teacherhome.html")
        except:  
            #flash("Wrong")
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
            #flash("Wrong")
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
            #flash("Wrong")
            return render_template("student.html")
        
if __name__ == "__main__":
	app.run(debug=True)
