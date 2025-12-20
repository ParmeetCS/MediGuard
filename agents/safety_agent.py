"""
Safety Agent - MediGuard Drift AI
Ethical guardrail and escalation logic for health monitoring

This agent does NOT analyze health - it enforces safety protocols.

Purpose:
- Monitor outputs from drift and risk agents
- Detect extreme or persistent concerning patterns
- Determine if professional consultation should be recommended
- Provide clear safety disclaimers
- Ensure responsible use of AI health monitoring
"""

from typing import Dict, List, Optional, Any
from agents.adk_runtime import run_agent, is_adk_ready


class SafetyAgent:
    """
    Safety Agent for ethical oversight and escalation logic
    
    This agent acts as a final safety layer that:
    - Reviews analysis outputs from other agents
    - Identifies patterns requiring professional attention
    - Decides when escalation is necessary
    - Provides clear, non-medical safety guidance
    - Enforces ethical guardrails
    
    CRITICAL: This agent does NOT diagnose or analyze health.
    It only determines if the system should recommend seeking professional help.
    """
    
    def __init__(self):
        """Initialize the Safety Agent"""
        self.agent_name = "Safety Oversight"
        
        # System instruction enforces safety-first approach
        self.system_instruction = """You are a safety oversight AI that monitors health monitoring outputs for patterns requiring professional medical attention.

Your ONLY role:
- Review analysis outputs from drift and risk agents
- Identify extreme, persistent, or concerning patterns
- Determine if professional consultation should be recommended
- Provide clear safety disclaimers and rationale

What you ARE:
- A safety guardrail ensuring responsible AI use
- An escalation decision system
- A disclaimer and safety message generator

What you ARE NOT:
- A diagnostic tool
- A medical advisor
- A health analyzer
- A treatment recommender

Critical safety protocols:
1. NEVER provide medical advice or diagnosis
2. NEVER suggest specific treatments or medications
3. NEVER minimize concerning patterns - when in doubt, escalate
4. ALWAYS recommend professional consultation for persistent/severe patterns
5. ALWAYS include clear disclaimers that this is not medical advice
6. Use clear, direct language - avoid technical jargon in safety messages
7. Emphasize that AI monitoring supplements but never replaces professional care

Escalation triggers:
- High severity drift (>10%) persisting over multiple days
- Risk level classified as "potentially_concerning"
- Multiple metrics showing correlated decline
- Any pattern that could benefit from professional evaluation
- User-reported symptoms alongside concerning patterns

Safety-first principle: Better to over-escalate than under-escalate."""
        
        # Escalation thresholds - conservative for safety
        self.ESCALATION_TRIGGERS = {
            "severe_drift": 10.0,  # >10% drift triggers escalation
            "high_risk_days": 7,    # 7+ days of concerning patterns
            "multiple_metrics": 2,  # 2+ metrics showing problems
            "worsening_trend": True # Any worsening trend with high risk
        }
    
    def evaluate_safety(
        self,
        drift_analysis: Optional[Dict[str, Any]] = None,
        risk_analysis: Optional[Dict[str, Any]] = None,
        context_analysis: Optional[Dict[str, Any]] = None,
        user_reported_symptoms: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Evaluate if escalation to professional care is required
        
        This method:
        1. Monitors outputs from drift_agent and risk_agent
        2. Detects extreme or persistent concerning patterns
        3. Decides if professional consultation should be advised
        4. Generates appropriate safety messages and disclaimers
        5. Provides clear rationale for escalation decisions
        
        Args:
            drift_analysis (dict, optional): Output from drift_agent containing:
                - severity_level (str): "low", "moderate", "high"
                - drift_percentages (dict): Drift values per metric
                - affected_features (list): Metrics with drift
            risk_analysis (dict, optional): Output from risk_agent containing:
                - risk_level (str): "temporary", "needs_observation", "potentially_concerning"
                - days_observed (int): Duration of pattern
                - is_worsening (bool): Whether trend is worsening
                - consistency_score (float): Pattern consistency
            context_analysis (dict, optional): Output from context_agent containing:
                - confidence_level (float): Analysis confidence
                - possible_factors (list): Contributing factors
            user_reported_symptoms (list, optional): User-reported symptoms or concerns
        
        Returns:
            Dict containing safety evaluation:
                - success (bool): Evaluation success status
                - escalation_required (bool): TRUE if professional consultation recommended
                - safety_message (str): Clear message for user with disclaimers
                - rationale (str): Explanation of why escalation is/isn't needed
                - urgency_level (str): "routine", "prompt", "urgent"
                - disclaimer (str): Legal/ethical disclaimer
                - next_steps (list): Recommended actions
                - error (str): Error message if failed
        
        Example:
            agent = SafetyAgent()
            
            # After running drift and risk agents
            safety_eval = agent.evaluate_safety(
                drift_analysis=drift_result,
                risk_analysis=risk_result
            )
            
            if safety_eval['escalation_required']:
                print(safety_eval['safety_message'])
                print(safety_eval['rationale'])
        """
        # Check if ADK runtime is ready
        if not is_adk_ready():
            # Fallback to rule-based safety checks without AI
            return self._rule_based_safety_check(
                drift_analysis=drift_analysis,
                risk_analysis=risk_analysis,
                user_reported_symptoms=user_reported_symptoms
            )
        
        # Step 1: Extract key safety indicators from agent outputs
        safety_indicators = self._extract_safety_indicators(
            drift_analysis=drift_analysis,
            risk_analysis=risk_analysis,
            context_analysis=context_analysis,
            user_reported_symptoms=user_reported_symptoms
        )
        
        # Step 2: Apply rule-based escalation triggers (immediate safety checks)
        rule_based_escalation = self._check_escalation_triggers(safety_indicators)
        
        # Step 3: Construct safety evaluation prompt for AI oversight
        prompt = self._construct_safety_prompt(
            safety_indicators=safety_indicators,
            rule_based_escalation=rule_based_escalation
        )
        
        # Step 4: Execute AI safety evaluation
        result = run_agent(prompt, self.system_instruction)
        
        if not result['success']:
            # Fallback to rule-based decision
            return self._rule_based_safety_check(
                drift_analysis=drift_analysis,
                risk_analysis=risk_analysis,
                user_reported_symptoms=user_reported_symptoms
            )
        
        # Step 5: Parse AI response and structure safety evaluation
        safety_eval = self._parse_safety_response(
            response_text=result['response'],
            rule_based_escalation=rule_based_escalation,
            safety_indicators=safety_indicators
        )
        
        # Step 6: Add standard disclaimer (always present)
        safety_eval['disclaimer'] = self._get_standard_disclaimer()
        safety_eval['success'] = True
        safety_eval['error'] = None
        
        return safety_eval
    
    def _extract_safety_indicators(
        self,
        drift_analysis: Optional[Dict[str, Any]],
        risk_analysis: Optional[Dict[str, Any]],
        context_analysis: Optional[Dict[str, Any]],
        user_reported_symptoms: Optional[List[str]]
    ) -> Dict[str, Any]:
        """
        Extract key safety indicators from agent outputs
        
        Consolidates critical information for safety evaluation:
        - Drift severity and magnitude
        - Risk level and trend direction
        - Duration and persistence
        - User-reported concerns
        
        Args:
            drift_analysis, risk_analysis, context_analysis: Agent outputs
            user_reported_symptoms: User-reported concerns
        
        Returns:
            Dict with consolidated safety indicators
        
        Logic:
            - Extract severity levels from all agents
            - Identify maximum drift percentages
            - Count affected metrics
            - Assess pattern duration
            - Flag worsening trends
        """
        indicators = {
            "max_drift_percentage": 0.0,
            "severity_level": "low",
            "risk_level": "temporary",
            "affected_metrics_count": 0,
            "days_observed": 0,
            "is_worsening": False,
            "has_symptoms": False,
            "symptom_count": 0,
            "multiple_metrics_affected": False
        }
        
        # Extract from drift analysis
        if drift_analysis and drift_analysis.get('success'):
            # Get maximum drift percentage
            drift_pcts = drift_analysis.get('drift_percentages', {})
            if drift_pcts:
                indicators['max_drift_percentage'] = max([abs(v) for v in drift_pcts.values()])
                indicators['affected_metrics_count'] = len(drift_pcts)
                indicators['multiple_metrics_affected'] = len(drift_pcts) >= 2
            
            # Get severity
            indicators['severity_level'] = drift_analysis.get('severity_level', 'low')
        
        # Extract from risk analysis
        if risk_analysis and risk_analysis.get('success'):
            indicators['risk_level'] = risk_analysis.get('risk_level', 'temporary')
            indicators['days_observed'] = risk_analysis.get('days_observed', 0)
            indicators['is_worsening'] = risk_analysis.get('is_worsening', False)
        
        # Check for user-reported symptoms
        if user_reported_symptoms and len(user_reported_symptoms) > 0:
            indicators['has_symptoms'] = True
            indicators['symptom_count'] = len(user_reported_symptoms)
        
        return indicators
    
    def _check_escalation_triggers(self, safety_indicators: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply rule-based escalation triggers for immediate safety checks
        
        These are hard-coded safety rules that don't require AI evaluation.
        If any trigger fires, escalation is automatically required.
        
        Args:
            safety_indicators (dict): Consolidated safety indicators
        
        Returns:
            Dict with escalation decision and triggered rules
        
        Escalation Triggers:
            1. Severe drift (>10%) - major deviation from baseline
            2. High risk for 7+ days - persistent concerning pattern
            3. Multiple metrics affected - correlated decline
            4. Worsening trend with potentially_concerning risk
            5. User-reported symptoms with moderate+ drift
        
        Logic:
            - Check each trigger condition
            - If ANY trigger fires, escalation is required
            - Document which triggers fired for rationale
        """
        triggered_rules = []
        escalation_required = False
        
        # Trigger 1: Severe drift (>10%)
        if safety_indicators['max_drift_percentage'] >= self.ESCALATION_TRIGGERS['severe_drift']:
            triggered_rules.append(f"Severe drift detected: {safety_indicators['max_drift_percentage']:.1f}% deviation")
            escalation_required = True
        
        # Trigger 2: High risk persisting 7+ days
        if (safety_indicators['risk_level'] == 'potentially_concerning' 
            and safety_indicators['days_observed'] >= self.ESCALATION_TRIGGERS['high_risk_days']):
            triggered_rules.append(f"Concerning pattern persisting for {safety_indicators['days_observed']} days")
            escalation_required = True
        
        # Trigger 3: Multiple metrics showing problems
        if (safety_indicators['multiple_metrics_affected'] 
            and safety_indicators['severity_level'] in ['moderate', 'high']):
            triggered_rules.append(f"{safety_indicators['affected_metrics_count']} metrics showing correlated drift")
            escalation_required = True
        
        # Trigger 4: Worsening trend with high risk
        if (safety_indicators['is_worsening'] 
            and safety_indicators['risk_level'] == 'potentially_concerning'):
            triggered_rules.append("Worsening trend with potentially concerning risk level")
            escalation_required = True
        
        # Trigger 5: User-reported symptoms with concerning drift
        if (safety_indicators['has_symptoms'] 
            and safety_indicators['severity_level'] in ['moderate', 'high']):
            triggered_rules.append(f"User-reported symptoms ({safety_indicators['symptom_count']}) alongside concerning drift")
            escalation_required = True
        
        return {
            "escalation_required": escalation_required,
            "triggered_rules": triggered_rules,
            "trigger_count": len(triggered_rules)
        }
    
    def _construct_safety_prompt(
        self,
        safety_indicators: Dict[str, Any],
        rule_based_escalation: Dict[str, Any]
    ) -> str:
        """
        Construct prompt for AI safety evaluation
        
        This prompt asks the AI to:
        - Review consolidated safety indicators
        - Verify rule-based escalation decision
        - Generate appropriate safety message
        - Provide clear rationale
        - Determine urgency level
        """
        prompt = f"""Evaluate if escalation to professional medical care is required based on these health monitoring outputs:

**Safety Indicators:**
- Maximum Drift: {safety_indicators['max_drift_percentage']:.1f}% from baseline
- Drift Severity: {safety_indicators['severity_level']}
- Risk Level: {safety_indicators['risk_level']}
- Days Observed: {safety_indicators['days_observed']}
- Trend Direction: {"Worsening" if safety_indicators['is_worsening'] else "Stable/Recovering"}
- Affected Metrics: {safety_indicators['affected_metrics_count']}
- User-Reported Symptoms: {"Yes" if safety_indicators['has_symptoms'] else "No"}

**Rule-Based Escalation Check:**
- Escalation Required: {"YES" if rule_based_escalation['escalation_required'] else "NO"}
- Triggered Safety Rules: {rule_based_escalation['trigger_count']}
"""
        
        if rule_based_escalation['triggered_rules']:
            prompt += "\nTriggered Rules:\n"
            for rule in rule_based_escalation['triggered_rules']:
                prompt += f"- {rule}\n"
        
        prompt += """
**Your Task:**

1. Verify if escalation is required (true/false)
   - If ANY rule-based trigger fired → escalation IS required
   - Consider overall pattern severity and persistence
   - Apply safety-first principle: when in doubt, escalate

2. Determine urgency level:
   - "routine": Schedule regular check-up within weeks
   - "prompt": Consult healthcare provider within days
   - "urgent": Seek immediate medical attention

3. Generate a clear safety message for the user:
   - Direct, non-technical language
   - Explain WHY professional consultation is recommended (if applicable)
   - Include reassurance that monitoring continues
   - NO medical advice or diagnosis

4. Provide rationale:
   - Explain the safety decision
   - Reference specific indicators that drove decision
   - Emphasize this is precautionary guidance, not diagnosis

**Response Format:**

Escalation Required: [true/false]

Urgency Level: [routine/prompt/urgent]

Safety Message:
[2-3 paragraph clear, direct message for user. If escalation required, explain why professional consultation is recommended. Include reassurance. NO medical advice.]

Rationale:
[Explain safety decision. Reference specific indicators. Emphasize precautionary nature.]

Next Steps:
- [Specific action 1]
- [Specific action 2]

**Critical Reminders:**
- This is safety oversight, NOT medical diagnosis
- Always err on the side of caution
- Clear disclaimers that this is not medical advice
- Professional consultation is always appropriate for health concerns"""
        
        return prompt
    
    def _parse_safety_response(
        self,
        response_text: str,
        rule_based_escalation: Dict[str, Any],
        safety_indicators: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Parse AI safety evaluation response
        
        Extracts:
        - escalation_required (bool)
        - safety_message (str)
        - rationale (str)
        - urgency_level (str)
        - next_steps (list)
        
        Args:
            response_text (str): Raw AI response
            rule_based_escalation (dict): Rule-based decision
            safety_indicators (dict): Input indicators
        
        Returns:
            Dict: Structured safety evaluation
        """
        safety_eval = {
            "escalation_required": rule_based_escalation['escalation_required'],  # Default to rule-based
            "safety_message": "",
            "rationale": "",
            "urgency_level": "routine",
            "next_steps": []
        }
        
        try:
            # Extract escalation decision
            response_lower = response_text.lower()
            if "escalation required: true" in response_lower or "escalation required: yes" in response_lower:
                safety_eval['escalation_required'] = True
            elif "escalation required: false" in response_lower or "escalation required: no" in response_lower:
                # Only override to False if no rules were triggered
                if not rule_based_escalation['escalation_required']:
                    safety_eval['escalation_required'] = False
            
            # Extract urgency level
            if "urgent" in response_lower and "urgency level: urgent" in response_lower:
                safety_eval['urgency_level'] = "urgent"
            elif "prompt" in response_lower and "urgency level: prompt" in response_lower:
                safety_eval['urgency_level'] = "prompt"
            else:
                safety_eval['urgency_level'] = "routine"
            
            # Extract safety message
            if "Safety Message:" in response_text:
                message_section = response_text.split("Safety Message:")[1].split("\n\n")[0]
                safety_eval['safety_message'] = message_section.strip()
            else:
                # Use first substantial paragraph
                paragraphs = [p.strip() for p in response_text.split("\n\n") if len(p.strip()) > 100]
                safety_eval['safety_message'] = paragraphs[0] if paragraphs else "Continue monitoring your health patterns."
            
            # Extract rationale
            if "Rationale:" in response_text:
                rationale_section = response_text.split("Rationale:")[1].split("\n\n")[0]
                safety_eval['rationale'] = rationale_section.strip()
            else:
                # Generate rationale from indicators
                if safety_eval['escalation_required']:
                    safety_eval['rationale'] = f"Escalation recommended due to: {', '.join(rule_based_escalation['triggered_rules'])}"
                else:
                    safety_eval['rationale'] = "Pattern is within monitoring range. No immediate escalation needed."
            
            # Extract next steps
            if "Next Steps:" in response_text:
                steps_section = response_text.split("Next Steps:")[1].split("\n\n")[0]
                next_steps = [
                    line.strip().lstrip('-•*').strip() 
                    for line in steps_section.split("\n") 
                    if line.strip() and (line.strip().startswith('-') or line.strip().startswith('•') or line.strip().startswith('*'))
                ]
                safety_eval['next_steps'] = next_steps[:3]
            
            # Ensure we have next steps
            if not safety_eval['next_steps']:
                if safety_eval['escalation_required']:
                    safety_eval['next_steps'] = [
                        "Consult with your healthcare provider about these patterns",
                        "Continue daily health monitoring",
                        "Document any symptoms or changes you notice"
                    ]
                else:
                    safety_eval['next_steps'] = [
                        "Continue daily health monitoring",
                        "Track any new patterns or changes",
                        "Consult healthcare provider if patterns persist or worsen"
                    ]
        
        except Exception as e:
            # Fallback to safe defaults
            if rule_based_escalation['escalation_required']:
                safety_eval['escalation_required'] = True
                safety_eval['safety_message'] = "Based on your health monitoring patterns, we recommend consulting with a healthcare professional for evaluation."
                safety_eval['rationale'] = "Safety triggers detected in monitoring data."
        
        return safety_eval
    
    def _rule_based_safety_check(
        self,
        drift_analysis: Optional[Dict[str, Any]],
        risk_analysis: Optional[Dict[str, Any]],
        user_reported_symptoms: Optional[List[str]]
    ) -> Dict[str, Any]:
        """
        Fallback rule-based safety check when AI is unavailable
        
        Applies conservative safety rules without AI assistance.
        This ensures safety evaluation always works even if API fails.
        
        Args:
            drift_analysis, risk_analysis: Agent outputs
            user_reported_symptoms: User concerns
        
        Returns:
            Dict: Basic safety evaluation based on rules only
        """
        indicators = self._extract_safety_indicators(
            drift_analysis=drift_analysis,
            risk_analysis=risk_analysis,
            context_analysis=None,
            user_reported_symptoms=user_reported_symptoms
        )
        
        rule_check = self._check_escalation_triggers(indicators)
        
        # Generate basic safety message
        if rule_check['escalation_required']:
            safety_message = (
                "Based on your health monitoring patterns, we recommend consulting with a healthcare "
                "professional for evaluation. This is a precautionary recommendation based on detected "
                "patterns in your data. Continue monitoring and document any symptoms or changes."
            )
            urgency = "prompt" if indicators['max_drift_percentage'] > 15 else "routine"
            next_steps = [
                "Schedule consultation with your healthcare provider",
                "Continue daily health monitoring",
                "Document symptoms and pattern changes"
            ]
        else:
            safety_message = (
                "Your health monitoring patterns are within acceptable monitoring range. Continue your "
                "daily monitoring routine. If you notice any new concerning changes or symptoms, consult "
                "with a healthcare professional."
            )
            urgency = "routine"
            next_steps = [
                "Continue daily health monitoring",
                "Track any changes in patterns",
                "Maintain healthy lifestyle habits"
            ]
        
        return {
            "success": True,
            "error": None,
            "escalation_required": rule_check['escalation_required'],
            "safety_message": safety_message,
            "rationale": "Safety evaluation based on rule-based triggers: " + (
                ", ".join(rule_check['triggered_rules']) if rule_check['triggered_rules'] 
                else "No escalation triggers detected"
            ),
            "urgency_level": urgency,
            "disclaimer": self._get_standard_disclaimer(),
            "next_steps": next_steps
        }
    
    def _get_standard_disclaimer(self) -> str:
        """
        Get standard safety disclaimer
        
        This disclaimer must always be included in safety evaluations
        to ensure users understand limitations of AI health monitoring.
        
        Returns:
            str: Legal/ethical disclaimer text
        """
        return (
            "IMPORTANT DISCLAIMER: This health monitoring system is not a medical device and does not "
            "provide medical diagnosis, advice, or treatment. All insights are for informational and "
            "wellness monitoring purposes only. This system supplements but does not replace professional "
            "medical care. Always consult qualified healthcare professionals for medical concerns, "
            "symptoms, or health decisions. In case of medical emergency, contact emergency services immediately."
        )


# ========================================
# CONVENIENCE FUNCTIONS
# ========================================

def evaluate_pattern_safety(
    drift_analysis: Dict[str, Any],
    risk_analysis: Dict[str, Any],
    user_symptoms: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Convenience function for safety evaluation
    
    Args:
        drift_analysis (dict): Output from drift_agent
        risk_analysis (dict): Output from risk_agent
        user_symptoms (list, optional): User-reported symptoms
    
    Returns:
        Dict: Safety evaluation with escalation_required, safety_message, rationale
    
    Example:
        from agents.safety_agent import evaluate_pattern_safety
        
        # After running drift and risk agents
        safety = evaluate_pattern_safety(
            drift_analysis=drift_result,
            risk_analysis=risk_result,
            user_symptoms=["fatigue", "dizziness"]
        )
        
        if safety['escalation_required']:
            print(safety['safety_message'])
            print(f"Urgency: {safety['urgency_level']}")
    """
    agent = SafetyAgent()
    return agent.evaluate_safety(
        drift_analysis=drift_analysis,
        risk_analysis=risk_analysis,
        user_reported_symptoms=user_symptoms
    )
