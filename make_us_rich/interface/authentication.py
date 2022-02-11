import jwt
import time

import streamlit as st
import extra_streamlit_components as stx

from datetime import datetime, timedelta
from typing import Tuple

from .database_handler import DatabaseHandler


class Authentication:
    def __init__(self, key: str = "mur-key", cookie_ttl: int = 10) -> Tuple[str, str, bool]:
        """
        Initialize the Authentication class.

        Parameters
        ----------
        cookie_ttl: int
            The time to live of the cookie. Default is 10.

        Returns
        -------
        Tuple[str, bool]:
            The token and the status of the authentication.
        """
        self.key = key
        self.cookie_ttl = cookie_ttl
        self.cookie_name = "make_us_rich_auth"

    
    def _generate_cookie_token(self) -> str:
        """
        Generate a random string to be used as the token for authentication cookie.

        Returns
        -------
        str:
            The JWT token.
        """
        return jwt.encode(
            payload={
                "username": st.session_state["username"], "expiration_date": self._generate_expiration_date()
            }, 
            key=self.key,
        )

    
    def _generate_expiration_date(self) -> str:
        """
        Generate the expiration date of the token.

        Returns
        -------
        str:
            The expiration date of the token.
        """
        return (datetime.utcnow() + timedelta(days=self.cookie_ttl)).timestamp()

    
    def _decode_token(self) -> str:
        """
        Decode the token.

        Returns
        -------
        str:
            The decoded token.
        """
        return jwt.decode(self.token, key=self.key, algorithms=["HS256"])


    def login(self, form_title: str) -> Tuple[str, str, bool]:
        """"""
        self.form_title = form_title
        cookie_manager = stx.CookieManager()

        if "authentication_status" not in st.session_state:
            st.session_state["authentication_status"] = None
        if "username" not in st.session_state:
            st.session_state["username"] = None
        if "role" not in st.session_state:
            st.session_state["role"] = None
        if "api_token" not in st.session_state:
            st.session_state["api_token"] = None

        if st.session_state["authentication_status"] != True:
            try:
                self.token = cookie_manager.get(self.cookie_name)
                self.token = self._decode_token()
                if self.token["expiration_date"] > datetime.utcnow().timestamp():
                    st.session_state["authentication_status"] = True
                    st.session_state["username"] = self.token["username"]
                else:
                    st.session_state["authentication_status"] = False
            except:
                st.session_state["authentication_status"] = None

        if st.session_state["authentication_status"] != True:
            login_form = st.form("Login")
            login_form.subheader(
                "Welcome 👋, please login first.\n"
                "If you don't have an account, it will be created automatically when you submit the form."
            )
            input_username_value = st.session_state["username"] if st.session_state["username"] else ""
            self.username = login_form.text_input("Username", value=input_username_value)
            self.password = login_form.text_input("Password", type="password")

            if login_form.form_submit_button("Submit"):
                user_exist = DatabaseHandler.check_if_user_exist(self.username)
                if user_exist["success"]:
                    results = DatabaseHandler.authentication(self.username, self.password)
                    login_message = f"{results['message']} Welcome back {self.username}! 🎉"
                else:
                    results = DatabaseHandler.create_user(self.username, self.password)
                    login_message = f"{results['message']} Welcome {self.username}! 🎉"
                if results["success"]:
                    st.session_state["authentication_status"] = True
                    st.session_state["username"] = results["username"]
                    self.token = self._generate_cookie_token()
                    cookie_manager.set(
                        self.cookie_name, self.token, 
                        expires_at=datetime.now() + timedelta(self.cookie_ttl)
                    )
                    st.success(login_message)
                    time.sleep(5)
                else:
                    st.error(results["message"])

        if st.session_state["authentication_status"] == True:
            st.session_state["role"] = DatabaseHandler._check_user_role(st.session_state["username"])["role"]
            st.session_state["api_token"] = DatabaseHandler.get_api_token(st.session_state["username"])["token"]
            st.sidebar.title("User Panel")
            st.sidebar.markdown(f"**{st.session_state['username']}**, log out by clicking the button below.", unsafe_allow_html=True)
            if st.sidebar.button("Logout", key="logout"):
                cookie_manager.delete(self.cookie_name)
                st.session_state["authentication_status"] = None
                st.session_state["username"] = None
                st.session_state["role"] = None
        
        return (
            st.session_state["username"], 
            st.session_state["role"], 
            st.session_state["api_token"],
            st.session_state["authentication_status"],
        )
