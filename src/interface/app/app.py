import pandas as pd
import streamlit as st 

from authentication import Authentication
from api_request import ApiRequest
from database_handler import DatabaseHandler
from plots import (
    candlestick_plot,
    scatter_plot,
    format_data,
)


st.set_page_config(
    layout="centered", page_title="Make Us Rich", page_icon=":moneybag:"
)
st.title("Make Us Rich")
st.subheader("Cryptocurrency Forecasting Dashboard 📈")
st.markdown("""
    ![Version](https://img.shields.io/badge/Version-1.0-green?style=flat-square)
    ![Streamlit](https://img.shields.io/badge/Streamlit-1.4.0-yellow?style=flat-square)
    ![License](https://img.shields.io/badge/License-Apache_2.0-orange?style=flat-square)

    Visit our [GitHub repository](https://github.com/ChainYo/make-us-rich) for source code.   
    Visit the project's 📖 [documentation](https://chainyo.github.io/make-us-rich/) for more information.
""")

api = ApiRequest()
authentication = Authentication()
username, role, token, authentication_status = authentication.login("login")

if authentication_status:
    menu_choices = ["Forecasting", "API Token", "Admin"] if role == "admin" else ["Forecasting", "API Token"]
    menu_choice = st.sidebar.selectbox("Menu", menu_choices)

    if menu_choice == "Forecasting":
        st.subheader("Forecasting")
        st.markdown("""
            """)
        st.session_state["available_models"] = api.number_of_available_models()
        if "models" in st.session_state["available_models"]:
            for model in st.session_state["available_models"]["models"]:
                curr, comp = model.split("_")
                response = api.prediction(curr, comp, token)
                if "error" not in response:
                    DatabaseHandler.increment_user_api_consumption(username)
                    data, prediction = format_data(response)
                    with st.expander(f"{curr.upper()}/{comp.upper()}"):
                        st.plotly_chart(scatter_plot(data, curr, comp, prediction))
                        st.plotly_chart(candlestick_plot(data, curr, comp, prediction))
        else:
            st.markdown("No models available.")

    elif menu_choice == "API Token":
        st.subheader("API Token")
        st.markdown("""
            🚧 This feature is not available yet.

            This is your personal API token. Never share it with anyone.
            You can use this forecasting service directly in your scripts by making API calls with this token.

            You can find more information about the API usage in the [Make Us Rich documentation](https://chainyo.github.io/make-us-rich/)
        """)
        with st.expander(label="⚠️ API Token", expanded=False):
            if authentication_status:
                st.markdown(f"Your API token is: `{token}`")
            else:
                st.markdown("You need to be logged in to see your API token.")
        user_api_consumption = DatabaseHandler.get_user_api_consumption(username)
        if user_api_consumption["success"]:
            st.markdown(f"""
            You API consumption is limited to 1000 calls per month.

            **You have already consumed: {user_api_consumption["consumption"]}/1000 calls.**
            """)
            st.progress(int(user_api_consumption["consumption"])/1000)
        else:
            st.markdown(f"""
            You API consumption is limited to 1000 calls per month.

            Something went wrong: {user_api_consumption["error"]}
            """)

    elif menu_choice == "Admin":
        st.subheader("Admin")
        st.markdown("""
            """)

