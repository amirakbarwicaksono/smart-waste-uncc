# import streamlit as st
# import pandas as pd

# LOG_FILE = "logs/transactions.csv"

# st.header("📊 Dashboard")

# try:
#     df = pd.read_csv(LOG_FILE)

#     st.subheader("Recent Activity")
#     st.dataframe(df.tail(20), use_container_width=True)

#     st.subheader("Bin Usage Count")
#     st.bar_chart(df["bin_type"].value_counts())

#     st.subheader("Waste Distribution")
#     st.bar_chart(df["waste_type"].value_counts())

# except:
#     st.warning("No data available yet.")

import streamlit as st
import pandas as pd
import time
import os

LOG_FILE = "logs/transactions.csv"

st.set_page_config(layout="wide")

st.header("📊 Smart Waste Real-Time Dashboard")

# =============================
# AUTO REFRESH
# =============================
refresh_rate = st.sidebar.slider("Refresh (seconds)", 1, 10, 2)

# =============================
# BIN LIST
# =============================
BINS = ["recycling", "food_waste", "other", "harmful"]

# =============================
# MAIN LOOP
# =============================
placeholder = st.empty()

while True:

    with placeholder.container():

        if os.path.exists(LOG_FILE):
            df = pd.read_csv(LOG_FILE)

            if len(df) > 0:

                # =============================
                # GET LAST STATE PER BIN
                # =============================
                latest = df.sort_values("timestamp").groupby("bin_type").tail(1)

                # =============================
                # UI: 4 BIN STATUS
                # =============================
                st.subheader("🗑️ Bin Status (Real-Time)")

                cols = st.columns(4)

                for i, bin_name in enumerate(BINS):

                    with cols[i]:

                        bin_data = latest[latest["bin_type"] == bin_name]

                        if not bin_data.empty:
                            state = bin_data.iloc[0]["bin_state"]

                            if state == "open":
                                st.markdown(f"### {bin_name.upper()}")
                                st.success("🟢 OPEN")
                            else:
                                st.markdown(f"### {bin_name.upper()}")
                                st.error("🔴 CLOSED")

                        else:
                            st.markdown(f"### {bin_name.upper()}")
                            st.warning("No Data")

                # =============================
                # CHARTS
                # =============================
                st.subheader("📈 Analytics")

                col1, col2 = st.columns(2)

                with col1:
                    st.write("Bin Usage")
                    bin_counts = df["bin_type"].value_counts().reset_index()
                    bin_counts.columns = ["bin_type", "count"]

                    st.bar_chart(bin_counts.set_index("bin_type"))

                with col2:
                    st.write("Waste Distribution")
                    waste_counts = df["waste_type"].value_counts().reset_index()
                    waste_counts.columns = ["waste_type", "count"]

                    st.bar_chart(waste_counts.set_index("waste_type"))

                # =============================
                # TABLE
                # =============================
                st.subheader("📄 Recent Activity")
                st.dataframe(df.tail(20), use_container_width=True)

            else:
                st.warning("Log file empty.")

        else:
            st.warning("No data available yet.")

    time.sleep(refresh_rate)