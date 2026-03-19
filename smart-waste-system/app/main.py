# ----------- app/main.py -----------

import streamlit as st

st.set_page_config(
    page_title="Smart Waste System",
    layout="wide"
)

st.title("♻️ Smart Waste Management System")

st.markdown("""
### Welcome 👋

Use the sidebar to navigate:

- 👤 User → Scan & dispose waste  
- 🛠️ Admin → Test classification  
- 📊 Dashboard → Monitor bins in real-time  
""")