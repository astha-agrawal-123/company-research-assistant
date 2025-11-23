import streamlit as st

class Session:
    def __init__(self):
        if "cra_state" not in st.session_state:
            st.session_state.cra_state = {
                "company": "",
                "logs": [],
                "raw_research": {},
                "synthesis": "",
                "account_plan": {}
            }

    def get(self, key, default=None):
        return st.session_state.cra_state.get(key, default)

    def set(self, key, value):
        st.session_state.cra_state[key] = value

    def append_log(self, text):
        st.session_state.cra_state.setdefault("logs", []).append(text)

    def set_account_section(self, section, text):
        st.session_state.cra_state.setdefault("account_plan", {})[section] = text

    def clear(self):
        st.session_state.cra_state = {
            "company": "",
            "logs": [],
            "raw_research": {},
            "synthesis": "",
            "account_plan": {}
        }