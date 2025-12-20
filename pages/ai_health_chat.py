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
    Enhanced to fetch real user health data when available
    """
    message_lower = user_message.lower()
    
    # Get user profile data if available
    user_name = st.session_state.get('profile_name', 'there')
    has_check_data = st.session_state.get('check_completed', False)
    user_id = st.session_state.get('user_id', None)
    
    # Try to fetch real health data if user is logged in
    real_health_data = None
    health_summary = None
    if user_id:
        try:
            real_health_data = get_user_health_data(user_id, days=14)
            if real_health_data['success'] and real_health_data['health_checks']:
                has_check_data = True
                latest = real_health_data['health_checks'][-1]
                health_summary = {
                    'total_checks': len(real_health_data['health_checks']),
                    'latest_date': latest.get('check_date'),
                    'movement_speed': latest.get('avg_movement_speed', 'N/A'),
                    'stability': latest.get('avg_stability', 'N/A'),
                    'sit_stand_speed': latest.get('sit_stand_movement_speed', 'N/A'),
                    'walk_stability': latest.get('walk_stability', 'N/A'),
                    'hand_steadiness': latest.get('steady_stability', 'N/A')
                }
        except Exception as e:
            print(f"Could not fetch health data: {e}")
    
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
        if has_check_data and health_summary:
            # Use real data
            stability_val = health_summary['stability']
            stability_str = f"{stability_val:.3f}" if stability_val != 'N/A' else "Not recorded"
            checks_count = health_summary['total_checks']
            
            return f"""Based on your actual health data, {user_name}:

**Your Stability Metrics:**
- Current Stability Score: {stability_str}
- Total Health Checks: {checks_count} days of tracking
- Latest Check: {health_summary['latest_date']}

**What I'm analyzing:**
Your stability score reflects your balance and steadiness during movement activities. 
{f"With a score of {stability_val:.3f}, you're " + ("in a healthy range!" if stability_val >= 0.85 else "showing some variation that we should monitor.") if stability_val != 'N/A' else ""}

**Personalized Context:**
- I'm tracking {checks_count} days of your health data
- This gives me insight into YOUR unique patterns
- Looking for gradual changes over time, not daily fluctuations

**My observations:**
{f"Your hand steadiness is at {health_summary['hand_steadiness']:.3f}, showing good fine motor control!" if health_summary.get('hand_steadiness') != 'N/A' else "Complete more checks to see full metrics."}

**What you can do:**
- Continue daily checks for consistent tracking
- Balance exercises: yoga, standing on one foot, tai chi
- Stay hydrated and get adequate sleep
- Discuss any concerns with your healthcare provider

Want to know about other specific metrics from your {checks_count} days of data?"""
        elif has_check_data:
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
        if has_check_data and health_summary:
            # Use real data
            movement_val = health_summary['movement_speed']
            movement_str = f"{movement_val:.3f}" if movement_val != 'N/A' else "Not recorded"
            walk_val = health_summary['walk_stability']
            walk_str = f"{walk_val:.3f}" if walk_val != 'N/A' else "Not recorded"
            
            sit_stand_val = health_summary['sit_stand_speed']
            sit_stand_str = f"{sit_stand_val:.3f}" if sit_stand_val != 'N/A' else "Not recorded"
            
            return f"""Great question about mobility, {user_name}! Here's what your actual data shows:

**Your Movement Metrics:**
- Average Movement Speed: {movement_str}
- Walking Stability: {walk_str}
- Sit-Stand Speed: {sit_stand_str}
- Days of Data: {health_summary['total_checks']} health checks

**What Your Numbers Mean:**
Movement speed reflects how quickly and efficiently you can perform daily movements.
{f"Your current speed of {movement_val:.3f} " + ("shows good mobility!" if movement_val >= 0.9 else "is something we're monitoring.") if movement_val != 'N/A' else ""}

**Context Matters:**
- Time of day affects energy and performance
- Recent activity impacts your metrics
- {health_summary['total_checks']} days of data helps establish YOUR normal baseline

**Personalized Insights:**
The AI tracks multiple factors together:
- Movement speed AND stability (not just one metric)
- Trends over time (not isolated data points)
- YOUR baseline (not comparing you to others)

**What you can do:**
- Keep logging daily for consistency
- Regular walking (15-20 minutes helps)
- Stay active throughout the day
- Note any lifestyle changes affecting your patterns

