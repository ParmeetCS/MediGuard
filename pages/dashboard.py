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
            val = latest.get('movement_speed', 0) or latest.get('avg_movement_speed', 0)
            prev_val = (previous.get('movement_speed', 0) or previous.get('avg_movement_speed', 0)) if previous is not None else 0
            st.metric("Movement Speed", f"{val:.2f}", delta=get_delta(val, prev_val))
            
        with col2:
            val = latest.get('stability', 0) or latest.get('avg_stability', 0)
            prev_val = (previous.get('stability', 0) or previous.get('avg_stability', 0)) if previous is not None else 0
            st.metric("Stability", f"{val:.2f}", delta=get_delta(val, prev_val))
            
        with col3:
            val = latest.get('sit_stand_movement_speed', 0)
            prev_val = previous.get('sit_stand_movement_speed', 0) if previous is not None else 0
            st.metric("Sit-Stand Speed", f"{val:.2f}", delta=get_delta(val, prev_val))

    st.markdown("---")
    
    # --------------------------------------------------------
    # TREND CHARTS
    # --------------------------------------------------------
    st.subheader("📉 Historical Trends")
    
    # Ensure date is the index for line_chart
    chart_df = df.set_index('date')
    
    # Determine which columns exist
    available_cols = chart_df.columns.tolist()
    
    # Chart 1: Movement Speed
    st.markdown("#### 🏃 Movement Speed Over Time")
    if 'movement_speed' in available_cols or 'avg_movement_speed' in available_cols:
        speed_col = 'avg_movement_speed' if 'avg_movement_speed' in available_cols else 'movement_speed'
        st.line_chart(chart_df[[speed_col]])
        st.caption("Higher is better - shows how quickly you can move.")
    else:
        st.info("Movement speed data not available yet.")

    # Chart 2: Stability
    st.markdown("#### ⚖️ Stability & Balance")
    if 'stability' in available_cols or 'avg_stability' in available_cols:
        stability_col = 'avg_stability' if 'avg_stability' in available_cols else 'stability'
        st.line_chart(chart_df[[stability_col]])
        st.caption("Higher is better - shows how steady you are.")
    else:
        st.info("Stability data not available yet.")
    
    # Chart 3: Sit-Stand Performance
    st.markdown("#### 🪑 Sit-Stand Speed")
    if 'sit_stand_movement_speed' in available_cols:
        st.line_chart(chart_df[['sit_stand_movement_speed']])
        st.caption("Higher is better - shows leg strength and mobility.")
    else:
        st.info("Sit-stand data not available yet.")

    # Data Table
    with st.expander("📋 View Raw Data History"):
        # Format only numeric columns
        format_dict = {}
        for col in df.columns:
            if col not in ['date', 'user_id', 'check_date', 'check_timestamp']:
                # Check if column is numeric
                if pd.api.types.is_numeric_dtype(df[col]):
                    format_dict[col] = "{:.3f}"
        
        if format_dict:
            st.dataframe(df.style.format(format_dict))
        else:
            st.dataframe(df)

    # Simple Insight logic
    st.markdown("### 🤖 Quick Insights")
    
    # Use whichever stability column exists
    stability_col = 'avg_stability' if 'avg_stability' in df.columns else 'stability' if 'stability' in df.columns else None
    
    if stability_col:
        avg_stability = df[stability_col].mean()
        if avg_stability >= 0.85:
            st.success(f"✅ Your balance is excellent! (Average: {avg_stability:.2f})")
        elif avg_stability >= 0.75:
            st.info(f"👍 Your balance is good. (Average: {avg_stability:.2f})")
        elif avg_stability >= 0.65:
            st.warning(f"⚠️ Your balance could use some work. (Average: {avg_stability:.2f})")
        else:
            st.error(f"📉 Consider working on balance exercises. (Average: {avg_stability:.2f})")
    else:
        st.info("Complete more health checks to see insights!")

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
