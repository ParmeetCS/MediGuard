# 🏥 MediGuard Drift AI - Technical Documentation

**Version:** 2.0.0  
**Last Updated:** December 2025  
**Status:** Production Ready  
**Document Type:** Complete Technical Reference

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [APIs & External Services](#apis--external-services)
4. [System Architecture](#system-architecture)
5. [Multi-Agent AI Pipeline (ADK)](#multi-agent-ai-pipeline-adk)
6. [Module Documentation](#module-documentation)
7. [Data Flow & Workflow](#data-flow--workflow)
8. [Security & Authentication](#security--authentication)
9. [Deployment Guide](#deployment-guide)
10. [Environment Configuration](#environment-configuration)

---

## 🎯 Project Overview

### What is MediGuard Drift AI?

MediGuard Drift AI is an **intelligent health monitoring platform** that combines:
- **Computer Vision** for movement and activity analysis
- **Multi-Agent AI System** for comprehensive health drift detection
- **Real-time Analytics** for tracking health trends over time

### Core Problem Solved

The system detects **subtle health changes (drift)** that may indicate early signs of:
- Mobility decline
- Balance issues
- Fall risk
- Parkinson's disease symptoms
- Arthritis progression
- General physical deterioration

### Target Users
- Elderly individuals (65+)
- Patients with chronic conditions
- Caregivers and family members
- Healthcare providers

---

## 🛠️ Technology Stack

### Programming Languages

| Language | Version | Purpose |
|----------|---------|---------|
| **Python** | 3.10+ | Primary backend & AI logic |
| **HTML/CSS** | 5/3 | UI styling in Streamlit |
| **SQL** | PostgreSQL | Database queries via Supabase |

### Frameworks & Libraries

| Technology | Company/Org | Version | Purpose |
|------------|-------------|---------|---------|
| **Streamlit** | Snowflake Inc. | Latest | Web application framework |
| **OpenCV** | Intel/OpenCV.org | 4.x | Computer vision & video processing |
| **NumPy** | NumFOCUS | Latest | Numerical computations |
| **Pandas** | NumFOCUS | Latest | Data manipulation & analysis |
| **Plotly** | Plotly Inc. | Latest | Interactive data visualization |
| **Matplotlib** | NumFOCUS | Latest | Static charts & graphs |
| **Pydantic** | Samuel Colvin | 2.x | Data validation & serialization |
| **ReportLab** | ReportLab Inc. | Latest | PDF report generation |
| **Pillow (PIL)** | PIL/Pillow | Latest | Image processing |
| **python-dotenv** | Saurabh Kumar | Latest | Environment variable management |

### AI & Machine Learning

| Technology | Company | Purpose |
|------------|---------|---------|
| **Google Gemini AI** | Google DeepMind | Large Language Model for chat & analysis |
| **google-generativeai** | Google | Python SDK for Gemini API |
| **Custom ADK Runtime** | MediGuard | Agent orchestration framework |

### Backend & Database

| Technology | Company | Purpose |
|------------|---------|---------|
| **Supabase** | Supabase Inc. | Backend-as-a-Service (BaaS) |
| **PostgreSQL** | PostgreSQL Global Dev Group | Relational database (via Supabase) |
| **Supabase Auth** | Supabase Inc. | User authentication & session management |

### Deployment

| Platform | Company | Purpose |
|----------|---------|---------|
| **Streamlit Cloud** | Snowflake Inc. | Cloud hosting & deployment |
| **GitHub** | Microsoft | Version control & CI/CD |

---

## 🔌 APIs & External Services

### 1. Google Gemini AI API

| Attribute | Details |
|-----------|---------|
| **Provider** | Google DeepMind |
| **Model** | gemini-1.5-flash / gemini-pro |
| **Endpoint** | `generativelanguage.googleapis.com` |
| **Authentication** | API Key |
| **Purpose** | Natural language processing, health analysis, chat responses |
| **Rate Limits** | 60 requests/minute (free tier) |

**Usage in MediGuard:**
- AI Health Chat conversations
- Medical report analysis (vision)
- Health recommendation generation
- Context-aware responses

### 2. Supabase API

| Attribute | Details |
|-----------|---------|
| **Provider** | Supabase Inc. |
| **Type** | REST API + Realtime |
| **Endpoint** | `https://<project>.supabase.co` |
| **Authentication** | API Key + JWT |
| **Database** | PostgreSQL |

**Services Used:**
- **Auth Service**: User signup, login, session management
- **Database Service**: Health records, user profiles, context data
- **Storage Service**: (Optional) File uploads

**Database Tables:**
```sql
-- Users & Authentication (managed by Supabase Auth)
auth.users

-- Health Check Records
health_checks (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES auth.users,
    check_date DATE,
    avg_movement_speed FLOAT,
    avg_stability FLOAT,
    sit_stand_movement_speed FLOAT,
    walk_stability FLOAT,
    steady_stability FLOAT,
    created_at TIMESTAMP
)

-- User Context/Lifestyle Data
user_context (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES auth.users,
    age INTEGER,
    gender TEXT,
    blood_type TEXT,
    medical_conditions TEXT,
    medications TEXT,
    sleep_hours FLOAT,
    stress_level TEXT,
    activity_level TEXT,
    mobility_aids TEXT,
    living_situation TEXT,
    report_summary TEXT,
    updated_at TIMESTAMP
)
```

### 3. Google Custom Search API (Optional)

| Attribute | Details |
|-----------|---------|
| **Provider** | Google Cloud |
| **Purpose** | Health information search |
| **Endpoint** | `customsearch.googleapis.com` |
| **Authentication** | API Key + Search Engine ID |

---

## 🏗️ System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                            │
│  ┌─────────┐ ┌──────────┐ ┌──────────┐ ┌─────────┐ ┌──────────┐ │
│  │  Home   │ │Dashboard │ │Daily     │ │AI Chat  │ │  Guide   │ │
│  │  Page   │ │   Page   │ │Health    │ │  Page   │ │  Page    │ │
│  │         │ │          │ │Check     │ │         │ │          │ │
│  └────┬────┘ └────┬─────┘ └────┬─────┘ └────┬────┘ └────┬─────┘ │
│       │           │            │            │           │        │
│       └───────────┴─────┬──────┴────────────┴───────────┘        │
│                         │                                         │
│                    ┌────▼────┐                                    │
│                    │ app.py  │  (Main Router)                     │
│                    └────┬────┘                                    │
└─────────────────────────┼───────────────────────────────────────┘
                          │
┌─────────────────────────┼───────────────────────────────────────┐
│                    BUSINESS LOGIC LAYER                          │
│                         │                                         │
│  ┌──────────────────────▼──────────────────────┐                 │
│  │         AI Agent Orchestrator               │                 │
│  │  ┌─────────────────────────────────────┐   │                 │
│  │  │     5-Agent ADK Pipeline            │   │                 │
│  │  │  ┌───────┐ ┌─────────┐ ┌──────┐    │   │                 │
│  │  │  │Drift  │→│Context  │→│Risk  │    │   │                 │
│  │  │  │Agent  │ │Agent    │ │Agent │    │   │                 │
│  │  │  └───────┘ └─────────┘ └──┬───┘    │   │                 │
│  │  │                           │         │   │                 │
│  │  │  ┌───────┐ ┌─────────────▼──┐      │   │                 │
│  │  │  │Care   │←│Safety Agent    │      │   │                 │
│  │  │  │Agent  │ │(Ethical Guard) │      │   │                 │
│  │  │  └───────┘ └────────────────┘      │   │                 │
│  │  └─────────────────────────────────────┘   │                 │
│  └─────────────────────────────────────────────┘                 │
│                         │                                         │
│  ┌──────────────────────▼──────────────────────┐                 │
│  │         Vision Processing Module            │                 │
│  │  ┌──────────┐ ┌───────────┐ ┌───────────┐  │                 │
│  │  │ Camera   │ │ Person    │ │ Feature   │  │                 │
│  │  │ Stream   │ │ Detection │ │ Extraction│  │                 │
│  │  └──────────┘ └───────────┘ └───────────┘  │                 │
│  └─────────────────────────────────────────────┘                 │
└─────────────────────────┼───────────────────────────────────────┘
                          │
┌─────────────────────────┼───────────────────────────────────────┐
│                    DATA LAYER                                    │
│                         │                                         │
│  ┌──────────────────────▼──────────────────────┐                 │
│  │              Storage Module                  │                 │
│  │  ┌──────────────┐ ┌─────────────────────┐   │                 │
│  │  │ database.py  │ │ health_repository.py│   │                 │
│  │  └──────────────┘ └─────────────────────┘   │                 │
│  │  ┌──────────────────┐ ┌─────────────────┐   │                 │
│  │  │context_repository│ │health_data_     │   │                 │
│  │  │       .py        │ │fetcher.py       │   │                 │
│  │  └──────────────────┘ └─────────────────┘   │                 │
│  └─────────────────────────────────────────────┘                 │
│                         │                                         │
│                    ┌────▼────┐                                    │
│                    │Supabase │ (Cloud Database)                   │
│                    │PostgreSQL│                                   │
│                    └─────────┘                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🤖 Multi-Agent AI Pipeline (ADK)

### Overview

The **Agent Development Kit (ADK)** is a custom-built orchestration system that runs 5 specialized AI agents in sequence to analyze health data.

### Agent Execution Order

```
┌─────────────────────────────────────────────────────────────┐
│                    ADK PIPELINE FLOW                         │
│                                                              │
│  INPUT: Health metrics + User context + Historical data     │
│                         │                                    │
│                         ▼                                    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ 1. DRIFT AGENT                                       │    │
│  │    • Detects WHAT changed in health metrics          │    │
│  │    • Statistical analysis of numerical drift         │    │
│  │    • Outputs: drift_percentage, trend, severity      │    │
│  └──────────────────────────┬──────────────────────────┘    │
│                              ▼                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ 2. CONTEXT AGENT                                     │    │
│  │    • Explains WHY changes occurred                   │    │
│  │    • Analyzes lifestyle factors (sleep, stress)      │    │
│  │    • Outputs: contextual_explanation, factors        │    │
│  └──────────────────────────┬──────────────────────────┘    │
│                              ▼                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ 3. RISK AGENT                                        │    │
│  │    • Evaluates HOW CONCERNING the changes are        │    │
│  │    • Temporal pattern analysis                        │    │
│  │    • Outputs: risk_level, days_observed, reasoning   │    │
│  └──────────────────────────┬──────────────────────────┘    │
│                              ▼                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ 4. SAFETY AGENT                                      │    │
│  │    • Ethical guardrail for medical escalation        │    │
│  │    • Determines IF professional help needed          │    │
│  │    • Outputs: escalation_needed, safety_notice       │    │
│  └──────────────────────────┬──────────────────────────┘    │
│                              ▼                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ 5. CARE AGENT                                        │    │
│  │    • Synthesizes all insights                         │    │
│  │    • Provides ACTIONABLE GUIDANCE                    │    │
│  │    • Outputs: recommendations, care_advice           │    │
│  └──────────────────────────┬──────────────────────────┘    │
│                              ▼                               │
│  OUTPUT: Comprehensive health analysis report               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Agent Details

#### 1. Drift Agent (`agents/drift_agent.py`)
| Attribute | Details |
|-----------|---------|
| **Purpose** | Detect numerical changes in health metrics |
| **Input** | Historical health check data (7-30 days) |
| **Algorithm** | Statistical comparison of baseline vs recent values |
| **Output** | `DriftSummary` (drift_percentage, trend, severity) |

#### 2. Context Agent (`agents/context_agent.py`)
| Attribute | Details |
|-----------|---------|
| **Purpose** | Explain why health changes occurred |
| **Input** | Drift results + User lifestyle context |
| **Factors Analyzed** | Sleep, stress, medications, activity level |
| **Output** | `ContextualExplanation` (factors, explanation) |

#### 3. Risk Agent (`agents/risk_agent.py`)
| Attribute | Details |
|-----------|---------|
| **Purpose** | Assess temporal risk patterns |
| **Input** | Drift history over time |
| **Risk Levels** | low, moderate, high, critical |
| **Output** | `RiskAssessment` (risk_level, days_observed, reasoning) |

#### 4. Safety Agent (`agents/safety_agent.py`)
| Attribute | Details |
|-----------|---------|
| **Purpose** | Ethical guardrail for medical escalation |
| **Input** | All previous agent outputs |
| **Decision** | Should user seek medical attention? |
| **Output** | `SafetyNotice` (escalation_needed, notice, disclaimer) |

#### 5. Care Agent (`agents/care_agent.py`)
| Attribute | Details |
|-----------|---------|
| **Purpose** | Generate actionable health guidance |
| **Input** | Complete pipeline results |
| **Output** | `CareRecommendations` (recommendations[], care_advice) |

---

## 📁 Module Documentation

### Project Structure

```
AI_Agent/
├── app.py                      # Main application entry point
├── requirements.txt            # Python dependencies
├── packages.txt                # System packages (Streamlit Cloud)
├── README.md                   # Project documentation
├── .env                        # Environment variables (not in git)
│
├── agents/                     # AI Agent System
│   ├── __init__.py
│   ├── orchestrator.py         # Central agent coordinator
│   ├── adk_runtime.py          # Agent execution runtime
│   ├── ai_integration.py       # AI model integration layer
│   ├── drift_agent.py          # Health drift detection
│   ├── context_agent.py        # Lifestyle factor analysis
│   ├── risk_agent.py           # Temporal risk assessment
│   ├── safety_agent.py         # Medical escalation guardrail
│   ├── care_agent.py           # Actionable guidance generation
│   └── health_search_agent.py  # Health information search
│
├── pages/                      # Streamlit UI Pages
│   ├── __init__.py
│   ├── home.py                 # Landing/welcome page
│   ├── profile.py              # User profile management
│   ├── daily_health_check.py   # Camera-based health tests
│   ├── dashboard.py            # Health trends visualization
│   ├── ai_health_chat.py       # AI chatbot interface
│   ├── context_inputs.py       # Lifestyle data collection
│   └── guide.py                # Health guide & reference
│
├── storage/                    # Data Persistence Layer
│   ├── __init__.py
│   ├── database.py             # Supabase connection manager
│   ├── health_repository.py    # Health records CRUD
│   ├── context_repository.py   # User context CRUD
│   └── health_data_fetcher.py  # Data retrieval utilities
│
├── vision/                     # Computer Vision Module
│   ├── __init__.py
│   ├── camera.py               # Webcam streaming
│   ├── person_detection.py     # HOG-based person detection
│   ├── feature_extraction.py   # Movement analysis
│   └── activity_runner.py      # Activity test coordinator
│
└── auth/                       # Authentication Module
    ├── __init__.py
    └── supabase_auth.py        # Supabase auth integration
```

### Key Files Explained

#### `app.py` - Main Application
- Streamlit app entry point
- Navigation sidebar
- Page routing logic
- Session state management
- Authentication flow

#### `agents/orchestrator.py` - ADK Brain
- Coordinates all 5 agents
- Manages data flow between agents
- Error handling and fallbacks
- Result consolidation

#### `pages/ai_health_chat.py` - AI Interface
- Gemini AI integration
- Real-time health data fetching
- PDF report generation
- Health search functionality

#### `pages/daily_health_check.py` - Health Tests
- Camera integration
- 3 activity tests (Movement, Stability, Sit-Stand)
- Real-time feature extraction
- Score calculation and rating

---

## 🔄 Data Flow & Workflow

### User Journey Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    USER WORKFLOW                             │
│                                                              │
│  1. SIGNUP/LOGIN                                             │
│     ├─→ Supabase Authentication                              │
│     └─→ Create user profile                                  │
│                                                              │
│  2. SETUP CONTEXT                                            │
│     ├─→ Enter personal info (age, conditions)               │
│     ├─→ Upload medical reports (optional)                   │
│     └─→ Set lifestyle factors (sleep, stress)               │
│                                                              │
│  3. DAILY HEALTH CHECK                                       │
│     ├─→ Movement Speed Test (45 sec walking)                │
│     ├─→ Stability Test (30 sec standing)                    │
│     ├─→ Sit-Stand Test (30 sec transitions)                 │
│     └─→ Results saved to database                           │
│                                                              │
│  4. VIEW DASHBOARD                                           │
│     ├─→ See health trends over time                         │
│     ├─→ Compare against baseline                            │
│     └─→ Track progress visually                             │
│                                                              │
│  5. AI HEALTH ANALYSIS                                       │
│     ├─→ Request AI analysis (7/14/30 days)                  │
│     ├─→ ADK Pipeline processes data                         │
│     ├─→ View comprehensive report                           │
│     └─→ Download PDF report                                 │
│                                                              │
│  6. AI CHAT                                                  │
│     ├─→ Ask health questions                                │
│     ├─→ Get personalized insights                           │
│     └─→ Search health information                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow Diagram

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Webcam     │────▶│   OpenCV     │────▶│   Feature    │
│   Input      │     │   Process    │     │   Extract    │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                  │
                                                  ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Supabase   │◀────│   Storage    │◀────│   Metrics    │
│   Database   │     │   Module     │     │   Scores     │
└──────────────┘     └──────────────┘     └──────────────┘
        │
        ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Fetch      │────▶│   ADK        │────▶│   Analysis   │
│   History    │     │   Pipeline   │     │   Results    │
└──────────────┘     └──────────────┘     └──────────────┘
                                                  │
                                                  ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   PDF        │◀────│   Care       │◀────│   User       │
│   Report     │     │   Recommend  │     │   Interface  │
└──────────────┘     └──────────────┘     └──────────────┘
```

---

## 🔐 Security & Authentication

### Authentication Flow

```
┌─────────────────────────────────────────────────────────────┐
│                 AUTHENTICATION FLOW                          │
│                                                              │
│  1. User enters email + password                             │
│                    │                                         │
│                    ▼                                         │
│  2. Supabase Auth validates credentials                      │
│                    │                                         │
│         ┌─────────┴─────────┐                               │
│         │                    │                               │
│         ▼                    ▼                               │
│     SUCCESS              FAILURE                             │
│         │                    │                               │
│         ▼                    ▼                               │
│  3. JWT Token issued    Error message                        │
│         │                                                    │
│         ▼                                                    │
│  4. Session stored in st.session_state                       │
│         │                                                    │
│         ▼                                                    │
│  5. User ID used for all data operations                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Security Measures

| Feature | Implementation |
|---------|----------------|
| **Password Hashing** | Supabase Auth (bcrypt) |
| **JWT Tokens** | Supabase session management |
| **Row Level Security** | PostgreSQL RLS policies |
| **API Key Protection** | Environment variables (.env) |
| **HTTPS** | Streamlit Cloud SSL |
| **Data Isolation** | user_id based filtering |

---

## 🚀 Deployment Guide

### Local Development

```bash
# 1. Clone repository
git clone https://github.com/your-repo/AI_Agent.git
cd AI_Agent

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# 5. Run application
streamlit run app.py
```

### Streamlit Cloud Deployment

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Deploy to Streamlit Cloud"
   git push origin main
   ```

2. **Connect to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect GitHub repository
   - Select `app.py` as main file

3. **Configure Secrets**
   - Add all `.env` variables to Streamlit Secrets
   - Format: `VARIABLE_NAME = "value"`

### Required Files for Deployment

| File | Purpose |
|------|---------|
| `requirements.txt` | Python package dependencies |
| `packages.txt` | System-level dependencies (apt) |
| `.streamlit/config.toml` | Streamlit configuration (optional) |

---

## ⚙️ Environment Configuration

### Required Environment Variables

```bash
# .env file

# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key

# Google Gemini AI
GEMINI_API_KEY=your-gemini-api-key

# Optional: Google Search (for health search feature)
GOOGLE_API_KEY=your-google-api-key
GOOGLE_SEARCH_ENGINE_ID=your-search-engine-id
```

### Streamlit Secrets Format

```toml
# .streamlit/secrets.toml

SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-supabase-anon-key"
GEMINI_API_KEY = "your-gemini-api-key"
```

---

## 📊 Health Metrics Reference

### Score Interpretation

| Score Range | Rating | Color | Meaning |
|-------------|--------|-------|---------|
| 85% - 100% | Excellent | 🟢 Green | Outstanding performance |
| 75% - 84% | Good | ✅ Green | Healthy, normal range |
| 65% - 74% | Fair | 🟡 Yellow | Some decline, monitor |
| < 65% | Needs Attention | 🔴 Red | Consult healthcare provider |

### Metrics Measured

| Metric | Test | What It Measures |
|--------|------|------------------|
| Movement Speed | Walking Test | Pace, gait, mobility |
| Stability | Standing Test | Balance, steadiness |
| Sit-Stand Speed | Chair Test | Lower body strength, mobility |

---

## 📞 Support & Contact

**MediGuard Drift AI**  
Version 2.0.0  
© 2025 MediGuard - All Rights Reserved

---

*This document is auto-generated and maintained as part of the MediGuard Drift AI project.*
