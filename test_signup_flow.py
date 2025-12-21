"""
Test Supabase Signup with Email Confirmation
This simulates what happens when a user signs up
"""

from auth.supabase_auth import sign_up, get_redirect_url, supabase, SUPABASE_URL, SUPABASE_ANON_KEY
import json

print("=" * 70)
print("  SUPABASE SIGNUP TEST")
print("=" * 70)
print()

# Check configuration
print("1. CONFIGURATION CHECK")
print("-" * 70)
print(f"Supabase URL: {SUPABASE_URL}")
print(f"Supabase Key: {SUPABASE_ANON_KEY[:30]}..." if SUPABASE_ANON_KEY else "NOT FOUND")
print(f"Redirect URL: {get_redirect_url()}")
print()

if not supabase:
    print("❌ ERROR: Supabase client not initialized!")
    print("   Check your credentials in .env or Streamlit secrets")
    exit(1)

print("✅ Supabase client initialized")
print()

# Test signup function
print("2. TESTING SIGNUP FUNCTION")
print("-" * 70)

test_email = "test_" + str(hash("test"))[:6] + "@example.com"
test_password = "TestPassword123!"

print(f"Test email: {test_email}")
print(f"Test password: {test_password}")
print()

print("Attempting signup with redirect URL...")
redirect_url = get_redirect_url()
print(f"Using redirect: {redirect_url}")
print()

# Call sign_up
success, message, user_data = sign_up(test_email, test_password, redirect_url)

print("RESULT:")
print(f"  Success: {success}")
print(f"  Message: {message}")
if user_data:
    print(f"  User ID: {user_data.get('id', 'N/A')}")
    print(f"  Email: {user_data.get('email', 'N/A')}")
print()

# Direct test with Supabase client
print("3. DIRECT SUPABASE API TEST")
print("-" * 70)

test_email2 = "direct_test_" + str(hash("direct"))[:6] + "@example.com"

print(f"Testing direct API call with: {test_email2}")
print()

try:
    # Direct API call
    response = supabase.auth.sign_up({
        "email": test_email2,
        "password": test_password,
        "options": {
            "email_redirect_to": redirect_url
        }
    })
    
    print("✅ Direct API call successful!")
    print(f"   User created: {response.user.email if response.user else 'No user returned'}")
    print(f"   Session: {'Yes' if response.session else 'No (email confirmation required)'}")
    print()
    
    # Check the response object
    if hasattr(response, 'user') and response.user:
        print("   User details:")
        print(f"   - ID: {response.user.id}")
        print(f"   - Email: {response.user.email}")
        print(f"   - Confirmed: {getattr(response.user, 'confirmed_at', 'Not confirmed')}")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    print()
    
    # Check if it's a rate limit or already exists error
    error_str = str(e).lower()
    if "rate" in error_str or "limit" in error_str:
        print("⚠️  RATE LIMIT HIT!")
        print("   Supabase free tier: 3 emails per hour")
        print("   Wait 1 hour or disable email confirmation")
    elif "already" in error_str:
        print("⚠️  Email already registered")
        print("   This is normal if testing multiple times")

print()
print("4. WHAT TO CHECK IN SUPABASE DASHBOARD")
print("-" * 70)
print()
print("A. Check Auth Logs:")
print("   https://app.supabase.com/project/hqdrdatcbwhunswiiuuw/logs/auth-logs")
print("   - Look for sign_up events")
print("   - Check for error messages")
print()
print("B. Check Users Table:")
print("   https://app.supabase.com/project/hqdrdatcbwhunswiiuuw/auth/users")
print("   - See if test users were created")
print("   - Check 'Confirmed At' column (should be empty if email not confirmed)")
print()
print("C. Check Email Provider:")
print("   https://app.supabase.com/project/hqdrdatcbwhunswiiuuw/auth/providers")
print("   - Verify 'Email' is enabled")
print("   - Check 'Confirm email' setting")
print()
print("D. Check Rate Limits:")
print("   https://app.supabase.com/project/hqdrdatcbwhunswiiuuw/settings/billing")
print("   - Free tier: 3 emails/hour")
print("   - You may have hit the limit from testing")
print()

print("=" * 70)
print()
print("RECOMMENDED ACTIONS:")
print()
print("1. Check Supabase auth logs (link above)")
print("2. Look for error messages or rate limit warnings")
print("3. Try disabling email confirmation temporarily:")
print("   - Go to Auth → Providers")
print("   - Turn OFF 'Confirm email'")
print("   - Test signup again")
print("   - This will prove if the issue is email-specific")
print()
print("4. If still failing, check:")
print("   - Site URL in Supabase (no trailing slash)")
print("   - Redirect URLs have /** wildcard")
print("   - Email templates don't have hardcoded URLs")
print()
print("=" * 70)
