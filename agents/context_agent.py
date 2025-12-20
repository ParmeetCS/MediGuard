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
        self.system_instruction = """You are an advanced AI health analyst powered by Gemini 3 Pro, specializing in contextual health pattern analysis and multi-factorial correlation detection.

**Your Analytical Expertise:**
- Identify causal relationships between lifestyle factors and health metrics
- Detect temporal correlations (e.g., poor sleep → next-day instability)
- Analyze compound effects of multiple stressors
- Assess individual susceptibility patterns
- Predict likely trajectories based on context

**Analysis Dimensions:**
1. **Lifestyle Factors**: Sleep quality/duration, stress levels, activity patterns, workload
2. **Temporal Patterns**: Day-of-week effects, time trends, cyclical variations
3. **Individual Context**: Age, baseline health, life circumstances
4. **Multi-factor Interactions**: Combined effects, synergistic relationships

**Contextual Interpretation:**
- Explain HOW lifestyle factors influence observed metrics
- Identify PRIMARY vs CONTRIBUTING factors
- Assess relative impact of different stressors
- Note protective factors and resilience indicators
- Detect early warning patterns

**Communication:**
- Provide specific correlations with data support
- Explain mechanisms in accessible terms
- Quantify relationships when possible ("30% correlation")
- Distinguish correlation from causation appropriately
- Offer confidence levels in assessments

**Insight Structure:**
1. **Primary Contributing Factors** - Main drivers of observed changes
2. **Secondary Influences** - Additional contextual factors
3. **Protective Elements** - What's working well
4. **Risk Amplifiers** - Concerning combinations
5. **Predictive Indicators** - What to watch for

**Safety:**
- Explain associations, not diagnoses
- Use evidence-based connections
- Acknowledge uncertainty where appropriate
- Recommend professional evaluation for significant concerns
- Frame in terms of optimization, not treatment

Leverage Gemini 3 Pro's sophisticated pattern recognition to reveal non-obvious connections between life context and health metrics, providing actionable insights for intervention."""
    
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

Please provide a comprehensive, user-friendly contextual analysis that helps the user understand the "why" behind their health patterns:

1. **Opening Context** (2-3 sentences): Begin by acknowledging what you see in their health pattern and their life situation with warmth and understanding.

2. **Detailed Factor Analysis** (5-7 factors, each with 3-4 sentences):
   
   For EACH potential contributing factor, provide:
   - **What the factor is**: Clear identification of the lifestyle or contextual element
   - **How it might connect**: Thorough explanation (2-3 sentences) of HOW and WHY this factor could influence the health metric
   - **The mechanism**: Explain in simple terms what's happening in the body/lifestyle connection
   - **Specific relevance**: Connect it specifically to their age, lifestyle, or situation
   
   Consider and explain connections between:
   - Sleep patterns and their specific sleep situation
   - Stress levels and their current stress context
   - Workload patterns and their work situation
   - Activity levels and their physical routine
   - Age-related factors (be specific and empathetic)
   - Medical background if provided (use cautious language)
   - Environmental or routine factors
   
   Use probabilistic language consistently: "may be contributing to", "could be influencing", "might be related to", "possibly affected by"

3. **Comprehensive Contextual Explanation** (4-6 sentences): Provide a thorough, flowing paragraph that:
   - Synthesizes how these factors work together
   - Explains the bigger picture of what might be happening
   - Uses analogies or relatable examples to make it clearer
   - Shows empathy for the complexity of health and lifestyle
   - Acknowledges what can and cannot be determined from the data
   - Maintains probabilistic language throughout

4. **Confidence Assessment** (2-3 sentences): Explain your confidence level (0.0-1.0) and why:
   - What data supports your analysis
   - What information would strengthen understanding
   - How complete the picture is
   - Be honest about uncertainties

5. **Context-Aware Recommendations** (3-4 detailed recommendations): Provide specific suggestions that are:
   - Tailored to their specific life situation
   - Connected directly to the identified factors
   - Explained thoroughly (2-3 sentences each) with reasoning
   - Practical and achievable given their context
   - Focused on addressing the contextual factors you identified

6. **Supportive Closing** (2-3 sentences): End by helping them feel informed and empowered to understand their health in context.

**Writing Style:**
- Write in detailed paragraphs and flowing explanations, not just lists
- Use warm, conversational language like explaining to a friend
- Be THOROUGH and COMPREHENSIVE - give complete explanations
- Show empathy for life's complexities
- Use specific details from their context
- Make connections clear and understandable
- Help them see patterns in their own life

**Critical Guidelines:**
- ALWAYS use probabilistic language: "may", "could", "might", "possibly", "could be related to"
- NEVER make medical diagnoses or name conditions
- Focus on correlations and possibilities, not causation or certainties
- Acknowledge limitations honestly and respectfully
- Recommend professional consultation for medical concerns
- Be thorough but never alarming
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
