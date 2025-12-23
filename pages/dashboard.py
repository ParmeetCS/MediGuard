"""
Dashboard Page - MediGuard Drift AI
Visualization of real health trends based on daily checkups.
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import plotly.graph_objects as go

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
            val_percent = val * 100
            prev_percent = prev_val * 100
            delta_percent = f"{val_percent - prev_percent:.1f}%" if prev_val > 0 else None
            status = "🟢" if val_percent >= 80 else "🟡" if val_percent >= 60 else "🟠"
            st.metric(f"{status} Movement Speed", f"{val_percent:.0f}%", delta=delta_percent)
            
        with col2:
            val = latest.get('stability', 0) or latest.get('avg_stability', 0)
            prev_val = (previous.get('stability', 0) or previous.get('avg_stability', 0)) if previous is not None else 0
            val_percent = val * 100
            prev_percent = prev_val * 100
            delta_percent = f"{val_percent - prev_percent:.1f}%" if prev_val > 0 else None
            status = "🟢" if val_percent >= 80 else "🟡" if val_percent >= 60 else "🟠"
            st.metric(f"{status} Stability", f"{val_percent:.0f}%", delta=delta_percent)
            
        with col3:
            val = latest.get('sit_stand_movement_speed', 0)
            prev_val = previous.get('sit_stand_movement_speed', 0) if previous is not None else 0
            val_percent = val * 100
            prev_percent = prev_val * 100
            delta_percent = f"{val_percent - prev_percent:.1f}%" if prev_val > 0 else None
            status = "🟢" if val_percent >= 80 else "🟡" if val_percent >= 60 else "🟠"
            st.metric(f"{status} Sit-Stand Speed", f"{val_percent:.0f}%", delta=delta_percent)

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
    st.markdown("<h4 style='color: #00E5FF;'>🏃 MOVEMENT SPEED OVER TIME</h4>", unsafe_allow_html=True)
    if 'movement_speed' in available_cols or 'avg_movement_speed' in available_cols:
        speed_col = 'avg_movement_speed' if 'avg_movement_speed' in available_cols else 'movement_speed'
        
        # Convert to percentage
        values_percent = [val * 100 for val in chart_df[speed_col]]
        dates = chart_df.index
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=values_percent,
            mode='lines+markers+text',
            name='Movement Speed',
            line=dict(color='#00E5FF', width=6),
            marker=dict(size=20, color='#00E5FF'),
            text=[f"<b>{val:.0f}%</b>" for val in values_percent],
            textposition='top center',
            textfont=dict(size=18, color='#FFFFFF', family='Arial Black'),
            hovertemplate='<b>%{x}</b><br>Speed: <b>%{y:.0f}%</b><extra></extra>'
        ))
        
        fig.update_layout(
            plot_bgcolor='#1e1e1e',
            paper_bgcolor='#262626',
            font=dict(color='#FFFFFF', size=14),
            xaxis_title='Date',
            yaxis_title='Movement Speed (%)',
            yaxis=dict(range=[0, 105]),
            height=400,
            hovermode='x unified',
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add interpretation guide
        with st.expander("ℹ️ Understanding Your Movement Speed"):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown("🟢 **Excellent** (≥90%)<br><small>Moving quickly & efficiently</small>", unsafe_allow_html=True)
            with col2:
                st.markdown("✅ **Good** (80-89%)<br><small>Healthy movement</small>", unsafe_allow_html=True)
            with col3:
                st.markdown("🟡 **Fair** (70-79%)<br><small>Slower than ideal</small>", unsafe_allow_html=True)
            with col4:
                st.markdown("🟠 **Needs Attention** (<70%)<br><small>Significant slowness</small>", unsafe_allow_html=True)
    else:
        st.info("Movement speed data not available yet.")

    # Chart 2: Stability
    st.markdown("<h4 style='color: #00E676;'>⚖️ STABILITY & BALANCE OVER TIME</h4>", unsafe_allow_html=True)
    if 'stability' in available_cols or 'avg_stability' in available_cols:
        stability_col = 'avg_stability' if 'avg_stability' in available_cols else 'stability'
        
        # Convert to percentage
        values_percent = [val * 100 for val in chart_df[stability_col]]
        dates = chart_df.index
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=values_percent,
            mode='lines+markers+text',
            name='Stability',
            line=dict(color='#00E676', width=6),
            marker=dict(size=20, color='#00E676'),
            text=[f"<b>{val:.0f}%</b>" for val in values_percent],
            textposition='top center',
            textfont=dict(size=18, color='#FFFFFF', family='Arial Black'),
            hovertemplate='<b>%{x}</b><br>Stability: <b>%{y:.0f}%</b><extra></extra>'
        ))
        
        fig.update_layout(
            plot_bgcolor='#1e1e1e',
            paper_bgcolor='#262626',
            font=dict(color='#FFFFFF', size=14),
            xaxis_title='Date',
            yaxis_title='Stability (%)',
            yaxis=dict(range=[0, 105]),
            height=400,
            hovermode='x unified',
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add interpretation guide
        with st.expander("ℹ️ Understanding Your Stability Score"):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown("🟢 **Excellent** (≥85%)<br><small>Very steady, low fall risk</small>", unsafe_allow_html=True)
            with col2:
                st.markdown("✅ **Good** (75-84%)<br><small>Mostly stable</small>", unsafe_allow_html=True)
            with col3:
                st.markdown("🟡 **Fair** (65-74%)<br><small>Some wobbliness</small>", unsafe_allow_html=True)
            with col4:
                st.markdown("🟠 **Needs Attention** (<65%)<br><small>Higher fall risk</small>", unsafe_allow_html=True)
    else:
        st.info("Stability data not available yet.")
    
    # Chart 3: Sit-Stand Performance
    st.markdown("<h4 style='color: #FF6B9D;'>🪑 SIT-STAND SPEED OVER TIME</h4>", unsafe_allow_html=True)
    if 'sit_stand_movement_speed' in available_cols:
        
        # Convert to percentage
        values_percent = [val * 100 for val in chart_df['sit_stand_movement_speed']]
        dates = chart_df.index
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=values_percent,
            mode='lines+markers+text',
            name='Sit-Stand Speed',
            line=dict(color='#FF6B9D', width=6),
            marker=dict(size=20, color='#FF6B9D'),
            text=[f"<b>{val:.0f}%</b>" for val in values_percent],
            textposition='top center',
            textfont=dict(size=18, color='#FFFFFF', family='Arial Black'),
            hovertemplate='<b>%{x}</b><br>Sit-Stand: <b>%{y:.0f}%</b><extra></extra>'
        ))
        
        fig.update_layout(
            plot_bgcolor='#1e1e1e',
            paper_bgcolor='#262626',
            font=dict(color='#FFFFFF', size=14),
            xaxis_title='Date',
            yaxis_title='Sit-Stand Speed (%)',
            yaxis=dict(range=[0, 105]),
            height=400,
            hovermode='x unified',
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add interpretation guide
        with st.expander("ℹ️ Understanding Your Sit-Stand Speed"):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown("🟢 **Excellent** (≥85%)<br><small>Stand up quickly & easily</small>", unsafe_allow_html=True)
            with col2:
                st.markdown("✅ **Good** (75-84%)<br><small>Normal speed, no issues</small>", unsafe_allow_html=True)
            with col3:
                st.markdown("🟡 **Fair** (65-74%)<br><small>Taking longer</small>", unsafe_allow_html=True)
            with col4:
                st.markdown("🟠 **Needs Attention** (<65%)<br><small>Struggling to stand</small>", unsafe_allow_html=True)
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
        avg_percent = avg_stability * 100
        if avg_stability >= 0.80:
            st.success(f"✅ Your balance is excellent! (Average: {avg_percent:.0f}%)")
        elif avg_stability >= 0.60:
            st.info(f"👍 Your balance is good. (Average: {avg_percent:.0f}%)")
        else:
            st.warning(f"⚠️ Your balance could use some work. (Average: {avg_percent:.0f}%)")
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
