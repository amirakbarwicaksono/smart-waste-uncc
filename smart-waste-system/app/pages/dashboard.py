import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

LOG_FILE = "logs/transactions.csv"
INFERENCE_FILE = "logs/inference_latency.csv"

st.set_page_config(page_title="Dashboard", layout="wide", page_icon="🎮")

# =============================
# CUSTOM CSS
# =============================
st.markdown("""
<style>
    .stApp { background: #0a0a0a; }
    .main-header { color: #fff; font-size: 1.8rem; font-weight: 600; text-align: center; margin-bottom: 0.5rem; }
    .sub-header { color: #888; font-size: 0.8rem; text-align: center; margin-bottom: 1rem; }
    .bin-card { border-radius: 10px; padding: 8px; text-align: center; margin: 3px; }
    .bin-open { border: 2px solid #fff; box-shadow: 0 0 10px rgba(255,255,255,0.3); }
    .metric-value { font-size: 1.5rem; font-weight: bold; }
    .metric-label { font-size: 0.7rem; color: #888; }
    .inference-card { background: #1a1a1a; border-radius: 10px; padding: 10px; margin: 3px; }
    hr { margin: 0.5rem 0; }
</style>
""", unsafe_allow_html=True)

# =============================
# SIDEBAR
# =============================
with st.sidebar:
    st.markdown("### ⚙️ Controls")
    time_range = st.selectbox("Time Range", ["Last Hour", "Last 6 Hours", "Last 24 Hours", "Last 7 Days", "All Time"], index=2)
    refresh_rate = st.slider("Refresh (sec)", 1, 5, 2)
    st.markdown("---")
    st.caption("Live data from smart waste system")

# =============================
# HEADER
# =============================
st.markdown('<div class="main-header">♻️ Dashboard | Smart Waste Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Real-time bin status & AI inference monitoring</div>', unsafe_allow_html=True)
st.markdown("---")

# =============================
# HELPER FUNCTIONS
# =============================
def filter_by_time(df, time_range):
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

def get_latest_inference():
    if os.path.exists(INFERENCE_FILE):
        df = pd.read_csv(INFERENCE_FILE)
        if len(df) > 0:
            return df.sort_values('timestamp', ascending=False).head(1)
    return pd.DataFrame()

def get_hourly_pattern(df):
    if len(df) == 0:
        return pd.DataFrame()
    df_copy = df[df["bin_state"] == "open"].copy()
    if len(df_copy) == 0:
        return pd.DataFrame()
    df_copy["hour"] = pd.to_datetime(df_copy["timestamp"]).dt.hour
    hourly = df_copy.groupby("hour").size()
    all_hours = pd.DataFrame(index=range(24))
    hourly = hourly.reindex(all_hours.index, fill_value=0)
    return hourly

# =============================
# COLORS
# =============================
BINS = ["recycling", "food_waste", "other", "harmful"]
BIN_ICONS = {"recycling": "♻️", "food_waste": "🍎", "other": "🗑️", "harmful": "⚠️"}
BIN_COLORS = {
    "recycling": {"bg": "#1e3a5f", "border": "#3b82f6", "open": "#60a5fa"},
    "food_waste": {"bg": "#1e4a2e", "border": "#22c55e", "open": "#4ade80"},
    "other": {"bg": "#2d2d2d", "border": "#6b7280", "open": "#9ca3af"},
    "harmful": {"bg": "#4a1a1a", "border": "#ef4444", "open": "#f87171"}
}

# =============================
# MAIN LOOP
# =============================
placeholder = st.empty()

