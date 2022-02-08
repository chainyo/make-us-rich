import streamlit as st 

from database_handler import DatabaseHandler
from authentication import Authentication


st.set_page_config(
    layout="centered", page_title="Make Us Rich", page_icon=":moneybag:"
)
st.title("Make Us Rich")
st.subheader("Cryptocurrency Forecasting Dashboard 📈")
st.markdown("""
    ![Version](https://img.shields.io/badge/Version-1.0-green)
    ![Streamlit](https://img.shields.io/badge/Streamlit-1.4.0-yellow)
    ![License](https://img.shields.io/badge/License-Apache_2.0-orange)
""")
with st.expander("About"):
    st.markdown("""
    """)

authentication = Authentication()
username, role, authentication_status = authentication.login("login")

if authentication_status:
    pass

