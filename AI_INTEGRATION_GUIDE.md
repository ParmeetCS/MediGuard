# AI Agent Integration - MediGuard Drift AI

## Overview
This document explains how the ADK (Agent Development Kit) is integrated with your MediGuard Drift AI application to provide intelligent health analysis using Gemini API.

## Architecture

```
User Input (Health Context) → Supabase Database
                                    ↓
Health Checks → Supabase Database
                                    ↓
AI Integration Layer (ai_integration.py)
                                    ↓
ADK Orchestrator (orchestrator.py)
                                    ↓
5 AI Agents (powered by Gemini API):
  1. Drift Agent → Detects WHAT changed
  2. Context Agent → Explains WHY it happened
  3. Risk Agent → Evaluates HOW CONCERNING
  4. Safety Agent → Decides IF ESCALATION needed
  5. Care Agent → Provides ACTIONABLE GUIDANCE
                                    ↓
Output to UI (Chat & Dashboard)
```

## Data Flow

### 1. **Data Collection**
   - Users input health context via `Health Context` page
   - Data stored in Supabase `user_context_data` table:
     - medical_summary
     - known_conditions
     - report_summary
     - sleep_hours
     - stress_level
     - workload
     - activity_level

### 2. **Health Monitoring**
   - Users complete daily health checks
   - Data stored in Supabase `health_checks` table:
     - Movement metrics
     - Stability scores
     - Mobility measurements
     - Timestamps

### 3. **AI Analysis**
   - `AIHealthAnalyzer` class fetches data from Supabase
   - Prepares data in ADK-compatible format:
     - Calculates baseline from first 5 days
     - Creates drift history with percentage changes
     - Combines user context with health metrics

### 4. **ADK Execution**
   - `HealthDriftOrchestrator` runs 5-agent pipeline:
     1. **Drift Agent**: Analyzes numerical changes in metrics
     2. **Context Agent**: Correlates changes with lifestyle factors (sleep, stress, workload)
     3. **Risk Agent**: Evaluates temporal patterns and consistency
     4. **Safety Agent**: Ethical guardrail checking if medical escalation needed
     5. **Care Agent**: Generates actionable, user-friendly guidance

### 5. **Output Display**
   - **AI Health Chat**: Conversational interface with AI-powered responses
   - **Dashboard**: Visual insights with AI analysis button

## Key Components

### `agents/ai_integration.py`
- **AIHealthAnalyzer**: Main integration class
  - `analyze_user_health()`: Full health analysis
  - `get_conversational_response()`: Chat responses
- Helper functions:
  - `get_ai_health_insights()`: Quick analysis for dashboard
  - `get_ai_chat_response()`: Quick chat response

### `agents/orchestrator.py`
- **HealthDriftOrchestrator**: Coordinates all 5 agents
  - `analyze_health_drift_comprehensive()`: Full pipeline
- Utility functions:
  - `run_full_health_analysis()`: Convenience wrapper
  - `quick_drift_check()`: Fast drift check

### `agents/context_agent.py`
- Fetches user context from Supabase via `ContextRepository`
- Uses Gemini API to explain changes based on lifestyle factors
- Outputs possible factors, contextual explanation, confidence level

### `storage/context_repository.py`
- **ContextRepository**: Data access layer for user context
  - `fetch_user_context()`: Gets context from Supabase
  - `user_has_context()`: Checks if context exists

## How It Works - Example

### User Journey:
1. **User fills Health Context form:**
   ```
   Sleep Hours: 5.5
   Stress Level: High
   Workload: Heavy
   Activity Level: Sedentary
   ```

2. **User completes daily health checks for 7 days:**
   ```
   Day 1: Stability = 92%
   Day 2: Stability = 90%
   Day 3: Stability = 89%
   Day 4: Stability = 87%
   Day 5: Stability = 86%
   Day 6: Stability = 85%
   Day 7: Stability = 84%
   ```

