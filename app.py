import streamlit as st
import pandas as pd

def hello():
    st.write("Hello World!")

st.title("Jira Server API")
username = st.text_input("Username")
password = st.text_input("Password", type="password")
st.subheader("Choose function: ")
col1, col2, col3, col4 = st.columns(4)
if col1.button("Bulk Users", use_container_width=True ):
    st.write("Bulk Users")
if col2.button("Bulk Projects", use_container_width=True ):
    st.write("Bulk Projects")
if col3.button("Bulk Delete Users", use_container_width=True ):
    st.write("Bulk Delete Users")
if col4.button("Bulk Project Details", use_container_width=True ):
    st.write("Bulk Project Details")