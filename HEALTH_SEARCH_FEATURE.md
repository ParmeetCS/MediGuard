# Health Information Search Feature

## 🌐 ADK-Powered Health Assistant with Google Search

### Overview
A new AI Health Assistant agent that uses Google's ADK (Agent Development Kit) with **Google Search Grounding** to provide evidence-based health information from trusted medical sources.

---

## ✨ Key Features

### 1. **Google Search Grounding**
- Real-time access to current medical information
- Sources from trusted health websites (Mayo Clinic, NIH, CDC, WebMD, etc.)
- Evidence-based responses with citations

### 2. **Beautiful User Interface**
- 🎨 Gradient header with clear instructions
- 🔍 Smart search box with quick topic buttons
- 📚 Organized source display with clickable links
- 💬 Action buttons (Copy, New Search, Follow-up)

### 3. **Quick Topics**
Pre-configured searches for common health concerns:
- 🧘 **Balance Exercises** - Best exercises for balance and fall prevention
- 🚶 **Fall Prevention** - Strategies to prevent falls at home
- 💪 **Mobility** - Exercises to improve flexibility and movement
- 🧠 **Cognitive Health** - Brain exercises and cognitive activities

### 4. **Context-Aware Responses**
- Personalizes answers based on user's age
- Considers tracked health conditions
- References user's health check history

---

## 🏗️ Technical Architecture

### Files Created/Modified

#### **New Files:**
1. **`agents/health_search_agent.py`** (400 lines)
   - `HealthSearchAgent` class with Google Search grounding
   - Methods: `search_health_info()`, `get_health_resources()`, `explain_health_term()`
   - Automatic source extraction and citation
   - Error handling and safety filters

2. **`test_health_search.py`** (80 lines)
   - Test suite for search functionality
   - Validates basic search, context-aware search, resources, and term explanation

#### **Modified Files:**
1. **`pages/ai_health_chat.py`**
   - Added Health Information Search section
   - Beautiful gradient UI with search interface
   - Quick topic buttons for common searches
   - Source display with clickable cards
   - Action buttons for user interaction

2. **`requirements.txt`**
   - Added `google-generativeai` (for ADK + Search grounding)
   - Added `plotly` (for dashboard graphs)

---

## 🎯 How It Works

### User Flow:
1. **User visits AI Health Chat page**
2. **Sees "Health Information Search" section** with gradient purple header
3. **Types question** or clicks quick topic button
4. **Agent searches Google** using Gemini with grounding
5. **Beautiful results displayed:**
   - Main response in bordered card
   - Clickable source links with icons
   - Action buttons for next steps

### Behind the Scenes:
```python
# Agent uses Gemini 2.0 with Google Search grounding
model = genai.GenerativeModel(
    model_name="models/gemini-2.0-flash-exp",
    tools='google_search_retrieval'  # Enable Google Search
)

# Searches and returns structured response with sources
result = search_health_info("balance exercises", user_context)
```

---

## 🎨 UI Components

### 1. **Gradient Header**
```
Purple gradient (667eea → 764ba2)
"AI Health Assistant with Google Search"
Clear description of capability
```

### 2. **Search Box**
```
3:1 column ratio
Text input with placeholder
Primary "Search" button
```

### 3. **Quick Topic Buttons**
```
4 equal-width buttons
Icons + descriptive text
Instant query loading
```

### 4. **Source Cards**
```
White background with subtle shadow
Numbered circles (1, 2, 3...)
Clickable title links
URL preview (truncated)
Arrow indicator →
```

### 5. **Action Buttons**
```
Copy Response - Shows code block for copying
New Search - Clears query and refreshes
Ask Follow-up - Prompts user guidance
```

---

## 🔧 Configuration

### Environment Variables (.env):
```bash
GOOGLE_API_KEY=your_google_api_key_here
```

