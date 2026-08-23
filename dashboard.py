import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="AeroDrift Dashboard", layout="wide")
st.title("🛡️ AeroDrift Enterprise Dashboard")

API_URL = "http://localhost:8000/api/v1"

tab1, tab2, tab3 = st.tabs(["Topology", "Drift Alerts", "Audit History"])
