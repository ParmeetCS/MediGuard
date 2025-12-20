"""
Care Agent - MediGuard Drift AI
Practical lifestyle guidance generator for health drift patterns

This agent provides actionable, non-medical wellness suggestions based on
detected health patterns, focusing on practical lifestyle adjustments that
users can implement immediately.

Purpose:
- Generate practical lifestyle suggestions
- Provide actionable guidance without medical claims
- Adapt tone based on severity of patterns
- Suggest follow-up monitoring strategies
"""

from typing import Dict, List, Optional, Any
from agents.adk_runtime import run_agent, is_adk_ready


class CareAgent:
    """
    AI Agent for generating practical lifestyle guidance
    
    This agent synthesizes insights from drift, context, and risk agents
    to provide user-friendly, actionable wellness suggestions.
    
    Key Capabilities:
    - Practical lifestyle recommendations (rest, hydration, activity, etc.)
    - Tone adaptation based on pattern severity
    - Follow-up monitoring suggestions
    - Non-medical, implementable guidance
    
    CRITICAL: This agent does NOT provide medical advice.
    All suggestions are general wellness practices.
    """
    
    def __init__(self):
        """Initialize the Care Agent"""
        self.agent_name = "Wellness Guidance"
        
        # System instruction enforces practical, non-medical guidance
        self.system_instruction = """You are a friendly, caring local doctor talking to a patient in your office. Use simple, everyday language that anyone can understand - no medical jargon, no technical terms, no complicated numbers.

Your role:
- Talk like you're having a friendly conversation over tea, not writing a medical report
- Use simple words: instead of "mobility" say "how well you can move around"
- Instead of "stability score 0.85" say "your balance is pretty good"
- Explain things the way you'd explain to your grandmother or neighbor
- Be warm, caring, and reassuring
- Give practical tips anyone can do at home

How to talk:
- "I noticed you're moving a bit slower than usual" NOT "Movement speed decreased 5.2%"
- "Your balance seems a little off lately" NOT "Stability metric shows downward drift"
- "You might want to get more sleep" NOT "Sleep optimization recommended for metric improvement"
- "Try walking for 15 minutes after lunch" NOT "Implement moderate aerobic activity protocol"
- "This could be because you've been stressed" NOT "Stress levels correlate with performance degradation"

What to suggest:
- Simple home remedies: drink more water, get better sleep, take short walks
- Easy habits: stretch in the morning, take breaks when sitting
- Practical tips: keep a glass of water on your desk, set a bedtime alarm
- When to rest and when to move
- Signs to watch for

Critical rules:
1. NO technical terms (no "metrics", "baseline", "threshold", "drift percentage")
2. NO decimal numbers (say "pretty good" not "0.87")
3. NO medical jargon (say "balance" not "postural stability")
4. Talk like a caring friend, not a computer
5. Keep it simple - 6th grade reading level
6. Be reassuring but honest
7. Always say "talk to your doctor if you're worried"

Response format:
- Provide 4-6 detailed recommendations (not just a short list)
- Each recommendation should be 3-5 sentences explaining what to do, why it helps, and how to start
- Include a warm opening that acknowledges the user's situation
- Close with encouragement and reassurance
- Use paragraphs for explanation sections, lists for actionable steps within each recommendation

Tone guidelines:
- Reassuring: For mild patterns - emphasize gentle adjustments and monitoring
- Cautious: For moderate patterns - balance practical guidance with professional consultation reminders
- Supportive: ALWAYS maintain encouraging, empowering, non-alarmist approach

Remember: You are helping someone take care of themselves. Be thorough, be kind, be specific. Give them the information they need to feel confident and supported."""
        
        # Guidance categories with example suggestions
        self.GUIDANCE_CATEGORIES = {
            "rest": ["Aim for 7-9 hours of sleep", "Take regular breaks during work", "Practice relaxation before bed"],
            "hydration": ["Drink water throughout the day", "Set hydration reminders", "Keep water bottle accessible"],
            "posture": ["Check posture every hour", "Stretch shoulders and neck", "Adjust workspace ergonomics"],
            "activity": ["Take short walks", "Light stretching exercises", "Balance practice"],
            "stress": ["Deep breathing exercises", "Scheduled breaks", "Time management strategies"],
            "monitoring": ["Track daily patterns", "Journal changes", "Consistent measurement times"]
        }
    
    def generate_guidance(
        self,
        drift_analysis: Optional[Dict[str, Any]] = None,
        context_analysis: Optional[Dict[str, Any]] = None,
        risk_analysis: Optional[Dict[str, Any]] = None,
        user_profile: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate practical lifestyle guidance based on agent outputs
        
        This method:
        1. Accepts outputs from drift, context, and risk agents
        2. Synthesizes insights to understand user's situation
        3. Generates specific, actionable wellness suggestions
        4. Adapts tone based on pattern severity
        5. Suggests appropriate follow-up monitoring
        
        Args:
            drift_analysis (dict, optional): Output from drift_agent containing:
                - severity_level (str): "low", "moderate", "high"
                - affected_features (list): Metrics with drift
                - explanation (str): Drift explanation
            context_analysis (dict, optional): Output from context_agent containing:
                - possible_factors (list): Contributing factors
                - contextual_explanation (str): Context-aware insights
            risk_analysis (dict, optional): Output from risk_agent containing:
                - risk_level (str): "temporary", "needs_observation", "potentially_concerning"
                - trend_description (str): Trend over time
            user_profile (dict, optional): User information containing:
                - age (int)
                - lifestyle (str)
                - Any other context from profile or context inputs
        
        Returns:
            Dict containing practical guidance:
                - success (bool): Generation success status
                - guidance_list (list): Specific actionable suggestions
                - tone (str): "reassuring" or "cautious"
                - follow_up_suggestion (str): Monitoring/follow-up guidance
                - rationale (str): Why these suggestions are appropriate
                - disclaimer (str): Non-medical guidance disclaimer
                - error (str): Error message if failed
        
        Example:
            agent = CareAgent()
            
            guidance = agent.generate_guidance(
                drift_analysis=drift_result,
                context_analysis=context_result,
                risk_analysis=risk_result,
                user_profile={"age": 45, "lifestyle": "working professional"}
            )
            
            print(f"Tone: {guidance['tone']}")
            for suggestion in guidance['guidance_list']:
                print(f"- {suggestion}")
        """
        # Check if ADK runtime is ready
        if not is_adk_ready():
            # Fallback to rule-based guidance
            return self._rule_based_guidance(
                drift_analysis=drift_analysis,
                risk_analysis=risk_analysis
            )
        
        # Step 1: Synthesize insights from all agent outputs
        synthesis = self._synthesize_agent_insights(
            drift_analysis=drift_analysis,
            context_analysis=context_analysis,
            risk_analysis=risk_analysis,
            user_profile=user_profile
        )
        
        # Step 2: Determine appropriate tone based on severity
        tone = self._determine_tone(synthesis)
        
        # Step 3: Construct guidance generation prompt
        prompt = self._construct_guidance_prompt(
            synthesis=synthesis,
            tone=tone
        )
        
        # Step 4: Execute AI guidance generation
        result = run_agent(prompt, self.system_instruction)
        
        if not result['success']:
            # Fallback to rule-based guidance
            return self._rule_based_guidance(
                drift_analysis=drift_analysis,
                risk_analysis=risk_analysis
            )
        
        # Step 5: Parse AI response and structure guidance
        guidance = self._parse_guidance_response(
            response_text=result['response'],
            tone=tone,
            synthesis=synthesis
        )
        
        # Step 6: Add standard elements
        guidance['success'] = True
        guidance['error'] = None
        guidance['disclaimer'] = self._get_guidance_disclaimer()
        
        return guidance
    
    def _synthesize_agent_insights(
        self,
        drift_analysis: Optional[Dict[str, Any]],
        context_analysis: Optional[Dict[str, Any]],
        risk_analysis: Optional[Dict[str, Any]],
        user_profile: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Synthesize insights from all agent outputs
        
        Consolidates information to understand:
        - What changed (drift)
        - Why it might have happened (context)
        - How concerning it is (risk)
        - User's situation (profile)
        
        Args:
            drift_analysis, context_analysis, risk_analysis, user_profile: Agent outputs
        
        Returns:
            Dict with synthesized insights for guidance generation
        
        Logic:
            - Extract severity levels
            - Identify contributing factors
            - Determine pattern duration
            - Note user context (age, lifestyle, stress, sleep)
            - Create comprehensive picture for guidance
        """
        synthesis = {
            "severity_level": "low",
            "risk_level": "temporary",
            "affected_metrics": [],
            "contributing_factors": [],
            "user_age": None,
            "user_lifestyle": None,
            "sleep_hours": None,
            "stress_level": None,
            "days_observed": 0,
            "is_worsening": False,
            "has_context": False
        }
        
        # Extract from drift analysis
        if drift_analysis and drift_analysis.get('success'):
            synthesis['severity_level'] = drift_analysis.get('severity_level', 'low')
            synthesis['affected_metrics'] = drift_analysis.get('affected_features', [])
        
        # Extract from context analysis
        if context_analysis and context_analysis.get('success'):
            synthesis['contributing_factors'] = context_analysis.get('possible_factors', [])
            synthesis['has_context'] = True
        
        # Extract from risk analysis
        if risk_analysis and risk_analysis.get('success'):
            synthesis['risk_level'] = risk_analysis.get('risk_level', 'temporary')
            synthesis['days_observed'] = risk_analysis.get('days_observed', 0)
            synthesis['is_worsening'] = risk_analysis.get('is_worsening', False)
        
        # Extract from user profile
        if user_profile:
            synthesis['user_age'] = user_profile.get('age')
            synthesis['user_lifestyle'] = user_profile.get('lifestyle')
            synthesis['sleep_hours'] = user_profile.get('sleep_hours')
            synthesis['stress_level'] = user_profile.get('stress_level')
        
        return synthesis
    
    def _determine_tone(self, synthesis: Dict[str, Any]) -> str:
        """
        Determine appropriate tone based on pattern severity
        
        Tone Selection:
        - Reassuring: Mild patterns, temporary risk, low severity
        - Cautious: Moderate/high severity, concerning risk, worsening trends
        
        Args:
            synthesis (dict): Synthesized insights
        
        Returns:
            str: "reassuring" or "cautious"
        
        Logic:
            - Check severity level (low → reassuring)
            - Check risk level (potentially_concerning → cautious)
            - Check trend (worsening → cautious)
            - Default to cautious when uncertain
        """
        # Cautious tone for concerning patterns
        if synthesis['severity_level'] in ['moderate', 'high']:
            return "cautious"
        
        if synthesis['risk_level'] == 'potentially_concerning':
            return "cautious"
        
        if synthesis['is_worsening']:
            return "cautious"
        
        # Reassuring tone for mild, temporary patterns
        return "reassuring"
    
    def _construct_guidance_prompt(
        self,
        synthesis: Dict[str, Any],
        tone: str
    ) -> str:
        """
        Construct prompt for practical guidance generation
        
        This prompt provides:
        - Synthesized insights from all agents
        - User context information
        - Required tone
        - Requests specific, actionable suggestions
        """
        prompt = f"""Generate practical lifestyle guidance based on these health monitoring insights:

**Pattern Summary:**
- Severity: {synthesis['severity_level']}
- Risk Level: {synthesis['risk_level']}
- Days Observed: {synthesis['days_observed']}
- Trend: {"Worsening" if synthesis['is_worsening'] else "Stable/Improving"}
- Affected Metrics: {', '.join(synthesis['affected_metrics']) if synthesis['affected_metrics'] else 'None'}

"""
        
        # Add contributing factors if available
        if synthesis['contributing_factors']:
            prompt += "**Identified Contributing Factors:**\n"
            for factor in synthesis['contributing_factors'][:3]:
                prompt += f"- {factor}\n"
            prompt += "\n"
        
        # Add user context if available
        if synthesis['user_age'] or synthesis['user_lifestyle']:
            prompt += "**User Context:**\n"
            if synthesis['user_age']:
                prompt += f"- Age: {synthesis['user_age']}\n"
            if synthesis['user_lifestyle']:
                prompt += f"- Lifestyle: {synthesis['user_lifestyle']}\n"
            if synthesis['sleep_hours']:
                prompt += f"- Sleep: {synthesis['sleep_hours']} hours/night\n"
            if synthesis['stress_level']:
                prompt += f"- Stress: {synthesis['stress_level']}\n"
            prompt += "\n"
        
        prompt += f"""**Required Tone:** {tone.upper()}

**Your Task:**

Please provide comprehensive, detailed wellness guidance that truly helps the user take action:

1. **Warm Opening** (2-3 sentences): Begin by acknowledging what you understand about their situation with empathy and support. Help them feel heard and understood.

2. **Detailed Wellness Recommendations** (5-7 recommendations, each with 3-5 sentences):
   
   For EACH recommendation, provide:
   - **What to do**: Specific, clear action (not vague)
   - **Why it matters**: Thorough explanation of how this helps (2-3 sentences)
   - **How to start**: Practical first steps that feel achievable
   - **Additional context**: Tips, timing, or modifications
   
   Cover these categories based on the situation:
   - Rest and recovery: Specific sleep schedules, rest periods, relaxation techniques
   - Hydration: Detailed water intake strategies with timing and amounts
   - Posture and ergonomics: Complete workspace setup, stretching routines with instructions
   - Light activity: Specific walking routines, gentle movement exercises, balance practices
   - Stress management: Detailed breathing exercises, time management strategies, break schedules
   - Monitoring: Clear tracking methods, journaling approaches, measurement timing
   - Lifestyle adjustments: Routine changes, environmental factors, habit formation
   
   Examples of GOOD detailed recommendations:
   ✓ "Focus on consistent sleep timing by going to bed at 10:30 PM and waking at 6:30 AM every day, even on weekends. This helps regulate your body's natural rhythms, which research suggests may support better balance and coordination. Start tonight by setting two alarms - one at 10 PM as a wind-down reminder, and one at 10:30 PM for lights out. Create a calming pre-bed routine like reading for 20 minutes or gentle stretching to help your mind prepare for rest."
   
   ✗ "Get more sleep and rest better"

3. **Follow-Up Monitoring Guidance** (4-5 sentences): Provide DETAILED instructions on:
   - Exactly how to track progress (specific methods, tools, or journals)
   - When to reassess (specific timeline)
   - What specific changes to watch for (be concrete)
   - How to know if adjustments are helping
   - When to seek additional support

4. **Encouraging Rationale** (3-4 sentences): Explain thoroughly:
   - Why these specific suggestions connect to their pattern
   - How the recommendations work together as a holistic approach
   - What positive changes they might notice over time
   - Affirmation of their proactive approach to wellbeing

5. **Supportive Closing** (2-3 sentences): End with genuine encouragement that helps them feel capable, supported, and motivated to take action.

**Writing Style:**
- Use flowing paragraphs for explanations, not just bullet lists
- Write in a warm, conversational tone like talking to a friend
- Be THOROUGH and DETAILED - users deserve complete guidance
- Include specific numbers, times, durations, and frequencies
- Use "you" language to make it personal and relatable
- Show empathy and understanding throughout
- Make every recommendation feel achievable and non-overwhelming

**Critical Reminders:**
- NO medical advice, diagnosis, or treatment recommendations
- NO medications, supplements, or medical interventions
- Focus on safe, general wellness practices appropriate for most adults
- Be specific and actionable in every recommendation
- Explain the why behind each suggestion to build trust and understanding
- Maintain supportive, encouraging tone throughout"""
        
        return prompt
    
    def _parse_guidance_response(
        self,
        response_text: str,
        tone: str,
        synthesis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Parse AI guidance response into structured format
        
        Extracts:
        - guidance_list (list of specific suggestions)
        - follow_up_suggestion (str)
        - rationale (str)
        - tone (str)
        
        Args:
            response_text (str): Raw AI response
            tone (str): Determined tone
            synthesis (dict): Input synthesis
        
        Returns:
            Dict: Structured guidance output
        """
        guidance = {
            "guidance_list": [],
            "tone": tone,
            "follow_up_suggestion": "",
            "rationale": ""
        }
        
        try:
            # Extract guidance suggestions
            if "Guidance Suggestions:" in response_text:
                suggestions_section = response_text.split("Guidance Suggestions:")[1].split("\n\n")[0]
                suggestions = [
                    line.strip().lstrip('-•*').strip() 
                    for line in suggestions_section.split("\n") 
                    if line.strip() and (line.strip().startswith('-') or line.strip().startswith('•') or line.strip().startswith('*'))
                ]
                guidance['guidance_list'] = suggestions[:6]  # Limit to 6
            
            # Extract follow-up monitoring
            if "Follow-Up Monitoring:" in response_text or "Follow-up Monitoring:" in response_text:
                followup_keyword = "Follow-Up Monitoring:" if "Follow-Up Monitoring:" in response_text else "Follow-up Monitoring:"
                followup_section = response_text.split(followup_keyword)[1].split("\n\n")[0]
                guidance['follow_up_suggestion'] = followup_section.strip()
            
            # Extract rationale
            if "Rationale:" in response_text:
                rationale_section = response_text.split("Rationale:")[1].split("\n\n")[0]
                guidance['rationale'] = rationale_section.strip()
            
            # Ensure we have minimum guidance
            if not guidance['guidance_list']:
                # Generate basic guidance based on synthesis
                guidance['guidance_list'] = self._generate_basic_guidance(synthesis)
            
            if not guidance['follow_up_suggestion']:
                guidance['follow_up_suggestion'] = "Continue daily monitoring and track any changes in your patterns over the next week."
            
            if not guidance['rationale']:
                guidance['rationale'] = "These suggestions focus on general wellness practices that support overall health."
        
        except Exception as e:
            # Fallback to basic guidance
            guidance['guidance_list'] = self._generate_basic_guidance(synthesis)
            guidance['follow_up_suggestion'] = "Monitor your patterns and consult healthcare provider if concerns persist."
            guidance['rationale'] = "General wellness suggestions based on monitoring patterns."
        
        return guidance
    
    def _generate_basic_guidance(self, synthesis: Dict[str, Any]) -> List[str]:
        """
        Generate basic guidance when AI parsing fails
        
        Provides safe, general wellness suggestions based on severity.
        
        Args:
            synthesis (dict): Synthesized insights
        
        Returns:
            List of basic wellness suggestions
        """
        basic_suggestions = [
            "Aim for 7-9 hours of quality sleep each night",
            "Stay well-hydrated by drinking water throughout the day",
            "Take short movement breaks every hour during sedentary activities"
        ]
        
        # Add severity-appropriate suggestions
        if synthesis['severity_level'] in ['moderate', 'high']:
            basic_suggestions.extend([
                "Monitor your patterns daily and document any changes",
                "Consider discussing these patterns with your healthcare provider"
            ])
        else:
            basic_suggestions.extend([
                "Continue your daily monitoring routine",
                "Maintain consistent healthy lifestyle habits"
            ])
        
        return basic_suggestions
    
    def _rule_based_guidance(
        self,
        drift_analysis: Optional[Dict[str, Any]],
        risk_analysis: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Fallback rule-based guidance when AI is unavailable
        
        Provides safe, general wellness suggestions without AI assistance.
        
        Args:
            drift_analysis, risk_analysis: Agent outputs
        
        Returns:
            Dict: Basic guidance structure
        """
        # Determine severity
        severity = "low"
        risk_level = "temporary"
        
        if drift_analysis and drift_analysis.get('success'):
            severity = drift_analysis.get('severity_level', 'low')
        
        if risk_analysis and risk_analysis.get('success'):
            risk_level = risk_analysis.get('risk_level', 'temporary')
        
        # Determine tone
        tone = "cautious" if severity in ['moderate', 'high'] or risk_level == 'potentially_concerning' else "reassuring"
        
        # Generate basic suggestions
        suggestions = [
            "Prioritize 7-9 hours of quality sleep each night",
            "Stay well-hydrated throughout the day",
            "Take regular breaks to stand, stretch, and move",
            "Practice stress management through deep breathing or relaxation"
        ]
        
        if tone == "cautious":
            suggestions.extend([
                "Monitor your patterns closely and document any changes",
                "Consider discussing these patterns with a healthcare provider"
            ])
        else:
            suggestions.append("Continue consistent daily health monitoring")
        
        follow_up = (
            "Track your daily patterns and reassess in one week. "
            "If patterns persist or worsen, consult with a healthcare professional."
        )
        
        rationale = (
            "These are general wellness practices that support overall health. "
            "They focus on foundational lifestyle factors: rest, hydration, movement, and stress management."
        )
        
        return {
            "success": True,
            "error": None,
            "guidance_list": suggestions,
            "tone": tone,
            "follow_up_suggestion": follow_up,
            "rationale": rationale,
            "disclaimer": self._get_guidance_disclaimer()
        }
    
    def _get_guidance_disclaimer(self) -> str:
        """
        Get standard guidance disclaimer
        
        This disclaimer clarifies that suggestions are wellness practices,
        not medical advice.
        
        Returns:
            str: Guidance disclaimer text
        """
        return (
            "These suggestions are general wellness practices and do not constitute medical advice. "
            "They are intended to support overall health and wellbeing. Always consult qualified "
            "healthcare professionals for medical concerns or before making significant lifestyle changes."
        )


# ========================================
# CONVENIENCE FUNCTIONS
# ========================================

def get_wellness_guidance(
    drift_analysis: Dict[str, Any],
    context_analysis: Optional[Dict[str, Any]] = None,
    risk_analysis: Optional[Dict[str, Any]] = None,
    user_profile: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Convenience function for wellness guidance generation
    
    Args:
        drift_analysis (dict): Output from drift_agent
        context_analysis (dict, optional): Output from context_agent
        risk_analysis (dict, optional): Output from risk_agent
        user_profile (dict, optional): User profile information
    
    Returns:
        Dict: Practical guidance with suggestions, tone, follow-up
    
    Example:
        from agents.care_agent import get_wellness_guidance
        
        guidance = get_wellness_guidance(
            drift_analysis=drift_result,
            context_analysis=context_result,
            risk_analysis=risk_result,
            user_profile={"age": 45, "lifestyle": "working professional"}
        )
        
        print(f"Tone: {guidance['tone']}")
        print("\nSuggestions:")
        for suggestion in guidance['guidance_list']:
            print(f"  • {suggestion}")
        print(f"\nFollow-up: {guidance['follow_up_suggestion']}")
    """
    agent = CareAgent()
    return agent.generate_guidance(
        drift_analysis=drift_analysis,
        context_analysis=context_analysis,
        risk_analysis=risk_analysis,
        user_profile=user_profile
    )
