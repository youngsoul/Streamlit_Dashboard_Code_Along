import streamlit as st

# YouTube: A Cozy follow-along introduction to Streamlit
#
# Url: https://www.youtube.com/watch?v=SVArhvcjnuE

##########################################
#### SETUP
##########################################
st.set_page_config(page_title="Financial Consumer Complaints",
                   page_icon=":phone:",
                   layout="wide")

complaints_page = st.Page(page="./app/complaints.py", title="Complaints")
about_page = st.Page(page="./app/about.py", title="About")

selected_page = st.navigation([complaints_page, about_page])
selected_page.run()
