import os
import psycopg2
from sqlalchemy import create_engine
import streamlit as st


def get_db_environment():
    try:
        return st.secrets.db_credentials
    except AttributeError:
        return {
            "database": os.environ.get("DATABASE"),
            "user": os.environ.get("USER"),
            "password": os.environ.get("PASSWORD"),
            "host": os.environ.get("HOST"),
            "port": os.environ.get("PORT"),
        }


@st.cache_resource(ttl=3600)
def get_db_connector():
    sec = get_db_environment()
    connector = psycopg2.connect(**sec)
    return connector


@st.cache_resource(ttl=3600)
def get_db_engine():
    sec = get_db_environment()
    db_engine = create_engine(
        f"postgresql://{sec.user}:{sec.password}@{sec.host}:{sec.port}/{sec.database}"
    )
    return db_engine
