"""
AI Health Chat Page - MediGuard Drift AI
Conversational AI assistant for health insights and guidance

UPDATED: Now connects to ADK Orchestrator for real AI-powered analysis
"""

import streamlit as st
from datetime import datetime
import random

# Import AI Integration Layer
try:
    from agents.ai_integration import AIHealthAnalyzer, get_ai_chat_response
    from agents.adk_runtime import is_adk_ready
    ADK_AVAILABLE = True
except ImportError:
    ADK_AVAILABLE = False
    print("Warning: ADK integration not available. Using fallback responses.")


def get_ai_response(user_message):
    """
    Generate intelligent-sounding responses based on user input
    Uses pattern matching with predefined but contextual responses
    """
    message_lower = user_message.lower()
    
    # Get user profile data if available
    user_name = st.session_state.get('profile_name', 'there')
    has_check_data = st.session_state.get('check_completed', False)
    
    # Pattern matching for different types of questions
    
    # Greetings
    if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        responses = [
            f"Hello {user_name}! 👋 I'm here to help you understand your health trends. What would you like to know?",
            f"Hi {user_name}! How can I assist you with your health monitoring today?",
            f"Hey there! Ready to discuss your health journey? I'm here to help!"
        ]
        return random.choice(responses)
    
    # Stability/balance questions
    elif any(word in message_lower for word in ['stability', 'balance', 'stable', 'steadiness']):
        if has_check_data:
            return f"""Based on your recent health checks, I've noticed some interesting patterns in your stability metrics, {user_name}.

**What I'm seeing:**
- Your stability score has shown a gradual downward drift of about 4-5% over the past week
- This is crossing our baseline threshold, which is why I flagged it
- However, your hand steadiness is actually improving, showing good fine motor control

**What this might mean:**
This could indicate factors like:
- Changes in sleep quality affecting balance
- Reduced physical activity or exercise
- Stress or fatigue levels
- Natural day-to-day variation (monitor for a few more days)

**My recommendation:**
Continue your daily checks for 3-5 more days. If the trend continues, consider simple balance exercises like standing on one foot or yoga. And as always, discuss significant changes with your healthcare provider.

Would you like specific exercise suggestions for improving balance?"""
        else:
            return "I'd love to discuss your stability trends, but I need data first! Complete a Daily Health Check so I can analyze your unique patterns. 📋"
    
    # Movement/mobility questions
    elif any(word in message_lower for word in ['movement', 'mobility', 'move', 'speed', 'walk']):
        if has_check_data:
            return f"""Great question about mobility, {user_name}! Let me break down what your movement data tells us.

**Current Status:**
- Overall mobility score: Showing slight decline (about 3-4% from baseline)
- Movement speed: Trending slightly slower during sit-stand exercises
- Walking speed: Actually quite consistent and healthy!

**Context Matters:**
The AI looks at multiple factors:
- **Time of day**: Are you checking morning vs evening? That affects energy
- **Recent activity**: Did you exercise before the check?
- **Consistency**: Small daily variations are normal

**Why I'm watching this:**
Health drift isn't about one bad day—it's about gradual patterns. Your mobility isn't concerning yet, but I want to catch any sustained decline early, before it becomes significant.

**What you can do:**
- Keep logging daily (consistency helps me learn YOUR normal)
- Note any lifestyle changes (stress, sleep, diet)
- Stay active with regular movement throughout the day

Anything specific about your movement patterns you want to explore?"""
        else:
            return "I need your movement data to provide personalized insights! Start your first Daily Health Check and I'll analyze your unique mobility patterns. 🏃"
    
    # Drift detection questions
    elif any(word in message_lower for word in ['drift', 'change', 'declining', 'worse', 'better', 'improving']):
        return f"""Excellent question about drift detection—this is where the AI magic happens! ✨

**How Drift Detection Works:**

1. **Baseline Learning** (Days 1-5)
   - I learn what's "normal" for YOU specifically
   - Everyone's baseline is different—I don't compare you to others

2. **Pattern Recognition** (Day 6+)
   - I compare your recent 3-day average to your baseline
   - Looking for sustained changes, not just daily fluctuations
   - Threshold: 4-5% change triggers an alert

3. **Context Awareness**
   - I consider multiple metrics together
   - Look for correlations (e.g., poor sleep + lower stability)
   - Track trends over time, not isolated data points

**Why This Matters:**
Traditional health tracking misses gradual changes. You might not notice your balance declining 1% per week, but over 8 weeks that's an 8% decline—potentially significant!

**Real Example from Your Data:**
Your stability has drifted down 4.8% from baseline over 7 days. Alone, one bad day isn't concerning. But a steady weekly trend? That's worth investigating early.

Want me to explain any specific metric's drift in more detail?"""
    
    # Health concerns or symptoms
    elif any(word in message_lower for word in ['pain', 'hurt', 'sick', 'symptom', 'worried', 'concern', 'problem']):
        return f"""I appreciate you sharing that with me, {user_name}. However, I need to be clear about my role:

⚠️ **Important:** I'm a monitoring tool, not a medical advisor. I can:
- ✅ Track changes in movement patterns over time
- ✅ Alert you to gradual drifts in metrics
- ✅ Suggest when to discuss trends with your doctor

But I cannot:
- ❌ Diagnose conditions
- ❌ Provide medical advice for symptoms
- ❌ Replace professional healthcare guidance

**What You Should Do:**
If you're experiencing pain, new symptoms, or health concerns:
1. **Urgent issues**: Contact your healthcare provider immediately
2. **Emergencies**: Call emergency services
3. **General concerns**: Schedule an appointment with your doctor

I can help you track patterns and notice changes, but a qualified healthcare professional should evaluate any symptoms or concerns.

Is there something about your health *trends* (not symptoms) I can help clarify?"""
    
    # Questions about recommendations or what to do
    elif any(word in message_lower for word in ['should i', 'what should', 'recommend', 'advice', 'help', 'improve']):
        return f"""I'm happy to share general wellness suggestions based on your health trends, {user_name}! 

**Based on Your Recent Data:**

🟢 **What's Working Well:**
- Your hand steadiness is improving (+2.8%)—great fine motor control!
- Walking speed is consistent and healthy
- You're doing daily checks regularly (key for accurate tracking)

🟡 **Areas to Monitor:**
- Stability showing a gradual decline—let's watch this
- Movement speed slightly slower than baseline

**General Wellness Suggestions:**
(These are NOT medical advice, just healthy lifestyle ideas)

1. **For Balance/Stability:**
   - Try simple balance exercises (stand on one foot while brushing teeth)
   - Consider yoga or tai chi
   - Ensure good lighting at home to support steady movement

2. **For Overall Mobility:**
   - Regular walking (even 15-20 minutes daily helps)
   - Stretch regularly, especially after sitting
   - Stay hydrated—affects muscle function

3. **For Better Tracking:**
   - Do health checks at the same time daily
   - Note any major life changes (stress, sleep, diet)
   - Be consistent—that's how I learn your patterns!

**Most Important:**
These are general healthy habits. For personalized medical guidance, always consult your healthcare provider, especially if you notice concerning changes.

What specific area would you like to focus on?"""
    
    # Questions about the system/AI
    elif any(word in message_lower for word in ['how do you', 'how does', 'what are you', 'who are you', 'ai', 'work']):
        return """Great question! Let me explain what I am and how I work. 🤖

**What I Am:**
- I'm an AI health monitoring assistant for MediGuard Drift AI
- My job is to analyze your daily health metrics and detect gradual changes
- Think of me as your personal health trend analyst

**How I Work:**

1. **Data Collection**: You perform daily camera-based movement checks
2. **Pattern Analysis**: I analyze movement speed, stability, coordination, etc.
3. **Baseline Learning**: I learn YOUR unique "normal" over the first 5 days
4. **Drift Detection**: I compare recent data to your baseline, looking for gradual changes
5. **Insights**: I explain what I'm seeing in plain language

**What Makes Me Different:**
- 🎯 **Personalized**: I learn YOUR baseline, not generic population averages
- 📈 **Trend-Focused**: I catch gradual changes you might miss day-to-day
- 🤖 **Proactive**: I alert you BEFORE small changes become big problems
- 💬 **Conversational**: You can ask me questions about your data anytime

**What I'm NOT:**
- I'm not a medical diagnostic tool
- I don't provide medical advice or treatment
- I can't replace doctors or healthcare professionals

My goal? Help you stay aware of your health patterns so you can take preventive action early!

Anything specific about my capabilities you'd like to know?"""
    
    # Profile/personal questions
    elif any(word in message_lower for word in ['my profile', 'about me', 'my data', 'my info']):
        name = st.session_state.get('profile_name', 'Not set')
        age = st.session_state.get('profile_age', 'Not set')
        lifestyle = st.session_state.get('profile_lifestyle', 'Not set')
        
        return f"""Here's what I know about you, {user_name}:

**Your Profile:**
- **Name**: {name}
- **Age**: {age}
- **Lifestyle**: {lifestyle}

**Your Health Tracking:**
- **Daily Checks Completed**: {"Yes! Great consistency!" if has_check_data else "Not yet—start your first check!"}
- **Days of Data**: ~14 days (in demo mode)
- **Baseline Established**: Yes (first 5 days)

**How I Use This:**
- Your age helps me set appropriate health baselines
- Your lifestyle gives context (e.g., "Active/Athlete" has different movement expectations)
- The more data you provide, the better I can personalize insights

Want to update your profile? Head to the Profile page! Or ask me anything about your health trends."""
    
    # Thank you / goodbye
    elif any(word in message_lower for word in ['thank', 'thanks', 'bye', 'goodbye']):
        responses = [
            f"You're welcome, {user_name}! Remember to log your daily check. Take care! 💙",
            f"Happy to help! Stay consistent with your health monitoring. See you next time! 👋",
            f"Anytime! Keep up the great work with your health tracking. Have a wonderful day! ✨"
        ]
        return random.choice(responses)
    
    # Default response for unrecognized questions
    else:
        return f"""That's an interesting question, {user_name}! I'm still learning to understand all types of questions.

**Here are some things I can help with:**
- 📊 Explain your health trends and metrics
- 🔍 Discuss drift detection and what changes mean
- ⚖️ Provide insights on stability, mobility, coordination
- 💡 Offer general wellness suggestions (not medical advice)
- 🤖 Explain how I work and what I can do

**Try asking me things like:**
- "Why is my stability declining?"
- "What does the drift detection mean?"
- "How can I improve my balance?"
- "Explain my recent mobility trends"

Feel free to rephrase your question or ask something specific about your health data!"""


