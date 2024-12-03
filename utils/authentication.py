import streamlit as st
import streamlit_authenticator as stauth
from functools import wraps
import yaml
from yaml.loader import SafeLoader
import os


# open auth_config.yaml file with current path taken into account
with open(f"{os.getcwd()}/.streamlit/auth_config.yaml", "r") as file:
    config = yaml.load(file, Loader=SafeLoader)


def login_required(func):
    """Decorator for requiring authentication."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        authenticator = stauth.Authenticate(
            config["credentials"],
            config["cookie"]["name"],
            config["cookie"]["key"],
            config["cookie"]["expiry_days"],
        )
        if not st.session_state["authentication_status"]:
            authenticator.login()
            st.stop()
        else:
            authenticator.logout()
            return func(*args, **kwargs)

    return wrapper


def log_activity(func):
    """Decorator for logging user activity."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        st.session_state.setdefault("activity_log", []).append(
            f"Accessed {func.__name__}"
        )
        return func(*args, **kwargs)

    return wrapper
