"""
Context Inputs Page - MediGuard Drift AI
Page for collecting additional user context and health information
"""

import streamlit as st
from auth.supabase_auth import get_supabase_client
from datetime import datetime
import os
from PIL import Image
import io
import base64
import requests
import json
try:
    from pdf2image import convert_from_bytes
except ImportError:
    convert_from_bytes = None


def analyze_health_report_with_gemini(uploaded_file) -> tuple[bool, str, str]:
    """
    Analyze uploaded health report PDF using OpenRouter Vision API
    
    Args:
        uploaded_file: Streamlit uploaded file object
    
    Returns:
        tuple: (success, summary, error_message)
    """
    try:
        # Get Vision API key from environment
        api_key = os.getenv('VISION_API_KEY')
        if not api_key or api_key == 'YOUR_VISION_API_KEY_HERE':
            return False, "", "Vision API key not configured. Please add VISION_API_KEY to your .env file."
        
        # Get Vision model name
        model_name = os.getenv('VISION_MODEL', 'google/gemma-3n-e2b-it:free')
        
        # Read the uploaded file
        file_bytes = uploaded_file.read()
        
        # Check if file is PDF
        if uploaded_file.type == "application/pdf":
            # Convert PDF to images
            if convert_from_bytes is None:
                return False, "", "PDF support not available. Please install pdf2image and poppler."
            
            try:
                images = convert_from_bytes(file_bytes)
                
                # Analyze first page (or all pages if needed)
                image = images[0]
                
                # Create prompt for medical report analysis
                prompt = """
                As a health advisor, analyze this medical report and provide clear, actionable information for the patient:
                
                **IMPORTANT FINDINGS:**
                - What are the key test results and what do they mean?
                - Are there any values outside normal ranges? (Highlight these clearly)
                - What conditions or health issues are identified?
                
                **HEALTH RECOMMENDATIONS:**
                - What immediate actions should the patient take?
                - Are there any lifestyle changes recommended? (diet, exercise, sleep, stress management)
                - What medications or treatments are suggested?
                - When should the patient schedule follow-up appointments?
                - What warning signs should the patient watch for?
                
                **POSITIVE ASPECTS:**
                - What values are in healthy ranges?
                - What aspects of health are good?
                
                **NEXT STEPS:**
                - Clear, prioritized action items for the patient
                - What questions should they ask their doctor?
                
                Use simple, patient-friendly language. Focus on what the patient needs to know and do to maintain or improve their health.
                """
                
                # Convert image to base64 for OpenRouter API
                buffered = io.BytesIO()
                image.save(buffered, format="PNG")
                img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
                
                # Make OpenRouter API request
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": model_name,
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": prompt
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{img_base64}"
                                    }
                                }
                            ]
                        }
                    ]
                }
                
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    summary = result['choices'][0]['message']['content']
                    return True, summary, ""
                else:
                    error_data = response.json() if response.text else {}
                    error_msg = error_data.get('error', {}).get('message', response.text)
                    return False, "", f"API Error ({response.status_code}): {error_msg}"
                
            except Exception as e:
                return False, "", f"Error processing PDF: {str(e)}"
        
        elif uploaded_file.type in ["image/jpeg", "image/jpg", "image/png"]:
            # Handle direct image upload
            image = Image.open(io.BytesIO(file_bytes))
            
            prompt = """
            As a health advisor, analyze this medical report and provide clear, actionable information for the patient:
            
            **IMPORTANT FINDINGS:**
            - What are the key test results and what do they mean?
            - Are there any values outside normal ranges? (Highlight these clearly)
            - What conditions or health issues are identified?
            
            **HEALTH RECOMMENDATIONS:**
            - What immediate actions should the patient take?
            - Are there any lifestyle changes recommended? (diet, exercise, sleep, stress management)
            - What medications or treatments are suggested?
            - When should the patient schedule follow-up appointments?
            - What warning signs should the patient watch for?
            
            **POSITIVE ASPECTS:**
            - What values are in healthy ranges?
            - What aspects of health are good?
            
            **NEXT STEPS:**
            - Clear, prioritized action items for the patient
            - What questions should they ask their doctor?
            
            Use simple, patient-friendly language. Focus on what the patient needs to know and do to maintain or improve their health.
            """
            
            # Convert image to base64 for OpenRouter API
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
            # Make OpenRouter API request
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": model_name,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{img_base64}"
                                }
                            }
                        ]
                    }
                ]
            }
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                summary = result['choices'][0]['message']['content']
                return True, summary, ""
            else:
                error_data = response.json() if response.text else {}
                error_msg = error_data.get('error', {}).get('message', response.text)
                return False, "", f"API Error ({response.status_code}): {error_msg}"
        
        else:
            return False, "", "Unsupported file type. Please upload PDF or image files (JPEG, PNG)."
            
    except Exception as e:
        return False, "", f"Error analyzing report: {str(e)}"


