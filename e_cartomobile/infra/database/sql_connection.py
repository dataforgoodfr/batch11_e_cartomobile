import streamlit as st
import psycopg2


@st.cache_resource(ttl=3600)
def get_db_connector():
    connector = psycopg2.connect(**st.secrets.db_credentials)
    return connector
