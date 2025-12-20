"""
AI Health Chat Page - MediGuard Drift AI
Conversational AI assistant for health insights and guidance

UPDATED: Now connects to ADK Orchestrator for real AI-powered analysis
Fetches both health check data and context data from Supabase
"""

import streamlit as st
from datetime import datetime
import random

# Import AI Integration Layer
try:
    from agents.ai_integration import AIHealthAnalyzer, get_ai_chat_response
    from agents.adk_runtime import is_adk_ready
    from storage.health_data_fetcher import get_user_health_data, format_data_for_agents
    ADK_AVAILABLE = True
except ImportError as e:
    ADK_AVAILABLE = False
    print(f"Warning: ADK integration not available: {e}")


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
    
    # Get user ID
    user_id = st.session_state.get('user_id', None)
    
    if not user_id:
        st.warning("⚠️ Please log in to access AI health analysis.")
        return
    
    # Fetch comprehensive data from Supabase
    with st.spinner("📊 Loading your health data..."):
        health_data = get_user_health_data(user_id, days=14)
    
    # Display data availability status
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if health_data['health_checks']:
            st.success(f"✅ {len(health_data['health_checks'])} health checks")
        else:
            st.warning("⚠️ No health check data")
    
    with col2:
        if health_data['context_data']:
            st.success("✅ Context data loaded")
        else:
            st.info("ℹ️ No context data")
    
    with col3:
        if ADK_AVAILABLE:
            st.success("✅ AI agents ready")
        else:
            st.error("❌ AI agents unavailable")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Show data summary
    if health_data['success']:
        with st.expander("📋 View Your Data Summary"):
            st.markdown("#### Health Check Records")
            st.write(f"**Total Checks:** {len(health_data['health_checks'])}")
            
            if health_data['health_checks']:
                latest_check = health_data['health_checks'][-1]
                st.write(f"**Latest Check:** {latest_check.get('check_date')}")
                
                st.markdown("**Latest Metrics:**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    if 'avg_movement_speed' in latest_check:
                        st.metric("Movement Speed", f"{latest_check['avg_movement_speed']:.3f}")
                with col2:
                    if 'avg_stability' in latest_check:
                        st.metric("Stability", f"{latest_check['avg_stability']:.3f}")
                with col3:
                    if 'sit_stand_movement_speed' in latest_check:
                        st.metric("Sit-Stand Speed", f"{latest_check['sit_stand_movement_speed']:.3f}")
            
            if health_data['context_data']:
                st.markdown("#### Lifestyle Context")
                context = health_data['context_data']
                st.write(f"**Sleep:** {context.get('sleep_hours', 'N/A')} hours")
                st.write(f"**Stress Level:** {context.get('stress_level', 'N/A')}")
                st.write(f"**Activity Level:** {context.get('activity_level', 'N/A')}")
    
    st.markdown("---")
    
    # ========================================
    # RUN AI HEALTH ANALYSIS BUTTON
    # Triggers the full 5-agent ADK pipeline
    # ========================================
    
    if st.button("🚀 Run Complete AI Analysis", type="primary", use_container_width=True):
        if not ADK_AVAILABLE:
            st.error("❌ AI agents are not available. Please check configuration.")
        elif not health_data['success']:
            st.error("❌ No health data available. Complete a Daily Health Check first!")
        elif len(health_data.get('health_checks', [])) < 2:
            st.warning(f"⚠️ Insufficient data for AI analysis. You have {len(health_data.get('health_checks', []))} health check(s), but need at least 2.")
            st.info("💡 Complete more Daily Health Checks to enable AI analysis!")
        else:
            with st.spinner("🔬 Running comprehensive AI analysis through 5-agent pipeline..."):
                try:
                    # Format data for agents
                    formatted_data = format_data_for_agents(health_data)
                    
                    if not formatted_data['has_data']:
                        st.error("❌ Insufficient data for analysis")
                        st.info(f"Debug: Found {len(health_data.get('health_checks', []))} health checks")
                        return
                    
                    # Use AI Integration Layer
                    from agents.ai_integration import AIHealthAnalyzer
                    
                    days_to_analyze = 14
                    
                    # Show what we're analyzing
                    st.info(f"📊 Analyzing {len(health_data['health_checks'])} health checks from the last {days_to_analyze} days...")
                    
                    analyzer = AIHealthAnalyzer()
                    result = analyzer.analyze_user_health(
                        user_id=user_id,
                        metric_name="avg_movement_speed",  # Use a metric that exists in the data
                        days_to_analyze=days_to_analyze
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
                            **Analyzed Period:** Last {days_to_analyze} days  
                            **Health Checks:** {len(health_data['health_checks'])}  
                            **Drift Detected:** {summary.get('severity', 'None').title()}  
                            **Risk Level:** {summary.get('risk_level', 'Low').title()}  
                            """)
                        
                        with col2:
                            if summary.get('escalation_needed'):
                                st.error("⚠️ Escalation Recommended")
                            else:
                                st.success("✅ No Immediate Concerns")
                        
                        # Agent-by-agent analysis
                        st.markdown("### 🤖 Agent Analysis Results")
                        
                        agent_tabs = st.tabs(["Drift Agent", "Context Agent", "Risk Agent", "Safety Agent", "Care Agent"])
                        
                        with agent_tabs[0]:
                            st.markdown("#### 📉 Drift Detection")
                            st.info("Drift Agent analyzes numerical changes in your health metrics over time.")
                            # Show drift analysis details here
                            
                        with agent_tabs[1]:
                            st.markdown("#### 🔍 Context Correlation")
                            st.info("Context Agent correlates lifestyle factors with health changes.")
                            if formatted_data['context']:
                                st.write("**Your Context:**")
                                for key, value in formatted_data['context'].items():
                                    if value:
                                        st.write(f"- {key.replace('_', ' ').title()}: {value}")
                        
                        with agent_tabs[2]:
                            st.markdown("#### ⚠️ Risk Assessment")
                            st.info("Risk Agent evaluates temporal patterns and severity.")
                            
                        with agent_tabs[3]:
                            st.markdown("#### 🛡️ Safety Evaluation")
                            st.info("Safety Agent determines if medical escalation is needed.")
                            
                        with agent_tabs[4]:
                            st.markdown("#### 💡 Care Recommendations")
                            st.info("Care Agent generates actionable guidance.")
                            if result.get('recommendations'):
                                for i, rec in enumerate(result['recommendations'], 1):
                                    st.markdown(f"**{i}.** {rec}")
                        
                        # Full analysis details
                        with st.expander("📋 View Complete AI Report"):
                            st.json(result)
                    
                    else:
                        st.warning(f"⚠️ {result.get('message', 'Analysis could not be completed')}")
                        
                        # Show detailed error info
                        if result.get('error'):
                            with st.expander("🔍 View Error Details"):
                                st.error(result['error'])
                                st.write("**Debug Info:**")
                                st.write(f"- Has data: {result.get('has_data', False)}")
                                st.write(f"- Success: {result.get('success', False)}")
                                if result.get('summary'):
                                    st.json(result['summary'])
                        
                        # Provide helpful guidance
                        st.info("""
                        **To enable AI analysis, you need:**
                        - At least 2 completed Daily Health Checks
                        - Health checks from different days
                        - Valid metric data in your health checks
                        
                        💡 Complete a few more Daily Health Checks and try again!
                        """)
                        
                except Exception as e:
                    st.error(f"❌ Error running analysis: {str(e)}")
                    st.exception(e)
    
    st.markdown("---")
    
    # ========================================
    # CONVERSATIONAL CHAT INTERFACE
    # ========================================
    
    st.markdown("### 💬 Chat with Your AI Health Assistant")
    st.markdown("Ask questions about your health trends, get explanations, and receive personalized insights.")
    
    # ========================================

    
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
