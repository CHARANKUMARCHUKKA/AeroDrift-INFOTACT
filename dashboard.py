import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="AeroDrift Dashboard", layout="wide")
st.title("🛡️ AeroDrift Enterprise Dashboard")

API_URL = "http://localhost:8000/api/v1"

tab1, tab2, tab3 = st.tabs(["Topology", "Drift Alerts", "Audit History"])

with tab1:
    st.header("Cloud Topology Graph")
    try:
        res = requests.get(f"{API_URL}/topology")
        if res.status_code == 200:
            data = res.json()
            st.metric("Total Nodes", len(data.get("nodes", [])))
            st.metric("Total Edges", len(data.get("edges", [])))
            st.json(data)
        else:
            st.error("Failed to fetch topology")
    except Exception as e:
        st.warning("API Server offline.")
