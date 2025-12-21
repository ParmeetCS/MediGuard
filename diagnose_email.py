"""
Diagnose Supabase Email Configuration Issues
Run this to identify why emails aren't being sent
"""

import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

def check_supabase_auth_settings():
    """Check Supabase authentication settings"""
    print("=" * 70)
    print("  SUPABASE EMAIL DIAGNOSIS")
    print("=" * 70 + "\n")
    
    # Get credentials
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
    STREAMLIT_APP_URL = os.getenv("STREAMLIT_APP_URL")
    
    print("1. ENVIRONMENT VARIABLES CHECK")
    print("-" * 70)
    print(f"✅ SUPABASE_URL: {SUPABASE_URL}")
    print(f"✅ SUPABASE_ANON_KEY: {SUPABASE_ANON_KEY[:30]}...")
    print(f"✅ STREAMLIT_APP_URL: {STREAMLIT_APP_URL}")
    
    # Check for trailing slash
    if STREAMLIT_APP_URL and STREAMLIT_APP_URL.endswith("/"):
        print(f"\n⚠️  WARNING: STREAMLIT_APP_URL has trailing slash")
        print(f"   Remove the trailing '/' from: {STREAMLIT_APP_URL}")
        print(f"   Should be: {STREAMLIT_APP_URL.rstrip('/')}")
    
    print("\n2. SUPABASE CONNECTION TEST")
    print("-" * 70)
    
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        print("✅ Supabase client connected successfully")
        
        # Try to get session (will be None but tests connection)
        session = supabase.auth.get_session()
        print("✅ Auth API is accessible")
        
    except Exception as e:
        print(f"❌ Connection error: {str(e)}")
        return
    
    print("\n3. REQUIRED SUPABASE DASHBOARD SETTINGS")
    print("-" * 70)
    print("Go to: https://app.supabase.com/project/hqdrdatcbwhunswiiuuw/auth/url-configuration")
    print()
    print("CHECK THESE SETTINGS:")
    print()
    print("A. Site URL (WITHOUT trailing slash):")
    print("   ✓ https://mediguard-feb6sybhmnworzdxmyngid.streamlit.app")
    print("   ✗ https://mediguard-feb6sybhmnworzdxmyngid.streamlit.app/  (NO slash!)")
    print()
    print("B. Redirect URLs (WITH /** wildcard):")
    print("   Must have BOTH of these:")
    print("   ✓ https://mediguard-feb6sybhmnworzdxmyngid.streamlit.app/**")
    print("   ✓ http://localhost:8501/**")
    print()
    print("   Click 'Add URL' button to add each one separately!")
    print()
    
    print("4. EMAIL CONFIRMATION SETTINGS")
    print("-" * 70)
    print("Go to: https://app.supabase.com/project/hqdrdatcbwhunswiiuuw/auth/providers")
    print()
    print("CHECK:")
    print("   ✓ Email provider is ENABLED")
    print("   ✓ 'Confirm email' is ENABLED (or disable if you want immediate access)")
    print()
    
    print("5. EMAIL TEMPLATE CHECK")
    print("-" * 70)
    print("Go to: https://app.supabase.com/project/hqdrdatcbwhunswiiuuw/auth/templates")
    print()
    print("CHECK 'Confirm signup' template:")
    print("   ✓ Should contain: {{ .ConfirmationURL }}")
    print("   ✗ Should NOT contain: localhost or hardcoded URLs")
    print()
    
    print("6. EMAIL RATE LIMITS")
    print("-" * 70)
    print("⚠️  Supabase FREE tier: Only 3 emails per hour!")
    print()
    print("If you've tested multiple times:")
    print("   - Wait 1 hour before testing again")
    print("   - OR upgrade to custom SMTP provider")
    print("   - OR temporarily disable email confirmation")
    print()
    
    print("7. QUICK TESTS TO TRY")
    print("-" * 70)
    print()
    print("Test A: Check spam folder")
    print("   - Supabase emails often end up in spam")
    print()
    print("Test B: Try different email provider")
    print("   - Gmail, Outlook, Yahoo - all behave differently")
    print()
    print("Test C: Check Supabase logs")
    print("   - Go to: https://app.supabase.com/project/hqdrdatcbwhunswiiuuw/logs/auth-logs")
    print("   - Look for sign_up events and any errors")
    print()
    print("Test D: Temporarily disable email confirmation")
    print("   - Go to: https://app.supabase.com/project/hqdrdatcbwhunswiiuuw/auth/providers")
    print("   - Turn OFF 'Confirm email'")
    print("   - Users can login immediately (test if other issues exist)")
    print()
    
    print("8. STREAMLIT CLOUD SECRETS")
    print("-" * 70)
    print("If on Streamlit Cloud, add these secrets:")
    print()
    print("SUPABASE_URL = \"https://hqdrdatcbwhunswiiuuw.supabase.co\"")
    print("SUPABASE_ANON_KEY = \"sb_publishable_kZLyTV9kEBwk3jZJtzqryA_agEnY11Y\"")
    print("STREAMLIT_APP_URL = \"https://mediguard-feb6sybhmnworzdxmyngid.streamlit.app\"")
    print("GOOGLE_API_KEY = \"AIzaSyAwnU5k8AWnyZI_IgFHkPzzjhXygHdiQb0\"")
    print()
    print("⚠️  Note: NO trailing slash in STREAMLIT_APP_URL!")
    print()
    
    print("=" * 70)
    print("\nMOST COMMON FIX:")
    print("=" * 70)
    print()
    print("1. Remove trailing slash from Site URL in Supabase")
    print("2. Add redirect URLs WITH /** wildcard (not just /)")
    print("3. Click 'Save changes' button")
    print("4. Wait 1-2 minutes for changes to propagate")
    print("5. Restart your Streamlit app")
    print("6. Test with a NEW email address (not one you've already used)")
    print()
    print("=" * 70 + "\n")


if __name__ == "__main__":
    check_supabase_auth_settings()
