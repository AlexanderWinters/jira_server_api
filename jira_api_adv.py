import sys
import os
import csv
import json
import requests
import smtplib
import ssl

from requests.auth import HTTPBasicAuth
from optparse import OptionParser

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


#SERVER INIT
headers = {"Accept": "application/json", "Content-Type": "application/json"}
endpoint = "api endpoint" #DEFINED BY FUNCTION
call_type = "POST" #DEFINED BY FUNCTION
payload = ({
    "data": "data"
}) #DEFINED BY FUNCTION


#API CALL DEF
def api_deploy(server, username, password, protocol, endpoint, call_type, payload):
    auth = HTTPBasicAuth(username, password)
    api_call = protocol + server + endpoint
    print("Deploying to endpoint: " + api_call)
    response = requests.request(
        call_type, 
        api_call, 
        data=payload, 
        headers=headers, 
        auth=auth)

def api_call_test(server, username, password, protocol):
    auth = HTTPBasicAuth(username, password)
    api = "/rest/auth/1/session"
    url = protocol + server + api
    response = requests.get(url, auth=auth)
    return response
#PAYLOAD FUNCTIONS
def bulk_users():
    endpoint = "/rest/api/2/user"
    call_type = "POST"
    #parser = OptionParser() DEPRECATED
    file = input("csv to read: ")
    delimiter = input("csv seperator used: ")
    while delimiter!="," and delimiter!=";" and delimiter!=".":
        delimiter=input("ERROR Invalid delimiter. Use a valid seperator (, : ;): ")
    with open(file) as csvfile:
        reader=csv.DictReader(csvfile, delimiter=delimiter)
        for row in reader:
            emailAddress = row['emailAddress']
            displayName = row['displayName']
            name = row['name']
            password = row['password']

            #USER PAYLOAD
            payload = json.dumps( {
                "emailAddress": emailAddress, 
                "displayName": displayName, 
                "name": name, 
                "password": password 
                } )
            api_deploy(endpoint=endpoint, call_type=call_type, payload=payload)
    
def bulk_projects():
    endpoint = "/rest/api/2/project"
    #parser = OptionParser() DEPRECATED
    file = input("csv to read: ")
    delimiter = input("csv seperator used: ")
    while delimiter!="," and delimiter!=";" and delimiter!=".":
        delimiter=input("ERROR Invalid delimiter. Use a valid seperator (, : ;): ")
    with open(file) as csvfile:
        reader=csv.DictReader(csvfile, delimiter=delimiter)
        for row in reader:
            group_number = row['Group Number']
            group_name = row['Group Name']
            project_leader = row['Project Leader']

            #PAYLOAD VARIABLES
            project_key = os.getenv('PROJECT_KEY') +  group_number
            project_name = os.getenv('PROJECT_PREFIX') + group_name
            catID = os.getenv('CATEGORY_ID')
            project_description = group_name
        
            #PAYLOAD
            payload = json.dumps( {
                "key": project_key,
                "name": project_name,
                "projectTypeKey": "software",
                "projectTemplateKey": "com.pyxis.greenhopper.jira:gh-scrum-template",
                "description": project_description,
                "lead": project_leader,
                "url": "http://" + server,
                "assigneeType": "PROJECT_LEAD",
                "avatarId": 10200,
                #"issueSecurityScheme": 10001,
                #"permissionScheme": 10011,
                #"notificationScheme": 10021,
                "categoryId": catID
            } )
            api_deploy(endpoint=endpoint, call_type=call_type, payload=payload)
def bulk_delete_users():
    endpoint = "/rest/api/2/user"
    call_type = "DELETE"
    file = input("csv to read: ")
    delimiter = input("csv seperator used: ")
    while delimiter!="," and delimiter!=";" and delimiter!=".":
        delimiter=input("ERROR Invalid delimiter. Use a valid seperator (, : ;): ")
    with open(file) as csvfile:
        reader=csv.DictReader(csvfile, delimiter=delimiter)
        for row in reader:
            name = row['name']
            key = row['password']

            #PAYLOAD
            payload = "?" + "username=" + name #+ "&key=" + key
            norm_payload = payload.replace(" ", "%20")
            api_call = "http://" + server + endpoint + norm_payload
            print("Deploying to endpoint: " + api_call)
            response = requests.request(
                call_type,
                api_call,
                data=payload,
                headers=headers,
                auth=auth)

def get_projects():
    endpoint = "/rest/api/2/projectCategory"
    call_type = "GET"
    api_call = "http://" + server + endpoint
    response = requests.request(
        call_type, 
        api_call,
        headers=headers, 
        auth=auth)
    print(response)
    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))


