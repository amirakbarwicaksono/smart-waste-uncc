import streamlit as st
# Sesuaikan import get_listener/get_messages dengan lokasi asli file listener Anda
# Contoh: dari core.mqtt.listener import ... 
# (Sesuaikan line di bawah ini dengan struktur file listener Anda)
from core.mqtt.listener import get_listener, get_messages 

def init_state():
    if 'latest_user_id' not in st.session_state:
        st.session_state.latest_user_id = None
    if 'mqtt_started' not in st.session_state:
        st.session_state.mqtt_started = False

def sync_mqtt_session():
    if not st.session_state.get('mqtt_started'):
        try:
            get_listener()
            st.session_state.mqtt_started = True
        except:
            return None

    messages = get_messages()
    if messages:
        last_uid = messages[-1].get('user_id')
        if last_uid:
            st.session_state.latest_user_id = last_uid
            return last_uid
    return None