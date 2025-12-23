# Health Score Rating System - Quick Reference

## 📊 Rating Categories

### 🟢 EXCELLENT (85-100%)
**Color:** Green (#4CAF50)  
**Emoji:** 🟢  
**Meaning:** Optimal performance, no concerns  
**Action:** Keep up current healthy habits

**Thresholds by Metric:**
- Movement Speed: ≥0.90 (≥90%)
- Stability: ≥0.85 (≥85%)
- Sit-Stand Speed: ≥0.85 (≥85%)

---

### ✅ GOOD (75-84%)
**Color:** Light Green (#8BC34A)  
**Emoji:** ✅  
**Meaning:** Healthy range, normal function  
**Action:** Continue regular activity and monitoring

**Thresholds by Metric:**
- Movement Speed: 0.80-0.89 (80-89%)
- Stability: 0.75-0.84 (75-84%)
- Sit-Stand Speed: 0.75-0.84 (75-84%)

---

### 🟡 FAIR (65-74%)
**Color:** Yellow (#FFC107)  
**Emoji:** 🟡  
**Meaning:** Below ideal, worth monitoring closely  
**Action:** Consider gentle exercises, track for changes

**Thresholds by Metric:**
- Movement Speed: 0.70-0.79 (70-79%)
- Stability: 0.65-0.74 (65-74%)
- Sit-Stand Speed: 0.65-0.74 (65-74%)

---

### 🟠 NEEDS ATTENTION (<65%)
**Color:** Orange (#FF9800)  
**Emoji:** 🟠  
**Meaning:** Significantly below normal, requires attention  
**Action:** Consult with doctor about these results

**Thresholds by Metric:**
- Movement Speed: <0.70 (<70%)
- Stability: <0.65 (<65%)
- Sit-Stand Speed: <0.65 (<65%)

---

## 📏 Metric-Specific Descriptions

### 🏃 Movement Speed

| Score | Rating | Description |
|-------|--------|-------------|
| ≥0.90 | 🟢 Excellent | Moving quickly and efficiently |
| 0.80-0.89 | ✅ Good | Healthy movement, nothing concerning |
| 0.70-0.79 | 🟡 Fair | Slower than ideal, worth monitoring |
| <0.70 | 🟠 Needs Attention | Significant slowness, consider check-up |

### ⚖️ Stability

| Score | Rating | Description |
|-------|--------|-------------|
| ≥0.85 | 🟢 Excellent | Very steady, low fall risk |
| 0.75-0.84 | ✅ Good | Mostly stable, acceptable range |
| 0.65-0.74 | 🟡 Fair | Some wobbliness, watch closely |
| <0.65 | 🟠 Needs Attention | Unsteady, higher fall risk |

### 🪑 Sit-Stand Speed

| Score | Rating | Description |
|-------|--------|-------------|
| ≥0.85 | 🟢 Excellent | Stand up quickly and easily |
| 0.75-0.84 | ✅ Good | Normal speed, no issues |
| 0.65-0.74 | 🟡 Fair | Taking longer, may indicate weakness |
| <0.65 | 🟠 Needs Attention | Struggling to stand, check with doctor |

---

## 🎯 Example Classifications

### Example 1: High Performer
```
Movement Speed: 0.923 → 🟢 Excellent (Moving quickly and efficiently)
Stability: 0.891 → 🟢 Excellent (Very steady, low fall risk)
Sit-Stand: 0.876 → 🟢 Excellent (Stand up quickly and easily)
```
**Overall:** All metrics excellent - keep up the great work! 🎉

### Example 2: Normal Range
```
Movement Speed: 0.845 → ✅ Good (Healthy movement, nothing concerning)
Stability: 0.782 → ✅ Good (Mostly stable, acceptable range)
Sit-Stand: 0.798 → ✅ Good (Normal speed, no issues)
```
**Overall:** All metrics in healthy range - continue monitoring 👍

### Example 3: Mixed Results (Like Your Screenshot)
```
Movement Speed: 0.023 → 🟠 Needs Attention (Significant slowness)
Stability: 1.000 → 🟢 Excellent (Very steady, low fall risk)
Sit-Stand: 0.030 → 🟠 Needs Attention (Struggling to stand)
```
**Overall:** Excellent stability but concerning movement scores - consult doctor ⚠️

### Example 4: Monitoring Needed
```
Movement Speed: 0.734 → 🟡 Fair (Slower than ideal, worth monitoring)
Stability: 0.698 → 🟡 Fair (Some wobbliness, watch closely)
Sit-Stand: 0.712 → 🟡 Fair (Taking longer, may indicate weakness)
```
**Overall:** All metrics fair - track trends and consider gentle exercise 📊

---

## 🏥 Medical Guidance

### When to Take Action

#### 🟢 Excellent / ✅ Good
- **Frequency:** Continue regular health checks
- **Action:** Maintain current activity level
- **Doctor Visit:** Only for routine checkups

#### 🟡 Fair
- **Frequency:** Monitor more closely (every 2-3 days)
- **Action:** Increase gentle exercise, track trends
- **Doctor Visit:** If scores decline or stay fair for 2+ weeks

#### 🟠 Needs Attention
- **Frequency:** Daily monitoring recommended
- **Action:** Immediate medical consultation
- **Doctor Visit:** Schedule appointment within 1-2 days

### Red Flags (Seek Immediate Medical Help)
1. ⚠️ Multiple "Needs Attention" scores
2. ⚠️ Sudden drop from Good/Excellent to Fair/Needs Attention
3. ⚠️ Accompanied by falls, dizziness, or pain
4. ⚠️ Difficulty performing daily activities
5. ⚠️ Progressive worsening over several days

---

## 🔄 Score Conversion

### Decimal to Percentage
```
0.00 = 0%
0.25 = 25%
0.50 = 50%
0.65 = 65% (Fair threshold)
0.75 = 75% (Good threshold)
0.85 = 85% (Excellent threshold)
1.00 = 100%
```

### Your Screenshot Values
```
Movement Speed: 0.023 = 2.3% = 🟠 Needs Attention
Stability: 1.000 = 100% = 🟢 Excellent  
Sit-Stand: 0.030 = 3.0% = 🟠 Needs Attention
```

---

## 💡 Tips for Patients

1. **Focus on Trends:** One bad day doesn't define you - look at patterns over time
2. **Context Matters:** Consider sleep, stress, time of day, recent activity
3. **Consistency:** Take tests at similar times for better comparison
4. **Don't Panic:** Fair/Needs Attention doesn't mean emergency - it means "let's check this out"
5. **Celebrate Progress:** Improvements from Fair to Good are victories!
6. **Track Overall:** Look at all three metrics together, not in isolation

---

## 📱 Implementation Details

### Where Ratings Appear
1. ✅ After each individual test completion
2. ✅ In the final summary (3-card layout)
3. ✅ On dashboard charts (with expandable guides)
4. ✅ In AI chat responses about health data
5. ✅ In exported reports (future feature)

### Technical Details
- **Function:** `rate_metric_value()` in `agents/ai_integration.py`
- **Inputs:** metric name (string), value (0.0-1.0 float)
- **Outputs:** rating, emoji, color hex, description
- **Usage:** Imported wherever health metrics displayed

---

**Remember:** These ratings help you understand your health journey. They're tools for awareness and action, not judgments! 💪