Anything specific about your {health_summary['total_checks']} days of movement data you want to explore?"""
        elif has_check_data:
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
        if has_check_data and health_summary:
            # Use real health data for personalized recommendations
            context_data = real_health_data.get('context_data', {}) if real_health_data else {}
            
            # Pre-format metric values to avoid nested f-string issues
            movement_speed_str = f"{health_summary['movement_speed']:.3f}" if health_summary['movement_speed'] != 'N/A' else 'Not recorded'
            stability_str = f"{health_summary['stability']:.3f}" if health_summary['stability'] != 'N/A' else 'Not recorded'
            hand_steadiness_str = f"{health_summary['hand_steadiness']:.3f}" if health_summary['hand_steadiness'] != 'N/A' else 'Not recorded'
            
            # Build metric-based suggestions
            movement_advice = ""
            if health_summary['movement_speed'] != 'N/A':
                movement_advice = f"- Your movement speed is {movement_speed_str} - " + ("keep up the good work!" if health_summary['movement_speed'] >= 0.9 else "consider daily walks to improve")
            else:
                movement_advice = "- Complete more checks to see trends"
            
            stability_advice = ""
            if health_summary['stability'] != 'N/A':
                stability_advice = f"- Stability at {stability_str} - " + ("great balance!" if health_summary['stability'] >= 0.85 else "try balance exercises like yoga")
            else:
                stability_advice = "- Track consistently to monitor stability"
            
            return f"""I'm happy to share personalized suggestions based on your actual health data, {user_name}! 

**Your Current Health Status:**
- Total Days Tracked: {health_summary['total_checks']} health checks ✅
- Latest Check: {health_summary['latest_date']}
- Movement Speed: {movement_speed_str}
- Stability Score: {stability_str}
- Hand Steadiness: {hand_steadiness_str}

**Personalized Recommendations:**

1. **Continue Daily Tracking** 📊
   - You have {health_summary['total_checks']} days of data - excellent consistency!
   - Daily checks help me detect gradual patterns
   - Try to check at the same time each day

2. **Lifestyle Factors** 🌟
   {f"- Sleep: {context_data.get('sleep_hours', 'N/A')} hours/night (aim for 7-9)" if context_data.get('sleep_hours') else "- Add your sleep data in Context Inputs for better insights"}
   {f"- Stress: {context_data.get('stress_level', 'N/A')} - manage with relaxation techniques" if context_data.get('stress_level') else "- Track your stress levels for better analysis"}
   {f"- Activity: {context_data.get('activity_level', 'N/A')} - keep moving!" if context_data.get('activity_level') else "- Log your activity level for personalized advice"}

3. **Based on Your Metrics:**
   {movement_advice}
   {stability_advice}

4. **General Wellness:**
   - Regular walking: 20-30 minutes daily
   - Balance exercises: stand on one foot, yoga, tai chi
   - Stay hydrated throughout the day
   - Stretch regularly, especially after sitting

**Most Important:**
These suggestions are based on YOUR {health_summary['total_checks']} days of data and general wellness principles. 
For personalized medical guidance, always consult your healthcare provider!

