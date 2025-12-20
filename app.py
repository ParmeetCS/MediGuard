"""
MediGuard Drift AI - Daily Health Drift Monitoring System
Entry point for the Streamlit application
"""

import streamlit as st

# ========================================
# PAGE CONFIGURATION
# ========================================
st.set_page_config(
    page_title="MediGuard Drift AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================
# CUSTOM CSS FOR HEALTHCARE THEME
# ========================================
st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --primary-color: #4A90E2;
        --secondary-color: #50C878;
        --background-color: #F8FAFB;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #4A90E2 0%, #50C878 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        color: #E8F4F8;
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: #F8FAFB;
    }
    
    /* Navigation buttons */
    div[data-testid="stSidebar"] > div:first-child {
        background-color: #F0F7FF;
    }
    
    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# ========================================
# SESSION STATE INITIALIZATION
# ========================================
# Initialize session state for page routing if not already set
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Home'

# ========================================
# HEADER SECTION
# ========================================
st.markdown("""
    <div class="main-header">
        <h1>🏥 MediGuard Drift AI</h1>
        <p>Daily Health Drift Monitoring System - Your Personal Health Guardian</p>
    </div>
""", unsafe_allow_html=True)

# ========================================
# SIDEBAR NAVIGATION
# ========================================
with st.sidebar:
    st.markdown("### 🧭 Navigation")
    st.markdown("---")
    
    # Navigation menu options
    menu_options = {
        "🏠 Home": "Home",
        "👤 Profile": "Profile",
        "📋 Daily Health Check": "Daily Health Check",
        "📊 Dashboard": "Dashboard",
        "💬 AI Health Chat": "AI Health Chat"
    }
    
    # Create navigation buttons
    for label, page_name in menu_options.items():
        if st.button(label, key=page_name, use_container_width=True):
            st.session_state.current_page = page_name
            st.rerun()
    
    st.markdown("---")
    
    # Additional sidebar information
    st.markdown("### ℹ️ About")
    st.info("""
        **MediGuard Drift AI** monitors your daily health metrics 
        and detects subtle changes that may indicate health drift.
    """)
    
    st.markdown("---")
    st.markdown("**Version:** 1.0.0")
    st.markdown("**© 2025 MediGuard**")

# ========================================
# PAGE ROUTING LOGIC
# ========================================
# Route to the appropriate page based on session state
current_page = st.session_state.current_page

try:
    # Import and load the selected page from the pages folder
    if current_page == "Home":
        from pages import home
        home.show()
    
    elif current_page == "Profile":
        from pages import profile
        profile.show()
    
    elif current_page == "Daily Health Check":
        from pages import daily_check
        daily_check.show()
    
    elif current_page == "Dashboard":
        from pages import dashboard
        dashboard.show()
    
    elif current_page == "AI Health Chat":
        from pages import chat_agent
        chat_agent.show()
    
except ImportError as e:
    # Handle missing page modules gracefully
    st.error(f"⚠️ Page '{current_page}' is not yet implemented.")
    st.info("""
        **Developer Note:** Please create the following structure:
        ```
        pages/
        ├── __init__.py
        ├── home.py
        ├── profile.py
        ├── daily_health_check.py
        ├── dashboard.py
        └── ai_health_chat.py
        ```
        Each page module should have a `show()` function.
    """)
    st.exception(e)

# ========================================
# FOOTER
# ========================================
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>🏥 MediGuard Drift AI - Protecting Your Health, One Day at a Time</p>
        <p style='font-size: 0.8rem;'>For medical emergencies, please call your local emergency services immediately.</p>
    </div>
""", unsafe_allow_html=True)
