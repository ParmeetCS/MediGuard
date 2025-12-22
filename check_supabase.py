"""
Check Supabase Auth Logs for Errors
"""
print("""
🔍 MANUAL CHECKS TO DO NOW:

1. DISABLE EMAIL CONFIRMATION (Quickest fix!)
   https://app.supabase.com/project/hqdrdatcbwhunswiiuuw/auth/providers
   → Turn OFF "Confirm email"
   → Click Save
   → Test signup immediately

2. CHECK AUTH LOGS
   https://app.supabase.com/project/hqdrdatcbwhunswiiuuw/logs/auth-logs
   → Look for signup events
   → Check for rate limit errors
   → Look for email delivery failures

3. CHECK USERS TABLE
   https://app.supabase.com/project/hqdrdatcbwhunswiiuuw/auth/users
   → Are users being created?
   → Check "Confirmed At" column

4. VERIFY REDIRECT URLS
   https://app.supabase.com/project/hqdrdatcbwhunswiiuuw/auth/url-configuration
   → Must have: https://mediguard-feb6sybhmnworzdxmyngid.streamlit.app/**
   → (with ** at the end!)
   → Must have: http://localhost:8501/**

5. CHECK SITE URL
   → Must be: https://mediguard-feb6sybhmnworzdxmyngid.streamlit.app
   → (NO trailing slash!)

═════════════════════════════════════════════════════════

RECOMMENDED ACTION:
Disable email confirmation temporarily (#1 above).
This proves signup works and isolates the email issue.

═════════════════════════════════════════════════════════
""")
