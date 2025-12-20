"""
Helper module to fetch both health check data and context data from Supabase
for AI agent analysis
"""

from auth.supabase_auth import get_supabase_client
from datetime import datetime, timedelta
import streamlit as st


def get_user_health_data(user_id: str, days: int = 14) -> dict:
    """
    Fetch comprehensive user health data from Supabase
    
    Args:
        user_id: User's unique ID
        days: Number of days of historical data to fetch
    
    Returns:
        dict with keys:
            - health_checks: list of health check records
            - context_data: user context/lifestyle data
            - profile: user profile data
            - success: bool indicating if data was fetched
    """
    result = {
        'health_checks': [],
        'context_data': {},
        'profile': {},
        'success': False,
        'message': ''
    }
    
    try:
        supabase = get_supabase_client()
        if not supabase:
            result['message'] = "Database not connected"
            return result
        
        # 1. Fetch health check data (from daily health checks)
        try:
            cutoff_date = (datetime.now() - timedelta(days=days)).date().isoformat()
            
            health_response = supabase.table('health_checks')\
                .select('*')\
                .eq('user_id', user_id)\
                .gte('check_date', cutoff_date)\
                .order('check_date', desc=False)\
                .execute()
            
            if health_response.data:
                result['health_checks'] = health_response.data
        except Exception as e:
            result['message'] += f"Health checks error: {str(e)}; "
        
        # 2. Fetch context data (lifestyle, sleep, stress, etc.)
        try:
            context_response = supabase.table('user_context_data')\
                .select('*')\
                .eq('user_id', user_id)\
                .execute()
            
            if context_response.data and len(context_response.data) > 0:
                result['context_data'] = context_response.data[0]
        except Exception as e:
            result['message'] += f"Context data error: {str(e)}; "
        
        # 3. Fetch user profile (age, name, lifestyle)
        try:
            profile_response = supabase.table('user_profiles')\
                .select('*')\
                .eq('user_id', user_id)\
                .execute()
            
            if profile_response.data and len(profile_response.data) > 0:
                result['profile'] = profile_response.data[0]
        except Exception as e:
            result['message'] += f"Profile error: {str(e)}; "
        
        # Check if we got at least health check data
        if result['health_checks']:
            result['success'] = True
            result['message'] = f"Found {len(result['health_checks'])} health checks"
        else:
            result['message'] = "No health check data found. Complete a daily health check first."
        
        return result
        
    except Exception as e:
        result['message'] = f"Error fetching data: {str(e)}"
        return result


def format_data_for_agents(health_data: dict) -> dict:
    """
    Format the fetched data into the structure expected by ADK agents
    
    Args:
        health_data: Output from get_user_health_data()
    
    Returns:
        dict formatted for agents with:
            - health_metrics: time series data
            - context: lifestyle factors
            - profile: user demographics
    """
    formatted = {
        'health_metrics': {},
        'context': {},
        'profile': {},
        'has_data': False
    }
    
    try:
        # Extract health metrics time series
        if health_data['health_checks']:
            formatted['has_data'] = True
            
            # Create time series for key metrics
            dates = []
            metrics = {
                'movement_speed': [],
                'stability': [],
                'sit_stand_movement_speed': [],
                'walk_stability': [],
                'steady_stability': []
            }
            
            for check in health_data['health_checks']:
                dates.append(check.get('check_date'))
                
                # Collect metrics
                for metric_key in metrics.keys():
                    value = check.get(metric_key)
                    if value is not None:
                        metrics[metric_key].append(float(value))
                    else:
                        metrics[metric_key].append(None)
            
            formatted['health_metrics'] = {
                'dates': dates,
                **metrics,
                'records_count': len(dates)
            }
        
        # Extract context/lifestyle data
        if health_data['context_data']:
            context = health_data['context_data']
            formatted['context'] = {
                'sleep_hours': context.get('sleep_hours', 7.0),
                'stress_level': context.get('stress_level', 'medium'),
                'workload': context.get('workload', 'moderate'),
                'activity_level': context.get('activity_level', 'moderate'),
                'medical_summary': context.get('medical_summary', ''),
                'known_conditions': context.get('known_conditions', '')
            }
        
        # Extract profile data
        if health_data['profile']:
            profile = health_data['profile']
            formatted['profile'] = {
                'name': profile.get('name', ''),
                'age': profile.get('age'),
                'lifestyle': profile.get('lifestyle', ''),
                'additional_context': profile.get('additional_context', '')
            }
        
        return formatted
        
    except Exception as e:
        st.error(f"Error formatting data: {str(e)}")
        return formatted
