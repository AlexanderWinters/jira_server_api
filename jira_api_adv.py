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


#API CALL DEF
def api_deploy(server, username, password, protocol, endpoint, call_type, payload):
    auth = HTTPBasicAuth(username, password)
    url = protocol + server + endpoint
    response = requests.request(
        call_type, 
        url,
        data=payload, 
        headers=headers, 
        auth=auth)
    return response

def api_call_test(server, username, password, protocol):
    auth = HTTPBasicAuth(username, password)
    api = "/rest/auth/1/session"
    url = protocol + server + api
    response = requests.get(url, auth=auth)
    return response
#PAYLOAD FUNCTIONS
def bulk_users(creds, file, delimiter):
    endpoint = "/rest/api/2/user"
    call_type = "POST"
    with open (file) as csvfile:
        reader=csv.DictReader(csvfile, delimiter=delimiter)
        for row in reader:
            emailAddress = row['emailAddress']
            displayName = row['displayName']
            name = row['name']
            key = row['password']

            #USER PAYLOAD
            payload = json.dumps( {
                "emailAddress": emailAddress, 
                "displayName": displayName, 
                "name": name, 
                "password": key
                } )
            response = api_deploy(creds["server"],
                                  creds["username"],
                                  creds["password"],
                                  creds["protocol"],
                                  endpoint=endpoint, call_type=call_type, payload=payload)


#What is needed from the app: server creds, project key, category id,
def bulk_projects(creds, catid, file, delimiter):
    endpoint = "/rest/api/2/project"
    call_type = "POST"
    url = creds["protocol"] + creds["server"]

    with open(file) as csvfile:
        reader=csv.DictReader(csvfile, delimiter=delimiter)
        for row in reader:
            group_number = row['Group Number']
            group_name = row['Group Name']
            leader = row['Project Leader']
            p_key = row['Project Key'] + group_number
            if row['Project Name']:
                p_name = row['Project Name']
            else:
                p_name = p_key + group_name
            project_description = group_name
        
            #PAYLOAD
            payload = json.dumps( {
                "key": p_key,
                "name": p_name,
                "projectTypeKey": "software",
                "projectTemplateKey": "com.pyxis.greenhopper.jira:gh-scrum-template",
                "description": project_description,
                "lead": leader,
                "url": url,
                "assigneeType": "PROJECT_LEAD",
                "avatarId": 10200,
                #"issueSecurityScheme": 10001,
                #"permissionScheme": 10011,
                #"notificationScheme": 10021,
                "categoryId": catid
            } )
            api_deploy(creds["server"],
                       creds["username"],
                       creds["password"],
                       creds["protocol"], endpoint=endpoint, call_type=call_type, payload=payload)
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

def get_projects(creds):
    endpoint = "/rest/api/2/projectCategory"
    call_type = "GET"
    url = creds["protocol"] + creds["server"] + endpoint
    auth = HTTPBasicAuth(creds["username"], creds["password"])
    response = requests.request(
        call_type, 
        url,
        headers=headers, 
        auth=auth)
    formatted_response = json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
    return formatted_response
    #print(response)
    #print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))


