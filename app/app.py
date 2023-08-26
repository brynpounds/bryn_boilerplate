from flask import Flask, render_template, send_from_directory, request, url_for, flash, redirect
import json
import requests
import time
import subprocess
from subprocess import PIPE
from dotenv import load_dotenv
from config import DNAC_URL, DNAC_PASS, DNAC_USER
from compliance_mon import *
load_dotenv()

try:
    from API import (app,
                     api,
                     HeathController,docs,
                     KeithController,
                     WeatherController,
                     DNACTokenController,
                     get_all_device_infoController,
                     get_device_infoController,
                     delete_deviceController,
                     get_project_idController,
                     get_project_infoController,
                     create_commit_templateController,
                     commit_templateController,
                     update_commit_templateController,
                     upload_templateController,
                     delete_templateController,
                     get_all_template_infoController,
                     get_template_name_infoController,
                     get_template_idController,
                     get_template_id_versionController,
                     get_template_id_versionController,
                     deploy_templateController,
                     check_template_deployment_statusController,
                     get_client_infoController,
                     locate_client_ipController,
                     get_device_id_nameController,
                     get_device_statusController,
                     get_device_management_ipController,
                     get_device_id_snController,
                     get_device_locationController,
                     create_siteController,
                     get_site_idController,
                     create_buildingController,
                     get_building_idController,
                     create_floorController,
                     get_floor_idController,
                     assign_device_sn_buildingController,
                     assign_device_name_buildingController,
                     get_geo_infoController,
                     sync_deviceController,
                     check_task_id_statusController,
                     check_task_id_outputController,
                     create_path_traceController,
                     get_path_trace_infoController,
                     check_ipv4_network_interfaceController,
                     get_device_info_ipController,
                     get_legit_cli_command_runnerController,
                     get_content_file_idController,
                     get_output_command_runnerController,
                     get_all_configsController,
                     get_device_configController,
                     check_ipv4_addressController,
                     check_ipv4_address_configsController,
                     check_ipv4_duplicateController,
                     get_device_healthController,
                     pnp_get_device_countController,
                     pnp_get_device_listController,
                     pnp_claim_ap_siteController,
                     pnp_delete_provisioned_deviceController,
                     pnp_get_device_infoController,
                     get_physical_topologyController                     
                     
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
    global DNAC_IP
    global DNAC_USER
    global DNAC_PASS
    global DNAC_URL
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
        DNAC_IP = ip_address
        DNAC_USER = username
        DNAC_PASS = password
        DNAC_URL = 'https://' + DNAC_IP
        
        
        
        if not ip_address:
            flash('IP Address is required!')
        elif not username:
            flash('Username is required!')        
        elif not password:
            flash('Password is required!')
        else:
            messages.append({'ip_address': ip_address, 'username': username, 'password':password})
            return redirect(url_for('status'))    
    return render_template("configure_system.html", messages=messages, DNAC_URL= DNAC_IP)

@app.route("/report", methods=('GET', 'POST'))
def serve_report():
    ########  If this pages is accessed with an HTTP POST via the submit button...   
    ########  (This code by Keith Baldwin)
    if request.method == 'POST':
        message = "Reports..."
        file_copy = subprocess.run(["mv", "/app/DNAC-CompMon-Data/Reports/*.pdf", "/app/API/static/", "/dev/null"], stdout=PIPE, stderr=PIPE)
        result = subprocess.run(["ls", "-l", "/app/API/static/", "/dev/null"], stdout=PIPE, stderr=PIPE)
        contents = result.stdout.decode('utf8')    
        
        time.sleep(2)
        os_setup()
        AUDIT_DATABASE = {}
        COMPLIANCE_DIRECTORY = "IOSXE"
        COMP_CHECKS = os.path.join(CONFIG_PATH, COMPLIANCE_STORE, COMPLIANCE_DIRECTORY)
        AUDIT_DATABASE = all_files_into_dict(COMP_CHECKS)
        Config_Files, Report_Files, Json_Files = data_library(CONFIG_PATH,CONFIG_STORE,REPORT_STORE,JSON_STORE)
        os.chdir(Config_Files)
    
        temp_run_config = "temp_run_config.txt"
        
        # logging, debug level, to file {application_run.log}
        logging.basicConfig(
            filename='application_run.log',
            level=logging.DEBUG,
            format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
        dnac_token = dnac_apis.get_dnac_jwt_token(DNAC_AUTH)
        
        # get the DNA C managed devices list (excluded wireless, for one location)
        all_devices_info = dnac_apis.get_all_device_info(dnac_token)
        all_devices_hostnames = []
        for device in all_devices_info:
            if device['family'] == 'Switches and Hubs' or device['family'] == 'Routers':
                all_devices_hostnames.append(device['hostname'])
            
        # Get the current date time in UTC timezone
        now_utc = datetime.datetime.now(pytz.UTC)
        # Convert to timezone
        time_zone = 'US/Eastern'
        tz = pytz.timezone(time_zone)
        now_tz = now_utc.astimezone(tz)
        # Format the date and time string
        date_str = now_tz.strftime('%m/%d/%Y').replace('/', '_')
        time_str = now_tz.strftime('%H:%M:%S').replace(':', '_')
        
        # get the config files, compare with existing (if one existing). Save new config if file not existing.
        for device in all_devices_hostnames:
            device_run_config = dnac_apis.get_device_config(device, dnac_token)
            filename = str(device) + '_' + date_str + '_run_config.txt'
            
            # save the running config to a temp file
            f_temp = open(temp_run_config, 'w')
            f_temp.write(device_run_config)
            f_temp.seek(0)  # reset the file pointer to 0
            f_temp.close()
            
            # check for existing configuration file
            # if yes; run the check for changes; diff function
            # if not; save; run the diff function
            # expected result create local config "database"
            
            if os.path.isfile(filename):
                diff = compare_configs(filename, temp_run_config)
                
                if diff != '':
                    # retrieve the device location using DNA C REST APIs
                    location = dnac_apis.get_device_location(device, dnac_token)
                    # find the users that made configuration changes
                    with open(temp_run_config, 'r') as f:
                        user_info = 'User info no available'
                        for line in f:
                            if 'Last configuration change' in line:
                                user_info = line
                    
                    # define the incident description and comment
                    short_description = 'Configuration Change Alert - ' + device
                    comment = 'The device with the name: ' + device + '\nhas detected a Configuration Change'
                                        
                    # get the device health from DNA Center
                    current_time_epoch = utils.get_epoch_current_time()
                    device_details = dnac_apis.get_device_health(device, current_time_epoch, dnac_token)
                    
                    device_sn = device_details['serialNumber']
                    device_mngmnt_ip_address = device_details['managementIpAddr']
                    device_family = device_details['platformId']
                    device_os_info = device_details['osType'] + ',  ' + device_details['softwareVersion']
                    device_health = device_details['overallHealth']
                    
                    updated_comment = '\nDevice location: ' + location
                    updated_comment += '\nDevice family: ' + device_family
                    updated_comment += '\nDevice OS info: ' + device_os_info
                    updated_comment += '\nDevice S/N: ' + device_sn
                    updated_comment += '\nDevice Health: ' + str(device_health) + '/10'
                    updated_comment += '\nDevice management IP address: ' + device_mngmnt_ip_address
                    updated_comment = '\nThe configuration changes are\n' + diff + '\n\n' + user_info
                else:
                    print('Device: ' + device + ' - No configuration changes detected')
            else:
                # new device discovered, save the running configuration to a file in the folder with the name
                # {Config_Files}
                
                f_config = open(filename, 'w')
                f_config.write(device_run_config)
                f_config.seek(0)
                f_config.close()
                
                # retrieve the device management IP address
                device_mngmnt_ip_address = dnac_apis.get_device_management_ip(device, dnac_token)
        report = compliance_run("./", AUDIT_DATABASE, Report_Files, Json_Files)
        time.sleep(2)
        return render_template('report.html', message=message, reports=contents.split("total")[1], debug=report)
              
    ########  If this pages is accessed with an HTTP GET...
    message = "Reports..."
    result = subprocess.run(["ls", "-l", "/app/API/static/", "/dev/null"], stdout=PIPE, stderr=PIPE)
    contents = result.stdout.decode('utf8')    
    return render_template('report.html', message=message, reports=contents.split("total")[1])

@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/status")
def status():
    file1 = open('/app/config.py', 'r')
    contents = file1.read()
    file1.close()
    
    
    url = 'http://localhost:8080/health_check'
    response = requests.get(url)
    our_response_content = response.content.decode('utf8')
    proper_json_response = json.loads(our_response_content)
    return render_template("status.html", testing=proper_json_response, DNAC_URL=DNAC_URL, DNAC_USER=DNAC_USER, messages=messages, contents=contents)

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
    #url = 'http://192.241.187.136/data/2.5/weather?zip=66085,us&appid=11a1aac6bc7d01ea13f0d2a8e78c227e'
    #my_response = requests.get(url)
    our_response_content = response.content.decode('utf8')
    proper_json_response = json.loads(our_response_content)
    return render_template("weather.html", message="HOWDY", testing=proper_json_response)

api.add_resource(HeathController, '/health_check')
docs.register(HeathController)

api.add_resource(KeithController, '/keith_code')
docs.register(KeithController)

api.add_resource(WeatherController, '/check_weather')
docs.register(WeatherController)

api.add_resource(DNACTokenController, '/get_dnac_token')
docs.register(DNACTokenController)

api.add_resource(get_all_device_infoController, '/get_all_device_info')
docs.register(get_all_device_infoController)

api.add_resource(get_device_infoController, '/get_device_info')
docs.register(get_device_infoController)

api.add_resource(delete_deviceController, '/delete_device')
docs.register(delete_deviceController)

api.add_resource(get_project_idController, '/get_project_id')
docs.register(get_project_idController)

api.add_resource(get_project_infoController, '/get_project_info')
docs.register(get_project_infoController)

api.add_resource(create_commit_templateController, '/create_commit_template')
docs.register(create_commit_templateController)

api.add_resource(commit_templateController, '/commit_template')
docs.register(commit_templateController)

api.add_resource(update_commit_templateController, '/update_commit_template')
docs.register(update_commit_templateController)

api.add_resource(upload_templateController, '/upload_template')
docs.register(upload_templateController)

api.add_resource(delete_templateController, '/delete_template')
docs.register(delete_templateController)

api.add_resource(get_all_template_infoController, '/get_all_template_info')
docs.register(get_all_template_infoController)

api.add_resource(get_template_name_infoController, '/get_template_name_info')
docs.register(get_template_name_infoController)

api.add_resource(get_template_idController, '/get_template_id')
docs.register(get_template_idController)

api.add_resource(get_template_id_versionController, '/get_template_id_version')
docs.register(get_template_id_versionController)

api.add_resource(deploy_templateController, '/deploy_template')
docs.register(deploy_templateController)

api.add_resource(check_template_deployment_statusController, '/check_template_deployment_status')
docs.register(check_template_deployment_statusController)

api.add_resource(get_client_infoController, '/get_client_info')
docs.register(get_client_infoController)

api.add_resource(locate_client_ipController, '/locate_client_ip')
docs.register(locate_client_ipController)

api.add_resource(get_device_id_nameController, '/get_device_id_name')
docs.register(get_device_id_nameController)

api.add_resource(get_device_statusController, '/get_device_status')
docs.register(get_device_statusController)

api.add_resource(get_device_management_ipController, '/get_device_management_ip')
docs.register(get_device_management_ipController)

api.add_resource(get_device_id_snController, '/get_device_id_sn')
docs.register(get_device_id_snController)

api.add_resource(get_device_locationController, '/get_device_location')
docs.register(get_device_locationController)

api.add_resource(create_siteController, '/create_site')
docs.register(create_siteController)

api.add_resource(get_site_idController, '/get_site_id')
docs.register(get_site_idController)

api.add_resource(create_buildingController, '/create_building')
docs.register(create_buildingController)

api.add_resource(get_building_idController, '/get_building_id')
docs.register(get_building_idController)

api.add_resource(create_floorController, '/create_floor')
docs.register(create_floorController)

api.add_resource(get_floor_idController, '/get_floor_id')
docs.register(get_floor_idController)

api.add_resource(assign_device_sn_buildingController, '/assign_device_sn_building')
docs.register(assign_device_sn_buildingController)

api.add_resource(assign_device_name_buildingController, '/assign_device_name_building')
docs.register(assign_device_name_buildingController)

api.add_resource(get_geo_infoController, '/get_geo_info')
docs.register(get_geo_infoController)

api.add_resource(sync_deviceController, '/sync_device')
docs.register(sync_deviceController)

api.add_resource(check_task_id_statusController, '/check_task_id_status')
docs.register(check_task_id_statusController)

api.add_resource(check_task_id_outputController, '/check_task_id_output')
docs.register(check_task_id_outputController)

api.add_resource(create_path_traceController, '/create_path_trace')
docs.register(create_path_traceController)

api.add_resource(get_path_trace_infoController, '/get_path_trace_info')
docs.register(get_path_trace_infoController)

api.add_resource(check_ipv4_network_interfaceController, '/check_ipv4_network_interface')
docs.register(check_ipv4_network_interfaceController)

api.add_resource(get_device_info_ipController, '/get_device_info_ip')
docs.register(get_device_info_ipController)

api.add_resource(get_legit_cli_command_runnerController, '/get_legit_cli_command_runner')
docs.register(get_legit_cli_command_runnerController)

api.add_resource(get_content_file_idController, '/get_content_file_id')
docs.register(get_content_file_idController)

api.add_resource(get_output_command_runnerController, '/get_output_command_runner')
docs.register(get_output_command_runnerController)

api.add_resource(get_all_configsController, '/get_all_configs')
docs.register(get_all_configsController)

api.add_resource(get_device_configController, '/get_device_config')
docs.register(get_device_configController)

api.add_resource(check_ipv4_addressController, '/check_ipv4_address')
docs.register(check_ipv4_addressController)

api.add_resource(check_ipv4_address_configsController, '/check_ipv4_address_configs')
docs.register(check_ipv4_address_configsController)

api.add_resource(check_ipv4_duplicateController, '/check_ipv4_duplicate')
docs.register(check_ipv4_duplicateController)

api.add_resource(get_device_healthController, '/get_device_health')
docs.register(get_device_healthController)

api.add_resource(pnp_get_device_countController, '/pnp_get_device_count')
docs.register(pnp_get_device_countController)

api.add_resource(pnp_get_device_listController, '/pnp_get_device_list')
docs.register(pnp_get_device_listController)

api.add_resource(pnp_claim_ap_siteController, '/pnp_claim_ap_site')
docs.register(pnp_claim_ap_siteController)

api.add_resource(pnp_delete_provisioned_deviceController, '/pnp_delete_provisioned_device')
docs.register(pnp_delete_provisioned_deviceController)

api.add_resource(pnp_get_device_infoController, '/pnp_get_device_info')
docs.register(pnp_get_device_infoController)

api.add_resource(get_physical_topologyController, '/get_physical_topology')
docs.register(get_physical_topologyController)



if __name__ == '__main__':
    app.run(threaded=True)