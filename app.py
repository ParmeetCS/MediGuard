"""
MediGuard Drift AI - Daily Health Drift Monitoring System
Entry point for the Streamlit application
"""

import streamlit as st
from auth.supabase_auth import sign_in, sign_up, sign_out, is_configured, get_redirect_url

# ========================================
# PAGE CONFIGURATION
# ========================================
st.set_page_config(
    page_title="MediGuard Drift AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide Streamlit's default page navigation
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# ========================================
# AUTHENTICATION GATE (HARD GATE)
# ========================================
# Initialize authentication state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

# Check if user is authenticated
if not st.session_state.authenticated:
    # ========================================
    # LOGIN/SIGNUP PAGE (BLOCKING ALL OTHER CONTENT)
    # ========================================
    
    # Hide sidebar when not authenticated
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Display login page
    st.markdown("""
        <div style='text-align: center; padding: 3rem 0 2rem 0;'>
            <h1 style='color: #4A90E2; font-size: 3rem;'>🏥 MediGuard Drift AI</h1>
            <p style='font-size: 1.3rem; color: #666; margin-top: 1rem;'>
                Daily Health Drift Monitoring System
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Check if Supabase is configured
    if not is_configured():
        st.error("""
        🔧 **Authentication Not Configured**
        
        Please configure your Supabase credentials in the `.env` file to enable authentication.
        
        1. Create a Supabase project at https://supabase.com
        2. Update `.env` with your project URL and anon key
        3. Restart the application
        """)
        st.stop()
    
    # Create tabs for Login and Sign Up
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Create Account"])
    
    # ========================================
    # LOGIN TAB
    # ========================================
    with tab1:
        st.markdown("### Welcome Back!")
        st.markdown("Sign in to access your health monitoring dashboard.")
        
        with st.form("login_form", clear_on_submit=False):
            email_login = st.text_input(
                "Email Address",
                placeholder="your.email@example.com",
                key="email_login"
            )
            password_login = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="password_login"
            )
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                login_button = st.form_submit_button("🔓 Login", use_container_width=True, type="primary")
            
            if login_button:
                if not email_login or not password_login:
                    st.error("❌ Please enter both email and password.")
                else:
                    with st.spinner("Authenticating..."):
                        success, message, session_data = sign_in(email_login, password_login)
                        
                        if success:
                            # Set authentication state
                            st.session_state.authenticated = True
                            st.session_state.user_email = session_data.get('email')
                            st.session_state.user_id = session_data.get('user_id')
                            
                            st.success(f"✅ {message}")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    # ========================================
    # SIGN UP TAB
    # ========================================
    with tab2:
        st.markdown("### Create Your Account")
        st.markdown("Start monitoring your health drift today!")
        
        with st.form("signup_form", clear_on_submit=True):
            email_signup = st.text_input(
                "Email Address",
                placeholder="your.email@example.com",
                key="email_signup"
            )
            password_signup = st.text_input(
                "Password",
                type="password",
                placeholder="Minimum 6 characters",
                key="password_signup",
                help="Choose a strong password with at least 6 characters"
            )
            password_confirm = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Re-enter your password",
                key="password_confirm"
            )
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                signup_button = st.form_submit_button("📝 Create Account", use_container_width=True, type="primary")
            
            if signup_button:
                if not email_signup or not password_signup or not password_confirm:
                    st.error("❌ Please fill in all fields.")
                elif password_signup != password_confirm:
                    st.error("❌ Passwords do not match. Please try again.")
                elif len(password_signup) < 6:
                    st.error("❌ Password must be at least 6 characters long.")
                else:
                    with st.spinner("Creating your account..."):
                        # Get the appropriate redirect URL for email confirmation
                        redirect_url = get_redirect_url()
                        success, message, user_data = sign_up(email_signup, password_signup, redirect_url)
                        
                        if success:
                            st.success(f"✅ {message}")
                            st.info("🔑 You can now login using your credentials in the Login tab.")
                        else:
                            st.error(f"❌ {message}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.warning("""
        📧 **Email Verification:** Depending on your Supabase settings, you may need to verify 
        your email before you can log in. Check your inbox for a verification link.
        """)
    
    # ========================================
    # INFORMATION SECTION
    # ========================================
    st.markdown("---")
    st.markdown("### 🔒 Secure Authentication")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🛡️ Privacy First**
        
        Your health data is personal. We use enterprise-grade authentication 
        to keep your information secure.
        """)
    
    with col2:
        st.markdown("""
        **🔐 Encrypted Storage**
        
        All data is encrypted at rest and in transit using industry-standard 
        security protocols.
        """)
    
    with col3:
        st.markdown("""
        **👤 Your Data, Your Control**
        
        You own your health data. Access it anytime, export it, or delete 
        it whenever you want.
        """)
    
    # Stop execution here - don't render any other content
    st.stop()

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
# USER IS AUTHENTICATED - SHOW MAIN APP
# ========================================

# Display user info in sidebar header
with st.sidebar:
    st.markdown(f"""
        <div style='background: #E3F2FD; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
            <p style='margin: 0; font-size: 0.9rem; color: #666;'>Logged in as:</p>
            <p style='margin: 0.3rem 0 0 0; font-weight: bold; color: #4A90E2;'>
                {st.session_state.user_email}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Logout button
    if st.button("🚪 Logout", use_container_width=True):
        # Clear authentication state
        st.session_state.authenticated = False
        st.session_state.user_email = None
        st.session_state.user_id = None
        st.session_state.current_page = 'Home'
        
        # Sign out from Supabase
        sign_out()
        
        st.success("Logged out successfully!")
        st.rerun()
    
    st.markdown("---")

# ========================================
# SIDEBAR NAVIGATION
# ========================================
with st.sidebar:
    st.markdown("### 🏥 MediGuard Drift AI")
    st.markdown("---")
    
    # Navigation menu options
    menu_options = {
        "🏠 Home": "Home",
        "👤 Profile": "Profile",
        "📝 Health Context": "Health Context",
        "🩺 Daily Health Check": "Daily Health Check",
        "📊 Dashboard": "Dashboard",
        "💬 AI Health Chat": "AI Health Chat",
        "📖 Guide": "Guide"
    }
    
    # Create navigation buttons with highlighting
    for label, page_name in menu_options.items():
        is_current = st.session_state.current_page == page_name
        button_type = "primary" if is_current else "secondary"
        
        if st.button(label, key=page_name, use_container_width=True, type=button_type):
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
    st.markdown("**Version:** 2.0.0")
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
    
    elif current_page == "Health Context":
        from pages import context_inputs
        context_inputs.show()
    
    elif current_page == "Daily Health Check":
        from pages import daily_health_check
        daily_health_check.show()
    
    elif current_page == "Dashboard":
        from pages import dashboard
        dashboard.show()
    
    elif current_page == "AI Health Chat":
        from pages import ai_health_chat
        ai_health_chat.show()
    
    elif current_page == "Guide":
        from pages import guide
        guide.show()

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
