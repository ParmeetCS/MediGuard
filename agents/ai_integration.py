"""
AI Integration Layer - MediGuard Drift AI
Connects Supabase data with ADK Orchestrator for intelligent health analysis
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import pandas as pd

# Import data repositories
from storage.context_repository import ContextRepository
from storage.health_repository import get_health_check_history

# Import ADK Orchestrator
from agents.orchestrator import run_full_health_analysis, quick_drift_check, HealthDriftOrchestrator
from agents.adk_runtime import is_adk_ready


class AIHealthAnalyzer:
    """
    High-level AI integration for health analysis
    
    This class:
    1. Fetches user data from Supabase (context + health checks)
    2. Prepares data in format needed by ADK agents
    3. Executes ADK orchestrator with real user data
    4. Returns structured insights for UI display
    """
    
    def __init__(self):
        """Initialize the AI analyzer"""
        self.context_repo = ContextRepository()
        self.orchestrator = HealthDriftOrchestrator()
    
    def analyze_user_health(
        self,
        user_id: str,
        metric_name: str = "avg_movement_speed",  # Changed default to a metric that exists
        days_to_analyze: int = 14
    ) -> Dict[str, Any]:
        """
        Perform comprehensive AI analysis of user's health data
        
        Args:
            user_id (str): User identifier
            metric_name (str): Metric to analyze (default: avg_movement_speed)
            days_to_analyze (int): Number of days of history to fetch
        
        Returns:
            Dict containing:
                - success (bool): Analysis status
                - has_data (bool): Whether user has sufficient data
                - analysis (dict): Full ADK orchestrator output
                - summary (dict): User-friendly summary
                - recommendations (list): Actionable recommendations
                - error (str): Error message if failed
                - message (str): User-friendly message
        """
        # Check if ADK is ready
        if not is_adk_ready():
            return {
                "success": False,
                "has_data": False,
                "analysis": {},
                "summary": {},
                "recommendations": [],
                "error": "AI system not configured. Please set GOOGLE_API_KEY in .env file."
            }
        
        # Fetch user context from Supabase
        context_result = self.context_repo.fetch_user_context(user_id)
        user_context = context_result.get('data', {})
        
        # Fetch health check history from Supabase
        health_result = get_health_check_history(user_id, days=days_to_analyze)
        
        if not health_result['success'] or len(health_result['data']) < 2:
            return {
                "success": False,
                "has_data": False,
                "analysis": {},
                "summary": {
                    "message": "Insufficient data for analysis. Please complete more daily health checks."
                },
                "recommendations": ["Complete daily health checks to establish baseline"],
                "error": "Not enough health check data",
                "message": f"You need at least 2 health checks for AI analysis. Currently have: {len(health_result['data']) if health_result['success'] else 0}"
            }
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame(health_result['data'])
        df['date'] = pd.to_datetime(df['check_date'])
        df = df.sort_values('date')
        
        # Check if metric exists in the data
        if metric_name not in df.columns:
            # Try to use a metric that exists
            available_metrics = [col for col in df.columns if 'movement_speed' in col or 'stability' in col]
            if available_metrics:
                metric_name = available_metrics[0]  # Use first available metric
            else:
                return {
                    "success": False,
                    "has_data": True,
                    "analysis": {},
                    "summary": {
                        "message": f"Metric '{metric_name}' not found in health data."
                    },
                    "recommendations": ["Complete health checks with all required metrics"],
                    "error": f"Metric '{metric_name}' not available. Available columns: {list(df.columns)}",
                    "message": f"Data issue: Metric '{metric_name}' not found in your health checks"
                }
        
        # Prepare data for ADK analysis
        baseline_value = self._calculate_baseline(df, metric_name)
        recent_value = df[metric_name].iloc[-1]
        drift_history = self._prepare_drift_history(df, metric_name, baseline_value)
        
        # Prepare user profile
        user_profile = {
            "age": user_context.get('age', 'Not provided'),
            "lifestyle": user_context.get('lifestyle', 'Not provided')
        }
        
        # Execute full ADK orchestrator pipeline
        try:
            analysis_result = run_full_health_analysis(
                metric_name=metric_name,
                baseline_value=baseline_value,
                recent_value=recent_value,
                drift_history=drift_history,
                user_profile=user_profile,
                user_id=user_id
            )
            
            # Extract key insights for UI
            summary = self._create_summary(analysis_result, metric_name, baseline_value, recent_value)
            recommendations = self._extract_recommendations(analysis_result)
            
            return {
                "success": True,
                "has_data": True,
                "analysis": analysis_result,
                "summary": summary,
                "recommendations": recommendations,
                "error": None
            }
            
        except Exception as e:
            return {
                "success": False,
                "has_data": True,
                "analysis": {},
                "summary": {},
                "recommendations": [],
                "error": f"Analysis error: {str(e)}"
            }
    
    def get_conversational_response(
        self,
        user_id: str,
        user_question: str
    ) -> Dict[str, Any]:
        """
        Generate AI-powered conversational response to user question
        
        Args:
            user_id (str): User identifier
            user_question (str): User's question
        
        Returns:
            Dict containing:
                - success (bool)
                - response (str): AI-generated response
                - analysis (dict): Supporting analysis data
                - error (str): Error if failed
        """
        # Analyze user's health first
        analysis_result = self.analyze_user_health(user_id)
        
        if not analysis_result['success']:
            return {
                "success": False,
                "response": "I need more health check data to provide meaningful insights. Please complete your daily health checks!",
                "analysis": {},
                "error": analysis_result.get('error')
            }
        
        # Generate contextual response based on analysis
        response = self._generate_contextual_response(
            question=user_question,
            analysis=analysis_result['analysis'],
            summary=analysis_result['summary']
        )
        
        return {
            "success": True,
            "response": response,
            "analysis": analysis_result['analysis'],
            "error": None
        }
    
    def _calculate_baseline(self, df: pd.DataFrame, metric_name: str) -> float:
        """Calculate baseline from first 5 days of data"""
        if len(df) >= 5:
            return df[metric_name].iloc[:5].mean()
        else:
            return df[metric_name].mean()
    
    def _prepare_drift_history(
        self,
        df: pd.DataFrame,
        metric_name: str,
        baseline_value: float
    ) -> List[Dict[str, Any]]:
        """Prepare drift history in format expected by ADK agents"""
        drift_history = []
        
        for idx, row in df.iterrows():
            value = row[metric_name]
            drift_percentage = ((value - baseline_value) / baseline_value) * 100
            
            drift_history.append({
                "day": idx + 1,
                "date": row['date'].strftime('%Y-%m-%d'),
                "value": round(value, 2),
                "drift_percentage": round(drift_percentage, 2)
            })
        
        return drift_history
    
    def _create_summary(
        self,
        analysis: Dict[str, Any],
        metric_name: str,
        baseline: float,
        recent: float
    ) -> Dict[str, Any]:
        """Create user-friendly summary from ADK analysis"""
        drift_percentage = ((recent - baseline) / baseline) * 100
        
        drift_summary = analysis.get('drift_summary', {})
        context_analysis = analysis.get('contextual_explanation', {})
        risk_assessment = analysis.get('risk_assessment', {})
        safety_notice = analysis.get('safety_notice', {})
        
        return {
            "metric_name": metric_name.replace('_', ' ').title(),
            "baseline_value": round(baseline, 2),
            "recent_value": round(recent, 2),
            "drift_percentage": round(drift_percentage, 2),
            "severity": drift_summary.get('severity_level', 'unknown'),
            "trend": drift_summary.get('trend_direction', 'unknown'),
            "risk_level": risk_assessment.get('risk_level', 'unknown'),
            "escalation_needed": safety_notice.get('escalation_required', False),
            "possible_factors": context_analysis.get('possible_factors', []),
            "confidence": context_analysis.get('confidence_level', 0.0)
        }
    
    def _extract_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Extract actionable recommendations from ADK analysis"""
        recommendations = []
        
        # From care agent
        care_guidance = analysis.get('care_guidance', {})
        if care_guidance.get('guidance_list'):
            recommendations.extend(care_guidance['guidance_list'][:3])
        
        # From context agent
        context_analysis = analysis.get('contextual_explanation', {})
        if context_analysis.get('recommendations'):
            recommendations.extend(context_analysis['recommendations'][:2])
        
        # From safety agent
        safety_notice = analysis.get('safety_notice', {})
        if safety_notice.get('escalation_required'):
            recommendations.insert(0, "⚠️ Consider consulting with a healthcare professional")
        
        return recommendations[:5]  # Limit to top 5
    
    def _generate_contextual_response(
        self,
        question: str,
        analysis: Dict[str, Any],
        summary: Dict[str, Any]
    ) -> str:
        """Generate contextual response based on analysis"""
        # Get key insights
        metric = summary['metric_name']
        drift_pct = summary['drift_percentage']
        severity = summary['severity']
        factors = summary['possible_factors']
        
        # Build response
        response = f"""Based on my analysis of your recent health data:\n\n"""
        
        response += f"**{metric} Status:**\n"
        response += f"- Current change: {drift_pct:+.1f}% from baseline\n"
        response += f"- Severity: {severity.title()}\n"
        response += f"- Trend: {summary['trend'].title()}\n\n"
        
        if factors:
            response += "**Possible Contributing Factors:**\n"
            for factor in factors[:3]:
                response += f"- {factor}\n"
            response += "\n"
        
        # Add care guidance
        care_guidance = analysis.get('care_guidance', {})
        if care_guidance.get('summary_message'):
            response += f"**Guidance:**\n{care_guidance['summary_message']}\n\n"
        
        # Add safety notice if needed
        if summary['escalation_needed']:
            response += "⚠️ **Important:** Based on the patterns I'm seeing, consider discussing these changes with your healthcare provider.\n\n"
        
        response += "_This analysis is for monitoring purposes only and does not replace professional medical advice._"
        
        return response


# Helper functions for easy access
def get_ai_health_insights(user_id: str, metric: str = "overall_mobility") -> Dict[str, Any]:
    """Quick function to get AI health insights for a user"""
    analyzer = AIHealthAnalyzer()
    return analyzer.analyze_user_health(user_id, metric)


def get_ai_chat_response(user_id: str, question: str) -> Dict[str, Any]:
    """Quick function to get AI chat response"""
    analyzer = AIHealthAnalyzer()
    return analyzer.get_conversational_response(user_id, question)
