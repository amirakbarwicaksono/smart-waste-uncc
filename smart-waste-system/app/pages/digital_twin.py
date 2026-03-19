import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta
import numpy as np

LOG_FILE = "logs/transactions.csv"

st.header("🎮 Digital Twin - Human Behavior Analytics")

# =============================
# SIDEBAR CONTROLS
# =============================
st.sidebar.subheader("⏰ Time Range")
time_range = st.sidebar.selectbox(
    "Select period:",
    ["Last Hour", "Last 6 Hours", "Last 24 Hours", "Last 7 Days", "All Time"],
    index=2
)

refresh_rate = st.sidebar.slider("Refresh Rate (seconds)", 1, 10, 2)

# =============================
# HELPER FUNCTIONS
# =============================
def filter_by_time(df, time_range):
    """Filter dataframe based on selected time range"""
    if len(df) == 0 or time_range == "All Time":
        return df
    
    now = datetime.now()
    if time_range == "Last Hour":
        cutoff = now - timedelta(hours=1)
    elif time_range == "Last 6 Hours":
        cutoff = now - timedelta(hours=6)
    elif time_range == "Last 24 Hours":
        cutoff = now - timedelta(days=1)
    elif time_range == "Last 7 Days":
        cutoff = now - timedelta(days=7)
    else:
        return df
    
    df['datetime'] = pd.to_datetime(df['timestamp'])
    return df[df['datetime'] >= cutoff]

def get_user_behavior(df):
    """Analyze user behavior patterns"""
    if len(df) == 0:
        return pd.DataFrame()
    
    # Get only open events for user analysis
    user_actions = df[df["bin_state"] == "open"].copy()
    
    if len(user_actions) == 0:
        return pd.DataFrame()
    
    # Group by user
    user_stats = user_actions.groupby("barcode").agg({
        "timestamp": "count",
        "bin_type": lambda x: x.mode()[0] if len(x.mode()) > 0 else "unknown",
        "waste_type": lambda x: x.mode()[0] if len(x.mode()) > 0 else "unknown",
        "bin_duration_sec": "mean"
    }).rename(columns={
        "timestamp": "total_actions",
        "bin_type": "favorite_bin",
        "waste_type": "favorite_waste",
        "bin_duration_sec": "avg_duration"
    }).round(1)
    
    # Add last active time
    last_active = user_actions.groupby("barcode")["timestamp"].max()
    user_stats["last_active"] = pd.to_datetime(last_active).dt.strftime("%H:%M:%S")
    
    return user_stats.sort_values("total_actions", ascending=False)

def get_hourly_pattern(df):
    """Analyze hourly usage patterns"""
    if len(df) == 0:
        return pd.DataFrame()
    
    df_copy = df[df["bin_state"] == "open"].copy()
    if len(df_copy) == 0:
        return pd.DataFrame()
    
    df_copy["hour"] = pd.to_datetime(df_copy["timestamp"]).dt.hour
    hourly = df_copy.groupby("hour").size()
    
    # Fill missing hours
    all_hours = pd.DataFrame(index=range(24))
    hourly = hourly.reindex(all_hours.index, fill_value=0)
    
    return hourly

