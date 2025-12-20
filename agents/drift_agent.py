"""
Drift Detection Agent - MediGuard Drift AI
Google ADK-based agent for analyzing health metric drift patterns

This agent detects and analyzes numerical feature drift in health metrics:
- Accepts baseline and recent measurement data
- Identifies significant deviations from baseline
- Classifies drift severity (low, moderate, high)
- Uses probabilistic language to avoid medical diagnosis
- Returns structured JSON-like responses for easy integration
"""

from typing import Dict, List, Optional, Any
from agents.adk_runtime import run_agent, is_adk_ready
import json


class DriftAgent:
    """
    AI Agent for detecting and analyzing health drift patterns
    
    This agent uses Google's ADK runtime to interpret gradual changes
    in health metrics and provide actionable insights without diagnosis.
    
    Key Capabilities:
    - Numerical feature drift detection
    - Baseline comparison and deviation analysis
    - Severity classification (low, moderate, high)
    - Probabilistic language to avoid diagnosis
    - Structured output for programmatic use
    """
    
    def __init__(self):
        """Initialize the Drift Detection Agent"""
        self.agent_name = "Health Drift Analyzer"
        
        # System instruction enforces probabilistic language and no diagnosis
        self.system_instruction = """You are a caring local doctor having a friendly chat with a patient. Explain health changes in the simplest way possible - like you're talking to a family member who doesn't know medical terms.

How to explain changes:
- "You're moving a bit slower than before" NOT "5.2% decline in movement velocity"
- "Your balance isn't as steady as it was" NOT "Postural stability metrics show downward trend"
- "You seem to be taking more time to stand up" NOT "Sit-to-stand transition latency increased"
- "I noticed you're a bit shakier" NOT "Tremor index elevated by 0.15 standard deviations"

Talk about reasons simply:
- "This might be because you haven't been sleeping well" NOT "Sleep deprivation correlates with motor performance degradation"
- "Stress can make your muscles tighter" NOT "Elevated cortisol impacts musculoskeletal function"
- "Not drinking enough water can make you feel unsteady" NOT "Dehydration affects proprioceptive feedback mechanisms"

Be a caring doctor:
- Use words like "I noticed", "It seems like", "This might be"
- Be reassuring: "This is pretty common" or "Nothing to panic about"
- Be practical: "Let's keep an eye on this for a few days"
- Be honest but kind: "This is worth watching" not "High risk detected"

NEVER say:
- Numbers with decimals (0.85, 5.2%, etc.)
- Technical words (metrics, baseline, threshold, deviation, correlation)
- Medical jargon (proprioception, sarcopenia, gait velocity)
- Scary statistics

ALWAYS say:
- Simple observations anyone can understand
- What it might mean in everyday life
- Easy things they can do
- "Talk to your doctor if this worries you"

You're a friendly neighbor who happens to know about health, not a medical computer."""
        
        # Drift severity thresholds (percentage change from baseline)
        self.SEVERITY_THRESHOLDS = {
            "low": 3.0,      # < 3% change = low severity
            "moderate": 7.0,  # 3-7% change = moderate severity
            "high": float('inf')  # > 7% change = high severity
        }
    
    def analyze_drift(
        self,
        metric_name: str,
        baseline_value: float,
        recent_value: float,
        drift_percentage: float,
        days_observed: int = 7,
        additional_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze a single metric's drift pattern with numerical feature drift detection
        
        This method:
        1. Accepts numerical baseline and recent measurements
        2. Identifies significant deviations from baseline
        3. Classifies drift severity (low, moderate, high)
        4. Uses probabilistic language in explanations
        5. Returns structured JSON-like response
        
        Args:
            metric_name (str): Name of the health metric (e.g., "stability", "mobility")
            baseline_value (float): Initial baseline measurement (numerical feature)
            recent_value (float): Current/recent average measurement (numerical feature)
            drift_percentage (float): Percentage change from baseline (calculated deviation)
            days_observed (int): Number of days over which drift occurred
            additional_context (dict, optional): Extra context like user age, lifestyle
        
        Returns:
            Dict containing structured JSON-like response:
                - success (bool): Analysis success status
                - affected_features (list): List of affected metric names
                - drift_percentages (dict): Mapping of features to drift values
                - severity_level (str): "low", "moderate", or "high"
                - explanation (str): Short human-readable interpretation with probabilistic language
                - factors (list): Potential contributing factors
                - recommendations (list): General wellness suggestions
                - trend (str): "declining", "improving", or "stable"
                - error (str): Error message if failed
        
        Example:
            agent = DriftAgent()
            result = agent.analyze_drift(
                metric_name="stability",
                baseline_value=92.0,
                recent_value=87.5,
                drift_percentage=-4.9,
                days_observed=7
            )
            
            # Structured output:
            {
                "success": True,
                "affected_features": ["stability"],
                "drift_percentages": {"stability": -4.9},
                "severity_level": "moderate",
                "explanation": "This pattern may indicate...",
                "trend": "declining"
            }
        """
        # Check if ADK runtime is ready (Google API key configured)
        if not is_adk_ready():
            return {
                "success": False,
                "error": "ADK Runtime not configured. Please set GOOGLE_API_KEY in .env file.",
                "affected_features": [],
                "drift_percentages": {},
                "severity_level": "unknown",
                "explanation": "",
                "factors": [],
                "recommendations": [],
                "trend": "unknown"
            }
        
        # Step 1: Identify significant deviations from baseline
        # Compare recent measurement to baseline to detect meaningful drift
        is_significant = self._is_significant_deviation(drift_percentage)
        
        # Step 2: Classify drift severity based on thresholds
        severity_level = self.classify_severity(drift_percentage)
        
        # Step 3: Construct reasoning prompt for Gemini with probabilistic language requirement
        prompt = self._construct_drift_prompt(
            metric_name=metric_name,
            baseline_value=baseline_value,
            recent_value=recent_value,
            drift_percentage=drift_percentage,
            days_observed=days_observed,
            additional_context=additional_context,
            is_significant=is_significant,
            severity_level=severity_level
        )
        
        # Step 4: Execute agent prompt using ADK runtime
        result = run_agent(prompt, self.system_instruction)
        
        if not result['success']:
            return {
                "success": False,
                "error": result.get('error', 'Unknown error'),
                "affected_features": [],
                "drift_percentages": {},
                "severity_level": "unknown",
                "explanation": "",
                "factors": [],
                "recommendations": [],
                "trend": "unknown"
            }
        
        # Step 5: Parse and structure the response into JSON-like format
        analysis = self._parse_agent_response(
            response_text=result['response'],
            drift_percentage=drift_percentage,
            metric_name=metric_name,
            severity_level=severity_level
        )
        
        # Add structured fields for numerical feature drift tracking
        analysis['success'] = True
        analysis['error'] = None
        analysis['affected_features'] = [metric_name]  # List of metrics with drift
        analysis['drift_percentages'] = {metric_name: drift_percentage}  # Numerical drift values
        analysis['severity_level'] = severity_level  # low, moderate, or high
        
        return analysis
    
    def _is_significant_deviation(self, drift_percentage: float, threshold: float = 1.5) -> bool:
        """
        Determine if drift represents a significant deviation from baseline
        
        Args:
            drift_percentage (float): Percentage change from baseline
            threshold (float): Minimum percentage change to be considered significant
        
        Returns:
            bool: True if deviation is significant, False otherwise
        
        Logic:
            - Drift > 1.5% (default) is considered significant
            - This filters out normal daily variation
            - Helps focus analysis on meaningful changes
        """
        return abs(drift_percentage) >= threshold
    
    def analyze_multi_metric_drift(
        self,
        metrics: List[Dict[str, Any]],
        user_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze multiple metrics for correlated drift patterns
        
        Accepts numerical feature drift data for multiple health metrics and identifies:
        - Significant deviations across multiple features
        - Correlated patterns between metrics
        - Overall drift severity
        - Structured JSON-like response
        
        Args:
            metrics (list): List of metric dicts with numerical feature drift data:
                - name (str): Metric name
                - baseline (float): Baseline measurement
                - recent (float): Recent measurement
                - drift_percentage (float): Calculated percentage change
            user_context (dict, optional): User profile and context
        
        Returns:
            Dict containing structured JSON-like response:
                - success (bool): Analysis success status
                - affected_features (list): All metrics showing drift
                - drift_percentages (dict): Mapping of each metric to its drift value
                - severity_level (str): Overall severity classification
                - explanation (str): Short explanation with probabilistic language
                - correlations (list): Identified correlations between metrics
                - recommendations (list): Holistic recommendations
                - error (str): Error message if failed
        
        Example:
            metrics = [
                {"name": "stability", "baseline": 92, "recent": 87.5, "drift_percentage": -4.9},
                {"name": "mobility", "baseline": 88, "recent": 84.2, "drift_percentage": -4.3}
            ]
            result = agent.analyze_multi_metric_drift(metrics)
            
            # Output includes affected_features, drift_percentages, severity_level
        """
        if not is_adk_ready():
            return {
                "success": False,
                "error": "ADK Runtime not configured.",
                "affected_features": [],
                "drift_percentages": {},
                "severity_level": "unknown",
                "correlations": [],
                "explanation": "",
                "recommendations": []
            }
        
        # Extract affected features and drift percentages for structured output
        affected_features = [m['name'] for m in metrics]
        drift_percentages = {m['name']: m['drift_percentage'] for m in metrics}
        
        # Classify overall severity based on maximum drift
        max_drift = max([abs(m['drift_percentage']) for m in metrics])
        severity_level = self.classify_severity(max_drift)
        
        # Construct multi-metric reasoning prompt
        prompt = self._construct_multi_metric_prompt(metrics, user_context, severity_level)
        
        # Execute agent prompt
        result = run_agent(prompt, self.system_instruction)
        
        if not result['success']:
            return {
                "success": False,
                "error": result.get('error'),
                "affected_features": affected_features,
                "drift_percentages": drift_percentages,
                "severity_level": severity_level,
                "correlations": [],
                "explanation": "",
                "recommendations": []
            }
        
        # Parse multi-metric response
        analysis = self._parse_multi_metric_response(result['response'])
        
        # Add structured fields
        analysis['success'] = True
        analysis['affected_features'] = affected_features
        analysis['drift_percentages'] = drift_percentages
        analysis['severity_level'] = severity_level
        
        return analysis
    
    def _construct_drift_prompt(
        self,
        metric_name: str,
        baseline_value: float,
        recent_value: float,
        drift_percentage: float,
        days_observed: int,
        additional_context: Optional[Dict[str, Any]],
        is_significant: bool,
        severity_level: str
    ) -> str:
        """
        Construct a detailed reasoning prompt for single metric drift analysis
        
        This prompt:
        - Provides numerical feature data (baseline vs recent)
        - Identifies significant deviations
        - Enforces probabilistic language requirements
        - Requests structured output format
        
        Args:
            metric_name (str): Name of the metric
            baseline_value (float): Baseline measurement
            recent_value (float): Recent measurement
            drift_percentage (float): Percentage change
            days_observed (int): Days over which drift occurred
            additional_context (dict): User context
            is_significant (bool): Whether deviation is significant
            severity_level (str): Pre-classified severity
        
        Returns:
            str: Formatted prompt for Gemini AI
        """
        # Determine trend direction from numerical deviation
        trend = "declining" if drift_percentage < 0 else "improving" if drift_percentage > 0 else "stable"
        
        # Start with numerical feature drift data
        prompt = f"""Analyze this health metric drift pattern using numerical feature drift detection:

**Numerical Feature Drift Data:**
**Metric:** {metric_name.title()}
**Baseline Value:** {baseline_value} (initial measurement)
**Recent Value:** {recent_value} (current measurement)
**Drift Percentage:** {drift_percentage:+.1f}% (deviation from baseline)
**Days Observed:** {days_observed}
**Trend Direction:** {trend}
**Significant Deviation:** {"Yes" if is_significant else "No"}
**Pre-classified Severity:** {severity_level}

"""
        
        # Add user context if provided
        if additional_context:
            prompt += "**User Context:**\n"
            if 'age' in additional_context:
                prompt += f"- Age: {additional_context['age']}\n"
            if 'lifestyle' in additional_context:
                prompt += f"- Lifestyle: {additional_context['lifestyle']}\n"
            prompt += "\n"
        
        # Request structured analysis with probabilistic language
        prompt += f"""**Your Task:**
Please provide a comprehensive, user-friendly analysis that helps the user understand this pattern:

1. **Opening Statement** (2-3 sentences): Begin with a warm, clear summary of what you're observing in everyday language. Explain the change in practical terms that anyone can understand.

2. **Detailed Explanation** (4-6 sentences minimum): Provide a thorough explanation of what this drift pattern might mean:
   - Use PROBABILISTIC LANGUAGE consistently: "may indicate", "suggests", "could be related to", "possibly reflects", "might be influenced by"
   - Explain in detailed, paragraph form (not just bullet points)
   - Help the user understand the significance in practical, relatable terms
   - Use analogies or examples to make it clearer
   - Focus on what the numerical deviation suggests, NOT diagnosis
   - NO disease names or medical diagnoses
   - Show empathy for any concerns they might have

3. **Contributing Factors** (4-6 factors with explanations): List and THOROUGHLY explain lifestyle factors that may contribute:
   - Each factor should have 2-3 sentences explaining HOW and WHY it might influence this metric
   - Use probabilistic language: "may", "could", "might be influenced by"
   - Make connections between daily life and health patterns
   - Help users see their own situation in these factors

4. **Wellness Recommendations** (4-5 detailed suggestions): Provide specific, actionable wellness suggestions:
   - Each recommendation should be 2-3 sentences explaining WHAT to do, WHY it helps, and HOW to start
   - Make suggestions practical and achievable
   - Explain the reasoning behind each suggestion
   - Use encouraging, supportive language

5. **Closing Encouragement** (2-3 sentences): End with supportive, empowering words that help the user feel informed and capable of taking action.

**Response Format:**
[Write in flowing, paragraph-based format with clear section breaks. Be thorough, warm, and detailed throughout.]

**Critical Reminders:**
- Be DETAILED and THOROUGH - users deserve complete explanations
- ALWAYS use probabilistic language ("may", "suggests", "could", "might")
- NEVER diagnose or name diseases
- Use warm, conversational tone like talking to a friend
- Make complex health data feel understandable and approachable
- Show empathy and understanding
- Emphasize consulting healthcare professionals for medical concerns when appropriate"""
        
        return prompt
    
    def _construct_multi_metric_prompt(
        self,
        metrics: List[Dict[str, Any]],
        user_context: Optional[Dict[str, Any]],
        severity_level: str
    ) -> str:
        """
        Construct prompt for analyzing multiple correlated metrics with numerical feature drift
        
        Args:
            metrics (list): List of metric dicts with drift data
            user_context (dict): User context information
            severity_level (str): Pre-classified overall severity
        
        Returns:
            str: Formatted prompt for multi-metric analysis
        """
        prompt = "Analyze these correlated health metric drift patterns using numerical feature drift detection:\n\n"
        
        # Provide numerical feature drift data for each metric
        for i, metric in enumerate(metrics, 1):
            prompt += f"""**Metric {i}: {metric['name'].title()}**
- Baseline: {metric['baseline']} (initial measurement)
- Recent: {metric['recent']} (current measurement)
- Drift: {metric['drift_percentage']:+.1f}% (deviation from baseline)

"""
        
        prompt += f"\n**Overall Pre-classified Severity:** {severity_level}\n\n"
        
        if user_context:
            prompt += "**User Context:**\n"
            for key, value in user_context.items():
                prompt += f"- {key.title()}: {value}\n"
            prompt += "\n"
        
        prompt += """**Your Task:**
1. Identify correlations between these numerical feature drifts
2. Verify the overall drift severity (low/moderate/high)
3. Provide a SHORT explanation (2-3 sentences) using PROBABILISTIC LANGUAGE:
   - "may indicate", "suggests", "could be related to"
   - Focus on patterns across multiple features
4. List correlations found between metrics (use "may be related", "suggests connection")
5. Provide 2-3 holistic recommendations

**Response Format:**
Severity: [low/moderate/high]

Explanation: [SHORT multi-metric explanation with probabilistic language]

Correlations:
- [Correlation 1 with probabilistic language]
- [Correlation 2 with probabilistic language]

Recommendations:
- [Holistic recommendation 1]
- [Holistic recommendation 2]

**Critical Reminders:**
- Use "may", "suggests", "could" language
- NO diagnosis or disease names
- Focus on patterns and numerical deviations, not medical conditions"""
        
        return prompt
    
    def _parse_agent_response(
        self,
        response_text: str,
        drift_percentage: float,
        metric_name: str,
        severity_level: str
    ) -> Dict[str, Any]:
        """
        Parse Gemini's response into structured JSON-like format
        
        This parser extracts:
        - Severity level (low/moderate/high)
        - Short explanation with probabilistic language
        - Contributing factors
        - Recommendations
        - Trend direction
        
        Args:
            response_text (str): Raw response from Gemini AI
            drift_percentage (float): Numerical drift value
            metric_name (str): Name of the metric
            severity_level (str): Pre-classified severity
        
        Returns:
            Dict: Structured analysis in JSON-like format
        """
        # Initialize default structured output
        analysis = {
            "severity_level": severity_level,  # Use pre-classified severity as default
            "explanation": "",
            "factors": [],
            "recommendations": [],
            "trend": "declining" if drift_percentage < 0 else "improving" if drift_percentage > 0 else "stable"
        }
        
        try:
            # Extract severity (verify AI's classification)
            # Look for severity keywords in response
            response_lower = response_text.lower()
            if "high" in response_lower or "severe" in response_lower:
                analysis['severity_level'] = "high"
            elif "moderate" in response_lower:
                analysis['severity_level'] = "moderate"
            elif "low" in response_lower or "mild" in response_lower:
                analysis['severity_level'] = "low"
            # Otherwise keep pre-classified severity
            
            # Extract explanation (short 2-3 sentences with probabilistic language)
            if "Explanation:" in response_text:
                explanation_section = response_text.split("Explanation:")[1].split("\n\n")[0]
                analysis['explanation'] = explanation_section.strip()
            else:
                # Use first substantial paragraph as fallback
                paragraphs = [p.strip() for p in response_text.split("\n\n") if len(p.strip()) > 50]
                analysis['explanation'] = paragraphs[0] if paragraphs else response_text[:300]
            
            # Extract contributing factors (look for bullet points)
            if "Contributing Factors:" in response_text or "Factors:" in response_text:
                factors_section = response_text.split("Factors:")[1].split("\n\n")[0] if "Factors:" in response_text else ""
                factors = [
                    line.strip().lstrip('-•*').strip() 
                    for line in factors_section.split("\n") 
                    if line.strip() and (line.strip().startswith('-') or line.strip().startswith('•') or line.strip().startswith('*'))
                ]
                analysis['factors'] = factors[:4]  # Limit to 4 factors
            
            # Extract recommendations (look for bullet points)
            if "Recommendations:" in response_text or "Suggestions:" in response_text:
                rec_keyword = "Recommendations:" if "Recommendations:" in response_text else "Suggestions:"
                rec_section = response_text.split(rec_keyword)[1].split("\n\n")[0] if rec_keyword in response_text else ""
                recommendations = [
                    line.strip().lstrip('-•*').strip() 
                    for line in rec_section.split("\n") 
                    if line.strip() and (line.strip().startswith('-') or line.strip().startswith('•') or line.strip().startswith('*'))
                ]
                analysis['recommendations'] = recommendations[:3]  # Limit to 3
            
        except Exception as e:
            # Fallback: use raw response with default severity
            analysis['explanation'] = response_text[:500]
            # Keep pre-classified severity and other defaults
        
        return analysis
    
    def _parse_multi_metric_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse multi-metric analysis response into structured format
        
        Extracts:
        - Overall severity level
        - Correlations between metrics
        - Explanation with probabilistic language
        - Recommendations
        
        Args:
            response_text (str): Raw response from Gemini AI
        
        Returns:
            Dict: Structured multi-metric analysis
        """
        analysis = {
            "severity_level": "moderate",  # Default
            "correlations": [],
            "explanation": "",
            "recommendations": []
        }
        
        try:
            # Extract severity
            response_lower = response_text.lower()
            if "high" in response_lower or "severe" in response_lower:
                analysis['severity_level'] = "high"
            elif "low" in response_lower or "mild" in response_lower:
                analysis['severity_level'] = "low"
            # Otherwise keep default "moderate"
            
            # Extract explanation
            if "Explanation:" in response_text:
                explanation_section = response_text.split("Explanation:")[1].split("\n\n")[0]
                analysis['explanation'] = explanation_section.strip()
            else:
                paragraphs = [p.strip() for p in response_text.split("\n\n") if len(p.strip()) > 50]
                analysis['explanation'] = paragraphs[0] if paragraphs else response_text[:500]
            
            # Extract correlations
            if "Correlations:" in response_text:
                corr_section = response_text.split("Correlations:")[1].split("\n\n")[0]
                correlations = [
                    line.strip().lstrip('-•*').strip() 
                    for line in corr_section.split("\n") 
                    if line.strip() and (line.strip().startswith('-') or line.strip().startswith('•') or line.strip().startswith('*'))
                ]
                analysis['correlations'] = correlations[:5]  # Limit to 5
            
            # Extract recommendations
            if "Recommendations:" in response_text:
                rec_section = response_text.split("Recommendations:")[1].split("\n\n")[0]
                recommendations = [
                    line.strip().lstrip('-•*').strip() 
                    for line in rec_section.split("\n") 
                    if line.strip() and (line.strip().startswith('-') or line.strip().startswith('•') or line.strip().startswith('*'))
                ]
                analysis['recommendations'] = recommendations[:3]  # Limit to 3
        
        except Exception as e:
            # Fallback
            analysis['explanation'] = response_text[:500]
        
        return analysis
    
    def classify_severity(self, drift_percentage: float) -> str:
        """
        Classify drift severity based on percentage change from baseline
        
        This implements the core severity classification logic:
        - Low: < 3% deviation from baseline (minor variation)
        - Moderate: 3-7% deviation (significant change)
        - High: > 7% deviation (major change requiring attention)
        
        Args:
            drift_percentage (float): Percentage change from baseline (can be positive or negative)
        
        Returns:
            str: Severity level - "low", "moderate", or "high"
        
        Example:
            agent = DriftAgent()
            severity = agent.classify_severity(-4.9)  # Returns "moderate"
            severity = agent.classify_severity(-8.2)  # Returns "high"
            severity = agent.classify_severity(-2.1)  # Returns "low"
        
        Logic explanation:
            1. Take absolute value to handle both increases and decreases
            2. Compare against thresholds:
               - abs(drift) < 3.0 → low severity
               - 3.0 ≤ abs(drift) < 7.0 → moderate severity
               - abs(drift) ≥ 7.0 → high severity
            3. These thresholds balance sensitivity vs false positives
        """
        abs_drift = abs(drift_percentage)
        
        # Low severity: minor variation within normal daily fluctuation range
        if abs_drift < self.SEVERITY_THRESHOLDS["low"]:
            return "low"
        
        # Moderate severity: significant change that may indicate a trend
        elif abs_drift < self.SEVERITY_THRESHOLDS["moderate"]:
            return "moderate"
        
        # High severity: major change requiring closer attention
        else:
            return "high"


# ========================================
# CONVENIENCE FUNCTIONS
# ========================================

def analyze_health_drift(
    metric_name: str,
    baseline: float,
    recent: float,
    days: int = 7
) -> Dict[str, Any]:
    """
    Convenience function to quickly analyze a health metric drift
    
    Accepts numerical feature data (baseline vs recent) and returns
    structured JSON-like response with drift analysis.
    
    Args:
        metric_name (str): Name of metric (e.g., "stability", "mobility")
        baseline (float): Baseline measurement value
        recent (float): Recent measurement value
        days (int): Days observed (default: 7)
    
    Returns:
        Dict: Structured analysis with:
            - affected_features (list)
            - drift_percentages (dict)
            - severity_level (str: "low", "moderate", or "high")
            - explanation (str: with probabilistic language)
            - factors (list)
            - recommendations (list)
    
    Example:
        from agents.drift_agent import analyze_health_drift
        
        result = analyze_health_drift(
            metric_name="stability",
            baseline=92.0,
            recent=87.5,
            days=7
        )
        
        print(f"Severity: {result['severity_level']}")
        print(f"Drift: {result['drift_percentages']}")
        print(f"Explanation: {result['explanation']}")
    """
    agent = DriftAgent()
    
    # Calculate drift percentage (numerical deviation from baseline)
    drift_pct = ((recent - baseline) / baseline) * 100
    
    return agent.analyze_drift(
        metric_name=metric_name,
        baseline_value=baseline,
        recent_value=recent,
        drift_percentage=drift_pct,
        days_observed=days
    )