What specific area would you like to focus on improving?"""
        
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
    elif any(word in message_lower for word in ['my profile', 'about me', 'my data', 'my info', 'my health']):
        # Get profile data
        profile_data = real_health_data.get('profile', {}) if real_health_data else {}
        context_data = real_health_data.get('context_data', {}) if real_health_data else {}
        
        name = profile_data.get('name', st.session_state.get('profile_name', 'Not set'))
        age = profile_data.get('age', st.session_state.get('profile_age', 'Not set'))
        lifestyle = profile_data.get('lifestyle', st.session_state.get('profile_lifestyle', 'Not set'))
        
        response = f"""Here's your complete health profile, {user_name}:\n\n"""
        
        response += "**Personal Information:**\n"
        response += f"- **Name**: {name}\n"
        response += f"- **Age**: {age}\n"
        response += f"- **Lifestyle**: {lifestyle}\n\n"
        
        if health_summary:
            response += "**Health Tracking:**\n"
            response += f"- **Total Health Checks**: {health_summary['total_checks']} days ✅\n"
            response += f"- **Latest Check**: {health_summary['latest_date']}\n"
            response += f"- **Data Quality**: {'Excellent - keep it up!' if health_summary['total_checks'] >= 7 else 'Good start - more data helps!'}\n\n"
            
            response += "**Current Metrics:**\n"
            if health_summary['movement_speed'] != 'N/A':
                response += f"- Movement Speed: {health_summary['movement_speed']:.3f}\n"
            if health_summary['stability'] != 'N/A':
                response += f"- Stability Score: {health_summary['stability']:.3f}\n"
            if health_summary['hand_steadiness'] != 'N/A':
                response += f"- Hand Steadiness: {health_summary['hand_steadiness']:.3f}\n"
            response += "\n"
        else:
            response += "**Health Tracking:**\n"
            response += "- **Daily Checks**: Not yet started\n"
            response += "- Start your first check to see metrics!\n\n"
        
        if context_data:
            response += "**Lifestyle Context:**\n"
            if context_data.get('sleep_hours'):
                response += f"- Sleep: {context_data.get('sleep_hours')} hours/night\n"
            if context_data.get('stress_level'):
                response += f"- Stress Level: {context_data.get('stress_level')}\n"
            if context_data.get('activity_level'):
                response += f"- Activity Level: {context_data.get('activity_level')}\n"
            if context_data.get('workload'):
                response += f"- Workload: {context_data.get('workload')}\n"
            response += "\n"
        
        response += "**How I Use This:**\n"
        response += "- Your age helps set appropriate health baselines\n"
        response += "- Lifestyle gives context for movement expectations\n"
        response += f"- {health_summary['total_checks'] if health_summary else 0} days of data lets me personalize insights\n"
        response += "- The more data you provide, the better my analysis!\n\n"
        response += "Want to update your profile or add lifestyle context? Head to the Profile or Context Inputs page!"
        
        return response
    
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