3. **AI Analysis Triggered:**
   - **Drift Agent**: "8.7% decline in stability over 7 days - Moderate severity"
   - **Context Agent**: "Possible factors: High stress (may affect balance), Low sleep (5.5 hours - may impair motor control), Sedentary lifestyle (may weaken core stability)"
   - **Risk Agent**: "Consistent downward trend with 85% consistency - Needs observation"
   - **Safety Agent**: "No immediate medical escalation needed - Continue monitoring"
   - **Care Agent**: "Recommendations: Improve sleep hygiene (aim for 7-8 hours), Manage stress (try meditation), Increase physical activity (15-min daily walks), Continue daily monitoring"

4. **User sees insights in:**
   - **Chat**: Ask "Why is my stability declining?" → Get AI-powered contextual answer
   - **Dashboard**: Click "Generate AI Analysis" → See comprehensive breakdown

## Configuration

### Required Environment Variables (`.env`):
```env
GOOGLE_API_KEY=your_gemini_api_key_here
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

### Gemini Model Settings:
- Model: `gemini-1.5-flash`
- Temperature: 0.7 (balance creativity/consistency)
- Top-p: 0.95 (nucleus sampling)
- Max tokens: 2048
- Safety settings: BLOCK_MEDIUM_AND_ABOVE

## Usage in UI

### AI Health Chat
```python
# User asks question
user_question = "Why is my stability declining?"

# Get AI-powered response
response = get_ai_chat_response(user_id, user_question)

# Display in chat interface
if response['success']:
    display(response['response'])  # Full contextual answer
```

### Dashboard
```python
# User clicks "Generate AI Analysis" button
ai_result = get_ai_health_insights(user_id, metric="overall_mobility")

# Display insights
if ai_result['success']:
    summary = ai_result['summary']  # Drift %, severity, risk
    recommendations = ai_result['recommendations']  # Action items
    analysis = ai_result['analysis']  # Full ADK output
```

## Benefits

1. **Personalized Analysis**: Uses YOUR health context (sleep, stress, lifestyle)
2. **Proactive Detection**: Catches gradual 1-2% changes before they accumulate
3. **Contextual Insights**: Explains WHY changes occur, not just WHAT changed
4. **Ethical AI**: Safety agent ensures appropriate medical escalation
5. **Actionable Guidance**: Care agent provides specific, useful recommendations

## Safety Features

- **No Diagnosis**: AI explicitly avoids medical diagnoses
- **Probabilistic Language**: Uses "may", "could", "might" (not certainties)
- **Escalation Logic**: Safety agent flags when professional care needed
- **Educational Focus**: Provides insights for monitoring, not treatment

## Testing

### Check if ADK is working:
```python
from agents.adk_runtime import is_adk_ready

if is_adk_ready():
    print("✅ ADK configured and ready")
else:
    print("❌ Configure GOOGLE_API_KEY in .env")
```

### Test full analysis:
```python
from agents.ai_integration import get_ai_health_insights

result = get_ai_health_insights(
    user_id="test-user-123",
    metric="overall_mobility"
)

print(result['summary'])
print(result['recommendations'])
```

## Future Enhancements

1. **Multi-metric Analysis**: Analyze correlations between multiple metrics
2. **Historical Comparisons**: Compare current patterns to past periods
3. **Predictive Modeling**: Forecast future trends based on current trajectory
4. **Voice Interaction**: Voice-based chat with AI assistant
5. **Smart Notifications**: Proactive alerts when drift accelerates

## Troubleshooting

### "AI system not configured"
→ Set `GOOGLE_API_KEY` in `.env` file

### "Insufficient data for analysis"
→ Complete at least 2-3 daily health checks

### "Error loading existing data"
→ Check Supabase table names match schema

### AI gives generic responses
→ Fill out Health Context form for personalized insights

---

**Last Updated**: December 20, 2025
**Status**: ✅ Fully Integrated and Operational
