# DNA Center Compliance Monitor
Using Cisco DNA Center for Configuration Monitoring and Compliance and sending notifications as incidents to ServiceNow

This repo will use xml formatted compliance rules from Cisco DNA Center to how to detect and mitigate unauthorized, or non-compliant configuration changes and notify ServiceNow or via Email.

- This repo is based on ConfigMon-DNAC by Gabi Z
- Compliance Engine additions by Keith Baldwin
- Docker/Flask/Swagger packaging by Bryn Pounds

## The Challenge: 
 - 70% of policy violations are due to user errors
 - Configuration drifting
 - non compliant code
 - compliancy audits

## The Goal: 
 - Detect and alert on all network configuration changes
 - Report on Non Complaint configurations

## The Solution:
 - Integration between Cisco DNA Center, ServiceNow, IOS XE Programmability, and Webex Teams
 - The application may run on demand, scheduled or continuously

## Workflow:
 - Collect network devices running configurations using the Cisco DNA Center Command Runner APIs
 - Create a local folder with all the running configurations
 - If the device is new, add the configuration to the local folder
 - If device is known, check for configuration changes
 - If a change occurred, identify who made the change, the device name, physical location and device health
 - Identify what changed and the relevant section of the configuration
 - Inspect against provided compliance policies:
   - no logging configuration changes, 
   - no access control lists configuration,
   - prevent IPv4 duplicate addresses
   - check for non compliant configurations using xml audits from Prime

## The Results: 
 - Non compliant configuration changes are notified and reported
 - Troubleshooting assistance by providing a real time view of all device configuration changes
 
## Setup and Configuration
 - The requirements.txt file include all the Python libraries needed for this application
 - This application requires:
   - Cisco DNA Center
 - The config.py is the only file needed to be customized to match your environment

## Roadmap:
 - Automate roll back of non-compliant changes
 - Approval process for all compliant configuration changes
 - Build a web based dashboard
 - Create additional compliance checks
 - Create northbound APIs to provide additional services like - device configuration file retrieval, configurations search, archiving, reporting

## Future Setup Configurations and Roadmap
 - In the future this application will requires:
   - IOS XE devices configured for NETCONF and RESTCONF
   - Cisco Webex Teams account
   - ServiceNow developer account
