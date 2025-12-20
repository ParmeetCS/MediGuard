"""
Test script to verify improved AI agent responses
Run this to see the enhanced, user-friendly medical responses
"""

from agents.drift_agent import DriftAgent
from agents.care_agent import CareAgent
from agents.context_agent import ContextAgent
from agents.risk_agent import RiskAgent

def test_drift_agent():
    """Test Drift Agent with sample data"""
    print("=" * 80)
    print("TESTING DRIFT AGENT - Enhanced User-Friendly Responses")
    print("=" * 80)
    
    agent = DriftAgent()
    
    # Sample drift data
    result = agent.analyze_drift(
        metric_name="stability",
        baseline_value=92.0,
        recent_value=87.5,
        drift_percentage=-4.9,
        days_observed=7,
        additional_context={
            "age": 45,
            "lifestyle": "working professional"
        }
    )
    
    if result['success']:
        print("\n✅ Drift Analysis Response:")
        print("-" * 80)
        print(result.get('explanation', 'No explanation provided'))
        print("-" * 80)
        print(f"\nSeverity: {result.get('severity_level', 'unknown')}")
        print(f"Response Length: {len(result.get('explanation', ''))} characters")
        print("\nFactors:")
        for factor in result.get('factors', [])[:3]:
            print(f"  - {factor}")
    else:
        print(f"\n❌ Error: {result.get('error', 'Unknown error')}")
    
    return result

def test_care_agent():
    """Test Care Agent with sample guidance request"""
    print("\n\n" + "=" * 80)
    print("TESTING CARE AGENT - Enhanced Wellness Guidance")
    print("=" * 80)
    
    agent = CareAgent()
    
    # Sample analysis data
    drift_analysis = {
        "success": True,
        "severity_level": "moderate",
        "affected_features": ["stability"],
        "explanation": "Moderate decline in stability detected"
    }
    
    risk_analysis = {
        "success": True,
        "risk_level": "needs_observation",
        "days_observed": 7,
        "is_worsening": False
    }
    
    user_profile = {
        "age": 45,
        "lifestyle": "working professional"
    }
    
    result = agent.generate_guidance(
        drift_analysis=drift_analysis,
        risk_analysis=risk_analysis,
        user_profile=user_profile
    )
    
    if result['success']:
        print("\n✅ Care Guidance Response:")
        print("-" * 80)
        print("\nGuidance Suggestions:")
        for i, suggestion in enumerate(result.get('guidance_list', []), 1):
            print(f"\n{i}. {suggestion}")
        print("-" * 80)
        print(f"\nTone: {result.get('tone', 'unknown')}")
        print(f"Response Length: {sum(len(s) for s in result.get('guidance_list', []))} characters")
    else:
        print(f"\n❌ Error: {result.get('error', 'Unknown error')}")
    
    return result

def main():
    """Run all tests"""
    print("\n" + "=" * 80)
    print("AI AGENT RESPONSE QUALITY TEST")
    print("Testing Enhanced User-Friendly Medical Responses")
    print("=" * 80)
    
    # Check if ADK is ready
    from agents.adk_runtime import is_adk_ready
    
    if not is_adk_ready():
        print("\n⚠️  WARNING: ADK Runtime not configured!")
        print("Please set GOOGLE_API_KEY in your .env file to test AI responses.")
        print("\nWithout API key, agents will use fallback rule-based responses.")
        print("=" * 80)
    else:
        print("\n✅ ADK Runtime is configured and ready!")
        print("=" * 80)
    
    # Test each agent
    drift_result = test_drift_agent()
    care_result = test_care_agent()
    
    # Summary
    print("\n\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    if drift_result.get('success') and care_result.get('success'):
        drift_length = len(drift_result.get('explanation', ''))
        care_length = sum(len(s) for s in care_result.get('guidance_list', []))
        
        print(f"\n✅ Drift Agent Response: {drift_length} characters")
        print(f"   Expected: 300+ characters (detailed explanation)")
        print(f"   Status: {'✓ GOOD' if drift_length > 300 else '⚠ TOO SHORT'}")
        
        print(f"\n✅ Care Agent Response: {care_length} characters")
        print(f"   Expected: 400+ characters (detailed guidance)")
        print(f"   Status: {'✓ GOOD' if care_length > 400 else '⚠ TOO SHORT'}")
        
        print("\n" + "=" * 80)
        print("✅ All agents are generating responses!")
        print("Check the detail level and tone above.")
        print("=" * 80)
    else:
        print("\n⚠️  Some agents failed. Check errors above.")
    
    print("\n")

if __name__ == "__main__":
    main()