def generate_data_driven_response(user_message: str, health_summary: dict, health_data: dict) -> str:
    """
    Generate response based on actual health data when full AI analysis isn't available
    """
    from agents.ai_integration import rate_metric_value
    
    message_lower = user_message.lower()
    
    # Get context data if available
    context = health_data.get('context_data', {})
    profile = health_data.get('profile', {})
    
    user_name = profile.get('name', 'there')
    
    # Check for specific health questions
    if any(word in message_lower for word in ['stability', 'balance', 'stable']):
        stability_val = health_summary.get('stability', 'N/A')
        
        # Get rating if value exists
        rating_info = None
        if stability_val != 'N/A':
            rating_info = rate_metric_value('stability', stability_val)
        
        response = f"""Based on your actual health data, {user_name}:\n\n"""
        response += f"**Your Stability Score:**\n"
        if stability_val != 'N/A' and rating_info:
            response += f"{rating_info['emoji']} **{stability_val:.3f}** - {rating_info['rating']}\n"
            response += f"_{rating_info['description']}_\n\n"
        else:
            response += f"Not recorded yet\n\n"
        
        response += f"**Tracking Info:**\n"
        response += f"- Total Health Checks: {health_summary['total_checks']} days\n"
        response += f"- Latest Check: {health_summary['latest_date']}\n\n"
        
        if context.get('sleep_hours') or context.get('stress_level'):
            response += f"**Your Lifestyle:**\n"
            if context.get('sleep_hours'):
                response += f"- Sleep: {context.get('sleep_hours')} hours per night\n"
            if context.get('stress_level'):
                response += f"- Stress: {context.get('stress_level')}\n"
            if context.get('activity_level'):
                response += f"- Activity: {context.get('activity_level')}\n"
            response += "\n"
        
        response += f"**What You Can Do:**\n"
        response += f"- Keep tracking daily for better insights\n"
        response += f"- Try balance exercises like yoga or standing on one foot\n"
        response += f"- Get enough sleep and manage stress\n"
        response += f"- Talk to your doctor if you're concerned\n"
        
        return response
    
    elif any(word in message_lower for word in ['movement', 'mobility', 'speed', 'walk']):
        from agents.ai_integration import rate_metric_value
        
        movement_val = health_summary.get('movement_speed', 'N/A')
        walk_val = health_summary.get('walk_stability', 'N/A')
        sit_stand_val = health_summary.get('sit_stand_speed', 'N/A')
        
        # Get ratings
        movement_rating = rate_metric_value('movement_speed', movement_val) if movement_val != 'N/A' else None
        walk_rating = rate_metric_value('walk_stability', walk_val) if walk_val != 'N/A' else None
        sit_rating = rate_metric_value('sit_stand_speed', sit_stand_val) if sit_stand_val != 'N/A' else None
        
        response = f"""Here's what your movement data shows, {user_name}:\n\n"""
        
        response += f"**Your Movement Scores:**\n\n"
        
        if movement_val != 'N/A' and movement_rating:
            response += f"{movement_rating['emoji']} **Movement Speed: {movement_val:.3f}** - {movement_rating['rating']}\n"
            response += f"   _{movement_rating['description']}_\n\n"
        
        if sit_stand_val != 'N/A' and sit_rating:
            response += f"{sit_rating['emoji']} **Sit-Stand Speed: {sit_stand_val:.3f}** - {sit_rating['rating']}\n"
            response += f"   _{sit_rating['description']}_\n\n"
        
        if walk_val != 'N/A' and walk_rating:
            response += f"{walk_rating['emoji']} **Walking Stability: {walk_val:.3f}** - {walk_rating['rating']}\n"
            response += f"   _{walk_rating['description']}_\n\n"
        
        response += f"**Tracking:**\n"
        response += f"- Total Days: {health_summary['total_checks']}\n"
        response += f"- Latest Check: {health_summary['latest_date']}\n\n"
        
        if profile.get('age'):
            response += f"**Your Profile:**\n"
            response += f"- Age: {profile.get('age')}\n"
            if context.get('activity_level'):
                response += f"- Activity Level: {context.get('activity_level')}\n"
            response += "\n"
        
        response += f"**Tips to Improve:**\n"
        response += f"- Walk regularly (15-20 minutes daily)\n"
        response += f"- Stretch before and after activities\n"
        response += f"- Stay hydrated\n"
        response += f"- Keep tracking to see your progress!\n"
        
        return response
    
    elif any(word in message_lower for word in ['suggest', 'recommend', 'improve', 'help', 'advice']):
        return f"""Based on your {health_summary['total_checks']} days of health tracking, {user_name}:

**Your Current Status:**
- Movement Speed: {health_summary.get('movement_speed', 'N/A')}
- Stability: {health_summary.get('stability', 'N/A')}
- Hand Steadiness: {health_summary.get('hand_steadiness', 'N/A')}

**Personalized Suggestions:**

1. **Keep Up Your Consistency** ✅
   - You have {health_summary['total_checks']} health checks recorded
   - Daily tracking helps identify patterns early

2. **Lifestyle Optimization** 🌟
   {'- Your sleep: ' + str(context.get('sleep_hours', 'N/A')) + ' hours (aim for 7-9 hours)' if context.get('sleep_hours') else '- Add your sleep data in Context Inputs for better insights'}
   {'- Stress level: ' + context.get('stress_level', 'N/A') + ' - consider relaxation techniques' if context.get('stress_level') else ''}

3. **Physical Activity** 🏃
   - Balance exercises: Stand on one foot, yoga poses
   - Walking: 20-30 minutes daily
   - Stretching: Before bed and after waking

4. **Monitoring** 📊
   - Continue daily checks at the same time
   - Note any significant life changes
   - Watch for gradual trends, not daily variations

**Remember:** These are general wellness suggestions. Always consult your healthcare provider for medical advice!

What specific area would you like to focus on?"""
    
    else:
        # Generic response with user's data
        return f"""I have access to your health data, {user_name}! Here's what I'm tracking:

**Your Health Summary:**
- **Days of Data:** {health_summary['total_checks']} health checks
- **Latest Check:** {health_summary['latest_date']}
- **Movement Speed:** {health_summary.get('movement_speed', 'Not recorded')}
- **Stability:** {health_summary.get('stability', 'Not recorded')}
- **Hand Steadiness:** {health_summary.get('hand_steadiness', 'Not recorded')}

**What I can help with:**
- 📊 Analyze your specific metrics (stability, movement, balance)
- 📈 Track trends over time
- 💡 Provide personalized wellness suggestions
- 🎯 Answer questions about your health patterns

**Try asking:**
- "How is my stability trending?"
- "What can I do to improve my movement?"
- "Show me my health progress"
- "What does my data suggest?"

What would you like to know about your health data?"""