def extract_key_points_from_analysis(analysis_text: str) -> dict:
    """
    Extract key points from AI analysis of health report
    
    Args:
        analysis_text (str): Full AI analysis text
    
    Returns:
        dict: Extracted key findings, recommendations, and risk indicators
    """
    key_data = {
        'key_findings': '',
        'health_recommendations': '',
        'abnormal_values': '',
        'positive_aspects': '',
        'next_steps': ''
    }
    
    if not analysis_text:
        return key_data
    
    try:
        # Split analysis into sections
        sections = analysis_text.split('**')
        
        for i, section in enumerate(sections):
            section_lower = section.lower()
            
            # Extract important findings
            if 'important finding' in section_lower or 'key finding' in section_lower:
                if i + 1 < len(sections):
                    key_data['key_findings'] = sections[i + 1].strip()[:500]
            
            # Extract health recommendations
            elif 'health recommendation' in section_lower or 'recommendation' in section_lower:
                if i + 1 < len(sections):
                    key_data['health_recommendations'] = sections[i + 1].strip()[:500]
            
            # Extract abnormal values
            elif 'abnormal' in section_lower or 'outside normal' in section_lower:
                if i + 1 < len(sections):
                    key_data['abnormal_values'] = sections[i + 1].strip()[:300]
            
            # Extract positive aspects
            elif 'positive aspect' in section_lower:
                if i + 1 < len(sections):
                    key_data['positive_aspects'] = sections[i + 1].strip()[:300]
            
            # Extract next steps
            elif 'next step' in section_lower:
                if i + 1 < len(sections):
                    key_data['next_steps'] = sections[i + 1].strip()[:300]
        
        return key_data
        
    except Exception as e:
        print(f"Error extracting key points: {e}")
        return key_data


def save_context_to_supabase(user_id: str, context_data: dict, update_only_ai_fields: bool = False) -> tuple[bool, str]:
    """
    Save user context data to Supabase
    
    Args:
        user_id (str): User's unique ID
        context_data (dict): Context data to save
        update_only_ai_fields (bool): If True, only update AI analysis fields without touching other columns
    
    Returns:
        tuple: (success, message)
    """
    try:
        supabase = get_supabase_client()
        
        if not supabase:
            return False, "Database connection not configured."
        
        if update_only_ai_fields:
            # Only update AI analysis fields, preserve existing data
            # First check if record exists
            existing = supabase.table('user_context_data').select('*').eq('user_id', user_id).execute()
            
            if existing.data and len(existing.data) > 0:
                # Update existing record with only AI fields
                update_data = {
                    "ai_key_findings": context_data.get('ai_key_findings', ''),
                    "ai_health_recommendations": context_data.get('ai_health_recommendations', ''),
                    "ai_abnormal_values": context_data.get('ai_abnormal_values', ''),
                    "ai_positive_aspects": context_data.get('ai_positive_aspects', ''),
                    "ai_next_steps": context_data.get('ai_next_steps', ''),
                    "updated_at": datetime.now().isoformat()
                }
                response = supabase.table('user_context_data').update(update_data).eq('user_id', user_id).execute()
            else:
                # Create new record with AI fields only
                data = {
                    "user_id": user_id,
                    "medical_summary": '',
                    "known_conditions": '',
                    "report_summary": '',
                    "sleep_hours": 7,
                    "stress_level": 'Medium',
                    "workload": 'Moderate',
                    "activity_level": 'Moderate',
                    "ai_key_findings": context_data.get('ai_key_findings', ''),
                    "ai_health_recommendations": context_data.get('ai_health_recommendations', ''),
                    "ai_abnormal_values": context_data.get('ai_abnormal_values', ''),
                    "ai_positive_aspects": context_data.get('ai_positive_aspects', ''),
                    "ai_next_steps": context_data.get('ai_next_steps', ''),
                    "created_at": datetime.now().isoformat()
                }
                response = supabase.table('user_context_data').insert(data).execute()
        else:
            # Full upsert with all fields
            data = {
                "user_id": user_id,
                "medical_summary": context_data.get('medical_summary', ''),
                "known_conditions": context_data.get('known_conditions', ''),
                "report_summary": context_data.get('report_summary', ''),
                "sleep_hours": context_data.get('sleep_hours', 7),
                "stress_level": context_data.get('stress_level', 'Medium'),
                "workload": context_data.get('workload', 'Moderate'),
                "activity_level": context_data.get('activity_level', 'Moderate'),
                "ai_key_findings": context_data.get('ai_key_findings', ''),
                "ai_health_recommendations": context_data.get('ai_health_recommendations', ''),
                "ai_abnormal_values": context_data.get('ai_abnormal_values', ''),
                "ai_positive_aspects": context_data.get('ai_positive_aspects', ''),
                "ai_next_steps": context_data.get('ai_next_steps', ''),
                "created_at": datetime.now().isoformat()
            }
            
            # Insert or update context data
            response = supabase.table('user_context_data').upsert(data, on_conflict='user_id').execute()
        
        return True, "Context data saved successfully!"
        
    except Exception as e:
        return False, f"Error saving data: {str(e)}"


