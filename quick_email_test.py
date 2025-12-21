"""
Quick Email Test - Check Supabase Settings
"""

from auth.supabase_auth import supabase, get_redirect_url
import sys

print("\n🔍 CHECKING SUPABASE EMAIL CONFIGURATION\n")

# Test with a proper Gmail format
test_email = "testuser12345@gmail.com"
test_password = "SecurePass123!"
redirect_url = get_redirect_url()

print(f"Test Email: {test_email}")
print(f"Redirect URL: {redirect_url}")
print(f"\nAttempting signup...\n")

try:
    response = supabase.auth.sign_up({
        "email": test_email,
        "password": test_password,
        "options": {
            "email_redirect_to": redirect_url
        }
    })
    
    if response.user:
        print("✅ SUCCESS! User created:")
        print(f"   - Email: {response.user.email}")
        print(f"   - ID: {response.user.id}")
        
        if response.session:
            print(f"   - Session: Active (no email confirmation needed)")
        else:
            print(f"   - Session: None (email confirmation required)")
            print(f"\n📧 CHECK YOUR EMAIL: {test_email}")
            print(f"   Look in inbox AND spam folder!")
            
    else:
        print("⚠️  User object is None - check Supabase settings")
        
except Exception as e:
    error = str(e)
    print(f"❌ ERROR: {error}\n")
    
    if "invalid" in error.lower():
        print("💡 POSSIBLE CAUSES:")
        print("   1. Supabase has email domain restrictions")
        print("   2. Check Auth → Providers → Email settings")
        print("   3. Verify 'Allow disposable email addresses' setting")
        
    elif "rate" in error.lower() or "limit" in error.lower():
        print("⚠️  RATE LIMIT EXCEEDED!")
        print("   Free tier: 3 emails per hour")
        print("   Solutions:")
        print("   - Wait 1 hour")
        print("   - Disable email confirmation temporarily")
        print("   - Upgrade to custom SMTP")
        
    elif "already" in error.lower():
        print("✅ Email already registered (normal for testing)")
        print("   Try a different email or check users in dashboard")
    
    print(f"\n🔗 Check Supabase Dashboard:")
    print(f"   Auth Logs: https://app.supabase.com/project/hqdrdatcbwhunswiiuuw/logs/auth-logs")
    print(f"   Users: https://app.supabase.com/project/hqdrdatcbwhunswiiuuw/auth/users")
    print(f"   Settings: https://app.supabase.com/project/hqdrdatcbwhunswiiuuw/auth/providers")

print("\n" + "="*70)
print("\n📝 IMPORTANT: Have you DEPLOYED the updated code to Streamlit yet?")
print("\nThe local code works, but your DEPLOYED app still has the old code!")
print("\nTO FIX:")
print("1. Push code to GitHub: git add . && git commit -m 'Fix email' && git push")
print("2. Streamlit will auto-deploy (or click Reboot)")
print("3. THEN test signup on deployed app")
print("\n" + "="*70 + "\n")
