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

- 👤 **User Mode** → Scan barcode & dispose waste  
- 🛠️ **Admin Mode** → Test classification & override  
- 📊 **Dashboard** → Monitor bins in real-time
- 🎮 **Digital Twin** → Virtual representation of waste bins
""")

# Optional: tampilkan preview
st.divider()
st.caption("📌 Select a page from the sidebar to get started")