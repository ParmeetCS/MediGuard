# 📊 MediGuard Workflows - Visual Diagrams

This document contains visual flowcharts for all major workflows in MediGuard.

---

## 1️⃣ User Onboarding Workflow

```mermaid
graph TD
    A[User Visits App] --> B[Sign Up Page]
    B --> C[Enter Email & Password]
    C --> D[Supabase Authentication]
    D --> E{Email Verified?}
    E -->|No| F[Send Verification Email]
    F --> G[User Clicks Link]
    G --> E
    E -->|Yes| H[Profile Setup Page]
    H --> I[Enter Health Info]
    I --> J[Context Input Page]
    J --> K[Enter Lifestyle Data]
    K --> L[First Health Check]
    L --> M[Dashboard]
```

---

## 2️⃣ Daily Health Check Workflow

```mermaid
graph TD
    A[User Login] --> B[Navigate to Health Check]
    B --> C[Select Activity Type]
    C --> D{Camera Available?}
    D -->|Yes| E[WebRTC Connection]
    D -->|No| F[Upload Video Option]
    E --> G{Connection Success?}
    G -->|Yes| H[Live Camera Recording]
    G -->|No| F
    F --> I[User Uploads Video]
    H --> J[Capture Frames]
    I --> K[Extract Frames from Video]
    J --> L[Feature Extraction]
    K --> L
    L --> M[Calculate Metrics]
    M --> N[Display Results]
    N --> O[Save to Database]
    O --> P[Update Dashboard]
```

---

## 3️⃣ Multi-Agent AI Pipeline

```mermaid
graph TD
    A[Health Data Input] --> B[Orchestrator]
    B --> C[Agent 1: Drift Agent]
    C --> D[Detect Metric Changes]
    D --> E[Calculate Trends]
    E --> F[Agent 2: Context Agent]
    F --> G[Fetch Lifestyle Data]
    G --> H[Correlate Factors]
    H --> I[Agent 3: Risk Agent]
    I --> J[Assess Risk Level]
    J --> K[Calculate Urgency]
    K --> L[Agent 4: Safety Agent]
    L --> M{Medical Escalation Needed?}
    M -->|Yes| N[Flag for Doctor]
    M -->|No| O[Agent 5: Care Agent]
    N --> O
    O --> P[Generate Recommendations]
    P --> Q[Synthesize Response]
    Q --> R[Display to User]
```

---

## 4️⃣ AI Health Chat Workflow

```mermaid
graph TD
    A[User Asks Question] --> B[Parse Intent]
    B --> C[Fetch User Health Data]
    C --> D[Build Context]
    D --> E[Send to Gemini AI]
    E --> F{Query Type?}
    F -->|Trend| G[Generate Chart]
    F -->|Comparison| H[Create Table]
    F -->|Advice| I[List Recommendations]
    F -->|General| J[Text Response]
    G --> K[Enhance with Visualizations]
    H --> K
    I --> K
    J --> K
    K --> L[Format Response]
    L --> M[Display to User]
    M --> N[Save to Chat History]
```

---

## 5️⃣ Data Storage Workflow

```mermaid
graph TD
    A[Activity Completed] --> B[Extract Features]
    B --> C[Movement Speed]
    B --> D[Stability Score]
    B --> E[Motion Smoothness]
    C --> F[Validate Data]
    D --> F
    E --> F
    F --> G{Valid?}
    G -->|No| H[Show Error]
    G -->|Yes| I[Transform Data]
    I --> J[Add User ID]
    J --> K[Add Timestamp]
    K --> L[Supabase Insert]
    L --> M{Success?}
    M -->|No| N[Retry 3x]
    N --> M
    M -->|Yes| O[Show Confirmation]
    O --> P[Update UI]
```

---

## 6️⃣ WebRTC Video Processing

```mermaid
graph TD
    A[Start Recording] --> B[Request Camera Permission]
    B --> C{Permission Granted?}
    C -->|No| D[Show Error]
    C -->|Yes| E[Load ICE Servers]
    E --> F[Try STUN Connection]
    F --> G{Connected?}
    G -->|No| H[Try TURN Server]
    H --> I{Connected?}
    I -->|No| J[Offer Upload Option]
    I -->|Yes| K[Start Video Stream]
    G -->|Yes| K
    K --> L[Capture Frames 30 FPS]
    L --> M[Sample Every 3rd Frame]
    M --> N[Convert BGR to RGB]
    N --> O[Store in Memory]
    O --> P{Duration Complete?}
    P -->|No| L
    P -->|Yes| Q[Stop Recording]
    Q --> R[Process Frames]
```

---

## 7️⃣ Video Upload Processing

