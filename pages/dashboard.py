"""
Dashboard Page - MediGuard Drift AI
Visualization of real health trends based on daily checkups.
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# Import database module for persistent storage
from storage.database import load_health_records

def load_data():
    """Load health records using the database module and return as DataFrame."""
    user_id = st.session_state.get('user_id', 'default_user')
    records = load_health_records(user_id)
    if not records:
        return pd.DataFrame()
        
    df = pd.DataFrame(records)
    
    # Ensure date column is datetime
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    
    return df.sort_values('date') if not df.empty else df

def show():
    st.title("📊 Health Trends Dashboard")
    
    # Load Real Data
    df = load_data()
    
    if df.empty:
        st.info("👋 No health records found yet.")
        st.markdown("""
        **Get Started:**
        1. Go to **Daily Health Check**
        2. Complete your first assessment
        3. Come back here to see your trends!
        """)
        
        if st.button("Go to Daily Check"):
            st.session_state.current_page = "Daily Health Check" # Assuming main app uses this key
            st.rerun()
        return

    # Summary Metrics (Latest vs Previous)
    st.subheader("📈 Current Status")
    
    if len(df) >= 1:
        latest = df.iloc[-1]
        
        # Try to get previous record
        previous = df.iloc[-2] if len(df) >= 2 else None
        
        col1, col2, col3 = st.columns(3)
        
        # Helper for delta
        def get_delta(curr, prev):
            if prev is None or prev == 0: return None
            return f"{(curr - prev):.2f}"

        with col1:
            val = latest.get('movement_speed', 0)
            prev_val = previous.get('movement_speed', 0) if previous is not None else 0
            st.metric("Movement Speed", f"{val:.2f}", delta=get_delta(val, prev_val))
            
        with col2:
            val = latest.get('stability', 0)
            prev_val = previous.get('stability', 0) if previous is not None else 0
            st.metric("Stability", f"{val:.2f}", delta=get_delta(val, prev_val))
            
        with col3:
            val = latest.get('posture_deviation', 0)
            prev_val = previous.get('posture_deviation', 0) if previous is not None else 0
            st.metric("Posture Deviation", f"{val:.2f}", delta=get_delta(val, prev_val), delta_color="inverse")

    st.markdown("---")
    
    # --------------------------------------------------------
    # TREND CHARTS
    # --------------------------------------------------------
    st.subheader("📉 Historical Trends")
    
    # Ensure date is the index for line_chart
    chart_df = df.set_index('date')
    
    # Chart 1: Stability & Movement
    st.markdown("#### 🏃 Movement & Stability")
    st.line_chart(chart_df[['movement_speed', 'stability']])
    st.caption("Higher is better for Stability and Speed.")

    # Chart 2: Posture Deviation
    st.markdown("#### 🧍 Posture Deviation")
    st.line_chart(chart_df[['posture_deviation']])
    st.caption("Lower is generally better (indicates less unnecessary swaying).")

    # Data Table
    with st.expander("📋 View Raw Data History"):
        st.dataframe(df.style.format({
            "movement_speed": "{:.2f}",
            "stability": "{:.2f}",
            "posture_deviation": "{:.2f}",
        }))

    # Simple Insight logic
    st.markdown("### 🤖 Quick Insights")
    avg_stability = df['stability'].mean()
    if avg_stability > 0.8:
        st.success(f"✅ Your stability is excellent! (Average: {avg_stability:.2f})")
    elif avg_stability > 0.5:
        st.warning(f"⚠️ Your stability is moderate. (Average: {avg_stability:.2f})")
    else:
        st.error(f"📉 Attention needed: Stability is low. (Average: {avg_stability:.2f})")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refresh Data"):
            st.rerun()
    with col2:
        if st.button("➕ New Checkup"):
            st.session_state.current_page = "Daily Health Check" # Fallback if app logic uses this
            # If the main app uses session_state.stage to control pages, user might need to click nav manually.
            # But usually Streamlit apps use a shared nav mechanism.
