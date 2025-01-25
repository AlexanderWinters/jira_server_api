import streamlit as st
import jira_api_adv as jira

@st.dialog("Add users in bulk")
def bulk_add_users():
    st.subheader("Upload CSV", divider="grey")
    csv = st.file_uploader(" ", type="csv",
                           help="Upload the CSV file to parse. You need to include displayName, email, username, password.",
                           accept_multiple_files=False)
    delimiter = st.selectbox("Delimiter", [",",";",":"],
                             help="Delimiter for CSV file. Default is ';'. You can open the file and see which character is used between the first values")
    if st.button("Parse and Add"):
        jira.bulk_users(st.session_state, csv, delimiter)
        #OUTPUT STDOUT

@st.dialog("Add projects in bulk")
def bulk_add_projects():
    st.subheader("Upload CSV", divider="grey")
    csv = st.file_uploader(" ", type="csv",
                           help="Upload the CSV file to parse. You need to include group number, group name, project leader, project key, project name, category ID.",
                           accept_multiple_files=False)
    delimiter = st.selectbox("Delimiter", [",",";",":"],)
    catid=st.text_input("Category ID", help="You can find the category with the Project Details function")
    if st.button("Parse and Add"):
        jira.bulk_projects(st.session_state, catid, csv, delimiter)
        #OUTPUT STDOUT

@st.dialog("Project Details function")
def project_details():
    st.subheader("Project Details")
    if st.button("Request Project Details"):
        p_response = jira.get_projects(st.session_state)
        import pandas as pd
        df = pd.read_json(p_response)
        df.drop(columns=['self'], inplace=True)
        st.dataframe(df)
        #st.json(p_response)
    if st.button("Done"):
        st.rerun()

#TITLE AND INTRO
st.title("Jira API Functions")
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
            response = jira.api_call_test(server, username, password, protocol)
            if response.status_code == 200:
                with st.spinner("Connecting..."):
                    import time
                    time.sleep(1)

                st.session_state.connected = True
                st.session_state.server = server
                st.session_state.protocol = protocol
                st.session_state.username = username
                st.session_state.password = password
            else:
                st.error(f'Failed to connect. Status code: {response.status_code}')
        except Exception as e:
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
    bulk_add_projects()
    #if "connected" in st.session_state:
    #    st.write("create bulk projects")
    #else:
    #    st.warning("Please connect to Jira server first.")
if box3.button("Bulk Delete Users", help="Delete a bulk of users",use_container_width=True):
    if "connected" in st.session_state:
        st.write("delete users")
    else:
        st.warning("Please connect to Jira server first.")
if box4.button("Project Details", help="Get all project categories. Used if you want to add projects under a category",use_container_width=True):
    project_details()
    #if "connected" in st.session_state:
    #    st.write("get project details")
    #else:
    #    st.warning("Please connect to Jira server first.")