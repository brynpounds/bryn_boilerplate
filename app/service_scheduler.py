#!/usr/bin/env python3

####################################################################################
# project: DNAC-ComplianceMon
# module: service_scheduler.py
# author: kebaldwi@cisco.com
# use case: Simple Check of XML audit files against configuration
# developers:
#            Gabi Zapodeanu, TME, Enterprise Networks, Cisco Systems
#            Keith Baldwin, TSA, EN Architectures, Cisco Systems
#            Bryn Pounds, PSA, WW Architectures, Cisco Systems
####################################################################################

# This section builds maintains and schedules compliance audits.

#     ------------------------------- IMPORTS -------------------------------

import json
import os
import sched
import time

# Initialize scheduler
scheduler = sched.scheduler(time.time, time.sleep)

# Load settings from file
settings_file = "settings.json"
if os.path.exists(settings_file):
    with open(settings_file, "r") as f:
        settings = json.load(f)
else:
    settings = {"entries": []}

# Define function to run the scheduled program
def run_program():
    # Replace this with the code you want to run
    print("Scheduled program is running...")

# Define function to schedule the program
def schedule_program():
    # Get user input for scheduling parameters
    date_str = input("Enter date (YYYY-MM-DD): ")
    time_str = input("Enter time (HH:MM:SS): ")
    interval_str = input("Enter interval in seconds (0 for one-time only): ")
    
    # Convert input to timestamp and interval
    timestamp = time.mktime(time.strptime(date_str + " " + time_str, "%Y-%m-%d %H:%M:%S"))
    interval = int(interval_str)
    
    # Schedule the program
    scheduler.enterabs(timestamp, 1, run_program)
    
    # Save the scheduled entry to settings
    settings["entries"].append({"timestamp": timestamp, "interval": interval})
    
    # Save settings to file
    with open(settings_file, "w") as f:
        json.dump(settings, f)
    
    print("Program scheduled successfully.")

# Define function to edit scheduled entries
def edit_schedule():
    # Display current scheduled entries
    print("Current scheduled entries:")
    for i, entry in enumerate(settings["entries"]):
        print(f"{i+1}. {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(entry['timestamp']))} (interval: {entry['interval']} seconds)")
    
    # Get user input for entry to edit
    entry_num = int(input("Enter entry number to edit: "))
    entry = settings["entries"][entry_num-1]
    
    # Get user input for new scheduling parameters
    date_str = input(f"Enter new date ({time.strftime('%Y-%m-%d', time.localtime(entry['timestamp']))}): ")
    time_str = input(f"Enter new time ({time.strftime('%H:%M:%S', time.localtime(entry['timestamp']))}): ")
    interval_str = input(f"Enter new interval in seconds ({entry['interval']}): ")
    
    # Convert input to timestamp and interval
    timestamp = time.mktime(time.strptime(date_str + " " + time_str, "%Y-%m-%d %H:%M:%S"))
    interval = int(interval_str)
    
    # Reschedule the program
    scheduler.cancel(entry["event"])
    event = scheduler.enterabs(timestamp, 1, run_program)
    
    # Update the scheduled entry in settings
    entry["timestamp"] = timestamp
    entry["interval"] = interval
    entry["event"] = event
    
    # Save settings to file
    with open(settings_file, "w") as f:
        json.dump(settings, f)
    
    print("Program rescheduled successfully.")

# Schedule previously saved entries
for entry in settings["entries"]:
    event = scheduler.enterabs(entry["timestamp"], 1, run_program)
    entry["event"] = event

# Main loop for user interaction
while True:
    choice = input("Enter 's' to schedule a program, 'e' to edit a scheduled entry, or 'q' to quit: ")
    
    if choice == "s":
        schedule_program()
    
    elif choice == "e":
        edit_schedule()
    
    elif choice == "q":
        break
    
    else:
        print("Invalid choice. Please try again.")

