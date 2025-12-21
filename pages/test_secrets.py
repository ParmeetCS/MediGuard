"""
Test Streamlit Secrets Configuration
Run this to verify secrets are loaded correctly when deployed
"""

import streamlit as st
import os

st.title("🔐 Streamlit Secrets Configuration Test")

st.markdown("---")

# Check if secrets are available
st.subheader("1. Secrets Availability")
if hasattr(st, 'secrets'):
    st.success("✅ Streamlit secrets are available!")
    
    # List all available secrets (without showing values)
    try:
        secret_keys = list(st.secrets.keys())
        st.info(f"Found {len(secret_keys)} secrets configured")
        
        st.write("**Configured secrets:**")
        for key in secret_keys:
            st.write(f"- {key}")
    except Exception as e:
        st.warning(f"Could not list secrets: {e}")
else:
    st.error("❌ Streamlit secrets not available (might be running locally)")

st.markdown("---")

# Test each required secret
st.subheader("2. Required Secrets Check")

required_secrets = [
    "SUPABASE_URL",
    "SUPABASE_ANON_KEY", 
    "GOOGLE_API_KEY",
    "STREAMLIT_APP_URL"
]

for secret_name in required_secrets:
    try:
        # Try to get from secrets
        if hasattr(st, 'secrets') and secret_name in st.secrets:
            value = st.secrets[secret_name]
            # Mask the value
            masked = value[:20] + "..." if len(value) > 20 else value
            st.success(f"✅ {secret_name}: {masked}")
        # Fall back to environment
        elif os.getenv(secret_name):
            value = os.getenv(secret_name)
            masked = value[:20] + "..." if len(value) > 20 else value
            st.info(f"ℹ️ {secret_name} (from .env): {masked}")
        else:
            st.error(f"❌ {secret_name}: NOT FOUND")
    except Exception as e:
        st.error(f"❌ {secret_name}: Error - {str(e)}")

st.markdown("---")

# Test authentication module
st.subheader("3. Authentication Module Test")

try:
    from auth.supabase_auth import get_env_var, SUPABASE_URL, SUPABASE_ANON_KEY, get_redirect_url
    
    st.success("✅ Authentication module imported successfully")
    
    # Test get_env_var function
    test_url = get_env_var("SUPABASE_URL")
    st.write(f"**SUPABASE_URL via get_env_var():** {test_url[:30]}..." if test_url else "❌ Not found")
    
    # Test global variables
    st.write(f"**Global SUPABASE_URL:** {SUPABASE_URL[:30]}..." if SUPABASE_URL else "❌ Not found")
    
    # Test redirect URL
    redirect = get_redirect_url()
    st.write(f"**Redirect URL:** {redirect}")
    
    if "streamlit.app" in redirect:
        st.success("✅ Using deployed URL")
    elif "localhost" in redirect:
        st.info("ℹ️ Using localhost (local development)")
    else:
        st.warning("⚠️ Unexpected redirect URL")
        
except Exception as e:
    st.error(f"❌ Error importing auth module: {str(e)}")

st.markdown("---")

# Test ADK runtime
st.subheader("4. ADK Runtime Test")

try:
    from agents.adk_runtime import GOOGLE_API_KEY, get_env_var
    
    st.success("✅ ADK runtime module imported successfully")
    
    # Test API key
    if GOOGLE_API_KEY:
        masked_key = GOOGLE_API_KEY[:20] + "..." if len(GOOGLE_API_KEY) > 20 else GOOGLE_API_KEY
        st.write(f"**Google API Key:** {masked_key}")
        st.success("✅ Google API key loaded")
    else:
        st.error("❌ Google API key not found")
        
except Exception as e:
    st.error(f"❌ Error importing ADK runtime: {str(e)}")

st.markdown("---")

# Environment detection
st.subheader("5. Environment Detection")

env_vars = {
    "STREAMLIT_SHARING_MODE": os.getenv("STREAMLIT_SHARING_MODE"),
    "STREAMLIT_RUNTIME_ENV": os.getenv("STREAMLIT_RUNTIME_ENV"),
}

st.write("**Environment variables:**")
for key, value in env_vars.items():
    if value:
        st.write(f"- {key}: {value}")
    else:
        st.write(f"- {key}: Not set")

# Determine environment
if any(env_vars.values()):
    st.success("✅ Running on Streamlit Cloud")
else:
    st.info("ℹ️ Running locally")

st.markdown("---")

# Summary
st.subheader("📊 Summary")

col1, col2 = st.columns(2)

with col1:
    st.metric("Secrets Available", "Yes" if hasattr(st, 'secrets') else "No")
    
with col2:
    # Count configured secrets
    configured = 0
    for secret in required_secrets:
        try:
            if (hasattr(st, 'secrets') and secret in st.secrets) or os.getenv(secret):
                configured += 1
        except:
            pass
    
    st.metric("Configured Secrets", f"{configured}/{len(required_secrets)}")

if configured == len(required_secrets):
    st.success("🎉 All secrets configured correctly!")
else:
    st.error(f"⚠️ Missing {len(required_secrets) - configured} secrets")
    st.info("Add missing secrets in Streamlit Cloud → Settings → Secrets")
