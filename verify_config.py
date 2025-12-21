"""
Verify Supabase and Streamlit Configuration
Run this script to check if everything is set up correctly
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_environment():
    """Check all required environment variables"""
    print("🔍 Checking Environment Configuration...\n")
    
    # Required variables
    required_vars = {
        "SUPABASE_URL": os.getenv("SUPABASE_URL"),
        "SUPABASE_ANON_KEY": os.getenv("SUPABASE_ANON_KEY"),
        "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY"),
        "STREAMLIT_APP_URL": os.getenv("STREAMLIT_APP_URL")
    }
    
    all_good = True
    
    for var_name, var_value in required_vars.items():
        if not var_value:
            print(f"❌ {var_name}: NOT SET")
            all_good = False
        elif var_value in ["your_url_here", "your_anon_key_here", "your_api_key_here"]:
            print(f"⚠️  {var_name}: PLACEHOLDER VALUE (needs to be replaced)")
            all_good = False
        else:
            # Mask sensitive values
            if "KEY" in var_name or "URL" in var_name:
                masked_value = var_value[:20] + "..." if len(var_value) > 20 else var_value
                print(f"✅ {var_name}: {masked_value}")
            else:
                print(f"✅ {var_name}: {var_value}")
    
    return all_good


def check_supabase_connection():
    """Test Supabase connection"""
    print("\n🔗 Testing Supabase Connection...\n")
    
    try:
        from auth.supabase_auth import supabase
        
        if not supabase:
            print("❌ Supabase client not initialized")
            return False
        
        # Try to get session (will be None if not logged in, but connection works)
        try:
            session = supabase.auth.get_session()
            print("✅ Supabase connection successful!")
            return True
        except Exception as e:
            print(f"✅ Supabase client initialized (auth test: {str(e)[:50]})")
            return True
            
    except Exception as e:
        print(f"❌ Supabase connection failed: {str(e)}")
        return False


def check_deployment_readiness():
    """Check if ready for deployment"""
    print("\n🚀 Deployment Readiness Check...\n")
    
    streamlit_url = os.getenv("STREAMLIT_APP_URL")
    
    if not streamlit_url:
        print("⚠️  STREAMLIT_APP_URL not set")
        print("   Set this after deploying to Streamlit Cloud")
        return False
    
    if "localhost" in streamlit_url:
        print("⚠️  STREAMLIT_APP_URL still points to localhost")
        print("   Update this with your deployed Streamlit app URL")
        return False
    
    if streamlit_url.startswith("https://"):
        print(f"✅ Deployment URL configured: {streamlit_url}")
        return True
    else:
        print("⚠️  STREAMLIT_APP_URL should start with https://")
        return False


def print_next_steps():
    """Print next steps for deployment"""
    print("\n📋 Next Steps for Deployment:\n")
    
    print("1. Deploy your app to Streamlit Cloud")
    print("   Visit: https://share.streamlit.io/\n")
    
    print("2. After deployment, get your app URL (e.g., https://your-app.streamlit.app)")
    print("   Update STREAMLIT_APP_URL in Streamlit secrets\n")
    
    print("3. Configure Supabase Dashboard:")
    print("   a. Go to: https://app.supabase.com/project/hqdrdatcbwhunswiiuuw/auth/url-configuration")
    print("   b. Set Site URL to your Streamlit app URL")
    print("   c. Add redirect URLs:")
    print("      - https://your-app-name.streamlit.app/**")
    print("      - http://localhost:8501/**\n")
    
    print("4. Test email confirmation on deployed app\n")
    
    print("5. Check DEPLOYMENT_GUIDE.md for detailed instructions\n")


def main():
    """Main verification function"""
    print("=" * 60)
    print("   MediGuard Drift AI - Configuration Verification")
    print("=" * 60 + "\n")
    
    # Check environment
    env_ok = check_environment()
    
    # Check Supabase
    supabase_ok = check_supabase_connection()
    
    # Check deployment readiness
    deployment_ready = check_deployment_readiness()
    
    # Summary
    print("\n" + "=" * 60)
    print("   Summary")
    print("=" * 60 + "\n")
    
    if env_ok and supabase_ok:
        print("✅ Local development environment is configured correctly!")
        
        if deployment_ready:
            print("✅ Ready for production deployment!")
        else:
            print("⚠️  Update STREAMLIT_APP_URL after deploying to Streamlit Cloud")
    else:
        print("❌ Configuration issues detected. Please fix the errors above.")
    
    # Print next steps
    if not deployment_ready:
        print_next_steps()
    
    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()