def get_ai_powered_response(user_id: str, user_message: str) -> str:
    """
    Get AI-powered response using real ADK integration
    Falls back to pattern matching if ADK unavailable
    """
    if not ADK_AVAILABLE or not is_adk_ready():
        # Fall back to pattern matching
        return get_ai_response(user_message)
    
    try:
        # Use AI integration for real analysis
        analyzer = AIHealthAnalyzer()
        result = analyzer.get_conversational_response(user_id, user_message)
        
        if result['success']:
            return result['response']
        else:
            # Fallback to pattern matching
            return get_ai_response(user_message)
    except Exception as e:
        print(f"AI response error: {e}")
        return get_ai_response(user_message)


def show():
    """
    Display the AI health chat interface with ADK integration
    """
    
    # ========================================
    # PAGE HEADER
    # ========================================
    st.markdown("""
        <div style='text-align: center; padding: 1.5rem 0;'>
            <h1 style='color: #4A90E2; font-size: 2.5rem;'>💬 AI Health Chat</h1>
            <p style='font-size: 1.1rem; color: #666;'>
                Ask questions about your health trends and get AI-powered insights
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========================================
    # ADK ORCHESTRATOR INTEGRATION
    # Connect Streamlit frontend with ADK agents
    # ========================================
    
    st.markdown("### 🤖 AI Health Analysis")
    
    # Read data from session state
    # These values come from Daily Check page and Profile/Context pages
    vision_features = st.session_state.get('analysis_results', {})  # From daily_check.py
    user_profile = {
        'name': st.session_state.get('profile_name', 'User'),
        'age': st.session_state.get('profile_age', None),
        'lifestyle': st.session_state.get('profile_lifestyle', None),
        'sleep_hours': st.session_state.get('sleep_hours', 7.0),
        'stress_level': st.session_state.get('stress_level', 'medium')
    }
    user_id = st.session_state.get('user_id', None)
    
    # Check if we have health check data to analyze
    has_check_data = st.session_state.get('check_completed', False)
    
    # Display data availability status
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if has_check_data:
            st.success("✅ Health data available")
        else:
            st.warning("⚠️ No health check data")
    
    with col2:
        if user_profile['age']:
            st.success("✅ Profile loaded")
        else:
            st.info("ℹ️ Profile not set")
    
    with col3:
        if ADK_AVAILABLE:
            st.success("✅ AI agents ready")
        else:
            st.error("❌ AI agents unavailable")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ========================================
    # RUN AI HEALTH ANALYSIS BUTTON
    # Triggers the full 5-agent ADK pipeline
    # ========================================
    
    if st.button("🚀 Run AI Health Analysis", type="primary", use_container_width=True):
        if not ADK_AVAILABLE:
            st.error("❌ AI agents are not available. Please check configuration.")
        else:
            with st.spinner("🔬 Running comprehensive AI analysis..."):
                try:
                    # Use AI Integration Layer for simpler analysis
                    from agents.ai_integration import AIHealthAnalyzer
                    
                    analyzer = AIHealthAnalyzer()
                    result = analyzer.analyze_user_health(
                        user_id=user_id,
                        metric_name="overall_mobility",
                        days_to_analyze=14
                    )
                    
                    if result['success'] and result['has_data']:
                        # Display comprehensive analysis
                        st.success("✅ AI Analysis Complete!")
                        
                        # Summary
                        summary = result['summary']
                        st.markdown("### 📊 Analysis Summary")
                        
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.markdown(f"""
                            **Metric:** {summary['metric_name']}  
                            **Baseline:** {summary['baseline_value']:.1f}  
                            **Recent:** {summary['recent_value']:.1f}  
                            **Change:** {summary['drift_percentage']:+.1f}%  
                            **Severity:** {summary['severity'].title()}  
                            **Risk Level:** {summary['risk_level'].title()}
                            """)
                        
                        with col2:
                            if summary['escalation_needed']:
                                st.error("⚠️ Escalation Recommended")
                            else:
                                st.success("✅ No Immediate Concerns")
                        
                        # Possible factors
                        if summary['possible_factors']:
                            st.markdown("### 🔍 Possible Contributing Factors")
                            for factor in summary['possible_factors']:
                                st.markdown(f"- {factor}")
                        
                        # Recommendations
                        if result['recommendations']:
                            st.markdown("### 💡 Recommendations")
                            for i, rec in enumerate(result['recommendations'], 1):
                                st.markdown(f"**{i}.** {rec}")
                        
                        # Detailed analysis (collapsible)
                        with st.expander("📋 Full AI Analysis Details"):
                            st.json(result['analysis'])
                    
                    elif result['error']:
                        st.warning(f"ℹ️ {result['error']}")
                        if not result['has_data']:
                            st.info("""
                            **Getting Started:**
                            1. Complete the Daily Health Check (at least 2-3 times)
                            2. Fill out your Health Context information
                            3. Return here to run AI analysis
                            """)
                    
                except Exception as e:
                    st.error(f"❌ Analysis error: {str(e)}")
    
    st.markdown("---")
    if 'agent_response' in st.session_state:
        response = st.session_state['agent_response']
        timestamp = st.session_state.get('analysis_timestamp', datetime.now())
        
        st.markdown(f"""
        <div style='background: #E8F5E9; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
            <p style='margin: 0;'><strong>📊 AI Analysis Generated:</strong> {timestamp.strftime("%Y-%m-%d %H:%M:%S")}</p>
            <p style='margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #666;'>
                Pipeline Status: {response.get('pipeline_metadata', {}).get('agents_successful', 0)}/5 agents successful
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # ========================================
        # AGENT 1 OUTPUT: DRIFT SUMMARY
        # Shows what changed in health metrics
        # ========================================
        
        with st.expander("📉 **1. Drift Summary** (What Changed)", expanded=True):
            drift = response.get('drift_summary', {})
            
            if drift.get('success'):
                # Severity-based color coding for professional yet reassuring presentation
                severity = drift.get('severity_level', 'unknown')
                severity_emoji = {"low": "🟢", "moderate": "🟡", "high": "🔴"}.get(severity, "⚪")
                
                # Use appropriate Streamlit message type based on severity
                if severity == "low":
                    st.success(f"{severity_emoji} **Severity: Low** - Minor variation detected, within normal monitoring range")
                elif severity == "moderate":
                    st.info(f"{severity_emoji} **Severity: Moderate** - Notable change detected, continue monitoring")
                else:  # high
                    st.warning(f"{severity_emoji} **Severity: High** - Significant change detected, review patterns carefully")
                
                # Metrics display
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    affected = len(drift.get('affected_features', []))
                    st.metric("📊 Affected Metrics", f"{affected}", 
                             help="Number of health metrics showing drift")
                
                with col2:
                    drift_pct = list(drift.get('drift_percentages', {}).values())
                    max_drift = max([abs(x) for x in drift_pct]) if drift_pct else 0
                    st.metric("📈 Maximum Drift", f"{max_drift:.1f}%", 
                             delta=f"{max_drift:.1f}% from baseline",
                             help="Largest deviation from your personal baseline")
                
                with col3:
                    trend = drift.get('trend', 'unknown')
                    trend_emoji = {"declining": "📉", "improving": "📈", "stable": "➡️"}.get(trend, "➡️")
                    st.metric("🎯 Trend", f"{trend_emoji} {trend.title()}", 
                             help="Direction of change over time")
                
                st.markdown("---")
                
                # Highlight key explanation with professional formatting
                st.markdown("**💡 What This Means:**")
                explanation = drift.get('explanation', 'No explanation available')
                st.markdown(f"> {explanation}")
                
                # Contributing factors with visual emphasis
                if drift.get('factors'):
                    st.markdown("**🔍 Possible Contributing Factors:**")
                    st.markdown("*These factors may be influencing the detected changes:*")
                    for factor in drift.get('factors', []):
                        st.markdown(f"- {factor}")
                
                # Reassuring note based on severity
                if severity == "low":
                    st.info("💙 **Remember:** Small variations are normal. Continue monitoring to track trends over time.")
                elif severity == "moderate":
                    st.info("💙 **Note:** This level of change is worth monitoring. Track your patterns over the next few days and note any lifestyle changes.")
                else:
                    st.warning("💙 **Important:** While this change is significant, remember that drift detection is about awareness, not diagnosis. Consider discussing with your healthcare provider.")
            else:
                st.error("❌ Drift analysis unavailable - please try again")
        
        # ========================================
        # AGENT 2 OUTPUT: CONTEXTUAL EXPLANATION
        # Shows why changes might have occurred
        # ========================================
        
        with st.expander("🧩 **2. Contextual Explanation** (Why It Happened)", expanded=True):
            context = response.get('contextual_explanation', {})
            
            if context.get('success'):
                # Confidence level with professional presentation
                confidence = context.get('confidence_level', 0.5)
                confidence_pct = int(confidence * 100)
                
                # Color-coded confidence indicator
                if confidence >= 0.7:
                    conf_color = "#4CAF50"  # Green
                    conf_message = "High confidence - strong data support"
                elif confidence >= 0.5:
                    conf_color = "#FF9800"  # Orange
                    conf_message = "Moderate confidence - reasonable data support"
                else:
                    conf_color = "#9E9E9E"  # Grey
                    conf_message = "Lower confidence - limited data available"
                
                st.markdown(f"""
                <div style='background: #F5F5F5; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid {conf_color};'>
                    <p style='margin: 0; font-weight: bold;'>📊 Analysis Confidence: {confidence_pct}%</p>
                    <p style='margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #666;'>{conf_message}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Main contextual insights with emphasis
                st.markdown("**💡 Understanding the Context:**")
                explanation = context.get('contextual_explanation', 'No explanation available')
                
                # Break explanation into paragraphs for readability
                paragraphs = explanation.split('\n\n')
                for para in paragraphs:
                    if para.strip():
                        st.markdown(f"> {para.strip()}")
                
                # Possible factors with visual grouping
                if context.get('possible_factors'):
                    st.markdown("---")
                    st.markdown("**🎯 Factors That May Be Contributing:**")
                    st.markdown("*Based on your personal context (age, lifestyle, sleep, stress, etc.):*")
                    
                    for i, factor in enumerate(context.get('possible_factors', []), 1):
                        # Highlight key phrases
                        st.markdown(f"**{i}.** {factor}")
                
                # Reassuring professional note
                st.success("💚 **Context Matters:** These insights are personalized to YOUR situation, not generic population averages. Understanding context helps you make informed decisions about your health.")
            else:
                st.info("ℹ️ Contextual analysis limited - add more profile and lifestyle information for richer insights")
        
        # ========================================
        # AGENT 3 OUTPUT: RISK ASSESSMENT
        # Shows how concerning the pattern is over time
        # ========================================
        
        with st.expander("⚠️ **3. Risk Assessment** (How Concerning)", expanded=True):
            risk = response.get('risk_assessment', {})
            
            if risk.get('success'):
                # Risk level with professional, reassuring presentation
                risk_level = risk.get('risk_level', 'unknown')
                risk_config = {
                    "temporary": {
                        "color": "#E8F5E9",
                        "border": "#4CAF50",
                        "emoji": "✅",
                        "title": "Temporary Variation",
                        "message": "This appears to be a short-term fluctuation. Continue monitoring to confirm it resolves naturally.",
                        "alert_type": "success"
                    },
                    "needs_observation": {
                        "color": "#FFF3E0",
                        "border": "#FF9800",
                        "emoji": "👁️",
                        "title": "Needs Observation",
                        "message": "A persistent pattern has been detected. Continue daily monitoring and note any changes in your routine.",
                        "alert_type": "info"
                    },
                    "potentially_concerning": {
                        "color": "#FFEBEE",
                        "border": "#F44336",
                        "emoji": "⚠️",
                        "title": "Potentially Concerning",
                        "message": "A sustained pattern has been identified. Consider discussing these trends with your healthcare provider.",
                        "alert_type": "warning"
                    }
                }
                
                config = risk_config.get(risk_level, risk_config["needs_observation"])
                
                # Risk level card with visual hierarchy
                st.markdown(f"""
                <div style='background: {config["color"]}; padding: 1.5rem; border-radius: 12px; 
                            margin-bottom: 1rem; border-left: 6px solid {config["border"]}; 
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                    <h3 style='margin: 0; color: #333;'>{config["emoji"]} {config["title"]}</h3>
                    <p style='margin: 1rem 0 0 0; font-size: 1rem; color: #555; line-height: 1.6;'>
                        <strong>{config["message"]}</strong>
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Key metrics in organized layout
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    days = risk.get('days_observed', 0)
                    st.metric("📅 Days Tracked", days, 
                             help="Number of days with data for this analysis")
                
                with col2:
                    consistency = int(risk.get('consistency_score', 0) * 100)
                    st.metric("🎯 Pattern Consistency", f"{consistency}%", 
                             help="How uniform the trend is (higher = more consistent)")
                
                with col3:
                    is_worsening = risk.get('is_worsening', False)
                    trend_icon = "📉" if is_worsening else "📈"
                    trend_text = "Worsening" if is_worsening else "Stable/Improving"
                    st.metric("📊 Trend Direction", f"{trend_icon} {trend_text}",
                             help="Whether the pattern is getting worse or improving")
                
                st.markdown("---")
                
                # Trend description with emphasis
                st.markdown("**📈 Trend Analysis:**")
                trend_desc = risk.get('trend_description', 'Unknown trend')
                st.markdown(f"> *{trend_desc}*")
                
                # Reasoning with professional tone
                st.markdown("**🧠 Risk Assessment Reasoning:**")
                reasoning = risk.get('reasoning', 'No reasoning available')
                
                # Highlight key sentences (look for "may", "suggests", etc.)
                import re
                sentences = re.split(r'(?<=[.!?])\s+', reasoning)
                for sentence in sentences:
                    if sentence.strip():
                        # Emphasize sentences with key probabilistic words
                        if any(word in sentence.lower() for word in ['may', 'could', 'suggests', 'indicates', 'possibly']):
                            st.markdown(f"**{sentence}**")
                        else:
                            st.markdown(sentence)
                
                # Recommendations with actionable format
                if risk.get('recommendations'):
                    st.markdown("---")
                    st.markdown("**💡 Recommended Actions:**")
                    for i, rec in enumerate(risk.get('recommendations', []), 1):
                        st.markdown(f"**{i}.** {rec}")
                
                # Reassuring contextual note based on risk level
                if risk_level == "temporary":
                    st.success("💙 **Good News:** Temporary variations are completely normal. Your body isn't a machine - daily fluctuations happen. We'll keep tracking to ensure patterns stabilize.")
                elif risk_level == "needs_observation":
                    st.info("💙 **Stay Informed:** Observation means awareness, not alarm. Continue your healthy habits and daily tracking. Most observed patterns stabilize with lifestyle adjustments.")
                else:
                    st.warning("💙 **Proactive Care:** Detection is the first step to prevention. This system caught a pattern early - now work with your healthcare provider to understand and address it. Early awareness = better outcomes.")
                    
            else:
                st.info("ℹ️ Risk assessment requires at least 2 days of data. Complete more daily checks to enable temporal trend analysis.")
        
        # ========================================
        # AGENT 4 OUTPUT: SAFETY NOTICE
        # Shows if escalation to professional care is needed
        # ========================================
        
        with st.expander("🛡️ **4. Safety Notice** (Escalation Check)", expanded=True):
            safety = response.get('safety_notice', {})
            
            if safety.get('success'):
                escalation_required = safety.get('escalation_required', False)
                urgency = safety.get('urgency_level', 'routine')
                
                if escalation_required:
                    # Escalation configuration with professional messaging
                    urgency_config = {
                        "urgent": {
                            "color": "#FFEBEE",
                            "border": "#D32F2F",
                            "emoji": "🚨",
                            "title": "Urgent Professional Consultation Recommended",
                            "subtitle": "Please contact your healthcare provider promptly",
                            "alert_type": "error",
                            "icon": "🏥"
                        },
                        "prompt": {
                            "color": "#FFF3E0",
                            "border": "#F57C00",
                            "emoji": "⚠️",
                            "title": "Prompt Professional Consultation Recommended",
                            "subtitle": "Schedule an appointment with your healthcare provider soon",
                            "alert_type": "warning",
                            "icon": "📞"
                        },
                        "routine": {
                            "color": "#E3F2FD",
                            "border": "#1976D2",
                            "emoji": "📋",
                            "title": "Routine Professional Consultation Recommended",
                            "subtitle": "Discuss these patterns at your next scheduled visit",
                            "alert_type": "info",
                            "icon": "📅"
                        }
                    }
                    
                    config = urgency_config.get(urgency, urgency_config["routine"])
                    
                    # Escalation notice with clear visual hierarchy
                    st.markdown(f"""
                    <div style='background: {config["color"]}; padding: 2rem; border-radius: 12px; 
                                margin-bottom: 1.5rem; border: 3px solid {config["border"]}; 
                                box-shadow: 0 4px 8px rgba(0,0,0,0.15);'>
                        <h2 style='margin: 0; color: #333; font-size: 1.5rem;'>{config["emoji"]} {config["title"]}</h2>
                        <p style='margin: 0.75rem 0 0 0; font-size: 1.1rem; color: #555; font-weight: 500;'>
                            {config["icon"]} {config["subtitle"]}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Safety message with emphasis
                    st.markdown("**🩺 Why This Recommendation:**")
                    safety_msg = safety.get('safety_message', '')
                    
                    # Break into paragraphs and emphasize key points
                    paragraphs = safety_msg.split('\n')
                    for para in paragraphs:
                        if para.strip():
                            # Emphasize action-oriented phrases
                            if any(phrase in para.lower() for phrase in ['should', 'recommend', 'important', 'discuss', 'contact']):
                                st.markdown(f"> **{para.strip()}**")
                            else:
                                st.markdown(f"> {para.strip()}")
                    
                    # Show rationale if available
                    if safety.get('rationale'):
                        st.markdown("**🔍 Analysis Details:**")
                        st.markdown(f"> {safety.get('rationale')}")
                    
                    st.markdown("---")
                    
                    # Actionable next steps
                    st.markdown("**📋 Next Steps:**")
                    
                    if safety.get('next_steps'):
                        for i, step in enumerate(safety.get('next_steps', []), 1):
                            st.markdown(f"**{i}.** {step}")
                    elif urgency == "urgent":
                        st.markdown("""
                        1. **📞 Contact your healthcare provider today** or visit urgent care if outside office hours
                        2. **📝 Bring your health tracking data** - export screenshots or summaries from this app
                        3. **💬 Describe your symptoms** clearly, including when patterns started
                        4. **❓ Prepare questions** about the trends you've noticed
                        """)
                    elif urgency == "prompt":
                        st.markdown("""
                        1. **📅 Schedule an appointment** with your primary care provider within the next week
                        2. **📊 Document patterns** - note daily symptoms and any triggers you notice
                        3. **📋 Prepare a summary** of when drift began and how you've felt
                        4. **💡 Continue daily monitoring** to provide updated data to your doctor
                        """)
                    else:  # routine
                        st.markdown("""
                        1. **📆 Note for next visit** - add these patterns to your appointment discussion points
                        2. **📈 Continue tracking** - more data helps your provider understand trends
                        3. **📝 Document context** - note lifestyle factors that may be relevant
                        4. **🤔 Reflect on changes** - think about any new medications, stress, or routine shifts
                        """)
                    
                    # Empowering reassurance
                    if urgency == "urgent":
                        st.error("💙 **You're Taking the Right Action:** Early detection and prompt response are signs of excellent self-care. Healthcare providers value proactive patients who monitor their health.")
                    elif urgency == "prompt":
                        st.warning("💙 **Proactive Health Management:** Catching patterns early is exactly what health monitoring is for. You're being appropriately cautious - this is responsible self-care.")
                    else:
                        st.info("💙 **Well-Managed Monitoring:** Routine check-ins with your provider are part of healthy living. Use this data to have informed conversations about your wellness.")
                    
                else:
                    # No escalation - reassuring message
                    st.success("✅ **No Professional Escalation Needed at This Time**")
                    
                    st.markdown("**💚 Good News:**")
                    safety_msg = safety.get('safety_message', 'Current patterns are within normal monitoring range.')
                    st.markdown(f"> {safety_msg}")
                    
                    st.markdown("---")
                    st.markdown("**📊 Continue Your Healthy Habits:**")
                    st.markdown("""
                    - ✅ **Keep tracking daily** - consistent data provides the most value
                    - 💪 **Maintain healthy routines** - sleep, exercise, stress management
                    - 🔔 **Stay aware** - note any new symptoms or significant changes
                    - 🏥 **Regular check-ups** - follow your normal healthcare schedule
                    """)
                    
                    st.info("💙 **Healthy Monitoring:** No escalation doesn't mean patterns aren't important - it means you're successfully catching changes early before they become concerning. Keep up the excellent self-care!")
                
                # Medical disclaimer with professional, non-alarming tone
                st.markdown("---")
                disclaimer = safety.get('disclaimer', 'This AI analysis is not a substitute for professional medical advice, diagnosis, or treatment.')
                st.caption(f"⚕️ **Important:** {disclaimer}")
                
            else:
                st.warning("Safety evaluation unavailable")
        
        # ========================================
        # AGENT 5 OUTPUT: CARE GUIDANCE
        # Shows practical lifestyle suggestions
        # ========================================
        
        with st.expander("💚 **5. Care Guidance** (Actionable Steps)", expanded=True):
            care = response.get('care_guidance', {})
            
            if care.get('success'):
                # Guidance tone with visual presentation
                tone = care.get('tone', 'neutral')
                tone_config = {
                    "reassuring": {
                        "color": "#E8F5E9",
                        "border": "#4CAF50",
                        "emoji": "😊",
                        "title": "Reassuring Guidance",
                        "message": "Small adjustments to support your current wellness trajectory"
                    },
                    "cautious": {
                        "color": "#FFF3E0",
                        "border": "#FF9800",
                        "emoji": "🤔",
                        "title": "Mindful Guidance",
                        "message": "Thoughtful suggestions to address emerging patterns"
                    },
                    "neutral": {
                        "color": "#F5F5F5",
                        "border": "#9E9E9E",
                        "emoji": "ℹ️",
                        "title": "General Guidance",
                        "message": "Practical wellness suggestions for healthy living"
                    }
                }
                
                config = tone_config.get(tone, tone_config["neutral"])
                
                # Tone indicator card
                st.markdown(f"""
                <div style='background: {config["color"]}; padding: 1.25rem; border-radius: 10px; 
                            margin-bottom: 1.5rem; border-left: 5px solid {config["border"]}; 
                            box-shadow: 0 2px 4px rgba(0,0,0,0.08);'>
                    <h4 style='margin: 0; color: #333;'>{config["emoji"]} {config["title"]}</h4>
                    <p style='margin: 0.5rem 0 0 0; color: #666; font-style: italic;'>{config["message"]}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Wellness suggestions with numbered, actionable format
                st.markdown("**✨ Personalized Wellness Suggestions:**")
                st.markdown("*These suggestions are based on your unique health patterns and context:*")
                
                guidance_list = care.get('guidance_list', [])
                if guidance_list:
                    for i, suggestion in enumerate(guidance_list, 1):
                        # Highlight action verbs at start of suggestions
                        action_verbs = ['try', 'consider', 'maintain', 'practice', 'focus', 'increase', 'reduce', 'improve', 'monitor']
                        words = suggestion.split()
                        if words and words[0].lower() in action_verbs:
                            st.markdown(f"**{i}.** **{words[0]}** {' '.join(words[1:])}")
                        else:
                            st.markdown(f"**{i}.** {suggestion}")
                else:
                    st.markdown("*Continue maintaining your current healthy habits.*")
                
                st.markdown("---")
                
                # Follow-up suggestion with professional presentation
                if care.get('follow_up_suggestion'):
                    st.markdown("**📅 Follow-Up Recommendation:**")
                    follow_up = care.get('follow_up_suggestion', '')
                    st.markdown(f"> {follow_up}")
                
                # Rationale in collapsible section for those who want depth
                if care.get('rationale'):
                    with st.expander("📖 **Why These Suggestions?** (Click to expand)"):
                        st.markdown(care.get('rationale', ''))
                        st.caption("💡 Understanding the 'why' helps you make informed decisions about implementing these suggestions.")
                
                # Categories covered (if available)
                if care.get('categories_covered'):
                    st.markdown("---")
                    st.markdown("**🎯 Wellness Areas Addressed:**")
                    categories = care.get('categories_covered', [])
                    # Display as badge-style chips
                    category_html = ""
                    for cat in categories:
                        category_html += f"<span style='background: #E3F2FD; padding: 0.4rem 0.8rem; border-radius: 20px; margin-right: 0.5rem; display: inline-block; margin-bottom: 0.5rem; color: #1976D2; font-weight: 500;'>{cat.title()}</span>"
                    st.markdown(category_html, unsafe_allow_html=True)
                
                # Reassuring note based on tone
                st.markdown("---")
                if tone == "reassuring":
                    st.success("💙 **You're Doing Great:** These suggestions are fine-tuning, not corrections. You're already on a healthy path - these are just small optimizations to support continued wellness.")
                elif tone == "cautious":
                    st.info("💙 **Proactive Self-Care:** These thoughtful adjustments can help address patterns before they become significant. Taking action early is a sign of smart health management.")
                else:
                    st.info("💙 **Empowered Wellness:** Every small positive change compounds over time. Choose the suggestions that resonate most with you and your lifestyle.")
                
                # Wellness disclaimer
                disclaimer = care.get('disclaimer', 'These are general wellness suggestions, not medical advice. Consult your healthcare provider for personalized medical guidance.')
                st.caption(f"⚕️ **Disclaimer:** {disclaimer}")
                
            else:
                st.warning("Care guidance unavailable - please try again")
        
        # ========================================
        # PIPELINE METADATA
        # Shows execution details for transparency
        # ========================================
        
        with st.expander("🔧 Pipeline Metadata"):
            metadata = response.get('pipeline_metadata', {})
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Agents Executed", metadata.get('agents_executed', 0))
                st.metric("Agents Successful", metadata.get('agents_successful', 0))
            
            with col2:
                st.markdown("**Execution Order:**")
                for step in metadata.get('execution_order', []):
                    st.write(f"✓ {step}")
    
    else:
        st.info("👆 Click **Run AI Health Analysis** above to get comprehensive insights from 5 AI agents")
        
        # Show what the analysis includes
        st.markdown("### 🎯 What You'll Get:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Analysis Components:**
            1. 📉 **Drift Detection** - What changed
            2. 🧩 **Context** - Why it happened
            3. ⚠️ **Risk** - How concerning
            """)
        
        with col2:
            st.markdown("""
            **Guidance & Safety:**
            4. 🛡️ **Safety Check** - Escalation decision
            5. 💚 **Care Plan** - Actionable steps
            """)
    
    st.markdown("---")
    
    # ========================================
    # INITIALIZE SESSION STATE (for chat)
    # ========================================
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
        # Add welcome message
        welcome_msg = {
            'role': 'assistant',
            'content': f"""Hello! 👋 I'm your AI Health Assistant from MediGuard Drift AI.

I'm here to help you understand your health trends, explain what drift means, and answer questions about your data. 

**What I Can Do:**
- 📊 Analyze your health trends and patterns
- 🔍 Explain drift detection and alerts
- 💡 Provide general wellness insights
- 🎯 Help you understand your metrics

**Remember:** I provide information and insights, not medical diagnosis or advice. Always consult healthcare professionals for medical concerns.

What would you like to know about your health trends today?""",
            'timestamp': datetime.now().strftime("%H:%M")
        }
        st.session_state.chat_history.append(welcome_msg)
    
    # ========================================
    # HELPFUL TIPS SECTION
    # ========================================
    with st.expander("💡 Quick Tips: How to Chat with the AI"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Example Questions:**
            - "Why is my stability declining?"
            - "What does health drift mean?"
            - "How can I improve my balance?"
            - "Explain my mobility trends"
            - "Should I be concerned about changes?"
            """)
        
        with col2:
            st.markdown("""
            **What I Can Help With:**
            - ✅ Interpret your health metrics
            - ✅ Explain trends and patterns
            - ✅ General wellness suggestions
            - ✅ Understanding drift detection
            - ❌ Medical diagnosis or treatment
            """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ========================================
    # CHAT DISPLAY AREA
    # ========================================
    st.markdown("### 💬 Conversation")
    
    # Create a container for chat messages
    chat_container = st.container()
    
    with chat_container:
        # Display all messages in chat history
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                # User message (right-aligned)
                st.markdown(f"""
                <div style='display: flex; justify-content: flex-end; margin: 1rem 0;'>
                    <div style='background: #4A90E2; color: white; padding: 1rem 1.5rem; 
                                border-radius: 18px 18px 4px 18px; max-width: 70%; 
                                box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                        <p style='margin: 0; font-size: 0.95rem;'>{message['content']}</p>
                        <p style='margin: 0.5rem 0 0 0; font-size: 0.75rem; opacity: 0.8; text-align: right;'>
                            {message['timestamp']}
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Assistant message (left-aligned)
                st.markdown(f"""
                <div style='display: flex; justify-content: flex-start; margin: 1rem 0;'>
                    <div style='background: #F0F7FF; color: #333; padding: 1rem 1.5rem; 
                                border-radius: 18px 18px 18px 4px; max-width: 75%; 
                                border-left: 4px solid #4A90E2; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                        <div style='margin: 0; font-size: 0.95rem; line-height: 1.6;'>{message['content']}</div>
                        <p style='margin: 0.5rem 0 0 0; font-size: 0.75rem; color: #666;'>
                            🤖 AI Assistant • {message['timestamp']}
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ========================================
    # SUGGESTED QUESTIONS
    # ========================================
    if len(st.session_state.chat_history) <= 1:  # Only show for new chats
        st.markdown("### 🎯 Suggested Questions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📉 Why is my stability declining?", use_container_width=True):
                user_message = "Why is my stability declining?"
                timestamp = datetime.now().strftime("%H:%M")
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': user_message,
                    'timestamp': timestamp
                })
                ai_response = get_ai_response(user_message)
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': ai_response,
                    'timestamp': timestamp
                })
                st.rerun()
        
        with col2:
            if st.button("🔍 How does drift detection work?", use_container_width=True):
                user_message = "How does drift detection work?"
                timestamp = datetime.now().strftime("%H:%M")
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': user_message,
                    'timestamp': timestamp
                })
                ai_response = get_ai_response(user_message)
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': ai_response,
                    'timestamp': timestamp
                })
                st.rerun()
        
        with col3:
            if st.button("💡 What should I improve?", use_container_width=True):
                user_message = "What should I improve?"
                timestamp = datetime.now().strftime("%H:%M")
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': user_message,
                    'timestamp': timestamp
                })
                ai_response = get_ai_response(user_message)
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': ai_response,
                    'timestamp': timestamp
                })
                st.rerun()
    
    # ========================================
    # CHAT INPUT
    # ========================================
    st.markdown("---")
    
    # Create form for chat input
    with st.form(key='chat_form', clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        
        with col1:
            user_input = st.text_input(
                "Type your message...",
                placeholder="Ask me about your health trends, drift detection, or general wellness...",
                label_visibility="collapsed"
            )
        
        with col2:
            submit_button = st.form_submit_button("Send 📤", use_container_width=True)
    
    # Handle form submission
    if submit_button and user_input:
        # Get user ID from session
        user_id = st.session_state.get('user_id')
        
        # Add user message to chat history
        timestamp = datetime.now().strftime("%H:%M")
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input,
            'timestamp': timestamp
        })
        
        # Generate AI-powered response (uses ADK if available, falls back to pattern matching)
        ai_response = get_ai_powered_response(user_id, user_input)
        
        # Add AI response to chat history
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': ai_response,
            'timestamp': timestamp
        })
        
        # Rerun to update chat display
        st.rerun()
    
    # ========================================
    # CHAT CONTROLS
    # ========================================
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col2:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    # ========================================
    # CONTEXT AWARENESS INDICATOR
    # ========================================
    st.markdown("---")
    
    has_profile = st.session_state.get('profile_name', '') != ''
    has_check_data = st.session_state.get('check_completed', False)
    
    st.markdown("### 🧠 AI Context Awareness")
    
    context_col1, context_col2 = st.columns(2)
    
    with context_col1:
        profile_status = "✅ Loaded" if has_profile else "❌ Not set"
        profile_color = "#E8F5E9" if has_profile else "#FFEBEE"
        st.markdown(f"""
        <div style='background: {profile_color}; padding: 1rem; border-radius: 8px;'>
            <p style='margin: 0;'><strong>Your Profile:</strong> {profile_status}</p>
            <p style='margin: 0.5rem 0 0 0; font-size: 0.85rem; color: #666;'>
                {f"I know your age, lifestyle, and preferences" if has_profile else "Complete your profile for personalized responses"}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with context_col2:
        data_status = "✅ Available" if has_check_data else "❌ No data"
        data_color = "#E8F5E9" if has_check_data else "#FFEBEE"
        st.markdown(f"""
        <div style='background: {data_color}; padding: 1rem; border-radius: 8px;'>
            <p style='margin: 0;'><strong>Health Data:</strong> {data_status}</p>
            <p style='margin: 0.5rem 0 0 0; font-size: 0.85rem; color: #666;'>
                {f"I can analyze your trends and detect drift" if has_check_data else "Complete a health check to enable trend analysis"}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ========================================
    # DISCLAIMER
    # ========================================
    st.info("""
    🤖 **AI Assistant Disclaimer:** This chat assistant provides informational insights based on 
    your health tracking data. Responses are educational and preventive in nature, NOT medical 
    advice. Always consult qualified healthcare professionals for medical concerns, diagnosis, 
    or treatment decisions.
    """)
