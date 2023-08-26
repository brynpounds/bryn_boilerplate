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

# Build Audit Rule from Rules in Array
def dictionary(comp_rule, counter):
    AUDIT_RULE = {counter : dictionary_builder(comp_rule)}
    return AUDIT_RULE

# Build Audit Rule from List of Rules in Array
def dictionary_list(comp_rule, counter):
    AUDIT_RULE = {counter : multi_dictionary_builder(comp_rule)}
    return AUDIT_RULE

# Build a Dictionary of Dictionaries for auditing CONFIGs
def dictionary_builder(comp_rule):
    if (comp_rule['CustomPolicy']['Rules']['Rule']['Conditions']['Condition']['Scope']):
        scope = comp_rule['CustomPolicy']['Rules']['Rule']['Conditions']['Condition']['Scope']
    else:
        scope = "none"
    if (comp_rule['CustomPolicy']['Rules']['Rule']['Conditions']['Condition']['Operator']):
        operator = comp_rule['CustomPolicy']['Rules']['Rule']['Conditions']['Condition']['Operator']
    else:
        operator = "none"
    if (comp_rule['CustomPolicy']['Rules']['Rule']['Conditions']['Condition']['Value']):
        value = comp_rule['CustomPolicy']['Rules']['Rule']['Conditions']['Condition']['Value']
    else:
        value = "none"
    if ('Violation' in comp_rule['CustomPolicy']['Rules']['Rule']['Conditions']['Condition']):
        msg = comp_rule['CustomPolicy']['Rules']['Rule']['Conditions']['Condition']['Violation']['Message']
    else:
        msg = "none"
    #print("\n\nCheck ",scope," ",operator," ",value," if in violation present: ",msg)
    RULE = {'Scope': scope, "Operator": operator, "Value": value, "Message": msg}
    return RULE

# Build a Dictionary of Multiple Dictionaries for auditing CONFIGs
def multi_dictionary_builder(comp_rule):
    subcounter = 0
    RULE = {}
    for i in range(len(comp_rule['CustomPolicy']['Rules']['Rule']['Conditions'])):
        if (comp_rule['CustomPolicy']['Rules']['Rule']['Conditions']['Condition'][i]['Scope']):
            scope = comp_rule['CustomPolicy']['Rules']['Rule']['Conditions']['Condition'][i]['Scope']
        else:
            scope = "none"
        if (comp_rule['CustomPolicy']['Rules']['Rule']['Conditions']['Condition'][i]['Operator']):
            operator = comp_rule['CustomPolicy']['Rules']['Rule']['Conditions']['Condition'][i]['Operator']
        else:
            operator = "none"
        if (comp_rule['CustomPolicy']['Rules']['Rule']['Conditions']['Condition'][i]['Value']):
            value = comp_rule['CustomPolicy']['Rules']['Rule']['Conditions']['Condition'][i]['Value']
        else:
           value = "none"
        if ('Violation' in comp_rule['CustomPolicy']['Rules']['Rule']['Conditions']['Condition'][i]):
            msg = comp_rule['CustomPolicy']['Rules']['Rule']['Conditions']['Condition'][i]['Violation']['Message']
        else:
            msg = "none"
        #scope = comp_rule['CustomPolicy']['Rules']['Rule']['Conditions']['Condition'][i]['Scope']
        print("\n\nCheck ",scope," ",operator," ",value," if in violation present: ",msg)
        rule = {subcounter :{'Scope': scope, "Operator": operator, "Value": value, "Message": msg}}
        rule.update(rule)
        subcounter = subcounter + 1
    RULE = {subcounter : rule}
    print(RULE)
    return RULE

# Read one XML file
def xml_file_reader(DIRECTORY):
    os.chdir(DIRECTORY)
    # parse the XML file
    with open('ISB_IOS_XE_1-1-1.xml', 'r') as f:
        xml_file = f.read()
    return xml_file

# Read all XML files
def all_files_into_dict(DIRECTORY):
    audit_database = {}
    counter = 0
    # parse the all the xml files
    for filename in os.listdir(DIRECTORY):
        if filename.endswith('.xml'):
            filepath = os.path.join(DIRECTORY, filename)
            with open(filepath, 'r') as f:
                xml_str = f.read()
            comp_rule = xmltodict.parse(xml_str)
            #print("\n\n",comp_rule)
            if type(comp_rule['CustomPolicy']['Rules']['Rule']['Conditions']['Condition']) != list :
                #audit_rule = dictionary_builder_single(comp_rule, counter)
                #print("\n\n",audit_rule)
                audit_database.update(dictionary(comp_rule, counter))
                #print("\n\n",audit_database)
                counter = counter + 1
            else:
                audit_database.update(dictionary_list(comp_rule, counter))
                counter = counter + 1
    return audit_database

#deal with array of conditions next

#     ----------------------------- MAIN -----------------------------

AUDIT_DATABASE = {}

COMPLIANCE_DIRECTORY = "IOSXE"
CONFIG_DATA = os.path.join(CONFIG_PATH, CONFIG_STORE)
COMP_CHECKS = os.path.join(CONFIG_PATH, COMPLIANCE_STORE, COMPLIANCE_DIRECTORY)

# Single file test 
#xml_file = xml_file_reader(COMP_CHECKS)
#comp_rule = xmltodict.parse(xml_file)
#print(f"Read the XML Compliance Rule:\n\n",comp_rule,"\n")
#AUDIT_DATABASE.update(dictionary_builder(comp_rule,0))

# Multi file test
AUDIT_DATABASE = all_files_into_dict(COMP_CHECKS)
print(f"And now loaded into an object for processing against configs\n\n",AUDIT_DATABASE)
