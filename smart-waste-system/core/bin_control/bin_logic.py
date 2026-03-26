
# ----------- core/bin_control/bin_logic.py -----------
import streamlit as st
import time


def open_bin(bin_type):
    start = time.time()
    # st.warning(f" {bin_type} bin...")

    # Log open state immediately
    open_time = round(start, 2)

    with st.spinner("Loading..."):
        time.sleep(30)

    end = time.time()
    duration = round(end - start, 2)

    st.success(f"{bin_type} bin closed")

    return {
        "bin_type": bin_type,
        "open_timestamp": start,
        "close_timestamp": end,
        "duration": duration
    }