def get_bin_transitions(df):
    """Track how users move between bins"""
    if len(df) == 0:
        return pd.DataFrame()
    
    # Sort by user and timestamp
    df_sorted = df[df["bin_state"] == "open"].sort_values(["barcode", "timestamp"])
    
    # Create transition pairs
    transitions = []
    for user in df_sorted["barcode"].unique():
        user_data = df_sorted[df_sorted["barcode"] == user]
        bins = user_data["bin_type"].tolist()
        for i in range(len(bins) - 1):
            transitions.append({
                "from_bin": bins[i],
                "to_bin": bins[i + 1]
            })
    
    if transitions:
        trans_df = pd.DataFrame(transitions)
        return trans_df.groupby(["from_bin", "to_bin"]).size().reset_index(name="count")
    return pd.DataFrame()

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
                
                # Apply time filter
                df_filtered = filter_by_time(df, time_range)
                
                # =============================
                # REAL-TIME HUMAN ACTIVITY METRICS
                # =============================
                st.subheader("👥 Live Human Activity")
                
                col1, col2, col3, col4 = st.columns(4)
                
                # Active users in last 5 minutes
                now = datetime.now()
                five_min_ago = now - timedelta(minutes=5)
                df['datetime'] = pd.to_datetime(df['timestamp'])
                active_users = df[df['datetime'] >= five_min_ago]['barcode'].nunique()
                
                with col1:
                    st.metric("Active Users Now", active_users, delta=None)
                
                # Total users in selected period
                total_users = df_filtered['barcode'].nunique()
                with col2:
                    st.metric("Total Users", total_users)
                
                # Total actions
                total_actions = len(df_filtered[df_filtered["bin_state"] == "open"])
                with col3:
                    st.metric("Total Actions", total_actions)
                
                # Actions per user
                actions_per_user = round(total_actions / total_users, 1) if total_users > 0 else 0
                with col4:
                    st.metric("Avg Actions/User", actions_per_user)
                
                st.divider()
                
                # =============================
                # BIN STATUS WITH HUMAN INTERACTION
                # =============================
                st.subheader("🗑️ Bin Status - Real Time")
                
                latest = df.sort_values("timestamp").groupby("bin_type").tail(1)
                open_events = df_filtered[df_filtered["bin_state"] == "open"]
                
                cols = st.columns(4)
                
                for i, bin_name in enumerate(BINS):
                    with cols[i]:
                        bin_data = latest[latest["bin_type"] == bin_name]
                        
                        if not bin_data.empty:
                            state = bin_data.iloc[0]["bin_state"]
                            last_time = bin_data.iloc[0]["timestamp"][-8:]
                            last_user = str(bin_data.iloc[0]["barcode"])
                            last_waste = bin_data.iloc[0]["waste_type"]
                            total_uses = len(open_events[open_events["bin_type"] == bin_name])
                            unique_users = df_filtered[df_filtered["bin_type"] == bin_name]['barcode'].nunique()
                            
                            if state == "open":
                                st.markdown(f"### {bin_name.upper()}")
                                st.success("🟢 OPEN")
                                st.caption(f"👤 Current: User {last_user[-4:]}")
                                st.caption(f"🗑️ Waste: {last_waste}")
                                st.caption(f"⏱️ Since: {last_time}")
                                st.caption(f"📊 Today: {total_uses} uses | {unique_users} users")
                            else:
                                st.markdown(f"### {bin_name.upper()}")
                                st.error("🔴 CLOSED")
                                st.caption(f"👤 Last: User {last_user[-4:]}")
                                st.caption(f"🗑️ Waste: {last_waste}")
                                st.caption(f"⏱️ At: {last_time}")
                                st.caption(f"📊 Today: {total_uses} uses | {unique_users} users")
                        else:
                            st.markdown(f"### {bin_name.upper()}")
                            st.warning("No Data")
                            st.caption("No activity recorded")
                
                st.divider()
                
                # =============================
                # USER BEHAVIOR ANALYSIS
                # =============================
                st.subheader("📊 User Behavior Analysis")
                
                user_stats = get_user_behavior(df_filtered)
                
                if not user_stats.empty:
                    tab1, tab2, tab3 = st.tabs(["Top Users", "Hourly Pattern", "Movement Flow"])
                    
                    with tab1:
                        col1, col2 = st.columns([1, 1])
                        
                        with col1:
                            st.write("**Most Active Users**")
                            top_users = user_stats.head(10).reset_index()
                            top_users['barcode_short'] = top_users['barcode'].astype(str).str[-4:]
                            st.dataframe(
                                top_users[['barcode_short', 'total_actions', 'favorite_bin', 'favorite_waste', 'last_active']],
                                use_container_width=True,
                                hide_index=True
                            )
                        
                        with col2:
                            st.write("**User Distribution**")
                            # Group users by number of actions
                            labels = ['1-2', '3-5', '6-10', '11-20', '21-50', '50+']
                            bins = [0, 2, 5, 10, 20, 50, 1000]
                            user_stats['action_group'] = pd.cut(user_stats['total_actions'], bins=bins, labels=labels)
                            dist = user_stats['action_group'].value_counts().sort_index()
                            st.bar_chart(dist)
                    
                    with tab2:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Hourly Activity Pattern**")
                            hourly = get_hourly_pattern(df_filtered)
                            if not hourly.empty:
                                st.line_chart(hourly, height=300)
                                # Peak hours
                                peak_hour = hourly.idxmax()
                                st.caption(f"🏆 Peak hour: {peak_hour}:00 ({hourly.max()} actions)")
                        
                        with col2:
                            st.write("**Peak Usage Times**")
                            # Show top 3 hours
                            top_hours = hourly.nlargest(3)
                            for hour, count in top_hours.items():
                                period = "AM" if hour < 12 else "PM"
                                display_hour = hour if hour <= 12 else hour - 12
                                display_hour = 12 if display_hour == 0 else display_hour
                                st.info(f"⏰ {display_hour}:00 {period} - {count} actions")
                    
                    with tab3:
                        st.write("**User Movement Between Bins**")
                        transitions = get_bin_transitions(df_filtered)
                        
                        if not transitions.empty:
                            # Show as a flow matrix
                            pivot = transitions.pivot(index="from_bin", columns="to_bin", values="count").fillna(0)
                            
                            # Reindex to show all bins
                            for bin_name in BINS:
                                if bin_name not in pivot.columns:
                                    pivot[bin_name] = 0
                                if bin_name not in pivot.index:
                                    pivot.loc[bin_name] = 0
                            
                            pivot = pivot[BINS].reindex(BINS)
                            st.dataframe(pivot.astype(int), use_container_width=True)
                            
                            st.caption("📊 Numbers show how many times users moved from one bin to another")
                        else:
                            st.info("Not enough data for movement analysis")
                else:
                    st.info("No user behavior data available for selected period")
                
                st.divider()
                
                # =============================
                # REAL-TIME ACTIVITY FEED
                # =============================
                st.subheader("🔄 Live Activity Feed")
                
                recent = df.sort_values("timestamp", ascending=False).head(10)
                
                for _, row in recent.iterrows():
                    time_str = row["timestamp"][-8:]
                    user_short = str(row["barcode"])[-4:]
                    
                    if row["bin_state"] == "open":
                        st.info(
                            f"🟢 [{time_str}] **User {user_short}** opened **{row['bin_type']}** bin for **{row['waste_type']}**",
                            icon="👤"
                        )
                    else:
                        st.success(
                            f"🔴 [{time_str}] **User {user_short}** closed **{row['bin_type']}** bin after **{row['bin_duration_sec']:.1f}s**",
                            icon="✅"
                        )
                
                st.divider()
                
                # =============================
                # BEHAVIOR INSIGHTS
                # =============================
                st.subheader("💡 Behavior Insights")
                
                if len(user_stats) > 0:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Most common waste type
                        top_waste = df_filtered[df_filtered["bin_state"] == "open"]["waste_type"].mode()
                        if len(top_waste) > 0:
                            st.info(f"🗑️ **Most Disposed Waste:** {top_waste.iloc[0]}")
                        
                        # Most active hour
                        hourly = get_hourly_pattern(df_filtered)
                        if not hourly.empty and hourly.max() > 0:
                            peak = hourly.idxmax()
                            period = "AM" if peak < 12 else "PM"
                            display = peak if peak <= 12 else peak - 12
                            display = 12 if display == 0 else display
                            st.info(f"⏰ **Peak Activity:** {display}:00 {period}")
                    
                    with col2:
                        # User with most actions
                        top_user = user_stats.head(1)
                        if len(top_user) > 0:
                            st.info(f"👑 **Most Active User:** User {str(top_user.index[0])[-4:]} ({top_user.iloc[0]['total_actions']} actions)")
                        
                        # Average session duration
                        avg_session = df_filtered[df_filtered["bin_state"] == "closed"]["bin_duration_sec"].mean()
                        if not pd.isna(avg_session):
                            st.info(f"⏱️ **Avg Interaction Time:** {avg_session:.1f} seconds")
                
                st.divider()
                
                # =============================
                # RECENT TRANSACTIONS
                # =============================
                st.subheader("📄 Recent Transactions")
                display_df = df[["timestamp", "barcode", "waste_type", "bin_type", "bin_state", "bin_duration_sec"]].tail(15).copy()
                display_df['barcode'] = display_df['barcode'].astype(str).str[-4:]  # Show last 4 digits only
                display_df['timestamp'] = pd.to_datetime(display_df['timestamp']).dt.strftime("%H:%M:%S")
                st.dataframe(display_df, use_container_width=True, hide_index=True)
                
            else:
                st.warning("Log file is empty.")
        else:
            st.warning("No data available yet. Please run some transactions first.")
    
    time.sleep(refresh_rate)
# 1. Live Human Activity Metrics

# Active users now (last 5 minutes)
# Total users in period
# Total actions
# Average actions per user
# 2. Bin Status dengan Konteks Manusia

# Current user (last 4 digits)
# Current waste type
# Time since open/last closed
# Total uses & unique users today
# 3. User Behavior Analysis

# Top Users Table: Most active users dengan preferensi mereka
# User Distribution: Kategorisasi pengguna (casual vs power users)
# Hourly Pattern: Kapan pengguna paling aktif
# Movement Flow: Bagaimana pengguna berpindah antar bin
# 4. Live Activity Feed

# Real-time updates dengan user info
# Waktu, user, bin, waste type, duration
# 5. Behavior Insights

# Most disposed waste type
# Peak activity hour
# Most active user
# Average interaction time
# 6. Privacy-Focused Display

# Hanya menampilkan 4 digit terakhir barcode
# Tidak menampilkan data sensitif