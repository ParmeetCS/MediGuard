"""
Supabase Authentication Module
Handles user authentication for MediGuard Drift AI
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import Dict, Tuple

# ========================================
# LOAD ENVIRONMENT VARIABLES
# ========================================
# Load environment variables from .env file
load_dotenv()

# Get Supabase credentials from environment
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# ========================================
# INITIALIZE SUPABASE CLIENT
# ========================================
def get_supabase_client() -> Client:
    """
    Initialize and return Supabase client
    
    Returns:
        Client: Configured Supabase client instance
    
    Raises:
        ValueError: If environment variables are not set
    """
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        raise ValueError(
            "Missing Supabase credentials. Please set SUPABASE_URL and "
            "SUPABASE_ANON_KEY in your .env file."
        )
    
    if SUPABASE_URL == "your_url_here" or SUPABASE_ANON_KEY == "your_anon_key_here":
        raise ValueError(
            "Please replace placeholder values in .env with your actual "
            "Supabase credentials."
        )
    
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)


# Create a global client instance
try:
    supabase: Client = get_supabase_client()
except ValueError as e:
    # Client will be None if credentials are not properly configured
    supabase = None
    print(f"Warning: Supabase client not initialized - {str(e)}")


# ========================================
# AUTHENTICATION FUNCTIONS
# ========================================

def sign_up(email: str, password: str) -> Tuple[bool, str, Dict]:
    """
    Register a new user with email and password
    
    Args:
        email (str): User's email address
        password (str): User's password (minimum 6 characters recommended)
    
    Returns:
        Tuple[bool, str, Dict]: 
            - Success status (True/False)
            - Message describing the result
            - User data dictionary (empty if failed)
    
    Example:
        success, message, user_data = sign_up("user@example.com", "password123")
        if success:
            print(f"Welcome! {message}")
        else:
            print(f"Error: {message}")
    """
    if not supabase:
        return False, "Authentication service not configured. Please check your .env file.", {}
    
    # Validate input
    if not email or not password:
        return False, "Email and password are required.", {}
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters long.", {}
    
    if "@" not in email:
        return False, "Please enter a valid email address.", {}
    
    try:
        # Attempt to sign up the user
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        
        # Check if sign up was successful
        if response.user:
            user_data = {
                "id": response.user.id,
                "email": response.user.email,
                "created_at": response.user.created_at
            }
            return True, "Account created successfully! Please check your email for verification.", user_data
        else:
            return False, "Sign up failed. Please try again.", {}
    
    except Exception as e:
        # Handle specific error cases
        error_message = str(e)
        
        if "already registered" in error_message.lower():
            return False, "This email is already registered. Please sign in instead.", {}
        elif "invalid email" in error_message.lower():
            return False, "Invalid email format. Please check and try again.", {}
        elif "weak password" in error_message.lower():
            return False, "Password is too weak. Use a stronger password.", {}
        else:
            return False, f"Sign up error: {error_message}", {}


def sign_in(email: str, password: str) -> Tuple[bool, str, Dict]:
    """
    Sign in an existing user with email and password
    
    Args:
        email (str): User's registered email address
        password (str): User's password
    
    Returns:
        Tuple[bool, str, Dict]: 
            - Success status (True/False)
            - Message describing the result
            - User data and session info (empty if failed)
    
    Example:
        success, message, session_data = sign_in("user@example.com", "password123")
        if success:
            print(f"Logged in: {session_data['email']}")
        else:
            print(f"Error: {message}")
    """
    if not supabase:
        return False, "Authentication service not configured. Please check your .env file.", {}
    
    # Validate input
    if not email or not password:
        return False, "Email and password are required.", {}
    
    try:
        # Attempt to sign in the user
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        # Check if sign in was successful
        if response.user and response.session:
            session_data = {
                "user_id": response.user.id,
                "email": response.user.email,
                "access_token": response.session.access_token,
                "refresh_token": response.session.refresh_token,
                "expires_at": response.session.expires_at
            }
            return True, f"Welcome back, {response.user.email}!", session_data
        else:
            return False, "Sign in failed. Please check your credentials.", {}
    
    except Exception as e:
        # Handle specific error cases
        error_message = str(e)
        
        if "invalid credentials" in error_message.lower() or "invalid login" in error_message.lower():
            return False, "Invalid email or password. Please try again.", {}
        elif "email not confirmed" in error_message.lower():
            return False, "Please verify your email before signing in.", {}
        elif "too many requests" in error_message.lower():
            return False, "Too many login attempts. Please try again later.", {}
        else:
            return False, f"Sign in error: {error_message}", {}


def sign_out() -> Tuple[bool, str]:
    """
    Sign out the currently authenticated user
    
    Returns:
        Tuple[bool, str]: 
            - Success status (True/False)
            - Message describing the result
    
    Example:
        success, message = sign_out()
        if success:
            print("Logged out successfully")
        else:
            print(f"Error: {message}")
    """
    if not supabase:
        return False, "Authentication service not configured. Please check your .env file."
    
    try:
        # Attempt to sign out the user
        supabase.auth.sign_out()
        return True, "Signed out successfully."
    
    except Exception as e:
        error_message = str(e)
        return False, f"Sign out error: {error_message}"


def get_current_user() -> Tuple[bool, Dict]:
    """
    Get the currently authenticated user's information
    
    Returns:
        Tuple[bool, Dict]: 
            - Success status (True if user is authenticated, False otherwise)
            - User data dictionary (empty if not authenticated)
    
    Example:
        is_authenticated, user_data = get_current_user()
        if is_authenticated:
            print(f"Current user: {user_data['email']}")
        else:
            print("No user is signed in")
    """
    if not supabase:
        return False, {}
    
    try:
        # Get the current session
        session = supabase.auth.get_session()
        
        if session and session.user:
            user_data = {
                "user_id": session.user.id,
                "email": session.user.email,
                "created_at": session.user.created_at
            }
            return True, user_data
        else:
            return False, {}
    
    except Exception as e:
        return False, {}


# ========================================
# UTILITY FUNCTIONS
# ========================================

def is_configured() -> bool:
    """
    Check if Supabase authentication is properly configured
    
    Returns:
        bool: True if configured, False otherwise
    """
    return supabase is not None


def reset_password(email: str) -> Tuple[bool, str]:
    """
    Send a password reset email to the user
    
    Args:
        email (str): User's registered email address
    
    Returns:
        Tuple[bool, str]: 
            - Success status (True/False)
            - Message describing the result
    
    Example:
        success, message = reset_password("user@example.com")
        print(message)
    """
    if not supabase:
        return False, "Authentication service not configured. Please check your .env file."
    
    if not email or "@" not in email:
        return False, "Please enter a valid email address."
    
    try:
        # Send password reset email
        supabase.auth.reset_password_for_email(email)
        return True, "Password reset email sent. Please check your inbox."
    
    except Exception as e:
        error_message = str(e)
        return False, f"Password reset error: {error_message}"
