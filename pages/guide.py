"""
Health Guide Page - MediGuard Drift AI
Comprehensive guide explaining all health test parameters and score interpretations
"""

import streamlit as st


def show():
    """Display the Health Guide page with all test parameters and score ranges"""
    
    # Header
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 30px; border-radius: 15px; margin-bottom: 30px;'>
            <h1 style='color: white; margin: 0; text-align: center;'>📖 Health Test Guide</h1>
            <p style='color: white; text-align: center; margin-top: 10px; font-size: 1.2rem;'>
                Understand your health scores and what they mean
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Quick Score Legend
    st.markdown("## 🎯 Quick Score Reference")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style='background: #4CAF50; padding: 20px; border-radius: 12px; text-align: center; color: white;'>
            <div style='font-size: 2rem;'>🟢</div>
            <h3 style='margin: 10px 0 5px 0; color: white;'>EXCELLENT</h3>
            <div style='font-size: 1.5rem; font-weight: bold;'>0.85 - 1.00</div>
            <div style='font-size: 0.9rem; margin-top: 5px;'>85% - 100%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: #8BC34A; padding: 20px; border-radius: 12px; text-align: center; color: white;'>
            <div style='font-size: 2rem;'>✅</div>
            <h3 style='margin: 10px 0 5px 0; color: white;'>GOOD</h3>
            <div style='font-size: 1.5rem; font-weight: bold;'>0.75 - 0.84</div>
            <div style='font-size: 0.9rem; margin-top: 5px;'>75% - 84%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: #FFC107; padding: 20px; border-radius: 12px; text-align: center; color: #333;'>
            <div style='font-size: 2rem;'>🟡</div>
            <h3 style='margin: 10px 0 5px 0; color: #333;'>FAIR</h3>
            <div style='font-size: 1.5rem; font-weight: bold;'>0.65 - 0.74</div>
            <div style='font-size: 0.9rem; margin-top: 5px;'>65% - 74%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style='background: #FF9800; padding: 20px; border-radius: 12px; text-align: center; color: white;'>
            <div style='font-size: 2rem;'>🟠</div>
            <h3 style='margin: 10px 0 5px 0; color: white;'>NEEDS ATTENTION</h3>
            <div style='font-size: 1.5rem; font-weight: bold;'>Below 0.65</div>
            <div style='font-size: 0.9rem; margin-top: 5px;'>Below 65%</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ========================================
    # THE 3 TESTS
    # ========================================
    st.markdown("---")
    st.markdown("## 🧪 The Three Health Tests")
    
    # Test 1: Sit-to-Stand
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 3px; border-radius: 15px; margin: 20px 0;'>
        <div style='background: white; padding: 25px; border-radius: 12px;'>
            <h2 style='color: #667eea; margin-top: 0;'>🪑 Test 1: Sit-to-Stand Test</h2>
            <p style='font-size: 1.1rem; color: #555;'>
                <b>What you do:</b> Sit on a chair with arms crossed. Stand up fully, then sit back down.
            </p>
            <p style='color: #666;'>
                <b>What it measures:</b> Your leg strength, core stability, and ability to transition from sitting to standing position.
            </p>
            <p style='color: #666;'>
                <b>Why it matters:</b> This test reveals lower body strength and fall risk. Difficulty standing may indicate muscle weakness or balance issues.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sit-to-Stand Parameters Table
    st.markdown("#### 📊 Sit-to-Stand Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #667eea;'>
            <h4 style='color: #667eea; margin-top: 0;'>🏃 Movement Speed</h4>
            <p><b>What it measures:</b> How quickly you can stand up from sitting position</p>
            <table style='width: 100%; margin-top: 10px;'>
                <tr style='background: #4CAF50; color: white;'>
                    <td style='padding: 8px;'>🟢 Excellent</td>
                    <td style='padding: 8px;'>≥ 0.85</td>
                    <td style='padding: 8px;'>Stand up quickly and easily</td>
                </tr>
                <tr style='background: #8BC34A; color: white;'>
                    <td style='padding: 8px;'>✅ Good</td>
                    <td style='padding: 8px;'>0.75 - 0.84</td>
                    <td style='padding: 8px;'>Normal speed, no issues</td>
                </tr>
                <tr style='background: #FFC107; color: #333;'>
                    <td style='padding: 8px;'>🟡 Fair</td>
                    <td style='padding: 8px;'>0.65 - 0.74</td>
                    <td style='padding: 8px;'>Taking longer, may indicate weakness</td>
                </tr>
                <tr style='background: #FF9800; color: white;'>
                    <td style='padding: 8px;'>🟠 Needs Attention</td>
                    <td style='padding: 8px;'>< 0.65</td>
                    <td style='padding: 8px;'>Struggling to stand, consult doctor</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #26c6da;'>
            <h4 style='color: #26c6da; margin-top: 0;'>⚖️ Stability</h4>
            <p><b>What it measures:</b> How steady and balanced you are during the sit-stand transition</p>
            <table style='width: 100%; margin-top: 10px;'>
                <tr style='background: #4CAF50; color: white;'>
                    <td style='padding: 8px;'>🟢 Excellent</td>
                    <td style='padding: 8px;'>≥ 0.85</td>
                    <td style='padding: 8px;'>Very steady, no wobbling</td>
                </tr>
                <tr style='background: #8BC34A; color: white;'>
                    <td style='padding: 8px;'>✅ Good</td>
                    <td style='padding: 8px;'>0.75 - 0.84</td>
                    <td style='padding: 8px;'>Mostly stable, acceptable</td>
                </tr>
                <tr style='background: #FFC107; color: #333;'>
                    <td style='padding: 8px;'>🟡 Fair</td>
                    <td style='padding: 8px;'>0.65 - 0.74</td>
                    <td style='padding: 8px;'>Some unsteadiness noticed</td>
                </tr>
                <tr style='background: #FF9800; color: white;'>
                    <td style='padding: 8px;'>🟠 Needs Attention</td>
                    <td style='padding: 8px;'>< 0.65</td>
                    <td style='padding: 8px;'>Unsteady, higher fall risk</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Test 2: Balance/Stability Test
    st.markdown("""
    <div style='background: linear-gradient(135deg, #26c6da 0%, #00acc1 100%); 
                padding: 3px; border-radius: 15px; margin: 20px 0;'>
        <div style='background: white; padding: 25px; border-radius: 12px;'>
            <h2 style='color: #26c6da; margin-top: 0;'>⚖️ Test 2: Balance Test</h2>
            <p style='font-size: 1.1rem; color: #555;'>
                <b>What you do:</b> Stand still with feet together, hands at sides. Maintain balance and focus ahead.
            </p>
            <p style='color: #666;'>
                <b>What it measures:</b> Your ability to maintain steadiness while standing still without swaying.
            </p>
            <p style='color: #666;'>
                <b>Why it matters:</b> Good balance reduces fall risk and indicates strong core muscles and proper neurological function.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Balance Test Parameters Table
    st.markdown("#### 📊 Balance Test Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #667eea;'>
            <h4 style='color: #667eea; margin-top: 0;'>🏃 Movement Speed</h4>
            <p><b>What it measures:</b> How much you move while trying to stand still (less is better)</p>
            <table style='width: 100%; margin-top: 10px;'>
                <tr style='background: #4CAF50; color: white;'>
                    <td style='padding: 8px;'>🟢 Excellent</td>
                    <td style='padding: 8px;'>≥ 0.90</td>
                    <td style='padding: 8px;'>Almost no movement, very still</td>
                </tr>
                <tr style='background: #8BC34A; color: white;'>
                    <td style='padding: 8px;'>✅ Good</td>
                    <td style='padding: 8px;'>0.80 - 0.89</td>
                    <td style='padding: 8px;'>Minimal movement, healthy</td>
                </tr>
                <tr style='background: #FFC107; color: #333;'>
                    <td style='padding: 8px;'>🟡 Fair</td>
                    <td style='padding: 8px;'>0.70 - 0.79</td>
                    <td style='padding: 8px;'>Some swaying noticed</td>
                </tr>
                <tr style='background: #FF9800; color: white;'>
                    <td style='padding: 8px;'>🟠 Needs Attention</td>
                    <td style='padding: 8px;'>< 0.70</td>
                    <td style='padding: 8px;'>Significant movement/swaying</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #26c6da;'>
            <h4 style='color: #26c6da; margin-top: 0;'>⚖️ Stability</h4>
            <p><b>What it measures:</b> Overall balance and steadiness while standing</p>
            <table style='width: 100%; margin-top: 10px;'>
                <tr style='background: #4CAF50; color: white;'>
                    <td style='padding: 8px;'>🟢 Excellent</td>
                    <td style='padding: 8px;'>≥ 0.85</td>
                    <td style='padding: 8px;'>Rock solid, low fall risk</td>
                </tr>
                <tr style='background: #8BC34A; color: white;'>
                    <td style='padding: 8px;'>✅ Good</td>
                    <td style='padding: 8px;'>0.75 - 0.84</td>
                    <td style='padding: 8px;'>Good balance, acceptable</td>
                </tr>
                <tr style='background: #FFC107; color: #333;'>
                    <td style='padding: 8px;'>🟡 Fair</td>
                    <td style='padding: 8px;'>0.65 - 0.74</td>
                    <td style='padding: 8px;'>Some wobbliness, monitor</td>
                </tr>
                <tr style='background: #FF9800; color: white;'>
                    <td style='padding: 8px;'>🟠 Needs Attention</td>
                    <td style='padding: 8px;'>< 0.65</td>
                    <td style='padding: 8px;'>Unsteady, higher fall risk</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Test 3: Movement Test
    st.markdown("""
    <div style='background: linear-gradient(135deg, #66bb6a 0%, #43a047 100%); 
                padding: 3px; border-radius: 15px; margin: 20px 0;'>
        <div style='background: white; padding: 25px; border-radius: 12px;'>
            <h2 style='color: #66bb6a; margin-top: 0;'>🏃 Test 3: Movement Test</h2>
            <p style='font-size: 1.1rem; color: #555;'>
                <b>What you do:</b> Walk in place energetically or perform coordinated arm movements.
            </p>
            <p style='color: #666;'>
                <b>What it measures:</b> Your overall mobility, coordination, and movement efficiency.
            </p>
            <p style='color: #666;'>
                <b>Why it matters:</b> Shows your general mobility and functional fitness. Changes may indicate muscle weakness, joint issues, or neurological changes.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Movement Test Parameters Table
    st.markdown("#### 📊 Movement Test Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #66bb6a;'>
            <h4 style='color: #66bb6a; margin-top: 0;'>🏃 Movement Speed</h4>
            <p><b>What it measures:</b> How quickly and efficiently you can move</p>
            <table style='width: 100%; margin-top: 10px;'>
                <tr style='background: #4CAF50; color: white;'>
                    <td style='padding: 8px;'>🟢 Excellent</td>
                    <td style='padding: 8px;'>≥ 0.90</td>
                    <td style='padding: 8px;'>Moving quickly and efficiently</td>
                </tr>
                <tr style='background: #8BC34A; color: white;'>
                    <td style='padding: 8px;'>✅ Good</td>
                    <td style='padding: 8px;'>0.80 - 0.89</td>
                    <td style='padding: 8px;'>Healthy movement, no concerns</td>
                </tr>
                <tr style='background: #FFC107; color: #333;'>
                    <td style='padding: 8px;'>🟡 Fair</td>
                    <td style='padding: 8px;'>0.70 - 0.79</td>
                    <td style='padding: 8px;'>Slower than ideal, worth monitoring</td>
                </tr>
                <tr style='background: #FF9800; color: white;'>
                    <td style='padding: 8px;'>🟠 Needs Attention</td>
                    <td style='padding: 8px;'>< 0.70</td>
                    <td style='padding: 8px;'>Significant slowness, check-up advised</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #26c6da;'>
            <h4 style='color: #26c6da; margin-top: 0;'>⚖️ Stability</h4>
            <p><b>What it measures:</b> How controlled and coordinated your movements are</p>
            <table style='width: 100%; margin-top: 10px;'>
                <tr style='background: #4CAF50; color: white;'>
                    <td style='padding: 8px;'>🟢 Excellent</td>
                    <td style='padding: 8px;'>≥ 0.85</td>
                    <td style='padding: 8px;'>Very controlled, smooth</td>
                </tr>
                <tr style='background: #8BC34A; color: white;'>
                    <td style='padding: 8px;'>✅ Good</td>
                    <td style='padding: 8px;'>0.75 - 0.84</td>
                    <td style='padding: 8px;'>Good coordination, stable</td>
                </tr>
                <tr style='background: #FFC107; color: #333;'>
                    <td style='padding: 8px;'>🟡 Fair</td>
                    <td style='padding: 8px;'>0.65 - 0.74</td>
                    <td style='padding: 8px;'>Some shakiness in movement</td>
                </tr>
                <tr style='background: #FF9800; color: white;'>
                    <td style='padding: 8px;'>🟠 Needs Attention</td>
                    <td style='padding: 8px;'>< 0.65</td>
                    <td style='padding: 8px;'>Uncoordinated, consult doctor</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ========================================
    # ADDITIONAL PARAMETERS
    # ========================================
    st.markdown("---")
    st.markdown("## 📋 Additional Parameters Measured")
    
    with st.expander("🎯 Motion Smoothness", expanded=False):
        st.markdown("""
        **What it measures:** How smooth and fluid your movements are during each test.
        
        | Score Range | Rating | Meaning |
        |-------------|--------|---------|
        | ≥ 0.80 | 🟢 Excellent | Very smooth, fluid movements |
        | 0.60 - 0.79 | ✅ Good | Generally smooth with minor variations |
        | 0.40 - 0.59 | 🟡 Fair | Some jerky or irregular movements |
        | < 0.40 | 🟠 Needs Attention | Jerky, uncoordinated movements |
        
        **Why it matters:** Smooth movements indicate good muscle control and coordination. Jerky movements may suggest muscle weakness or neurological issues.
        """)
    
    with st.expander("📐 Posture Deviation", expanded=False):
        st.markdown("""
        **What it measures:** How much your posture deviates from ideal alignment during tests.
        
        ⚠️ **Note:** For this metric, **lower scores are better!**
        
        | Score Range | Rating | Meaning |
        |-------------|--------|---------|
        | < 0.15 | 🟢 Excellent | Excellent posture, minimal deviation |
        | 0.15 - 0.25 | ✅ Good | Good posture with slight variations |
        | 0.25 - 0.35 | 🟡 Fair | Noticeable posture issues |
        | > 0.35 | 🟠 Needs Attention | Significant posture problems |
        
        **Why it matters:** Good posture reduces strain on joints and muscles, preventing pain and injury.
        """)
    
    with st.expander("🔬 Micro-Movements", expanded=False):
        st.markdown("""
        **What it measures:** Small, involuntary movements or tremors during tests.
        
        ⚠️ **Note:** For this metric, **lower scores are better!**
        
        | Score Range | Rating | Meaning |
        |-------------|--------|---------|
        | < 0.10 | 🟢 Excellent | Very minimal micro-movements |
        | 0.10 - 0.20 | ✅ Good | Normal level of small movements |
        | 0.20 - 0.30 | 🟡 Fair | Noticeable tremors or shakiness |
        | > 0.30 | 🟠 Needs Attention | Significant tremors, consult doctor |
        
        **Why it matters:** Excessive micro-movements may indicate essential tremor, anxiety, or neurological conditions.
        """)
    
    with st.expander("📏 Range of Motion", expanded=False):
        st.markdown("""
        **What it measures:** How fully you can move your body during tests.
        
        | Score Range | Rating | Meaning |
        |-------------|--------|---------|
        | ≥ 0.80 | 🟢 Excellent | Full range of motion |
        | 0.60 - 0.79 | ✅ Good | Good flexibility, minor limitations |
        | 0.40 - 0.59 | 🟡 Fair | Limited range, may indicate stiffness |
        | < 0.40 | 🟠 Needs Attention | Very limited, joint issues possible |
        
        **Why it matters:** Good range of motion helps with daily activities and prevents injury.
        """)
    
    # ========================================
    # WHEN TO SEEK HELP
    # ========================================
    st.markdown("---")
    st.markdown("## ⚠️ When to Consult Your Doctor")
    
    st.markdown("""
    <div style='background: #f44336; color: white; padding: 25px; border-radius: 12px; margin: 20px 0;'>
        <h3 style='color: white; margin-top: 0;'>🏥 Seek Medical Advice If:</h3>
        <ul style='font-size: 1.1rem; line-height: 1.8;'>
            <li><b>Multiple scores</b> are in the "Needs Attention" range (below 0.65)</li>
            <li><b>Sudden drop</b> in scores over a few days (from Good/Excellent to Fair/Needs Attention)</li>
            <li>You're experiencing <b>falls or near-falls</b></li>
            <li>You have <b>difficulty with daily activities</b> (walking, climbing stairs, getting up)</li>
            <li>You feel <b>pain or discomfort</b> during movement</li>
            <li>You notice <b>dizziness or lightheadedness</b> when standing</li>
            <li>Any <b>concerns about your mobility</b> or balance</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================
    # POSSIBLE MEDICAL CONDITIONS BY SCORE RANGE
    # ========================================
    st.markdown("---")
    st.markdown("## 🩺 Possible Medical Conditions by Score Range")
    
    st.warning("⚠️ **Disclaimer:** This information is for educational purposes only. Low scores do NOT diagnose any condition. Always consult a healthcare professional for proper evaluation and diagnosis.")
    
    # Movement Speed Conditions
    st.markdown("### 🏃 Low Movement Speed - Possible Conditions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: #fff3e0; padding: 20px; border-radius: 12px; border-left: 5px solid #ff9800;'>
            <h4 style='color: #e65100; margin-top: 0;'>🟡 Fair Range (0.65 - 0.74)</h4>
            <p style='color: #333;'><b>May indicate:</b></p>
            <ul style='color: #555;'>
                <li><b>Mild muscle weakness</b> - Reduced strength in legs/core</li>
                <li><b>Early fatigue</b> - Low energy or tiredness</li>
                <li><b>Mild joint stiffness</b> - Early arthritis signs</li>
                <li><b>Deconditioning</b> - Reduced fitness from inactivity</li>
                <li><b>Medication side effects</b> - Some drugs cause slowness</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: #ffebee; padding: 20px; border-radius: 12px; border-left: 5px solid #f44336;'>
            <h4 style='color: #c62828; margin-top: 0;'>🟠 Needs Attention (Below 0.65)</h4>
            <p style='color: #333;'><b>May indicate:</b></p>
            <ul style='color: #555;'>
                <li><b>Parkinson's Disease</b> - Bradykinesia (slow movement)</li>
                <li><b>Peripheral Neuropathy</b> - Nerve damage affecting movement</li>
                <li><b>Stroke effects</b> - Post-stroke mobility issues</li>
                <li><b>Severe Arthritis</b> - Joint pain limiting movement</li>
                <li><b>Heart/Lung conditions</b> - Reduced oxygen affecting mobility</li>
                <li><b>Frailty Syndrome</b> - Age-related decline</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Stability/Balance Conditions
    st.markdown("### ⚖️ Low Stability/Balance - Possible Conditions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: #fff3e0; padding: 20px; border-radius: 12px; border-left: 5px solid #ff9800;'>
            <h4 style='color: #e65100; margin-top: 0;'>🟡 Fair Range (0.65 - 0.74)</h4>
            <p style='color: #333;'><b>May indicate:</b></p>
            <ul style='color: #555;'>
                <li><b>Inner ear issues</b> - Mild vestibular problems</li>
                <li><b>Core weakness</b> - Weak abdominal/back muscles</li>
                <li><b>Vision problems</b> - Poor depth perception</li>
                <li><b>Mild neuropathy</b> - Reduced sensation in feet</li>
                <li><b>Muscle fatigue</b> - Overexertion or tiredness</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: #ffebee; padding: 20px; border-radius: 12px; border-left: 5px solid #f44336;'>
            <h4 style='color: #c62828; margin-top: 0;'>🟠 Needs Attention (Below 0.65)</h4>
            <p style='color: #333;'><b>May indicate:</b></p>
            <ul style='color: #555;'>
                <li><b>Vertigo/BPPV</b> - Inner ear balance disorder</li>
                <li><b>Cerebellar disorders</b> - Brain coordination issues</li>
                <li><b>Multiple Sclerosis</b> - Nerve damage affecting balance</li>
                <li><b>Stroke effects</b> - Post-stroke balance impairment</li>
                <li><b>Severe neuropathy</b> - Diabetic or other nerve damage</li>
                <li><b>Orthostatic hypotension</b> - Blood pressure drops</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Sit-Stand Speed Conditions
    st.markdown("### 🪑 Low Sit-Stand Speed - Possible Conditions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: #fff3e0; padding: 20px; border-radius: 12px; border-left: 5px solid #ff9800;'>
            <h4 style='color: #e65100; margin-top: 0;'>🟡 Fair Range (0.65 - 0.74)</h4>
            <p style='color: #333;'><b>May indicate:</b></p>
            <ul style='color: #555;'>
                <li><b>Quadriceps weakness</b> - Weak thigh muscles</li>
                <li><b>Mild knee arthritis</b> - Joint pain when rising</li>
                <li><b>Hip stiffness</b> - Limited hip mobility</li>
                <li><b>Lower back pain</b> - Affecting ability to rise</li>
                <li><b>Obesity effects</b> - Extra weight making rising harder</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: #ffebee; padding: 20px; border-radius: 12px; border-left: 5px solid #f44336;'>
            <h4 style='color: #c62828; margin-top: 0;'>🟠 Needs Attention (Below 0.65)</h4>
            <p style='color: #333;'><b>May indicate:</b></p>
            <ul style='color: #555;'>
                <li><b>Sarcopenia</b> - Age-related muscle loss</li>
                <li><b>Severe arthritis</b> - Knee/hip joint damage</li>
                <li><b>Heart failure</b> - Weakness from poor circulation</li>
                <li><b>COPD</b> - Lung disease causing weakness</li>
                <li><b>Myopathy</b> - Muscle disease</li>
                <li><b>Hip/knee replacement needed</b> - Joint deterioration</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Combined Low Scores - Serious Conditions
    st.markdown("### ⚠️ Multiple Low Scores - Serious Conditions to Consider")
    
    st.markdown("""
    <div style='background: #b71c1c; color: white; padding: 25px; border-radius: 12px; margin: 20px 0;'>
        <h4 style='color: white; margin-top: 0;'>🚨 When Multiple Test Scores are Low</h4>
        <p style='color: #ffcdd2;'>If you have low scores in 2 or more tests, this may indicate more serious conditions:</p>
        <table style='width: 100%; color: white; margin-top: 15px;'>
            <tr style='background: rgba(255,255,255,0.1);'>
                <td style='padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.2);'><b>🧠 Neurological Conditions</b></td>
                <td style='padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.2);'>Parkinson's, MS, Stroke, Dementia</td>
            </tr>
            <tr>
                <td style='padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.2);'><b>❤️ Cardiovascular Issues</b></td>
                <td style='padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.2);'>Heart failure, Arrhythmias, Poor circulation</td>
            </tr>
            <tr style='background: rgba(255,255,255,0.1);'>
                <td style='padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.2);'><b>🦴 Musculoskeletal Problems</b></td>
                <td style='padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.2);'>Severe arthritis, Osteoporosis, Spinal stenosis</td>
            </tr>
            <tr>
                <td style='padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.2);'><b>🩺 Metabolic Disorders</b></td>
                <td style='padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.2);'>Uncontrolled diabetes, Thyroid issues, Vitamin deficiencies</td>
            </tr>
            <tr style='background: rgba(255,255,255,0.1);'>
                <td style='padding: 12px;'><b>👴 Age-Related Syndromes</b></td>
                <td style='padding: 12px;'>Frailty syndrome, Sarcopenia, Fall risk syndrome</td>
            </tr>
        </table>
        <p style='color: #ffcdd2; margin-top: 15px; font-weight: bold;'>
            ⚕️ Please consult a doctor immediately if you have multiple low scores!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Score Range Summary Table
    st.markdown("### 📋 Quick Reference: Score Ranges & Health Implications")
    
    st.markdown("""
    <div style='background: #263238; color: white; padding: 25px; border-radius: 12px; margin: 20px 0;'>
        <table style='width: 100%; color: white; border-collapse: collapse;'>
            <tr style='background: #37474f;'>
                <th style='padding: 15px; text-align: left; border-bottom: 2px solid #546e7a;'>Score Range</th>
                <th style='padding: 15px; text-align: left; border-bottom: 2px solid #546e7a;'>Rating</th>
                <th style='padding: 15px; text-align: left; border-bottom: 2px solid #546e7a;'>Health Status</th>
                <th style='padding: 15px; text-align: left; border-bottom: 2px solid #546e7a;'>Action Required</th>
            </tr>
            <tr style='background: #4CAF50;'>
                <td style='padding: 12px;'><b>0.85 - 1.00</b></td>
                <td style='padding: 12px;'>🟢 Excellent</td>
                <td style='padding: 12px;'>Optimal health, no concerns</td>
                <td style='padding: 12px;'>Maintain current lifestyle</td>
            </tr>
            <tr style='background: #8BC34A;'>
                <td style='padding: 12px;'><b>0.75 - 0.84</b></td>
                <td style='padding: 12px;'>✅ Good</td>
                <td style='padding: 12px;'>Healthy, normal function</td>
                <td style='padding: 12px;'>Continue regular monitoring</td>
            </tr>
            <tr style='background: #FF9800; color: #333;'>
                <td style='padding: 12px;'><b>0.65 - 0.74</b></td>
                <td style='padding: 12px;'>🟡 Fair</td>
                <td style='padding: 12px;'>Mild issues possible</td>
                <td style='padding: 12px;'>Increase exercise, monitor closely</td>
            </tr>
            <tr style='background: #f44336;'>
                <td style='padding: 12px;'><b>Below 0.65</b></td>
                <td style='padding: 12px;'>🟠 Needs Attention</td>
                <td style='padding: 12px;'>Potential medical condition</td>
                <td style='padding: 12px;'><b>Consult doctor soon</b></td>
            </tr>
            <tr style='background: #b71c1c;'>
                <td style='padding: 12px;'><b>Below 0.50</b></td>
                <td style='padding: 12px;'>🔴 Critical</td>
                <td style='padding: 12px;'>Significant impairment</td>
                <td style='padding: 12px;'><b>See doctor immediately</b></td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================
    # TIPS FOR BETTER SCORES
    # ========================================
    st.markdown("---")
    st.markdown("## 💪 Tips to Improve Your Scores")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: #1565c0; padding: 20px; border-radius: 12px; height: 280px; color: white;'>
            <h4 style='color: #ffffff; margin-top: 0;'>🚶 Daily Walking</h4>
            <p style='color: #e3f2fd;'>Walk for 15-30 minutes daily to improve:</p>
            <ul style='color: #ffffff;'>
                <li><b>Movement Speed</b></li>
                <li><b>Overall Stability</b></li>
                <li><b>Leg Strength</b></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: #7b1fa2; padding: 20px; border-radius: 12px; height: 280px; color: white;'>
            <h4 style='color: #ffffff; margin-top: 0;'>🧘 Balance Exercises</h4>
            <p style='color: #f3e5f5;'>Practice standing on one foot to improve:</p>
            <ul style='color: #ffffff;'>
                <li><b>Stability Scores</b></li>
                <li><b>Core Strength</b></li>
                <li><b>Fall Prevention</b></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: #2e7d32; padding: 20px; border-radius: 12px; height: 280px; color: white;'>
            <h4 style='color: #ffffff; margin-top: 0;'>🏋️ Strength Training</h4>
            <p style='color: #e8f5e9;'>Light resistance exercises improve:</p>
            <ul style='color: #ffffff;'>
                <li><b>Sit-Stand Speed</b></li>
                <li><b>Movement Efficiency</b></li>
                <li><b>Overall Mobility</b></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================
    # IMPORTANT REMINDERS
    # ========================================
    st.markdown("---")
    st.markdown("## 💡 Important Reminders")
    
    st.info("""
    **🕐 Consistency is Key**  
    Take your health tests at similar times each day for the most accurate comparisons.
    """)
    
    st.info("""
    **📈 Focus on Trends**  
    One bad day doesn't define your health. Look at patterns over several days or weeks.
    """)
    
    st.info("""
    **🌟 Context Matters**  
    Your scores may be affected by sleep quality, stress levels, time of day, and recent physical activity.
    """)
    
    st.warning("""
    **⚕️ Not a Medical Diagnosis**  
    These scores are tools for monitoring and awareness. They are NOT medical diagnoses. 
    Always consult healthcare professionals for medical advice.
    """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #888; padding: 20px;'>
        <p>📖 Health Test Guide | MediGuard Drift AI</p>
        <p>For questions about your results, please consult your healthcare provider.</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    show()
