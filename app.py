import requests
import streamlit as st
from requests import RequestException

import jira_api_adv as jira

@st.dialog("Add users in bulk")
def bulk_add_users():
    """
    Handles the functionality to upload and parse a CSV file for bulk adding of users,
    and performs the operation by triggering the integration with Jira's API. Provides
    visual and interactive components for the user to upload files, select delimiters,
    and perform actions to handle user addition workflow.

    :raises RequestException: If the connection to the Jira API fails.
    :raises DeprecationWarning: If any streamlit deprecations occur during the usage.
    """
    st.subheader("Upload CSV", divider="grey")
    csv = st.file_uploader(" ", type="csv",
                           help="Upload the CSV file to parse. You need to include displayName, email, username, password.",
                           accept_multiple_files=False)
    delimiter = st.selectbox("Delimiter", [",",";",":"],
                             help="Delimiter for CSV file. Default is ';'. You can open the file and see which character is used between the first values")
    if st.button("Parse and Add"):
        jira.bulk_users(st.session_state, csv, delimiter)
        try:
            response = jira.bulk_users(st.session_state, csv, delimiter) #BULK USERS RESPONSE
            if response.status_code == requests.codes.ok:
                st.success("Successfully added users")
                if st.button("Done"):
                    st.rerun()
        except RequestException as e:
            st.error(f'Failed to connect. Status code: {test_response.status_code}')
        #OUTPUT STDOUT

@st.dialog("Add projects in bulk")
def bulk_add_projects():
    """
    Handles the bulk addition of projects to a system via an uploaded CSV file. The function provides
    a graphical interface using Streamlit to upload a CSV file, specify a delimiter, and input a category ID.
    It then parses the data and submits it to the system for bulk project creation. The system provides
    feedback to the user regarding the success or failure of the process.

    :return: None
    """
    st.subheader("Upload CSV", divider="grey")
    csv = st.file_uploader(" ", type="csv",
                           help="Upload the CSV file to parse. You need to include group number, group name, project leader, project key, project name, category ID.",
                           accept_multiple_files=False)
    delimiter = st.selectbox("Delimiter", [",",";",":"],)
    catid=st.text_input("Category ID", help="You can find the category with the Project Details function")
    if st.button("Parse and Add"):
        jira.bulk_projects(st.session_state, catid, csv, delimiter)
        try:
            response = jira.bulk_projects(st.session_state, catid, csv, delimiter) #BULK PROJECT RESPONSE
            if response.status_code == requests.codes.ok:
                st.success("Successfully added projects")
                if st.button("Done"):
                    st.rerun()
        except RequestException as e:
            st.error(f'Failed to connect. Status code: {test_response.status_code}')
        #OUTPUT STDOUT

@st.dialog("Project Details function")
def project_details():
    """
    Handles the interactive user interface to display project details fetched
    from JIRA. Allows users to request project details and render them within
    a Streamlit dataframe. Provides options to finalize the operation and
    redirect the application flow.

    Exceptions during API calls or data processing are managed externally.

    :raises: This function does not explicitly raise errors. Errors
             during API calls, JSON parsing, or data processing
             should be handled by external mechanisms.

    :return: None
    """
    st.subheader("Project Details")
    if st.button("Request Project Details"):
        p_response = jira.get_projects(st.session_state)
        import pandas as pd
        df = pd.read_json(p_response)
        df.drop(columns=['self'], inplace=True)
        st.dataframe(df)
        #st.json(p_response)
    if st.button("Done", type="primary"):
        st.rerun()

@st.dialog("Delete users in bulk")
def bulk_delete_users():
    """
    Handles the bulk deletion of users by uploading a CSV file containing user data and
    parsing it using a specified delimiter. The method interfaces with an external service
    to execute the deletion operations and displays appropriate user feedback based on
    the response received.

    :raises RequestException: If the connection to the external service fails.
    :param csv: CSV file containing user data for deletion.
    :type csv: file-like
    :param delimiter: Character used to separate values in the CSV file.
    :type delimiter: str
    :rtype: None
    """
    st.subheader("Upload CSV", divider="grey")
    csv = st.file_uploader(" ", type="csv",
                           help="Upload the CSV file to parse. You need to include name",
                           accept_multiple_files=False)
    delimiter = st.selectbox("Delimiter", [",",";",":"],
                             help="Delimiter for CSV file. Default is ';'. You can open the file and see which character is used between the first values")
    if st.button("Parse and Delete"):
        try:
            response = jira.bulk_delete_users(st.session_state, csv, delimiter) #DELETE RESPONSE
            if response.status_code == requests.codes.ok:
                st.success("Successfully deleted")
                if st.button("Done"):
                    st.rerun()
        except RequestException as e:
            st.error(f'Failed to connect. Status code: {test_response.status_code}')
        #OUTPUT STDOUT

#TITLE AND INTRO
st.set_page_config(
    page_title="Jira Tools",
    page_icon="🛠️",
    #layout="wide",
    #initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/AlexanderWinters/jira_server_api',
        'Report a bug': "https://github.com/AlexanderWinters/jira_server_api/issues",
        'About': "Trying to make Jira suck a little less. Follow me on Github for more cool projects. https://github.com/AlexanderWinters"
    }
)
st.title("Jira API Toolbox")
st.subheader("Expand your Jira instance functionality with this tool.", help="First, connect to your Jira instance, and then pick a function to run.")

#CONNECTION CONTAINER - CONNECT TO SERVER
with st.container(border=True):
    server = st.text_input("Server", help="Use either the IP address or the hostname")
    protocol = st.selectbox("Protocol", ["http://", "https://"])
    log1, log2 = st.columns(2)
    username = log1.text_input("Username", help="You have to be an admin user")
    password = log2.text_input("Password", type="password")
    if st.button("Connect"):#, use_container_width=True):
        try:
            test_response = jira.api_call_test(server, username, password, protocol)
            if test_response.status_code == 200:
                with st.spinner("Connecting..."):
                    import time
                    time.sleep(1)

                st.session_state.connected = True
                st.session_state.server = server
                st.session_state.protocol = protocol
                st.session_state.username = username
                st.session_state.password = password
            else:
                st.error(f'Failed to connect. Status code: {test_response.status_code}')
        except RequestException as e:
            st.error('Error connecting to server. Make sure you are using a valid Jira server.')

if "connected" in st.session_state:
    st.success('Connected to Jira as ' + st.session_state.username)

st.divider()
st.subheader("Choose function: ")
box1, box2 = st.columns(2)
box3, box4 = st.columns(2)
if box1.button("Bulk Users", help="Create a bulk of users", use_container_width=True):
    if "connected" in st.session_state:
        bulk_add_users()
    else :
        st.warning("Please connect to Jira server first.")
if box2.button("Bulk Projects", help="Create a bulk of projects. If you want to create the projects in a category, run first Project Details.",use_container_width=True):
    if "connected" in st.session_state:
        bulk_add_projects()
    else:
        st.warning("Please connect to Jira server first.")
if box3.button("Bulk Delete Users", help="Delete a bulk of users",use_container_width=True):
    if "connected" in st.session_state:
        bulk_delete_users()
    else:
        st.warning("Please connect to Jira server first.")
if box4.button("Project Details", help="Get all project categories. Used if you want to add projects under a category",use_container_width=True):
    if "connected" in st.session_state:
        project_details()
    else:
        st.warning("Please connect to Jira server first.")