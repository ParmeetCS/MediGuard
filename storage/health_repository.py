"""
Health Data Repository - MediGuard Drift AI
Functions for storing and retrieving health check data from Supabase
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, date, timedelta
from auth.supabase_auth import get_supabase_client


def save_health_check(user_id: str, health_data: Dict[str, float], check_date: Optional[date] = None) -> Dict[str, Any]:
    """
    Save health check data to Supabase
    
    Args:
        user_id (str): User's unique ID
        health_data (dict): Dictionary containing health metrics
        check_date (date): Date of check (defaults to today)
    
    Returns:
        dict: {'success': bool, 'message': str, 'data': dict}
    """
    try:
        supabase = get_supabase_client()
        
        if not supabase:
            return {
                'success': False,
                'message': 'Database connection not configured',
                'data': None
            }
        
        # Prepare data for insertion
        data = {
            'user_id': user_id,
            'check_date': check_date.isoformat() if check_date else date.today().isoformat(),
            'sit_stand_speed': health_data.get('sit_stand_speed'),
            'sit_stand_stability': health_data.get('sit_stand_stability'),
            'walk_speed': health_data.get('walk_speed'),
            'walk_stability': health_data.get('walk_stability'),
            'gait_symmetry': health_data.get('gait_symmetry'),
            'hand_steadiness': health_data.get('hand_steadiness'),
            'tremor_index': health_data.get('tremor_index'),
            'coordination_score': health_data.get('coordination_score'),
            'overall_mobility': health_data.get('overall_mobility')
        }
        
        # Upsert data (insert or update if exists for this user+date)
        response = supabase.table('health_checks').upsert(data, on_conflict='user_id,check_date').execute()
        
        return {
            'success': True,
            'message': 'Health check saved successfully',
            'data': response.data[0] if response.data else data
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Error saving health check: {str(e)}',
            'data': None
        }


def get_latest_health_check(user_id: str) -> Dict[str, Any]:
    """
    Get the most recent health check for a user
    
    Args:
        user_id (str): User's unique ID
    
    Returns:
        dict: {'success': bool, 'data': dict, 'message': str}
    """
    try:
        supabase = get_supabase_client()
        
        if not supabase:
            return {
                'success': False,
                'data': None,
                'message': 'Database connection not configured'
            }
        
        response = supabase.table('health_checks')\
            .select('*')\
            .eq('user_id', user_id)\
            .order('check_date', desc=True)\
            .limit(1)\
            .execute()
        
        if response.data and len(response.data) > 0:
            return {
                'success': True,
                'data': response.data[0],
                'message': 'Latest health check retrieved'
            }
        else:
            return {
                'success': False,
                'data': None,
                'message': 'No health checks found for this user'
            }
        
    except Exception as e:
        return {
            'success': False,
            'data': None,
            'message': f'Error retrieving health check: {str(e)}'
        }


def get_health_check_history(user_id: str, days: int = 14) -> Dict[str, Any]:
    """
    Get health check history for specified number of days
    
    Args:
        user_id (str): User's unique ID
        days (int): Number of days to retrieve (default 14)
    
    Returns:
        dict: {'success': bool, 'data': list, 'message': str}
    """
    try:
        supabase = get_supabase_client()
        
        if not supabase:
            return {
                'success': False,
                'data': [],
                'message': 'Database connection not configured'
            }
        
        # Calculate cutoff date
        cutoff_date = (date.today() - timedelta(days=days)).isoformat()
        
        response = supabase.table('health_checks')\
            .select('*')\
            .eq('user_id', user_id)\
            .gte('check_date', cutoff_date)\
            .order('check_date', desc=False)\
            .execute()
        
        return {
            'success': True,
            'data': response.data,
            'message': f'Retrieved {len(response.data)} health checks'
        }
        
    except Exception as e:
        return {
            'success': False,
            'data': [],
            'message': f'Error retrieving health check history: {str(e)}'
        }


def get_baseline_values(user_id: str, lookback_days: int = 30) -> Dict[str, Any]:
    """
    Calculate baseline values from historical data
    Uses the average of measurements from a specified lookback period
    
    Args:
        user_id (str): User's unique ID
        lookback_days (int): Number of days to look back for baseline calculation
    
    Returns:
        dict: {'success': bool, 'baseline': dict, 'message': str}
    """
    try:
        supabase = get_supabase_client()
        
        if not supabase:
            return {
                'success': False,
                'baseline': {},
                'message': 'Database connection not configured'
            }
        
        # Get historical data for baseline calculation
        cutoff_date = (date.today() - timedelta(days=lookback_days)).isoformat()
        
        response = supabase.table('health_checks')\
            .select('*')\
            .eq('user_id', user_id)\
            .gte('check_date', cutoff_date)\
            .execute()
        
        if not response.data or len(response.data) < 3:
            return {
                'success': False,
                'baseline': {},
                'message': f'Insufficient data for baseline calculation. Need at least 3 checks, found {len(response.data) if response.data else 0}'
            }
        
        # Calculate averages for each metric
        metrics = [
            'sit_stand_speed', 'sit_stand_stability', 'walk_speed', 
            'walk_stability', 'gait_symmetry', 'hand_steadiness',
            'tremor_index', 'coordination_score', 'overall_mobility'
        ]
        
        baseline = {}
        for metric in metrics:
            values = [check.get(metric) for check in response.data if check.get(metric) is not None]
            if values:
                baseline[metric] = sum(values) / len(values)
        
        return {
            'success': True,
            'baseline': baseline,
            'message': f'Baseline calculated from {len(response.data)} health checks'
        }
        
    except Exception as e:
        return {
            'success': False,
            'baseline': {},
            'message': f'Error calculating baseline: {str(e)}'
        }


def get_drift_history(user_id: str, metric_name: str, days: int = 7) -> Dict[str, Any]:
    """
    Calculate drift history for a specific metric over specified days
    
    Args:
        user_id (str): User's unique ID
        metric_name (str): Name of the metric to track
        days (int): Number of days to retrieve
    
    Returns:
        dict: {'success': bool, 'drift_history': list, 'baseline_value': float, 'message': str}
    """
    try:
        # Get baseline
        baseline_result = get_baseline_values(user_id, lookback_days=30)
        if not baseline_result['success']:
            return {
                'success': False,
                'drift_history': [],
                'baseline_value': None,
                'message': baseline_result['message']
            }
        
        baseline_value = baseline_result['baseline'].get(metric_name)
        if baseline_value is None:
            return {
                'success': False,
                'drift_history': [],
                'baseline_value': None,
                'message': f'No baseline data for metric: {metric_name}'
            }
        
        # Get recent history
        history_result = get_health_check_history(user_id, days=days)
        if not history_result['success']:
            return {
                'success': False,
                'drift_history': [],
                'baseline_value': baseline_value,
                'message': history_result['message']
            }
        
        # Calculate drift for each day
        drift_history = []
        for i, check in enumerate(history_result['data'], 1):
            current_value = check.get(metric_name)
            if current_value is not None:
                drift_percentage = ((current_value - baseline_value) / baseline_value) * 100
                drift_history.append({
                    'day': i,
                    'date': check.get('check_date'),
                    'value': current_value,
                    'drift_percentage': round(drift_percentage, 2)
                })
        
        return {
            'success': True,
            'drift_history': drift_history,
            'baseline_value': baseline_value,
            'message': f'Retrieved {len(drift_history)} days of drift data'
        }
        
    except Exception as e:
        return {
            'success': False,
            'drift_history': [],
            'baseline_value': None,
            'message': f'Error calculating drift history: {str(e)}'
        }