### Model Configuration:
- **Model:** `gemini-2.0-flash-exp`
- **Tools:** `google_search_retrieval`
- **Temperature:** 0.7 (balanced creativity)
- **Max Tokens:** 2048 (comprehensive responses)

---

## 📊 Example Queries

### Excellent Questions:
✅ "What are the best exercises for improving balance in seniors?"
✅ "How can I prevent falls at home?"
✅ "Explain proprioception in simple terms"
✅ "What causes dizziness when standing up?"
✅ "Exercises to strengthen legs for better mobility"

### System Handles Well:
- General health questions
- Exercise recommendations
- Medical term explanations
- Preventive care advice
- Lifestyle modifications

### System Disclaims:
- Personal medical diagnosis
- Specific treatment plans
- Emergency medical situations
- Prescription medication advice

---

## 🛡️ Safety Features

### 1. **Clear Disclaimers**
- Not a replacement for medical advice
- Recommends consulting healthcare professionals
- Emphasizes emergency services when needed

### 2. **Safety Filters**
- Gemini safety settings enabled
- Blocks harmful/dangerous content
- Filters inappropriate health claims

### 3. **Source Verification**
- Prioritizes trusted medical sources
- Shows clickable source links
- Users can verify information independently

---

## 🚀 Future Enhancements

### Possible Additions:
1. **Search History** - Save and recall previous searches
2. **Bookmarking** - Save useful resources for later
3. **Follow-up Questions** - Automatic related questions
4. **PDF Export** - Download search results as PDF
5. **Voice Search** - Speech-to-text for queries
6. **Multi-language** - Support for different languages
7. **Image Search** - Visual exercises and diagrams

---

## 📝 Usage Instructions

### For Users:
1. Navigate to **AI Health Chat** page
2. Scroll to **Health Information Search** section
3. Type your health question OR click a Quick Topic
4. Click **🔍 Search** button
5. Read the response and check sources
6. Click source links to read full articles
7. Use action buttons for next steps

### For Developers:
```python
# Import the agent
from agents.health_search_agent import search_health_info

# Basic search
result = search_health_info("balance exercises")

# With user context
result = search_health_info(
    "balance exercises",
    user_context={'age': 65, 'health_conditions': 'monitoring balance'}
)

# Check result
if result['success']:
    print(result['response'])
    for source in result['sources']:
        print(f"{source['title']}: {source['url']}")
```

---

## 🧪 Testing

### Run Test Suite:
```bash
python test_health_search.py
```

### Expected Output:
- ✅ Basic search test passes
- ✅ Context-aware search works
- ✅ Resource retrieval successful
- ✅ Term explanation clear

### Requirements:
- Valid `GOOGLE_API_KEY` in `.env`
- Internet connection
- Google API quota available

---

## 📈 Benefits

### For Users:
✅ Instant access to trusted health information
✅ Evidence-based answers with sources
✅ Beautiful, easy-to-use interface
✅ Clickable links to read more
✅ No need to Google search manually

### For Platform:
✅ Adds significant value to health app
✅ Increases user engagement
✅ Provides educational content
✅ Complements health tracking features
✅ Positions app as comprehensive health assistant

---

## ⚠️ Important Notes

1. **This is NOT medical advice** - Always emphasize this to users
2. **API Quota** - Monitor Google API usage (free tier has limits)
3. **Internet Required** - Search feature needs active connection
4. **Source Quality** - Gemini prioritizes trusted sources but review results
5. **User Responsibility** - Users must verify information with healthcare providers

---

## 🎉 Summary

The **Health Information Search** feature transforms the AI Health Chat page into a comprehensive health assistant. Users can:
- 🔍 Search trusted medical sources instantly
- 📚 Get evidence-based answers with citations
- 🔗 Access clickable links to full articles
- 💬 Ask follow-up questions
- 🎨 Enjoy a beautiful, intuitive interface

This feature bridges the gap between health tracking and health education, empowering users to understand their health better!
