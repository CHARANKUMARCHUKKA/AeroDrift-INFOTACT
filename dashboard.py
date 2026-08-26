import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="AeroDrift Dashboard", layout="wide")
st.title("🛡️ AeroDrift Enterprise Dashboard")

API_URL = "http://localhost:8000/api/v1"


if "token" not in st.session_state:
    st.session_state["token"] = None

if not st.session_state["token"]:
    st.subheader("Login to AeroDrift")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        res = requests.post(f"{API_URL}/token", data={"username": username, "password": password})
        if res.status_code == 200:
            st.session_state["token"] = res.json()["access_token"]
            st.rerun()
        else:
            st.error("Invalid credentials")
    st.stop()

tab1, tab2, tab3 = st.tabs(["Topology", "Drift Alerts", "Audit History"])

with tab1:
    st.header("Cloud Topology Graph")
    try:
        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        res = requests.get(f"{API_URL}/topology", headers=headers)
        if res.status_code == 200:
            data = res.json()
            st.metric("Total Nodes", len(data.get("nodes", [])))
            st.metric("Total Edges", len(data.get("edges", [])))
            st.json(data)
        else:
            st.error("Failed to fetch topology")
    except Exception as e:
        st.warning("API Server offline.")

with tab2:
    st.header("Active Security Drifts")
    if st.button("Run Security Scan"):
        try:
            headers = {"Authorization": f"Bearer {st.session_state['token']}"}
            res = requests.get(f"{API_URL}/drift", headers=headers)
            if res.status_code == 200:
                data = res.json()
                if data["status"] == "secure":
                    st.success("All systems secure! No drift detected.")
                else:
                    st.error("Vulnerabilities Detected!")
                    for alert in data["alerts"]:
                        st.warning(alert)
        except Exception:
            st.warning("API Server offline.")

with tab3:
    st.header("Historical Audit Logs")
    if st.button("Load History"):
        try:
            headers = {"Authorization": f"Bearer {st.session_state['token']}"}
            res = requests.get(f"{API_URL}/history", headers=headers)
            if res.status_code == 200:
                data = res.json()
                df = pd.DataFrame(data["history"])
                st.dataframe(df)
        except Exception:
            st.warning("API Server offline.")
