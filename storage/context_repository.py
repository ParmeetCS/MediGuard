"""
Context Repository - MediGuard Drift AI
Data access layer for user context data stored in Supabase
"""

from typing import Optional, Dict, Any
from auth.supabase_auth import get_supabase_client


class ContextRepository:
    """
    Repository for accessing user context data from Supabase
    
    This class provides a clean interface for fetching user health context
    without mixing data access with business logic or AI operations.
    """
    
    def __init__(self):
        """Initialize the context repository"""
        self.supabase = None
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Initialize Supabase client"""
        try:
            self.supabase = get_supabase_client()
        except Exception as e:
            print(f"Warning: Could not initialize Supabase client - {str(e)}")
            self.supabase = None
    
    def fetch_user_context(self, user_id: str) -> Dict[str, Any]:
        """
        Fetch latest context data for a given user
        
        Args:
            user_id (str): Unique user identifier
        
        Returns:
            Dict containing user context data with keys:
                - success (bool): Whether fetch was successful
                - data (dict): User context data (empty dict if not found)
                - error (str): Error message if failed
        
        Example:
            repo = ContextRepository()
            result = repo.fetch_user_context("user-123")
            
            if result['success']:
                context = result['data']
                print(f"Sleep hours: {context.get('sleep_hours', 7)}")
        """
        if not self.supabase:
            return {
                "success": False,
                "data": {},
                "error": "Database connection not configured"
            }
        
        if not user_id:
            return {
                "success": False,
                "data": {},
                "error": "User ID is required"
            }
        
        try:
            # Query user_context_data table
            response = self.supabase.table('user_context_data').select('*').eq('user_id', user_id).execute()
            
            # Check if data was found
            if response.data and len(response.data) > 0:
                context_data = response.data[0]
                
                # Return structured data
                return {
                    "success": True,
                    "data": {
                        "user_id": context_data.get('user_id'),
                        "medical_summary": context_data.get('medical_summary', ''),
                        "known_conditions": context_data.get('known_conditions', ''),
                        "report_summary": context_data.get('report_summary', ''),
                        "sleep_hours": context_data.get('sleep_hours', 7.0),
                        "stress_level": context_data.get('stress_level', 'medium'),
                        "workload": context_data.get('workload', 'moderate'),
                        "activity_level": context_data.get('activity_level', 'moderate'),
                        "created_at": context_data.get('created_at'),
                        "updated_at": context_data.get('updated_at')
                    },
                    "error": None
                }
            else:
                # No data found for this user (not an error, just no data yet)
                return {
                    "success": True,
                    "data": self._get_default_context(),
                    "error": None
                }
        
        except Exception as e:
            return {
                "success": False,
                "data": {},
                "error": f"Database error: {str(e)}"
            }
    
    def user_has_context(self, user_id: str) -> bool:
        """
        Check if user has any context data stored
        
        Args:
            user_id (str): Unique user identifier
        
        Returns:
            bool: True if context exists, False otherwise
        
        Example:
            repo = ContextRepository()
            if repo.user_has_context("user-123"):
                print("User has context data")
        """
        result = self.fetch_user_context(user_id)
        
        if not result['success']:
            return False
        
        # Check if any meaningful data exists (not just defaults)
        data = result['data']
        
        return bool(
            data.get('medical_summary') or
            data.get('known_conditions') or
            data.get('report_summary')
        )
    
    def get_context_summary(self, user_id: str) -> str:
        """
        Get a formatted summary of user context for AI prompts
        
        Args:
            user_id (str): Unique user identifier
        
        Returns:
            str: Formatted context summary for AI consumption
        
        Example:
            repo = ContextRepository()
            summary = repo.get_context_summary("user-123")
            # Use summary in AI prompt
        """
        result = self.fetch_user_context(user_id)
        
        if not result['success']:
            return "No context data available."
        
        data = result['data']
        
        # Build formatted summary
        summary_parts = []
        
        # Basic lifestyle factors
        summary_parts.append(f"Sleep: {data.get('sleep_hours', 7)} hours/night")
        summary_parts.append(f"Stress: {data.get('stress_level', 'medium')}")
        summary_parts.append(f"Workload: {data.get('workload', 'moderate')}")
        summary_parts.append(f"Activity: {data.get('activity_level', 'moderate')}")
        
        # Medical context if available
        if data.get('medical_summary'):
            summary_parts.append(f"Medical history: {data['medical_summary'][:100]}...")
        
        if data.get('known_conditions'):
            summary_parts.append(f"Known conditions: {data['known_conditions'][:100]}...")
        
        return " | ".join(summary_parts)
    
    def _get_default_context(self) -> Dict[str, Any]:
        """
        Get default context values when no data is stored
        
        Returns:
            Dict: Default context values
        """
        return {
            "user_id": None,
            "medical_summary": "",
            "known_conditions": "",
            "report_summary": "",
            "sleep_hours": 7.0,
            "stress_level": "medium",
            "workload": "moderate",
            "activity_level": "moderate",
            "created_at": None,
            "updated_at": None
        }
    
    def is_configured(self) -> bool:
        """
        Check if repository is properly configured
        
        Returns:
            bool: True if Supabase client is ready
        """
        return self.supabase is not None


# ========================================
# CONVENIENCE FUNCTIONS
# ========================================

def get_user_context(user_id: str) -> Dict[str, Any]:
    """
    Convenience function to fetch user context
    
    Args:
        user_id (str): User identifier
    
    Returns:
        Dict: Context data result
    
    Example:
        from storage.context_repository import get_user_context
        
        context = get_user_context("user-123")
        if context['success']:
            print(context['data'])
    """
    repo = ContextRepository()
    return repo.fetch_user_context(user_id)


def get_context_for_ai(user_id: str) -> str:
    """
    Get formatted context summary for AI prompts
    
    Args:
        user_id (str): User identifier
    
    Returns:
        str: Formatted context summary
    
    Example:
        from storage.context_repository import get_context_for_ai
        
        context_summary = get_context_for_ai("user-123")
        prompt = f"User context: {context_summary}\n\nAnalyze their health drift..."
    """
    repo = ContextRepository()
    return repo.get_context_summary(user_id)


def has_context_data(user_id: str) -> bool:
    """
    Check if user has stored context data
    
    Args:
        user_id (str): User identifier
    
    Returns:
        bool: True if context exists
    """
    repo = ContextRepository()
    return repo.user_has_context(user_id)
