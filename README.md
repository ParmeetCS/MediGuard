# MediGuard Drift AI 🏥

**Daily Health Drift Monitoring System with AI-Powered Analysis**

## Overview

MediGuard Drift AI is an intelligent health monitoring platform that combines computer vision-based activity tracking with a sophisticated multi-agent AI system to detect, analyze, and respond to subtle health changes over time. The system uses a pipeline of specialized AI agents to provide personalized health insights and early warning detection for potential health deterioration.

## Key Features

### 🤖 Multi-Agent AI System (ADK Pipeline)
The heart of MediGuard is a 5-agent orchestration system that analyzes health data through multiple specialized lenses:

1. **Drift Agent** - Detects numerical changes in health metrics using statistical analysis
2. **Context Agent** - Explains why changes occurred by analyzing lifestyle factors and user context
3. **Risk Agent** - Evaluates temporal risk patterns and assesses concern levels
4. **Safety Agent** - Acts as an ethical guardrail to determine if medical escalation is needed
5. **Care Agent** - Synthesizes insights to provide actionable, personalized health guidance

### 📹 Vision-Based Activity Tracking
- **Camera Integration**: Real-time video capture for physical activity assessment
- **Activity Types**:
  - Sit-to-Stand transitions (30 seconds)
  - Short walks (45 seconds)
  - Hand steadiness tests (30 seconds)
- **Feature Extraction**: Automated analysis of movement speed, stability, and coordination

### 📊 Health Metrics Monitoring
Tracks key health indicators:
- Movement speed
- Stability and balance
- Sit-to-stand performance
- Walking stability
- Hand steadiness

### 💬 AI Health Chat Assistant
- Conversational interface powered by Google's Gemini AI
- Fetches real user health data from the database
- Provides personalized insights based on actual health trends
- Pattern-matched responses for common health queries

### 🔐 Secure Authentication
- Supabase-based authentication system
- Secure user data storage and management
- Privacy-protected health records

### 📈 Dashboard & Analytics
- Daily health check tracking
- Visual trend analysis
- Historical data comparison
- Progress monitoring

## Technology Stack

### Core Technologies
- **Python 3.x** - Primary programming language
- **Streamlit** - Web application framework
- **Google Gemini AI** - Advanced language model for natural conversations
- **Supabase** - Backend database and authentication

### Computer Vision
- **OpenCV** - Real-time video processing
- **NumPy** - Numerical computations for feature extraction
- **Matplotlib** - Data visualization

### AI & Machine Learning
- **Pydantic** - Data validation and structured outputs
- **Custom ADK Runtime** - Agent orchestration framework

## Project Structure

```
AI_Agent/
├── app.py                          # Main Streamlit application entry point
├── requirements.txt                # Python dependencies
│
├── agents/                         # Multi-agent AI system
│   ├── orchestrator.py            # Central agent coordination
│   ├── drift_agent.py             # Health drift detection
│   ├── context_agent.py           # Lifestyle factor analysis
│   ├── risk_agent.py              # Temporal risk assessment
│   ├── safety_agent.py            # Ethical escalation guardrails
│   ├── care_agent.py              # Actionable guidance generation
│   ├── ai_integration.py          # AI model integration layer
│   └── adk_runtime.py             # Agent execution runtime
│
├── pages/                          # Streamlit pages
│   ├── home.py                    # Landing page
│   ├── dashboard.py               # Health metrics dashboard
│   ├── daily_check.py             # Daily health check interface
│   ├── ai_health_chat.py          # AI chatbot interface
│   ├── context_inputs.py          # User context collection
│   ├── profile.py                 # User profile management
│   └── test_data_generator.py    # Testing utilities
│
├── storage/                        # Data persistence layer
│   ├── database.py                # Database connection management
│   ├── health_repository.py       # Health data CRUD operations
│   ├── context_repository.py      # Context data management
│   └── health_data_fetcher.py     # Data retrieval utilities
│
├── vision/                         # Computer vision system
│   ├── camera.py                  # Camera capture management
│   ├── activity_runner.py         # Timed activity execution
│   └── feature_extraction.py      # Movement analysis algorithms
│
└── auth/                           # Authentication system
    └── supabase_auth.py           # Supabase authentication handlers
```

