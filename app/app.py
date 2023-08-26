from flask import Flask, render_template, send_from_directory, request, url_for, flash, redirect
import json
import requests
import time
import subprocess
from subprocess import PIPE
from dotenv import load_dotenv


try:
    from API import (app,
                     api,
                     HeathController,docs,
                     WeatherController
                     )
except Exception as e:
    print("Modules are Missing : {} ".format(e))
    
messages=["howdy"]
    
@app.route("/")
def home():
    my_var = "Howdy"
    return render_template("home.html", message = my_var)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/configure_system", methods=('GET', 'POST'))
def configure_system():
    if request.method == 'POST':
        ip_address = request.form['ip_address']
        username = request.form['username']
        password = request.form['password']
        file1 = open('/app/config.py', 'w')
        #file1.writelines("\nNew DNAC URL: " + ip_address + "\nNew Username :" + username + "\nNew Password: " + password)
        file1.write('''####################################################################################
# project: DNAC-ComplianceMon
# module: config.py
# author: kebaldwi@cisco.com
# use case: Simple Check of XML audit files against configuration
# developers:
#            Gabi Zapodeanu, TME, Enterprise Networks, Cisco Systems
#            Keith Baldwin, TSA, EN Architectures, Cisco Systems
#            Bryn Pounds, PSA, WW Architectures, Cisco Systems
####################################################################################

import socket

# This file contains the:
# DNAC username and password, server info and file locations

# Update this section with the DNA Center server info and user information
DNAC_IP = "''' + ip_address + '''"
DNAC_USER = "''' + username + '''"
DNAC_PASS = "''' + password + '''"
DNAC_URL = 'https://' + DNAC_IP
DNAC_FQDN = socket.getfqdn(DNAC_IP)

# Update this section for Email Notification
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
# Enter your address
SMTP_EMAIL = "sender@gmail.com"
SMTP_PASS = "16-digit-app-password"
# Enter receiver address
NOTIFICATION_EMAIL = "receiver@gmail.com"

# Update this section for the Time Zone
TIME_ZONE = 'US/Eastern'

# File location to be used for configurations05a356
CONFIG_PATH = f"./"
CONFIG_STORE = f"DNAC-CompMon-Data/Configs/"
JSON_STORE = f"DNAC-CompMon-Data/JSONdata/"
REPORT_STORE = f"API/static/"
COMPLIANCE_STORE = f"PrimeComplianceChecks/"''')
        file1.close()  
        if not ip_address:
            flash('IP Address is required!')
        elif not username:
            flash('Username is required!')        
        elif not password:
            flash('Password is required!')
        else:
            messages.append({'ip_address': ip_address, 'username': username, 'password':password})
            return redirect(url_for('status'))    
    return render_template("configure_system.html", messages=messages)

@app.route("/report", methods=('GET', 'POST'))
def serve_report():
    ########  If this pages is accessed with an HTTP POST via the submit button...   
    if request.method == 'POST':
        message = "Reports...(HTTP POST)"
        file_copy = subprocess.run(["mv", "/app/DNAC-CompMon-Data/Reports/*.pdf", "/app/API/static/", "/dev/null"], stdout=PIPE, stderr=PIPE)
        result = subprocess.run(["ls", "-l", "/app/API/static/", "/dev/null"], stdout=PIPE, stderr=PIPE)
        contents = result.stdout.decode('utf8')    
        return render_template('report.html', message=message, reports=contents.split("total")[1])
              
    ########  If this pages is accessed with an HTTP GET...
    message = "Reports... (HTTP GET)"
    result = subprocess.run(["ls", "-l", "/app/API/static/", "/dev/null"], stdout=PIPE, stderr=PIPE)
    contents = result.stdout.decode('utf8')    
    return render_template('report.html', message=message, reports=contents.split("total")[1])

@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/status")
def status():
    url = 'http://localhost:8080/health_check'
    response = requests.get(url)
    our_response_content = response.content.decode('utf8')
    proper_json_response = json.loads(our_response_content)
    return render_template("status.html", testing=proper_json_response)

@app.route("/weather")
def weather():
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    
    json_data = {
        'city': 'Overland Park',
        'zip': '66085',
    }
    
    response = requests.post('http://localhost:8080/check_weather', headers=headers, json=json_data)    
    our_response_content = response.content.decode('utf8')
    proper_json_response = json.loads(our_response_content)
    return render_template("weather.html", message="HOWDY", testing=proper_json_response)

api.add_resource(HeathController, '/health_check')
docs.register(HeathController)

api.add_resource(WeatherController, '/check_weather')
docs.register(WeatherController)



if __name__ == '__main__':
    app.run(threaded=True)