"""
Context Agent - MediGuard Drift AI
Google ADK-based agent for contextual analysis of health drift patterns
Explains WHY changes might be occurring based on user's personal context
"""

from typing import Dict, List, Optional, Any
from agents.adk_runtime import run_agent, is_adk_ready
from storage.context_repository import get_user_context


class ContextAgent:
    """
    AI Agent for contextual analysis of health drift
    
    This agent uses Google's ADK runtime to analyze health drift patterns
    in the context of the user's age, lifestyle, sleep, stress, workload,
    and medical background to explain potential contributing factors.
    """
    
    def __init__(self):
        """Initialize the Context Agent"""
        self.agent_name = "Health Context Analyzer"
        self.system_instruction = """You are a health context analysis AI that explains potential factors behind health metric changes.

Your role:
- Analyze health drift patterns in the context of user's personal situation
- Consider age, lifestyle, sleep, stress, workload, and medical background
- Identify possible contributing factors using probabilistic language
- Provide evidence-based contextual explanations
- Assess confidence level in your analysis

Critical guidelines:
- NEVER make medical diagnoses
- Use probabilistic language: "may", "could be", "might indicate", "possibly related to"
- Present factors as possibilities, not certainties
- Acknowledge limitations when data is insufficient
- Emphasize that these are potential correlations, not causation
- Always recommend consulting healthcare professionals for medical concerns

Focus on helping users understand possible connections between their lifestyle and health patterns."""
    
    def analyze_with_context(
        self,
        drift_analysis: Dict[str, Any],
        user_profile: Dict[str, Any],
        user_id: str
    ) -> Dict[str, Any]:
        """
        Analyze health drift with full user context
        
        Args:
            drift_analysis (dict): Results from drift_agent analysis containing:
                - metric_name (str)
                - severity (str)
                - drift_percentage (float)
                - trend (str)
                - explanation (str)
            user_profile (dict): User profile data containing:
                - name (str)
                - age (int)
                - lifestyle (str)
            user_id (str): User identifier for fetching context from database
        
        Returns:
            Dict containing:
                - success (bool): Analysis success status
                - possible_factors (list): List of potential contributing factors
                - contextual_explanation (str): Detailed explanation with context
                - confidence_level (float): Confidence score 0.0-1.0
                - recommendations (list): Context-aware recommendations
                - error (str): Error message if failed
        
        Example:
            agent = ContextAgent()
            result = agent.analyze_with_context(
                drift_analysis={
                    "metric_name": "stability",
                    "severity": "moderate",
                    "drift_percentage": -4.9,
                    "trend": "declining"
                },
                user_profile={
                    "age": 45,
                    "lifestyle": "working professional"
                },
                user_id="user-123"
            )
        """
        if not is_adk_ready():
            return {
                "success": False,
                "possible_factors": [],
                "contextual_explanation": "AI analysis not available. Please configure GOOGLE_API_KEY.",
                "confidence_level": 0.0,
                "recommendations": [],
                "error": "ADK Runtime not configured"
            }
        
        # Fetch user context from Supabase
        context_result = get_user_context(user_id)
        
        if not context_result['success']:
            # Proceed with limited context
            user_context = self._get_default_context()
        else:
            user_context = context_result['data']
        
        # Construct comprehensive analysis prompt
        prompt = self._construct_context_prompt(
            drift_analysis=drift_analysis,
            user_profile=user_profile,
            user_context=user_context
        )
        
        # Execute agent prompt using ADK runtime
        result = run_agent(prompt, self.system_instruction)
        
        if not result['success']:
            return {
                "success": False,
                "possible_factors": [],
                "contextual_explanation": "",
                "confidence_level": 0.0,
                "recommendations": [],
                "error": result.get('error', 'Unknown error')
            }
        
        # Parse and structure the response
        analysis = self._parse_context_response(
            response_text=result['response'],
            has_full_context=context_result['success']
        )
        
        analysis['success'] = True
        analysis['error'] = None
        
        return analysis
    
    def _construct_context_prompt(
        self,
        drift_analysis: Dict[str, Any],
        user_profile: Dict[str, Any],
        user_context: Dict[str, Any]
    ) -> str:
        """
        Construct a detailed reasoning prompt with full user context
        """
        prompt = f"""Analyze this health drift pattern in the context of the user's personal situation.

**Health Drift Detected:**
- Metric: {drift_analysis.get('metric_name', 'Unknown').title()}
- Change: {drift_analysis.get('drift_percentage', 0):+.1f}%
- Severity: {drift_analysis.get('severity', 'unknown')}
- Trend: {drift_analysis.get('trend', 'unknown')}

**User Profile:**
- Age: {user_profile.get('age', 'Not provided')}
- Lifestyle: {user_profile.get('lifestyle', 'Not provided')}

**Current Lifestyle Context:**
- Sleep: {user_context.get('sleep_hours', 7)} hours per night
- Stress Level: {user_context.get('stress_level', 'medium')}
- Workload: {user_context.get('workload', 'moderate')}
- Activity Level: {user_context.get('activity_level', 'moderate')}

"""
        
        # Add medical context if available
        if user_context.get('medical_summary'):
            prompt += f"""**Medical Background:**
{user_context['medical_summary'][:300]}

"""
        
        if user_context.get('known_conditions'):
            prompt += f"""**Known Conditions:**
{user_context['known_conditions'][:200]}

"""
        
        prompt += """**Your Task:**

1. Analyze how the user's age and lifestyle might relate to this drift
2. Identify 3-5 possible factors that COULD BE contributing to this change
   - Consider sleep patterns, stress, workload, activity level
   - Consider age-related factors
   - Consider medical context if provided
3. Provide a contextual explanation using probabilistic language
4. Assign a confidence level (0.0-1.0) based on:
   - How well the context explains the drift
   - Quality and completeness of context data
   - Strength of evidence for correlations
5. Suggest 2-3 context-aware recommendations

**Response Format:**

Possible Factors:
- [Factor 1 with "may" or "could" language]
- [Factor 2 with "may" or "could" language]
- [Factor 3 with "may" or "could" language]

Contextual Explanation:
[2-3 paragraph explanation connecting the drift to user's context. Use probabilistic language. Acknowledge what you can and cannot determine from the data.]

Confidence Level: [0.0-1.0]

Recommendations:
- [Context-aware recommendation 1]
- [Context-aware recommendation 2]
- [Context-aware recommendation 3]

**Remember:**
- Use "may", "could", "might", "possibly" - never state certainties
- Focus on correlations, not causation
- Acknowledge limitations
- No medical diagnosis
- Recommend professional consultation for concerns
"""
        
        return prompt
    
    def _parse_context_response(
        self,
        response_text: str,
        has_full_context: bool
    ) -> Dict[str, Any]:
        """
        Parse Gemini's context analysis into structured format
        """
        analysis = {
            "possible_factors": [],
            "contextual_explanation": "",
            "confidence_level": 0.5,  # Default moderate confidence
            "recommendations": []
        }
        
        try:
            # Extract possible factors
            if "Possible Factors:" in response_text:
                factors_section = response_text.split("Possible Factors:")[1].split("\n\n")[0]
                factors = [
                    line.strip().lstrip('-•*').strip()
                    for line in factors_section.split("\n")
                    if line.strip() and (line.strip().startswith('-') or line.strip().startswith('•'))
                ]
                analysis['possible_factors'] = factors[:5]  # Limit to 5 factors
            
            # Extract contextual explanation
            if "Contextual Explanation:" in response_text:
                explanation_section = response_text.split("Contextual Explanation:")[1].split("\n\n")[0]
                analysis['contextual_explanation'] = explanation_section.strip()
            else:
                # Use first substantial paragraph
                paragraphs = [p.strip() for p in response_text.split("\n\n") if len(p.strip()) > 100]
                analysis['contextual_explanation'] = paragraphs[0] if paragraphs else response_text[:500]
            
            # Extract confidence level
            if "Confidence Level:" in response_text:
                confidence_line = response_text.split("Confidence Level:")[1].split("\n")[0].strip()
                # Extract number from string (handles "0.7" or "0.7 (high)" etc)
                import re
                confidence_match = re.search(r'(\d+\.?\d*)', confidence_line)
                if confidence_match:
                    confidence = float(confidence_match.group(1))
                    # Ensure it's between 0 and 1
                    if confidence > 1.0:
                        confidence = confidence / 100.0
                    analysis['confidence_level'] = min(1.0, max(0.0, confidence))
            
            # Extract recommendations
            if "Recommendations:" in response_text:
                rec_section = response_text.split("Recommendations:")[1].split("\n\n")[0]
                recommendations = [
                    line.strip().lstrip('-•*').strip()
                    for line in rec_section.split("\n")
                    if line.strip() and (line.strip().startswith('-') or line.strip().startswith('•'))
                ]
                analysis['recommendations'] = recommendations[:3]  # Limit to 3
            
            # Adjust confidence if context is incomplete
            if not has_full_context:
                analysis['confidence_level'] = min(analysis['confidence_level'], 0.6)
        
        except Exception as e:
            # Fallback: use raw response with low confidence
            analysis['contextual_explanation'] = response_text[:500]
            analysis['confidence_level'] = 0.3
        
        return analysis
    
    def _get_default_context(self) -> Dict[str, Any]:
        """
        Get default context when database fetch fails
        """
        return {
            "sleep_hours": 7.0,
            "stress_level": "medium",
            "workload": "moderate",
            "activity_level": "moderate",
            "medical_summary": "",
            "known_conditions": "",
            "report_summary": ""
        }
    
    def quick_context_check(
        self,
        metric_name: str,
        drift_percentage: float,
        user_age: int,
        sleep_hours: float,
        stress_level: str
    ) -> str:
        """
        Quick contextual analysis with minimal inputs
        
        Args:
            metric_name (str): Health metric name
            drift_percentage (float): Percentage change
            user_age (int): User's age
            sleep_hours (float): Average sleep hours
            stress_level (str): Stress level
        
        Returns:
            str: Brief contextual insight
        
        Example:
            agent = ContextAgent()
            insight = agent.quick_context_check(
                metric_name="stability",
                drift_percentage=-4.9,
                user_age=45,
                sleep_hours=5.5,
                stress_level="high"
            )
        """
        if not is_adk_ready():
            return "AI analysis not available."
        
        prompt = f"""Briefly explain how these factors might relate to a {drift_percentage:+.1f}% change in {metric_name}:
- Age: {user_age}
- Sleep: {sleep_hours} hours
- Stress: {stress_level}

Respond in 2-3 sentences using "may" or "could" language. No diagnosis."""
        
        result = run_agent(prompt, self.system_instruction)
        
        if result['success']:
            return result['response']
        else:
            return "Unable to provide contextual analysis."


# ========================================
# CONVENIENCE FUNCTIONS
# ========================================

def analyze_drift_with_context(
    drift_analysis: Dict[str, Any],
    user_profile: Dict[str, Any],
    user_id: str
) -> Dict[str, Any]:
    """
    Convenience function to analyze drift with full user context
    
    Args:
        drift_analysis (dict): Drift detection results
        user_profile (dict): User profile data
        user_id (str): User identifier
    
    Returns:
        Dict: Contextual analysis results
    
    Example:
        from agents.context_agent import analyze_drift_with_context
        
        result = analyze_drift_with_context(
            drift_analysis=drift_result,
            user_profile=profile_data,
            user_id="user-123"
        )
        
        if result['success']:
            print(f"Confidence: {result['confidence_level']}")
            print(f"Factors: {result['possible_factors']}")
    """
    agent = ContextAgent()
    return agent.analyze_with_context(drift_analysis, user_profile, user_id)