## Installation

### Prerequisites
- Python 3.8 or higher
- Webcam (for vision-based activities)
- Supabase account (for data storage)
- Google Gemini API key (for AI features)

### Setup Steps

1. **Clone the repository**
   ```bash
   cd AI_Agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   # Supabase Configuration
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_KEY=your_supabase_anon_key
   
   # Google Gemini AI
   GEMINI_API_KEY=your_gemini_api_key
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

## Usage

### First Time Setup
1. **Sign Up**: Create an account using email and password
2. **Complete Profile**: Enter basic health information
3. **Add Context**: Provide lifestyle and environmental context
4. **First Check**: Perform your initial daily health check

### Daily Workflow
1. **Login**: Authenticate to access your dashboard
2. **Daily Check**: Complete vision-based activities (5-10 minutes)
3. **Review Dashboard**: Check your health trends and metrics
4. **Chat with AI**: Ask questions about your health patterns
5. **Act on Insights**: Follow personalized recommendations

### AI Chat Examples
- "How is my stability trending?"
- "What factors might affect my balance?"
- "Show me my progress over the last week"
- "What should I focus on improving?"

## AI Agent Pipeline

### Orchestrator Flow
```
User Health Data Input
        ↓
[1] Drift Agent → Detects metric changes (drift detection)
        ↓
[2] Context Agent → Explains why changes occurred
        ↓
[3] Risk Agent → Assesses severity and trends
        ↓
[4] Safety Agent → Determines if escalation needed
        ↓
[5] Care Agent → Generates actionable guidance
        ↓
Unified Response to User
```

### Agent Responsibilities

- **Drift Agent**: Analyzes numerical health metrics to detect statistically significant changes
- **Context Agent**: Correlates health changes with lifestyle factors (sleep, stress, diet, etc.)
- **Risk Agent**: Evaluates temporal patterns to assess urgency and concern levels
- **Safety Agent**: Applies ethical guardrails and determines if medical professional consultation is needed
- **Care Agent**: Creates personalized, actionable recommendations in user-friendly language

## Data Privacy & Security

- **Encryption**: All data transmitted over HTTPS
- **Authentication**: Secure Supabase authentication
- **Privacy**: Health data is user-specific and not shared
- **Compliance**: Designed with healthcare data sensitivity in mind

## Testing

The project includes several test files for validation:

- `test_supabase_connection.py` - Database connectivity
- `test_supabase_save.py` - Data persistence
- `test_gemini_chat.py` - AI chat functionality
- `test_data_saved.py` - Data integrity
- `test_insert_sample_data.py` - Sample data generation

Run tests:
```bash
python test_supabase_connection.py
python test_gemini_chat.py
```

## Contributing

This is a health monitoring research project. Contributions focused on:
- Improved feature extraction algorithms
- Enhanced AI agent prompts
- Additional health metrics
- Better visualization

## Limitations & Disclaimers

⚠️ **Important Medical Disclaimer**

- This system is for informational and monitoring purposes only
- NOT a substitute for professional medical advice, diagnosis, or treatment
- Always consult qualified healthcare providers for medical decisions
- In case of emergency, contact emergency services immediately

## Future Enhancements

- [ ] Integration with wearable devices
- [ ] Advanced anomaly detection algorithms
- [ ] Multi-user family monitoring
- [ ] Medication tracking
- [ ] Telemedicine integration
- [ ] Mobile app version
- [ ] Offline mode capabilities

## License

[Specify your license here]

## Support

For issues, questions, or suggestions:
- Create an issue in the repository
- Contact: [Your contact information]

## Acknowledgments

- Built with Streamlit for rapid web development
- Powered by Google Gemini AI for intelligent conversations
- Uses Supabase for scalable backend infrastructure
- Computer vision capabilities via OpenCV

---

**Version**: 2.0.0  
**Last Updated**: December 2025  
**Status**: Active Development