while True:
    with placeholder.container():
        
        if os.path.exists(LOG_FILE):
            df = pd.read_csv(LOG_FILE)
            
            if len(df) > 0:
                df_filtered = filter_by_time(df, time_range)
                latest_inference = get_latest_inference()
                
                # =============================
                # TOP METRICS (4 columns)
                # =============================
                now = datetime.now()
                five_min_ago = now - timedelta(minutes=5)
                df['datetime'] = pd.to_datetime(df['timestamp'])
                active_users = df[df['datetime'] >= five_min_ago]['barcode'].nunique()
                total_actions = len(df_filtered[df_filtered["bin_state"] == "open"])
                total_users = df_filtered['barcode'].nunique()
                conf_val = latest_inference.iloc[0]['confidence'] * 100 if not latest_inference.empty else 0
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.markdown(f'<div class="metric-value">{active_users}</div><div class="metric-label">ACTIVE NOW</div>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f'<div class="metric-value">{total_actions}</div><div class="metric-label">TOTAL DISPOSALS</div>', unsafe_allow_html=True)
                with col3:
                    st.markdown(f'<div class="metric-value">{total_users}</div><div class="metric-label">TOTAL USERS</div>', unsafe_allow_html=True)
                with col4:
                    st.markdown(f'<div class="metric-value">{conf_val:.0f}%</div><div class="metric-label">AI CONFIDENCE</div>', unsafe_allow_html=True)
                
                st.markdown("---")
                
                # =============================
                # BIN STATUS (4 cards in one row)
                # =============================
                st.markdown("### 🗑️ Bin Status")
                
                latest_bin = df.sort_values("timestamp").groupby("bin_type").tail(1)
                open_events = df_filtered[df_filtered["bin_state"] == "open"]
                
                bin_cols = st.columns(4)
                for i, bin_name in enumerate(BINS):
                    with bin_cols[i]:
                        colors = BIN_COLORS[bin_name]
                        bin_data = latest_bin[latest_bin["bin_type"] == bin_name]
                        
                        if not bin_data.empty:
                            state = bin_data.iloc[0]["bin_state"]
                            last_time = bin_data.iloc[0]["timestamp"][-8:]
                            total_uses = len(open_events[open_events["bin_type"] == bin_name])
                            
                            if state == "open":
                                st.markdown(f"""
                                <div class="bin-card bin-open" style="background: {colors['bg']};">
                                    <div style="font-size: 1.6rem;">{BIN_ICONS[bin_name]}</div>
                                    <div style="font-weight: bold;">{bin_name.upper()}</div>
                                    <div style="color: {colors['open']};">🟢 OPEN</div>
                                    <div style="font-size: 0.7rem;">Since: {last_time}</div>
                                    <div style="font-size: 0.7rem;">Uses: {total_uses}</div>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.markdown(f"""
                                <div class="bin-card" style="background: {colors['bg']};">
                                    <div style="font-size: 1.6rem;">{BIN_ICONS[bin_name]}</div>
                                    <div style="font-weight: bold;">{bin_name.upper()}</div>
                                    <div style="color: #ff6666;">🔴 CLOSED</div>
                                    <div style="font-size: 0.7rem;">Last: {last_time}</div>
                                    <div style="font-size: 0.7rem;">Uses: {total_uses}</div>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="bin-card" style="background: {colors['bg']}; opacity: 0.5;">
                                <div style="font-size: 1.6rem;">{BIN_ICONS[bin_name]}</div>
                                <div>{bin_name.upper()}</div>
                                <div style="font-size: 0.7rem;">No Data</div>
                            </div>
                            """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # =============================
                # AI INFERENCE (Full details)
                # =============================
                st.markdown("### 🤖 AI Inference")
                
                if not latest_inference.empty:
                    latest = latest_inference.iloc[0]
                    confidence = latest['confidence'] * 100
                    
                    col_left, col_right = st.columns([1, 1])
                    
                    with col_left:
                        # Metrics table
                        st.markdown(f"""
                        <div class="inference-card">
                            <div style="font-size: 1.2rem; font-weight: bold;">{latest.get('waste_type', 'N/A')}</div>
                            <div style="font-size: 0.8rem; color: #aaa;">→ {latest.get('bin_type', 'N/A')}</div>
                            <hr>
                            <table style="width: 100%; font-size: 0.75rem;">
                                <tr><td>Preprocessing:</td><td style="text-align: right;"><b>{latest['preprocessing_ms']:.0f}ms</b></td></tr>
                                <tr><td>Stage 1 (Root):</td><td style="text-align: right;"><b>{latest['stage1_inference_ms']:.0f}ms</b></td></tr>
                                <tr><td>Stage 2:</td><td style="text-align: right;"><b>{latest['stage2_inference_ms']:.0f}ms</b></td></tr>
                                <tr><td>Overall Latency:</td><td style="text-align: right;"><b style="color: #ffaa44;">{latest['overall_latency_ms']:.0f}ms</b></td></tr>
                                <tr><td>Root Category:</td><td style="text-align: right;">{latest.get('root_category', 'N/A')}</td></tr>
                                <tr><td>Specialist Model:</td><td style="text-align: right;">{latest.get('stage2_model', 'N/A')}</td></tr>
                            </table>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_right:
                        # Gauge chart
                        fig = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=confidence,
                            title={'text': "Confidence Score", 'font': {'size': 12}},
                            domain={'x': [0, 1], 'y': [0, 1]},
                            gauge={
                                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickfont': {'size': 9}},
                                'bar': {'color': "#3b82f6"},
                                'bgcolor': "rgba(50,50,50,0.5)",
                                'steps': [
                                    {'range': [0, 50], 'color': "rgba(239,68,68,0.3)"},
                                    {'range': [50, 75], 'color': "rgba(234,179,8,0.3)"},
                                    {'range': [75, 100], 'color': "rgba(34,197,94,0.3)"}
                                ]
                            }
                        ))
                        fig.update_layout(height=180, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor='rgba(0,0,0,0)', font={'color': 'white'})
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Waiting for AI data...")
                
                st.markdown("---")
                
                # =============================
                # CHARTS (2 columns)
                # =============================
                col_c1, col_c2 = st.columns(2)
                
                with col_c1:
                    st.markdown("### 📈 Hourly Activity")
                    hourly = get_hourly_pattern(df_filtered)
                    if not hourly.empty:
                        fig = px.line(hourly, labels={'value': 'Disposals', 'hour': 'Hour'})
                        fig.update_layout(height=200, margin=dict(l=30, r=20, t=30, b=20), plot_bgcolor='rgba(30,30,30,0.5)', paper_bgcolor='rgba(0,0,0,0)', font={'color': '#ccc'}, xaxis=dict(tickmode='linear', tick0=0, dtick=4))
                        fig.update_traces(line=dict(color='#3b82f6', width=2))
                        st.plotly_chart(fig, use_container_width=True)
                
                with col_c2:
                    st.markdown("### 📊 Top Waste Types")
                    waste_counts = df_filtered[df_filtered["bin_state"] == "open"]["waste_type"].value_counts().head(5)
                    if not waste_counts.empty:
                        fig = px.bar(x=waste_counts.values, y=waste_counts.index, orientation='h', labels={'x': '', 'y': ''})
                        fig.update_layout(height=200, margin=dict(l=20, r=20, t=30, b=20), plot_bgcolor='rgba(30,30,30,0.5)', paper_bgcolor='rgba(0,0,0,0)', font={'color': '#ccc'})
                        fig.update_traces(marker_color='#22c55e')
                        st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("---")
                
                # =============================
                # ACTIVITY FEED
                # =============================
                st.markdown("### 🔄 Recent Activity")
                
                recent = df.sort_values("timestamp", ascending=False).head(5)
                for _, row in recent.iterrows():
                    time_str = row["timestamp"][-8:]
                    user_short = str(row["barcode"])[-8:]
                    icon = "🟢" if row["bin_state"] == "open" else "🔴"
                    action = "opened" if row["bin_state"] == "open" else "closed"
                    
                    st.markdown(f"""
                    <div style="border-left: 2px solid {'#22c55e' if row['bin_state'] == 'open' else '#ef4444'}; padding-left: 8px; margin: 3px 0; font-size: 0.8rem;">
                        {icon} <strong>{time_str}</strong> - User {user_short} {action} {row['bin_type']} bin for {row['waste_type']}
                    </div>
                    """, unsafe_allow_html=True)
                
            else:
                st.warning("No data available")
        else:
            st.warning("Waiting for data...")
    
    time.sleep(refresh_rate)