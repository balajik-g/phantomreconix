# streamlit_app.py
import streamlit as st
import sys
import os

# Add project root to sys.path so 'app' can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.nmap_runner import run_nmap_scan
from app.zap_runner import run_zap_scan
from app.sqlmap_runner import run_sqlmap_scan
from app.api_runner import run_api_fuzz

st.set_page_config(page_title="PhantomReconix - Pentest UI", layout="wide")
st.title("🛡️ PhantomReconix - Autonomous Pentest UI")

# Sidebar - Input
target_url = st.sidebar.text_input("🔗 Enter Target URL", "http://localhost:3000")
selected_tools = st.sidebar.multiselect("🛠️ Select Tools", ["Nmap", "ZAP", "SQLMap", "API Fuzz"], default=["Nmap"])
start_scan = st.sidebar.button("🚀 Start Scan")

# Main - Summary
st.subheader("🔍 Scan Summary")
st.write(f"**Target:** `{target_url}`")
st.write(f"**Selected Tools:** {', '.join(selected_tools)}")

# Scan Results Tabs
if start_scan:
    st.success("✅ Scan started. Please wait...")
    with st.spinner("Running scans..."):
        if "Nmap" in selected_tools:
            with st.expander("📡 Nmap Scan Output"):
                result = run_nmap_scan(target_url)
                st.code(result)

        if "ZAP" in selected_tools:
            with st.expander("🛡️ ZAP Scan Output"):
                result = run_zap_scan(target_url)
                st.code(result)

        if "SQLMap" in selected_tools:
            with st.expander("🩻 SQLMap Scan Output"):
                result = run_sqlmap_scan(target_url)
                st.code(result)

        if "API Fuzz" in selected_tools:
            with st.expander("🔗 API Fuzz Scan Output"):
                result = run_api_fuzz(target_url)
                st.code(result)

    st.success("✅ All selected scans completed.")