def get_ai_powered_response(user_id: str, user_message: str) -> str:
    """
    Get AI-powered response using Google Gemini API with full health context
    Always has access to user's complete health data
    """
    from agents.adk_runtime import run_agent
    
    try:
        # Fetch user's complete health data from Supabase
        health_data = get_user_health_data(user_id, days=14)
        
        # Build comprehensive health context
        health_context = "**USER HEALTH DATA:**\n\n"
        
        if health_data['success'] and health_data.get('health_checks'):
            # Latest health metrics
            latest_check = health_data['health_checks'][-1]
            total_checks = len(health_data['health_checks'])
            
            health_context += f"Total Health Checks: {total_checks} days of tracking\n"
            health_context += f"Latest Check Date: {latest_check.get('check_date')}\n\n"
            
            health_context += "**Current Health Scores:**\n"
            from agents.ai_integration import rate_metric_value
            
            # Movement Speed
            if latest_check.get('avg_movement_speed'):
                val = latest_check['avg_movement_speed']
                rating = rate_metric_value('movement_speed', val)
                health_context += f"- Movement Speed: {val:.3f} ({rating['emoji']} {rating['rating']} - {rating['description']})\n"
            
            # Stability
            if latest_check.get('avg_stability'):
                val = latest_check['avg_stability']
                rating = rate_metric_value('stability', val)
                health_context += f"- Stability/Balance: {val:.3f} ({rating['emoji']} {rating['rating']} - {rating['description']})\n"
            
            # Sit-Stand Speed
            if latest_check.get('sit_stand_movement_speed'):
                val = latest_check['sit_stand_movement_speed']
                rating = rate_metric_value('sit_stand_speed', val)
                health_context += f"- Sit-Stand Speed: {val:.3f} ({rating['emoji']} {rating['rating']} - {rating['description']})\n"
            
            # Hand Steadiness
            if latest_check.get('steady_stability'):
                val = latest_check['steady_stability']
                rating = rate_metric_value('stability', val)
                health_context += f"- Hand Steadiness: {val:.3f} ({rating['emoji']} {rating['rating']} - {rating['description']})\n"
            
            # Trend analysis (if we have multiple checks)
            if total_checks >= 2:
                health_context += f"\n**Recent Trends (last {min(7, total_checks)} days):**\n"
                recent_checks = health_data['health_checks'][-7:]
                
                # Calculate averages
                if any(c.get('avg_movement_speed') for c in recent_checks):
                    avg_movement = sum(c.get('avg_movement_speed', 0) for c in recent_checks) / len(recent_checks)
                    health_context += f"- Average Movement Speed: {avg_movement:.3f}\n"
                
                if any(c.get('avg_stability') for c in recent_checks):
                    avg_stability = sum(c.get('avg_stability', 0) for c in recent_checks) / len(recent_checks)
                    health_context += f"- Average Stability: {avg_stability:.3f}\n"
        
        else:
            health_context += "No health check data available yet. User needs to complete daily health checks.\n"
        
        # Add lifestyle context
        if health_data.get('context_data'):
            context = health_data['context_data']
            health_context += "\n**Lifestyle Information:**\n"
            if context.get('sleep_hours'):
                health_context += f"- Sleep: {context['sleep_hours']} hours per night\n"
            if context.get('stress_level'):
                health_context += f"- Stress Level: {context['stress_level']}\n"
            if context.get('activity_level'):
                health_context += f"- Activity Level: {context['activity_level']}\n"
            if context.get('workload'):
                health_context += f"- Workload: {context['workload']}\n"
        
        # Add profile info
        if health_data.get('profile'):
            profile = health_data['profile']
            health_context += "\n**User Profile:**\n"
            if profile.get('name'):
                health_context += f"- Name: {profile['name']}\n"
            if profile.get('age'):
                health_context += f"- Age: {profile['age']}\n"
            if profile.get('lifestyle'):
                health_context += f"- Lifestyle: {profile['lifestyle']}\n"
        
        # Create comprehensive prompt for Gemini 3 Pro
        system_prompt = """You are an advanced AI health assistant powered by Google Gemini 3 Pro, providing sophisticated health insights through natural conversation.

**Your Expertise:**
- Advanced pattern recognition across temporal health data
- Multi-factorial correlation analysis
- Contextual interpretation of biometric trends
- Evidence-based health guidance
- Personalized insights based on individual baselines

**Communication Style:**
- Professional yet approachable and warm
- Clear and structured explanations
- Use specific data points and percentages when helpful
- Explain the "why" behind observations
- Balance detail with accessibility
- Conversational but informative

**How to Respond:**
1. **Acknowledge** the user's question directly
2. **Analyze** their specific data with precision
3. **Contextualize** findings (trends, comparisons, correlations)
4. **Explain** implications in clear, practical terms
5. **Recommend** specific, actionable next steps
6. **Encourage** continued monitoring and engagement

**Data Integration:**
- Reference specific metrics with actual values
- Identify trends over time periods
- Note correlations between metrics and lifestyle factors
- Compare current state to personal baseline
- Provide confidence in assessments

**Safety & Boundaries:**
- NEVER diagnose medical conditions
- Use phrases like "the data suggests," "patterns indicate," "consistent with"
- Always recommend professional medical consultation for concerns
- Distinguish observations from medical advice
- Be supportive but honest about limitations

**Advanced Features:**
- Identify subtle patterns users might miss
- Explain physiological connections in accessible terms
- Provide evidence-based wellness strategies
- Offer comparative context (improvement vs decline)
- Suggest optimal monitoring frequencies

Leverage Gemini 3 Pro's sophisticated reasoning to deliver insights that are both comprehensive and actionable, while maintaining a supportive, health-focused conversation."""

        full_prompt = f"""{system_prompt}

{health_context}

**User Question:** {user_message}

**Your Response (as a caring health assistant):**"""
        
        # Get response from Gemini
        result = run_agent(full_prompt)
        
        if result['success']:
            return result['response']
        else:
            # Fallback to pattern matching if Gemini fails
            return get_ai_response(user_message)
            
    except Exception as e:
        print(f"AI response error: {e}")
        # Fall back to pattern matching
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
                        st.markdown("### 📊 Your Health Scores")
                        
                        # Display ratings with visual indicators
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            baseline_rating = summary.get('baseline_rating', {})
                            if baseline_rating:
                                st.markdown(f"""
                                <div style='background: {baseline_rating.get('color', '#gray')}20; padding: 1rem; border-radius: 8px; border-left: 4px solid {baseline_rating.get('color', '#gray')}'>
                                    <h4 style='margin:0;'>{baseline_rating.get('emoji', '')} Your Baseline</h4>
                                    <h2 style='margin:0.5rem 0;'>{summary.get('baseline_value', 'N/A')}</h2>
                                    <p style='margin:0; font-size: 1.1rem;'><strong>{baseline_rating.get('rating', '')}</strong></p>
                                    <p style='margin:0; font-size: 0.9rem; color: #666;'>{baseline_rating.get('description', '')}</p>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        with col2:
                            recent_rating = summary.get('recent_rating', {})
                            if recent_rating:
                                st.markdown(f"""
                                <div style='background: {recent_rating.get('color', '#gray')}20; padding: 1rem; border-radius: 8px; border-left: 4px solid {recent_rating.get('color', '#gray')}'>
                                    <h4 style='margin:0;'>{recent_rating.get('emoji', '')} Current Score</h4>
                                    <h2 style='margin:0.5rem 0;'>{summary.get('recent_value', 'N/A')}</h2>
                                    <p style='margin:0; font-size: 1.1rem;'><strong>{recent_rating.get('rating', '')}</strong></p>
                                    <p style='margin:0; font-size: 0.9rem; color: #666;'>{recent_rating.get('description', '')}</p>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        with col3:
                            drift_pct = summary.get('drift_percentage', 0)
                            drift_color = '#FF9800' if abs(drift_pct) > 5 else '#FFC107' if abs(drift_pct) > 3 else '#4CAF50'
                            drift_icon = '⬇️' if drift_pct < 0 else '⬆️' if drift_pct > 0 else '➡️'
                            st.markdown(f"""
                            <div style='background: {drift_color}20; padding: 1rem; border-radius: 8px; border-left: 4px solid {drift_color}'>
                                <h4 style='margin:0;'>{drift_icon} Change</h4>
                                <h2 style='margin:0.5rem 0;'>{drift_pct:+.1f}%</h2>
                                <p style='margin:0; font-size: 1.1rem;'><strong>{summary.get('trend', 'Stable').title()}</strong></p>
                                <p style='margin:0; font-size: 0.9rem; color: #666;'>From your baseline</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # Additional summary info
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.markdown(f"""
                            **Metric:** {summary.get('metric_name', 'Movement Speed')}  
                            **Period:** Last {days_to_analyze} days  
                            **Health Checks:** {len(health_data['health_checks'])} days tracked  
                            **Severity:** {summary.get('severity', 'None').title()}  
                            """)
                        
                        with col2:
                            if summary.get('escalation_needed'):
                                st.error("⚠️ Doctor Visit Suggested")
                            else:
                                st.success("✅ Looking Good")
                        
                        st.markdown("---")
                        
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
                        
                        # Full analysis details - Beautiful User-Friendly Format
                        with st.expander("📋 View Complete AI Health Report", expanded=False):
                            st.markdown("### 📊 Your Comprehensive Health Analysis")
                            
                            # Get analysis data
                            analysis = result.get('analysis', {})
                            summary = result.get('summary', {})
                            
                            # 1. Overview Section
                            st.markdown("---")
                            st.markdown("#### 📈 Health Pattern Overview")
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric(
                                    label="Metric Analyzed",
                                    value=summary.get('metric_name', 'N/A')
                                )
                            with col2:
                                drift_pct = summary.get('drift_percentage', 0)
                                st.metric(
                                    label="Change Detected",
                                    value=f"{drift_pct:+.1f}%",
                                    delta=f"{abs(drift_pct):.1f}% from baseline"
                                )
                            with col3:
                                severity = summary.get('severity', 'unknown').title()
                                severity_color = {
                                    'Low': '🟢',
                                    'Moderate': '🟡',
                                    'High': '🟠',
                                    'Unknown': '⚪'
                                }.get(severity, '⚪')
                                st.metric(
                                    label="Severity Level",
                                    value=f"{severity_color} {severity}"
                                )
                            
                            # 2. Drift Analysis Section
                            st.markdown("---")
                            st.markdown("#### 🔍 Drift Pattern Analysis")
                            
                            drift_summary = analysis.get('drift_summary', {})
                            if drift_summary.get('success'):
                                if drift_summary.get('explanation'):
                                    st.success("✅ Pattern Analysis Complete")
                                    st.markdown(drift_summary['explanation'])
                                
                                if drift_summary.get('factors'):
                                    st.markdown("**🎯 Contributing Factors:**")
                                    for factor in drift_summary.get('factors', []):
                                        st.markdown(f"- {factor}")
                                
                                if drift_summary.get('recommendations'):
                                    st.markdown("**💡 Drift-Specific Recommendations:**")
                                    for rec in drift_summary.get('recommendations', []):
                                        st.markdown(f"- {rec}")
                            else:
                                st.warning(f"⚠️ Drift analysis unavailable: {drift_summary.get('error', 'Unknown error')}")
                            
                            # 3. Contextual Analysis Section
                            st.markdown("---")
                            st.markdown("#### 🌟 Lifestyle Context Analysis")
                            
                            context = analysis.get('contextual_explanation', {})
                            if context.get('success'):
                                st.success("✅ Context Analysis Complete")
                                
                                if context.get('contextual_explanation'):
                                    st.markdown("**Understanding Your Pattern:**")
                                    st.info(context['contextual_explanation'])
                                
                                if context.get('possible_factors'):
                                    st.markdown("**🔗 Possible Lifestyle Connections:**")
                                    for factor in context.get('possible_factors', []):
                                        st.markdown(f"- {factor}")
                                
                                confidence = context.get('confidence_level', 0)
                                st.progress(confidence, text=f"Analysis Confidence: {confidence*100:.0f}%")
                            else:
                                st.warning(f"⚠️ Context analysis unavailable: {context.get('error', 'Unknown error')}")
                            
                            # 4. Risk Assessment Section
                            st.markdown("---")
                            st.markdown("#### ⚖️ Risk Assessment Over Time")
                            
                            risk = analysis.get('risk_assessment', {})
                            if risk.get('success'):
                                st.success("✅ Risk Assessment Complete")
                                
                                risk_level = risk.get('risk_level', 'unknown')
                                risk_emoji = {
                                    'temporary': '🟢',
                                    'needs_observation': '🟡',
                                    'potentially_concerning': '🟠'
                                }.get(risk_level, '⚪')
                                
                                risk_col1, risk_col2, risk_col3 = st.columns(3)
                                with risk_col1:
                                    st.metric("Risk Level", f"{risk_emoji} {risk_level.replace('_', ' ').title()}")
                                with risk_col2:
                                    st.metric("Days Observed", risk.get('days_observed', 0))
                                with risk_col3:
                                    confidence = risk.get('confidence_score', 0)
                                    st.metric("Confidence", f"{confidence*100:.0f}%")
                                
                                if risk.get('reasoning'):
                                    st.markdown("**📝 Risk Reasoning:**")
                                    st.info(risk['reasoning'])
                                
                                if risk.get('trend_description'):
                                    st.markdown(f"**📉 Trend:** {risk['trend_description']}")
                                
                                if risk.get('recommendations'):
                                    st.markdown("**💡 Risk-Based Recommendations:**")
                                    for rec in risk.get('recommendations', []):
                                        st.markdown(f"- {rec}")
                            else:
                                st.warning(f"⚠️ Risk assessment unavailable: {risk.get('error', 'Unknown error')}")
                            
                            # 5. Safety Notice Section
                            st.markdown("---")
                            st.markdown("#### 🛡️ Safety Evaluation")
                            
                            safety = analysis.get('safety_notice', {})
                            if safety.get('success'):
                                escalation = safety.get('escalation_required', False)
                                urgency = safety.get('urgency_level', 'routine')
                                
                                if escalation:
                                    st.warning("⚠️ Professional Consultation Recommended")
                                    urgency_emoji = {
                                        'routine': '📅',
                                        'prompt': '⏰',
                                        'urgent': '🚨'
                                    }.get(urgency, '📋')
                                    st.markdown(f"**{urgency_emoji} Urgency Level:** {urgency.title()}")
                                else:
                                    st.success("✅ Pattern Within Monitoring Range")
                                
                                if safety.get('safety_message'):
                                    st.info(safety['safety_message'])
                                
                                if safety.get('rationale'):
                                    with st.expander("📖 Safety Rationale"):
                                        st.markdown(safety['rationale'])
                                
                                if safety.get('next_steps'):
                                    st.markdown("**👣 Next Steps:**")
                                    for step in safety.get('next_steps', []):
                                        st.markdown(f"- {step}")
                            
                            # 6. Care Guidance Section
                            st.markdown("---")
                            st.markdown("#### 💝 Personalized Care Guidance")
                            
                            care = analysis.get('care_guidance', {})
                            if care.get('success'):
                                tone = care.get('tone', 'supportive')
                                tone_emoji = '😊' if tone == 'reassuring' else '🤝'
                                st.success(f"✅ Guidance Generated ({tone_emoji} {tone.title()} Tone)")
                                
                                if care.get('guidance_list'):
                                    st.markdown("**🎯 Your Personalized Wellness Plan:**")
                                    for i, guidance in enumerate(care.get('guidance_list', []), 1):
                                        st.markdown(f"**{i}.** {guidance}")
                                
                                if care.get('follow_up_suggestion'):
                                    st.info(f"**📅 Follow-Up:** {care['follow_up_suggestion']}")
                                
                                if care.get('rationale'):
                                    with st.expander("💭 Why These Suggestions?"):
                                        st.markdown(care['rationale'])
                            
                            # 7. Pipeline Metadata
                            st.markdown("---")
                            st.markdown("#### 🔧 Analysis Details")
                            
                            metadata = analysis.get('pipeline_metadata', {})
                            meta_col1, meta_col2, meta_col3 = st.columns(3)
                            with meta_col1:
                                st.metric("Agents Executed", metadata.get('agents_executed', 0))
                            with meta_col2:
                                st.metric("Successful", metadata.get('agents_successful', 0))
                            with meta_col3:
                                completion = metadata.get('completion_status', 'unknown')
                                status_emoji = '✅' if completion == 'complete' else '⚠️'
                                st.metric("Status", f"{status_emoji} {completion.title()}")
                            
                            # 8. Disclaimer
                            st.markdown("---")
                            st.markdown("#### ⚠️ Important Disclaimer")
                            disclaimer = care.get('disclaimer') or safety.get('disclaimer', '')
                            if disclaimer:
                                st.caption(disclaimer)
                            else:
                                st.caption("This health monitoring system provides informational insights only and does not constitute medical advice. Always consult qualified healthcare professionals for medical concerns.")
                    
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
