from flask import Flask, render_template, request, session
from dotenv import load_dotenv
import gspread
import random
import os
import resend
load_dotenv()
API_KEY= os.getenv("RESEND_API_KEY")
resend.api_key=API_KEY

connection=gspread.service_account(filename="robotics-attendance-505719-469542db1a26.json")
spreadsheet=connection.open_by_key("1wBvikd-lND2i-rx7CW4u8vMQSOYtKxtLs3ZV_Lnhp4c")
worksheet=spreadsheet.worksheet("Students")
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
    email=session["email"] 
    number=random.randint(100000,999999) 
    session["code"]=number 
    #Generates random 6-digit session and saves in session
    params={"subject":"verification code", "text":f"This is your verification code for today's session: {number}", "to":email, "from":"onboarding@resend.dev"} 
    #Create verification email
    send=resend.Emails.send(params) 
    return render_template("checkin.html")