def load_existing_context(user_id: str) -> dict:
    """
    Load existing context data for a user from Supabase
    
    Args:
        user_id (str): User's unique ID
    
    Returns:
        dict: Existing context data or empty dict if none found
    """
    try:
        supabase = get_supabase_client()
        
        if not supabase:
            return {}
        
        response = supabase.table('user_context_data').select('*').eq('user_id', user_id).execute()
        
        if response.data and len(response.data) > 0:
            data = response.data[0]
            return {
                'medical_summary': data.get('medical_summary', ''),
                'known_conditions': data.get('known_conditions', ''),
                'report_summary': data.get('report_summary', ''),
                'sleep_hours': data.get('sleep_hours', 7.0),
                'stress_level': data.get('stress_level', 'Medium'),
                'workload': data.get('workload', 'Moderate'),
                'activity_level': data.get('activity_level', 'Moderate'),
                'ai_key_findings': data.get('ai_key_findings', ''),
                'ai_health_recommendations': data.get('ai_health_recommendations', ''),
                'ai_abnormal_values': data.get('ai_abnormal_values', ''),
                'ai_positive_aspects': data.get('ai_positive_aspects', ''),
                'ai_next_steps': data.get('ai_next_steps', ''),
                'created_at': data.get('created_at'),
                'updated_at': data.get('updated_at')
            }
        return {}
        
    except Exception as e:
        st.error(f"Error loading existing data: {str(e)}")
        return {}


