import streamlit as st
import pandas as pd
import json
import os
import time

DATA_FILE = os.path.join(os.path.dirname(__file__), "analyzed_alerts.json")

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return []

st.set_page_config(page_title="SOC AI Analyst Dashboard", layout="wide")

st.title("🛡️ SOC AI Analyst Dashboard")
st.markdown("Monitor and review AI-analyzed security alerts in real-time.")

data = load_data()

if st.button("Refresh Data"):
    data = load_data()

if not data:
    st.info("No analyzed alerts found yet. Provide some alerts to the log monitor.")
else:
    df = pd.DataFrame(data)
    
    # Overview Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Alerts", len(df))
    with col2:
        st.metric("High Severity", len(df[df['severity'].astype(str).str.lower() == 'high']) if 'severity' in df.columns else 0)
    with col3:
        unique_ips = df['source_ip'].nunique() if 'source_ip' in df.columns else 0
        st.metric("Unique Source IPs", unique_ips)
    with col4:
        st.metric("Latest Alert", df['timestamp'].iloc[-1] if not df.empty else "N/A")

    st.subheader("Alert Timeline & Overview")
    display_df = df[['timestamp', 'rule_id', 'severity', 'attack_type', 'source_ip', 'mitre_technique']].copy()
    display_df.sort_values(by='timestamp', ascending=False, inplace=True)
    st.dataframe(display_df, use_container_width=True)

    st.subheader("Recent SOC Reports")
    for idx, row in df.iloc[::-1].head(10).iterrows():
        with st.expander(f"Alert {row.get('id', 'Unknown')} - {row.get('attack_type', 'Unknown')} (Severity: {row.get('severity', 'Unknown')})"):
            st.text(row.get('report', 'No report available'))
