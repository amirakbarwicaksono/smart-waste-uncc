# ----------- app/pages/blockchain_dashboard.py -----------
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from pathlib import Path
import numpy as np

from core.blockchain import get_client

st.set_page_config(page_title="Blockchain Dashboard", layout="wide", page_icon="🔗")

# =============================
# CUSTOM CSS - MODERN & EYE-CATCHING
# =============================
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
    }
    
    /* Header styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00ff88, #00ccff, #ffaa44);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    
    .sub-header {
        text-align: center;
        color: #888;
        margin-bottom: 2rem;
        font-size: 0.9rem;
    }
    
    /* Metric cards with glow effect */
    .metric-card {
        background: linear-gradient(135deg, rgba(26,26,46,0.9), rgba(22,33,62,0.9));
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1.2rem;
        border: 1px solid rgba(0,255,136,0.3);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3), 0 0 20px rgba(0,255,136,0.1);
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #00ff88;
        box-shadow: 0 12px 40px rgba(0,255,136,0.2);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, #00ff88, #00ccff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
    }
    
    .metric-label {
        font-size: 0.8rem;
        color: #aaa;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 0.5rem;
    }
    
    .metric-detail {
        font-size: 0.7rem;
        color: #666;
        margin-top: 0.3rem;
    }
    
    /* Transaction cards */
    .tx-card {
        background: linear-gradient(135deg, #0f0f1a, #0a0a0f);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        border-left: 4px solid;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .tx-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00ff88, transparent);
        transform: translateX(-100%);
        transition: transform 0.5s;
    }
    
    .tx-card:hover::before {
        transform: translateX(100%);
    }
    
    .tx-card:hover {
        transform: translateX(5px);
        background: linear-gradient(135deg, #14141f, #0e0e16);
    }
    
    .tx-success {
        border-left-color: #00ff88;
    }
    
    .tx-skipped {
        border-left-color: #ff4444;
    }
    
    .points-badge {
        background: linear-gradient(135deg, #00ff8820, #00ccff20);
        color: #00ff88;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: bold;
        border: 1px solid rgba(0,255,136,0.3);
    }
    
    /* Chart container */
    .chart-container {
        background: rgba(10,10,20,0.5);
        border-radius: 20px;
        padding: 1rem;
        border: 1px solid rgba(255,255,255,0.05);
    }
    
    /* Sidebar styling */
    .sidebar-status {
        background: linear-gradient(135deg, #00ff8810, #00ccff10);
        border-radius: 15px;
        padding: 1rem;
        border: 1px solid rgba(0,255,136,0.2);
    }
</style>
""", unsafe_allow_html=True)

# =============================
# HELPER FUNCTIONS
# =============================
def get_all_transactions():
    """Get all transactions from blockchain ledger"""
    try:
        ledger_path = Path(__file__).parent.parent.parent / "logs" / "blockchain_ledger.json"
        if ledger_path.exists():
            with open(ledger_path, 'r') as f:
                ledger = json.load(f)
                return ledger.get("transactions", [])
    except Exception as e:
        print(f"Error loading ledger: {e}")
    return []

def format_timestamp(timestamp_str):
    """Format timestamp to readable format"""
    try:
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        return dt.strftime('%d %b %Y, %H:%M:%S')
    except:
        return timestamp_str[:16]

# =============================
# LOAD DATA
# =============================
all_transactions = get_all_transactions()

# Convert to DataFrame for analysis
if all_transactions:
    df = pd.DataFrame(all_transactions)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.strftime('%Y-%m-%d')
    df['date_display'] = df['timestamp'].dt.strftime('%d %b')
    df['hour'] = df['timestamp'].dt.hour
    df['points'] = df['metrics'].apply(lambda x: x.get('points_earned', 0))
    df['waste_type'] = df['waste'].apply(lambda x: x.get('type', 'Unknown'))
    df['bin_type'] = df['waste'].apply(lambda x: x.get('bin_type', 'Unknown'))
    df['user_short'] = df['user'].apply(lambda x: x.get('display_name', 'Unknown')[:12])
    
    # Statistics
    total_tx = len(df)
    total_points = df['points'].sum()
    verified_tx = len(df[df['points'] > 0])
    unique_users = df['user_short'].nunique()
    avg_points = total_points / verified_tx if verified_tx > 0 else 0
    success_rate = (verified_tx / total_tx * 100) if total_tx > 0 else 0
    
    verified_df = df[df['points'] > 0]

# =============================
# HEADER
# =============================
st.markdown('<div class="main-header">🔗 Blockchain Ledger</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Immutable record of verified waste disposal transactions</div>', unsafe_allow_html=True)

# =============================
# KPI CARDS - MODERN METRICS
# =============================
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{total_tx}</div>
        <div class="metric-label">Total Transactions</div>
        <div class="metric-detail">On-chain records</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{unique_users}</div>
        <div class="metric-label">Active Users</div>
        <div class="metric-detail">Unique participants</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{total_points:.1f}</div>
        <div class="metric-label">Total Points</div>
        <div class="metric-detail">Rewards distributed</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{avg_points:.2f}</div>
        <div class="metric-label">Avg Points/TX</div>
        <div class="metric-detail">Per verified disposal</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{success_rate:.0f}%</div>
        <div class="metric-label">Success Rate</div>
        <div class="metric-detail">Verified disposals</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =============================
# CHARTS SECTION - EYE-CATCHING VISUALS
# =============================
if all_transactions:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Daily Activity")
        if not df.empty:
            daily_tx = df.groupby('date').size().reset_index(name='count')
            daily_tx = daily_tx.sort_values('date')
            
            # 🔧 FILTER: Hanya tampilkan tanggal yang memiliki transaksi
            daily_tx = daily_tx[daily_tx['count'] > 0]
            
            if not daily_tx.empty:
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=daily_tx['date'],
                    y=daily_tx['count'],
                    marker=dict(
                        color=daily_tx['count'],
                        colorscale='Viridis',
                        showscale=True,
                        colorbar=dict(title="Transactions", x=1.05)
                    ),
                    text=daily_tx['count'],
                    textposition='outside',
                    hovertemplate='Date: %{x}<br>Transactions: %{y}<extra></extra>'
                ))
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0.2)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    height=400,
                    xaxis_title="Date",
                    yaxis_title="Number of Transactions",
                    xaxis_tickangle=45,
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No transaction data for the selected period")
    
    with col2:
        st.markdown("### 💰 Points Trend")
        if not verified_df.empty:
            daily_points = verified_df.groupby('date')['points'].sum().reset_index(name='points')
            daily_points = daily_points.sort_values('date')
            
            # 🔧 FILTER: Hanya tampilkan tanggal yang memiliki points
            daily_points = daily_points[daily_points['points'] > 0]
            
            if not daily_points.empty:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=daily_points['date'],
                    y=daily_points['points'],
                    mode='lines+markers',
                    line=dict(color='#ffaa44', width=3),
                    marker=dict(size=12, color='#ffaa44', symbol='diamond'),
                    fill='tozeroy',
                    fillcolor='rgba(255,170,68,0.1)',
                    hovertemplate='Date: %{x}<br>Points: %{y}<extra></extra>'
                ))
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0.2)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    height=400,
                    xaxis_title="Date",
                    yaxis_title="Points Earned",
                    xaxis_tickangle=45,
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No points earned yet")
        else:
            st.info("No verified transactions yet")
            st.caption("💡 Select 'Yes' when confirming weight to earn points!")
    
    st.markdown("---")
    
    # Second row - Waste Type Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ♻️ Waste Type Distribution")
        if not verified_df.empty:
            waste_counts = verified_df['waste_type'].value_counts()
            
            colors = px.colors.sequential.Viridis
            fig = px.pie(
                values=waste_counts.values, 
                names=waste_counts.index,
                hole=0.4,
                color_discrete_sequence=colors
            )
            fig.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate='%{label}<br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0.2)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No waste type data available")
    
    with col2:
        st.markdown("### 🏆 Top Contributors")
        if not verified_df.empty:
            user_points = verified_df.groupby('user_short')['points'].sum().sort_values(ascending=False).head(10)
            
            fig = px.bar(
                x=user_points.values,
                y=user_points.index,
                orientation='h',
                color=user_points.values,
                color_continuous_scale='Viridis',
                labels={'x': 'Points', 'y': 'User'}
            )
            fig.update_traces(
                text=user_points.values,
                textposition='outside',
                hovertemplate='User: %{y}<br>Points: %{x}<extra></extra>'
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0.2)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=400,
                xaxis_title="Points Earned",
                yaxis_title=""
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No contributor data available")
    
    st.markdown("---")

# =============================
# RECENT TRANSACTIONS - LIVE FEED
# =============================
st.markdown("### 🔄 Live Transaction Feed")

if all_transactions:
    # 🔧 FIX: Sort transactions by timestamp (newest first)
    sorted_tx = sorted(all_transactions, key=lambda x: x.get('timestamp', ''), reverse=True)
    
    # Display last 10 transactions (newest first)
    for tx in sorted_tx[:10]:
        tx_id = tx.get('transaction_id', 'unknown')[:12]
        timestamp = format_timestamp(tx.get('timestamp', ''))
        waste_type = tx.get('waste', {}).get('type', 'Unknown')
        bin_type = tx.get('waste', {}).get('bin_type', 'Unknown')
        points = tx.get('metrics', {}).get('points_earned', 0)
        user = tx.get('user', {}).get('display_name', 'Unknown')[:16]
        is_verified = points > 0
        
        status_class = "tx-success" if is_verified else "tx-skipped"
        
        st.markdown(f"""
        <div class="tx-card {status_class}">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <span style="font-family: monospace; font-size: 0.8rem; background: #1a1a2e; padding: 4px 8px; border-radius: 6px;">{tx_id}...</span>
                    <span style="font-size: 0.7rem; color: #888;">{timestamp}</span>
                </div>
                <div>
                    <span class="points-badge">{'✅ +' + str(points) + ' pts' if is_verified else '⏭️ Skipped'}</span>
                </div>
            </div>
            <div style="margin-top: 12px; display: flex; gap: 20px; flex-wrap: wrap;">
                <div><strong>🗑️ Waste:</strong> {waste_type}</div>
                <div><strong>📦 Bin:</strong> <span style="color: #00ff88;">{bin_type}</span></div>
                <div><strong>👤 User:</strong> {user}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Show timestamp of latest transaction
    if sorted_tx:
        latest_ts = sorted_tx[0].get('timestamp', '')
        st.caption(f"📡 Last updated: {format_timestamp(latest_ts)} (showing 10 most recent)")
else:
    st.info("ℹ️ No transactions recorded yet")

# =============================
# SIDEBAR - BLOCKCHAIN STATUS
# =============================
with st.sidebar:
    st.markdown("### 🔗 Blockchain Status")
    st.markdown("---")
    
    st.markdown(f"""
    <div class="sidebar-status">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
            <div style="width: 10px; height: 10px; background: #00ff88; border-radius: 50%; box-shadow: 0 0 10px #00ff88;"></div>
            <span style="font-weight: bold;">Network Active</span>
        </div>
        <div style="font-size: 0.8rem; color: #aaa;">Consensus: Proof of Waste</div>
        <div style="font-size: 0.8rem; color: #aaa;">Block Time: ~30 seconds</div>
        <div style="font-size: 0.8rem; color: #aaa;">Chain ID: smart-waste-01</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📊 Quick Stats")
    
    st.metric("Block Height", total_tx if all_transactions else 0)
    st.metric("Total Value Locked", f"{total_points:.1f} pts" if all_transactions else "0 pts")
    st.metric("Success Rate", f"{success_rate:.0f}%" if all_transactions else "0%")
    
    st.markdown("---")
    st.markdown("### ⚙️ System Info")
    st.caption(f"Mode: Blockchain Simulator")
    st.caption(f"Transactions: {total_tx if all_transactions else 0}")
    st.caption(f"Verified: {verified_tx if all_transactions else 0}")
    
    st.markdown("---")
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()