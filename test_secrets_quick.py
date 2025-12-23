"""
Quick Secrets Test - Verify all secrets are accessible
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Load .env for local testing
load_dotenv()

st.title("🔐 Quick Secrets Test")

def get_secret(key):
    """Get secret from st.secrets or environment"""
    try:
        if hasattr(st, 'secrets') and key in st.secrets:
            return st.secrets[key]
    except:
        pass
    return os.getenv(key)

# Test all required secrets
secrets_to_test = [
    "SUPABASE_URL",
    "SUPABASE_ANON_KEY",
    "GOOGLE_API_KEY",
    "STREAMLIT_APP_URL",
    "VISION_API_KEY",
    "VISION_MODEL"
]

st.markdown("### Testing Secrets Access")

all_passed = True
for secret_name in secrets_to_test:
    value = get_secret(secret_name)
    if value:
        # Mask sensitive values
        if len(value) > 30:
            masked = value[:20] + "..." + value[-10:]
        else:
            masked = value[:15] + "..." if len(value) > 15 else value
        
        st.success(f"✅ **{secret_name}**: `{masked}`")
    else:
        st.error(f"❌ **{secret_name}**: NOT FOUND")
        all_passed = False

st.markdown("---")

if all_passed:
    st.balloons()
    st.success("🎉 **ALL SECRETS CONFIGURED CORRECTLY!**")
    
    # Test imports
    st.markdown("### Testing Module Imports")
    
    try:
        from auth.supabase_auth import get_env_var, SUPABASE_URL
        st.success(f"✅ Auth module: SUPABASE_URL = `{SUPABASE_URL[:30]}...`")
    except Exception as e:
        st.error(f"❌ Auth module error: {e}")
    
    try:
        from agents.adk_runtime import GOOGLE_API_KEY, is_adk_ready
        st.success(f"✅ ADK Runtime: API Key = `{GOOGLE_API_KEY[:20]}...`")
        st.info(f"ADK Ready: {is_adk_ready()}")
    except Exception as e:
        st.error(f"❌ ADK Runtime error: {e}")
    
else:
    st.error("⚠️ **SOME SECRETS ARE MISSING!**")
    st.info("Please check your `.streamlit/secrets.toml` file or `.env` file")
