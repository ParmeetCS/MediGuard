"""
AI Agent Orchestrator - MediGuard Drift AI
Central coordination system for the 5-agent ADK pipeline

This is the ADK brain that orchestrates all agents in the correct order,
passing structured outputs between agents to create a comprehensive
health drift analysis.

Agent Execution Order (CRITICAL):
1. drift_agent → Detects WHAT changed (numerical drift detection)
2. context_agent → Explains WHY it happened (lifestyle factors)
3. risk_agent → Evaluates HOW CONCERNING (temporal risk assessment)
4. safety_agent → Decides IF ESCALATION needed (ethical guardrail)
5. care_agent → Provides ACTIONABLE GUIDANCE (user-visible value)
"""

from typing import Dict, List, Optional, Any
from agents.adk_runtime import is_adk_ready
from agents.drift_agent import DriftAgent
from agents.context_agent import ContextAgent
from agents.risk_agent import RiskAgent
from agents.safety_agent import SafetyAgent
from agents.care_agent import CareAgent


class HealthDriftOrchestrator:
    """
    Central orchestrator for the 5-agent health drift analysis pipeline
    
    This orchestrator:
    - Executes agents in the correct dependency order
    - Passes structured outputs between agents
    - Maintains session context throughout pipeline
    - Consolidates results into unified response
    - Handles errors gracefully with fallbacks
    
    Pipeline Flow:
    1. drift_agent: Analyzes numerical feature drift in health metrics
    2. context_agent: Uses drift results + user context to explain factors
    3. risk_agent: Uses drift history to assess temporal risk
    4. safety_agent: Reviews all outputs to determine escalation need
    5. care_agent: Synthesizes insights to generate practical guidance
    """
    
    def __init__(self):
        """Initialize the orchestrator with all 5 agents"""
        # Initialize all agents
        self.drift_agent = DriftAgent()
        self.context_agent = ContextAgent()
        self.risk_agent = RiskAgent()
        self.safety_agent = SafetyAgent()
        self.care_agent = CareAgent()
        
        # Track pipeline state
        self.pipeline_name = "Health Drift Analysis Pipeline"
        self.agent_count = 5
    
    def analyze_health_drift_comprehensive(
        self,
        metric_name: str,
        baseline_value: float,
        recent_value: float,
        drift_history: Optional[List[Dict[str, Any]]] = None,
        user_profile: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None,
        user_symptoms: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Execute complete 5-agent pipeline for comprehensive health drift analysis
        
        This method orchestrates all agents in sequence, passing outputs between
        them to create a holistic analysis from detection through actionable guidance.
        
        Args:
            metric_name (str): Name of health metric (e.g., "stability", "mobility")
            baseline_value (float): Initial baseline measurement
            recent_value (float): Current/recent measurement
            drift_history (list, optional): Multi-day drift data for risk analysis:
                [{"day": 1, "value": 91.5, "drift_percentage": -0.5}, ...]
            user_profile (dict, optional): User information:
                {"age": 45, "lifestyle": "working professional", ...}
            user_id (str, optional): User ID for fetching Supabase context
            user_symptoms (list, optional): User-reported symptoms
        
        Returns:
            Dict containing consolidated analysis:
                - success (bool): Overall pipeline success
                - drift_summary (dict): Output from drift_agent
                - contextual_explanation (dict): Output from context_agent
                - risk_assessment (dict): Output from risk_agent
                - safety_notice (dict): Output from safety_agent
                - care_guidance (dict): Output from care_agent
                - pipeline_metadata (dict): Execution details
                - error (str): Error message if pipeline failed
        
        Example:
            orchestrator = HealthDriftOrchestrator()
            
            result = orchestrator.analyze_health_drift_comprehensive(
                metric_name="stability",
                baseline_value=92.0,
                recent_value=87.5,
                drift_history=[...],
                user_profile={"age": 45, "lifestyle": "working professional"},
                user_id="user-123"
            )
            
            # Access agent outputs
            print(result['drift_summary']['severity_level'])
            print(result['contextual_explanation']['possible_factors'])
            print(result['risk_assessment']['risk_level'])
            print(result['safety_notice']['escalation_required'])
            print(result['care_guidance']['guidance_list'])
        """
        # Initialize consolidated response
        consolidated_response = {
            "success": False,
            "drift_summary": {},
            "contextual_explanation": {},
            "risk_assessment": {},
            "safety_notice": {},
            "care_guidance": {},
            "pipeline_metadata": {
                "agents_executed": 0,
                "agents_successful": 0,
                "execution_order": []
            },
            "error": None
        }
        
        # Check if ADK runtime is ready
        if not is_adk_ready():
            consolidated_response['error'] = "ADK Runtime not configured. Please set GOOGLE_API_KEY in .env file."
            return consolidated_response
        
        try:
            # Calculate drift percentage for agents
            drift_percentage = ((recent_value - baseline_value) / baseline_value) * 100
            
            # ========================================
            # AGENT 1: DRIFT AGENT
            # Detects WHAT changed through numerical feature drift detection
            # ========================================
            
            consolidated_response['pipeline_metadata']['execution_order'].append("drift_agent")
            consolidated_response['pipeline_metadata']['agents_executed'] += 1
            
            # Execute drift analysis
            drift_result = self.drift_agent.analyze_drift(
                metric_name=metric_name,
                baseline_value=baseline_value,
                recent_value=recent_value,
                drift_percentage=drift_percentage,
                days_observed=len(drift_history) if drift_history else 1,
                additional_context=user_profile
            )
            
            # Store drift analysis output
            consolidated_response['drift_summary'] = drift_result
            
            if drift_result.get('success'):
                consolidated_response['pipeline_metadata']['agents_successful'] += 1
            
            # ========================================
            # AGENT 2: CONTEXT AGENT
            # Explains WHY changes might have occurred based on user context
            # ========================================
            
            consolidated_response['pipeline_metadata']['execution_order'].append("context_agent")
            consolidated_response['pipeline_metadata']['agents_executed'] += 1
            
            # Execute context analysis (uses drift results + user context)
            context_result = self.context_agent.analyze_with_context(
                drift_analysis=drift_result,
                user_profile=user_profile or {},
                user_id=user_id or ""
            )
            
            # Store context analysis output
            consolidated_response['contextual_explanation'] = context_result
            
            if context_result.get('success'):
                consolidated_response['pipeline_metadata']['agents_successful'] += 1
            
            # ========================================
            # AGENT 3: RISK AGENT
            # Evaluates HOW CONCERNING the pattern is over time
            # ========================================
            
            consolidated_response['pipeline_metadata']['execution_order'].append("risk_agent")
            consolidated_response['pipeline_metadata']['agents_executed'] += 1
            
            # Execute risk assessment (uses drift history for temporal analysis)
            if drift_history and len(drift_history) >= 2:
                risk_result = self.risk_agent.analyze_risk_over_time(
                    drift_history=drift_history,
                    metric_name=metric_name,
                    baseline_value=baseline_value,
                    user_context=user_profile
                )
            else:
                # Fallback: Single-point risk assessment
                risk_result = {
                    "success": True,
                    "risk_level": "temporary",  # Default for single measurement
                    "trend_description": "Single measurement - trend not yet established",
                    "confidence_score": 0.3,  # Low confidence with limited data
                    "reasoning": "Risk assessment requires multiple days of data for accurate evaluation.",
                    "days_observed": 1,
                    "consistency_score": 0.0,
                    "is_worsening": False,
                    "recommendations": ["Continue daily monitoring to establish trend"]
                }
            
            # Store risk assessment output
            consolidated_response['risk_assessment'] = risk_result
            
            if risk_result.get('success'):
                consolidated_response['pipeline_metadata']['agents_successful'] += 1
            
            # ========================================
            # AGENT 4: SAFETY AGENT
            # Decides IF ESCALATION to professional care is needed (ethical guardrail)
            # ========================================
            
            consolidated_response['pipeline_metadata']['execution_order'].append("safety_agent")
            consolidated_response['pipeline_metadata']['agents_executed'] += 1
            
            # Execute safety evaluation (reviews all prior agent outputs)
            safety_result = self.safety_agent.evaluate_safety(
                drift_analysis=drift_result,
                risk_analysis=risk_result,
                context_analysis=context_result,
                user_reported_symptoms=user_symptoms
            )
            
            # Store safety evaluation output
            consolidated_response['safety_notice'] = safety_result
            
            if safety_result.get('success'):
                consolidated_response['pipeline_metadata']['agents_successful'] += 1
            
            # ========================================
            # AGENT 5: CARE AGENT
            # Provides ACTIONABLE GUIDANCE for user (user-visible value)
            # ========================================
            
            consolidated_response['pipeline_metadata']['execution_order'].append("care_agent")
            consolidated_response['pipeline_metadata']['agents_executed'] += 1
            
            # Execute care guidance generation (synthesizes all insights)
            care_result = self.care_agent.generate_guidance(
                drift_analysis=drift_result,
                context_analysis=context_result,
                risk_analysis=risk_result,
                user_profile=user_profile
            )
            
            # Store care guidance output
            consolidated_response['care_guidance'] = care_result
            
            if care_result.get('success'):
                consolidated_response['pipeline_metadata']['agents_successful'] += 1
            
            # ========================================
            # PIPELINE COMPLETION
            # ========================================
            
            # Mark overall success if all agents completed
            consolidated_response['success'] = (
                consolidated_response['pipeline_metadata']['agents_successful'] >= 4
            )  # Allow 1 agent to fail and still succeed
            
            # Add summary metadata
            consolidated_response['pipeline_metadata']['completion_status'] = (
                "complete" if consolidated_response['success'] else "partial"
            )
            
        except Exception as e:
            # Handle pipeline-level errors
            consolidated_response['error'] = f"Pipeline execution error: {str(e)}"
            consolidated_response['success'] = False
        
        return consolidated_response
    
    def analyze_single_metric_quick(
        self,
        metric_name: str,
        baseline: float,
        recent: float,
        user_profile: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Quick analysis for single metric without full context
        
        Simplified pipeline for rapid feedback:
        - Drift detection only
        - Basic care guidance
        - No risk assessment (requires history)
        - No safety escalation (requires full context)
        
        Args:
            metric_name (str): Metric name
            baseline (float): Baseline value
            recent (float): Recent value
            user_profile (dict, optional): Basic user info
        
        Returns:
            Dict with drift summary and basic guidance
        
        Example:
            result = orchestrator.analyze_single_metric_quick(
                metric_name="stability",
                baseline=92.0,
                recent=87.5
            )
        """
        drift_percentage = ((recent - baseline) / baseline) * 100
        
        # Execute drift agent only
        drift_result = self.drift_agent.analyze_drift(
            metric_name=metric_name,
            baseline_value=baseline,
            recent_value=recent,
            drift_percentage=drift_percentage,
            days_observed=1,
            additional_context=user_profile
        )
        
        # Generate basic care guidance
        care_result = self.care_agent.generate_guidance(
            drift_analysis=drift_result,
            user_profile=user_profile
        )
        
        return {
            "success": True,
            "drift_summary": drift_result,
            "care_guidance": care_result,
            "note": "Quick analysis - for comprehensive insights, use analyze_health_drift_comprehensive()"
        }
    
    def get_agent_status(self) -> Dict[str, Any]:
        """
        Get status of all agents in the pipeline
        
        Returns:
            Dict with agent readiness and configuration status
        """
        return {
            "pipeline_name": self.pipeline_name,
            "total_agents": self.agent_count,
            "adk_runtime_ready": is_adk_ready(),
            "agents": {
                "drift_agent": {"name": self.drift_agent.agent_name, "initialized": True},
                "context_agent": {"name": self.context_agent.agent_name, "initialized": True},
                "risk_agent": {"name": self.risk_agent.agent_name, "initialized": True},
                "safety_agent": {"name": self.safety_agent.agent_name, "initialized": True},
                "care_agent": {"name": self.care_agent.agent_name, "initialized": True}
            },
            "execution_order": [
                "1. drift_agent - Detects WHAT changed",
                "2. context_agent - Explains WHY it happened",
                "3. risk_agent - Evaluates HOW CONCERNING",
                "4. safety_agent - Decides IF ESCALATION needed",
                "5. care_agent - Provides ACTIONABLE GUIDANCE"
            ]
        }


# ========================================
# CONVENIENCE FUNCTIONS
# ========================================

def run_full_health_analysis(
    metric_name: str,
    baseline_value: float,
    recent_value: float,
    drift_history: Optional[List[Dict[str, Any]]] = None,
    user_profile: Optional[Dict[str, Any]] = None,
    user_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Convenience function to run complete 5-agent analysis
    
    Args:
        metric_name (str): Health metric name
        baseline_value (float): Baseline measurement
        recent_value (float): Recent measurement
        drift_history (list, optional): Multi-day drift data
        user_profile (dict, optional): User information
        user_id (str, optional): User ID for context fetch
    
    Returns:
        Dict: Consolidated analysis from all 5 agents
    
    Example:
        from agents.orchestrator import run_full_health_analysis
        
        result = run_full_health_analysis(
            metric_name="stability",
            baseline_value=92.0,
            recent_value=87.5,
            drift_history=[
                {"day": 1, "value": 91.5, "drift_percentage": -0.5},
                {"day": 2, "value": 90.2, "drift_percentage": -1.9},
                {"day": 3, "value": 88.7, "drift_percentage": -3.6},
                {"day": 4, "value": 87.5, "drift_percentage": -4.9}
            ],
            user_profile={"age": 45, "lifestyle": "working professional"},
            user_id="user-123"
        )
        
        # Access results
        drift = result['drift_summary']
        context = result['contextual_explanation']
        risk = result['risk_assessment']
        safety = result['safety_notice']
        care = result['care_guidance']
    """
    orchestrator = HealthDriftOrchestrator()
    return orchestrator.analyze_health_drift_comprehensive(
        metric_name=metric_name,
        baseline_value=baseline_value,
        recent_value=recent_value,
        drift_history=drift_history,
        user_profile=user_profile,
        user_id=user_id
    )


def quick_drift_check(
    metric_name: str,
    baseline: float,
    recent: float
) -> Dict[str, Any]:
    """
    Quick drift check without full pipeline
    
    Args:
        metric_name (str): Metric name
        baseline (float): Baseline value
        recent (float): Recent value
    
    Returns:
        Dict: Basic drift analysis and guidance
    
    Example:
        from agents.orchestrator import quick_drift_check
        
        result = quick_drift_check(
            metric_name="stability",
            baseline=92.0,
            recent=87.5
        )
        
        print(result['drift_summary']['severity_level'])
        print(result['care_guidance']['guidance_list'])
    """
    orchestrator = HealthDriftOrchestrator()
    return orchestrator.analyze_single_metric_quick(
        metric_name=metric_name,
        baseline=baseline,
        recent=recent
    )
