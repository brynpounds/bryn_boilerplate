#!/usr/bin/env python3

####################################################################################
# project: DNAC-ComplianceMon
# module: primecompliance.py
# author: kebaldwi@cisco.com
# use case: Simple Check of XML audit files against configuration
# developers:
#            Gabi Zapodeanu, TME, Enterprise Networks, Cisco Systems
#            Keith Baldwin, TSA, EN Architectures, Cisco Systems
####################################################################################

# This program is written to meet the requirements set out in the README.md

#     ------------------------------- IMPORTS -------------------------------
import os
import sys
import os.path
import datetime
import time

import utils
import difflib
import re  # needed for regular expressions matching
import logging
import warnings


import json
import xml
import xml.dom.minidom
import json
import xml.etree.ElementTree as ET
import xmltodict
import select
import socket  # needed for IPv4 validation
import ipaddress  # needed for IPv4 address validation

from config import CONFIG_PATH, CONFIG_STORE, COMPLIANCE_STORE

#     ----------------------------- DEFINITIONS -----------------------------

def xml_to_dict(xml_str):
    root = ET.fromstring(xml_str)
    result = {}
    for child in root:
        if len(child) == 0:
            result[child.tag] = child.text
        else:
            result[child.tag] = xml_to_dict(ET.tostring(child))
    return result

def xml_file_reader(CONFIG_PATH, COMPLIANCE_STORE, COMPLIANCE_DIRECTORY):
    COMP_CHECKS = os.path.join(CONFIG_PATH, COMPLIANCE_STORE, COMPLIANCE_DIRECTORY)
    os.chdir(COMP_CHECKS)
    # parse the XML file
    with open('ISB_IOS_XE_1-1-1.xml', 'r') as f:
        xml_file = f.read()
    return xml_file

#     ----------------------------- MAIN -----------------------------
AUDIT_DATABASE = {}
COMPLIANCE_DIRECTORY = "IOSXE"
CONFIG_DATA = os.path.join(CONFIG_PATH, CONFIG_STORE)

xml_file = xml_file_reader(CONFIG_PATH, COMPLIANCE_STORE, COMPLIANCE_DIRECTORY)

comp_rule = xmltodict.parse(xml_file)
print("Read the XML Compliance Rule:\n\n",comp_rule,"\n\n")

# print the variables to make sure they contain the expected values
scope = comp_rule['CustomPolicy']['Rules']['Rule']['Conditions']['Condition']['Scope']
operator = comp_rule['CustomPolicy']['Rules']['Rule']['Conditions']['Condition']['Operator']
value = comp_rule['CustomPolicy']['Rules']['Rule']['Conditions']['Condition']['Value']
msg = comp_rule['CustomPolicy']['Rules']['Rule']['Conditions']['Condition']['Violation']['Message']

print("Check ",scope," ",operator," ",value," if in violation present: ",msg)

AUDIT_RULE = {'CompRule1' : {'Scope': scope, "Operator": operator, "Value": value, "Message": msg}}

# Create a new dictionary of dictionaries
#new_dict = {'item2': {'key3': 'value3', 'key4': 'value4'}}

# Append the new dictionary of dictionaries to the original dictionary
AUDIT_DATABASE.update(AUDIT_RULE)

print("\n\nAnd now loaded into an object for processing against configs\n\n",AUDIT_DATABASE)