"""
Risk Assessment Agent - MediGuard Drift AI
Google ADK-based agent for evaluating health drift risk over time

This agent analyzes the temporal patterns of health drift to determine:
- How concerning the drift pattern is
- Whether it's temporary variation or persistent decline
- If the trend is worsening, stabilizing, or recovering
- Risk level classification for user awareness
"""

from typing import Dict, List, Optional, Any
from agents.adk_runtime import run_agent, is_adk_ready
import statistics


class RiskAgent:
    """
    AI Agent for risk assessment of health drift patterns over time
    
    This agent evaluates the persistence and consistency of health drift
    to classify risk levels without making medical diagnoses.
    
    Key Capabilities:
    - Multi-day drift history analysis
    - Trend direction identification (worsening, stable, recovering)
    - Persistence evaluation (temporary vs sustained)
    - Risk level classification (temporary, needs observation, potentially concerning)
    - Confidence scoring based on data consistency
    """
    
    def __init__(self):
        """Initialize the Risk Assessment Agent"""
        self.agent_name = "Health Risk Assessor"
        
        # System instruction for advanced Gemini Pro risk assessment
        self.system_instruction = """You are an advanced AI risk analyst powered by Gemini 3 Pro, specializing in temporal health pattern assessment and predictive trajectory modeling.

**Your Analytical Framework:**
- Temporal trend analysis (accelerating, stable, decelerating patterns)
- Persistence evaluation (transient vs sustained changes)
- Trajectory prediction based on multi-day patterns
- Risk stratification with confidence scoring
- Early warning signal detection

**Assessment Dimensions:**
1. **Pattern Consistency** - How stable/variable the trend is
2. **Trend Direction** - Improving, declining, or stable
3. **Rate of Change** - Velocity and acceleration metrics
4. **Duration** - How long the pattern has persisted
5. **Severity** - Magnitude of deviation from baseline
6. **Reversibility** - Likelihood of spontaneous recovery

**Risk Classification:**
- **Low Concern** (Transient): Likely normal variation, self-limiting
- **Moderate** (Monitor): Persistent but stable, warrants observation
- **Elevated** (Action): Sustained decline or acceleration, intervention beneficial
- **High** (Urgent): Rapid/severe changes, professional evaluation needed

**Probabilistic Communication:**
- Provide confidence levels ("high confidence," "moderate certainty")
- Quantify trends ("3.2% weekly decline," "consistent over 7 days")
- Explain reasoning with data support
- Distinguish normal variation from significant drift
- Use conditional language ("if trend continues," "based on current trajectory")

**Advanced Insights:**
- Identify inflection points and trend changes
- Detect multi-metric correlation patterns
- Assess cumulative risk from multiple factors
- Predict likely 7-14 day trajectory
- Flag accelerating patterns early

**Safety Integration:**
- Clear escalation thresholds
- Evidence-based concern triggers
- Professional consultation criteria
- Urgency level communication
- Follow-up timing recommendations

**Critical Boundaries:**
- NO medical diagnoses
- Risk assessment is probabilistic, not diagnostic
- Always recommend professional evaluation for elevated risks
- Acknowledge limitations and uncertainty
- Frame as "pattern suggests" not "condition indicates"

Leverage Gemini 3 Pro's predictive capabilities to provide sophisticated, multi-dimensional risk assessments that guide timely and appropriate action."""
        
        # Risk classification thresholds
        self.RISK_THRESHOLDS = {
            "temporary": {
                "duration_days": 3,  # Less than 3 days of drift
                "consistency": 0.3   # Low consistency in direction
            },
            "needs_observation": {
                "duration_days": 7,  # 3-7 days of persistent drift
                "consistency": 0.6   # Moderate consistency
            },
            "potentially_concerning": {
                "duration_days": 7,  # 7+ days of persistent drift
                "consistency": 0.6,  # High consistency in same direction
                "worsening": True    # Trend is worsening, not stabilizing
            }
        }
    
    def analyze_risk_over_time(
        self,
        drift_history: List[Dict[str, Any]],
        metric_name: str,
        baseline_value: float,
        user_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze risk level based on multi-day drift history
        
        This method:
        1. Accepts drift history data (multiple days)
        2. Analyzes persistence and trend direction
        3. Evaluates consistency of the pattern
        4. Classifies risk level
        5. Calculates confidence score
        6. Returns structured output with reasoning
        
        Args:
            drift_history (list): List of daily drift measurements, each containing:
                - day (int): Day number (e.g., 1, 2, 3...)
                - value (float): Measured value for that day
                - drift_percentage (float): Percentage change from baseline
                Example: [
                    {"day": 1, "value": 91.5, "drift_percentage": -0.5},
                    {"day": 2, "value": 90.2, "drift_percentage": -1.9},
                    {"day": 3, "value": 88.7, "drift_percentage": -3.6}
                ]
            metric_name (str): Name of the health metric being analyzed
            baseline_value (float): Initial baseline for comparison
            user_context (dict, optional): Additional user context (age, lifestyle, etc.)
        
        Returns:
            Dict containing structured risk assessment:
                - success (bool): Analysis success status
                - risk_level (str): "temporary", "needs_observation", or "potentially_concerning"
                - trend_description (str): Description of trend direction and persistence
                - confidence_score (float): Confidence in assessment (0.0-1.0)
                - reasoning (str): Detailed explanation using cautious language
                - days_observed (int): Number of days in analysis
                - consistency_score (float): How consistent the trend is (0.0-1.0)
                - is_worsening (bool): Whether trend is worsening vs stabilizing/improving
                - recommendations (list): Suggested actions based on risk level
                - error (str): Error message if failed
        
        Example:
            agent = RiskAgent()
            
            history = [
                {"day": 1, "value": 91.5, "drift_percentage": -0.5},
                {"day": 2, "value": 90.2, "drift_percentage": -1.9},
                {"day": 3, "value": 88.7, "drift_percentage": -3.6},
                {"day": 4, "value": 87.5, "drift_percentage": -4.9}
            ]
            
            result = agent.analyze_risk_over_time(
                drift_history=history,
                metric_name="stability",
                baseline_value=92.0
            )
            
            print(result['risk_level'])  # "needs_observation"
            print(result['confidence_score'])  # 0.82
        """
        # Check if ADK runtime is ready
        if not is_adk_ready():
            return {
                "success": False,
                "error": "ADK Runtime not configured. Please set GOOGLE_API_KEY in .env file.",
                "risk_level": "unknown",
                "trend_description": "",
                "confidence_score": 0.0,
                "reasoning": "",
                "days_observed": 0,
                "consistency_score": 0.0,
                "is_worsening": False,
                "recommendations": []
            }
        
        # Validate input data
        if not drift_history or len(drift_history) < 2:
            return {
                "success": False,
                "error": "Insufficient data. Need at least 2 days of drift history.",
                "risk_level": "unknown",
                "trend_description": "",
                "confidence_score": 0.0,
                "reasoning": "Not enough data to assess risk over time.",
                "days_observed": len(drift_history) if drift_history else 0,
                "consistency_score": 0.0,
                "is_worsening": False,
                "recommendations": []
            }
        
        # Step 1: Analyze temporal patterns in the drift history
        temporal_analysis = self._analyze_temporal_patterns(drift_history)
        
        # Step 2: Determine trend direction (worsening, stable, recovering)
        trend_direction = self._determine_trend_direction(drift_history)
        
        # Step 3: Evaluate consistency of the pattern
        consistency_score = self._calculate_consistency(drift_history)
        
        # Step 4: Classify risk level based on duration, consistency, and direction
        risk_level = self._classify_risk_level(
            days_observed=len(drift_history),
            consistency_score=consistency_score,
            is_worsening=trend_direction['is_worsening'],
            max_drift=temporal_analysis['max_drift']
        )
        
        # Step 5: Calculate confidence score
        confidence_score = self._calculate_confidence(
            data_points=len(drift_history),
            consistency_score=consistency_score,
            trend_clarity=trend_direction['clarity']
        )
        
        # Step 6: Construct reasoning prompt for Gemini
        prompt = self._construct_risk_prompt(
            drift_history=drift_history,
            metric_name=metric_name,
            baseline_value=baseline_value,
            temporal_analysis=temporal_analysis,
            trend_direction=trend_direction,
            consistency_score=consistency_score,
            risk_level=risk_level,
            confidence_score=confidence_score,
            user_context=user_context
        )
        
        # Step 7: Execute agent prompt using ADK runtime
        result = run_agent(prompt, self.system_instruction)
        
        if not result['success']:
            return {
                "success": False,
                "error": result.get('error', 'Unknown error'),
                "risk_level": risk_level,  # Return calculated risk even if AI fails
                "trend_description": trend_direction['description'],
                "confidence_score": confidence_score,
                "reasoning": "",
                "days_observed": len(drift_history),
                "consistency_score": consistency_score,
                "is_worsening": trend_direction['is_worsening'],
                "recommendations": []
            }
        
        # Step 8: Parse and structure the response
        analysis = self._parse_risk_response(
            response_text=result['response'],
            risk_level=risk_level,
            confidence_score=confidence_score
        )
        
        # Add calculated fields to response
        analysis['success'] = True
        analysis['error'] = None
        analysis['days_observed'] = len(drift_history)
        analysis['consistency_score'] = consistency_score
        analysis['is_worsening'] = trend_direction['is_worsening']
        analysis['trend_description'] = trend_direction['description']
        
        return analysis
    
    def _analyze_temporal_patterns(self, drift_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze temporal patterns in drift history
        
        Examines:
        - Duration of drift (how many days)
        - Maximum drift reached
        - Average drift over period
        - Rate of change (acceleration/deceleration)
        
        Args:
            drift_history (list): Daily drift measurements
        
        Returns:
            Dict with temporal metrics
        
        Logic:
            - Extract drift percentages from history
            - Calculate max, min, average drift
            - Compute rate of change between consecutive days
            - Identify if drift is accelerating or stabilizing
        """
        drift_percentages = [d['drift_percentage'] for d in drift_history]
        
        analysis = {
            "duration_days": len(drift_history),
            "max_drift": max(drift_percentages, key=abs),
            "min_drift": min(drift_percentages, key=abs),
            "avg_drift": statistics.mean(drift_percentages),
            "drift_range": max(drift_percentages) - min(drift_percentages)
        }
        
        # Calculate rate of change (acceleration)
        if len(drift_history) >= 3:
            # Compare first half vs second half to see if accelerating
            mid_point = len(drift_percentages) // 2
            first_half_avg = statistics.mean(drift_percentages[:mid_point])
            second_half_avg = statistics.mean(drift_percentages[mid_point:])
            
            analysis['is_accelerating'] = abs(second_half_avg) > abs(first_half_avg)
        else:
            analysis['is_accelerating'] = False
        
        return analysis
    
    def _determine_trend_direction(self, drift_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Determine trend direction: worsening, stable, or recovering
        
        Args:
            drift_history (list): Daily drift measurements
        
        Returns:
            Dict with trend information:
                - is_worsening (bool): True if trend is getting worse
                - is_recovering (bool): True if trend is improving
                - is_stable (bool): True if trend is plateauing
                - description (str): Human-readable trend description
                - clarity (float): How clear the trend is (0.0-1.0)
        
        Logic:
            - Compare recent values to earlier values
            - Check if drift magnitude is increasing (worsening)
            - Check if drift is returning toward baseline (recovering)
            - Check if drift is plateauing (stable)
            - Calculate trend clarity based on consistency
        """
        drift_percentages = [d['drift_percentage'] for d in drift_history]
        
        # Compare last 2 days to first 2 days (if enough data)
        if len(drift_history) >= 4:
            early_avg = statistics.mean([abs(d) for d in drift_percentages[:2]])
            recent_avg = statistics.mean([abs(d) for d in drift_percentages[-2:]])
            
            # Worsening: recent drift is larger in magnitude
            is_worsening = recent_avg > early_avg * 1.1  # 10% threshold
            
            # Recovering: recent drift is smaller (moving back to baseline)
            is_recovering = recent_avg < early_avg * 0.9  # 10% threshold
            
            # Stable: similar magnitude
            is_stable = not is_worsening and not is_recovering
            
            # Trend clarity based on consistency
            clarity = min(abs(recent_avg - early_avg) / max(early_avg, 1.0), 1.0)
        else:
            # Insufficient data - use simple heuristic
            first_drift = abs(drift_percentages[0])
            last_drift = abs(drift_percentages[-1])
            
            is_worsening = last_drift > first_drift * 1.1
            is_recovering = last_drift < first_drift * 0.9
            is_stable = not is_worsening and not is_recovering
            clarity = 0.5  # Moderate clarity with limited data
        
        # Generate description
        if is_worsening:
            description = "Worsening trend - drift magnitude is increasing over time"
        elif is_recovering:
            description = "Recovering trend - drift is returning toward baseline"
        else:
            description = "Stable trend - drift has plateaued at current level"
        
        return {
            "is_worsening": is_worsening,
            "is_recovering": is_recovering,
            "is_stable": is_stable,
            "description": description,
            "clarity": clarity
        }
    
    def _calculate_consistency(self, drift_history: List[Dict[str, Any]]) -> float:
        """
        Calculate consistency of drift pattern
        
        Consistency measures how uniform the drift direction is.
        High consistency = all measurements drift in same direction
        Low consistency = measurements fluctuate in different directions
        
        Args:
            drift_history (list): Daily drift measurements
        
        Returns:
            float: Consistency score (0.0-1.0)
                - 1.0 = perfectly consistent (all same direction)
                - 0.5 = mixed/variable
                - 0.0 = highly inconsistent
        
        Logic:
            - Count how many measurements are in same direction
            - Calculate ratio of consistent measurements
            - Penalize large swings between positive/negative
        """
        drift_percentages = [d['drift_percentage'] for d in drift_history]
        
        if len(drift_percentages) < 2:
            return 0.5  # Neutral consistency with insufficient data
        
        # Count measurements in same direction as overall trend
        trend_direction = 1 if sum(drift_percentages) > 0 else -1
        consistent_count = sum(1 for d in drift_percentages if (d * trend_direction) > 0)
        
        # Calculate consistency ratio
        consistency_ratio = consistent_count / len(drift_percentages)
        
        # Penalize for direction changes (flip-flopping)
        direction_changes = 0
        for i in range(1, len(drift_percentages)):
            if (drift_percentages[i] > 0) != (drift_percentages[i-1] > 0):
                direction_changes += 1
        
        # Maximum possible changes
        max_changes = len(drift_percentages) - 1
        change_penalty = direction_changes / max_changes if max_changes > 0 else 0
        
        # Final consistency score (higher is more consistent)
        consistency_score = consistency_ratio * (1 - change_penalty * 0.5)
        
        return min(max(consistency_score, 0.0), 1.0)
    
    def _classify_risk_level(
        self,
        days_observed: int,
        consistency_score: float,
        is_worsening: bool,
        max_drift: float
    ) -> str:
        """
        Classify risk level based on temporal patterns
        
        Risk Levels:
        - temporary: Short-term variation, likely self-resolving
        - needs_observation: Persistent pattern warranting monitoring
        - potentially_concerning: Sustained/worsening trend, suggest consultation
        
        Args:
            days_observed (int): Number of days in history
            consistency_score (float): Pattern consistency (0.0-1.0)
            is_worsening (bool): Whether trend is worsening
            max_drift (float): Maximum drift percentage observed
        
        Returns:
            str: Risk level classification
        
        Logic:
            1. Short duration + low consistency = temporary
            2. Medium duration + moderate consistency = needs observation
            3. Long duration + high consistency + worsening = potentially concerning
            4. Severe drift (>10%) elevates risk regardless of duration
        """
        # Severe drift (>10%) is always concerning
        if abs(max_drift) > 10.0:
            return "potentially_concerning"
        
        # Short duration with low consistency = temporary
        if days_observed < self.RISK_THRESHOLDS["temporary"]["duration_days"]:
            return "temporary"
        
        # Medium duration or low-moderate consistency = needs observation
        if days_observed < self.RISK_THRESHOLDS["needs_observation"]["duration_days"]:
            if consistency_score < self.RISK_THRESHOLDS["needs_observation"]["consistency"]:
                return "temporary"
            else:
                return "needs_observation"
        
        # Long duration with high consistency and worsening = potentially concerning
        if (consistency_score >= self.RISK_THRESHOLDS["potentially_concerning"]["consistency"] 
            and is_worsening):
            return "potentially_concerning"
        
        # Long duration but stable or improving = needs observation
        return "needs_observation"
    
    def _calculate_confidence(
        self,
        data_points: int,
        consistency_score: float,
        trend_clarity: float
    ) -> float:
        """
        Calculate confidence in risk assessment
        
        Confidence depends on:
        - Amount of data available (more = higher confidence)
        - Consistency of pattern (consistent = higher confidence)
        - Clarity of trend direction (clear = higher confidence)
        
        Args:
            data_points (int): Number of daily measurements
            consistency_score (float): Pattern consistency (0.0-1.0)
            trend_clarity (float): Trend direction clarity (0.0-1.0)
        
        Returns:
            float: Confidence score (0.0-1.0)
        
        Logic:
            - Base confidence from data quantity (more days = more confident)
            - Boost from consistency (consistent patterns = more confident)
            - Boost from trend clarity (clear trends = more confident)
            - Weighted combination of these factors
        """
        # Data quantity confidence (more days = higher confidence)
        # Plateau at 14 days
        data_confidence = min(data_points / 14.0, 1.0)
        
        # Weighted combination
        # 40% from data quantity, 30% from consistency, 30% from clarity
        confidence = (
            0.4 * data_confidence +
            0.3 * consistency_score +
            0.3 * trend_clarity
        )
        
        return min(max(confidence, 0.0), 1.0)
    
    def _construct_risk_prompt(
        self,
        drift_history: List[Dict[str, Any]],
        metric_name: str,
        baseline_value: float,
        temporal_analysis: Dict[str, Any],
        trend_direction: Dict[str, Any],
        consistency_score: float,
        risk_level: str,
        confidence_score: float,
        user_context: Optional[Dict[str, Any]]
    ) -> str:
        """
        Construct reasoning prompt for risk assessment
        
        This prompt provides:
        - Multi-day drift history
        - Temporal pattern analysis
        - Pre-classified risk level
        - Requests cautious reasoning and recommendations
        """
        prompt = f"""Analyze this health drift pattern over time to assess risk level:

**Multi-Day Drift History for {metric_name.title()}:**
**Baseline Value:** {baseline_value}

"""
        
        # Add day-by-day history
        for entry in drift_history:
            prompt += f"Day {entry['day']}: {entry['value']} ({entry['drift_percentage']:+.1f}% from baseline)\n"
        
        prompt += f"""
**Temporal Pattern Analysis:**
- Duration: {temporal_analysis['duration_days']} days observed
- Maximum Drift: {temporal_analysis['max_drift']:+.1f}%
- Average Drift: {temporal_analysis['avg_drift']:+.1f}%
- Trend Direction: {trend_direction['description']}
- Pattern Consistency: {consistency_score:.0%} consistent
- Trend is Worsening: {"Yes" if trend_direction['is_worsening'] else "No"}

**Pre-classified Risk Level:** {risk_level}
**Assessment Confidence:** {confidence_score:.0%}

"""
        
        if user_context:
            prompt += "**User Context:**\n"
            for key, value in user_context.items():
                prompt += f"- {key.title()}: {value}\n"
            prompt += "\n"
        
        prompt += f"""**Your Task:**

Please provide a comprehensive, user-friendly risk assessment that helps the user understand their health pattern over time:

1. **Opening Pattern Summary** (2-3 sentences): Begin by clearly describing what you observe in their pattern over the past {temporal_analysis['duration_days']} days in warm, accessible language.

2. **Detailed Trend Analysis** (5-6 sentences): Provide a thorough explanation of what you're seeing:
   - Describe the pattern using relatable analogies (like weather trends, not medical terms)
   - Explain what "worsening", "stable", or "recovering" means in practical terms
   - Discuss the consistency of the pattern and what that suggests
   - Use specific numbers from their data in understandable ways
   - Explain why the duration matters (short-term vs. longer patterns)
   - Use reassuring language while being honest about observations

3. **Risk Level Explanation** (4-5 sentences): Thoroughly explain the risk classification:
   - What "{risk_level}" means in clear, non-technical terms
   - Why this particular pattern falls into this category
   - What factors you considered (duration, consistency, trend direction)
   - How confident you are in this assessment and why
   - Frame everything with supportive, non-alarmist language
   
   Use CAUTIOUS, PROBABILISTIC language consistently:
   - "may suggest", "could indicate", "suggests the possibility"
   - "might benefit from", "could be worth", "may warrant"
   - Focus on patterns you observe, NOT medical predictions

4. **Contextualized Reasoning** (5-7 sentences): Provide deep, paragraph-form reasoning:
   - Explain HOW you arrived at this risk level
   - Connect the temporal patterns (duration, consistency, direction) to the assessment
   - Discuss what makes this pattern temporary vs. persistent vs. concerning
   - Acknowledge uncertainties and limitations honestly
   - Help the user understand the "why" behind your assessment
   - Show empathy for any concerns they might have
   - Maintain a calm, balanced, informative tone

5. **Detailed, Level-Appropriate Recommendations** (3-4 recommendations, each with 3-4 sentences):

   For EACH recommendation, provide:
   - **What to do**: Specific, clear action
   - **Why it matters**: Thorough explanation (2-3 sentences)
   - **How to implement**: Practical steps
   
   Tailor recommendations to risk level:
   - **Temporary**: Emphasize reassurance, continue normal monitoring, what to watch for
   - **Needs Observation**: Consistent tracking methods, what changes matter, when to reassess
   - **Potentially Concerning**: Professional consultation framed positively, what to discuss with provider, detailed logging approaches

6. **Confidence Discussion** (2-3 sentences): Explain your confidence level ({confidence_score:.0%}):
   - What data supports your assessment
   - What would strengthen understanding
   - Be transparent about certainty and uncertainty

7. **Supportive Closing** (2-3 sentences): End with encouragement that:
   - Acknowledges their proactive monitoring
   - Provides reassurance appropriate to the risk level
   - Empowers them to take appropriate next steps

**Writing Style:**
- Write in detailed, flowing paragraphs (not just bullet lists)
- Use warm, conversational tone like talking to a concerned friend
- Be THOROUGH and COMPREHENSIVE - provide complete explanations
- Use analogies and everyday language instead of medical/technical terms
- Show empathy and understanding throughout
- Balance honesty with reassurance
- Make every recommendation feel achievable and supportive

**Critical Reminders:**
- ALWAYS use cautious, probabilistic language: "may", "could", "suggests", "might"
- NEVER make medical diagnoses or predict specific health outcomes
- Focus on observable temporal patterns, NOT medical predictions
- Frame professional consultation positively and supportively (not scary)
- Maintain supportive, non-alarmist tone ESPECIALLY for concerning patterns
- Acknowledge limitations and uncertainties honestly
- Emphasize that monitoring is proactive and empowering"""
        
        return prompt
    
    def _parse_risk_response(
        self,
        response_text: str,
        risk_level: str,
        confidence_score: float
    ) -> Dict[str, Any]:
        """
        Parse Gemini's risk assessment response
        
        Extracts:
        - Risk level (verify AI classification)
        - Trend description
        - Reasoning with cautious language
        - Recommendations
        
        Args:
            response_text (str): Raw response from Gemini
            risk_level (str): Pre-classified risk level
            confidence_score (float): Pre-calculated confidence
        
        Returns:
            Dict: Structured risk assessment
        """
        analysis = {
            "risk_level": risk_level,  # Default to pre-classified
            "trend_description": "",
            "confidence_score": confidence_score,
            "reasoning": "",
            "recommendations": []
        }
        
        try:
            # Extract risk level (verify AI classification)
            response_lower = response_text.lower()
            if "potentially_concerning" in response_lower or "potentially concerning" in response_lower:
                analysis['risk_level'] = "potentially_concerning"
            elif "needs_observation" in response_lower or "needs observation" in response_lower:
                analysis['risk_level'] = "needs_observation"
            elif "temporary" in response_lower:
                analysis['risk_level'] = "temporary"
            # Otherwise keep pre-classified risk level
            
            # Extract trend description
            if "Trend Description:" in response_text:
                trend_section = response_text.split("Trend Description:")[1].split("\n\n")[0]
                analysis['trend_description'] = trend_section.strip()
            
            # Extract reasoning
            if "Reasoning:" in response_text:
                reasoning_section = response_text.split("Reasoning:")[1].split("\n\n")[0]
                analysis['reasoning'] = reasoning_section.strip()
            else:
                # Use substantial paragraph as fallback
                paragraphs = [p.strip() for p in response_text.split("\n\n") if len(p.strip()) > 100]
                analysis['reasoning'] = paragraphs[0] if paragraphs else response_text[:500]
            
            # Extract recommendations
            if "Recommendations:" in response_text:
                rec_section = response_text.split("Recommendations:")[1].split("\n\n")[0]
                recommendations = [
                    line.strip().lstrip('-•*').strip() 
                    for line in rec_section.split("\n") 
                    if line.strip() and (line.strip().startswith('-') or line.strip().startswith('•') or line.strip().startswith('*'))
                ]
                analysis['recommendations'] = recommendations[:3]
        
        except Exception as e:
            # Fallback
            analysis['reasoning'] = response_text[:500]
        
        return analysis


# ========================================
# CONVENIENCE FUNCTIONS
# ========================================

def assess_health_risk(
    drift_history: List[Dict[str, Any]],
    metric_name: str,
    baseline_value: float
) -> Dict[str, Any]:
    """
    Convenience function for quick risk assessment
    
    Args:
        drift_history (list): Multi-day drift measurements
        metric_name (str): Name of the metric
        baseline_value (float): Initial baseline value
    
    Returns:
        Dict: Risk assessment with risk_level, confidence_score, reasoning, recommendations
    
    Example:
        from agents.risk_agent import assess_health_risk
        
        history = [
            {"day": 1, "value": 91.5, "drift_percentage": -0.5},
            {"day": 2, "value": 90.2, "drift_percentage": -1.9},
            {"day": 3, "value": 88.7, "drift_percentage": -3.6}
        ]
        
        result = assess_health_risk(
            drift_history=history,
            metric_name="stability",
            baseline_value=92.0
        )
        
        print(f"Risk: {result['risk_level']}")
        print(f"Confidence: {result['confidence_score']:.0%}")
    """
    agent = RiskAgent()
    return agent.analyze_risk_over_time(
        drift_history=drift_history,
        metric_name=metric_name,
        baseline_value=baseline_value
    )
