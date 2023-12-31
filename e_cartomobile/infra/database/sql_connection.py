import psycopg2
from sqlalchemy import create_engine
import streamlit as st


@st.cache_resource(ttl=3600)
def get_db_connector():
    connector = psycopg2.connect(**st.secrets.db_credentials)
    return connector

@st.cache_resource(ttl=3600)
def get_db_engine():
    sec = st.secrets.db_credentials
    db_engine = create_engine(f'postgresql://{sec.user}:{sec.password}@{sec.host}:{sec.port}/{sec.database}')
    return db_engine