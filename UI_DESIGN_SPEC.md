# 🎨 UI DESIGN SPECIFICATION - Health Search Feature

## Visual Layout Description

### 1. HEADER SECTION
```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║  🌐 AI Health Assistant with Google Search                   ║
║                                                               ║
║  Get evidence-based health information from trusted medical  ║
║  sources. Ask questions about conditions, symptoms,          ║
║  treatments, exercises, or preventive care.                  ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```
**Style:**
- Background: Linear gradient (135deg, #667eea → #764ba2)
- Text color: White (#FFFFFF)
- Padding: 1.5rem all sides
- Border radius: 12px
- Font: Bold header (h4), regular body text

---

### 2. SEARCH INPUT SECTION
```
┌─────────────────────────────────────────────┬─────────────┐
│  e.g., What are the best exercises for     │   🔍 Search  │
│       balance improvement?                  │              │
└─────────────────────────────────────────────┴─────────────┘
```
**Style:**
- Input: 75% width, white background
- Button: 25% width, primary blue color
- Height: Standard input height
- Placeholder: Gray italic text

---

### 3. QUICK TOPIC BUTTONS
```
┌──────────────┬──────────────┬──────────────┬──────────────┐
│              │              │              │              │
│ 🧘 Balance   │ 🚶 Fall      │ 💪 Mobility  │ 🧠 Cognitive │
│   Exercises  │   Prevention │              │   Health     │
│              │              │              │              │
└──────────────┴──────────────┴──────────────┴──────────────┘
```
**Style:**
- 4 equal-width columns
- Button background: Light gray (#F5F5F5)
- Hover: Darker gray (#E0E0E0)
- Padding: 0.75rem vertical
- Border radius: 8px
- Font: Emoji + text, centered

---

### 4. RESULTS HEADER
```
──────────────────────────────────────────────────────────────

📚 Results for: "balance exercises for seniors"

──────────────────────────────────────────────────────────────
```
**Style:**
- Separator lines: Light gray
- Title: Large font (1.5rem), semi-bold
- Query text: Italic, purple color (#667eea)

---

### 5. MAIN RESPONSE CARD
```
┌───────────────────────────────────────────────────────────┐
│ ┃                                                          │
│ ┃  Balance exercises are crucial for preventing falls... │
│ ┃                                                          │
│ ┃  Recommended Exercises:                                 │
│ ┃  1. Single-leg stands                                   │
│ ┃  2. Heel-to-toe walk                                    │
│ ┃  3. Chair squats                                        │
│ ┃                                                          │
│ ┃  Safety Tips:                                           │
│ ┃  - Start near a wall or chair for support              │
│ ┃  - Practice in a clear space                           │
│ ┃  - Progress gradually                                   │
│ ┃                                                          │
└───────────────────────────────────────────────────────────┘
```
**Style:**
- Background: Light gray (#F8F9FA)
- Border-left: 4px solid purple (#667eea)
- Padding: 1.5rem all sides
- Border radius: 12px
- Font: Regular (1rem), line height 1.6
- Numbered lists and bullet points formatted

---

### 6. SOURCES SECTION HEADER
```
──────────────────────────────────────────────────────────────

🔗 Sources & References

──────────────────────────────────────────────────────────────
```
**Style:**
- Same as Results Header style
- Icon: Link emoji

---

### 7. SOURCE CARDS (CLICKABLE)
```
┌──────────────────────────────────────────────────────────┐
│  ┌──┐                                                  →  │
│  │ 1│  Balance Exercises for Seniors - Mayo Clinic       │
│  └──┘  https://mayoclinic.org/healthy-lifestyle/fit...  │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│  ┌──┐                                                  →  │
│  │ 2│  Fall Prevention Guide - NIH                        │
│  └──┘  https://nih.gov/health/falls-prevention...        │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│  ┌──┐                                                  →  │
│  │ 3│  Senior Balance Training - Cleveland Clinic        │
│  └──┘  https://clevelandclinic.org/health/article...     │
└──────────────────────────────────────────────────────────┘
```
**Style:**
- Background: White (#FFFFFF)
- Border: 1px solid light gray (#E0E0E0)
- Box shadow: 0 2px 4px rgba(0,0,0,0.05)
- Border radius: 8px
- Padding: 1rem
- Margin bottom: 0.5rem

**Number Badge:**
- Background: Purple (#667eea)
- Color: White
- Size: 28px circle
- Font: Bold, centered
- Margin right: 1rem

**Title Link:**
- Color: Purple (#667eea)
- Font weight: 600 (semi-bold)
- Font size: 1rem
- Hover: Underline

**URL Text:**
- Color: Gray (#666)
- Font size: 0.85rem
- Truncated with ellipsis if > 80 chars
- Word break: break-all

**Arrow Indicator:**
- Color: Purple (#667eea)
- Font size: 1.2rem
- Position: Right side

---

### 8. ACTION BUTTONS
```
┌────────────────┬────────────────┬────────────────┐
│                │                │                │
│  📋 Copy       │  🔄 New        │  💬 Ask        │
│     Response   │     Search     │     Follow-up  │
│                │                │                │
└────────────────┴────────────────┴────────────────┘
```
**Style:**
- 3 equal-width columns
- Button background: White with border
- Hover: Light purple background
- Padding: 0.75rem vertical
- Border radius: 8px
- Font: Emoji + text, centered
- Border: 1px solid gray

---

## COLOR PALETTE

### Primary Colors:
- **Purple Gradient Start:** #667eea
- **Purple Gradient End:** #764ba2
- **Primary Blue:** #4A90E2 (Streamlit default)
- **Link Purple:** #667eea

### Background Colors:
- **Card Background:** #F8F9FA
- **White Background:** #FFFFFF
- **Light Gray:** #F5F5F5
- **Border Gray:** #E0E0E0

### Text Colors:
- **Primary Text:** #333333
- **Secondary Text:** #666666
- **White Text:** #FFFFFF

### Accent Colors:
- **Success Green:** #28A745
- **Warning Yellow:** #FFC107
- **Error Red:** #DC3545
- **Info Blue:** #17A2B8

---

## TYPOGRAPHY

### Font Family:
- Default: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif

### Font Sizes:
- **Header (h4):** 1.5rem (24px)
- **Subheader:** 1.25rem (20px)
- **Body:** 1rem (16px)
- **Small:** 0.85rem (13.6px)
- **Caption:** 0.75rem (12px)

### Font Weights:
- **Bold:** 700
- **Semi-bold:** 600
- **Regular:** 400
- **Light:** 300

### Line Heights:
- **Headers:** 1.3
- **Body text:** 1.6
- **Compact:** 1.4

---

## SPACING

### Margins:
- **Large:** 2rem (32px)
- **Medium:** 1rem (16px)
- **Small:** 0.5rem (8px)

### Padding:
- **Cards:** 1.5rem (24px)
- **Buttons:** 0.75rem vertical, 1rem horizontal
- **Input fields:** 0.5rem (8px)

### Border Radius:
- **Large cards:** 12px
- **Small cards:** 8px
- **Buttons:** 8px
- **Circles:** 50%

---

## INTERACTIVE STATES

### Hover Effects:
- **Buttons:** Background color darkens 10%
- **Links:** Underline appears
- **Cards:** Box shadow increases slightly

### Active States:
- **Buttons:** Background color darkens 20%
- **Input focus:** Blue border (2px)

### Disabled States:
- **Opacity:** 0.5
- **Cursor:** not-allowed
- **Background:** Gray (#CCCCCC)

---

## RESPONSIVE BEHAVIOR

### Desktop (> 768px):
- Full width cards
- 4-column quick topics
- 3-column action buttons

### Tablet (480px - 768px):
- 2-column quick topics
- Full width action buttons

### Mobile (< 480px):
- Single column layout
- Stacked quick topics
- Full width buttons

---

## ACCESSIBILITY

### WCAG Compliance:
- **Color Contrast:** All text meets WCAG AA standards (4.5:1 minimum)
- **Focus Indicators:** Clear blue outline on keyboard focus
- **Alt Text:** All icons have descriptive text
- **Clickable Areas:** Minimum 44x44px touch targets

### Screen Reader Support:
- Semantic HTML structure
- ARIA labels on interactive elements
- Clear heading hierarchy
- Descriptive link text

---

## ANIMATIONS (Optional Future)

### Suggested Animations:
- **Search button:** Spin on click (0.5s)
- **Source cards:** Fade in from bottom (0.3s stagger)
- **Hover effects:** Smooth transition (0.2s)
- **Loading state:** Pulsing gradient animation

---

This specification ensures consistent, beautiful, and accessible UI across the Health Search feature!
