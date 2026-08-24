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
