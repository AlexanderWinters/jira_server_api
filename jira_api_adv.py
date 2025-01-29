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
    """
    Makes an API call to deploy a resource using the specified server, endpoint,
    protocol, and authentication credentials. This function is designed to
    initiate various types of API calls (e.g., GET, POST) by passing the HTTP
    method type, payload, and endpoint. It returns the response object that
    contains all the details of the API interaction.

    :param server: The domain or IP address of the server to which the API request
        is to be sent.
    :type server: str

    :param username: Username credential used for HTTP Basic Authentication.
    :type username: str

    :param password: Password credential used for HTTP Basic Authentication.
    :type password: str

    :param protocol: The protocol (e.g., 'http', 'https') to be used when connecting
        to the server.
    :type protocol: str

    :param endpoint: The specific API endpoint or path to append to the base URL to
        make the full API call.
    :type endpoint: str

    :param call_type: HTTP method used for the API call, such as 'GET', 'POST',
        'PUT', 'DELETE', etc.
    :type call_type: str

    :param payload: Data payload to be sent in the body of the request for HTTP
        methods like 'POST' or 'PUT'.
    :type payload: dict or None

    :return: The response object from the API call containing the status code,
        response headers, and body.
    :rtype: requests.Response
    """
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
    """
    Test API call using HTTP Basic Authentication.

    This function attempts to authenticate a user to a server using HTTP Basic
    Authentication and sends a GET request to the server's specified API endpoint.
    It constructs the complete URL from the provided server base URL and API endpoint,
    makes the request, and returns the response object.

    :param server: The base URL of the server to connect to (e.g., "example.com").
    :type server: str
    :param username: The username for HTTP Basic Authentication.
    :type username: str
    :param password: The password for HTTP Basic Authentication.
    :type password: str
    :param protocol: The protocol to use for connecting (e.g., "http://", "https://").
    :type protocol: str
    :return: The response object from the server after the GET request.
    :rtype: requests.Response
    """
    auth = HTTPBasicAuth(username, password)
    api = "/rest/auth/1/session"
    url = protocol + server + api
    response = requests.get(url, auth=auth)
    return response
#PAYLOAD FUNCTIONS
def bulk_users(creds, file, delimiter):
    """
    Bulk creates users using data from a CSV file and specified delimiter.

    This function reads user data from a provided CSV file, constructs payloads
    for user creation in the system via API calls, and processes those requests
    using the provided credentials and connection details.

    :param creds: Dictionary containing server credentials and connection
                  information. Required keys include "server", "username",
                  "password", and "protocol".
    :param file: Path to the CSV file containing user data. Each row must
                 have the fields: `emailAddress`, `displayName`, `name`,
                 and `password` with appropriate values.
    :param delimiter: Delimiter used in the CSV file to separate fields.
                      For example, `,` for standard CSV format.
    :return: The response from the API after processing the user's creation request.
    :rtype: Any
    """
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
            return response


#What is needed from the app: server creds, project key, category id,
def bulk_projects(creds, catid, file, delimiter):
    """
    Creates multiple Jira projects in bulk using input from a CSV file. The function reads the project details
    from a provided CSV file, constructs the project payload, and sends requests to the Jira API to create
    the projects based on the details provided in the file.

    :param creds: A dictionary containing credentials and connection details required to interact with the Jira API.
    :param catid: Integer ID representing the category to which the created projects belong.
    :param file: The file path of the CSV containing project details to create the projects.
    :param delimiter: The character used to delimit fields in the CSV file.
    :return: A response object resulting from the API request for project creation.
    """
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
            response = api_deploy(creds["server"],
                       creds["username"],
                       creds["password"],
                       creds["protocol"], endpoint=endpoint, call_type=call_type, payload=payload)
            return response
def bulk_delete_users(creds, file, delimiter):
    """
    Deletes multiple users from the system based on details provided in a CSV file.

    This function reads user details from the specified CSV file and sends a DELETE
    request for each username provided in the file. The connection settings and credentials
    are provided as an input argument.

    :param creds: A dictionary containing credentials and server details.
                  It should have the keys `protocol`, `server`, `username`,
                  and `password`.
    :param file: The file path to a CSV containing the user details.
    :param delimiter: The delimiter used in the CSV file to separate values.
    :return: The response of the DELETE request from the API for the last user in the
             CSV file.
    """
    endpoint = "/rest/api/2/user"
    call_type = "DELETE"
    with open(file) as csvfile:
        reader=csv.DictReader(csvfile, delimiter=delimiter)
        for row in reader:
            name = row['name']
            key = row['password']

            #PAYLOAD
            payload = "?" + "username=" + name #+ "&key=" + key
            norm_payload = payload.replace(" ", "%20")
            api_call = creds["protocol"] + creds["server"] + endpoint + norm_payload
            auth = HTTPBasicAuth(creds["username"], creds["password"])
            response = requests.request(
                call_type,
                api_call,
                data=payload,
                headers=headers,
                auth=auth)
            return response

def get_projects(creds):
    """
    Fetches and formats the list of project categories from the JIRA API.

    This function makes a GET request to the JIRA REST API to retrieve details
    about the project categories available in a JIRA instance specified by the
    `creds` dictionary. The response is formatted as a JSON string to improve
    readability and usability.

    :param creds: Dictionary containing credentials and server configuration
        required for the JIRA API request. It should include the following keys:
        - "protocol": Protocol type ("http" or "https").
        - "server": Server address (e.g., "jira.example.com").
        - "username": Username with access to the JIRA API.
        - "password": Corresponding password for the username.
    :return: The JSON-formatted string containing details of the project categories.
    :rtype: str
    """
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


