from flask import Flask, render_template, request, session
from dotenv import load_dotenv
import gspread
import random
import os
import resend
import datetime
load_dotenv()
API_KEY= os.getenv("RESEND_API_KEY")
resend.api_key=API_KEY

connection=gspread.service_account(filename="robotics-attendance-505719-469542db1a26.json")
spreadsheet=connection.open_by_key("1wBvikd-lND2i-rx7CW4u8vMQSOYtKxtLs3ZV_Lnhp4c")
worksheet=spreadsheet.worksheet("Students")
worksheet2=spreadsheet.worksheet("Attendance")
#connects the website to the google sheet using google cloud console 

app = Flask(__name__)
app.config.update(SECRET_KEY="session_data")

@app.route("/")
def home():
    return "Attendance System" 

@app.route("/register", methods=["GET","POST"])
#routes the code to specific page and recieves & post
def register():
    if(request.method=="POST"):
        email=request.form.get("email")
        name=request.form.get("name")
        subteam=request.form.get("subteam")
        #gets the input from the form submitted in registration page
        if email in worksheet.col_values(1):
            return "You're already registered."
        #checks for duplicate emails
        worksheet.append_row([email,name,subteam,"Yes"])
        session["email"]=email
        #Adds to google sheet and stores email
        return "Registration was successful"
        
    else:
        return render_template("register.html")
    
@app.route("/checkin",methods=["GET","POST"]) 
def checkin(): 
    if(request.method=="POST"):
        email=session["email"] 
        number=random.randint(100000,999999) 
        session["code"]=number 
        #Generates random 6-digit code and saves in session
        params={"subject":"Verification Code for Checkin", "text":f"This is your verification code for today's session: {number}", "to":email, "from":"onboarding@resend.dev"} 
        #Create verification email
        send=resend.Emails.send(params) 
        return render_template("checkin.html")
    return render_template("checkin.html")

@app.route("/verify", methods=["GET","POST"]) 
def verify(): 
    code=request.form.get("code") 
    num=int(code)
    #gets the code and converts it to integer
    if (num==session["code"]): 
        current=datetime.datetime.now()
        #stores current date and time
        row_email=worksheet.find(session["email"])
        row=row_email.row
        email=session["email"]
        name=worksheet.cell(row,2).value
        subteam=worksheet.cell(row,3).value
        #it finds the students name and subteam from students google sheet
        date=str(current.date())
        time=str(current.time())
        #stores current date and time in 2 individual variables
        worksheet2.append_row([email,name,date,time,"",subteam])
        return "You're checked in!" 
    else: 
        return "The code is incorrect. Please try again" 
    #adds row in attendance google sheet and/or returns messages accordingly

@app.route("/checkout",methods=["GET","POST"])
def checkout():
    if(request.method=="POST"):
        email=session["email"]
        number=random.randint(100000,999999) 
        session["code"]=number 
        params={"subject":"Verification Code for Checkout", "text":f"This is your verification code to end today's session: {number}", "to":email, "from":"onboarding@resend.dev"} 
        send=resend.Emails.send(params)
        return render_template("checkout.html")
    return render_template("checkout.html")

@app.route("/confirm",methods=["GET","POST"])
def confirm():
    code=request.form.get("code")
    num=int(code)
    if(num==session["code"]):
        current=datetime.datetime.now()
        row_email=worksheet2.find(session["email"])
        row=row_email.row
        time=str(current.time())
        worksheet2.update_cell(row,5,time)
        return "You're checked out!"
    else: 
        return "The code is incorrect. Please try again"
if __name__ == "__main__": 
    app.run(debug=True)