```mermaid
graph TD
    A[User Selects Video] --> B[Validate File Type]
    B --> C{Valid Format?}
    C -->|No| D[Show Error]
    C -->|Yes| E[Check File Size]
    E --> F{Size < 50MB?}
    F -->|No| D
    F -->|Yes| G[Create Temp File]
    G --> H[Write Video Data]
    H --> I[Open with OpenCV]
    I --> J[Read Frame]
    J --> K{More Frames?}
    K -->|Yes| L[Sample Frame]
    L --> M[Convert to RGB]
    M --> N[Store Frame]
    N --> J
    K -->|No| O[Close Video]
    O --> P[Delete Temp File]
    P --> Q[Process Frames]
    Q --> R[Extract Features]
```

---

## 8️⃣ Error Handling Flow

```mermaid
graph TD
    A[Error Occurs] --> B{Error Type?}
    B -->|WebRTC Timeout| C[Show Warning]
    C --> D[Enable Upload Option]
    D --> E[Guide User]
    B -->|Database Error| F[Retry Insert]
    F --> G{Success?}
    G -->|No| H[Log Error]
    H --> I[Notify User]
    G -->|Yes| J[Continue]
    B -->|AI API Error| K{Error Code?}
    K -->|Quota| L[Show Quota Message]
    K -->|Network| M[Retry Request]
    K -->|Safety| N[Use Fallback Response]
    L --> O[Suggest Retry Later]
    M --> P{Success?}
    P -->|Yes| J
    P -->|No| O
    N --> J
```

---

## 9️⃣ Authentication Flow

```mermaid
graph TD
    A[User Action] --> B{Action Type?}
    B -->|Sign Up| C[Collect Email/Password]
    C --> D[Validate Input]
    D --> E{Valid?}
    E -->|No| F[Show Validation Error]
    E -->|Yes| G[Supabase Sign Up]
    G --> H{Success?}
    H -->|No| I[Show Error Message]
    H -->|Yes| J[Send Verification Email]
    J --> K[Wait for Verification]
    B -->|Sign In| L[Collect Credentials]
    L --> M[Supabase Sign In]
    M --> N{Authenticated?}
    N -->|No| O[Show Login Error]
    N -->|Yes| P[Create Session]
    P --> Q[Redirect to Dashboard]
    B -->|Sign Out| R[Clear Session]
    R --> S[Redirect to Home]
```

---

## 🔟 Feature Extraction Pipeline

```mermaid
graph TD
    A[Video Frames Array] --> B[Convert to Grayscale]
    B --> C[Frame Differencing]
    C --> D[Calculate Motion Values]
    D --> E[Compute Statistics]
    E --> F[Mean Motion]
    E --> G[Motion Std Dev]
    E --> H[Max/Min Motion]
    F --> I[Calculate Movement Speed]
    G --> J[Calculate Stability]
    H --> K[Calculate Range of Motion]
    D --> L[Track Velocity Changes]
    L --> M[Calculate Smoothness]
    I --> N[Normalize to 0-1]
    J --> N
    K --> N
    M --> N
    N --> O[Feature Vector Output]
```

---

## 1️⃣1️⃣ Database Schema Flow

```mermaid
graph TD
    A[User Data] --> B[users Table]
    B --> C[user_id PK]
    C --> D[email]
    C --> E[created_at]
    
    F[Health Check] --> G[health_records Table]
    G --> H[id PK]
    H --> I[user_id FK]
    I --> J[movement_speed]
    I --> K[stability]
    I --> L[date]
    
    M[Context Input] --> N[user_context Table]
    N --> O[id PK]
    O --> P[user_id FK]
    P --> Q[sleep_hours]
    P --> R[stress_level]
    P --> S[diet_quality]
```

---

## 1️⃣2️⃣ Complete System Architecture

```mermaid
graph TB
    subgraph "Frontend Layer"
        A[Streamlit UI]
        B[Pages]
        C[Components]
    end
    
    subgraph "Application Layer"
        D[Vision System]
        E[AI Agents]
        F[Auth System]
    end
    
    subgraph "Data Layer"
        G[Health Repository]
        H[Context Repository]
        I[Database Module]
    end
    
    subgraph "External Services"
        J[Supabase DB]
        K[Google Gemini AI]
        L[WebRTC TURN/STUN]
    end
    
    A --> B
    B --> C
    C --> D
    C --> E
    C --> F
    D --> G
    E --> H
    F --> I
    G --> J
    H --> J
    I --> J
    E --> K
    D --> L
```

---

**Note:** These diagrams use Mermaid syntax and will render as interactive flowcharts in GitHub, VS Code, and other Markdown viewers that support Mermaid.