def show():
    """
    Display the context inputs page
    """
    
    # ========================================
    # PAGE HEADER
    # ========================================
    st.markdown("""
        <div style='text-align: center; padding: 1.5rem 0;'>
            <h1 style='color: #4A90E2; font-size: 2.5rem;'>📝 Health Context</h1>
            <p style='font-size: 1.1rem; color: #666;'>
                Provide additional context for personalized health insights
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========================================
    # LOAD EXISTING DATA
    # ========================================
    user_id = st.session_state.get('user_id')
    
    if not user_id:
        st.error("❌ User not authenticated. Please log in.")
        return
    
    existing_data = load_existing_context(user_id)
    
    # Show existing data summary if available
    has_medical_data = existing_data and (existing_data.get('medical_summary') or existing_data.get('known_conditions'))
    has_ai_data = existing_data and (existing_data.get('ai_key_findings') or 
                                      existing_data.get('ai_health_recommendations') or 
                                      existing_data.get('ai_abnormal_values'))
    
    if has_medical_data or has_ai_data:
        with st.expander("📄 **Your Current Context Data** (Click to view)", expanded=False):
            
            # Only show medical/lifestyle columns if there's medical data
            if has_medical_data:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**🏥 Medical Information:**")
                    if existing_data.get('medical_summary'):
                        st.write(f"Medical History: {existing_data['medical_summary'][:100]}...")
                    if existing_data.get('known_conditions'):
                        st.write(f"Known Conditions: {existing_data['known_conditions'][:100]}...")
                    if existing_data.get('report_summary'):
                        st.write(f"Recent Reports: {existing_data['report_summary'][:100]}...")
                
                with col2:
                    st.markdown("**🌟 Lifestyle Factors:**")
                    st.write(f"Sleep Hours: {existing_data.get('sleep_hours', 7)} hours/night")
                    st.write(f"Stress Level: {existing_data.get('stress_level', 'medium').title()}")
                    st.write(f"Workload: {existing_data.get('workload', 'moderate').title()}")
                    st.write(f"Activity Level: {existing_data.get('activity_level', 'moderate').title()}")
                
                if has_ai_data:
                    st.markdown("---")
            
            # Show AI Analysis if available
            if has_ai_data:
                st.markdown("**🤖 AI-Extracted Report Analysis:**")
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    if existing_data.get('ai_key_findings'):
                        st.markdown("🔍 **Key Findings:**")
                        st.caption(existing_data['ai_key_findings'][:150] + "..." if len(existing_data['ai_key_findings']) > 150 else existing_data['ai_key_findings'])
                    
                    if existing_data.get('ai_abnormal_values'):
                        st.markdown("⚠️ **Abnormal Values:**")
                        st.caption(existing_data['ai_abnormal_values'][:150] + "..." if len(existing_data['ai_abnormal_values']) > 150 else existing_data['ai_abnormal_values'])
                    
                    if existing_data.get('ai_positive_aspects'):
                        st.markdown("✅ **Positive Aspects:**")
                        st.caption(existing_data['ai_positive_aspects'][:150] + "..." if len(existing_data['ai_positive_aspects']) > 150 else existing_data['ai_positive_aspects'])
                
                with col_b:
                    if existing_data.get('ai_health_recommendations'):
                        st.markdown("💊 **Recommendations:**")
                        st.caption(existing_data['ai_health_recommendations'][:150] + "..." if len(existing_data['ai_health_recommendations']) > 150 else existing_data['ai_health_recommendations'])
                    
                    if existing_data.get('ai_next_steps'):
                        st.markdown("📝 **Next Steps:**")
                        st.caption(existing_data['ai_next_steps'][:150] + "..." if len(existing_data['ai_next_steps']) > 150 else existing_data['ai_next_steps'])
            
            if existing_data.get('updated_at'):
                st.caption(f"Last updated: {existing_data['updated_at']}")
        
        st.info("💡 **Tip:** Fill in the form below to update your context information.")
    
    # ========================================
    # PRIVACY NOTICE
    # ========================================
    st.info("""
    🔒 **Privacy Notice**
    
    The information you provide here helps our AI provide more personalized insights. 
    All data is encrypted and stored securely. You can update or delete this information 
    anytime. This data is for monitoring purposes only—not for diagnosis or treatment.
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ========================================
    # PDF UPLOAD SECTION (OUTSIDE FORM)
    # ========================================
    st.markdown("### 📄 Upload Health Reports")
    st.info("💡 Upload your medical reports, lab results, or health documents for AI-powered analysis using Google Gemini Vision")
    
    uploaded_file = st.file_uploader(
        "Choose a PDF or image file",
        type=["pdf", "jpg", "jpeg", "png"],
        help="Upload medical reports, lab results, or health documents for analysis",
        key="health_report_upload"
    )
    
    # Initialize session state for analysis result
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = ""
    
    if uploaded_file is not None:
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔍 Analyze with Gemini Vision", type="primary", use_container_width=True):
                with st.spinner("🤖 Analyzing health report with AI Vision..."):
                    success, summary, error = analyze_health_report_with_gemini(uploaded_file)
                    
                    if success:
                        st.session_state.analysis_result = summary
                        
                        # Extract key points and save to database
                        key_points = extract_key_points_from_analysis(summary)
                        
                        context_data = {
                            'ai_key_findings': key_points['key_findings'],
                            'ai_health_recommendations': key_points['health_recommendations'],
                            'ai_abnormal_values': key_points['abnormal_values'],
                            'ai_positive_aspects': key_points['positive_aspects'],
                            'ai_next_steps': key_points['next_steps']
                        }
                        
                        # Save extracted points to Supabase
                        save_success, save_msg = save_context_to_supabase(user_id, context_data, update_only_ai_fields=True)
                        
                        st.success("✅ Analysis complete and key points saved!")
                        if not save_success:
                            st.warning(f"⚠️ Analysis saved locally but database update failed: {save_msg}")
                        st.rerun()
                    else:
                        st.error(f"❌ {error}")
        
        # Display analysis result if available
        if st.session_state.analysis_result:
            st.markdown("---")
            st.markdown("#### 📊 AI Analysis Results:")
            st.markdown(st.session_state.analysis_result)
            st.info("💡 You can copy this analysis and add it to your Report Summary in the form below")
            
            if st.button("🗑️ Clear Analysis", type="secondary"):
                st.session_state.analysis_result = ""
                st.rerun()
    
    st.markdown("---")
    
    # ========================================
    # CONTEXT INPUT FORM
    # ========================================
    st.markdown("### 📋 Health & Lifestyle Context")
    
    with st.form("context_form", clear_on_submit=False):
        
        # Medical History Section
        st.markdown("#### 🏥 Medical Background")
        st.caption("Provide a brief summary to help contextualize your health patterns")
        
        medical_summary = st.text_area(
            "Medical Summary",
            value=existing_data.get('medical_summary', ''),
            placeholder="Brief summary of relevant medical history...",
            height=100,
            help="Optional: General medical background that might be relevant to health monitoring"
        )
        
        known_conditions = st.text_area(
            "Known Conditions",
            value=existing_data.get('known_conditions', ''),
            placeholder="Any conditions you're currently managing or monitoring...",
            height=80,
            help="Optional: Conditions you're aware of"
        )
        
        report_summary = st.text_area(
            "Report Summary",
            value=existing_data.get('report_summary', ''),
            placeholder="Summary of recent checkups or test results...",
            height=100,
            help="Optional: Brief notes from recent visits or test results"
        )
        
        st.markdown("---")
        
        # Lifestyle Factors Section
        st.markdown("#### 🌟 Daily Lifestyle Factors")
        st.caption("These factors help us understand patterns in your health data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            sleep_hours = st.number_input(
                "Average Sleep Hours per Night",
                min_value=0.0,
                max_value=12.0,
                value=float(existing_data.get('sleep_hours', 7.0)),
                step=0.5,
                help="Typical number of hours you sleep each night"
            )
            
            # Get stress level index
            stress_options = ["Low", "Medium", "High"]
            current_stress = existing_data.get('stress_level', 'Medium')
            stress_index = stress_options.index(current_stress) if current_stress in stress_options else 1
            
            stress_level = st.selectbox(
                "Stress Level",
                options=stress_options,
                index=stress_index,
                help="Your general stress level over the past week"
            )
            
        with col2:
            # Get workload index
            workload_options = ["Light", "Moderate", "Heavy"]
            current_workload = existing_data.get('workload', 'Moderate')
            workload_index = workload_options.index(current_workload) if current_workload in workload_options else 1
            
            workload = st.selectbox(
                "Workload",
                options=workload_options,
                index=workload_index,
                help="How demanding is your current work or study schedule?"
            )
            
            # Get activity level index
            activity_options = ["Sedentary", "Moderate", "Active"]
            current_activity = existing_data.get('activity_level', 'Moderate')
            activity_index = activity_options.index(current_activity) if current_activity in activity_options else 1
            
            activity_level = st.selectbox(
                "Activity Level",
                options=activity_options,
                index=activity_index,
                help="Your typical level of physical activity throughout the day"
            )
        
        st.markdown("---")
        
        # Submit Button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submit_button = st.form_submit_button(
                "💾 Save / Update",
                type="primary",
                use_container_width=True
            )
        
        # Handle form submission
        if submit_button:
            # Get user ID from session state
            user_id = st.session_state.get('user_id')
            
            if not user_id:
                st.error("❌ User not authenticated. Please log in again.")
            else:
                # Prepare context data
                context_data = {
                    'medical_summary': medical_summary,
                    'known_conditions': known_conditions,
                    'report_summary': report_summary,
                    'sleep_hours': sleep_hours,
                    'stress_level': stress_level,
                    'workload': workload,
                    'activity_level': activity_level
                }
                
                # Save to Supabase
                with st.spinner("Saving your context data..."):
                    success, message = save_context_to_supabase(user_id, context_data)
                    
                    if success:
                        st.success(f"✅ {message}")
                        st.balloons()
                    else:
                        st.error(f"❌ {message}")
    
    st.markdown("---")
    
    # ========================================
    # INFORMATION SECTION
    # ========================================
    st.markdown("### 💡 Why We Collect This Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🎯 Personalization**
        
        Your context helps our AI understand YOUR unique health baseline 
        and provide insights tailored to your specific situation.
        """)
    
    with col2:
        st.markdown("""
        **📊 Better Analysis**
        
        Lifestyle factors like sleep and stress significantly affect health metrics. 
        This context improves drift detection accuracy.
        """)
    
    with col3:
        st.markdown("""
        **🔐 Your Control**
        
        You own this data. Update it anytime, and it stays private and encrypted. 
        We never share without your explicit permission.
        """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ========================================
    # IMPORTANT REMINDERS
    # ========================================
    st.warning("""
    ⚠️ **Important Reminders**
    
    - This information is for health monitoring context only
    - Do NOT use this as a replacement for medical records or consultations
    - Always discuss health concerns with qualified healthcare professionals
    - We do not store or analyze actual medical documents—only your summaries
    - This data helps AI provide insights but does NOT diagnose conditions
    """)
    
    st.markdown("---")
    
    # ========================================
    # DATA MANAGEMENT
    # ========================================
    st.markdown("### ⚙️ Manage Your Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Update Context", use_container_width=True):
            st.info("Fill in the form above with updated information and click 'Save Context'")
    
    with col2:
        if st.button("🗑️ Clear All Context", use_container_width=True, type="secondary"):
            st.warning("This feature will be available soon. Contact support if you need to delete your data.")
