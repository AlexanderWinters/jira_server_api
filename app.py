import streamlit as st
import jira_api_adv as jira

# Change server connect to popup. Add a button that opens the popup. Have a status bar under the button.
# Expand the api call to also test the connection.
@st.dialog("Connect to Jira Server")
def server_connect():
    server= st.text_input("Server", help="Use either the IP address or the hostname")
    protocol = st.selectbox("Protocol", ["http://", "https://"])
    log1, log2 = st.columns(2)
    username = log1.text_input("Username", help="You have to be an admin user")
    password = log2.text_input("Password", type="password")
    connected = False
    if st.button("Connect to Jira"):
        # Here do the api test call
        try:
            response = jira.api_call_test(server, username, password, protocol)
            if response.status_code == 200:
                with st.spinner("Connecting..."):
                    import time
                    time.sleep(1)
                    st.success('Connected')
                    time.sleep(1)


                connected = True
                st.session_state.server_connect = {
                    "server": server,
                    "protocol": protocol,
                    "username": username,
                    "password": password,
                    "response": response,
                    "connected": connected}
                st.rerun()
            else:
                st.error(f'Failed to connect. Status code: {response.status_code}')
        except Exception as e:
            st.error('Error connecting to server. Make sure you are using a valid Jira server.')

@st.dialog("Add users in bulk")
def bulk_add_users():
    st.subheader("Upload CSV", divider="grey")
    csv = st.file_uploader(" ", type="csv",
                           help="Upload the CSV file to parse. You need to include displayName, email, username, password.",
                           accept_multiple_files=False)
    delimiter = st.selectbox("Delimiter", [",",";",":"],
                             help="Delimiter for CSV file. Default is ';'. You can open the file and see which character is used between the first values")
    if st.button("Parse and Add"):
        jira.bulk_users(st.session_state.server_connect["server"],
                        st.session_state.server_connect["username"],
                        st.session_state.server_connect["password"],
                        st.session_state.server_connect["protocol"],
                        csv, delimiter)

st.title("Jira Server API")
if st.button("Connect", use_container_width=True):
    server_connect()
if "server_connect" in st.session_state and st.session_state.server_connect["response"].status_code == 200:
    st.success("Connected at " + st.session_state.server_connect["server"])

st.subheader(" ")
st.subheader("Choose function: ", divider="grey")
col1, col2, col3, col4 = st.columns(4)
if col1.button("Bulk Users", use_container_width=True ):
    if "server_connect" in st.session_state and st.session_state.server_connect["connected"]:
        bulk_add_users()
    else :
        st.warning("Please connect to Jira server first.")
if col2.button("Bulk Projects", use_container_width=True ):
    st.write("Bulk Projects")
if col3.button("Bulk Delete Users", use_container_width=True ):
    st.write("Bulk Delete Users")
if col4.button("Bulk Project Details", use_container_width=True ):
    st.write("Bulk Project Details")