import streamlit as st
import jira_api_adv as jira


def hello():
    st.write("Hello World!")

st.title("Jira Server API")
# Change server connect to popup. Add a button that opens the popup. Have a status bar under the button.
# Expand the api call to also test the connection.
@st.dialog("Connect to Jira Server")
def server_connect():
    #status = "not connected"
    server= st.text_input("Server", help="Use either the IP address or the hostname")
    protocol = st.selectbox("Protocol", ["http://", "https://"])
    log1, log2 = st.columns(2)
    username = log1.text_input("Username", help="You have to be an admin user")
    password = log2.text_input("Password", type="password")
    if st.button("Connect to Jira"):
        # Here do the api test call
        try:
            response = jira.api_call_test(server, username, password, protocol)
            if response.status_code == 200:
                st.success('Connection successful!')
            else:
                st.error(f'Failed to connect. Status code: {response.status_code}')
        except Exception as e:
            st.error(f'Error connecting to server: {str(e)}')
        st.session_state.server_connect = {"server": server, "protocol": protocol, "username": username, "password": password , "response":response}
        st.rerun()

if st.button("Connect", use_container_width=True):
    server_connect()

if "server_connect" in st.session_state:
    if st.session_state.server_connect["response"].status_code == 200:
        st.write("Connected at " + st.session_state.server_connect["server"])
    else :
        st.write("Connection failed.")

st.header(" ")
st.subheader("Upload CSV", divider="grey")
csv = st.file_uploader(" ", type="csv", help="Upload the CSV file to parse. You need to include displayName, email, username, password.",accept_multiple_files=False)
st.header(" ")
st.subheader("Choose function: ", divider="grey")
col1, col2, col3, col4 = st.columns(4)
if col1.button("Bulk Users", use_container_width=True ):
    st.write("Bulk Users")
if col2.button("Bulk Projects", use_container_width=True ):
    st.write("Bulk Projects")
if col3.button("Bulk Delete Users", use_container_width=True ):
    st.write("Bulk Delete Users")
if col4.button("Bulk Project Details", use_container_width=True ):
    st.write("Bulk Project Details")