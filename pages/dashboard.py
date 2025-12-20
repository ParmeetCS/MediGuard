"""
Dashboard Page - MediGuard Drift AI
Visualization of health trends and drift detection
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random


def generate_dummy_data(days=14):
    """
    Generate realistic dummy time-series health data with gradual drift
    """
    base_date = datetime.now() - timedelta(days=days-1)
    dates = [base_date + timedelta(days=i) for i in range(days)]
    
    # Generate movement speed data (with slight downward drift)
    movement_speed = []
    base_speed = 3.2
    for i in range(days):
        # Add gradual drift and daily variation
        drift = -0.02 * i  # Gradual decline
        noise = random.uniform(-0.15, 0.15)
        value = base_speed + drift + noise
        movement_speed.append(round(max(2.0, value), 2))
    
    # Generate stability data (with slight downward drift)
    stability = []
    base_stability = 92
    for i in range(days):
        drift = -0.3 * i
        noise = random.uniform(-2, 2)
        value = base_stability + drift + noise
        stability.append(round(max(70, min(100, value)), 1))
    
    # Generate walk speed data (relatively stable)
    walk_speed = []
    base_walk = 1.2
    for i in range(days):
        drift = -0.01 * i
        noise = random.uniform(-0.08, 0.08)
        value = base_walk + drift + noise
        walk_speed.append(round(max(0.8, value), 2))
    
    # Generate hand steadiness (showing improvement)
    hand_steadiness = []
    base_steady = 85
    for i in range(days):
        drift = 0.2 * i  # Slight improvement
        noise = random.uniform(-1.5, 1.5)
        value = base_steady + drift + noise
        hand_steadiness.append(round(max(70, min(100, value)), 1))
    
    # Generate overall mobility score
    overall_mobility = []
    for i in range(days):
        # Composite of other metrics
        score = (stability[i] * 0.4 + hand_steadiness[i] * 0.3 + 
                (100 - movement_speed[i] * 10) * 0.3)
        overall_mobility.append(round(score, 1))
    
    return pd.DataFrame({
        'date': dates,
        'movement_speed': movement_speed,
        'stability': stability,
        'walk_speed': walk_speed,
        'hand_steadiness': hand_steadiness,
        'overall_mobility': overall_mobility
    })


def detect_drift(data, column, threshold_change=5):
    """
    Simple drift detection: compare recent average to baseline
    """
    if len(data) < 7:
        return False, 0
    
    baseline = data[column].iloc[:5].mean()
    recent = data[column].iloc[-3:].mean()
    change_percent = ((recent - baseline) / baseline) * 100
    
    drift_detected = abs(change_percent) > threshold_change
    return drift_detected, round(change_percent, 1)


def show():
    """
    Display the dashboard page with health trends and drift detection
    """
    
    # ========================================
    # PAGE HEADER
    # ========================================
    st.markdown("""
        <div style='text-align: center; padding: 1.5rem 0;'>
            <h1 style='color: #4A90E2; font-size: 2.5rem;'>📊 Health Dashboard</h1>
            <p style='font-size: 1.1rem; color: #666;'>
                Track your health trends and detect drift over time
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========================================
    # GENERATE DUMMY DATA
    # ========================================
    # Check if user has completed a health check
    has_data = st.session_state.get('check_completed', False)
    
    if not has_data:
        st.info("""
        📋 **No Data Available Yet**
        
        Complete your first Daily Health Check to start seeing your personalized dashboard.
        Once you have data, you'll see:
        - Trend charts for all your health metrics
        - AI-powered drift detection
        - Personalized insights and recommendations
        """)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("📋 Start Health Check", type="primary", use_container_width=True):
                st.session_state.current_page = "Daily Health Check"
                st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Preview Dashboard (Demo Data)")
        st.caption("Below is a preview with simulated data to show what your dashboard will look like")
        st.markdown("<br>", unsafe_allow_html=True)
    
    # Generate 14 days of dummy data
    df = generate_dummy_data(days=14)
    
    # ========================================
    # SUMMARY CARDS
    # ========================================
    st.markdown("### 📈 Current Status Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Get latest values
    latest_mobility = df['overall_mobility'].iloc[-1]
    latest_stability = df['stability'].iloc[-1]
    latest_speed = df['movement_speed'].iloc[-1]
    latest_steadiness = df['hand_steadiness'].iloc[-1]
    
    # Calculate changes from previous day
    mobility_change = df['overall_mobility'].iloc[-1] - df['overall_mobility'].iloc[-2]
    stability_change = df['stability'].iloc[-1] - df['stability'].iloc[-2]
    speed_change = df['movement_speed'].iloc[-1] - df['movement_speed'].iloc[-2]
    steadiness_change = df['hand_steadiness'].iloc[-1] - df['hand_steadiness'].iloc[-2]
    
    with col1:
        st.metric(
            label="Overall Mobility",
            value=f"{latest_mobility}%",
            delta=f"{mobility_change:+.1f}%"
        )
    
    with col2:
        st.metric(
            label="Stability Score",
            value=f"{latest_stability}%",
            delta=f"{stability_change:+.1f}%"
        )
    
    with col3:
        st.metric(
            label="Movement Speed",
            value=f"{latest_speed}s",
            delta=f"{speed_change:+.2f}s",
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            label="Hand Steadiness",
            value=f"{latest_steadiness}%",
            delta=f"{steadiness_change:+.1f}%"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    
    # ========================================
    # DRIFT DETECTION STATUS
    # ========================================
    st.markdown("### 🔍 Drift Detection Status")
    
    # Detect drift in key metrics
    stability_drift, stability_change = detect_drift(df, 'stability', threshold_change=4)
    mobility_drift, mobility_change = detect_drift(df, 'overall_mobility', threshold_change=4)
    speed_drift, speed_change = detect_drift(df, 'movement_speed', threshold_change=8)
    
    # Count detected drifts
    drift_count = sum([stability_drift, mobility_drift, speed_drift])
    
    if drift_count == 0:
        st.success("""
        ✅ **No Significant Drift Detected**
        
        Your health metrics are stable and within expected ranges. Keep up the great work 
        with your daily checks!
        """)
    else:
        st.warning(f"""
        ⚠️ **{drift_count} Drift Alert{'s' if drift_count > 1 else ''}**
        
        Our AI has detected gradual changes in some of your health metrics. Review the 
        detailed charts below and consider discussing these trends with your healthcare provider.
        """)
    
    # Drift details
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_icon = "🔴" if stability_drift else "🟢"
        st.markdown(f"""
        <div style='background: {"#FFF3E0" if stability_drift else "#E8F5E9"}; 
                    padding: 1rem; border-radius: 8px; text-align: center;'>
            <h3 style='margin: 0; font-size: 1.5rem;'>{status_icon}</h3>
            <p style='margin: 0.5rem 0; font-weight: bold;'>Stability Score</p>
            <p style='margin: 0; color: #666;'>{stability_change:+.1f}% change</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        status_icon = "🔴" if mobility_drift else "🟢"
        st.markdown(f"""
        <div style='background: {"#FFF3E0" if mobility_drift else "#E8F5E9"}; 
                    padding: 1rem; border-radius: 8px; text-align: center;'>
            <h3 style='margin: 0; font-size: 1.5rem;'>{status_icon}</h3>
            <p style='margin: 0.5rem 0; font-weight: bold;'>Overall Mobility</p>
            <p style='margin: 0; color: #666;'>{mobility_change:+.1f}% change</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        status_icon = "🔴" if speed_drift else "🟢"
        st.markdown(f"""
        <div style='background: {"#FFF3E0" if speed_drift else "#E8F5E9"}; 
                    padding: 1rem; border-radius: 8px; text-align: center;'>
            <h3 style='margin: 0; font-size: 1.5rem;'>{status_icon}</h3>
            <p style='margin: 0.5rem 0; font-weight: bold;'>Movement Speed</p>
            <p style='margin: 0; color: #666;'>{speed_change:+.1f}% change</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    
    # ========================================
    # TREND CHARTS
    # ========================================
    st.markdown("### 📉 14-Day Trend Analysis")
    
    # Chart 1: Overall Mobility Score
    st.markdown("#### 🏃 Overall Mobility Score")
    
    fig_mobility = go.Figure()
    
    # Add main line
    fig_mobility.add_trace(go.Scatter(
        x=df['date'],
        y=df['overall_mobility'],
        mode='lines+markers',
        name='Mobility Score',
        line=dict(color='#4A90E2', width=3),
        marker=dict(size=8)
    ))
    
    # Add baseline reference
    baseline_mobility = df['overall_mobility'].iloc[:5].mean()
    fig_mobility.add_hline(
        y=baseline_mobility,
        line_dash="dash",
        line_color="green",
        annotation_text="Baseline Average",
        annotation_position="right"
    )
    
    # Add drift threshold zone
    fig_mobility.add_hrect(
        y0=baseline_mobility - 5,
        y1=baseline_mobility + 5,
        fillcolor="green",
        opacity=0.1,
        line_width=0,
        annotation_text="Normal Range",
        annotation_position="left"
    )
    
    fig_mobility.update_layout(
        title="Overall Mobility Score Over Time",
        xaxis_title="Date",
        yaxis_title="Mobility Score (%)",
        hovermode='x unified',
        height=400,
        showlegend=True
    )
    
    st.plotly_chart(fig_mobility, use_container_width=True)
    
    # AI Insight for mobility
    if mobility_drift:
        st.warning(f"""
        🤖 **AI Insight:** Your overall mobility has declined by **{abs(mobility_change):.1f}%** 
        over the past week. This gradual decrease suggests a drift in your movement patterns. 
        Consider reviewing your activity levels and discussing with your healthcare provider.
        """)
    else:
        st.info("""
        🤖 **AI Insight:** Your mobility score is stable and consistent with your baseline. 
        This indicates healthy, consistent movement patterns. Continue your current routine!
        """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Chart 2: Stability Score
    st.markdown("#### ⚖️ Stability Score")
    
    fig_stability = go.Figure()
    
    fig_stability.add_trace(go.Scatter(
        x=df['date'],
        y=df['stability'],
        mode='lines+markers',
        name='Stability',
        line=dict(color='#50C878', width=3),
        marker=dict(size=8),
        fill='tonexty',
        fillcolor='rgba(80, 200, 120, 0.1)'
    ))
    
    baseline_stability = df['stability'].iloc[:5].mean()
    fig_stability.add_hline(
        y=baseline_stability,
        line_dash="dash",
        line_color="orange",
        annotation_text=f"Baseline: {baseline_stability:.1f}%",
        annotation_position="right"
    )
    
    # Highlight drift threshold
    threshold_line = baseline_stability * 0.96  # 4% decline threshold
    fig_stability.add_hline(
        y=threshold_line,
        line_dash="dot",
        line_color="red",
        annotation_text="Drift Threshold",
        annotation_position="left"
    )
    
    fig_stability.update_layout(
        title="Balance & Stability Trend",
        xaxis_title="Date",
        yaxis_title="Stability Score (%)",
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig_stability, use_container_width=True)
    
    # AI Insight for stability
    if stability_drift:
        st.warning(f"""
        🤖 **AI Insight:** Stability has decreased by **{abs(stability_change):.1f}%** from your 
        baseline. This drift crossed our detection threshold. Factors like fatigue, stress, or 
        reduced activity may contribute. Monitor closely over the next few days.
        """)
    else:
        st.success("""
        🤖 **AI Insight:** Your stability remains strong and within normal variation. 
        Balance is a key indicator of overall health—keep it up!
        """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Chart 3: Multi-Metric Comparison
    st.markdown("#### 📊 Multi-Metric Comparison")
    
    fig_multi = go.Figure()
    
    # Normalize all metrics to 0-100 scale for comparison
    fig_multi.add_trace(go.Scatter(
        x=df['date'],
        y=df['stability'],
        mode='lines',
        name='Stability',
        line=dict(color='#50C878', width=2)
    ))
    
    fig_multi.add_trace(go.Scatter(
        x=df['date'],
        y=df['hand_steadiness'],
        mode='lines',
        name='Hand Steadiness',
        line=dict(color='#FF9800', width=2)
    ))
    
    fig_multi.add_trace(go.Scatter(
        x=df['date'],
        y=df['overall_mobility'],
        mode='lines',
        name='Overall Mobility',
        line=dict(color='#4A90E2', width=2, dash='dash')
    ))
    
    # Normalize walking speed to percentage (higher is better)
    normalized_walk = (df['walk_speed'] / df['walk_speed'].max()) * 100
    fig_multi.add_trace(go.Scatter(
        x=df['date'],
        y=normalized_walk,
        mode='lines',
        name='Walk Speed (normalized)',
        line=dict(color='#9C27B0', width=2)
    ))
    
    fig_multi.update_layout(
        title="All Metrics Comparison (Normalized to %)",
        xaxis_title="Date",
        yaxis_title="Score (%)",
        hovermode='x unified',
        height=450,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig_multi, use_container_width=True)
    
    st.info("""
    🤖 **AI Insight:** This comparison view helps identify correlations between different metrics. 
    Notice how hand steadiness has been improving while stability shows a slight decline? 
    This suggests your fine motor control is getting better, but overall balance may need attention.
    """)
    
    st.markdown("---")
    
    # ========================================
    # DATA TABLE
    # ========================================
    with st.expander("📋 View Raw Data"):
        st.markdown("##### Recent 7 Days - Detailed Metrics")
        
        display_df = df.tail(7).copy()
        display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
        display_df = display_df.rename(columns={
            'date': 'Date',
            'movement_speed': 'Movement Speed (s)',
            'stability': 'Stability (%)',
            'walk_speed': 'Walk Speed (m/s)',
            'hand_steadiness': 'Hand Steadiness (%)',
            'overall_mobility': 'Overall Mobility (%)'
        })
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # ========================================
    # AI RECOMMENDATIONS
    # ========================================
    st.markdown("### 🤖 AI-Generated Recommendations")
    
    rec_col1, rec_col2 = st.columns(2)
    
    with rec_col1:
        st.markdown("""
        <div style='background: #E3F2FD; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #4A90E2;'>
            <h4 style='color: #4A90E2; margin-top: 0;'>✅ What's Working</h4>
            <ul style='margin: 0; padding-left: 1.5rem;'>
                <li><strong>Hand Steadiness:</strong> Improving trend—fine motor control is excellent</li>
                <li><strong>Walk Speed:</strong> Remaining consistent and within healthy range</li>
                <li><strong>Daily Consistency:</strong> You're logging data regularly, which helps accuracy</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with rec_col2:
        st.markdown("""
        <div style='background: #FFF3E0; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #FF9800;'>
            <h4 style='color: #FF9800; margin-top: 0;'>📌 Suggestions</h4>
            <ul style='margin: 0; padding-left: 1.5rem;'>
                <li><strong>Stability:</strong> Consider balance exercises or yoga</li>
                <li><strong>Movement Speed:</strong> Monitor for another 3-5 days</li>
                <li><strong>Overall:</strong> If trends continue, discuss with your doctor</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ========================================
    # NEXT STEPS
    # ========================================
    st.markdown("### 🎯 Take Action")
    
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        if st.button("📋 Log Today's Check", use_container_width=True, type="primary"):
            st.session_state.current_page = "Daily Health Check"
            st.rerun()
    
    with action_col2:
        if st.button("💬 Ask AI Questions", use_container_width=True):
            st.session_state.current_page = "AI Health Chat"
            st.rerun()
    
    with action_col3:
        if st.button("📥 Export Data", use_container_width=True):
            st.info("Export feature coming soon! You'll be able to download your data as CSV.")
    
    st.markdown("---")
    
    # ========================================
    # FOOTER
    # ========================================
    st.caption("""
    💡 **About Drift Detection:** Our AI compares your recent 3-day average to your first 5-day 
    baseline. A change exceeding 4-5% triggers a drift alert. This helps catch gradual changes 
    that might be missed in day-to-day comparisons.
    """)
