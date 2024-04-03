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

from dotenv import load_dotenv

#SERVER INIT
server = "server"
username = input("Enter username: ")
password = input("Enter password: ")
auth = HTTPBasicAuth(username,password)

endpoint = "api endpoint" #DEFINED BY FUNCTION
call_type = "POST" #DEFINED BY FUNCTION
payload = ({
    "data": "data"
}) #DEFINED BY FUNCTION

headers = {"Accept": "application/json", "Content-Type": "application/json"}

def bulk_users():
    endpoint = "/rest/api/2/project"
    call_type = "POST"
    #parser = OptionParser() DEPRECATED
    file = input("csv to read: ")
    delimiter = input("csv seperator used: ")
    while delimiter!="," or delimiter!=";" or delimiter!=".":
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
    



def bulk_projects():
    endpoint = "/rest/api/2/user"
    #parser = OptionParser() DEPRECATED
    file = input("csv to read: ")
    delimiter = input("csv seperator used: ")
    while delimiter!="," or delimiter!=";" or delimiter!=".":
        delimiter=input("ERROR Invalid delimiter. Use a valid seperator (, : ;): ")
    with open(file) as csvfile:
        reader=csv.DictReader(csvfile, delimiter=delimiter)
        for row in reader:
            group_number = row['Group Number']
            group_name = row['Group Name']
            project_leader = row['Project Leader']

            #PAYLOAD VARIABLES
            load_dotenv()
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

def get_projects():
    endpoint = "/rest/api/2/projectCategory"
    call_type = "GET"


api_call = "http://" + server + endpoint
response = requests.request(
    call_type, 
    api_call, 
    data=payload, 
    headers=headers, 
    auth=auth)