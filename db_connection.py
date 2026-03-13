from sqlalchemy import create_engine
import streamlit as st

DB_USER = "postgres"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "superstore_db"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

 ## test the connection##
 
st.title("Database connection test")

try:
    conn = engine.connect()
    st.success("Connected to PostgreSQL successfully!")
    conn.close()
except Exception as e:
    st.error(f"Connection failed: {e}")